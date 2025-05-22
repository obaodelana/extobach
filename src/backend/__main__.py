from sonar.product import Product

product_name = input("What product will you like to see? ")
product = Product(product_name)

product_details = product.details
print(repr(product_details))
