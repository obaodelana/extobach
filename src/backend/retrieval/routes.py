from flask import Blueprint, request

from .yt import YTRetriever

retrieval_bp = Blueprint("retrieval", __name__, url_prefix="/retrieve")


@retrieval_bp.post("/yt")
def get_youtube_data():
    data = request.get_json()

    product_name = data.get('productName')
    release_date = data.get('releaseDate')

    if not product_name:
        return {'error': 'productName is required'}, 400
    elif not release_date:
        return {'error': 'releaseDate is required'}, 400

    try:
        yt_retriever = YTRetriever(product_name, int(release_date))
        return {'videos': yt_retriever.retrieve()}
    except Exception as e:
        return {'error': str(e)}, 500
