from apikeys import key_geocoder
import requests
import json


def get_ll_by_name(name, pt=False):
    name = ''.join(name.split())
    req = f"http://geocode-maps.yandex.ru/1.x/?apikey={key_geocoder}&geocode={name}&size=650,450&format=json"
    response = requests.get(req)
    # with open('response.json', 'w') as jsonfile:
    #     json.dump(response.json(), jsonfile)
    ll = response.json()['response']["GeoObjectCollection"]["featureMember"][0][
        "GeoObject"]['Point']['pos'].split()
    ll = ','.join(ll)
    return ll
 


# перемещает карту в зависимости от указанного направления
def move_map(direction, ll, spn_x, spn_y):
    size = "650,450"
    if ll is None:
        return ll
    ll = [float(i) for i in ll.split(',')]
    if direction == 'вверх' or direction == 'вниз':
        if ll[1] + spn_y <= 90 and direction == 'вверх':
            ll[1] = ll[1] + spn_y
        elif ll[1] - spn_y >= -90 and direction == 'вниз':
            ll[1] -= spn_y
    else:
        if ll[0] + spn_x <= 180 and direction == 'вправо':
            ll[0] += spn_x
        elif ll[0] - spn_x >= -180:
             ll[0] -= spn_x
        # ll[0] = ll[0] + spn_x if direction == 'вправо' else ll[0] - spn_x
    return ','.join([str(i) for i in ll])


# функция получает объект со списком объектов геокодера
# она пробегается по всем объектам и если находит нужно поле то останавливает работу и
# возвращает полученный адрес
def range_geoobject(geoobject):
    address = None
    for i in geoobject:
        try:
            address = i["GeoObject"]["metaDataProperty"] \
                ["GeocoderMetaData"]["text"]
            break
        except Exception as e:
            pass
    if address is not None:
        return address
    return '---адрес не был получен---'


# функция по координатам находит находит адрес объекта используя выше указанную функцию
def get_address(ll):
    req = f"http://geocode-maps.yandex.ru/1.x/?apikey={key_geocoder}&geocode={ll}&format=json"
    response = requests.get(req)
    with open('response.json', 'w') as jsonfile:
        json.dump(response.json(), jsonfile, ensure_ascii=False)
    address = range_geoobject(
        response.json()['response']["GeoObjectCollection"]["featureMember"])
    return address


def get_postcode_range(toponym):
    postcode = None
    for i in toponym:
        try:
            postcode = i['GeoObject']['metaDataProperty']['GeocoderMetaData']['Address'][
                'postal_code']
        except Exception:
            pass
    if postcode is None:
        return ''
    else:
        return postcode


def get_postcode_low(points):
    try:
        ll = ','.join(points[0].split(',')[:2])
        req = f"http://geocode-maps.yandex.ru/1.x/?apikey={key_geocoder}&geocode={ll}&format=json"
        response = requests.get(req)
        with open('response.json', 'w') as jsonfile:
            json.dump(response.json(), jsonfile, ensure_ascii=False)
        toponym = response.json()["response"]["GeoObjectCollection"]["featureMember"]
        postcode = get_postcode_range(toponym)
        return postcode
    except Exception:
        return ''


def get_ll_by_click(ll, spn_x, spn_y, coords):
    x, y = coords
    ll = [float(i) for i in ll.split(',')]
    ll = [ll[0] - spn_x * 1.5, ll[1] + spn_y * 3 / 4]
    ll_x = (x / 650) * 3 * spn_x + ll[0]
    if 375 > y > 225:
        plus = 50
    elif y > 225:
        plus = 80
    else:
        plus = 20
    ll_y = ll[1] - ((y + plus) / 450) * 4 * spn_y / 3
    ll = f"{ll_x},{ll_y}"
    return ll
