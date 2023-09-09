import requests
from maps.geocoder import get_ll_by_name, move_map, get_address, get_postcode_low, \
    get_ll_by_click
from maps.points import get_points, Point
from maps.search_org import find_businesses

"""класс для управления"""



class Dispatcher:
    def __init__(self):
        self.map_type = 'map'
        self.size = "650,450"
        self.ll = None
        self.spn_x, self.spn_y = 1.164530999, 0.806213076
        self.points = get_points()
        self.address = ''
    
    def get_map_by_ll(self, point=None):
        if self.ll is None:
            return 'Вы еще не выбрали точку'
        map_request = f"http://static-maps.yandex.ru/1.x/?ll={self.ll}&size={self.size}&spn={self.spn_x},{self.spn_y}&l={self.map_type}"
        if point:
            self.points.append(point)

        if self.points:
            fn = lambda point: f"{point.latitude},{point.longitude},{point.letter}"
            map_request += f"&pt={'~'.join([fn(point) for point in self.points])}"

        response = requests.get(map_request)

        if not response:
            message = f"Ошибка выполнения запроса. Http статус: {response.status_code} ({response.reason})"
            return message

        # Запишем полученное изображение в файл.
        map_file = "files/map.png"
        try:
            with open(map_file, "wb") as file:
                file.write(response.content)
            return True
        except IOError as ex:
            return "Что то пошло не так"

    def get_map_by_name(self, name):
        ll = get_ll_by_name(name)
        self.ll = ll
        
        lt, lg = [float(i) for i in ll.split(",")]
        # self.points.append(
        #     Point(
        #         letter="pm2rdm",
        #         longitude=lg,
        #         latitude=lt)
        #     )
        
        self.get_map_by_ll()
        self.spn_x, self.spn_y = 1.164530999, 0.806213076

    def move_map_on_direction(self, direction):
        ll = move_map(direction=direction, ll=self.ll, spn_x=self.spn_x, spn_y=self.spn_y)
        self.ll = ll

    def get_address(self):
        address = get_address(ll=','.join(f"{point.latitude},{point.longitude},{point.letter}" for point in self.points ))
        self.address = address

    def get_postcode(self):
        return get_postcode_low(self.points)

    def get_coords_by_click(self, coords):
        if self.ll is not None:
            ll_point = get_ll_by_click(ll=self.ll, spn_y=self.spn_y, spn_x=self.spn_x,
                                       coords=coords)
            print(ll_point)
            lt, lg = [float(i) for i in ll_point.split(",")]
            self.points.append(
                Point(
                    letter="pm2rdm",
                    longitude=lg,
                    latitude=lt)
                ) 
            # self.points.append(f"{ll_point},pm2rdm")

    def scale_up(self):
        if self.spn_x < 1.164530999 * 2 ** 6:
            self.spn_x *= 2
            self.spn_y *= 2
        self.get_map_by_ll()

    def scale_down(self):
        if 1.164530999 / self.spn_x < 2 ** 12:
            self.spn_x /= 2
            self.spn_y /= 2
        self.get_map_by_ll()

    def get_biz_by_click(self, coords):
        if self.ll is not None:
            ll_point = get_ll_by_click(ll=self.ll, spn_y=self.spn_y, spn_x=self.spn_x,
                                       coords=coords)
            address = get_address(ll=self.ll)
            biz = find_businesses(ll_point, address=address)
            self.points = [biz]

    def clean_search(self, flag=False):
        if not flag:
            self.points = self.points[:-1]
        else:
            self.points = []
        self.address = ''
