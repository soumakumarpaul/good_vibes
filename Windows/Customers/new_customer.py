from PySide6.QtWidgets import QDialog, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSizePolicy, QPushButton, QLineEdit, QComboBox, QMessageBox
from PySide6.QtCore import Qt, QRegularExpression, Signal, QTimer
from PySide6.QtGui import QRegularExpressionValidator, QShortcut, QKeySequence
from datetime import datetime
import re
from tinydb import TinyDB
from Utilities.counters import Counters
from Windows.General.select_box import SelectBox

class NewCustomer(QDialog):
    shared_data = Signal(object)
    
    def __init__(self, file_path, phone:str = ""):
        super().__init__()
        self.setModal(True)
        self.setFixedSize(400, 400)
        self.db = TinyDB(file_path + "/customers_db.json")
        self.file_path = file_path
        self.phone = phone
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.init_widgets()
        self.init_shortcut()
        QTimer.singleShot(0, self.customer_name.setFocus)
        self.customer_name.setCursorPosition(0)

    def init_shortcut(self):
        esc_shortcut = QShortcut(QKeySequence(Qt.Key_Escape), self)
        esc_shortcut.setContext(Qt.WindowShortcut)
        esc_shortcut.activated.connect(self.exit)

        save_shortcut = QShortcut(QKeySequence.Save, self)
        save_shortcut.setContext(Qt.WindowShortcut)
        save_shortcut.activated.connect(self.save_customer)

    def init_widgets(self):
        # 2layouts
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0,0,0,0)
        main_layout.setSpacing(0)

        #header
        header = self.init_header()
        main_layout.addWidget(header)

        #form fields
        form_widget = self.init_form()
        main_layout.addWidget(form_widget)

        #action widgets
        action_widget = self.init_actions()
        main_layout.addWidget(action_widget)

        self.setLayout(main_layout)

    def init_header(self):
        #Header label
        header_label = QLabel("""<b>New Customer</b>""", self)
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

        input_field_lable = """
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: #C0C0C0;
                border: 0px solid;
            }
        """
        #Name
        name_layout = QVBoxLayout()
        name_layout.setContentsMargins(0,0,0,0)
        name_layout.setSpacing(0)
        self.name_lbl = QLabel("Customer Name")
        self.name_lbl.setStyleSheet(input_field_lable)
        self.customer_name = QLineEdit()
        self.customer_name.setPlaceholderText("Name")
        self.customer_name.setStyleSheet(input_field_style)
        name_layout.addWidget(self.name_lbl)
        name_layout.addSpacing(5)
        name_layout.addWidget(self.customer_name)
        
        #Phone Number
        phone_layout = QVBoxLayout()
        phone_layout.setContentsMargins(0,0,0,0)
        phone_layout.setSpacing(0)
        phone_pattern = r"^[6-9]\d{9}$"
        regex = QRegularExpression(phone_pattern)
        validator = QRegularExpressionValidator(regex)
        phone_lbl = QLabel("Mobile Number")
        phone_lbl.setStyleSheet(input_field_lable)
        set_phone = ""
        if re.match(phone_pattern, self.phone):
            set_phone = self.phone
        self.phone_number = QLineEdit(set_phone)
        self.phone_number.setPlaceholderText("Contact Number")
        self.phone_number.setStyleSheet(input_field_style)
        self.phone_number.setValidator(validator)
        phone_layout.addWidget(phone_lbl)
        phone_layout.addSpacing(5)
        phone_layout.addWidget(self.phone_number)

        #Gender
        gender_layout = QVBoxLayout()
        gender_layout.setContentsMargins(0,0,0,0)
        gender_layout.setSpacing(0)
        gender_lbl = QLabel("Gender")
        gender_lbl.setStyleSheet(input_field_lable)
        self.gender_combo = SelectBox()
        self.gender_combo.setFocusPolicy(Qt.StrongFocus)
        self.gender_combo.addItems(["Female", "Male", "Other"])
        self.gender_combo.setStyleSheet(input_field_style)
        gender_layout.addWidget(gender_lbl)
        gender_layout.addSpacing(5)
        gender_layout.addWidget(self.gender_combo)

        form_layout.addLayout(phone_layout)
        form_layout.addLayout(name_layout)
        form_layout.addLayout(gender_layout)
        form_layout.addStretch(1)
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
        self.save_button.clicked.connect(self.save_customer)

        # layout
        buttons_layout = QHBoxLayout(actions_container)
        buttons_layout.setContentsMargins(0,0,0,0)
        buttons_layout.setSpacing(0)
        buttons_layout.addWidget(self.save_button)
        buttons_layout.addWidget(self.cancel_button)
        return actions_container

    def save_customer(self):
        customer = {
            "_id": self.generate_id(),
            "name": self.customer_name.text().strip().title(),
            "mobile": self.phone_number.text().strip(),
            "gender": self.gender_combo.currentText(),
            "registered_on": datetime.today().strftime("%d %b %Y"),
            "timestamp": datetime.today().timestamp()
        }
        # insert customer
        self.db.insert(customer)
        message = "New Customer Added Successfully."
        response = customer
        self.shared_data.emit(response) 
        alert = QMessageBox()
        alert.setWindowTitle("Success")
        alert.setText(message)
        alert.setStandardButtons(QMessageBox.Ok)
        alert.exec()
        self.close()
    
    def generate_id(self):
        now = datetime.now()
        month = f"{now.month:02d}"
        year = now.year
        counter = Counters(self.file_path)
        id = int(counter.get_count("CUSTOMERS"))
        return f"CUST-{id:04d}-{month}-{year}"

    def exit(self):
        self.shared_data.emit(None)
        self.close()