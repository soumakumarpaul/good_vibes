from PySide6.QtWidgets import QDialog, QWidget, QLabel, QLineEdit, QSizePolicy, QVBoxLayout, QHBoxLayout, QPushButton, QMessageBox
from PySide6.QtCore import Qt, Signal, QTimer
from PySide6.QtGui import QShortcut, QKeySequence
from datetime import date
from tinydb import TinyDB, Query
from Utilities.counters import Counters
from datetime import datetime, date

class Invoice(QDialog):

    invoice_response = Signal(bool)

    def __init__(self, folder_path, job_details):
        super().__init__()
        self.setModal(True)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setFixedSize(400, 500)
        self.folder_path = folder_path
        self.job_details = job_details
        self.net_amount = self.job_details.get('net_amount', 0)
        self.init_shortcuts()
        self.init_widgets()
        self.init_customer_advance()

        QTimer.singleShot(0, self.txt_upi.setFocus)
        self.txt_upi.selectAll()
        self.txt_upi.setCursorPosition(len(self.txt_upi.text()))

    def init_shortcuts(self):
        exit_shortcut = QShortcut(QKeySequence("Ctrl+X"), self)
        exit_shortcut.setContext(Qt.WindowShortcut)
        exit_shortcut.activated.connect(self.exit)

        save_shortcut = QShortcut(QKeySequence("Return"), self)
        save_shortcut.setContext(Qt.WindowShortcut)
        save_shortcut.activated.connect(self.save_invoice)

        complete_shortcut = QShortcut(QKeySequence("Enter"), self)
        complete_shortcut.setContext(Qt.WindowShortcut)
        complete_shortcut.activated.connect(self.save_invoice)

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
                font-size: 20px;
                font-weight: bold;
                color: #FFFFFF;
                padding: 5px;
            }
        """

        payment_lbl = QLabel("To Pay:")
        payment_lbl.setStyleSheet(payment_style)
        payment_layout.addWidget(payment_lbl)
        amt = f"{self.net_amount:.2f}"
        self.amount_lbl = QLabel(amt)
        self.amount_lbl.setStyleSheet(payment_style)
        self.amount_lbl.setAlignment(Qt.AlignRight)
        payment_layout.addWidget(self.amount_lbl)

        return payment_container

    def init_payment_form(self):
        form_container = QWidget()
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
                font-size: 18px;
                font-weight: bold
                color: #C0C0C0;
            }
        """

        #Advance
        advance_layout = QVBoxLayout()
        advance_layout.setContentsMargins(0, 0, 0, 0)
        advance_layout.setSpacing(0)
        advance_label = QLabel("Advance")
        advance_label.setStyleSheet(input_field_label)
        self.txt_advance = QLineEdit("0.00")
        self.txt_advance.setPlaceholderText("0.00")
        self.txt_advance.setStyleSheet(input_field_style)
        self.txt_advance.textChanged.connect(self.compute_payment)

        advance_layout.addWidget(advance_label)
        advance_layout.addWidget(self.txt_advance)

        # Cash
        cash_layout = QVBoxLayout()
        cash_layout.setContentsMargins(0,0,0,0)
        cash_layout.setSpacing(0)
        cash_label = QLabel("Cash")
        cash_label.setStyleSheet(input_field_label)
        self.txt_cash = QLineEdit("0.00")
        self.txt_cash.setPlaceholderText("0.00")
        self.txt_cash.setStyleSheet(input_field_style)
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
        self.txt_card.textEdited.connect(self.compute_payment)
        card_layout.addWidget(card_label)
        card_layout.addWidget(self.txt_card)

        # Credit Layout
        credit_layout = QVBoxLayout()
        credit_layout.setContentsMargins(0,0,0,0)
        credit_layout.setSpacing(0)
        credit_label = QLabel("Credit")
        credit_label.setStyleSheet(input_field_label)
        self.txt_credit = QLineEdit("0.00")
        self.txt_credit.setPlaceholderText("0.00")
        self.txt_credit.setStyleSheet(input_field_style)
        self.txt_credit.textEdited.connect(self.compute_payment)
        credit_layout.addWidget(credit_label)
        credit_layout.addWidget(self.txt_credit)
        
        form_layout.addLayout(upi_layout)
        form_layout.addLayout(cash_layout)
        form_layout.addLayout(card_layout)
        form_layout.addLayout(credit_layout)
        form_layout.addLayout(advance_layout)

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
        if (self.txt_advance.text().strip != "" and 
            self.txt_credit.text().strip() != "" and
            self.txt_card.text().strip() != "" and
            self.txt_cash.text().strip() != "" and
            self.txt_upi.text().strip() != ""):
            try:
                self.net_amount = (float(self.job_details['net_amount']) - 
                                (float(self.txt_advance.text()) + 
                                    float(self.txt_credit.text()) + 
                                    float(self.txt_card.text()) + 
                                    float(self.txt_cash.text()) + 
                                    float(self.txt_upi.text())))
                self.amount_lbl.setText(f"{self.net_amount:.2f}")
            except (ValueError, TypeError):
                QMessageBox.critical(self, "Invalid Amount", "Only Numbers are allowed in amounts.")

    def init_customer_advance(self):
        customer_info = self.job_details['customer']
        if customer_info:
            advance = float(customer_info.get('advance', 0))
            amount = float(self.net_amount)
            if advance < amount:
                self.txt_advance.setText(f"{advance:.2f}")
            else:
                self.txt_advance.setText(f"{amount:.2f}")
        else:
            self.txt_advance.setText('0.00')

    def save_invoice(self):
        if float(self.txt_credit.text().strip()) > 0 and not self.job_details['customer']:
            QMessageBox.critical(self, "Invoice", "Credit cannot be provided without customer details")
            return
        if float(self.net_amount != 0):
            QMessageBox.information(self, "Error", "Please update payment methods carefully")
            return
        invoice = {
            "_id": self.generate_invoice_id(),
            "payments": {
                "cash": self.txt_cash.text(),
                "card": self.txt_card.text(),
                "advance": self.txt_advance.text(),
                "upi": self.txt_upi.text(),
                "credits": self.txt_credit.text()
            },
            "details": self.job_details,
            "date":  date.today().isoformat(),
            "time": datetime.now().time().isoformat(timespec="seconds")
        }
        if self.update_customer_info():
            self.save_expenses(self.job_details['_id'])
            db = TinyDB(self.folder_path + "/jobs_db.json")
            Jobs = Query()
            db.update({'isComplete': True}, Jobs._id == self.job_details['_id'])
            db.close()
            invoice_db = TinyDB(self.folder_path + "/invoice_db.json")
            invoice_db.insert(invoice)
            invoice_db.close()
            self.invoice_response.emit(True)
            self.close()
        else:
            self.exit()

    def generate_invoice_id(self):
        counter = Counters(self.file_path)
        now = datetime.now()
        month = f"{now.month:02d}"
        year = now.year
        return f"INV-{int(counter.get_count("INVOICE")):04d}-{month}-{year}"

    def save_expenses(self, invoice_id):
        cash_amount = float(self.txt_cash.text())
        card_amount = float(self.txt_card.text())
        upi_amount = float(self.txt_upi.text())
        credit_amount = float(self.txt_credit.text())
        if cash_amount > 0:
            self.record_expenses("cash", cash_amount, invoice_id)
        if card_amount > 0:
            self.record_expenses("card", card_amount, invoice_id)
        if upi_amount > 0:
            self.record_expenses("upi", upi_amount, invoice_id)
        if credit_amount > 0:
            self.record_expenses("credit", credit_amount, invoice_id)
        
    def record_expenses(self, method, amount, invoice_id):
        response = {
            "amount": amount,
            "purpose": invoice_id,
            "method": method,
            "from": "",
            "payer": "",
            "date": date.today().isoformat(),
            "type": "debit" if method == "credit" else "credit"
        }
        db = TinyDB(self.folder_path + "/accounts_db.json")
        db.insert(response)
        db.close()

    def update_customer_info(self):
        customer = self.job_details.get("customer", None)
        services = self.job_details.get("services", None)
        advance_payment = 0
        credits_payment = 0
        for service in services:
            if service['type'] == "advance":
                advance_payment = service['price']
            if service['type'] == "credit":
                credits_payment = service['price']
        if customer:
            advance_payment = float(advance_payment) + float(customer.get('advance', 0)) - float(self.txt_advance.text())
            credits = float(customer.get('credits', 0)) + float(self.txt_credit.text()) - credits_payment
            db = TinyDB(self.folder_path + "/customers_db.json")
            Customers = Query()
            customer_id = customer['_id']
            db.update({"advance": advance_payment, 'credit': credits}, Customers._id == customer_id)
            db.close()
        else:
            QMessageBox.critical(self, "No Customers Selected", "Customer details not available. Always mention customer details.")
        return True

    def exit(self):
        self.invoice_response.emit(False)
        self.close()

    def print_invoice(self):
        pass     