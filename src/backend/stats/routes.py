from flask import Blueprint, request
from random import sample

from .relevancy import Relevancy
from .yt import YTRetriever

stats_bp = Blueprint("stats", __name__, url_prefix="/stats")


@stats_bp.post("")
def get_all_stats():
    data = request.get_json()

    product_name = data.get('productName')
    release_date = data.get('releaseDate')

    if not product_name:
        return {'error': '"productName" is required'}, 400
    elif not release_date:
        return {'error': '"releaseDate" is required'}, 400

    try:
        yt_data = YTRetriever(product_name, release_date).retrieve()
        return {
            "comments": get_some_comments(yt_data),
            "relevancy": get_relevancy(yt_data),
            "sentiment": get_sentiment(yt_data)
        }
    except Exception as e:
        return {'error': str(e)}, 500


def get_some_comments(yt_data: dict) -> list:
    chosen_comments = []
    for _, videos in yt_data.items():
        some_videos = sample(videos, min(3, len(videos)))
        for video in some_videos:
            comments = video.get("topComments", [])
            if len(comments) == 0:
                continue
            some_comments = sample(comments, min(2, len(comments)))
            chosen_comments += some_comments
    return chosen_comments


def get_relevancy(yt_data: dict) -> dict:
    relevancy = Relevancy(yt_data)

    return relevancy.get_score()


def get_sentiment(yt_data: dict) -> dict:
    # TODO
    return {}
