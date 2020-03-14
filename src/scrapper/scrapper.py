import logging
import sys
# GUI
from gui.basepage import BasePage
from gui.offer import Offer
from gui.search_area import SearchArea
from gui.detailed_search import DetailedSearch
from gui.pagination import Pagination
from gui.variables import Vars


log = logging.getLogger(__name__)


class SearchInfo:
    MAKE = ''       
    MODEL = ''       
    STATE = ''    
    MIN_PRICE = 0   
    MAX_PRICE = 0     
    MIN_MILEAGE = 0    
    MAX_MILEAGE = 0     
    MIN_YEAR = 0   
    MAX_YEAR = 0   
    HAS_VIN = False   
    FUEL_TYPE = ''      

    RESULTS = 0

    def __init__(self, data):
        self.data = data
        self.set_car_specification()
        self.set_max_results()

    def set_car_specification(self):
        for spec_name, spec_value in self.data['car_spec'].items():
            setattr(self, spec_name.upper(), spec_value)

    def set_max_results(self):
        self.RESULTS = self.data['results']


class Scrapper(BasePage):

    def __init__(self, driver, data):
        super().__init__(driver)
        self.search_info = SearchInfo(data)
        
        self.pagination = Pagination(self.driver)
        self.searchbox = SearchArea(self.driver)
        self.detailed_search = DetailedSearch(self.driver)
        self.offer = Offer(self.driver)

    def search(self):
        self.searchbox.select_state_of_use(self.search_info.STATE)
        self.searchbox.select_car_make(self.search_info.MAKE)
        self.searchbox.select_car_model(self.search_info.MODEL)
        self.searchbox.select_price_range(self.search_info.MIN_PRICE, 
                                          self.search_info.MAX_PRICE)
        self.searchbox.select_mileage_range(self.search_info.MIN_MILEAGE, 
                                            self.search_info.MAX_MILEAGE)
        self.searchbox.select_production_range(self.search_info.MIN_YEAR, 
                                               self.search_info.MAX_YEAR)
        self.searchbox.select_fuel_type(self.search_info.FUEL_TYPE)
        if self.search_info.HAS_VIN:
            self.searchbox.check_vin_history()
        self.searchbox.click_search()

    def verify_results(self):
        if not self.detailed_search.is_any_results():
            print(f'No results found for: {self.search_info.__dict__}')
            sys.exit()
        self.pagination.accept_cookies()

    def get_offer_data(self):
        offer_urls = self.get_offer_urls()
        yield self.offer.get_offers_data(offer_urls)

    def get_offer_urls(self):
        pages_num = self.pagination.get_pages_num()
        if pages_num > 1:
            offer_urls = self._get_offers_from_all_pages()
        else:
            offer_urls = list(self._get_offers_from_current_page())
        log.info(f'"{len(offer_urls)}" found for "{pages_num}" pages.')
        return offer_urls

    def _get_offers_from_all_pages(self): 
        offer_urls = []
        for _ in range(1, self.pagination.get_pages_num()):
            offer_urls += list(self._get_offers_from_current_page())
            if len(offer_urls) > self.search_info.RESULTS:
                del offer_urls[self.search_info.RESULTS:]
                break
            self.pagination.click_next_page()
        return offer_urls

    def _get_offers_from_current_page(self):
        for result in self.detailed_search.get_results():
            yield self.detailed_search.get_offer_link(result).split('/')[-1]
