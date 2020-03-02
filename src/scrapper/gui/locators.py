from selenium.webdriver.common.by import By  # TODO: change all elements to By


class SearchAreaLocators:
    SEARCH_AREA = '//div[contains(@class, "om-searcharea")]'
    
    CATEGORIES = SEARCH_AREA + '//div[contains(@class, "categories-main-block")]'
    CONTENT = SEARCH_AREA + '//div[contains(@class, "om-tabs-content")]'

    # Car State
    CAR_STATE_AREA = CONTENT + '//*[contains(@class, "search-area__form")]'

    # Make and Model
    # MAKE_AREA = CONTENT + '//*[@data-key="make"]'  # TODO: check why MAKE|MODLE does not work with it.
    MAKE = '//select[@id="param571"]'
    MODEL = '//select[@id="param573"]'

    # Price
    PRICE_AREA = CONTENT + '//div[@data-key="price"]'
    MIN_PRICE = PRICE_AREA + '/span[1]//select'
    MAX_PRICE = PRICE_AREA + '/span[2]//select'

    # Mileage
    MILEAGE_AREA = CONTENT + '//div[@data-key="mileage"]'
    MIN_MILEAGE = MILEAGE_AREA + '/span[1]//select'
    MAX_MILEAGE = MILEAGE_AREA + '/span[2]//select'

    # Production
    PRODUCTION_AREA = CONTENT + '//div[@data-key="year"]'
    MIN_YEAR = PRODUCTION_AREA + '/span[1]//select'
    MAX_YEAR = PRODUCTION_AREA + '/span[2]//select'

    # Fuel type
    FUEL_AREA = CONTENT + '//div[@data-key="fuel_type"]'

    # VIN history
    HAS_VIN = CONTENT + '//div[@data-key="has_vin"]/label[2]'
    
    # Search button
    SUBMIT = CONTENT + '//button[@type="submit"]'


class DetailedSearchLocators:
    HEADER_ROOT = '//header[@class="header-container"]'
    DETAILED_PARAMS_ROOT = '//fieldset[@id="paramsList"]'
    SEARCH_RESULTS_ROOT = '//div[@id="listContainer"]'

    RESULTS = SEARCH_RESULTS_ROOT + '//div[@class="offers list"]'
    RESULT = RESULTS + '//article'
    OFFER_LINK = '//h2/a'

    NO_RESULTS = '//div[@class="om-emptyinfo"]'


class PaginationLocators:
    PAGINATION_ROOT = (By.XPATH, '//ul[@class="om-pager rel"]')
    NEXT_PAGE = (By.XPATH, PAGINATION_ROOT[1] + '//li[@class="next abs"]/a')
    PREVIOUS_PAGE = (By.XPATH, PAGINATION_ROOT[1] + '//li[@class="prev abs"]/a')
    LAST_PAGE = (By.XPATH, PAGINATION_ROOT[1] + '/li[last()]')
    CURRENT_PAGE = (By.XPATH, PAGINATION_ROOT[1] + '//li[@class="active"]')
    PAGES = (By.XPATH, PAGINATION_ROOT[1] + '//span[@class="page"]/parent::a')

    COOKIE = (By.XPATH, '//*[@id="cookiesBar"]/div/div/a')


class OfferLocators:
    PRICE = (By.XPATH, '//span[@class="offer-price__number"]')
    CURRENCY = (By.XPATH, '//span[@class="offer-price__currency"]')

    LOCATION = (By.XPATH, '//span[@class="seller-box__seller-address__label"]')
    BASE_IMAGE = (By.XPATH, '//div[@class="photo-item"]/img')

    PHONES_ROOT = '//div[@class="seller-phones"]'
    PHONE = (By.XPATH, PHONES_ROOT + '/div[@class="number-box newPhoneStyle"]')
    CLICK_PHONE = (By.XPATH, PHONES_ROOT + '//a[@class="spoiler seller-phones__button"]')

    OFFER_PARAMS_ROOT = '//div[@class="offer-params"]'