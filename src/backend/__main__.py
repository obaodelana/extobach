from sonar.product import Product

product_name = input("What product will you like to see? ")
product = Product(product_name)

product_details = product.get_details()
if product_details:
    print(repr(product_details))
else:
    print("Oopsie")
