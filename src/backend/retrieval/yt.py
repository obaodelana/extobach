import os
from googleapiclient.discovery import build
from datetime import datetime
import random
from concurrent import futures

from .retriever import Retriever


class YTRetriever(Retriever):
    def __init__(self,
                 product_name: str,
                 release_date: int) -> None:
        super().__init__(product_name, release_date)

        self._api_key = os.getenv('YOUTUBE_API_KEY', None)
        assert self._api_key is not None, "API key not found. Please set the YOUTUBE_API_KEY environment variable."

    def retrieve(self) -> dict:
        all_videos = {}

        # Get videos for each year concurrently
        with futures.ThreadPoolExecutor(max_workers=6) as exec:
            current_year = datetime.now().year
            # Start a new thread for each year
            future_yt = {
                exec.submit(self.get_videos, year): year
                for year in range(
                    # Release data or five years before current date (whichever is closer)
                    max(self.release_date, current_year-5+1),
                    current_year + 1)  # Up to current year
            }

            for future in futures.as_completed(future_yt):
                year = future_yt[future]
                try:
                    videos = future.result()
                    all_videos[year] = videos
                except Exception as exec:
                    print("Failed to get videos in", year)
                else:
                    print("Got videos in", year)
                    print("-"*20)
                    print()

        return all_videos

    def get_video(self, dct: dict, year: int, youtube) -> dict:
        assert type(dct) is dict
        assert type(year) is int and year > 0
        assert youtube is not None

        video_id = dct['id']['videoId']
        video_title = dct['snippet']['title']
        video_published = dct['snippet']['publishedAt']

        # Retrieve statistics of that particular video
        video_response = youtube.videos().list(
            part='statistics',
            id=video_id
        ).execute()

        stats = video_response['items'][0]['statistics']

        # Retrieve comments

        comment_threads = []
        next_page_token = None
        comments_year_limit = f"{year}-12-31T23:59:59Z"

        # Get up to 10 comments
        while len(comment_threads) < 10:
            comment_response = youtube.commentThreads().list(
                part='snippet',
                videoId=video_id,
                maxResults=50,
                pageToken=next_page_token,
                textFormat='plainText',
                order='time'
            ).execute()
            retrieved_comments = comment_response.get('items', [])

            print(
                f"Got {len(retrieved_comments)} comments of '{video_title}' ({year})")

            for item in retrieved_comments:
                comment = item['snippet']['topLevelComment']['snippet']
                comment_date = comment['publishedAt']
                if comment_date <= comments_year_limit:
                    print("Added comment to list")
                    comment_threads.append({
                        'author': comment['authorDisplayName'],
                        'text': comment['textDisplay'],
                        'publishedAt': comment_date
                    })

            next_page_token = comment_response.get('nextPageToken')
            # If no more comments left, then exit loop
            if not next_page_token:
                print(f"No more comments for {video_title} ({year})")
                break

        return {
            'videoId': video_id,
            'title': video_title,
            'publishedAt': video_published,
            'statistics': {
                'views': stats.get('viewCount', 'N/A'),
                'likes': stats.get('likeCount', 'N/A'),
                'comments': stats.get('commentCount', 'N/A')
            },
            'topComments': comment_threads
        }

    def get_videos(self, year: int) -> list[dict]:
        assert type(year) is int and year > 0

        youtube = build('youtube', 'v3', developerKey=self._api_key)

        start_date = f"{year}-01-01T00:00:00Z"
        end_date = f"{year}-12-31T23:59:59Z"

        # Search for videos
        search_response = youtube.search().list(
            q=self.product_name,
            part='id,snippet',
            type='video',
            publishedAfter=start_date,
            publishedBefore=end_date,
            maxResults=20  # Increase pool for randomness
        ).execute()

        items = search_response.get('items', [])
        if len(items) == 0:
            return []

        videos = []

        # Randomly select 5 videos
        sampled_videos = random.sample(items, min(5, len(items)))
        for item in sampled_videos:
            videos.append(self.get_video(item, year, youtube))

        return videos
