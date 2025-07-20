from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout,
                               QPushButton, QComboBox, QLineEdit,
                               QLabel, QSizePolicy, QWidget)
from PySide6.QtCore import Qt, Signal
from tinydb import TinyDB
from datetime import date


class Expense(QDialog):
    expense_response = Signal(bool)
    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path
        self.setModal(True)
        self.setFixedSize(500, 400)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.init_widgets()

    def init_widgets(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Initialize Header Section
        layout.addWidget(self._init_header())

        # Intialize Expense Form
        layout.addWidget(self._init_form())

        layout.addStretch(1)
        # Initialize Actions
        layout.addWidget(self._init_actions())

        self.setLayout(layout)

    def _init_header(self):
        #Header label
        header_label = QLabel("""<b>Record Expenses</b>""", self)
        header_label.setTextFormat(Qt.RichText)
        header_label.setStyleSheet("""
            QLabel {
                background-color: #7851a9;
                color: #ffffff;
                font-size: 14px;
                padding: 20px;
                text-align: center;
                border: 1px solid #FFFFFF;
                }
            """)
        header_label.setAlignment(Qt.AlignCenter)
        header_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        return header_label 

    def _init_form(self):
        form_container = QWidget()
        form_layout = QVBoxLayout(form_container)
        form_layout.setContentsMargins(10, 10, 10, 10)
        form_layout.setSpacing(0)

        #Line Edit
        input_field_style = """
            QLineEdit, QComboBox {
                padding: 4px;
                font-size: 20px;
                background-color: #FFFFFF;
                color: #2c2c2c;
                border: 2px solid #7851a9;
                margin: 4px;
            }
            QComboBox QAbstractItemView {
                background-color: #C0C0C0;
                color: #FFFFFF;
                selection-background-color: #7851a9; 
            }
        """

        input_field_label = """
            QLabel {
                font-size: 14px;
                color: #C0C0C0;
                border: 0px solid;
                margin: 4px;
            }
        """

        #Amount
        amount_layout = QVBoxLayout()
        amount_label = QLabel("Amount:")
        amount_label.setStyleSheet(input_field_label)
        self.txt_amount = QLineEdit("0.00")
        self.txt_amount.setPlaceholderText("Amount")
        self.txt_amount.setStyleSheet(input_field_style)
        amount_layout.addWidget(amount_label)
        amount_layout.addWidget(self.txt_amount)

        #Method
        method_layout = QVBoxLayout()
        method_label = QLabel("Payment Method:")
        method_label.setStyleSheet(input_field_label)
        self.txt_method = QComboBox()
        self.txt_method.addItems(["Cash", "UPI", "Card"])
        self.txt_method.setStyleSheet(input_field_style)
        method_layout.addWidget(method_label)
        method_layout.addWidget(self.txt_method)

        #Account Type
        type_layout = QVBoxLayout()
        type_label = QLabel("Paid From:")
        type_label.setStyleSheet(input_field_label)
        self.txt_type = QComboBox()
        self.txt_type.addItems(["Business", "Personal"])
        self.txt_type.setStyleSheet(input_field_style)
        type_layout.addWidget(type_label)
        type_layout.addWidget(self.txt_type)

        #Paid By
        payer_layout = QVBoxLayout()
        payer_lbl = QLabel("Paid By:")
        payer_lbl.setStyleSheet(input_field_label)
        self.txt_payer = QComboBox()
        self.txt_payer.addItems(["Priya", "Subarna", "Others"])
        self.txt_payer.setStyleSheet(input_field_style)
        payer_layout.addWidget(payer_lbl)
        payer_layout.addWidget(self.txt_payer)

        #Purpose
        purpose_layout = QVBoxLayout()
        purpose_label = QLabel("Payment Purpose:")
        purpose_label.setStyleSheet(input_field_label)
        self.txt_purpose = QLineEdit()
        self.txt_purpose.setPlaceholderText("Purpose of the Expense")
        self.txt_purpose.setStyleSheet(input_field_style)
        purpose_layout.addWidget(purpose_label)
        purpose_layout.addWidget(self.txt_purpose)

        amount_group = QHBoxLayout()
        amount_group.addLayout(amount_layout)
        amount_group.addLayout(method_layout)

        payer_group = QHBoxLayout()
        payer_group.addLayout(payer_layout)
        payer_group.addLayout(type_layout)

        form_layout.addLayout(amount_group)
        form_layout.addLayout(payer_group)
        form_layout.addLayout(purpose_layout)

        return form_container

    def _init_actions(self):
        actions_container = QWidget()
        actions_container.setStyleSheet("background-color: #7851a9;")

        #Buttons
        buttons_style = """
            QPushButton {
                font-size: 20px;
                font-weight: bold;
                color: "#7851a9";
                padding: 10px;
                margin: 15px;
                background-color: #e5c8dc;
            }
            QPushButton:hover {
                background-color: #7851a9;
                color: #FFFFFF;
            }
        """

        # buttons
        self.save_button = QPushButton("Save [Enter]")
        self.save_button.setStyleSheet(buttons_style)
        self.cancel_button = QPushButton("Cancel [ESC]")
        self.cancel_button.setStyleSheet(buttons_style)

        self.cancel_button.clicked.connect(self.exit)
        self.save_button.clicked.connect(self.save_expense)

        # layout
        buttons_layout = QHBoxLayout(actions_container)
        buttons_layout.setContentsMargins(0,0,0,0)
        buttons_layout.setSpacing(0)
        buttons_layout.addWidget(self.save_button)
        buttons_layout.addWidget(self.cancel_button)
        return actions_container

    def save_expense(self):
        response = {
            "amount": self.txt_amount.text().strip(),
            "purpose": self.txt_purpose.text().strip(),
            "method": self.txt_method.currentText(),
            "from": self.txt_type.currentText(),
            "payer": self.txt_payer.currentText(),
            "date": date.today().isoformat(),
            "type": "debit"
        }
        db = TinyDB(self.file_path + "/accounts_db.json")
        db.insert(response)
        db.close()
        self.exit(didRecordExpense=True)
        
    def exit(self, didRecordExpense = False):
        self.expense_response.emit(didRecordExpense)
        self.close()