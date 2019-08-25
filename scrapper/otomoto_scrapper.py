import logging as log
import os
import re
import json
import csv
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
    LOG_PATH = 'artifacts/logs'
    SCRAP_PATH = 'artifacts/scrapper'

    DOCKER_ARGS = ['verbose', 'headless', 'disable-gpu', 'no-sandbox']

    MAX_RESULTS = 2

    def __init__(self, vehicle_data):
        self.vehicle_data = vehicle_data
        self.vehicle = self.vehicle_data['model'] + ' ' + self.vehicle_data['mark']
        
        self.prepare_artifacts()

        self.driver = self.estabilish_driver()
        self.driver.get(OtoMotoScrapper.URL)

        self.data = []

    def prepare_artifacts(self):
        for _path in [self.LOG_PATH, self.SCRAP_PATH]:
            if not os.path.exists(_path):
                os.makedirs(_path)

    def estabilish_driver(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument(f'--log-path={self.LOG_PATH}/chromedriver.log')

        if os.environ.get('SCRAPPER_ENV', '') == 'DOCKER':
            for arg in self.DOCKER_ARGS:
                chrome_options.add_argument(f'--{arg}')
    
        return webdriver.Chrome(chrome_options=chrome_options)

    def select_vehicle_element(self, element, string):
        """
        Selects vehicle element: model, mark, price, etc.
        """
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
        
        self.select_vehicle_element(select_brand, 'BMW')
        self.select_vehicle_element(select_mark, 'M3')
        self.driver.find_element_by_xpath('//*[@id="searchmain_29"]/button[1]').click()

    def get_offer_info(self):
        results = []

        offer_urls = list(self.get_offer_urls())
        for url in offer_urls:
            self.driver.get(url)

            results2 = self.get_specific_offer_info()
            results2.update({'url': url})
            results.append(results2)
        
        self.data.append({'car': self.vehicle, 'additionalInfo': [], 'results': results})

    def get_offer_urls(self):
        for num in range(1, OtoMotoScrapper.MAX_RESULTS + 1):
            element = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, f'//*[@id="body-container"]/div[2]/div[1]/div/div[1]/div[4]/article[{num}]'))
            )
            num += 1
            yield element.get_attribute('data-href')

    def get_specific_offer_info(self):
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
        #phone_number = self.driver.find_element_by_class_name('phone-n$numberBoxumber.seller-phones__number').text
        self.driver.implicitly_wait(10)
        phone_number = self.driver.find_element_by_xpath('//*[@id="siteWrap"]/main/section/div[3]/div[2]/span/span/span[2]').text

        car_image_url = self.driver.find_element_by_xpath('//*[@id="offer-photos"]/div[2]/div/div/div[1]/div/div/img').get_attribute('src')

        # Download car image locally.
        image = f'{self.vehicle}_{phone_number}.jpg'.replace(' ', '_')
        self.download_car_image(car_image_url, image)

        return {'price': price, 'contact': phone_number, 'image': car_image_url} 
        
    def test(self):
        self.select_vehicle()
        self.get_offer_info()

        self.save_data(self.data)

    @staticmethod
    def download_car_image(url, name):
        image_path = os.path.join(OtoMotoScrapper.SCRAP_PATH, 'images')
        if not os.path.exists(image_path):
            os.mkdir(image_path)
        urlretrieve(url, f'{image_path}/{name}')

    @staticmethod
    def save_data(data):
        """
        Saves results to txt and json files.
        :param data = 
        """
        filename = os.path.join(OtoMotoScrapper.SCRAP_PATH, 'otomoto_scrap')
        
        with open(f'{filename}.json', 'w') as f:
            json.dump(data, f, indent=4)

        log.info(f'Data saved to {filename}.json')
        
        with open(f'{filename}.txt', 'w', newline='') as csvfile:
            carwriter = csv.writer(csvfile, delimiter=',')
            carwriter.writerow(['Car', 'Price', 'Contact', 'Url', 'Image'])
            for i in data:
                car = i['car']
                for d in i['results']:
                    carwriter.writerow([car, d['price'], d['contact'], d['url'], d['image']])
        
        log.info(f'Data saved to {filename}.txt')
    
    def clean(self):
        self.driver.close()
    

if __name__ == '__main__':
    data = {'model': 'BMW', 'mark': 'M3'}

    sc = OtoMotoScrapper(vehicle_data=data)
    sc.test()
