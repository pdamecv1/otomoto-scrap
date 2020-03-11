import logging
import json
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

    # Save data
    with open('scrapper_data.json', 'w') as f:
        json.dump(scrapper.get_offer_data(), f, indent=4)    
