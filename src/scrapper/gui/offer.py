import logging
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
# GUI
from .basepage import BasePage
from .locators import OfferLocators


class Offer(BasePage):

    TIMEOUT = 10

    def get_location(self):
        location = WebDriverWait(self.driver, self.TIMEOUT).until(
            EC.visibility_of_element_located(OfferLocators.LOCATION)
            )
        return location.text.strip()

    def get_phone_number(self):
        phones = []
        phones_ele = WebDriverWait(self.driver, self.TIMEOUT).until(
            EC.presence_of_all_elements_located(OfferLocators.PHONE)
            )

        for phone in phones_ele:
            click_ele = phone.find_element_by_xpath('span[1]/span[3]')
            ActionChains(self.driver).move_to_element(phone).click(click_ele).perform()

            number_ele = phone.find_element_by_xpath('span[1]/span[2]')
            phone_number = number_ele.text
            print(phone_number)
        return phones

    def get_image_url(self):
        image = WebDriverWait(self.driver, self.TIMEOUT).until(
            EC.visibility_of_element_located(OfferLocators.BASE_IMAGE)
            )
        return image.get_attribute('src')  