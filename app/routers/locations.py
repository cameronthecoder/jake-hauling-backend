from fastapi import APIRouter

router = APIRouter(prefix='/api/locations', tags=['Locations'])


@router.get("/")
async def get_locations():
    return [{"username": "Rick"}, {"username": "Morty"}]


