from PySide6.QtWidgets import (
    QApplication, QMainWindow, QScrollArea, QTabWidget, QWidget, QVBoxLayout, QLabel
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 設定主視窗
        self.setWindowTitle("居")
        self.setGeometry(100, 100, 800, 600)

        # 創建 Tab Widget，作為主要的標籤頁容器
        self.tab_widget = QTabWidget(self)
        self.setCentralWidget(self.tab_widget)

        # 在標籤頁中添加內容
        for i in range(1, 9):
            scroll_area = QScrollArea()
            scroll_area.setWidgetResizable(True)

            # 每個標籤頁的內容
            content_widget = QWidget()
            content_layout = QVBoxLayout(content_widget)

            # 模擬每個標籤頁內的大量內容
            for j in range(1, 21):
                label = QLabel(f"Content in Tab {i}, Line {j}")
                label.setStyleSheet("font-size: 18px; padding: 5px;")
                content_layout.addWidget(label)

            scroll_area.setWidget(content_widget)
            self.tab_widget.addTab(scroll_area, f"Tab {i}")


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
