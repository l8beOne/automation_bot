from dotenv import load_dotenv
from os import getenv
load_dotenv()

BOT_TOKEN =         getenv('BOT_TOKEN')
CREDENTIALS_FILE =  getenv('CREDENTIALS_FILE')
spreadsheet_id =    getenv('spreadsheet_id')
ADMIN_ID =          getenv('ADMIN_ID')

POSTGRES_HOST=      getenv("POSTGRES_HOST","localhost")
POSTGRES_PORT=      getenv("POSTGRES_PORT", 5434)
POSTGRES_USER=      getenv("POSTGRES_USER","myusername")
POSTGRES_PASSWORD=  getenv("POSTGRES_PASSWORD","mypassword")
POSTGRES_DB=        getenv("POSTGRES_DB","schedule_db")

POSTGRES_DSN_ASYNC: str = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
POSTGRES_DSN: str = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
