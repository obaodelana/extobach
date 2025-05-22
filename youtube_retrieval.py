# Youtube API Retrieval System

from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
from googleapiclient.discovery import build

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
        search_response = youtube.search().list(
            q = product_name,
            part = 'id,snippet',
            type = 'video',
            maxResults = 1 #Can increase if needed
        ).execute()

        if not search_response['items']:
            return jsonify({'error': 'No video found for this product.'}), 404
    

        video_id = search_response['items'][0]['id']['videoId']
        video_title = search_response['items'][0]['snippet']['title']

        #Retrieve statistics (views, likes, comments included)
        video_response = youtube.videos().list(
            part='statistics',
            id=video_id
        ).execute()

        stats = video_response['items'][0]['statistics']

        #Retrieve comments
        comments_response = youtube.commentThreads().list(
            part='snippet',
            videoId=video_id,
            maxResults=20,
            textFormat='plainText'
        ).execute()

        comments = [
            {
                'author': item['snippet']['topLevelComment']['snippet']['authorDisplayName'],
                'text': item['snippet']['topLevelComment']['snippet']['textDisplay'],
                'publishedAt': item['snippet']['topLevelComment']['snippet']['publishedAt']
            }
            for item in comments_response.get('items', [])
        ]

        #Return structured JSON
        return jsonify({
            'videoId': video_id,
            'title': video_title,
            'statistics': {
                'views': stats.get('viewCount', 'N/A'),
                'likes': stats.get('likeCount', 'N/A'),
                'comments': stats.get('commentCount', 'N/A')
            },
            'topComments': comments
        })


    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug = True)






