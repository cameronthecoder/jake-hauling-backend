from fastapi import APIRouter, Depends
from fastapi.param_functions import Query
from ..models import Company
from ..schemas import CompanyList
from ..dependencies import get_db
from sqlalchemy.orm import Session


router = APIRouter(prefix='/api/companies', tags=['Companies'])


@router.get("/", response_model=CompanyList)
def get_companies(page: int = Query(1, ge=0), searchTerm: str = Query(None), limit: int = 100, db: Session = Depends(get_db)):
    # Pagination
    if searchTerm is not None:
        companies = db.query(Company).\
            filter(Company.name.ilike('%{searchTerm}%')).all()
    else:
        if page == 0:
            companies = db.query(Company).\
                order_by(Company.id).\
                limit(limit)\
                .offset(page*limit).all()
        elif limit == -1:
            companies = db.query(Company)\
                .order_by(Company.id).all()
        else:
            companies = db.query(Company)\
                .order_by(Company.id).\
                limit(limit)\
                .offset((page-1)*limit).all()
    count = db.query(Company).count()
    return {"companies": companies, "total": count}
