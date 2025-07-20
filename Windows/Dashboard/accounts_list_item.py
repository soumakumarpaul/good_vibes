from PySide6.QtWidgets import QVBoxLayout, QWidget, QLabel, QHBoxLayout, QPushButton
from PySide6.QtCore import Qt

class AccountsItemWidget(QWidget):

    def __init__(self, expense_details):
        super().__init__()
        self.expense = expense_details
        self.setMouseTracking(True)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5,5,5,5)
        layout.setSpacing(0)
        layout.addWidget(self.init_header())
        layout.addLayout(self.init_sub_row())

    def init_header(self):
        header_container = QWidget()
        header_container.setContentsMargins(0, 0, 0, 0)
        layout = QHBoxLayout(header_container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        debit_lbl_style = """
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #FF0800;
            }
        """

        credit_lbl_style = """
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #2E6f40;
            }
        """
        expense_txt = QLabel(self.expense.get("purpose", ""))
        amount_txt = QLabel("{:.2f}".format(float(self.expense.get("amount", 0.00))))
        if self.expense['type'] == 'debit':
            expense_txt.setStyleSheet(debit_lbl_style)
            amount_txt.setStyleSheet(debit_lbl_style)
        else:
            expense_txt.setStyleSheet(credit_lbl_style)
            amount_txt.setStyleSheet(credit_lbl_style)
        layout.addWidget(expense_txt, 1)
        layout.addWidget(amount_txt)

        return header_container
    
    def init_sub_row(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        debit_lbl_style = """
            QLabel {
                font-size: 12px;
                font-weight: bold;
                color: #2c2c2c;
            }
        """
        date_txt = QLabel(self.expense.get("date"))
        date_txt.setStyleSheet(debit_lbl_style)
        type_txt = QLabel(self.expense.get("method"))
        type_txt.setStyleSheet(debit_lbl_style)
        layout.addWidget(date_txt, 1)
        layout.addWidget(type_txt)
        return layout
