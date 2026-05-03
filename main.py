from fastapi import Depends,FastAPI 
from models import Product, ProductUpdate
from database import session, engine
import database_models
from sqlalchemy.orm import Session
app = FastAPI()

# for creating tables
database_models.Base.metadata.create_all(bind = engine)

@app.get("/")
def greet():
    return "Welcome to my page"

products = [
    Product(id = 1, name ="phone", description = "budget phone",price= 99,quantity = 1),
    Product(id = 2, name ="laptop", description = "dell laptop",price= 599,quantity = 7),
    Product(id = 3, name ="watch", description = "watch",price= 50,quantity = 2),
]

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()

def init_db():
    db = session()
    count = db.query(database_models.Product).count
    if count == 0:
        for product in products:
            db.add(database_models.Product(**product.model_dump()))
        
        db.commit()

init_db()

@app.get("/products")
def get_all_products(db: Session = Depends(get_db)):
    db_products = db.query(database_models.Product).all()
    return  db_products

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
    