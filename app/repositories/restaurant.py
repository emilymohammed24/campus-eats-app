from sqlmodel import Session, select
from typing import Optional, List
from app.models.restaurant import Restaurant
import logging

logger = logging.getLogger(__name__)


class RestaurantRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, restaurant: Restaurant) -> Optional[Restaurant]:
        try:
            self.db.add(restaurant)
            self.db.commit()
            self.db.refresh(restaurant)
            return restaurant
        except Exception as e:
            logger.error(f"Error creating restaurant: {e}")
            self.db.rollback()
            raise

    def get_all(self) -> List[Restaurant]:
        return self.db.exec(select(Restaurant)).all()
    
    def get_by_id(self, restaurant_id: int) -> Optional[Restaurant]:
        return self.db.get(Restaurant, restaurant_id)
    
    def update(self, restaurant_id: int, data: dict) -> Restaurant:
        restaurant = self.db.get(Restaurant, restaurant_id)
        if not restaurant:
            raise Exception("Restaurant not found")

        for key, value in data.items():
            setattr(restaurant, key, value)

        try:
            self.db.add(restaurant)
            self.db.commit()
            self.db.refresh(restaurant)
            return restaurant
        except Exception as e:
            logger.error(f"Error updating restaurant: {e}")
            self.db.rollback()
            raise

    def delete(self, restaurant_id: int):
        restaurant = self.db.get(Restaurant, restaurant_id)
        if not restaurant:
            raise Exception("Restaurant not found")

        try:
            self.db.delete(restaurant)
            self.db.commit()
        except Exception as e:
            logger.error(f"Error deleting restaurant: {e}")
            self.db.rollback()
            raise