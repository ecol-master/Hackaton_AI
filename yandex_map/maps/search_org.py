import requests


def find_businesses(ll, address, locale="ru_RU"):
    # поиск организации
    search_api_server = "https://search-maps.yandex.ru/v1/"
    params = {'apikey': 'dda3ddba-c9ea-4ead-9010-f43fbc15c6e3',
              'll': ll, 'type': 'biz',
              'text': address,
              'spn': '0.000000042,0.000000042', 'lang': locale,
              'results': '1'}

    response = requests.get(search_api_server, params=params)
    if not response:
        return None

    response = response.json()
    coords = response['features'][0]['geometry']['coordinates']
    coords = f"{coords[0]},{coords[1]},org"
    return coords
