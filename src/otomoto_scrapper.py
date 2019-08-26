import os
import re
import json
import csv
import logging as log
from urllib.request import urlretrieve
from .settings import URL, DOCKER_ARGS, SCRAP_PATH, LOG_PATH

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException


logger = log.getLogger(__name__)


class OtoMotoScrapper:

    MAX_RESULTS = 10

    def __init__(self, input_data):
        """Scrapper used for automating specific car search at https://www.otomoto.pl.

        Arguments:
        input_data -- data to control workflow of automation. Example in input.json
            car_spec -- contains fields for searchbox on main page.
                *model -- BMW / Audi
                *mark  -- M3 / Q4
            results -- number of pages to be scrapped.
            download_file -- whether to download car image locally in artifacts.

        * Required fields.
        """
        self.car_data = input_data['car_spec']
        self.is_download = input_data.get('download_image', False)
        self.max_results = input_data.get('results', self.MAX_RESULTS)

        self.vehicle = self.car_data['model'] + ' ' + self.car_data['mark']
        
        self.driver = self.estabilish_driver()
        self.driver.get(URL)

        self.data = []

    def estabilish_driver(self):
        """
        Creates chromedriver instance with arguments.
        
        If used inside Docker, specify env variable: SCRAPPER_ENV=DOCKER
        to inject additional arguments to driver for stability.
        """
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument(f'--log-path={LOG_PATH}/chromedriver.log')

        if os.environ.get('SCRAPPER_ENV', '') == 'DOCKER':
            for arg in DOCKER_ARGS:
                chrome_options.add_argument(f'--{arg}')
    
        return webdriver.Chrome(chrome_options=chrome_options)

    @staticmethod
    def select_vehicle_element(element, string):
        """
        Selects vehicle's model, mark, price range, etc. from select element
        that is located in search box at main page: https://www.otomoto.pl

        Arguments:
        element -- selenium select node
        string  -- desired word, i.e. BMW, M3, etc.
        """
        select = Select(element)

        element = None
        for ele in select.options:
            if string in ele.text:
                element = ele
                logger.info(f'{string} found in: {ele}')
                ele.click()
                break

        if element is None:
            logger.info(f'{string} not found in: {select}')

    def search_vehicle(self):
        select_brand = self.driver.find_element_by_id('param571')
        select_mark = self.driver.find_element_by_id('param573')
        
        self.select_vehicle_element(select_brand, '')  # brand / BMW
        self.select_vehicle_element(select_mark, 'M3')  # mark / M3
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
        for num in range(1, self.max_results + 1):
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

        # Downloads car image locally.
        if self.is_download:
            image = f'{self.vehicle}_{phone_number}.jpg'.replace(' ', '_')
            self.download_car_image(car_image_url, image)

        return {'price': price, 'contact': phone_number, 'image': car_image_url} 
        
    def download_car_image(self, url, name):
        """Downloads car image.

        Arguments:
        url -- url of an image
        name -- filename
        """
        image_path = os.path.join(SCRAP_PATH, 'images')
        if not os.path.exists(image_path):
            os.mkdir(image_path)
        urlretrieve(url, f'{image_path}/{name}')

    @staticmethod
    def save_data(data):
        """Saves data to txt and json files.

        Arguments:
        data --  example data structure can be found in README.MD
        """
        filename = os.path.join(SCRAP_PATH, 'otomoto_scrap')
        
        with open(f'{filename}.json', 'w') as f:
            json.dump(data, f, indent=4)

        logger.info(f'Data saved to {filename}.json')
        
        with open(f'{filename}.txt', 'w', newline='') as csvfile:
            carwriter = csv.writer(csvfile, delimiter=',')
            carwriter.writerow(['car', 'price', 'contact', 'url', 'image'])
            for i in data:
                car = i['car']
                for d in i['results']:
                    carwriter.writerow([car, d['price'], d['contact'], d['url'], d['image']])
        
        logger.info(f'Data saved to {filename}.txt')
    
    def clean(self):
        """Closes chromdriver instance."""
        self.driver.close()

    def scrap(self):
        self.search_vehicle()
        self.get_offer_info()

        self.save_data(self.data)
        self.clean()