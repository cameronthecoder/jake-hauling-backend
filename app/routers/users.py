from fastapi import APIRouter, Query
from fastapi.param_functions import Depends
from sqlalchemy.orm.session import Session
from ..schemas import User as UserSchema, UserIn, Users
from ..models import User
from ..dependencies import get_db, pwd_context

router = APIRouter(prefix='/api/users', tags=['Users'])

@router.get("/", response_model=Users)
def get_users(page: int = Query(1, ge=0), limit: int = 100, db: Session = Depends(get_db)):
    # Pagination
    if page == 0:
        users = db.query(User).order_by(User.id).limit(limit).offset(page*limit).all()
    elif limit == -1:
        users = db.query(User).order_by(User.id).all()
    else:
        users = db.query(User).order_by(User.id).limit(limit).offset((page-1)*limit).all()
    count = db.query(User).count()
    return {"users": users, "total": count}


@router.post("/", response_model=UserSchema)
def create_user(user: UserIn, db: Session = Depends(get_db)):
    hashed = pwd_context.hash(user.password)
    user = User(email=user.email, first_name=user.first_name, last_name=user.last_name, password=hashed)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

