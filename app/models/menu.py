from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List


class MenuItem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    price: float
    description: Optional[str] = None
    is_available: bool = True

    restaurant_id: int = Field(foreign_key="restaurant.id")

    restaurant: Optional["Restaurant"] = Relationship(back_populates="menu_items")
    order_items: List["OrderItem"] = Relationship(back_populates="menu_item")