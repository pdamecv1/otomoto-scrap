import os
import json
import logging as log
from src.otomoto_scrapper import OtoMotoScrapper
from src.db_sync import DbSync, Car
from src.report import GenerateReport
from src.settings import LOG_PATH, SCRAP_PATH

def load_json(filename):
    with open(filename) as f:
        return json.load(f)

def prepare_artifacts():
    for path_ in [LOG_PATH, SCRAP_PATH]:
        if not os.path.exists(path_):
            os.makedirs(path_)

def create_logger():
    handler = log.FileHandler(os.path.join(LOG_PATH, 'debug.log'), 'w+', 'utf-8')
    format_ = '%(levelname)s:%(message)s'
    return log.basicConfig(handlers=[handler], format=format_, level=log.INFO)


if __name__ == '__main__':

    # Preparation
    data = load_json('input.json')
    
    prepare_artifacts()
    create_logger()
    
    # Scrapper
    log.info(f'Data provided in input.json: {data}')
    sc = OtoMotoScrapper(input_data=data)
    sc.scrap()

#     # DB sync
#     dbs = DbSync() 
#     dbs.insert_car_data()

#     # Generate report
#     gr = GenerateReport(dbs.db, Car)
#     gr.generate_report()
