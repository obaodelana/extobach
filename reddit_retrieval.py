from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
import praw
import datetime
import calendar
import random

load_dotenv()

client_id = os.getenv("REDDIT_CLIENT_ID")
client_secret = os.getenv("REDDIT_CLIENT_SECRET")
user_agent = os.getenv("REDDIT_USER_AGENT")

assert client_id and client_secret and user_agent, "Missing Reddit API credentials"

reddit = praw.Reddit(
    client_id = client_id,
    client_secret=client_secret,
    user_agent=user_agent
)

app = Flask(__name__)

@app.route('/api/reddit', methods=['POST'])

def get_reddit_data():
    data = request.get_json()
    product_name = data.get('productName')

    if not product_name:
        return jsonify({'error': 'productName is required'}), 400
    
    try:
        current_year = datetime.datetime.now().year
        all_posts = []

        #From 5 years ago till now
        for year in range(current_year - 5, current_year + 1):
            #Retrieve start of the year and end of the year as unix epochs (Number of seconds since 1970)
            #calendar.timegm() assumes time tuple is in UTC without applying any timezone effect. (Creates consistency accross different timezones)
            start_epoch = int(calendar.timegm(datetime.datetime(year, 1, 1).timetuple())) 
            end_epoch = int(calendar.timegm(datetime.datetime(year, 12, 31, 23, 59, 59).timetuple()))

            #Search posts from all subreddits that includes product name

            query = f'title:{product_name} OR selftext:{product_name}'

            submissions = list(reddit.subreddit('all').search(
                query = query,
                #Sort by relevance not by 'new' (New pulls most recent posts which come from 2025)
                sort = 'relevance',
                syntax = 'lucene',
                time_filter = 'all',
                #Larger pool of posts to sample from to potentially include older posts
                limit = 500
            ))

            #Filter submissions that were published within the year (PRAW doesn't support date range filtering directly :C)
            filtered_submissions = [s for s in submissions if start_epoch <= s.created_utc <= end_epoch]

            #Select exactly 10 random submissions given there are more than 10 submissions. If not, select all submissions.
            sampled_submissions = random.sample(filtered_submissions, min(10, len(filtered_submissions)))

            for submission in sampled_submissions:
                #Loads "5 batches" of additional comments
                submission.comments.replace_more(limit=5)
                #Selects up to the first 100
                comments = submission.comments.list()[:100]
            
            #Retrieve comment data
            comment_data = [{
                'author': comment.author.name if comment.author else 'deleted',
                'text': comment.body,
                'publishedAt': datetime.datetime.fromtimestamp(comment.created_utc, tz=datetime.timezone.utc).isoformat().replace('+00:00', 'Z')
            } for comment in comments]

            #Append the post data
            all_posts.append({
                'postId': submission.id,
                'title': submission.title,
                'subreddit': submission.subreddit.display_name,
                'publishedAt': datetime.datetime.fromtimestamp(submission.created_utc, tz=datetime.timezone.utc).isoformat().replace('+00:00', 'Z'),
                'score': submission.score,
                'numComments': submission.num_comments,
                'topComments': comment_data
            })

        return jsonify({'posts': all_posts})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)




