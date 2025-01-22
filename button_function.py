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

    def food_add(self, food_dict, add_list, ppl_layout):
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
            if add_list:
                for row_list in add_list:
                    if row_list[0].isChecked():
                        all_filled = all(edit.toPlainText().strip() != "" for edit in row_list[1])
                        if all_filled:
                            name = row_list[1][0].toPlainText()
                            price = row_list[1][1].toPlainText()
                            count = row_list[1][2].toPlainText()
                            if "手動輸入" not in f_option_dict.keys():
                                f_option_dict["手動輸入"] = {}
                            f_option_dict["手動輸入"][name] = [price, int(count)]
            for ppl in ppl_list:
                f_layout = ppl_layout[ppl][0]
                self.add_option("f", f_layout, f_option_dict)
        except ValueError:
            self.alert.alert_text("值輸入錯誤")
            return
    
    def drink_add(self, drink_list, ppl_layout):
        d_option_list = []
        ppl_list = ppl_layout.keys()
        try:
            if drink_list:
                for row_list in drink_list:
                    all_filled = all(edit.toPlainText().strip() != "" for edit in row_list)
                    if all_filled:
                        name = row_list[0].toPlainText()
                        price = row_list[1].toPlainText()
                        count = row_list[2].toPlainText()
                        d_option_list.append([name, int(price), int(count)])
            if d_option_list:
                for ppl in ppl_list:
                    d_layout = ppl_layout[ppl][1]
                    self.add_option("d", d_layout, d_option_list)
        except ValueError:
            self.alert.alert_text("值輸入錯誤")
            return

    
    def add_option(self, layout_type, layout, data):
        t_font = QFont()
        t_font.setPixelSize(15)
        font = QFont()
        font.setPixelSize(14)
        if layout_type == "f":
            types = data.keys()
            for t in types:
                meals = data[t].keys()
                if len(meals) != 0:
                    type_label = QLabel()
                    type_label.setText(t)
                    type_label.setFont(t_font)
                    layout.addWidget(type_label)
                    for m in meals:
                        m_info = data[t][m]
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
        elif layout_type == "d":
            for d in data:
                d_widget = QWidget()
                d_widget.setFixedSize(200, 40)
                d_radio = QRadioButton(d_widget)
                d_radio.setText(d[0])
                d_radio.setGeometry(0, 0, 150, 40)
                d_radio.setFont(font)
                d_price = QLabel(d_widget)
                d_price.setGeometry(170, 0, 40, 40)
                d_price.setText(str(d[1]))
                d_price.setFont(font)
                d_count = QLabel(d_widget)
                d_count.setGeometry(230, 0, 40, 40)
                d_count.setText(str(d[2]))
                d_count.setFont(font)
                layout.addWidget(d_widget, 0)