import logging
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
# GUI
from .basepage import BasePage
from .locators import DetailedSearchLocators as DSLocators


log = logging.getLogger(__name__)


class DetailedSearch(BasePage):
    """
    Class contains all methods linked to detailed search page: 
        https://www.otomoto.pl/ + osobowe|czesci|motocykle-i-quady
    The page also contains the search results.
    """
    
    TIMEOUT = 10

    def get_results(self):
        results = WebDriverWait(self.driver, self.TIMEOUT).until(
            EC.presence_of_all_elements_located((By.XPATH, DSLocators.RESULT))
            )
        return results

    def is_any_results(self):
        try:
            _ = WebDriverWait(self.driver, self.TIMEOUT).until(
                    EC.visibility_of_element_located((By.XPATH, DSLocators.NO_RESULTS))
                )
            return False
        except TimeoutException:
            return True

    @staticmethod
    def get_offer_link(context):
        """Returns link element (a) pointing to detailed offer
        """
        return WebDriverWait(context, DetailedSearch.TIMEOUT).until(
            EC.visibility_of_element_located((By.XPATH, '.' + DSLocators.OFFER_LINK))
            ).get_attribute('href')
