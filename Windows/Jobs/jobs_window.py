from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QGridLayout, QListView, QLineEdit, QLabel, QSizePolicy, QVBoxLayout, QHBoxLayout, QTableView, QHeaderView
from PySide6.QtGui import QStandardItemModel, QStandardItem, QKeySequence, QShortcut
from PySide6.QtCore import Qt
from tinydb import TinyDB, Query
from PySide6.QtWidgets import QAbstractItemView
import re
from functools import partial
from Windows.Customers.new_customer import NewCustomer

class Jobs(QWidget):
    def __init__(self, file_path: str):
        super().__init__()
        self.file_path = file_path
        self.catalog = []
        self.customer_info = {}
        self.service_results = []
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
        self.close()

    def save(self):
        pass

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
                print("Heelo")
                self.add_customer = NewCustomer(db, phone_number)
                self.add_customer.shared_data.connect(self.get_new_customer)
                self.add_customer.exec()
            else:
                self.customer_info = results[0]
            db.close()
            self.customer_name_field.setText(self.customer_info["name"])
            membership_details = self.customer_info.get("membership", {})
            self.membership_points.setText(f"Points: {membership_details.get("points", 0)}")

    def get_new_customer(self, data):
        self.customer_name_field.setText(data.get("Name"))
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

        services_layout.addWidget(search_bar)
        services_layout.addWidget(self.services_list)

        return services_layout

    def search_services(self, search_keyword: str = ""):
        model: QStandardItemModel = QStandardItemModel()
        keyword = search_keyword.strip().lower().split()
        items = [item for item in self.service_results
                 if all(word in item.get("name", "").lower() for word in keyword)]
        for item in items:
            service_item = QStandardItem(item["name"])
            service_item.setToolTip(item["name"])
            service_item.setData(item, Qt.UserRole)
            model.appendRow(service_item)
        self.services_list.setModel(model)

    def init_invoice_layout(self):
        invoice_layout = QVBoxLayout()
        invoice_layout.setContentsMargins(0, 0, 0, 0)
        invoice_layout.setSpacing(0)

        invoice_layout.addWidget(self.init_customer())
        invoice_layout.addWidget(self.invoice_view())

        return invoice_layout
    
    def invoice_view(self):
        invoice_table = QTableView()
        invoice_table.setStyleSheet("""
            QTableView {
                background-color: #ffffff;
                color: #7851a9;
                gridline-color: #7851a9;
                font-size: 20px;
            }
            QHeaderView::Section {
                background-color: #2c2c2c;
                font-weight: bold;
                color: #c0c0c0;
            }
            QTableView::item:selected {
                background-color: #7851a9;
                color: #FFFFFF;
                border-color: #C0C0C0;
            }
        """)
        invoice_table.setEditTriggers(QTableView.NoEditTriggers)
        invoice_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        invoice_table.setSelectionMode(QAbstractItemView.SingleSelection)
        invoice_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        invoice_table.verticalHeader().setVisible(False)
        return invoice_table


