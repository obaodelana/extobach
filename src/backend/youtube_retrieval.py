# Youtube API Retrieval System

from flask import Blueprint, request
import os
from googleapiclient.discovery import build
from datetime import datetime
import random

api_key = os.getenv('YOUTUBE_API_KEY', None)
assert api_key is not None, "API key not found. Please set the YOUTUBE_API_KEY environment variable."

youtube = build(
    'youtube',
    'v3',
    developerKey=api_key
)

# Initialize Flask app
yt_bp = Blueprint("youtube", __name__, url_prefix="/youtube")


@yt_bp.post("")
def get_youtube_data():
    data = request.get_json()
    product_name = data.get('productName')

    if not product_name:
        return {'error': 'productName is required'}, 400

    try:
        current_year = datetime.now().year

        all_videos = []
        for year in range(current_year - 5, current_year + 1):
            print(f"Checking year {year}")

            start_date = f"{year}-01-01T00:00:00Z"
            end_date = f"{year}-12-31T23:59:59Z"

            # Search for videos
            search_response = youtube.search().list(
                q=product_name,
                part='id,snippet',
                type='video',
                publishedAfter=start_date,
                publishedBefore=end_date,
                maxResults=25  # Increase pool for randomness
            ).execute()

            items = search_response.get('items', [])
            if not items:
                continue
            else:
                print(f"Found {len(items)} videos")

            sampled_videos = random.sample(items, min(5, len(items)))
            # For each video
            for item in sampled_videos:
                video_id = item['id']['videoId']
                video_title = item['snippet']['title']
                video_published = item['snippet']['publishedAt']

                print(f"Looking at comments of video '{video_title}'...")

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
                    print(f"Got {len(retrieved_comments)} comments")
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
                        print("No more comments to look at")
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
                print("Added new video to list")
                print("-"*20)
                print()

        return {'videos': all_videos}

    except Exception as e:
        return {'error': str(e)}, 500
