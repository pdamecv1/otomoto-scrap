import json


class Utils:    

    @staticmethod
    def format_integer(value):
        return f'{value:,}'.replace(',', ' ')

    @staticmethod
    def parse_json(filename):
        with open(filename, 'r') as f:
            return json.load(f)
