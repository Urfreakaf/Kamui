from PySide6.QtWidgets import QApplication, QScrollArea, QTabWidget, QWidget, QVBoxLayout, QLabel, QTextEdit, QHBoxLayout, QRadioButton, QPushButton
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QIcon, QPixmap, QImage
import base64
from PIL import Image
from io import BytesIO
from food import Food
from icon.add import add_image_base64
from button_function import Add

class MainWindow(QScrollArea):
    def __init__(self):
        super().__init__()
        self.add_class = Add()

    def set_Ui(self):
    # MainWindow
        self.setWindowTitle("居")
        self.resize(600, 800)
        self.setWidgetResizable(True)

    # Widget
        self.windows = QTabWidget(self)
        self.windows.setGeometry(0, 0, 600, 800)

        tab_list = ["食事", "酒水"]

    # Attendee List
        with open(r"data\出席.txt", "r", encoding="utf-8") as a_list:
            for line in a_list:
                tab_list.append(line.strip())

        tab_list.append("金額")

        self.tab_dict = {}

    # Add icon
        add_image_data = base64.b64decode(add_image_base64)
        add_image = Image.open(BytesIO(add_image_data))
        add_img_byte_arr = BytesIO()
        add_image.save(add_img_byte_arr, format='PNG')
        add_qimage = QImage.fromData(add_img_byte_arr.getvalue())
        add_pixmap = QPixmap.fromImage(add_qimage)
        self.add_icon = QIcon(add_pixmap)

    # Add Tab
    # Attendee：self.tab_dict
        for i in range(len(tab_list)):
            tab_text = f"{tab_list[i]}"
            scroll_area = QScrollArea()
            scroll_area.setWidgetResizable(True)
            if tab_text == "食事":
                self.food_tab = QWidget()
                scroll_area.setWidget(self.food_tab)
                self.windows.addTab(scroll_area, tab_text)
            elif tab_text == "酒水":
                self.drink_tab = QWidget()
                scroll_area.setWidget(self.drink_tab)
                self.windows.addTab(scroll_area, tab_text)
            elif tab_text == "金額":
                self.money_tab = QWidget()
                scroll_area.setWidget(self.money_tab)
                self.windows.addTab(scroll_area, tab_text)
            else:
                tab_widget = QWidget()
                scroll_area.setWidget(tab_widget)
                self.windows.addTab(scroll_area, tab_text)
                self.tab_dict[tab_text] = tab_widget

        tab_count = self.windows.count()
        self.tab_fixed_width = (self.windows.width() - 30)/ tab_count
        self.windows.setStyleSheet(f"""
            QTabBar::tab {{
                width: {self.tab_fixed_width}px;
                height: 40px
            }}
            QTabBar::tab:selected{{
                width: {self.tab_fixed_width + 30}px;
            }}
        """)

    # Add option in food page
    # Count how many dishes：food_count_dict：{Type:{Meal:[button, price, count]}}
        self.food_count_dict = {}
        food_label_font = QFont()
        food_label_font.setPixelSize(18)
        food_option_font = QFont()
        food_option_font.setPixelSize(14)
        food_button = QPushButton(self.food_tab)
        food_button.setText("輸入")
        food_button.clicked.connect(lambda: self.add_food_option(self.food_count_dict, self.ppl_layout))
        food_button.setGeometry(450, 20, 100, 40)
        food_layout = QVBoxLayout(self.food_tab)
        food_block = QWidget()
        food_block.setFixedSize(400, 60)
        food_menu = QWidget()
        food_layout.addWidget(food_block)
        food_layout.addWidget(food_menu)
        self.food_frant = QHBoxLayout(food_menu)
        self.food_left = QWidget()
        self.food_layout1 = QVBoxLayout()
        self.food_layout1.setSizeConstraint(QVBoxLayout.SetMinAndMaxSize)
        self.food_left.setLayout(self.food_layout1)
        self.food_right = QWidget()
        self.food_layout2 = QVBoxLayout()
        self.food_layout2.setSizeConstraint(QVBoxLayout.SetMinAndMaxSize)
        self.food_right.setLayout(self.food_layout2)
        self.food_right.resize(250, 800)
        self.food_left.resize(250, 800)
        menu_path = r"data\食事.xlsx"
        food = Food(menu_path)
        food_dict = food.read_excel()
        food_types = food_dict.keys()
        price_label_1 = QLabel(self.food_left)
        price_label_1.setGeometry(170, -10, 40, 40)
        price_label_1.setText("價格")
        price_label_1.setFont(food_option_font)
        price_label_2 = QLabel(self.food_right)
        price_label_2.setGeometry(170, -10, 40, 40)
        price_label_2.setText("價格")
        price_label_2.setFont(food_option_font)
        count_label_1 = QLabel(self.food_left)
        count_label_1.setGeometry(210, -10, 40, 40)
        count_label_1.setText("數量")
        count_label_1.setFont(food_option_font)
        count_label_2 = QLabel(self.food_right)
        count_label_2.setGeometry(210, -10, 40, 40)
        count_label_2.setText("數量")
        count_label_2.setFont(food_option_font)
        for t in food_types:
            food_option_dict = food_dict[t]
            self.food_count_dict[t] = {}
            type_label = QLabel()
            type_label.setFont(food_label_font)
            type_label.setFixedSize(160, 40)
            if t in ["一品料理", "揚げ物", "火之意志"]:
                self.food_layout2.addWidget(type_label)
                type_label.setText(t)
                food_option = food_option_dict.keys()
                for option in food_option:
                    food_widget = QWidget()
                    food_widget.setFixedSize(250, 40)
                    food_button = QRadioButton(food_widget)
                    food_button.setText(option)
                    food_button.setFont(food_option_font)
                    food_button.setGeometry(13, 0, 147, 40)
                    food_price = QLabel(food_widget)
                    price = food_option_dict[option]
                    food_price.setText(str(price))
                    food_price.setGeometry(160, 0 , 40, 40)
                    food_count = QTextEdit(food_widget)
                    food_count.setText(str(1))
                    food_count.setAlignment(Qt.AlignCenter)
                    food_count.setGeometry(205, 6, 25, 29)
                    self.food_layout1.addWidget(food_widget)
                    self.food_layout2.addWidget(food_widget)
                    self.food_count_dict[t][option] = [food_button, price, food_count]
            else:
                self.food_layout1.addWidget(type_label)
                type_label.setText(t)
                food_option = food_option_dict.keys()
                for option in food_option:
                    food_widget = QWidget()
                    food_widget.setFixedSize(250, 40)
                    food_button = QRadioButton(food_widget)
                    food_button.setText(option)
                    food_button.setFont(food_option_font)
                    food_button.setGeometry(13, 0, 147, 40)
                    food_price = QLabel(food_widget)
                    price = food_option_dict[option]
                    food_price.setText(str(price))
                    food_price.setGeometry(160, 0 , 40, 40)
                    food_count = QTextEdit(food_widget)
                    food_count.setText(str(1))
                    food_count.setAlignment(Qt.AlignCenter)
                    food_count.setGeometry(205, 6, 25, 29)
                    self.food_layout1.addWidget(food_widget)
                    self.food_count_dict[t][option] = [food_button, price, food_count]
            self.food_frant.addWidget(self.food_left)
            self.food_frant.addWidget(self.food_right)

    # Drink
    # Count how many drinks：drink_count_list：[[drink_name, drink_price, drink_count]]
        self.drink_count_list = []
        drink_font = QFont()
        drink_font.setPixelSize(18)
        self.drink_frant = QVBoxLayout(self.drink_tab)
        drink_block = QWidget()
        drink_block.setFixedSize(500, 65)
        self.drink_frant.addWidget(drink_block)
        drink_button = QPushButton(self.drink_tab)
        drink_button.setText("輸入")
        drink_button.setGeometry(450, 20, 100, 40)
        drink_add_button = QPushButton(self.drink_tab)
        drink_add_button.setIcon(self.add_icon)
        drink_add_button.setGeometry(488, 110, 30, 30)
        drink_col = QLabel("        品名\t\t\t\t         金額\t             數量")
        drink_col.setFixedSize(550, 20)
        self.drink_frant.addWidget(drink_col)
        drink_widget = QWidget()
        drink_widget.setFixedSize(450, 80)
        drink_name = QTextEdit(drink_widget)
        drink_name.setGeometry(20, 15, 220, 40)
        drink_name.setFont(drink_font)
        drink_name.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        drink_price = QTextEdit(drink_widget)
        drink_price.setGeometry(260, 15, 80, 40)
        drink_price.setFont(drink_font)
        drink_price.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        drink_count = QTextEdit(drink_widget)
        drink_count.setText(str(1))
        drink_count.setFont(drink_font)
        drink_count.setAlignment(Qt.AlignCenter)
        drink_count.setGeometry(360, 15, 40, 40)
        self.drink_frant.addWidget(drink_widget, 0)
        self.drink_frant.setSizeConstraint(QVBoxLayout.SetMinAndMaxSize)
        self.drink_count_list.append([drink_name, drink_price, drink_count])

    # Add tab
    # How much each pay：ppl_pay：{ppl：pay}
    # Option of each tab：ppl_layout：{ppl：[food_option, drink_option]}
        self.ppl_pay = {}
        self.ppl_layout = {}
        name_font = QFont()
        name_font.setPixelSize(20)
        ppl_font = QFont()
        ppl_font.setPixelSize(12)
        attend_list = self.tab_dict.keys()
        for ppl in attend_list:
            ppl_widget = self.tab_dict[ppl]
            name_text = QTextEdit(ppl_widget)
            name_text.setText(ppl)
            name_text.setGeometry(20, 10, 150, 40)
            name_text.setFont(name_font)
            pay_label = QLabel(ppl_widget)
            pay_label.setText("出的錢")
            pay_label.setGeometry(300, 20, 40, 20)
            pay_label.setFont(ppl_font)
            pay_box = QTextEdit(ppl_widget)
            pay_box.setGeometry(350, 10, 150, 40)
            pay_box.setFont(name_font)
            f_option_scroll = QScrollArea(ppl_widget)
            f_option_scroll.setGeometry(10, 60, 575, 490)
            f_option_scroll.setWidgetResizable(True)
            f_option_widget = QWidget()
            f_option_scroll.setWidget(f_option_widget)
            f_label = QLabel("食事")
            f_label.setFont(name_font)
            f_label.setFixedSize(400, 40)
            d_option_scroll = QScrollArea(ppl_widget)
            d_option_scroll.setGeometry(10, 550, 575, 180)
            d_option_scroll.setWidgetResizable(True)
            d_option_widget = QWidget()
            d_option_scroll.setWidget(d_option_widget)
            d_label = QLabel("酒水")
            d_label.setFont(name_font)
            d_label.setFixedSize(400, 40)
            f_option_layout = QVBoxLayout(f_option_widget)
            f_option_layout.addWidget(f_label)
            f_option_layout.setSizeConstraint(QVBoxLayout.SetMinAndMaxSize)
            d_option_layout = QVBoxLayout(d_option_widget)
            d_option_layout.addWidget(d_label)
            d_option_layout.setSizeConstraint(QVBoxLayout.SetMinAndMaxSize)
            self.ppl_pay[ppl] = pay_box
            self.ppl_layout[ppl] = [f_option_layout, d_option_layout]

    def add_food_option(self, food_dict, ppl_layout):
        self.add_class.food_add(food_dict, ppl_layout)


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = MainWindow()
    window.set_Ui()
    window.show()
    
    sys.exit(app.exec())