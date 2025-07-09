from PySide6.QtWidgets import QVBoxLayout, QWidget, QLabel, QHBoxLayout

class InvoiceItemWidget(QWidget):
    
    def __init__(self, service_details):
        super().__init__()
        self.service = service_details

        layout = QVBoxLayout(self)
        layout.addWidget(self.init_header())
        layout.addLayout(self.init_particulars())
        layout.addLayout(self.init_servers())
        layout.setContentsMargins(5, 2, 5, 2)

    # Header Label - Service Name
    def init_header(self):
        service_label = QLabel(self.service.get("name", ""))
        service_label.setStyleSheet("""
            QLabel{
                font-weight: bold,
                font-size: 16px;
                color: #7851a9;
            }
        """)
        return service_label
    
    # Particulars
    def init_particulars(self):
        particulars_layout = QHBoxLayout()
        
        secondary_label = """
            QLabel{
                font-size: 12px;
                color: #7851a9;
            }
        """

        rate_label = QLabel(f"₹{self.service['rate']} x {self.service['quantity']}")
        rate_label.setStyleSheet(secondary_label)

        discount_label = QLabel(f"Less: {self.service['discount']}%")
        discount_label.setStyleSheet(secondary_label)

        total_label = QLabel(f"₹{self.service['price']}")
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
                font-size: 10px;
                color: #7851a9;
            }
        """
        server = self.service.get("server")
        server = server if server else "NA"
        helper = self.service.get("helper")
        helper = helper if helper else "NA"
        server_label = QLabel(server)
        divider = QLabel("X")
        helper_label = QLabel(helper)

        servers_layout.addWidget(server_label)
        servers_layout.addStretch()
        servers_layout.addWidget(divider)
        servers_layout.addStretch()
        servers_layout.addWidget(helper_label)
        return servers_layout

