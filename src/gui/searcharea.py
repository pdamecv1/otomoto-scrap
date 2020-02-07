import logging
from selenium import webdriver
# GUI
from basepage import BasePage
from factory import SeleniumFactory as SF
from locators import SearchAreaLocators
from utils import Utils


log = logging.getLogger(__name__)


class SearchArea(BasePage):

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
            make [str]: BMW|Honda, etc.
        """
        make_element = self.driver.find_element_by_xpath(SearchAreaLocators.MAKE)
        SF.select(element=make_element, value=make.lower())

    def select_car_model(self, model):
        """
        Selects model of the car.
            make [str]: BMW|Honda, etc.
        """
        model_element = self.driver.find_element_by_xpath(SearchAreaLocators.MODEL)
        SF.select(element=model_element, text=model)

    def select_price_range(self, min_price, max_price):
        """
        Selects price range, i.e. from 2 000 to 20 000 PLN.
        The ranges MUST MATCH what's on the GUI.
            min_price [int|str]: 2000
            max_price [int|str]: 20000
        """
        self.select_min_price(min_price)
        self.select_max_price(max_price)

    def select_min_price(self, min_price):
        min_price_ele = self.driver.find_element_by_xpath(SearchAreaLocators.MIN_PRICE)
        SF.select(element=min_price_ele, text=Utils.parse_price(min_price))

    def select_max_price(self, max_price):
        max_price_ele = self.driver.find_element_by_xpath(SearchAreaLocators.MAX_PRICE)
        SF.select(element=max_price_ele, text=Utils.parse_price(max_price))

if __name__ == '__main__':
    chrome_options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.get('https://www.otomoto.pl')
    
    ac = SearchArea(driver)
    ac.select_state_of_use('new')
    ac.select_car_make('BMW')
    ac.select_car_model('M8')
    ac.select_price_range(2000, 200000)

    