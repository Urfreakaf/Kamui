from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout
from PySide6.QtCore import QTimer

app = QApplication([])

# 建立主視窗
main_widget = QWidget()
layout = QVBoxLayout(main_widget)

# 建立目標 widget
target_widget = QPushButton("目標 Widget")
target_widget.setObjectName("target")  # 設定 ObjectName，讓樣式只影響此 widget
layout.addWidget(target_widget)

def highlight_widget(widget):
    """讓 widget 以虛線邊框閃爍 2 秒 (不影響子部件)"""
    original_style = widget.styleSheet()  # 儲存原始樣式
    highlight_style = "#target { border: 2px dashed red; }"  # 只影響 objectName 為 target 的部件

    def toggle_border():
        """切換邊框樣式"""
        if widget.styleSheet() == highlight_style:
            widget.setStyleSheet(original_style)
        else:
            widget.setStyleSheet(highlight_style)

    timer = QTimer()
    timer.timeout.connect(toggle_border)
    timer.start(300)  # 每 300ms 切換一次

    # 2 秒後停止閃爍並恢復原狀
    QTimer.singleShot(2000, lambda: (timer.stop(), widget.setStyleSheet(original_style)))

# 測試按鈕，按下後讓 target_widget 閃爍
test_button = QPushButton("閃爍目標 Widget")
test_button.clicked.connect(lambda: highlight_widget(target_widget))
layout.addWidget(test_button)

main_widget.show()
app.exec()
