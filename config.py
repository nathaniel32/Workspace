SERVICE_HOST = "localhost"
SERVICE_PORT = 9000

ORIGINS = []

#DB_USERNAME = "nathaniel"
#DB_PASSWORD = "niel12"
DB_USERNAME = "postgres"
DB_PASSWORD = "020810"
DB_DATABASE = "nathaniel_db"

URL_DATABASE = f'postgresql+psycopg2://{DB_USERNAME}:{DB_PASSWORD}@localhost:5432/{DB_DATABASE}'

APP_NAME = "Order Hub"

SECRET_KEY = "123didojqwoi13"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXP_STD = 24

VERIFIED_ACCOUNT_CODE = 1