from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, List
from pydantic import EmailStr
from datetime import datetime


class UserBase(SQLModel,):
    username: str = Field(index=True, unique=True)
    email: EmailStr = Field(index=True, unique=True)
    password: str
    role:str = ""

class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    orders: List["Order"] = Relationship(back_populates="user")

class Restaurant(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    location: str
    description: Optional[str] = None

    menu_items: List["MenuItem"] = Relationship(back_populates="restaurant")

class MenuItem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    price: float
    description: Optional[str] = None
    is_available: bool = True

    restaurant_id: int = Field(foreign_key="restaurant.id")
    restaurant: Optional["Restaurant"] = Relationship(back_populates="menu_items")

    order_items: List["OrderItem"] = Relationship(back_populates="menu_item")

class Order(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    user_id: int = Field(foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    status: str = "pending"

    user: Optional["User"] = Relationship(back_populates="orders")
    items: List["OrderItem"] = Relationship(back_populates="order")

class OrderItem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    order_id: int = Field(foreign_key="order.id")
    menu_item_id: int = Field(foreign_key="menuitem.id")

    quantity: int
    price: float  # snapshot price

    order: Optional["Order"] = Relationship(back_populates="items")
    menu_item: Optional["MenuItem"] = Relationship(back_populates="order_items")