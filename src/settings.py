# DB
REQUIRED_VARS = ['POSTGRES_USER', 'POSTGRES_PASSWORD', 'POSTGRES_HOSTNAME', 'POSTGRES_DB', 'POSTGRES_PORT']
CARS_TABLE = 'cars'

# Scrapper
URL = 'https://www.otomoto.pl'
SCRAP_PATH = 'artifacts/scrapper'
DOCKER_ARGS = ['verbose', 'headless', 'disable-gpu', 'no-sandbox']

# Logging
LOG_PATH = 'artifacts/logs'

# Report
REPORT_PATH = 'artifacts/report'
