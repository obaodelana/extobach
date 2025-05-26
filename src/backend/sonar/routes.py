from flask import Blueprint, request

from .product_suggestions import ProductSuggestions

sonar_bp = Blueprint("sonar", __name__, url_prefix="/sonar")


@sonar_bp.post("/suggestions")
def get_product_suggestions():
    data = request.get_json()

    query = data.get("query")
    if not query:
        return {'error': 'query is required'}, 400

    try:
        product_suggestions = ProductSuggestions(query)
        return {"suggestions": product_suggestions.names}
    except Exception as e:
        return {"error": str(e)}, 500
