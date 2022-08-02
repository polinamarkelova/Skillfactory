import json
import requests
from config import currencies


class APIException(Exception):
    pass


class Convertor:
    @staticmethod
    def get_value(base, quote, amount):
        try:
            base_key = currencies[base.lower()]
        except KeyError:
            raise APIException(f'Валюта {base}, что вы ввели, не была найдена в базе. Перепроверьте данные.')

        try:
            quote_key = currencies[quote.lower()]
        except KeyError:
            raise APIException(f'Валюта {quote}, что вы ввели, не была найдена в базе. Перепроверьте данные.')

        if base_key == quote_key:
            raise APIException(f'Вы не можете конвертировать одинаковые валюты {base}')

        try:
            amount == float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}. Перепроверьте данные.')

        r = requests.get(f"https://min-api.cryptocompare.com/data/price?fsym={base_key}&tsyms={quote_key}")
        resp = json.loads(r.content)
        new_value = resp[quote_key] * float(amount)
        new_value = round(new_value, 3)
        return new_value
