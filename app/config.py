from pydantic import BaseSettings


class Settings(BaseSettings):
    database_url: str
    intuit_client_id: str
    intuit_client_secret: str
    secret_key: str

settings = Settings('.env')