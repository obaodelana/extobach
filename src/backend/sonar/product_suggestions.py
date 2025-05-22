from .util.prompt import prompt
from .models.product_names import ProductNames


class ProductSuggestions:
    def __init__(self, query: str) -> None:
        assert type(query) is str

        self.query = query

    @prompt(max_tokens=100, temperature=0.5, json_schema=ProductNames.model_json_schema())
    def _get_suggestions(self) -> str:
        """
        # Identity
        You are a Canadian product researcher.
        You search e-commerce sites for a list of products that are most closely related to the given search query.
        You responses are one-line phrases of a product's full name.

        # Input
        You are given a search query. It might be a complete product name, some unrelated concept or gibberish.

        # Output format
        {
            "names": [
                "Product Name 1",
                "Product Name 2",
                "Product Name 3",
                ...
            ]
        }

        # Instructions
        - When given a search query, return the 3-10 most popular products related to the query.
        - Only return product names. Do not return any other information about the product.
        - Include the brand name when giving the product name. 
        - Respond in JSON format
        """

        return f"Give me the top 3-10 product names most related to '{self.query}'"
