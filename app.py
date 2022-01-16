import os
import sys
import requests
import pandas as pd
import config
import logging

SAVE_LIMIT = config.SAVE_LIMIT
SOURCE_FILE = config.SOURCE_FILE
DESTINATION_FILE = config.DESTINATION_FILE
SHOULD_TIMESTAMP_DATA = config.SHOULD_TIMESTAMP_DATA

logger = logging.getLogger(__name__)
FORMAT = "[%(asctime)s] %(message)-25s [%(funcName)s():%(filename)8s:%(lineno)s]"
logging.basicConfig(format=FORMAT)
logger.setLevel(logging.INFO)

class ApiToCsv:
    def __init__(self):
        self.query_url = config.QUERY_URL
    def fetch(self):
        logger.debug("QUERY_URL: %s", self.query_url)
        try:
            response = requests.get(self.query_url).json()
        except BaseException as e:
            logger.critical("Fetching response failed: %s", e)
            sys.exit(-1)
        return response

    def extract_attribute(self, response) -> pd.DataFrame:
        """extracts json attribute from response"""
        df = pd.DataFrame(response)
        try:
            df_parsed =  pd.DataFrame(df[config.SELECTED_JSON_ATTRIBUTE]).transpose()
        except KeyError:
            logger.critical(f"Wrong JSON attribute ['{config.SELECTED_JSON_ATTRIBUTE}'] response has: {list(df.columns)}")
            sys.exit(-1)
        except BaseException as e:
            logger.critical("Extracting attribute failed %s", e)
            sys.exit(-1)

        if SHOULD_TIMESTAMP_DATA: # TODO refactor to generic timestamping
            if hasattr(df,"timestamp"):
                df_parsed.insert(0,"timestamp", pd.Timestamp(df.timestamp[0], unit="s"))
            else: logger.error("SHOULD_TIMESTAMP_DATA is not supporting this format yet, skipping...")
        logger.debug("Latest data:\n%s\n", df_parsed.to_string(index=False))
        return df_parsed

    def save(self, df_latest)->int:
        """ Saves latest DataFrame to csv and overwrites oldest result if len(csv) == SAVE_LIMIT"""
        is_csv_created = os.path.isfile(DESTINATION_FILE)
        if is_csv_created:
            df_csv = pd.read_csv(DESTINATION_FILE)
            written_rows = len(df_csv.index)
            if written_rows == config.SAVE_LIMIT:
                df_csv = df_csv[1:] #skip oldest result
                df_updated = df_csv.append(df_latest)
                with open(DESTINATION_FILE, 'w') as f:
                    df_updated.to_csv(f, header = True, index=False)
            else:
                with open(DESTINATION_FILE, 'a') as f:
                    df_latest.to_csv(f, header = False, index=False)
        else:
            # if csv is not created yet, write data with columns (header option)
            with open(DESTINATION_FILE, 'w') as f:
                df_latest.to_csv(f, header = True, index=False)
        return 0

try:
    api = ApiToCsv()
    response = api.fetch()
    df_latest = api.extract_attribute(response)
    if api.save(df_latest) == 0:
        logger.info("OK %s saved", DESTINATION_FILE)
except BaseException as ex:
    logger.critical("Critical Error %s", ex)
    sys.exit(-1)
