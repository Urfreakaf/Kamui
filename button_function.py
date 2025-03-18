from PySide6.QtWidgets import QWidget, QRadioButton, QLabel, QScrollArea, QVBoxLayout, QFrame
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
        try:
            for t in types:
                f_option_dict[t] = {}
                meal_dict = food_dict[t]
                meals = meal_dict.keys()
                for meal in meals:
                    meal_info = meal_dict[meal]
                    if meal_info[0].isChecked():
                        f_option_dict[t][meal] = [meal_info[1], int(meal_info[2].text())]
            if add_list:
                for row_list in add_list:
                    if row_list[0].isChecked():
                        all_filled = all(edit.text().strip() != "" for edit in row_list[1])
                        if all_filled:
                            name = row_list[1][0].text()
                            price = row_list[1][1].text()
                            count = row_list[1][2].text()
                            if "手動輸入" not in f_option_dict.keys():
                                f_option_dict["手動輸入"] = {}
                            f_option_dict["手動輸入"][name] = [price, int(count)]
            self.add_option("f", ppl_layout, f_option_dict)
        except ValueError:
            self.alert.alert_text("值輸入錯誤")
            return
    
    def drink_add(self, drink_list, ppl_layout):
        d_option_list = []
        try:
            if drink_list:
                for row_list in drink_list:
                    all_filled = all(edit.text().strip() != "" for edit in row_list)
                    if all_filled:
                        name = row_list[0].text()
                        price = row_list[1].text()
                        count = row_list[2].text()
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
            count_dict["f"] = {}
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
                        type_label.setFixedSize(235, 40)
                        f_layout.addWidget(type_label, 0)
                        for m in meals:
                            m_info = data[t][m]
                            m_widget = QWidget()
                            m_widget.setFixedSize(235, 40)
                            m_radio = QRadioButton(m_widget)
                            m_radio.setChecked(False)
                            m_radio.setText(m)
                            m_radio.setGeometry(0, 0, 140, 40)
                            m_radio.setFont(font)
                            m_price = QLabel(m_widget)
                            m_price.setGeometry(155, 0, 40, 40)
                            m_price.setText(str(m_info[0]))
                            m_price.setFont(font)
                            m_count = QLabel(m_widget)
                            m_count.setGeometry(215, 0, 20, 40)
                            m_count.setText(str(m_info[1]))
                            m_count.setFont(font)
                            f_layout.addWidget(m_widget, 0)
                            if m not in count_dict["f"].keys():
                                count_dict["f"][m] = {"info":[m_info[0], m_info[1]], "ppl":{}}
                            count_dict["f"][m]["ppl"][ppl] = m_radio
        elif layout_type == "d":
            count_dict["d"] = {}
            for ppl in ppl_list:
                d_layout = ppl_layout[ppl][1]
                self.clear_layout(d_layout)
                for d in data:
                    d_widget = QWidget()
                    d_widget.setFixedSize(235, 40)
                    d_radio = QRadioButton(d_widget)
                    d_radio.setText(d[0])
                    d_radio.setGeometry(0, 0, 140, 40)
                    d_radio.setFont(font)
                    d_price = QLabel(d_widget)
                    d_price.setGeometry(155, 0, 40, 40)
                    d_price.setText(str(d[1]))
                    d_price.setFont(font)
                    d_count = QLabel(d_widget)
                    d_count.setGeometry(215, 0, 20, 40)
                    d_count.setText(str(d[2]))
                    d_count.setFont(font)
                    d_layout.addWidget(d_widget, 0)
                    if d[0] not in count_dict["d"].keys():
                        count_dict["d"][d[0]] = {"info":[d[1], d[2]], "ppl":{}}
                    count_dict["d"][d[0]]["ppl"][ppl] = d_radio

    def count(self, ppl_pay, discount, layout):
        global count_dict
        if not count_dict or count_dict == {"f":{}, "d":{}}:
            return
        money_dict = {}
        money_text = {}
        ppl = list(ppl_pay.keys()).copy()
        try:
            for p in ppl:
                money_dict[p] = []
                money_text[p] = {"f":["\t食事："], "d":["\t酒水："]}
                how_much = ppl_pay[p].text()
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
                if eat_count == 0:
                    self.alert.alert_text(f"{m}未被選取")
                    return
                m_per_ppl = (f_price * f_c) / eat_count
                for pp in ppl:
                    if count_dict["f"][m]["ppl"][pp].isChecked():
                        money_dict[pp].append(m_per_ppl)
                        money_text[pp]["f"].append(f"\t\t{m}： {f_price * f_c} / {eat_count} = {round(m_per_ppl, 4)}")
            drinks = count_dict["d"].keys()
            for d in drinks:
                drink_count = 0
                d_price = int(count_dict["d"][d]["info"][0])
                d_c = int(count_dict["d"][d]["info"][1])
                for pp in ppl:
                    if count_dict["d"][d]["ppl"][pp].isChecked():
                        drink_count += 1
                if drink_count == 0:
                    self.alert.alert_text(f"{d}未被選取")
                    return
                elif drink_count > d_c:
                    self.alert.alert_text(f"{d}選取超過杯數")
                    return
                d_per_ppl = (d_price * d_c) / drink_count
                for pp in ppl:
                    if count_dict["d"][d]["ppl"][pp].isChecked():
                        money_dict[pp].append(d_per_ppl)
                        money_text[pp]["d"].append(f"\t\t{d_price * d_c} / {drink_count} = {round(d_per_ppl, 4)}")
            for p in ppl:
                if len(money_dict[p]) <= 1:
                    del money_dict[p]
                    del money_text[p]
            self.count_text(money_dict, money_text, discount, layout)
        except ValueError:
            self.alert.alert_text("值輸入錯誤")
            return
        
    def count_text(self, money_dict, money_text, discount, layout):
        self.clear_layout(layout)
        ppl_count = len(money_dict)
        if discount != "0":
            dis_per_ppl = (float(discount) / ppl_count) * (-1)
        for p in money_dict.keys():
            money_list = money_dict[p]
            money = sum(money_list)
            money_item_scroll = QScrollArea()
            money_item_scroll.setFixedSize(410, 130)
            money_item_scroll.setWidgetResizable(True)
            #money_item_scroll.setFrameShape(QFrame.NoFrame)
            money_item_area = QWidget()
            money_item_scroll.setWidget(money_item_area)
            money_item_layout = QVBoxLayout()
            money_item_area.setLayout(money_item_layout)
            money_item_layout.setSizeConstraint(QVBoxLayout.SetMinAndMaxSize)
            money_total_text = QLabel()
            money_total_text.setFixedSize(370, 17)
            if "dis_per_ppl" in locals():
                money += dis_per_ppl
                money = int(money) + (money > int(money))
                money_total_text.setText(f"{p}：{str(money)}")
                layout.addWidget(money_total_text)
                discount_title =QLabel("\t折扣")
                discount_title.setFixedSize(370, 17)
                discount_text =QLabel(f"\t\t{float(discount) * (-1)} / {ppl_count} = {round(dis_per_ppl, 4)}")
                discount_text.setFixedSize(370, 17)
                money_item_layout.addWidget(discount_title)
                money_item_layout.addWidget(discount_text)
            else:
                money = int(money) + (money > int(money))
                money_total_text.setText(f"{p}：{str(money)}")
                layout.addWidget(money_total_text)
            
            f_text_list = money_text[p]["f"]
            if len(f_text_list) > 1:
                for m_row in f_text_list:
                    f_money_item =QLabel(m_row)
                    f_money_item.setFixedSize(370, 17)
                    money_item_layout.addWidget(f_money_item)
            d_text_list = money_text[p]["d"]
            if len(d_text_list) > 1:
                for d_row in d_text_list:
                    d_money_item =QLabel(d_row)
                    d_money_item.setFixedSize(370, 17)
                    money_item_layout.addWidget(d_money_item)
            layout.addWidget(money_item_scroll)

    def clear_layout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()