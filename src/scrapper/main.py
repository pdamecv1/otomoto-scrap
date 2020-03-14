import logging
import json
import requests
from selenium import webdriver
# GUI
from gui.variables import Vars
from scrapper import Scrapper
from gui.utils import Utils
from gui.offer import Offer


log = logging.getLogger(__name__)


if __name__ == '__main__':
    # For testing purposes. Will be rewritten.
    chrome_options = webdriver.ChromeOptions() 
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.get(Vars.OTOMOTO)
    
    data = Utils.parse_json('input.json')
    scrapper = Scrapper(driver=driver, data=data)
    scrapper.search()
    scrapper.verify_results()
    
    for record in scrapper.get_offer_data():
        req = requests.post('http://127.0.0.1:8000/offers/', data=record[0])
        print(req.status_code)
        print(req.text)

    # # Save data
    # with open('scrapper_data.json', 'w') as f:
    #     json.dump(, f, indent=4)    
    driver.close()