"config for app.py"
import os

BASE_URL = "http://api.exchangeratesapi.io/v1/latest"
API_KEY = os.getenv("API_KEY")
QUERY_URL = BASE_URL + "?access_key=" + API_KEY +"&base=EUR&symbols=USD,CHF,PLN,GBP,JPY"

SELECTED_JSON_ATTRIBUTE = "rates"
DESTINATION_FILE = "rates.csv"
SOURCE_FILE = "response.json"

SAVE_LIMIT = 7

SHOULD_TIMESTAMP_DATA = True
