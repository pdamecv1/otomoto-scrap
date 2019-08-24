import logging as log
import re
import json
from urllib.request import urlretrieve

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException

class OtoMotoScrapper:
    
    URL = 'https://www.otomoto.pl'

    MAX_RESULTS = 10

    def __init__(self, vehicle_data):
        self.vehicle_data = vehicle_data
        self.vehicle = self.vehicle_data['model'] + ' ' + self.vehicle_data['mark']
        
        self.driver = webdriver.Chrome()
        self.driver.get(OtoMotoScrapper.URL)

        self.data = []

    def get_vehicle_element(self, element, string):
        
        select = Select(element)

        for ele in select.options:
            if string in ele.text:
                log.debug(f'{string} found in element: {ele}')
                ele.click()
                break
            else:
                log.debug(f'{string} not found.')

    def select_vehicle(self):
        select_brand = self.driver.find_element_by_id('param571')
        select_mark = self.driver.find_element_by_id('param573')
        
        self.get_vehicle_element(select_brand, 'BMW')
        self.get_vehicle_element(select_mark, 'M3')
        self.driver.find_element_by_xpath('//*[@id="searchmain_29"]/button[1]').click()

    def get_offer_info(self):
        offer_urls = list(self.get_offer_urls())
        for url in offer_urls:
            self.driver.get(url)
            self.get_specific_offer()

    def get_offer_urls(self):
        for num in range(1, OtoMotoScrapper.MAX_RESULTS + 1):
            element = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, f'//*[@id="body-container"]/div[2]/div[1]/div/div[1]/div[4]/article[{num}]'))
            )
            num += 1
            yield element.get_attribute('data-href')

    def get_specific_offer(self):
        price = self.driver.find_element_by_class_name('offer-price').get_attribute('data-price')

        # attempt = 1
        # max_attempts = 5
        # self.driver.implicitly_wait(4) #
        # phone_number = self.driver.find_element_by_xpath('//*[@id="siteWrap"]/main/section/div[3]/div[2]/span/span/span[3]').click()

        # while True:
        #     try:
        #         phone_number = self.driver.find_element_by_xpath('//*[@id="siteWrap"]/main/section/div[3]/div[2]/span/span/span[2]').text
        #         break
        #     except StaleElementReferenceException:
        #         if attempt == max_attempts:
        #             raise
        #         attempt += 1
        
        phone_number = self.driver.find_element_by_xpath('//*[@id="siteWrap"]/main/section/div[3]/div[2]/span/span/span[3]').click()
        phone_number = self.driver.find_element_by_xpath('//*[@id="siteWrap"]/main/section/div[3]/div[2]/span/span/span[2]').text

        car_image_url = self.driver.find_element_by_xpath('//*[@id="offer-photos"]/div[2]/div/div/div[1]/div/div/img').get_attribute('src')

        # Download file locally.
        urlretrieve(car_image_url, f'{phone_number}-car.jpg')

        # Save data
        self.data.append({
                'car': self.vehicle, 
                'price':price, 
                'contact': phone_number, 
                'image': car_image_url
            }) 
        
    def test(self):
        self.select_vehicle()
        self.get_offer_info()

        self.save_data(self.data)

    @staticmethod
    def save_data(data):
        with open('test.json', 'w') as f:
            json.dump(data, f, indent=4) 

    def clean(self):
        self.driver.close()
    

data = {'model': 'BMW', 'mark': 'M3'}

sc = OtoMotoScrapper(vehicle_data=data)
sc.test()


