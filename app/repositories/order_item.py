from sqlmodel import Session, select
from typing import Optional, List
from app.models.order_item import OrderItem
import logging

logger = logging.getLogger(__name__)


class OrderItemRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, order_item: OrderItem) -> Optional[OrderItem]:
        try:
            self.db.add(order_item)
            self.db.commit()
            self.db.refresh(order_item)
            return order_item
        except Exception as e:
            logger.error(f"Error creating order item: {e}")
            self.db.rollback()
            raise

    def get_by_id(self, item_id: int) -> Optional[OrderItem]:
        return self.db.get(OrderItem, item_id)
    
    def get_by_order(self, order_id: int) -> List[OrderItem]:
        statement = select(OrderItem).where(OrderItem.order_id == order_id)
        return self.db.exec(statement).all()
    
    def update(self, item_id: int, data: dict) -> OrderItem:
        item = self.db.get(OrderItem, item_id)
        if not item:
            raise Exception("Order item not found")

        for key, value in data.items():
            setattr(item, key, value)

        try:
            self.db.add(item)
            self.db.commit()
            self.db.refresh(item)
            return item
        except Exception as e:
            logger.error(f"Error updating order item: {e}")
            self.db.rollback()
            raise

    def delete(self, item_id: int):
        item = self.db.get(OrderItem, item_id)
        if not item:
            raise Exception("Order item not found")

        try:
            self.db.delete(item)
            self.db.commit()
        except Exception as e:
            logger.error(f"Error deleting order item: {e}")
            self.db.rollback()
            raise