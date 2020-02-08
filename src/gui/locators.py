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
    
    