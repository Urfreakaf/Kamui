from PySide6.QtWidgets import QApplication, QMainWindow, QScrollArea, QTabWidget, QWidget, QVBoxLayout, QLabel, QTextEdit, QHBoxLayout, QRadioButton
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from food import Food

class MainWindow(QScrollArea):
    def __init__(self):
        super().__init__()

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
    # Count how many dishes：food_count_dict
        self.food_count_dict = {}
        food_label_font = QFont()
        food_label_font.setPixelSize(18)
        food_option_font = QFont()
        food_option_font.setPixelSize(14)
        self.food_frant = QHBoxLayout(self.food_tab)
        self.food_left = QWidget()
        self.food_layout1 = QVBoxLayout()
        self.food_left.setLayout(self.food_layout1)
        self.food_right = QWidget()
        self.food_layout2 = QVBoxLayout()
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
    # Count how many dishes：drink_count_dict
        self.drink_count_list = []
        drink_font = QFont()
        drink_font.setPixelSize(18)
        self.drink_frant = QVBoxLayout(self.drink_tab)
        block = QLabel("        品名\t\t\t\t         金額\t             數量")
        block.setFixedSize(550, 20)
        self.drink_frant.addWidget(block)
        drink_widget = QWidget()
        drink_widget.setFixedSize(550, 80)
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
        self.drink_frant.setSpacing(0) 
        self.drink_frant.addStretch(1)
        self.drink_count_list.append([drink_name, drink_price, drink_count])

    # Add tab
        self.ppl_dict = {}
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
            option_widget = QWidget(ppl_widget)
            option_widget.setGeometry(10, 60, 575, 690)
            option_layout = QVBoxLayout(option_widget)
            self.ppl_dict[ppl] = [pay_box, option_layout]
        

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = MainWindow()
    window.set_Ui()
    window.show()
    
    sys.exit(app.exec())