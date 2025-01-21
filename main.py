from PySide6.QtWidgets import QApplication, QMainWindow, QScrollArea, QTabWidget, QWidget, QVBoxLayout, QLabel, QTextEdit, QHBoxLayout, QRadioButton
from food import Food

class MainWindow(QScrollArea):
    def __init__(self):
        super().__init__()

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
        food_count_dict = {}
        self.food_frant = QHBoxLayout(self.food_tab)
        self.food_left = QWidget()
        self.food_left.resize(300, 400)
        self.food_layout1 = QVBoxLayout()
        self.food_left.setLayout(self.food_layout1)
        self.food_right = QWidget()
        self.food_right.resize(300, 400)
        self.food_layout2 = QVBoxLayout()
        self.food_right.setLayout(self.food_layout2)
        menu_path = r"data\食事.xlsx"
        food = Food(menu_path)
        food_dict = food.read_excel()
        food_types = food_dict.keys()
        for t in food_types:
            food_option_dict = food_dict[t]
            food_count_dict[t] = {}
            type_label = QLabel()
            if t in ["一品料理", "揚げ物", "火之意志"]:
                self.food_layout2.addWidget(type_label)
                type_label.setText(t)
                food_option = food_option_dict.keys()
                for option in food_option:
                    food_widget = QWidget()
                    food_button = QRadioButton(food_widget)
                    food_button.setText(option)
                    food_price = QLabel(food_widget)
                    food_price.setText(str(food_option_dict[option]))
                    food_count = QTextEdit(food_widget)
                    food_count.setText(str(1))
                    self.food_layout2.addWidget(food_widget)
            else:
                self.food_layout1.addWidget(type_label)
                type_label.setText(t)
                food_option = food_option_dict.keys()
                for option in food_option:
                    food_widget = QWidget()
                    food_widget.resize(300, 40)
                    food_button = QRadioButton(food_widget)
                    food_button.setText(option)
                    #food_price = QLabel(food_widget)
                    #food_price.setText(str(food_option_dict[option]))
                    #food_count = QTextEdit(food_widget)
                    #food_count.setText(str(1))
                    self.food_layout1.addWidget(food_widget)
            self.food_frant.addWidget(self.food_left)
            self.food_frant.addWidget(self.food_right)
            

        # Add 
        '''tab_layout = QVBoxLayout(tab_widget)
        info = QWidget()
        info.resize(600, 300)
        name = QTextEdit(info)
        name.setGeometry(10, 10, 160, 40)
        name.setText(tab_text)
        tab_layout.addWidget(info)'''
        

if __name__ == "__main__":
    app = QApplication([])
    app.setStyle("Fusion")
    window = MainWindow()
    window.show()
    app.exec()