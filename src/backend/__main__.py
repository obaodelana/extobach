# from sonar.product import Product
from sonar.product_suggestions import ProductSuggestions

query = input("Search for some product: ")
product_suggestions = ProductSuggestions(query)

product_names = product_suggestions.names
print(repr(product_names))

# product_name = input("What product will you like to see? ")
# product = Product(product_name)

# product_details = product.details
# print(repr(product_details))
