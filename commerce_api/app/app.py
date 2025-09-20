from fastapi import FastAPI
from . import models
from .database import engine
from routers import auth, products, orders, cart, shipping

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router)
app.include_router(products.router)
app.include_router(cart.router)
app.include_router(orders.router)
app.include_router(shipping.router)

