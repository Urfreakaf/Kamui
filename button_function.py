from PySide6.QtWidgets import QWidget, QRadioButton, QLabel
from PySide6.QtGui import QFont
from alert import Alert

# Count how many dishes：food_count_dict：{Type:{Meal:[button, price, count]}}
# Count how many drinks：drink_count_list：[[drink_name, drink_price, drink_count]]
# How much each pay：ppl_pay：{ppl：pay}
# Option of each tab：ppl_layout：{ppl：[food_option, drink_option]}

class Add:
    def __init__(self):
        self.alert = Alert()

    def food_add(self, food_dict, ppl_layout):
        f_option_dict = {}
        types = food_dict.keys()
        ppl_list = ppl_layout.keys()
        try:
            for t in types:
                f_option_dict[t] = {}
                meal_dict = food_dict[t]
                meals = meal_dict.keys()
                for meal in meals:
                    meal_info = meal_dict[meal]
                    if meal_info[0].isChecked():
                        f_option_dict[t][meal] = [meal_info[1], int(meal_info[2].toPlainText())]
            for ppl in ppl_list:
                f_layout = ppl_layout[ppl][0]
                self.add_option("f", f_layout, f_option_dict)
        except ValueError:
            self.alert.alert_text("值輸入錯誤")
            return
        return f_option_dict
    
    def add_option(self, layout_type, layout, dict):
        t_font = QFont()
        t_font.setPixelSize(15)
        font = QFont()
        font.setPixelSize(14)
        if layout_type == "f":
            types = dict.keys()
            for t in types:
                meals = dict[t].keys()
                if len(meals) != 0:
                    type_label = QLabel()
                    type_label.setText(t)
                    type_label.setFont(t_font)
                    layout.addWidget(type_label)
                    for m in meals:
                        m_info = dict[t][m]
                        m_widget = QWidget()
                        m_widget.setFixedSize(200, 40)
                        m_radio = QRadioButton(m_widget)
                        m_radio.setText(m)
                        m_radio.setGeometry(0, 0, 150, 40)
                        m_radio.setFont(font)
                        m_price = QLabel(m_widget)
                        m_price.setGeometry(170, 0, 40, 40)
                        m_price.setText(str(m_info[0]))
                        m_price.setFont(font)
                        m_count = QLabel(m_widget)
                        m_count.setGeometry(230, 0, 40, 40)
                        m_count.setText(str(m_info[1]))
                        m_count.setFont(font)
                        layout.addWidget(m_widget, 0)