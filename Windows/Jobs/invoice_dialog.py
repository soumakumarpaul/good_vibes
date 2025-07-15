from PySide6.QtWidgets import QDialog, QWidget, QLabel, QLineEdit, QSizePolicy, QVBoxLayout, QHBoxLayout, QPushButton
from Utilities.environments import Environment
from PySide6.QtCore import Qt, QRegularExpression, Signal
from PySide6.QtGui import QRegularExpressionValidator, QShortcut, QKeySequence

class Invoice(QDialog):

    invoice_response = Signal(object)

    def __init__(self, folder_path, job_details):
        super().__init__()
        self.setModal(True)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setFixedSize(400, 400)
        self.env = Environment()
        self.folder_path = folder_path
        self.job_details = job_details
        self.init_shortcuts()
        self.init_widgets()

    def init_shortcuts(self):
        exit_shortcut = QShortcut(QKeySequence("Ctrl+X"), self)
        exit_shortcut.setContext(Qt.WindowShortcut)
        exit_shortcut.activated.connect(self.exit)

        save_shortcut = QShortcut(QKeySequence("Ctrl+S"), self)
        save_shortcut.setContext(Qt.WindowShortcut)
        save_shortcut.activated.connect(self.save_invoice)

        invoice_shortcut = QShortcut(QKeySequence("Ctrl+P"), self)
        invoice_shortcut.setContext(Qt.WindowShortcut)
        invoice_shortcut.activated.connect(self.print_invoice)

    def init_widgets(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        main_layout.addWidget(self.init_header())

        main_layout.addWidget(self.init_payment())

        #form fields
        main_layout.addWidget(self.init_payment_form())

        #actions widgets
        main_layout.addStretch()
        main_layout.addWidget(self.init_actions())
        self.setLayout(main_layout)

    def init_header(self):
        header_label = QLabel("""<b>Payment</b>""", self)
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
    
    def init_payment(self):
        payment_container = QWidget()
        payment_layout = QHBoxLayout(payment_container)
        payment_layout.setContentsMargins(0, 0, 0, 0)
        payment_layout.setSpacing(0)

        payment_style = """
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #7851a9;
                padding: 5px;
            }
        """

        payment_lbl = QLabel("To Pay:")
        payment_lbl.setStyleSheet(payment_style)
        payment_layout.addWidget(payment_lbl)
        amt = f"{self.job_details.get('net_amount', "0.00"):.2f}"
        self.amount_lbl = QLabel(amt)
        self.amount_lbl.setStyleSheet(payment_style)
        self.amount_lbl.setAlignment(Qt.AlignRight)
        payment_layout.addWidget(self.amount_lbl)

        return payment_container

    def init_payment_form(self):
        form_container = QWidget()
        form_container.setStyleSheet('border: 2px solid #c0c0c0;')
        form_layout = QVBoxLayout(form_container)

        #Line Edit
        input_field_style = """
            QLineEdit, QComboBox {
                padding: 4px;
                font-size: 20px;
                background-color: #FFFFFF;
                color: #2c2c2c;
                border: 2px solid #7851a9;
            }
            QComboBox QAbstractItemView {
                background-color: #C0C0C0;
                color: #FFFFFF;
                selection-background-color: #7851a9; 
            }
        """

        input_field_label = """
            QLabel {
                font-size: 10px;
                color: #C0C0C0;
                border: 0px solid;
            }
        """
        price_validator = QRegularExpressionValidator(QRegularExpression(r"^[1-9]\d{1,4}(\.\d{1,2})?$"))
        #membership credit
        members_layout = QVBoxLayout()
        members_layout.setContentsMargins(0,0,0,0)
        members_layout.setSpacing(0)
        members_label = QLabel("Loyalty Credit")
        members_label.setStyleSheet(input_field_label)
        self.txt_members = QLineEdit("0.00")
        self.txt_members.setPlaceholderText("0.00")
        self.txt_members.setStyleSheet(input_field_style)
        self.txt_members.setValidator(price_validator)

        self.txt_members.textChanged.connect(self.compute_payment)
        self.txt_members.setReadOnly(True)
        members_layout.addWidget(members_label)
        members_layout.addWidget(self.txt_members)

        # Cash
        cash_layout = QVBoxLayout()
        cash_layout.setContentsMargins(0,0,0,0)
        cash_layout.setSpacing(0)
        cash_label = QLabel("Cash")
        cash_label.setStyleSheet(input_field_label)
        self.txt_cash = QLineEdit("0.00")
        self.txt_cash.setPlaceholderText("0.00")
        self.txt_cash.setStyleSheet(input_field_style)
        self.txt_cash.setValidator(price_validator)
        self.txt_cash.textEdited.connect(self.compute_payment)
        cash_layout.addWidget(cash_label)
        cash_layout.addWidget(self.txt_cash)

        # UPI
        upi_layout = QVBoxLayout()
        upi_layout.setContentsMargins(0,0,0,0)
        upi_layout.setSpacing(0)
        upi_label = QLabel("UPI")
        upi_label.setStyleSheet(input_field_label)
        self.txt_upi = QLineEdit("0.00")
        self.txt_upi.setPlaceholderText("0.00")
        self.txt_upi.setStyleSheet(input_field_style)
        self.txt_upi.setValidator(price_validator)
        self.txt_upi.textEdited.connect(self.compute_payment)
        upi_layout.addWidget(upi_label)
        upi_layout.addWidget(self.txt_upi)

        # Card
        card_layout = QVBoxLayout()
        card_layout.setContentsMargins(0,0,0,0)
        card_layout.setSpacing(0)
        card_label = QLabel("Card")
        card_label.setStyleSheet(input_field_label)
        self.txt_card = QLineEdit("0.00")
        self.txt_card.setPlaceholderText("0.00")
        self.txt_card.setStyleSheet(input_field_style)
        self.txt_card.setValidator(price_validator)
        self.txt_card.textEdited.connect(self.compute_payment)
        card_layout.addWidget(card_label)
        card_layout.addWidget(self.txt_card)

        form_layout.addLayout(members_layout)
        form_layout.addLayout(cash_layout)
        form_layout.addLayout(upi_layout)
        form_layout.addLayout(card_layout)

        return form_container

    def init_actions(self):
        actions_container = QWidget()
        actions_container.setStyleSheet("background-color: #7851a9;")

        #Buttons
        buttons_style = """
            QPushButton {
                font-size: 14px;
                font-weight: bold;
                color: "#7851a9";
                padding: 5px;
                background-color: #e5c8dc;
            }
            QPushButton:hover {
                background-color: #7851a9;
                color: #FFFFFF;
            }
        """

        # buttons
        self.save_button = QPushButton("Complete")
        self.save_button.setStyleSheet(buttons_style)
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setStyleSheet(buttons_style)
        self.print_button = QPushButton("Print")
        self.print_button.setStyleSheet(buttons_style)

        self.cancel_button.clicked.connect(self.exit)
        self.save_button.clicked.connect(self.save_invoice)
        self.print_button.clicked.connect(self.print_invoice)

        # layout
        buttons_layout = QHBoxLayout(actions_container)
        buttons_layout.setContentsMargins(0,0,0,0)
        buttons_layout.setSpacing(0)
        buttons_layout.addWidget(self.print_button)
        buttons_layout.addWidget(self.save_button)
        buttons_layout.addWidget(self.cancel_button)
        return actions_container

    def compute_payment(self, amount):
        net_amount = float(self.job_details['net_amount']) - (float(self.txt_card.text()) + float(self.txt_cash.text()) + float(self.txt_upi.text()))
        self.amount_lbl.setText(f"{net_amount:.2f}")

    def save_invoice(self):
        pass

    def exit(self):
        self.invoice_response.emit(None)
        self.close()

    def print_invoice(self):
        pass     