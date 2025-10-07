from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, func, Boolean
from sqlalchemy.orm import relationship
from .database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)

    orders = relationship("Order", back_populates="user")
    cart_items = relationship("CartItem", back_populates="user", cascade="all, delete")




class Admin(Base):
     __tablename__ = "admins"
     id = Column(Integer, primary_key=True, index=True)
     username = Column(String, unique=True, index=True, nullable=False)
     email = Column(String, unique=True, index=True, nullable=False)
     hashed_password = Column(String, nullable=False)
     is_admin = Column(Boolean, default=True)



class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    stock = Column(Integer, default=0)

    items = relationship("OrderItem", back_populates="product")
# app/models.py

class OrderItem(Base):
    __tablename__ = "order_items"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer, default=1)

    order = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="items")

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    status = Column(String, default="pending")
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order")
    shipping = relationship("Shipping", back_populates="order", uselist=False, cascade="all, delete")



# app/models.py

class CartItem(Base):
    __tablename__ = "cart_items"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"))
    # product_name = Column(String, ForeignKey("products.name", ondelete="CASCADE"))
    quantity = Column(Integer, nullable=False, default=1)

    user = relationship("User")
    product = relationship("Product")



class Shipping(Base):
    __tablename__ = "shipping"

    id = Column(Integer, primary_key=True, index=True)
    address = Column(String, nullable=False)
    city = Column(String, nullable=False)
    country = Column(String, nullable=False)

    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    order = relationship("Order", back_populates="shipping")

