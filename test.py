from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel

app = QApplication([])

# 主視窗
window = QWidget()
window.resize(100, 500)
window.setWindowTitle("固定大小的 Widget 排列於頂部")

# 主佈局
layout = QVBoxLayout(window)

# 新增 10 個固定大小的 QLabel
for i in range(2):
    label = QLabel(f"Label {i + 1}")
    label.setFixedHeight(30)  # 設定固定高度
    layout.addWidget(label)

# 設置 QVBoxLayout 的間距為 0
layout.setSpacing(0)  # 元件之間無間距
layout.addStretch(1)  # 在末尾加入伸縮，讓元件靠上排列

window.show()
app.exec()
