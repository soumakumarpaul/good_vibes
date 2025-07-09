from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QSizePolicy, QWidget, QLineEdit, QHBoxLayout, QComboBox, QPushButton, QMessageBox
from PySide6.QtCore import Signal, Qt, QRegularExpression
from PySide6.QtGui import QShortcut, QKeySequence, QRegularExpressionValidator
from tinydb import TinyDB

class ServiceDialog(QDialog):
    service_data = Signal(object)

    def __init__(self, folder_path, service = {}):
        super().__init__()
        self.db_path = folder_path
        self.employees = self.init_employees()
        self.setModal(True)
        self.setFixedSize(500, 500)
        self.service_details = service
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.init_shortucts()
        self.init_widgets()

    # Initialize all window shortcuts for this dialog
    def init_shortucts(self):
        '''
        Initialize Shortucts
        '''
        save_shortcut = QShortcut(QKeySequence.Save, self)
        save_shortcut.setContext(Qt.WindowShortcut)
        save_shortcut.activated.connect(self.save_service)

    # Initialize Widgets
    def init_widgets(self):
        #Main Layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Adding the header section.
        main_layout.addWidget(self.init_header())

        # Adding the form
        main_layout.addWidget(self.init_form())

        # Adding buttons
        main_layout.addWidget(self.init_actions())
        self.setLayout(main_layout)

    # Initialize the Header
    def init_header(self):
        #Header label
        header_label = QLabel("""<b>Service Details</b>""", self)
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

    # Initialize the form
    def init_form(self):
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

        # Service Name
        service_name = QLabel(self.service_details.get("name", ""))
        service_name.setStyleSheet("""
            QLabel {
                font-size: 20px;
                font-weight: bold;
                border: 2px solid #7851a9;
                color: #FFFFFF;
            }
        """)

        #Quantity Layout
        quantity_layout = QHBoxLayout()
        quantity_layout.setContentsMargins(0, 0, 0, 0)
        quantity_layout.setSpacing(0)

        # Price
        price_layout = QVBoxLayout()
        price_layout.setSpacing(5)
        price_validator = QRegularExpressionValidator(QRegularExpression(r"^[1-9]\d{1,4}(\.\d{1,2})?$"))
        price_lbl = QLabel("Price")
        price_lbl.setStyleSheet(input_field_label)
        service_price = str(self.service_details.get("price", 0.00))
        self.txt_price = QLineEdit(service_price)
        self.txt_price.setPlaceholderText("0.00")
        self.txt_price.setStyleSheet(input_field_style)
        self.txt_price.setValidator(price_validator)
        self.txt_price.textEdited.connect(self.compute_service)
        price_layout.addWidget(price_lbl)
        price_layout.addWidget(self.txt_price)

        # Quanitity
        qty_layout=QVBoxLayout()
        qty_layout.setSpacing(5)
        qty_validator = QRegularExpressionValidator(QRegularExpression(r"^[1-9]\d{1,2}$"))
        qty_lbl = QLabel("Qty")
        qty_lbl.setStyleSheet(input_field_label)
        self.txt_qty = QLineEdit("1")
        self.txt_qty.setStyleSheet(input_field_style)
        self.txt_qty.setValidator(qty_validator)
        self.txt_qty.textEdited.connect(self.compute_service)
        qty_layout.addWidget(qty_lbl)
        qty_layout.addWidget(self.txt_qty)
        
        quantity_layout.addLayout(price_layout)
        quantity_layout.addLayout(qty_layout)

        #Amount Layout
        amount_layout = QHBoxLayout()
        amount_layout.setContentsMargins(0, 0, 0, 0)
        amount_layout.setSpacing(0)

        # Discount
        discount_layout = QVBoxLayout()
        discount_layout.setSpacing(5)
        discount_validator = QRegularExpressionValidator(QRegularExpression(r"^[0-9]\d{0,1}(\.\d{1,2})?$"))
        discount_lbl = QLabel("Discount")
        discount_lbl.setStyleSheet(input_field_label)
        self.txt_discount = QLineEdit("0")
        self.txt_discount.setStyleSheet(input_field_style)
        self.txt_discount.setValidator(discount_validator)
        self.txt_discount.textEdited.connect(self.compute_net_amount)
        discount_layout.addWidget(discount_lbl)
        discount_layout.addWidget(self.txt_discount)

        # Amount
        amt_layout=QVBoxLayout()
        amt_layout.setSpacing(5)
        amt_validator = QRegularExpressionValidator(QRegularExpression(r"^[1-9]\d{1,4}(\.\d{1,2})?$"))
        amt_lbl = QLabel("Amount")
        amt_lbl.setStyleSheet(input_field_label)
        self.txt_amt = QLineEdit(str(self.service_details.get("price", "0.00")))
        self.txt_amt.setStyleSheet(input_field_style)
        self.txt_amt.setValidator(amt_validator)
        self.txt_amt.textEdited.connect(self.compute_discount)
        amt_layout.addWidget(amt_lbl)
        amt_layout.addWidget(self.txt_amt)
        
        amount_layout.addLayout(discount_layout)
        amount_layout.addLayout(amt_layout)

        # Server
        servers = [emp_name.get("name", "") for emp_name in self.employees]
        server_layout = QVBoxLayout()
        server_layout.setContentsMargins(0, 0, 0, 0)
        server_layout.setSpacing(0)
        server_lbl = QLabel("Server Name:")
        server_lbl.setStyleSheet(input_field_label)
        self.server_combo = QComboBox()
        self.server_combo.addItem("")
        self.server_combo.addItems(servers)
        self.server_combo.setStyleSheet(input_field_style)
        server_layout.addWidget(server_lbl)
        server_layout.addWidget(self.server_combo)

        # Helper
        helper_layout = QVBoxLayout()
        helper_layout.setContentsMargins(0, 0, 0, 0)
        helper_layout.setSpacing(0)
        helper_lbl = QLabel("Helper Name:")
        helper_lbl.setStyleSheet(input_field_label)
        self.helper_combo = QComboBox()
        self.helper_combo.addItem("")
        self.helper_combo.addItems(servers)
        self.helper_combo.setStyleSheet(input_field_style)
        helper_layout.addWidget(helper_lbl)
        helper_layout.addWidget(self.helper_combo)

        form_layout.addWidget(service_name)
        form_layout.addLayout(quantity_layout)
        form_layout.addLayout(amount_layout)
        form_layout.addLayout(server_layout)
        form_layout.addLayout(helper_layout)
        form_layout.addStretch(1)
        return form_container

    #Compute the amount based on quantity and price
    def compute_service(self, txt: str):
        if self.txt_qty.text() != "":
            rate = float(self.txt_price.text())
            quantity = int(self.txt_qty.text())
            self.txt_discount.setText("0")
            amount = rate * quantity
            self.txt_amt.setText("{:.2f}".format(amount))

    def compute_discount(self, net_price: str):
        rate = float(self.txt_price.text())
        quantity = int(self.txt_qty.text())
        discount = 100 - ((float(net_price)/(rate * quantity)) * 100)
        if 0 <= discount <= 100:
            self.txt_discount.setText("{:.2f}".format(discount))
        else:
            alert = QMessageBox()
            alert.setWindowTitle("Success")
            alert.setText("Discount should be in between 0 and 100")
            alert.setStandardButtons(QMessageBox.Ok)
            alert.exec()
            self.txt_amt.setText(str(self.service_details.get("price", "0.00")))

    def compute_net_amount(self, discount: str):
        rate = float(self.txt_price.text())
        quantity = int(self.txt_qty.text())
        print(discount)
        discount = float(discount)
        if discount > 100:
            alert = QMessageBox()
            alert.setWindowTitle("Success")
            alert.setText("Discount should be in between 0 and 100")
            alert.setStandardButtons(QMessageBox.Ok)
            alert.exec()
            self.txt_discount.setText("0")
        else:
            net_amount = (rate * quantity) * (100 - discount)/100
            self.txt_amt.setText("{:.2f}".format(net_amount))
            
    # Intialize the buttons. The Actions on the dialog like Save and Cancel
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
        self.save_button.clicked.connect(self.save_service)

        # layout
        buttons_layout = QHBoxLayout(actions_container)
        buttons_layout.setContentsMargins(0,0,0,0)
        buttons_layout.setSpacing(0)
        buttons_layout.addWidget(self.save_button)
        buttons_layout.addWidget(self.cancel_button)
        return actions_container
    
    # Execute validation of form and saving the service
    def save_service(self):
        '''
        Validate the form and save the service.
        This is also used to update the service.
        '''
        if self.server_combo.currentText() != "" and self.server_combo.currentText() == self.helper_combo.currentText():
            alert = QMessageBox()
            alert.setWindowTitle("Success")
            alert.setText("Server and Helper for a service should not be same.")
            alert.setStandardButtons(QMessageBox.Ok)
            alert.exec()
            return
        response = {
            "service": self.service_details.get("name", ""),
            "quantity": self.txt_qty.text(),
            "rate": self.txt_price.text(),
            "discount": self.txt_discount.text(),
            "price": self.txt_amt.text(),
            "server": self.server_combo.currentText(),
            "helper": self.helper_combo.currentText()
        }
        self.service_data.emit(response)
        self.close()

    # Get the employee names
    def init_employees(self):
        employee_db = TinyDB(self.db_path + "/employee_db.json")
        return employee_db.all()
    
    # Close the dialog.
    def exit(self):
        self.service_data.emit(None)
        self.close()
        
