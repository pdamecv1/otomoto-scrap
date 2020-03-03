import logging
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
# GUI
from .basepage import BasePage
from .locators import OfferLocators
from .variables import Vars, OfferVars
from .factory import SeleniumFactory as SF


class Offer(BasePage):

    TIMEOUT = 10

    def get_offers_data(self, offer_urls):
        offer_data = []
        for offer_url in offer_urls:
            offer_data.append(self.get_offer_data(offer_url))
        return offer_data

    def get_offer_data(self, offer_url):
        offer_url = Vars.OFFER_URL + '/' + offer_url
        SF.get_page(self.driver, offer_url)

        record = {
            'url': offer_url,
            'location': self.get_location(),
            'creation': self.get_creation_time(),
            'image': self.get_image_url(),
            'phone': self.get_phone_number(),
            'description': self.get_description(),
            'specification': self.get_car_spec()
        }
        return record

    def get_description(self):
        description = WebDriverWait(self.driver, self.TIMEOUT).until(
            EC.visibility_of_element_located(OfferLocators.DESCRIPTION)
            )
        return description.text.strip()

    def get_creation_time(self):
        offer_time = WebDriverWait(self.driver, self.TIMEOUT).until(
            EC.visibility_of_element_located(OfferLocators.CREATION_DATE)
            )
        return offer_time.text.strip()

    def get_car_spec(self):
        specification = {}
        for spec_name, gui_spec_translation in OfferVars.CAR_SPEC.items():
            spec_xpath = f'//span[contains(text(), "{gui_spec_translation}")]/following-sibling::div'
            specification[spec_name] = self.driver.find_element_by_xpath(spec_xpath).text.strip()
        return specification

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
