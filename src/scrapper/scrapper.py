import logging
# GUI
from gui.basepage import BasePage
from gui.offer import Offer
from gui.search_area import SearchArea
from gui.detailed_search import DetailedSearch
from gui.pagination import Pagination
from gui.variables import Vars

log = logging.getLogger(__name__)


class Scrapper(BasePage):

    def __init__(self, driver):
        super().__init__(driver)
        self.pagination = Pagination(self.driver)
        self.searchbox = SearchArea(self.driver)
        self.detailed_search = DetailedSearch(self.driver)
        self.offer = Offer(self.driver)

        self.offer_urls = []

    def search(self, data):
        #self.searchbox.select_state_of_use('new')
        self.searchbox.select_car_make('BMW')
        self.searchbox.select_car_model('M4')
        #self.searchbox.select_price_range(2000, 200000)
        #self.searchbox.select_mileage_range(20000, 125000)
        #self.searchbox.select_production_range(2010, 2015)
        #self.searchbox.check_vin_history()
        #self.searchbox.select_fuel_type('diesel')
        self.searchbox.click_search()

    def verify_results(self):
        if not self.detailed_search.is_any_results():
            msg = 'No results'
            raise Exception(msg)
        self.pagination.accept_cookies()

    def get_offer_from_all_pages(self):
        for _ in range(1, self.pagination.get_pages_num()):
            self._get_offers_from_current_page()
            self.pagination.click_next_page()
    
    def _get_offers_from_current_page(self):
        for result in self.detailed_search.get_results():
            offer = self.detailed_search.get_offer_link(result).split('/')[-1]
            self.offer_urls.append(offer)

