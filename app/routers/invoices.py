from fastapi import APIRouter

router = APIRouter(prefix='/api/invoices', tags=['Invoices'])


@router.get("/")
async def get_invoices():
    return [{"username": "Rick"}, {"username": "Morty"}]


