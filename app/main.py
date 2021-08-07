from typing import Set
from fastapi import FastAPI
from fastapi_csrf_protect import CsrfProtect
from fastapi_csrf_protect.exceptions import CsrfProtectError
from fastapi.middleware.cors import CORSMiddleware
from .dependencies import Base, engine
from . import models

Base.metadata.create_all(bind=engine)
origins = [
    "http://localhost:3280",
    "http://127.0.0.1:3280",
    "https://oms.jakehauling.com",
    "https://demo.oms.jakehauling.com",
]


from starlette.responses import Response
from starlette.requests import Request

async def catch_exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception:
        # you probably want some kind of logging here
        return Response("Internal server error", status_code=500)


app = FastAPI()
app.middleware('http')(catch_exceptions_middleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



from .routers import companies, invoices, locations, orders, intuit, auth, users as user_router
from .internal import companies_utils
from .schemas import CsrfSettings    


@CsrfProtect.load_config
def get_csrf_config():
  return CsrfSettings()

app.include_router(companies.router)
app.include_router(invoices.router)
app.include_router(orders.router)
app.include_router(locations.router)
app.include_router(intuit.router)
app.include_router(companies_utils.router)
app.include_router(auth.router)
app.include_router(user_router.router)