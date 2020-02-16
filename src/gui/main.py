import logging
from selenium import webdriver
# GUI
from vars import Vars
from search_area import SearchArea
from detailed_search import DetailedSearch

log = logging.getLogger(__name__)


if __name__ == '__main__':
    chrome_options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.get(Vars.OTOMOTO)
    
    searchbox = SearchArea(driver)
    searchbox.select_state_of_use('new')
    searchbox.select_car_make('BMW')
    searchbox.select_car_model('M4')
    searchbox.select_price_range(2000, 200000)
    searchbox.select_mileage_range(20000, 125000)
    searchbox.select_production_range(2010, 2015)
    searchbox.check_vin_history()
    searchbox.select_fuel_type('diesel')
    searchbox.click_search()
    
    asd = DetailedSearch(driver)
    if asd.is_any_results():
        asd.get_results()