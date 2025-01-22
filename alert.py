from PySide6.QtWidgets import QMessageBox

class Alert:
    def __init__(self):
        pass
    def alert_text(self,text):
        confirm_box = QMessageBox()
        confirm_box.setIcon(QMessageBox.Warning)
        confirm_box.setWindowTitle("錯誤")
        confirm_box.setText(text)
        confirm_box.setStandardButtons(QMessageBox.Yes)
        confirm_box.setDefaultButton(QMessageBox.Yes)
        yes_button = confirm_box.button(QMessageBox.Yes)
        yes_button.setText("確定")
        reply = confirm_box.exec()
        if reply == QMessageBox.Yes:
            confirm_box.close()