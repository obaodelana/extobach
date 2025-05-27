from pydantic import ValidationError

from .util.prompt import prompt
from .models.product_names import ProductNames


class ProductSuggestions:
    def __init__(self, query: str) -> None:
        assert type(query) is str

        self.query = query

    @prompt(max_tokens=200, temperature=0.5, json_schema=ProductNames.model_json_schema())
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
                "Product 1",
                "Product 2",
                "Product 3",
                ...
            ]
        }

        # Instructions
        - When given a search query, return the 3-10 most popular products related to the query.
        - Only return product names prepended with their brands. Do not return any other information about the product.
        - Don't just return brand names. Return a real product with its brand e.g., "'Brand' 'Product Name'".
        - Respond in JSON format.
        """

        return f"Give me the top 3-5 product names most related to '{self.query}'"

    @property
    def names(self) -> list[str]:
        response = self._get_suggestions()

        output = response["choices"][0]["message"]["content"]  # type: ignore
        try:
            suggestions = ProductNames.model_validate_json(output).names
            return suggestions
        except ValidationError:
            raise Exception(f"Cannot parse: '{output}'")
