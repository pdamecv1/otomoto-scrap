import logging
from basepage import BasePage
# GUI
from selenium.webdriver.support.ui import Select


log = logging.getLogger(__name__)


class SeleniumFactory(BasePage):

    @staticmethod
    def select(element, **kwargs):
        select = Select(element)

        for k, v in kwargs.items():
            log.info(f'Selecting "{v}" by "{k}".')

            if not isinstance(v, str):
                v = str(v)

            if k == 'text':
                select.select_by_visible_text(v)
            elif k == 'value':
                select.select_by_value(v)
