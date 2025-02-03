from PySide6.QtWidgets import QWidget, QRadioButton, QLabel
from PySide6.QtGui import QFont
from alert import Alert

# Count how many dishes：food_count_dict：{Type:{Meal:[button, price, count]}}
# Count how many drinks：drink_count_list：[[drink_name, drink_price, drink_count]]
# How much each pay：ppl_pay：{ppl：pay}
# Option of each tab：ppl_layout：{ppl：[food_option, drink_option]}

global count_dict
count_dict = {"f":{}, "d":{}}

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
            self.add_option("f", ppl_layout, f_option_dict)
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
                self.add_option("d", ppl_layout, d_option_list)
        except ValueError:
            self.alert.alert_text("值輸入錯誤")
            return

    
    def add_option(self, layout_type, ppl_layout, data):
        global count_dict
        ppl_list = ppl_layout.keys()
        t_font = QFont()
        t_font.setPixelSize(15)
        font = QFont()
        font.setPixelSize(14)
        if layout_type == "f":
            types = data.keys()
            for ppl in ppl_list:
                f_layout = ppl_layout[ppl][0]
                self.clear_layout(f_layout)
                for t in types:
                    meals = data[t].keys()
                    if len(meals) != 0:
                        type_label = QLabel()
                        type_label.setText(t)
                        type_label.setFont(t_font)
                        type_label.setFixedSize(300, 40)
                        f_layout.addWidget(type_label, 0)
                        for m in meals:
                            m_info = data[t][m]
                            m_widget = QWidget()
                            m_widget.setFixedSize(300, 40)
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
                            f_layout.addWidget(m_widget, 0)
                            if m not in count_dict["f"].keys():
                                count_dict["f"][m] = {"info":[m_info[0], m_info[1]], "ppl":{}}
                            count_dict["f"][m]["ppl"][ppl] = m_radio
        elif layout_type == "d":
            for ppl in ppl_list:
                d_layout = ppl_layout[ppl][1]
                self.clear_layout(d_layout)
                for d in data:
                    d_widget = QWidget()
                    d_widget.setFixedSize(300, 40)
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
                    d_layout.addWidget(d_widget, 0)
                    if d[0] not in count_dict["d"].keys():
                        count_dict["d"][d[0]] = {"info":[d[1], d[2]], "ppl":{}}
                    count_dict["d"][d[0]]["ppl"][ppl] = d_radio

    def count(self, ppl_pay, layout):
        global count_dict
        money_dict = {}
        ppl = ppl_pay.keys()
        try:
            for p in ppl:
                money_dict[p] = []
                how_much = ppl_pay[p].toPlainText()
                if how_much == "":
                    how_much = 0
                pay = int(how_much) * -1
                money_dict[p].append(pay)
            meals = count_dict["f"].keys()
            for m in meals:
                eat_count = 0
                f_price = int(count_dict["f"][m]["info"][0])
                f_c = int(count_dict["f"][m]["info"][1])
                for pp in ppl:
                    if count_dict["f"][m]["ppl"][pp].isChecked():
                        eat_count += 1
                m_per_ppl = (f_price * f_c) / eat_count
                m_per_ppl = int(m_per_ppl) + (m_per_ppl > int(m_per_ppl))
                for pp in ppl:
                    if count_dict["f"][m]["ppl"][pp].isChecked():
                        money_dict[pp].append(m_per_ppl)
            drinks = count_dict["d"].keys()
            for d in drinks:
                drink_count = 0
                d_price = int(count_dict["d"][d]["info"][0])
                d_c = int(count_dict["d"][d]["info"][1])
                for pp in ppl:
                    if count_dict["d"][d]["ppl"][pp].isChecked():
                        drink_count += 1
                m_per_ppl = (d_price * d_c) / drink_count
                m_per_ppl = int(m_per_ppl) + (m_per_ppl > int(m_per_ppl))
                for pp in ppl:
                    if count_dict["d"][d]["ppl"][pp].isChecked():
                        money_dict[pp].append(m_per_ppl)
            self.count_text(money_dict, layout)
        except ValueError:
            self.alert.alert_text("值輸入錯誤")
            return
        
    def count_text(self, dict, layout):
        ppl = dict.keys()
        self.clear_layout(layout)
        for p in ppl:
            money_list = dict[p]
            money = sum(money_list)
            money_text = QLabel(p)
            money_text.setFixedSize(400, 40)
            money_text.setText(f"{p}：{str(money)}")
            layout.addWidget(money_text)

    def clear_layout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()