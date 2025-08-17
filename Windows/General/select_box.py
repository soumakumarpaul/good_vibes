from PySide6.QtWidgets import QComboBox

class SelectBox(QComboBox):

    def focusInEvent(self, e):
        self.showPopup()
        return super().focusInEvent(e)
