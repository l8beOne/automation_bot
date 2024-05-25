from os import getenv
from typing import List

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = getenv("BOT_TOKEN")

CREDENTIALS_FILE = getenv("CREDENTIALS_FILE")
spreadsheet_id = getenv("spreadsheet_id")
SCHEDULE_PARAMS = [spreadsheet_id, "A1:M62", "ROWS"]
CERTIFICATE_SPREADSHEET_ID = getenv("CERTIFICATE_SPREADSHEET_ID")
CERTIFICATE_USER_NAME = [
    CERTIFICATE_SPREADSHEET_ID,
    "Ответы на форму (1)!A:A",
    "COLUMNS",
]
SERVICE_ACCOUNT_CREDS_PRIVATE_KEY_ID = getenv(
    "SERVICE_ACCOUNT_CREDS_PRIVATE_KEY_ID"
)
SERVICE_ACCOUNT_CREDS_PRIVATE_KEY = str(
    getenv("SERVICE_ACCOUNT_CREDS_PRIVATE_KEY")
)

SERVICE_ACCOUNT_CREDS = {
    "type": "service_account",
    "project_id": "hseautomationbot",
    "private_key_id": SERVICE_ACCOUNT_CREDS_PRIVATE_KEY_ID,
    "private_key": SERVICE_ACCOUNT_CREDS_PRIVATE_KEY,
    "client_email": "ctx-761@hseautomationbot.iam.gserviceaccount.com",
    "client_id": "112944286413506438492",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": (
        "https://www.googleapis.com/oauth2/v1/certs"
    ),
    "client_x509_cert_url": (
        "https://www.googleapis.com/robot/v1/metadata/x509/"
        "ctx-761%40hseautomationbot.iam.gserviceaccount.com"
    ),
    "universe_domain": "googleapis.com",
}

ADMIN_IDS: List[int] = list(map(int, str(getenv("ADMIN_IDS")).split(",")))


POSTGRES_HOST = getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = getenv("POSTGRES_PORT", 5430)
POSTGRES_USER = getenv("POSTGRES_USER", "myusername")
POSTGRES_PASSWORD = getenv("POSTGRES_PASSWORD", "mypassword")
POSTGRES_DB = getenv("POSTGRES_DB", "schedule_db")

REDDIS_HOST = getenv("REDDIS_HOST", "localhost")
REDDIS_PORT = int(getenv("REDDIS_PORT", 6379))

POSTGRES_DSN_ASYNC: str = (
    f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
    f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)
POSTGRES_DSN: str = (
    f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
    f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)
