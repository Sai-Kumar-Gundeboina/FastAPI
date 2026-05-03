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
def get_product(id:int, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    
    if db_product:
        return db_product
    
    return {"message": "Product not found"}

@app.post("/product")
def add_product(product: Product, db: Session = Depends(get_db)):
    
    db.add(database_models.Product(**product.model_dump()))
    db.commit()
    return {"message": "success", "body": product}

@app.delete("/product/{id}")
def delete_product(id:int, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
        return {"message": "success"}
    return {"message":"Invlaid product id", "id":id}

@app.put("/product")
def update_product(id:int, prod: ProductUpdate, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_product:
        updated_data = prod.dict(exclude_unset= True)

        for key, value in updated_data.items():
            setattr(db_product, key , value)
        db.commit()
        return {"message":"success"}
    return {"error":"Invalid Product Id"}
    