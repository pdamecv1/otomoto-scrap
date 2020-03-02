import logging
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
# GUI
from .basepage import BasePage
from .locators import OfferLocators
from .variables import Vars


class Offer(BasePage):

    TIMEOUT = 10

    def get_offers_data(self, offer_urls):
        offer_data = []
        for offer_url in offer_urls:
            offer_data.append(self._get_offer_data(offer_url))
            from pprint import pprint
            pprint(offer_data)
        return offer_data

    def _get_offer_data(self, offer_url):
        offer_url = Vars.OFFER_URL + '/' + offer_url
        self.driver.get(offer_url)

        record = {
            'offerUrl': offer_url,
            'location': self.get_location(),
            'imgUrl': self.get_image_url(),
            'phone': self.get_phone_number(),
            'carSpec': self.get_car_spec()
        }
        return record

    def get_car_spec(self):
        record = {
            'make': 
        }
        pass

    def get_location(self):
        location = WebDriverWait(self.driver, self.TIMEOUT).until(
            EC.visibility_of_element_located(OfferLocators.LOCATION)
            )
        return location.text.strip()

    def get_phone_number(self):
        phones = []
        # phones_ele = WebDriverWait(self.driver, self.TIMEOUT).until(
        #     EC.presence_of_all_elements_located(OfferLocators.PHONE)
        #     )

        # for phone in phones_ele:
        #     import pdb; pdb.set_trace()
        #     spoil_phone = self.driver.find_element_by_xpath(f'.//a')
        #     spoil_phone.click()
        return phones

    def get_image_url(self):
        image = WebDriverWait(self.driver, self.TIMEOUT).until(
            EC.visibility_of_element_located(OfferLocators.BASE_IMAGE)
            )
        return image.get_attribute('src') 
