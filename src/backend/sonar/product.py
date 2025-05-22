from pydantic import ValidationError

from .models.product_details import ProductDetails
from .util.prompt import prompt


class Product:
    def __init__(self, product_name: str) -> None:
        assert type(product_name) is str

        self.name = product_name

    @prompt(json_schema=ProductDetails.model_json_schema(), return_images=True)
    def _get_details(self) -> str:
        """
        # Identity
        You are a Canadian product researcher.
        You search e-commerce sites and product sites for product information.
        Your responses are straight to the point and you respond only with "None" when you don't know the answer.

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
        - If the product's name is incomprehensible or vague, then respond with "None".
        - If the product does not exist, then respond with "None".
        - Keep the product description concise and summarized.
        - Return the product's price in Canadian dollars. If the price is not available in Canadian dollars, return it in US dollars. 
        - Keep the output very concise, avoid explaining your answers.
        - Do not include any additional information apart from the requested output.
        - Respond in JSON format.
        """

        return f"Get me the latest product information on '{self.name}'."

    @property
    def details(self) -> ProductDetails:
        response = self._get_details()

        image_urls = []
        for image in response.get("images", []):  # type: ignore
            image_urls.append(image["image_url"])
        output = response["choices"][0]["message"]["content"]  # type: ignore

        try:
            details = ProductDetails.model_validate_json(output)
            details.images = image_urls

            return details
        except ValidationError as e:
            raise Exception(output)
