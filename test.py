from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QScrollArea, QVBoxLayout, QSizePolicy

app = QApplication([])

# 建立主視窗
window = QWidget()
window.setWindowTitle("QScrollArea Example")

# 創建外層 QVBoxLayout
main_layout = QVBoxLayout(window)

# 建立一個包含 QHBoxLayout 的 widget1
widget1 = QWidget()
hbox_layout = QHBoxLayout(widget1)

# 左側 widget，並添加 QVBoxLayout
left_vbox = QVBoxLayout()
left_vbox.addWidget(QLabel("Left - Item 1"))
left_vbox.addWidget(QLabel("Left - Item 2"))
left_widget = QWidget()
left_widget.setLayout(left_vbox)

# 右側 widget，並添加 QVBoxLayout
right_vbox = QVBoxLayout()
right_widget = QWidget()
right_widget.setLayout(right_vbox)

# 將左側和右側 widget 添加到 QHBoxLayout
hbox_layout.addWidget(left_widget)
hbox_layout.addWidget(right_widget)

# 建立 QScrollArea 並包裹 widget1 以支援滾動
scroll_area = QScrollArea()
scroll_area.setWidgetResizable(True)  # 讓內容能夠自適應調整
scroll_area.setWidget(widget1)

# 把 QScrollArea 加入主佈局
main_layout.addWidget(scroll_area)

# 模擬超過顯示範圍的 100 個 widget
for i in range(2):
    label = QLabel(f"Item {i+1}")
    right_vbox.addWidget(label)  # 這樣會在右側的 QVBoxLayout 中添加更多項目

# 顯示主視窗
window.show()
app.exec()
