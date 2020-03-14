import logging
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
# GUI
from .basepage import BasePage
from .factory import SeleniumFactory as SF
from .locators import SearchAreaLocators
from .utils import Utils
from .detailed_search import DetailedSearch


log = logging.getLogger(__name__)


class SearchArea(BasePage):
    """
    Class containing functionality connected to the Searchbox/Searcharea 
    at the main page: https://www.otomoto.pl/
    """

    TIMEOUT = 10

    def select_state_of_use(self, state='all'):
        """
        Selects car's state of use. By default the state is set to "all".
            state [str]: all|new|used
        """
        if state != 'all':
            state_xpath = SearchAreaLocators.CAR_STATE_AREA + f'//input[@value="{state}"]/following-sibling::label'
            state = self.driver.find_element_by_xpath(state_xpath)
            state.click()

    def select_car_make(self, make):
        """
        Selects make of the car.
            make [str]: BMW|Honda|Audi, etc.
        """
        make_element = self.driver.find_element_by_xpath(SearchAreaLocators.MAKE)
        SF.select(element_xpath=make_element, value=make.lower())

    def select_car_model(self, model):
        """
        Selects model of the car.
            make [str]: M4|Accord|Q7, etc.
        """
        model_element = self.driver.find_element_by_xpath(SearchAreaLocators.MODEL)
        SF.select(element_xpath=model_element, text=model)

    def select_price_range(self, min_price, max_price):
        """
        Selects price range, i.e. from 2 000 to 7 500 000 PLN.
        The ranges MUST MATCH what's on the GUI.
            min_price [str]: 2000
            max_price [str]: 20000
        """
        self._select_min_price(min_price)
        self._select_max_price(max_price)

    def _select_min_price(self, min_price):
        min_price_ele = self.driver.find_element_by_xpath(SearchAreaLocators.MIN_PRICE)
        SF.select(element_xpath=min_price_ele, text=Utils.format_integer(min_price) + ' PLN')

    def _select_max_price(self, max_price):
        max_price_ele = self.driver.find_element_by_xpath(SearchAreaLocators.MAX_PRICE)
        SF.select(element_xpath=max_price_ele, text=Utils.format_integer(max_price) + ' PLN')

    def select_mileage_range(self, min_mileage, max_mileage):
        """
        Selects mileage range, i.e. from 20 000 to 250 000 km.
        The ranges MUST MATCH what's on the GUI.
            min_price [str]: 2000
            max_price [str]: 20000
        """    
        self._select_min_mileage(min_mileage)
        self._select_max_mileage(max_mileage)

    def _select_min_mileage(self, min_mileage):
        min_mileage_ele = self.driver.find_element_by_xpath(SearchAreaLocators.MIN_MILEAGE)
        SF.select(element_xpath=min_mileage_ele, text=Utils.format_integer(min_mileage) + ' km')

    def _select_max_mileage(self, max_mileage):
        max_mileage_ele = self.driver.find_element_by_xpath(SearchAreaLocators.MAX_MILEAGE)
        SF.select(element_xpath=max_mileage_ele, text=Utils.format_integer(max_mileage) + ' km')

    def select_production_range(self, min_year, max_year):
        """
        Selects production range, i.e. from 1900 to current.
        The ranges MUST MATCH what's on the GUI.
            min_price [str]: 1900
            max_price [str]: 2020
        """    
        self._select_min_year(min_year)
        self._select_max_year(max_year)
    
    def _select_min_year(self, min_year):
        min_year_ele = self.driver.find_element_by_xpath(SearchAreaLocators.MIN_YEAR)
        SF.select(element_xpath=min_year_ele, text=min_year)

    def _select_max_year(self, max_year):
        max_year_ele = self.driver.find_element_by_xpath(SearchAreaLocators.MAX_YEAR)
        SF.select(element_xpath=max_year_ele, text=max_year)

    def select_fuel_type(self, fuel):
        """
        Selects the type of fuel. 
            fuel [str]: diesel|petrol|all
        By default the fuel is set to "all".
        """
        if fuel != 'all':
            fuel_xpath = SearchAreaLocators.FUEL_AREA + f'/span[@data-key="{fuel}"]'
            fuel_ele = WebDriverWait(self.driver, self.TIMEOUT).until(EC.element_to_be_clickable((By.XPATH, fuel_xpath)))
            fuel_ele.click()

    def check_vin_history(self):
        """Clicks on checkbox to show only offers that have VIN history."""
        # vin_btn = self.driver.find_element_by_xpath('//*[@class="search-area__status-label hasVinCheckbox"]')
        vin_btn = WebDriverWait(self.driver, self.TIMEOUT).until(EC.element_to_be_clickable((By.XPATH, SearchAreaLocators.HAS_VIN)))
        vin_btn.click() 

    def click_search(self):
        """Clicks on the search button."""
        search_btn = WebDriverWait(self.driver, self.TIMEOUT).until(EC.element_to_be_clickable((By.XPATH, SearchAreaLocators.SUBMIT))) 
        search_btn.click()
