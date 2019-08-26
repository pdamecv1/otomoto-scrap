import os
import re
import json
import csv
import logging as log
from urllib.request import urlretrieve
from .settings import URL, DOCKER_ARGS, SCRAP_PATH, LOG_PATH
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException


logger = log.getLogger(__name__)


class OtoMotoScrapper:

    MAX_RESULTS = 10

    def __init__(self, input_data):
        """Scrapper used for automating specific car search at https://www.otomoto.pl.

        Arguments:
        input_data -- data to control workflow of automation. Example in input.json
            car_spec -- contains fields for searchbox on main page.
                *make   -- BMW | Audi
                *model  -- M3  | Q4
            results -- number of offers to be scrapped.
            download_file -- whether to download car image locally in artifacts.

        * Required fields, rest is optional.
        """
        self.car_data = input_data['car_spec']
        self.is_download = input_data.get('download_image', False)
        self.max_results = input_data.get('results', self.MAX_RESULTS)

        self.vehicle = self.car_data['make'] + ' ' + self.car_data['model']
        
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

    def search_vehicle(self):
        make_ele = self.driver.find_element_by_id('param571')
        model_ele = self.driver.find_element_by_id('param573')

        self.select_vehicle_element(make_ele, self.car_data['make'])  # BMW
        self.select_vehicle_element(model_ele, self.car_data['model'])  # M3

        self.driver.find_element_by_xpath('//*[@id="searchmain_29"]/button[1]').click()

    def select_vehicle_element(self, element, string):
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
                element.click()
                break

        if element is None:
            logger.info(f'{string} not found in: {select}')

    def get_available_offers(self):
        """Gets available offers in range of max results."""
        offers = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'om-list-container'))
        )
        articles = offers.find_elements_by_tag_name('article')
        log.info(f'Number of found offers: {len(articles)}')

        # Drop results being out of desired range.
        if len(articles) > self.max_results:
            del articles[self.max_results:]
            log.info(f'Reducing offer results to satisfy desired range: {self.max_results}')
        return articles

    def get_offer_urls(self):
        """Gets url of an offer"""
        articles = self.get_available_offers()

        for article in articles:
            ActionChains(self.driver).move_to_element(article).perform()
            yield article.get_attribute('data-href')

    def get_offer_info(self):
        """
        Gets information per offer.
        Returns final data that will be later saved in artifacts and/or put to DB.
        """
        results = []

        offer_urls = list(self.get_offer_urls())
        for url in offer_urls:
            self.driver.get(url)

            offer_info = self.get_specific_offer_info()
            offer_info.update({'url': url})
            results.append(offer_info)
        
        self.data.append({'car': self.vehicle, 'additionalInfo': [], 'results': results})

    def get_specific_offer_info(self):
        """Gets price, contact, car image."""
        # Price
        price_ele = self.driver.find_element_by_class_name('offer-price')
        price = price_ele.get_attribute('data-price')

        # Phone number
        try:
            con_ele = self.driver.find_element_by_class_name('seller-phones')

            # con_ele= WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'seller-phones')))
            click_ele = con_ele.find_element_by_xpath('span[1]/span[3]')
            ActionChains(self.driver).move_to_element(con_ele).click(click_ele).perform()

            time.sleep(10)  # TBD: change logic for ensuring the number is visible.
            number_ele = con_ele.find_element_by_xpath('span[1]/span[2]')
            phone_number = number_ele.text
        except NoSuchElementException as e:
            phone_number = None
            logger.info(f'Phone number was not provided for {self.driver.current_url}')
            logger.error(e)

        # Image
        try:
            img_ele = self.driver.find_element_by_class_name('photo-item')
            car_image_url = img_ele.find_element_by_xpath('img[1]').get_attribute('src')
        except NoSuchElementException as e:
            car_image_url = None
            logger.info(f'Car image does not exist for offer: {self.driver.current_url}')
            logger.error(e)

        # Downloads car image locally.
        if self.is_download and car_image_url is not None:
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
        data -- example data structure can be found in README.MD
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