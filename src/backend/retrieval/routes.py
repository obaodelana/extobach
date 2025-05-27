from flask import Blueprint, request

from .yt import YTRetriever
from .reddit import RedditRetriever

retrieval_bp = Blueprint("retrieval", __name__, url_prefix="/retrieve")


@retrieval_bp.post("/yt")
def get_youtube_data():
    data = request.get_json()

    product_name = data.get('productName')
    release_date = data.get('releaseDate')

    if not product_name:
        return {'error': '"productName" is required'}, 400
    elif not release_date:
        return {'error': '"releaseDate" is required'}, 400

    try:
        yt_retriever = YTRetriever(product_name, int(release_date))
        return {'videos': yt_retriever.retrieve()}
    except Exception as e:
        return {'error': str(e)}, 500


@retrieval_bp.post("/reddit")
def get_reddit_data():
    data = request.get_json()

    product_name = data.get('productName')
    release_date = data.get('releaseDate')

    if not product_name:
        return {'error': '"productName" is required'}, 400
    elif not release_date:
        return {'error': '"releaseDate" is required'}, 400

    try:
        reddit_retriever = RedditRetriever(product_name, int(release_date))
        return {"posts": reddit_retriever.retrieve()}
    except Exception as e:
        return {'error': str(e)}, 500
