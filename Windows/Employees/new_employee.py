from PySide6.QtWidgets import QDialog, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSizePolicy, QPushButton, QLineEdit, QComboBox, QListView, QMessageBox
from PySide6.QtCore import Qt, QRegularExpression, Signal
from PySide6.QtGui import QRegularExpressionValidator, QShortcut, QKeySequence, QStandardItem, QStandardItemModel
from tinydb import Query
from datetime import datetime
import re

class NewEmployee(QDialog):
    shared_data = Signal(object)

    def __init__(self, db):
        super().__init__()
        self.setModal(True)
        self.setFixedSize(400, 400)
        self.db = db
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.init_widgets()
        self.init_shortcut()

    def init_shortcut(self):
        save_shortcut = QShortcut(QKeySequence.Save, self)
        save_shortcut.setContext(Qt.WindowShortcut)
        save_shortcut.activated.connect(self.save_employee)

    def init_widgets(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        #header
        header = self.init_header()
        main_layout.addWidget(header)

        #form fields        
        form_widget = self.init_form()
        main_layout.addWidget(form_widget)

        #actions container
        actions_widget = self.init_actions()
        main_layout.addWidget(actions_widget)

        self.setLayout(main_layout)

    def init_header(self):
        #Header label
        header_label = QLabel("""<b>New Employee</b>""", self)
        header_label.setTextFormat(Qt.RichText)
        header_label.setStyleSheet("""
            QLabel {
                background-color: #7851a9;
                color: #ffffff;
                font-size: 30px;
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
            QLineEdit {
                padding: 4px;
                font-size: 20px;
                background-color: #FFFFFF;
                color: #7851a9;
                border: 2px solid #9c65e0;
            }
        """

        input_field_lable = """
            QLabel {
                font-size: 10px;
                color: #C0C0C0;
                border: 0px solid;
            }
        """
        #Name
        name_layout = QVBoxLayout()
        name_layout.setContentsMargins(0,0,0,0)
        name_layout.setSpacing(0)
        self.name_lbl = QLabel("Employee Name")
        self.name_lbl.setStyleSheet(input_field_lable)
        self.employee_name = QLineEdit()
        self.employee_name.setPlaceholderText("Name")
        self.employee_name.setStyleSheet(input_field_style)
        name_layout.addWidget(self.name_lbl)
        name_layout.addSpacing(5)
        name_layout.addWidget(self.employee_name)
        
        #Phone Number
        phone_layout = QVBoxLayout()
        phone_layout.setContentsMargins(0,0,0,0)
        phone_layout.setSpacing(0)
        phone_pattern = r"^[6-9]\d{9}$"
        regex = QRegularExpression(phone_pattern)
        validator = QRegularExpressionValidator(regex)
        phone_lbl = QLabel("Mobile Number")
        phone_lbl.setStyleSheet(input_field_lable)
        self.phone_number = QLineEdit()
        self.phone_number.setPlaceholderText("Contact Number")
        self.phone_number.setStyleSheet(input_field_style)
        self.phone_number.setValidator(validator)
        phone_layout.addWidget(phone_lbl)
        phone_layout.addSpacing(5)
        phone_layout.addWidget(self.phone_number)

        form_layout.addLayout(name_layout)
        form_layout.addLayout(phone_layout)
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
        self.save_button.clicked.connect(self.save_employee)

        # layout
        buttons_layout = QHBoxLayout(actions_container)
        buttons_layout.setContentsMargins(0,0,0,0)
        buttons_layout.setSpacing(0)
        buttons_layout.addWidget(self.save_button)
        buttons_layout.addWidget(self.cancel_button)
        return actions_container

    def generate_id(self):
        records = self.db.all()
        now = datetime.now()
        month = f"{now.month:02d}"
        year = now.year

        if records:
            last_id = records[-1].get("id", "")
            match = re.match(r"EMP-(\d+)-\d{2}-\d{4}", last_id)
            if match:
                last_seq = int(match.group(1))
            else:
                last_seq = 0
        else:
            last_seq = 0
        return f"EMP-{last_seq+1:03d}-{month}-{year}"

    def exit(self):
        self.shared_data.emit(None)
        self.close()

    def save_employee(self):
        employee = {
            "_id": self.generate_id(),
            "name": self.employee_name.text().strip(),
            "mobile": self.phone_number.text().strip()
        }
        self.db.insert(employee)
        response = {"Name": self.employee_name.text().strip(), "Phone": self.phone_number.text().strip()}
        self.shared_data.emit(response)
        alert = QMessageBox()
        alert.setWindowTitle("Success")
        alert.setText("New Employee Added Successfully")
        alert.setStandardButtons(QMessageBox.Ok)
        alert.exec()
        self.exit()