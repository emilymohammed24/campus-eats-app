from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from app.models.order import Order
from app.models.menu import MenuItem


class OrderItem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    order_id: int = Field(foreign_key="order.id")
    menu_item_id: int = Field(foreign_key="menuitem.id")

    quantity: int
    price: float

    order: Optional["Order"] = Relationship(back_populates="items")
    menu_item: Optional["MenuItem"] = Relationship(back_populates="order_items")