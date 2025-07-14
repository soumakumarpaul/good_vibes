from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QGridLayout, QListView, QListWidget, QLineEdit, QLabel, QSizePolicy, QVBoxLayout, QHBoxLayout, QMessageBox, QListWidgetItem
from PySide6.QtGui import QStandardItemModel, QStandardItem, QKeySequence, QShortcut
from PySide6.QtCore import Qt
from tinydb import TinyDB, Query
from PySide6.QtWidgets import QAbstractItemView
import re
from functools import partial
from Windows.Customers.new_customer import NewCustomer
from .service_dialog import ServiceDialog
from .invoice_item_widget import InvoiceItemWidget

class Jobs(QWidget):
    def __init__(self, file_path: str):
        super().__init__()
        self.file_path = file_path
        self.catalog = []
        self.customer_info = {}
        self.service_results = []
        self.job_details = {"services": [], "gross_total": 0, "discount": 0, "net_amount": 0} # This is the invoice details.
        self.setWindowFlags(Qt.Window | Qt.CustomizeWindowHint | Qt.WindowTitleHint)
        self.init_shortcuts()
        self.init_widgets()

    def init_shortcuts(self):
        exit_shortcut = QShortcut(QKeySequence("Ctrl+X"), self)
        exit_shortcut.setContext(Qt.WindowShortcut)
        exit_shortcut.activated.connect(self.exit)

        save_shortcut = QShortcut(QKeySequence("Ctrl+S"), self)
        save_shortcut.setContext(Qt.WindowShortcut)
        save_shortcut.activated.connect(self.save)

        invoice_shortcut = QShortcut(QKeySequence("Ctrl+I"), self)
        invoice_shortcut.setContext(Qt.WindowShortcut)
        invoice_shortcut.activated.connect(self.invoice)

    def exit(self):
        reply = QMessageBox.question(self, 
                                     "Confirmation", 
                                     "Cancel without Saving the Job?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.close()

    def save(self):
        if len(self.job_details['services']) == 0:
            QMessageBox.information(self, "Save Job", "No Services in job to save.", QMessageBox.Ok)
        else:
            jobs_db = TinyDB(self.file_path + "/jobs_db.json")
            self.job_details['customer'] = self.customer_info
            self.job_details['state'] = "active"
            jobs_db.insert(self.job_details)
            QMessageBox.information(self, "Save Successful", "The Job is successfully saved.", QMessageBox.Ok)
            self.close()

    def invoice(self):
        pass

    def init_catalog(self):
        db = TinyDB(self.file_path + "/catalog_db.json")
        self.catalog = db.all()
        db.close()

    def get_customer_info(self, phone_number: str):
        if re.match(r"^[6-9]\d{9}$", phone_number):
            db = TinyDB(self.file_path + "/customers_db.json")
            Customer: Query = Query()
            results = db.search(Customer.mobile == phone_number)
            if results == []:
                self.add_customer = NewCustomer(db, phone_number)
                self.add_customer.shared_data.connect(self.get_new_customer)
                self.add_customer.exec()
            else:
                self.customer_info = results[0]
            db.close()
            self.customer_name_field.setText(self.customer_info.get("name", ""))
            membership_details = self.customer_info.get("membership", {})
            self.membership_points.setText(f"Points: {membership_details.get("points", 0)}")

    def get_new_customer(self, data):
        self.customer_name_field.setText(data.get("name"))
        self.membership_points.setText("Points: 0")
    
    def init_widgets(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Header
        main_layout.addWidget(self.init_header())

        main_layout.addLayout(self.invoice_layout())

        self.setLayout(main_layout)
    
    def init_header(self):
        header_label = QLabel("""<b>Jobs Unit</b>""", self)
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
    
    def init_customer(self):
        customer_container = QWidget()
        customer_container.setContentsMargins(0, 0, 0, 0)
        customer_container.setStyleSheet("background-color: #f1eafb;")
        customer_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        customer_layout = QVBoxLayout(customer_container)
        customer_layout.setSpacing(0)

        customer_phone = QLineEdit()
        customer_phone.setPlaceholderText("Customer Number")
        customer_phone.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                font-size: 16px;
                background-color: #FFFFFF;
                font-weight: bold;
                color: #7851a9;
                border: 1px solid #2c2c2c;
            }
        """)
        customer_phone.textChanged.connect(self.get_customer_info)

        customer_layout.addWidget(customer_phone)

        customer_info_layout = QHBoxLayout()
        customer_name = QLabel("Name")
        customer_name.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
                padding: 10px;
                background-color: #ccaff0;
                color: #7851a9;
                border: 1px solid #7851a9;
                margin-top: 5px;
            }
        """)
        self.customer_name_field = customer_name

        customer_points = QLabel("Points:")
        customer_points.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
                padding: 10px;
                background-color: #ccaff0;
                color: #7851a9;
                border: 1px solid #7851a9;
                margin-top: 5px;
            }
        """)
        self.membership_points = customer_points
        
        customer_info_layout.addWidget(self.customer_name_field)
        customer_info_layout.addWidget(customer_points)

        customer_layout.addLayout(customer_info_layout)
        return customer_container
    
    def invoice_layout(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.init_service_picker())
        layout.addLayout(self.init_invoice_layout())
        return layout
  
    def init_service_picker(self):
        service_container = QWidget()
        service_container.setMinimumWidth(900)
        service_container.setContentsMargins(0, 0, 0, 0)
        service_container.setStyleSheet("border: 1px solid #ffffff;")
        layout = QHBoxLayout(service_container)
        layout.setSpacing(0)
        layout.addWidget(self.init_catalog_category())

        #initialize sub category layout
        sub_cat_container = QWidget()
        sub_cat_container.setFixedWidth(300)
        self.sub_cat_layout = QGridLayout(sub_cat_container)
        self.sub_cat_layout.setContentsMargins(0, 0, 0, 0)
        self.sub_cat_layout.setSpacing(0)

        layout.addWidget(sub_cat_container)

        layout.addLayout(self.init_services())

        return service_container

    def init_catalog_category(self):
        self.init_catalog()
        category_container = QWidget()
        category_layout = QVBoxLayout(category_container)
        category_layout.setContentsMargins(0, 0, 0, 0)
        category_layout.setSpacing(0)

        button_styles = """
            QPushButton{
            font-size: 14px;
            font-weight: bold;
            color: #FFFFFF;
            background-color: #2c2c2c;
            border: 1px solid #FFFFFF;
            padding: 5px;
            }
        """

        for category in self.catalog:
            category_name = category.get("category", "").replace(" ", "\n")
            button = QPushButton(category_name)
            
            button.setStyleSheet(button_styles)
            button.clicked.connect(partial(self.init_sub_category, category.get("catalog", [])))
            button.setFixedWidth(120)
            button.setCursor(Qt.PointingHandCursor)
            button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
            category_layout.addWidget(button, stretch=1)
        return category_container

    def init_sub_category(self, catalog = []):
        self.clear_sub_layout()
        button_styles = """
            QPushButton{
            font-size: 14px;
            font-weight: bold;
            color: #FFFFFF;
            background-color: #7851a9;
            border: 1px solid #FFFFFF;
            padding: 10px;
            }
        """
        for index, category in enumerate(catalog):
            sub_category = category.get("sub-category", "").replace(" ", "\n")
            button = QPushButton(sub_category)
            button.setStyleSheet(button_styles)
            button.setFixedWidth(150)
            button.setCursor(Qt.PointingHandCursor)
            button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
            button.clicked.connect(partial(self.get_services, category.get("services", [])))
            row = index // 2
            col = index % 2
            self.sub_cat_layout.addWidget(button, row, col)

    def get_services(self, services = []):
        self.service_results = services
        self.search_services()

    def clear_sub_layout(self):
        while self.sub_cat_layout.count():
            item = self.sub_cat_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)

    def init_services(self, services = []):
        services_layout = QVBoxLayout()
        services_layout.setContentsMargins(0, 0, 0, 0)
        services_layout.setSpacing(0)

        search_bar = QLineEdit()
        search_bar.setPlaceholderText("Search Catalog")
        search_bar.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                font-size: 16px;
                background-color: #FFFFFF;
                font-weight: bold;
                color: #7851a9;
                border: 1px solid #2c2c2c;
            }
        """)
        search_bar.textEdited.connect(lambda text: self.search_services(text))

        self.services_list = QListView()
        self.services_list.setStyleSheet("""
            QListView {
                background-color: #FFFFFF;
                border: 1px solid #2c2c2c;
                font-size: 16px;
            }
            QListView::item {
                padding: 5px;
                border-bottom: 1px solid #2c2c2c;
                color: #7851a9;
                font-weight: bold;
            }
            QListView::item:hover {
                background-color: #f5f5f5;
            }
            QListView::item:selected {
                background-color: #d0f0ff;
                color: black;
            }
        """)

        self.services_list.setTextElideMode(Qt.ElideRight)
        self.services_list.setWordWrap(False)
        self.services_list.setUniformItemSizes(True)

        self.services_list.clicked.connect(self.on_service_selected)

        services_layout.addWidget(search_bar)
        services_layout.addWidget(self.services_list)

        return services_layout

    def search_services(self, search_keyword: str = ""):
        model: QStandardItemModel = QStandardItemModel()
        keyword = search_keyword.strip().lower().split()
        items = [item for item in self.service_results
                 if all(word in item.get("name", "").lower() for word in keyword)]
        for item in items:
            service_item = QStandardItem(item["service"])
            service_item.setToolTip(item["service"])
            service_item.setData(item, Qt.UserRole)
            model.appendRow(service_item)
        self.service_list_model = model
        self.services_list.setModel(model)

    # Select the service from the service picker
    def on_service_selected(self, index):
        if self.service_list_model:
            item = self.service_list_model.itemFromIndex(index)
            service_details = item.data(Qt.UserRole)
            self.service_dialog = ServiceDialog(self.file_path, service_details)
            self.service_dialog.service_data.connect(self.add_service_invoice)
            self.service_dialog.exec()

    # Adding service to invoice
    def add_service_invoice(self, service_data):
        if service_data != None:
            index = len(self.job_details['services'])
            self.job_details["services"].append(service_data)
            self.reinitialize_invoice_amount()
            self.add_service_to_invoice_list(service_data, index)

    def init_invoice_layout(self):
        invoice_layout = QVBoxLayout()
        invoice_layout.setContentsMargins(0, 0, 0, 0)
        invoice_layout.setSpacing(0)

        invoice_layout.addWidget(self.init_customer())
        invoice_layout.addWidget(self.invoice_view(), 1)
        invoice_layout.addStretch()
        invoice_layout.addLayout(self.invoice_total_view())
        invoice_layout.addLayout(self.job_actions())
        return invoice_layout
    
    def invoice_view(self):
        self.invoice_list = QListWidget()
        self.invoice_list.setStyleSheet("""
        QListWidget {
            background-color: #ffffff;
            border: 1px solid #7851a9;
        }
        QListWidget::item {
            border-bottom: 1px solid #7851a9;
        }
        QListWidget::item:selected {
            background-color: #f2f2f2;
        }
        """)
        for index, service in enumerate(self.job_details['services']):
            self.add_service_to_invoice_list(service)
        return self.invoice_list
    
    def add_service_to_invoice_list(self, service, index):
        item = QListWidgetItem()
        widget = InvoiceItemWidget(service, index+1)
        widget.adjustSize()
        item.setSizeHint(widget.sizeHint())
        self.invoice_list.addItem(item)
        self.invoice_list.setItemWidget(item, widget)
        widget.delete_button.clicked.connect(lambda: self.delete_service_from_invoice(index))
        widget.edit_button.clicked.connect(lambda: self.edit_service_from_invoice(index))

    def delete_service_from_invoice(self, index):
        reply = QMessageBox.question(self, "Confirmation",
                                     f"Do you want to delete - {self.job_details['services'][index]['service']}?", 
                                     QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)
        if(reply == QMessageBox.Yes):
            del(self.job_details['services'][index])
            self.invoice_list.clear()
            for index, service in enumerate(self.job_details['services']):
                self.add_service_to_invoice_list(service, index)
            self.reinitialize_invoice_amount()

    def edit_service_from_invoice(self, index):
        self.service_dialog = ServiceDialog(self.file_path, self.job_details['services'][index])
        self.service_dialog.service_data.connect(lambda data: self.update_service_invoice(data, index))
        self.service_dialog.exec()

    def update_service_invoice(self, service_data, index):
        if service_data != None:
            service = self.job_details['services'][index]
            service['rate'] = service_data['rate']
            service['discount'] = service_data['discount']
            service['price'] = service_data['price']
            service['server'] = service_data['server']
            service['helper'] = service_data['helper']
            self.invoice_list.clear()
            for index, service in enumerate(self.job_details['services']):
                self.add_service_to_invoice_list(service, index)
            self.reinitialize_invoice_amount()
            
    def invoice_total_view(self):
        amount_layout = QVBoxLayout()

        invoice_total_style = """
            QLabel {
                font-weight: bold;
                color: 2c2c2c;
                border-bottom: 1px solid #2c2c2c;
                font-size: 20px;
                padding:10px;
            }
        """

        #Gross Total
        gross_layout = QHBoxLayout()
        gross_label = QLabel("Gross:")
        gross_label.setStyleSheet(invoice_total_style)
        self.gross_amt_label = QLabel("₹{:.2f}".format(self.job_details["gross_total"]))
        self.gross_amt_label.setStyleSheet(invoice_total_style)
        gross_layout.addWidget(gross_label)
        gross_layout.addStretch()
        gross_layout.addWidget(self.gross_amt_label)

        #Discount Total
        discount_layout = QHBoxLayout()
        discount_label = QLabel("Discount:")
        discount_label.setStyleSheet(invoice_total_style)
        self.discount_amt_label = QLabel("₹{:.2f}".format(self.job_details["discount"]))
        self.discount_amt_label.setStyleSheet(invoice_total_style)
        discount_layout.addWidget(discount_label)
        discount_layout.addStretch()
        discount_layout.addWidget(self.discount_amt_label)

        #Net Amount
        net_layout = QHBoxLayout()
        net_label = QLabel("Total:")
        net_label.setStyleSheet(invoice_total_style)
        self.net_amt_label = QLabel("₹{:.2f}".format(self.job_details["net_amount"]))
        self.net_amt_label.setStyleSheet(invoice_total_style)
        net_layout.addWidget(net_label)
        net_layout.addStretch()
        net_layout.addWidget(self.net_amt_label)

        amount_layout.addLayout(gross_layout)
        amount_layout.addLayout(discount_layout)
        amount_layout.addLayout(net_layout)

        return amount_layout
    
    def job_actions(self):
        actions_layout = QHBoxLayout()

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

        cancel_btn = QPushButton("Exit [Ctrl+X]")
        cancel_btn.setStyleSheet(buttons_style)
        cancel_btn.setCursor(Qt.PointingHandCursor)

        save_btn = QPushButton("Save [Ctrl+S]")
        save_btn.setStyleSheet(buttons_style)
        save_btn.setCursor(Qt.PointingHandCursor)

        invoice_btn = QPushButton("Invoice [Ctrl+I]")
        invoice_btn.setStyleSheet(buttons_style)
        invoice_btn.setCursor(Qt.PointingHandCursor)

        actions_layout.addWidget(cancel_btn)
        actions_layout.addWidget(save_btn)
        actions_layout.addWidget(invoice_btn)

        cancel_btn.clicked.connect(self.exit)
        save_btn.clicked.connect(self.save)
        invoice_btn.clicked.connect(self.invoice)

        return actions_layout
    
    # Computing the invoice amount
    def reinitialize_invoice_amount(self):
        gross_total = 0
        net_amount = 0
        for service in self.job_details["services"]:
            gross_total += float(service['rate'])
            net_amount += float(service['price'])

        self.job_details['gross_total'] = gross_total
        self.job_details['net_amount'] = net_amount
        self.job_details['discount'] = gross_total - net_amount
        discount_percent = 100 - ((net_amount/gross_total)*100)
        self.gross_amt_label.setText("₹{:.2f}".format(self.job_details["gross_total"]))
        self.discount_amt_label.setText("[{:.2f}%] ₹{:.2f}".format(discount_percent, self.job_details["discount"]))
        self.net_amt_label.setText("₹{:.2f}".format(self.job_details["net_amount"]))



