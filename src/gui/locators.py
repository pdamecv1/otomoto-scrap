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