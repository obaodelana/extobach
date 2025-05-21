from pydantic import ValidationError
import os
from inspect import getdoc
import requests

from .models.product_details import ProductDetails


class Product:
    def __init__(self, product_name: str, country_code: str = "CA") -> None:
        assert type(product_name) is str
        assert type(country_code) is str

        self.name = product_name
        self.country = country_code

    def get_details(self) -> ProductDetails:
        """
        # Identity
        You are a Canadian product researcher. You search e-commerce sites and product sites for product information. Your responses are straight to the point and you respond only with "None" when you don't know the answer.

        # Output format
        {
            "name": The product's full name
            "description": The product's description
            "price": {
                "low": Minimum price
                "high": Maximum price
            },
            "currency": "CAD", if the price is in Canadian dollars, otherwise, "USD" for US dollars
            "brand": The name of the company that made the product
            "category": The product's category, e.g., "Technology", "Fashion", "Beauty", "Books"
            "availability": "In stock" if it is available on any site you search, or "Out of stock" otherwise ("None" if you're not sure)
            "rating": The average rating (out of 5) of the product across all the sites you've searched, or "None" if nothing is found
        }

        # Instructions
        - If the product's name is too vague (e.g., "shirt", "big bag", "love"), then respond with "Could you be more specific?".
        - If the product's name is incomprehensible (e.g., "nn", "argh"), then respond with "Product not found".
        - If the product does not exist, then respond with "Product not found".
        - If the product's name is ambiguous (e.g., "Lululemon shirt" or "Makeup from Mac"), then respond with a list of 3-5 possible product names (one per line.)
        - Keep the product description concise and summarized
        - Return the product's price in Canadian dollars. If the price is not available in Canadian dollars, return it in US dollars. 
        - Keep the output very concise, avoid explaining your answers.
        - Do not include any additional information apart from the requested output.
        - Respond in JSON format
        """

        url = "https://api.perplexity.ai/chat/completions"
        payload = {
            "model": "sonar",
            "messages": [
                {
                    "role": "system",
                    "content": getdoc(self.get_details)
                },
                {
                    "role": "user",
                    "content": f"Get me the latest product information on '{self.name}'"
                }
            ],
            "max_tokens": 500,
            "return_images": True,
            "response_format": {
                "type": "json_schema",
                "json_schema": {"schema": ProductDetails.model_json_schema()}
            },
            "web_search_options": {
                "search_context_size": "low",
                "user_location": {"country": self.country}
            }
        }

        api_key = os.getenv("PERPLEXITY_API_KEY", None)
        assert api_key is not None, "Can't find 'PERPLEXITY_API_KEY' environment variable"

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()

        res_json: dict = response.json()

        image_url = None
        if "images" in res_json and len(res_json["images"]) > 0:
            image_url = res_json["images"][0].get("image_url")
        output = res_json["choices"][0]["message"]["content"]

        try:
            details = ProductDetails.model_validate_json(output)
            details.image_url = image_url

            return details
        except ValidationError as e:
            raise Exception(output)
