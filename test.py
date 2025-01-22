from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QRadioButton, QPushButton

app = QApplication([])

# 創建主窗口
window = QWidget()
layout = QVBoxLayout(window)

# 創建多個 QRadioButton
radio_buttons = []
for i in range(5):
    rb = QRadioButton(f"Option {i + 1}")
    layout.addWidget(rb)
    radio_buttons.append(rb)

# 創建 QPushButton
button = QPushButton("Check Selection")
layout.addWidget(button)

# 定義按鈕點擊時的功能
def on_button_clicked():
    for rb in radio_buttons:
        if rb.isChecked():
            print(rb.text())
            break  # 找到後可以中斷迴圈

button.clicked.connect(on_button_clicked)

window.show()
app.exec()
