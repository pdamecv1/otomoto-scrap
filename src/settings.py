# DB
REQUIRED_VARS = ['POSTGRES_USER', 'POSTGRES_PASSWORD', 'HOSTNAME', 'POSTGRES_DB']
CARS_TABLE = 'cars'

# Scrapper
URL = 'https://www.otomoto.pl'
SCRAP_PATH = 'artifacts/scrapper'
DOCKER_ARGS = ['verbose', 'headless', 'disable-gpu', 'no-sandbox']

# Logging
LOG_PATH = 'artifacts/logs'
