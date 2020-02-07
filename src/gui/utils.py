class Utils:

    @staticmethod
    def parse_price(price):
        return f'{price:,}'.replace(',', ' ') + ' PLN'
