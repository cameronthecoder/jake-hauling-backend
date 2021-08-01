from app.schemas import User
from sqlalchemy import func, select
from .models import Order, Company, Address, User
from sqlalchemy.orm import Session

class UserService(object):
    @staticmethod
    def get_user_by_email(db: Session, email):
        return db.query(User).filter(User.email == email).first()
    
    
class OrderService(object):
    @staticmethod
    def get_ready_orders(db: Session):
        orders = db.query(Order).\
            filter(func.date_part('week', Order.estimated_ready_date) == func.date_part('week', func.current_date())).\
            limit(4)
        return orders

    @staticmethod
    def create_order(db: Session, order):
        order = Order(**order)
        
