import logging
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
# GUI
from .basepage import BasePage

log = logging.getLogger(__name__)


class SeleniumFactory(BasePage):

    @staticmethod
    def select(element_xpath, **kwargs):
        select = Select(element_xpath)

        for k, v in kwargs.items():
            log.info(f'Selecting "{v}" by "{k}".')

            if not isinstance(v, str):
                v = str(v)

            if k == 'text':
                select.select_by_visible_text(v)
            elif k == 'value':
                select.select_by_value(v)

    @staticmethod
    def click_element(context, element, timeout=10):
        element = WebDriverWait(context, timeout).until(EC.element_to_be_clickable(element))
        element.click()
        log.info(f'Clicked on element: {element}.')

    @staticmethod
    def move_to(context, element):
        ActionChains(context).move_to_element(element).perform()

    @staticmethod
    def get_page(driver, url):
        retry_max = 10
        retry = 0

        while retry <= retry_max:
            try:
                driver.get(url)
                break
            except Exception as e:
                print(e)
                retry += 1
