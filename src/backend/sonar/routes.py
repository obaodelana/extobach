from flask import Blueprint, request

from .product_suggestions import ProductSuggestions
from .product import Product

sonar_bp = Blueprint("sonar", __name__, url_prefix="/sonar")


@sonar_bp.post("/suggestions")
def get_product_suggestions():
    data = request.get_json()

    query = data.get("query")
    if not query:
        return {'error': '"query" is required'}, 400

    try:
        product_suggestions = ProductSuggestions(query)
        return {"suggestions": product_suggestions.names}
    except Exception as e:
        return {"error": str(e)}, 500


@sonar_bp.post("/product")
def get_product_details():
    data = request.get_json()

    product_name = data.get("productName")
    if not product_name:
        return {'error': '"productName" is required'}, 400

    try:
        product_details = Product(product_name).details
        if product_details.name == "None":
            return {"error": "Product not found."}, 404
        return product_details.model_dump(mode="json", exclude_none=True)
    except Exception as e:
        return {"error": str(e)}, 500
