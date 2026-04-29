from fastapi import FastAPI 
from models import Product, ProductUpdate

app = FastAPI()

@app.get("/")
def greet():
    return "Welcome to my page"

products = [
    Product(id = 1, name ="phone", description = "budget phone",price= 99,quantity = 1),
    Product(id = 2, name ="laptop", description = "dell laptop",price= 599,quantity = 7),
    Product(id = 3, name ="watch", description = "watch",price= 50,quantity = 2),
]

@app.get("/products")
def get_all_products():
    return  products

@app.get("/product/{id}")
def get_product(id:int):
    for product in products:
        if product.id == id:
            return product
    return []

@app.post("/product")
def add_product(product: Product):
    products.append(product)
    return {"message": "success", "body": product}

@app.delete("/product/{id}")
def delete_product(id:int):
    for product in products:
        if product.id == id:
            products.remove(product)
            return {"message": "success", "body": product}
    return {"message":"Invlaid product id", "id":id}

@app.put("/product")
def update_product(product_id:int, prod: ProductUpdate):
    for product in products:
        if product.id == product_id:
            updated_data = prod.dict(exclude_unset= True)

            for key, value in updated_data.items():
                setattr(product, key , value)
            return {"message":"success", "updated":product}
    return {"error":"Invalid Product Id"}
    