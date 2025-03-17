from PySide6.QtCore import QObject, QEvent
from PySide6.QtWidgets import QMainWindow, QPushButton, QLineEdit, QVBoxLayout, QWidget

class HighlightEffect(QObject):
    def __init__(self, main, widget):
        super().__init__(main)  # 呼叫父類的初始化
        self.main = main
        self.widget = widget
        self.default_style = self.widget.styleSheet()
        self.triggered_style = '''
            QWidget { background-color: gray; }
            QRadioButton::indicator {
                border: 1px solid gray;
                border-radius: 7px;
                background-color: white;
            }
            QRadioButton { color: white; }
            QLabel { color: white; }
            QLineEdit { background-color: white; }
        '''
        self.main.installEventFilter(self)  # 使用 eventFilter

    def changeStyle(self):
        # 改變樣式為觸發效果
        self.widget.setStyleSheet(self.triggered_style)

    def eventFilter(self, obj, event):
        # 監控各種事件
        if event.type() == QEvent.MouseButtonPress:
            # 點擊事件
            print("Mouse button pressed!")
            self.widget.setStyleSheet(self.triggered_style)  # 改變樣式
            return True  # 事件被處理，返回 True 來阻止進一步處理

        if event.type() == QEvent.KeyPress:
            # 鍵盤按鍵事件
            print("Key pressed!")
            # 這裡可以加入你需要的行為
            return True

        if event.type() == QEvent.FocusIn:
            # 焦點進入事件
            print("Focus entered!")
            return True
        return super().eventFilter(obj, event)

# 測試用例
if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QVBoxLayout, QWidget
    
    app = QApplication([])
    main_window = QMainWindow()
    
    # 設置主界面
    main_widget = QWidget()
    layout = QVBoxLayout(main_widget)
    button = QPushButton("Click me!")
    line_edit = QLineEdit("Type something...")
    
    layout.addWidget(button)
    layout.addWidget(line_edit)
    
    main_window.setCentralWidget(main_widget)
    main_window.show()
    
    # 初始化高亮效果
    highlight_effect = HighlightEffect(main_window, button)  # 可以將任意widget傳入這裡
    
    app.exec()
