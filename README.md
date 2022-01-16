## Overview
This dockerized app automatically downloads currency rates, exports them to .csv, and backups them based on a configurable schedule.

- [Overview](#overview)
- [Features](#features)
- [Setup](#setup)
  * [bash](#bash)
  * [configurating](#configurating)
- [Project structure](#project-structure)
- [Runtime flow](#runtime-flow)
  * [Fetching data](#fetching-data)
  * [Backuping data](#backuping-data)
- [Possible improvements](#possible-improvements)
  * [Dockerfile](#dockerfile)
  * [app.py](#apppy)
  * [backupRates.sh](#backupratessh)

## Features
* Collecting .csv data for any currency configuration
* Scheduled fetching and backuping data
* Overwritting oldest data
* Backuping data
* Logging results


## Setup
### bash
```console
#download file
cd /path/to/dowloaded/file/
unzip cron-api.zip
cd cron-api
docker build -t currency_rates . &&
docker run -td --name currency_fetcher currency_fetcher && 
docker logs -f currency_fetcher
```
### configurating
Example configuration:
```bash
#.credentials
export RESTIC_PASSWORD=YOUR_PASSWORD_FOR_BACKUPS
export API_KEY=YOUR_API_KEY
```
```python
#config.py
QUERY_URL = "http://api.exchangeratesapi.io/v1/latest?access_key=" + 
            API_KEY + "&base=EUR&symbols=USD,CHF,PLN,GBP,JPY"
SELECTED_JSON_ATTRIBUTE = "rates"
```
Switching to antoher API with response format:
```json
{
    "success": true,
    "timestamp": 1619296206,
    "load": {
        "Zaphod": 0.02,
        "Deep Thought": 0.21,
        "Vogon": 0.19,
    }
}
```
To grab data from load attribute edit:
```python
#config.py
QUERY_URL = "http://api.yourapi.com/monitoring/loadbalancers/load/?access_key=" + API_KEY
SELECTED_JSON_ATTRIBUTE = "load"
```
## Project structure
```
app/
|- app.py           # script fetching API data
|- config.py	    # app.py configuration
|- updateRates.sh   # script refreshing app.py
|- backupRates.sh   # script creating backups
|- cronJobs	        # cron schedule
|- .cronrc          # environmental config for cron
|- .credentials     # passwords and API_KEYS
```
## Runtime flow
### Fetching data
```
cron -> updateRates.sh -> .credentials -> app.py -> docker logs
```

### Backuping data
```
cron -> backupRates.sh -> .credentials -> .cronrc -> docker logs
```


## Possible improvements
### Dockerfile
- switch Dockerfile from Debian to Alpine (lighter image)
- run cron in root-less way
- pin packages version

### app.py
- extract base API class which would allow on
- replace pandas with plain python (lighter image)

### backupRates.sh
- preprocess output from restic to one-line logging
- specify forget policy for pruning oldest backups
- pushing backups to AWS s3 / GCP Cloud Storage
