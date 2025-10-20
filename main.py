from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import Product
from sqlalchemy.orm import Session
from database import session, engine
import database_models


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins= ["http://localhost:3000"],
    allow_credentials= True,
    allow_methods= ["*"],
    allow_headers= ["*"],
)

database_models.Base.metadata.create_all(bind=engine)

@app.get("/")
def greet():
    return {"message": "Welcome to Telusko Trac"}

products = [
    Product(id= 1, name="phone", description="A new phone", price=5300.90, quantity=30),
    Product(id= 2, name="car", description="A new car", price=205300.90, quantity=4),
    Product(id= 3, name="broom", description="A new broom", price=5300.90, quantity=32),
    Product(id= 4, name="kite", description="A new kite", price=100.90, quantity=130),
    Product(id= 7, name="pencil", description="A new pencil", price=5300.90, quantity=230),
    Product(id= 8, name="pencil", description="A new pencil", price=5300.90, quantity=230)
]

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()
        

def _init_db():
    db = session()
    
    count = db.query(database_models.Product).count()
    
    if count == 0:
        for product in products:
            db.add(database_models.Product(**product.model_dump()))
            
        db.commit()
        

_init_db()

@app.get("/products")
def get_all_products(db: Session = Depends(get_db)):
   
   db_products = db.query(database_models.Product).all()
   
   return db_products

@app.get("/products/{id}")
def get_product_by_id(id: int, db: Session = Depends(get_db)):
    
    db_products = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if not db_products:
        raise HTTPException(status_code=404, detail="product not found")
    
    return db_products
        
@app.post("/products")
def add_product(product: Product, db: Session = Depends(get_db)):
    
    db.add(database_models.Product(**product.model_dump()))
    db.commit()
    return product

@app.put("/products/{id}")
def update_product(id: int, product: Product, db: Session = Depends(get_db)):
    
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if  not db_product:
        raise HTTPException(status_code=404, detail="product not found")
        
    db_product.name = product.name  # type: ignore
    db_product.description = product.description  # type: ignore
    db_product.price = product.price  # type: ignore
    db_product.quantity = product.quantity  # type: ignore
    db.commit()
    return {"message": "product Updated successfully"}

@app.delete("/products/{id}")
def delete_product(id: int, db: Session = Depends(get_db)):
    
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  
    if  not db_product:
        raise HTTPException(status_code=404, detail="product not found")
        
    db.delete(db_product) 
    db.commit()
    return {"message": "Product deleted successfully!"}

