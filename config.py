from dotenv import load_dotenv
from os import getenv
load_dotenv()

BOT_TOKEN = getenv('BOT_TOKEN')
CREDENTIALS_FILE = getenv('CREDENTIALS_FILE')
spreadsheet_id = getenv('spreadsheet_id')
