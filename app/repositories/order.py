from sqlmodel import Session, select
from typing import Optional, List
from app.models.order import Order
import logging

logger = logging.getLogger(__name__)


class OrderRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, order: Order) -> Optional[Order]:
        try:
            self.db.add(order)
            self.db.commit()
            self.db.refresh(order)
            return order
        except Exception as e:
            logger.error(f"Error creating order: {e}")
            self.db.rollback()
            raise

    def get_by_id(self, order_id: int) -> Optional[Order]:
        return self.db.get(Order, order_id)
    
    def get_all(self) -> List[Order]:
        return self.db.exec(select(Order)).all()
    
    def get_by_user(self, user_id: int) -> List[Order]:
        statement = select(Order).where(Order.user_id == user_id)
        return self.db.exec(statement).all()
    
    def update_status(self, order_id: int, status: str) -> Order:
        order = self.db.get(Order, order_id)
        if not order:
            raise Exception("Order not found")

        order.status = status

        try:
            self.db.add(order)
            self.db.commit()
            self.db.refresh(order)
            return order
        except Exception as e:
            logger.error(f"Error updating order status: {e}")
            self.db.rollback()
            raise

    def delete(self, order_id: int):
        order = self.db.get(Order, order_id)
        if not order:
            raise Exception("Order not found")

        try:
            self.db.delete(order)
            self.db.commit()
        except Exception as e:
            logger.error(f"Error deleting order: {e}")
            self.db.rollback()
            raise