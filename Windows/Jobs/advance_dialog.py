from PySide6.QtWidgets import (QDialog, QVBoxLayout, QLabel, 
                               QSizePolicy, QWidget, QHBoxLayout, 
                               QLineEdit, QPushButton, QMessageBox)
from PySide6.QtCore import Qt, Signal
import re

class AdvanceDialog(QDialog):

    advance_response = Signal(object)

    def __init__(self, particulars = {}):
        super().__init__()
        self.particulars = particulars
        self.setModal(True)
        self.setFixedSize(300, 300)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.init_widgets()

    def init_widgets(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        main_layout.addWidget(self.init_header())

        main_layout.addWidget(self.init_input_form())
        main_layout.addStretch()

        main_layout.addWidget(self.init_actions())

        self.setLayout(main_layout)

    def init_header(self):
        #Header label
        header_label = QLabel("""<b>Advance Payment</b>""", self)
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
    
    def init_actions(self):
        actions_container = QWidget()
        actions_container.setStyleSheet("background-color: #7851a9;")

        #Buttons
        buttons_style = """
            QPushButton {
                font-size: 20px;
                font-weight: bold;
                color: #7851a9;
                padding: 10px;
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
        self.save_button.clicked.connect(self.save)

        # layout
        buttons_layout = QHBoxLayout(actions_container)
        buttons_layout.setContentsMargins(0,0,0,0)
        buttons_layout.setSpacing(0)
        buttons_layout.addWidget(self.save_button)
        buttons_layout.addWidget(self.cancel_button)
        return actions_container

    def init_input_form(self):
        form_container = QWidget()
        form_container.setStyleSheet('border: 2px solid #c0c0c0;')
        form_layout = QVBoxLayout(form_container)
        form_layout.setContentsMargins(5, 5, 5, 5)

        #Line Edit
        input_field_style = """
            QLineEdit {
                padding: 4px;
                font-size: 20px;
                background-color: #FFFFFF;
                color: #2c2c2c;
                border: 2px solid #7851a9;
            }
        """

        input_field_label = """
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: #C0C0C0;
                border: 0px solid;
            }
        """

        amount_lbl = QLabel("Amount:")
        amount_lbl.setStyleSheet(input_field_label)

        payment = self.particulars.get('price', '0.00')
        self.amount_txt = QLineEdit(payment)
        self.amount_txt.setPlaceholderText("Advance Amount")
        self.amount_txt.setStyleSheet(input_field_style)

        form_layout.addWidget(amount_lbl)
        form_layout.addWidget(self.amount_txt)
        return form_container

    def save(self):
        pattern = r'^\d+(\.\d{1,2})?$'
        amount = self.amount_txt.text().strip()
        if re.match(pattern, amount):
            response = {
                "service": f"Advance Payment: ₹{amount}",
                "rate": amount,
                "discount": "0",
                "quantity": "1",
                "price": amount,
                "server": "",
                "helper": "",
                "category": self.particulars.get('category', 'Credits'),
                "type": "advance"
            }
            self.advance_response.emit(response)
            self.close()
        else:
            QMessageBox.critical(self, 
                                 "Payment Error", 
                                 "Please check the amount",
                                 QMessageBox.Ok,
                                 defaultButton=QMessageBox.Ok)
            
    def exit(self):
        self.advance_response.emit(None)
        self.close()
