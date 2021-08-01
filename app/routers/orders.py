from app.models import Order
from app.dependencies import get_db
from fastapi.param_functions import Depends
from sqlalchemy.orm.session import Session
from app.services import OrderService
from datetime import date
from fastapi import APIRouter
from typing import List
from ..schemas import Order as OrderSchema, OrderCreate
router = APIRouter(prefix='/api/orders', tags=['Orders'])


@router.get('/ready/')
def ready_orders(db: Session = Depends(get_db)):
    ready_orders = OrderService.get_ready_orders(db)
    return ready_orders

@router.get('/', response_model=List[OrderSchema])
def orders(db: Session = Depends(get_db)):
    orders = db.query(Order).all()
    return orders 

@router.post('/', response_model=OrderSchema)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    order = OrderService.create_order(db, order)
    return order

