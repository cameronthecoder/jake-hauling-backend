from app.services import UserService
from pydantic.main import BaseModel
from pydantic.networks import HttpUrl
from fastapi import APIRouter, Depends
from starlette.responses import JSONResponse, RedirectResponse
from intuitlib.enums import Scopes
from fastapi_csrf_protect import CsrfProtect
from intuitlib.client import AuthClient
from ..config import settings
from ..dependencies import get_db
from ..models import User
from ..schemas import User as UserSchema, UserOut
from .auth import get_current_active_user
from cryptography.fernet import Fernet
import aiohttp
import os.path
file_exists = os.path.isfile('secret.key') 

router = APIRouter(prefix='/api', tags=['Intuit Quickbooks'])

redirect_uri = 'http://localhost:8000/api/intuit-callback/'
base_url = 'https://sandbox-quickbooks.api.intuit.com'


def generate_key():
    key = Fernet.generate_key()
    if not file_exists:
        with open("secret.key", "wb") as key_file:
            key_file.write(key)


generate_key()


def load_key():
    return open("secret.key", "rb").read()

# Oauth flow from client:

# 1. Client requests ouath URL
# 2. Intuit Callback sets realm_id, access_token, refresh_token, and id_token to current user


def get_intuit_auth_client(**kwargs):
    return AuthClient(
        client_id=settings.intuit_client_id,
        client_secret=settings.intuit_client_secret,
        environment='sandbox',
        redirect_uri=redirect_uri,
        **kwargs
    )


class IntuitOauth(BaseModel):
    authorization_url: HttpUrl


@router.get("/oauth/", response_model=IntuitOauth)
async def intuit_oauth(csrf_protect: CsrfProtect = Depends(), current_user: UserSchema = Depends(get_current_active_user)):
    # does this CSRF token need to be encrypted?
    auth_client = get_intuit_auth_client(
        state_token=csrf_protect.generate_csrf())
    auth_url = auth_client.get_authorization_url(scopes=[Scopes.ACCOUNTING])
    query = users.select().where(users.c.email == current_user.email)
    #result = await database.execute(query)
    if 0:
        try:
            query = users.update().where(users.c.email == current_user.email).values(intuit_state_token=auth_client.state_token)
            #await database.execute(query)
        except:
            return JSONResponse({'error': 'An unexpected error occurred while trying to update the user.'}, status_code=500)

    return {'authorization_url': auth_url}


@router.get("/intuit-callback/")
def intuit_callback(code: str, state: str, realmId: int, error: str = None):
    auth_client = get_intuit_auth_client()
    if error:
        print(error)
        return {'error': 'error from intuit server'}
    query = users.select().where(users.c.intuit_state_token == state)
    #result = await database.fetch_one(query)
    if not 0:
        return JSONResponse({'error': 'Unauthorized'}, status_code=401)

    response = RedirectResponse('http://localhost:3280')
    key = load_key()
    f = Fernet(key)

    response.set_cookie(key="realm_id", value=realmId)

    auth_client.get_bearer_token(code, realm_id=realmId)

    access_token_encoded = auth_client.access_token.encode()
    refresh_token_encoded = auth_client.refresh_token.encode()
    update_user = users.update().where(users.c.email == result[3]).values(
        intuit_access_token=f.encrypt(access_token_encoded),
        intuit_refresh_token=f.encrypt(refresh_token_encoded),
        intuit_realm_id=auth_client.realm_id)
    #await database.execute(update_user)

    return response


@router.get("/intuit-company/")
async def intuit_verification(current_user: UserOut = Depends(get_current_active_user)):
    url = '{0}/v3/company/{1}/companyinfo/{1}'.format(base_url, current_user.intuit_realm_id)
    # Decrypt access token
    key = load_key()
    f = Fernet(key)
    access_token = f.decrypt(current_user.intuit_access_token)
    headers = {"Authorization": "Bearer {0}".format(access_token.decode()), "Accept": "application/json"}
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url) as resp:
            response = await resp.json()
            return response
