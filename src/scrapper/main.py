import logging
from selenium import webdriver
# GUI
from gui.variables import Vars
from scrapper import Scrapper
from gui.offer import Offer


log = logging.getLogger(__name__)


if __name__ == '__main__':
    # For testing purposes. Will be rewritten.
    chrome_options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.get(Vars.OTOMOTO)
    
    scrapper = Scrapper(driver=driver)
    scrapper.search(data={})
    scrapper.verify_results()
    scrapper.get_offer_from_all_pages()

    # Testing the offer data
    print(scrapper.offer_urls)
    scrapper.get_offer_data()
