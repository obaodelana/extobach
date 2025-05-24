# Youtube API Retrieval System

from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
from googleapiclient.discovery import build
import datetime
import random

load_dotenv()
api_key = os.getenv('YOUTUBE_API_KEY', None)
assert api_key is not None, "API key not found. Please set the YOUTUBE_API_KEY environment variable."

youtube = build(
    'youtube',
    'v3',
    developerKey = api_key
)

#Initialize Flask app
app = Flask(__name__)

@app.route('/api/youtube', methods=['POST'])

def get_youtube_data():
    data = request.get_json
    product_name = data.get('productName')

    if not product_name:
        return jsonify({'error': 'productName is required'}), 400
    
    try:

        current_year = datetime.datetime.now().year
        all_videos = []

        for year in range(current_year - 5 + 1, current_year + 1):
            start_date = f"{year}-01-01T00:00:00Z"
            end_date = f"{year}-12-31T23:59:59Z"

            search_response = youtube.search().list(
                q=product_name,
                part='id,snippet',
                type='video',
                publishedAfter=start_date,
                publishedBefore=end_date,
                maxResults=50  # Increase pool for randomness
            ).execute()

            items = search_response.get('items', [])
            if not items:
                continue

            sampled_videos = random.sample(items, min(10, len(items)))

            for item in sampled_videos:
                video_id = item['id']['videoId']
                video_title = item['snippet']['title']
                video_published = item['snippet']['publishedAt']

                # Retrieve statistics
                video_response = youtube.videos().list(
                    part='statistics',
                    id=video_id
                ).execute()

                stats = video_response['items'][0]['statistics']

                # Retrieve up to 100 comments
                comment_threads = []
                next_page_token = None
                comments_year_limit = f"{year}-12-31T23:59:59Z"

                while len(comment_threads) < 100:
                    comment_response = youtube.commentThreads().list(
                        part='snippet',
                        videoId=video_id,
                        maxResults=min(100 - len(comment_threads), 50),
                        pageToken=next_page_token,
                        textFormat='plainText',
                        order='time'
                    ).execute()

                    for item in comment_response.get('items', []):
                        comment = item['snippet']['topLevelComment']['snippet']
                        comment_date = comment['publishedAt']
                        if comment_date <= comments_year_limit:
                            comment_threads.append({
                                'author': comment['authorDisplayName'],
                                'text': comment['textDisplay'],
                                'publishedAt': comment_date
                            })

                    next_page_token = comment_response.get('nextPageToken')
                    if not next_page_token:
                        break

                all_videos.append({
                    'videoId': video_id,
                    'title': video_title,
                    'publishedAt': video_published,
                    'statistics': {
                        'views': stats.get('viewCount', 'N/A'),
                        'likes': stats.get('likeCount', 'N/A'),
                        'comments': stats.get('commentCount', 'N/A')
                    },
                    'topComments': comment_threads
                })

        return jsonify({'videos': all_videos})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug = True)






