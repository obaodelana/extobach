import os
from praw import Reddit
from praw.reddit import Comment
import datetime
import calendar
import random
from concurrent import futures

from .retriever import Retriever


class RedditRetriever(Retriever):
    def __init__(self, product_name: str, release_date: int) -> None:
        super().__init__(product_name, release_date)

        self._client_id = os.getenv("REDDIT_CLIENT_ID")
        self._client_secret = os.getenv("REDDIT_CLIENT_SECRET")
        self._user_agent = os.getenv("REDDIT_USER_AGENT")

        assert self._client_id and self._client_secret and self._user_agent, \
            "Missing Reddit API credentials"

    def _get_thread(self, year: int) -> list[dict]:
        assert type(year) is int

        reddit = Reddit(
            client_id=self._client_id,
            client_secret=self._client_secret,
            user_agent=self._user_agent
        )

        # Retrieve start of the year and end of the year as unix epochs (Number of seconds since 1970)
        # calendar.timegm() assumes time tuple is in UTC without applying any timezone effect. (Creates consistency accross different timezones)
        start_epoch = int(calendar.timegm(
            datetime.datetime(year, 1, 1).timetuple()))
        end_epoch = int(calendar.timegm(datetime.datetime(
            year, 12, 31, 23, 59, 59).timetuple()))

        # Search posts from all subreddits that includes product name

        query = f'title:{self.product_name} OR selftext:{self.product_name}'

        submissions = list(reddit.subreddit('all').search(
            query=query,
            # Sort by relevance not by 'new' (New pulls most recent posts which come from 2025)
            sort='relevance',
            syntax='lucene',
            time_filter='all',
            # Larger pool of posts to sample from to potentially include older posts
            limit=500
        ))

        # Filter submissions that were published within the year (PRAW doesn't support date range filtering directly :C)
        filtered_submissions = [s for s in submissions
                                if start_epoch <= s.created_utc <= end_epoch]

        # Select exactly 10 random submissions given there are more than 10 submissions. If not, select all submissions.
        sampled_submissions = random.sample(
            filtered_submissions, min(10, len(filtered_submissions)))

        thread = []
        for submission in sampled_submissions:
            # Loads "5 batches" of additional comments
            submission.comments.replace_more(limit=5)
            # Selects up to the first 100
            comments: list[Comment] = submission.comments.list()[
                :100]  # type: ignore

            # Retrieve comment data
            comment_data = [{
                'author': comment.author.name if comment.author else 'deleted',
                'text': comment.body,
                'publishedAt': datetime.datetime.fromtimestamp(comment.created_utc, tz=datetime.timezone.utc).isoformat().replace('+00:00', 'Z')
            } for comment in comments]

            # Append the post data
            thread.append({
                'postId': submission.id,
                'title': submission.title,
                'subreddit': submission.subreddit.display_name,
                'publishedAt': datetime.datetime.fromtimestamp(submission.created_utc, tz=datetime.timezone.utc).isoformat().replace('+00:00', 'Z'),
                'score': submission.score,
                'numComments': submission.num_comments,
                'topComments': comment_data
            })

        return thread

    def retrieve(self) -> dict:
        all_posts = {}

        current_year = datetime.datetime.now().year
        # Run concurrently
        with futures.ThreadPoolExecutor(max_workers=6) as exec:
            futures_reddit = {
                exec.submit(self._get_thread, year): year
                # From 5 years ago till now (or from release date)
                for year in range(max(self.release_date, current_year - 4), current_year + 1)
            }

            for future in futures.as_completed(futures_reddit):
                year = futures_reddit[future]
                try:
                    reddit = future.result()
                    all_posts[year] = reddit
                except Exception:
                    print("Failed to get posts in", year)

        return all_posts
