from dotenv import load_dotenv
from os import getenv
from typing import List
load_dotenv()

BOT_TOKEN =         getenv("BOT_TOKEN")
CREDENTIALS_FILE =  getenv("CREDENTIALS_FILE")
spreadsheet_id =    getenv("spreadsheet_id")
ADMIN_IDS: List[int] = list(map(int, str(getenv("ADMIN_IDS")).split(",")))
 

POSTGRES_HOST=      getenv("POSTGRES_HOST","localhost")
POSTGRES_PORT=      getenv("POSTGRES_PORT", 5430)
POSTGRES_USER=      getenv("POSTGRES_USER","myusername")
POSTGRES_PASSWORD=  getenv("POSTGRES_PASSWORD","mypassword")
POSTGRES_DB=        getenv("POSTGRES_DB","schedule_db")

REDDIS_HOST = getenv("REDDIS_HOST","localhost")
REDDIS_PORT = int(getenv("REDDIS_PORT", 6379))

POSTGRES_DSN_ASYNC: str = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
POSTGRES_DSN: str = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
