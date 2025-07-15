from PySide6.QtWidgets import QVBoxLayout, QWidget, QLabel, QHBoxLayout, QPushButton
from PySide6.QtCore import Qt

class InvoiceItemWidget(QWidget):
    
    def __init__(self, service_details, index):
        super().__init__()
        self.index = index
        self.service = service_details
        self.setMouseTracking(True)
        layout = QVBoxLayout(self)
        layout.addWidget(self.init_header(), 1)
        layout.addLayout(self.init_particulars())
        layout.addLayout(self.init_servers())
        layout.setContentsMargins(8, 6, 8, 6)
        layout.setSpacing(4)

    # Header Label - Service Name
    def init_header(self):
        header_container = QWidget()
        header_container.setContentsMargins(0, 0, 0, 0)
        layout = QHBoxLayout(header_container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        service_lbl_txt = f"{self.index:02d}. {self.service.get("service", "")}\n        {self.service.get("category", "")}"
        service_label = QLabel(service_lbl_txt)
        service_label.setStyleSheet("""
            QLabel{
                font-weight: bold;
                font-size: 16px;
                color: #7851a9;
            }
        """)

        self.delete_button = QPushButton("Delete")
        self.edit_button = QPushButton("Edit")

        for btn in (self.edit_button, self.delete_button):
            btn.setFlat(True)
            btn.setVisible(False)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setStyleSheet("""
                QPushButton {
                    color: #2c2c2c;
                    font-weight: bold;
                    border: 1px solid #2c2c2c;
                    margin-left: 10px;
                    font-size: 12px;
                    padding: 4px;
                }
            """)

        layout.addWidget(service_label, 1)
        layout.addWidget(self.edit_button)
        layout.addWidget(self.delete_button)
        return header_container
    
    # Particulars
    def init_particulars(self):
        particulars_layout = QHBoxLayout()
        
        secondary_label = """
            QLabel{
                font-size: 14px;
                color: #7851a9;
            }
        """

        rate_label = QLabel("₹{:.2f}".format(float(self.service['rate'])))
        rate_label.setStyleSheet(secondary_label)

        discount = "{:.2f}".format(float(self.service['discount']))
        discount_label = QLabel(f"Less: {discount}%")
        discount_label.setStyleSheet(secondary_label)

        total_label = QLabel("₹{:.2f}".format(float(self.service['price'])))
        total_label.setStyleSheet(secondary_label)

        particulars_layout.addWidget(rate_label)
        particulars_layout.addStretch()
        particulars_layout.addWidget(discount_label)
        particulars_layout.addStretch()
        particulars_layout.addWidget(total_label)
        return particulars_layout
    
    # Assignee
    def init_servers(self):
        servers_layout = QHBoxLayout()

        secondary_label = """
            QLabel{
                font-size: 12px;
                color: #7851a9;
            }
        """
        server = self.service.get("server")
        server = server if server else "NA"
        helper = self.service.get("helper")
        helper = helper if helper else "NA"
        server_label = QLabel(server)
        server_label.setStyleSheet(secondary_label)
        divider = QLabel("X")
        divider.setStyleSheet(secondary_label)
        helper_label = QLabel(helper)
        helper_label.setStyleSheet(secondary_label)

        servers_layout.addWidget(server_label)
        servers_layout.addStretch()
        servers_layout.addWidget(divider)
        servers_layout.addStretch()
        servers_layout.addWidget(helper_label)
        return servers_layout
    
    def enterEvent(self, event):
        self.edit_button.setVisible(True)
        self.delete_button.setVisible(True)

    def leaveEvent(self, event):
        self.edit_button.setVisible(False)
        self.delete_button.setVisible(False)

