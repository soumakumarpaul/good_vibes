from PySide6.QtWidgets import (QDialog, QWidget, QPushButton, 
                               QLabel, QVBoxLayout, QHBoxLayout, QSizePolicy,
                               QLineEdit)
from PySide6.QtCore import Qt, QRegularExpression, Signal
from PySide6.QtGui import QRegularExpressionValidator
from datetime import datetime, timedelta

class Loyalty(QDialog):
    loyalty_response = Signal(object)
    def __init__(self, particulars = {}):
        super().__init__()
        self.setModal(True)
        self.setFixedSize(400, 400)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.particulars = particulars
        self.init_widgets()

    def init_widgets(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        #initialize Header Section
        layout.addWidget(self.init_header())

        #initialize form
        layout.addWidget(self.init_loyalty_form())
        layout.addStretch(1)
        #actions layout
        layout.addWidget(self.init_actions())
        self.setLayout(layout)

    def init_header(self):
        #Header label
        header_label = QLabel("""<b>Loyalty Program</b>""", self)
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
    
    #initalize Loyalty form
    def init_loyalty_form(self):
        form_container = QWidget()
        form_layout = QVBoxLayout(form_container)
        form_layout.setContentsMargins(0, 0, 0, 0)
        form_layout.setSpacing(0)

        #Line Edit
        input_field_style = """
            QLineEdit, QLabel {
                padding: 4px;
                font-size: 20px;
                background-color: #FFFFFF;
                color: #2c2c2c;
                border: 2px solid #7851a9;
                margin: 4px;
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

        #amount
        amount_layout = QHBoxLayout()
        amount_layout.setSpacing(5)

        price_validator = QRegularExpressionValidator(QRegularExpression(r"^[1-9]\d{3,4}(\.\d{1,2})?$"))

        amt_layout = QVBoxLayout()
        amt_lbl = QLabel("Amount:")
        amt_lbl.setStyleSheet(input_field_label)
        amt = self.particulars.get("price", "1000.00")
        self.txt_amt = QLineEdit(amt)
        self.txt_amt.setStyleSheet(input_field_style)
        self.txt_amt.setValidator(price_validator)
        self.txt_amt.textChanged.connect(self.compute_loyalty)
        amt_layout.addWidget(amt_lbl)
        amt_layout.addWidget(self.txt_amt)

        discount_validator = QRegularExpressionValidator(QRegularExpression(r"^[1-4]\d{0,1}?$"))
        discount_layout = QVBoxLayout()
        discount_lbl = QLabel("Loyalty Percent")
        discount_lbl.setStyleSheet(input_field_label)
        discount = self.particulars.get("discount", "10")
        self.txt_percent = QLineEdit("10")
        self.txt_percent.setStyleSheet(input_field_style)
        self.txt_percent.setValidator(discount_validator)
        self.txt_percent.textChanged.connect(self.compute_loyalty)
        discount_layout.addWidget(discount_lbl)
        discount_layout.addWidget(self.txt_percent)

        amount_layout.addLayout(amt_layout)
        amount_layout.addLayout(discount_layout)

        #credits
        credits_layout = QVBoxLayout()

        credits_lbl = QLabel("Loyalty Credits")
        credits_lbl.setStyleSheet(input_field_label)

        self.txt_credits_lbl = QLabel("1100")
        self.txt_credits_lbl.setStyleSheet(input_field_style)

        credits_layout.addWidget(credits_lbl)
        credits_layout.addWidget(self.txt_credits_lbl)

        #Validity
        validity_layout = QHBoxLayout()
        
        days_validator = QRegularExpressionValidator(QRegularExpression(r"^[1-9]\d{2,3}?$"))
        days_layout = QVBoxLayout()
        days_lbl = QLabel("Validity(Days):")
        days_lbl.setStyleSheet(input_field_label)
        duration = 30
        self.txt_days = QLineEdit(str(duration))
        self.txt_days.setStyleSheet(input_field_style)
        self.txt_days.setValidator(days_validator)
        self.txt_days.textChanged.connect(self.compute_expiry)
        days_layout.addWidget(days_lbl)
        days_layout.addWidget(self.txt_days)

        date_layout = QVBoxLayout()
        date_lbl = QLabel("Valid Through")
        date_lbl.setStyleSheet(input_field_label)
        expiry = datetime.today() + timedelta(days=30)
        self.txt_date = QLabel(expiry.strftime('%d %b %Y'))
        self.txt_date.setStyleSheet(input_field_style)
        date_layout.addWidget(date_lbl)
        date_layout.addWidget(self.txt_date)

        validity_layout.addLayout(days_layout)
        validity_layout.addLayout(date_layout)

        form_layout.addLayout(amount_layout)
        form_layout.addLayout(credits_layout)
        form_layout.addLayout(validity_layout)

        return form_container
    
    def init_actions(self):
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
        self.save_button = QPushButton("Save [Ctrl+S]")
        self.save_button.setStyleSheet(buttons_style)
        self.cancel_button = QPushButton("Cancel [ESC]")
        self.cancel_button.setStyleSheet(buttons_style)

        self.cancel_button.clicked.connect(self.exit)
        self.save_button.clicked.connect(self.save_loyalty)

        # layout
        buttons_layout = QHBoxLayout(actions_container)
        buttons_layout.setContentsMargins(0,0,0,0)
        buttons_layout.setSpacing(0)
        buttons_layout.addWidget(self.save_button)
        buttons_layout.addWidget(self.cancel_button)
        return actions_container
    
    def compute_loyalty(self, txt: str):
        amount = float(self.txt_amt.text())
        discount = float(self.txt_percent.text())
        credits = amount * (100 + discount)/100
        self.txt_credits_lbl.setText(f"{credits:.2f}")

    def compute_expiry(self, txt: str):
        days = int(txt) - 1
        expiry = datetime.today() + timedelta(days = days)
        self.txt_date.setText(expiry.strftime('%d %b %Y'))

    def exit(self):
        self.loyalty_response.emit(None)
        self.close()

    def save_loyalty(self):
        response = {
                "service": f"Credits: {self.txt_credits_lbl.text()} Valid: {self.txt_days.text()} Days",
                "rate": self.txt_credits_lbl.text(),
                "discount": self.txt_percent.text(),
                "quantity": "1",
                "price": self.txt_amt.text(),
                "server": "",
                "helper": "",
                "category": self.particulars.get('category', 'Elite Member'),
                "type": "loyalty"
        }
        self.loyalty_response.emit(response)
        self.close()