from PyQt5.QtWidgets import QLabel, QMainWindow, QApplication, QPushButton, QRadioButton, \
    QCheckBox
from PyQt5 import uic
from maps.main import Dispatcher
from PyQt5.Qt import Qt
from PyQt5.QtGui import QPixmap
import sys


class MapShow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle('')
        uic.loadUi('files/form.ui', self)

        # создаю объект поиска
        self.dp = Dispatcher()

        # кнопка для показа карты
        self.show_map.clicked.connect(self.press_button_show_map)

        # кнопка для поиска объектов по имени
        self.searchbutton.clicked.connect(self.press_search_map)

        # кнопка для очистки поиска
        self.searchbutton_2.clicked.connect(self.click_clear_search)

        # кнопки для переключения типа карты
        self.radioButton.clicked.connect(self.change_radio_button)
        self.radioButton_2.clicked.connect(self.change_radio_button)
        self.radioButton_3.clicked.connect(self.change_radio_button)

        # check-box для приписывания полного адреса
        self.checkBox.clicked.connect(self.click_check_box)

        self.is_clear = False
        self.is_postcode = False

    def set_pixmap(self):
        result = self.dp.get_map_by_ll()
        if not self.is_clear:
            self.dp.get_address()
        self.set_address()
        if result and self.dp.ll is not None:
            self.image_map: QLabel
            pixmap = QPixmap('files/map.png')
            self.image_map.setPixmap(pixmap)
        else:
            self.error_label.setText(result)

    def set_address(self):
        postcode = self.dp.get_postcode()
        address = self.dp.address if not self.is_postcode else f"{self.dp.address} {postcode}"
        self.addres_label.setText(address)

    def press_button_show_map(self):
        self.coords_input: QLabel
        coords = ','.join(self.coords_input.text().strip().split())
        self.dp.ll = coords
        self.dp.points.append(f"{coords},pm2wtm")
        self.set_pixmap()

    # событие смены координат
    def change_map(self):
        try:
            coords = ','.join(self.coords_input.text().strip().split())
            self.set_pixmap()
        except Exception:
            pass
        self.error_label: QLabel
        self.error_label.setText('Вы ввели неверное значение координат!')

    # функция для изменения типа возвращаемой карты
    def change_radio_button(self):
        dates = {"Спутник": "sat", "Гибрид": "sat,skl", "Схема": "map"}
        self.dp.map_type = dates[self.sender().text()]
        self.set_pixmap()

    def press_search_map(self):
        object_name = self.coords_input_2.text()
        self.dp.get_map_by_name(object_name)
        self.set_pixmap()

    def click_clear_search(self):
        self.dp.clean_search()
        self.is_clear = True
        self.set_pixmap()
        self.is_clear = False

    def click_check_box(self):
        self.is_postcode = not self.is_postcode
        self.set_pixmap()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageUp:
            self.dp.scale_down()
            self.set_pixmap()
        if event.key() == Qt.Key_PageDown:
            self.dp.scale_up()
            self.set_pixmap()
        if event.key() == Qt.Key_Up:
            self.dp.move_map_on_direction('вверх')
            self.set_pixmap()
        if event.key() == Qt.Key_Down:
            self.dp.move_map_on_direction('вниз')
            self.set_pixmap()
        if event.key() == Qt.Key_Right:
            self.dp.move_map_on_direction('вправо')
            self.set_pixmap()
        if event.key() == Qt.Key_Left:
            self.dp.move_map_on_direction('влево')
            self.set_pixmap()

    def mousePressEvent(self, event):
        print(f"Координаты:{event.x()}, {event.y()}")
        if event.button() == Qt.LeftButton:
            x, y = event.x() - 30, event.y() - 30
            if 0 <= x <= 650 and 0 <= y <= 450:
                self.dp.get_coords_by_click(coords=[x, y])
                self.set_pixmap()
        elif event.button() == Qt.RightButton:
            x, y = event.x() - 30, event.y() - 30
            if 0 <= x <= 650 and 0 <= y <= 450:
                self.dp.get_biz_by_click(coords=[x, y])
                self.set_pixmap()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    map = MapShow()
    map.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
