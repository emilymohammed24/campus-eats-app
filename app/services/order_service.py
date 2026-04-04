from app.repositories.order_repository import OrderRepository
from app.repositories.order_item_repository import OrderItemRepository
from app.repositories.menu_repository import MenuRepository
from app.models.order import Order
from app.models.order_item import OrderItem


class OrderService:
    def __init__(
        self,
        order_repo: OrderRepository,
        order_item_repo: OrderItemRepository,
        menu_repo: MenuRepository
    ):
        self.order_repo = order_repo
        self.order_item_repo = order_item_repo
        self.menu_repo = menu_repo

    def place_order(self, user_id: int, items: list[dict]):
        order = Order(user_id=user_id)
        order = self.order_repo.create(order)

        total = 0

        for item in items:
            menu_item = self.menu_repo.get_by_id(item["menu_item_id"])

            if not menu_item:
                raise Exception("Menu item not found")

            if not menu_item.is_available:
                raise Exception(f"{menu_item.name} is not available")

            quantity = item["quantity"]
            price = menu_item.price

            total += price * quantity

            order_item = OrderItem(
                order_id=order.id,
                menu_item_id=menu_item.id,
                quantity=quantity,
                price=price
            )

            self.order_item_repo.create(order_item)

        return {
            "order_id": order.id,
            "total": total
        }
    
    def get_user_orders(self, current_user):
        return self.order_repo.get_by_user(current_user.id)