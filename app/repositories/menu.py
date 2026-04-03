from sqlmodel import Session, select
from typing import Optional, List
from app.models.menu import MenuItem
import logging

logger = logging.getLogger(__name__)


class MenuRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, item: MenuItem) -> Optional[MenuItem]:
        try:
            self.db.add(item)
            self.db.commit()
            self.db.refresh(item)
            return item
        except Exception as e:
            logger.error(f"Error creating menu item: {e}")
            self.db.rollback()
            raise
            raise

    def get_by_id(self, item_id: int) -> Optional[MenuItem]:
        return self.db.get(MenuItem, item_id)
    
    def get_all(self) -> List[MenuItem]:
        return self.db.exec(select(MenuItem)).all()
    
    def get_by_restaurant(self, restaurant_id: int) -> List[MenuItem]:
        statement = select(MenuItem).where(MenuItem.restaurant_id == restaurant_id)
        return self.db.exec(statement).all()
    
    def update(self, item_id: int, data: dict) -> MenuItem:
        item = self.db.get(MenuItem, item_id)
        if not item:
            raise Exception("Menu item not found")

        for key, value in data.items():
            setattr(item, key, value)

        try:
            self.db.add(item)
            self.db.commit()
            self.db.refresh(item)
            return item
        except Exception as e:
            logger.error(f"Error updating menu item: {e}")
            self.db.rollback()
            raise

    def delete(self, item_id: int):
        item = self.db.get(MenuItem, item_id)
        if not item:
            raise Exception("Menu item not found")

        try:
            self.db.delete(item)
            self.db.commit()
        except Exception as e:
            logger.error(f"Error deleting menu item: {e}")
            self.db.rollback()
            raise