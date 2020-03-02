import logging
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
# GUI
from .basepage import BasePage
from .locators import PaginationLocators
from .factory import SeleniumFactory as SF


log = logging.getLogger(__name__)


class Pagination(BasePage):

    TIMEOUT = 10

    @property
    def pagination_root(self):
        return WebDriverWait(self.driver, self.TIMEOUT).until(
            EC.presence_of_element_located(PaginationLocators.PAGINATION_ROOT))

    def get_pages(self):
        pages = WebDriverWait(self.driver, self.TIMEOUT).until(
            EC.presence_of_all_elements_located(PaginationLocators.PAGES)
            )
        SF.move_to(self.driver, self.pagination_root)
        pages.append(self.get_current_page())  # add current page
        return pages

    def get_pages_num(self):
        return len(self.get_pages())

    def get_current_page(self):
        current_page = WebDriverWait(self.driver, self.TIMEOUT).until(
            EC.visibility_of_element_located(PaginationLocators.CURRENT_PAGE)
            )
        return current_page
    
    def get_current_page_num(self):
        return self.get_current_page().text.strip()

    def click_on_page_by_num(self, num):
        page_xpath = (By.XPATH, f'//span[@class="page" and text()="{num}"]/parent::a')
        SF.click_element(self.driver, page_xpath)
    
    def get_page_by_num(self, num):
        pass

    def click_next_page(self):
        SF.move_to(self.driver, self.pagination_root)
        SF.click_element(self.driver, PaginationLocators.NEXT_PAGE)
    
    def click_previous_page(self):
        SF.click_element(self.driver, PaginationLocators.PREVIOUS_PAGE)
    
    def click_first_page(self):
        self.click_on_page_by_num(1)

    def click_last_page(self):
        SF.click_element(self.driver, PaginationLocators.LAST_PAGE)

    def accept_cookies(self):
        SF.click_element(self.driver, PaginationLocators.COOKIE)
