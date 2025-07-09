from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QTableView, QHeaderView, QLineEdit, QLabel, QSizePolicy, QVBoxLayout, QHBoxLayout
from PySide6.QtGui import QStandardItemModel, QStandardItem, QKeySequence, QShortcut
from PySide6.QtCore import Qt
from tinydb import TinyDB, Query
from PySide6.QtWidgets import QAbstractItemView
from .new_customer import NewCustomer
import re

class Customers(QWidget):
    def __init__(self, file_path: str):
        super().__init__()
        self.file_path = file_path
        self.db = None
        self.init_db()
        self.setWindowFlags(Qt.Window | Qt.CustomizeWindowHint | Qt.WindowTitleHint)
        self.init_widgets()
        self.init_shortcuts()

    def init_db(self):
        if self.db is not None:
            self.db.close()
        self.db = TinyDB(self.file_path + "/customers_db.json")

    def init_shortcuts(self):
        esc_shortcut = QShortcut(QKeySequence("Ctrl+X"), self)
        esc_shortcut.setContext(Qt.WindowShortcut)
        esc_shortcut.activated.connect(self.exit_customers)

        new_shortcut = QShortcut(QKeySequence("Ctrl+N"), self)
        new_shortcut.setContext(Qt.WindowShortcut)
        new_shortcut.activated.connect(self.add_customer)

        search_shortcut = QShortcut(QKeySequence("Ctrl+S"), self)
        search_shortcut.setContext(Qt.WindowShortcut)
        search_shortcut.activated.connect(self.search_customers)

        reload_shortcut = QShortcut(QKeySequence("Ctrl+R"), self)
        reload_shortcut.setContext(Qt.WindowShortcut)
        reload_shortcut.activated.connect(self.clear_customers)
    
    def init_widgets(self):
        self.table_view = QTableView()
        self.table_view.setStyleSheet("""
            QTableView {
                background-color: #ffffff;
                color: #7851a9;
                gridline-color: #7851a9;
                font-size: 14px;
            }
            QHeaderView::Section {
                background-color: #7851a9;
                font-weight: bold;
                color: #c0c0c0;
                border: 1px solid #FFFFFF;
            }
        """)
        self.table_view.setEditTriggers(QTableView.NoEditTriggers)
        self.table_view.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_view.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_view.verticalHeader().setVisible(False)

        #Buttons
        buttons_container = QWidget()
        buttons_container.setStyleSheet("background-color: #C0C0C0;")
        buttons_style = """
            QPushButton {
                font-size: 16px;
                color: #FFFFFF;
                padding: 10px;
                background-color: #9c65e0;
                font-weight: bold;
                border: 1px solid #FFFFFF;
            }
        """
        self.search_button = QPushButton("Search[Ctrl+S]")
        self.search_button.setStyleSheet(buttons_style)
        self.search_button.setCursor(Qt.PointingHandCursor)
        self.clear_button = QPushButton("Reload[Ctrl+R]]")
        self.clear_button.setStyleSheet(buttons_style)
        self.clear_button.setCursor(Qt.PointingHandCursor)
        self.add_button = QPushButton("New[Ctrl+N]")
        self.add_button.setStyleSheet(buttons_style)
        self.add_button.setCursor(Qt.PointingHandCursor)
        self.update_button = QPushButton("Update[Ctrl+E]")
        self.update_button.setStyleSheet(buttons_style)
        self.update_button.setCursor(Qt.PointingHandCursor)
        self.exit_button = QPushButton("Exit[Ctrl+X]")
        self.exit_button.setStyleSheet(buttons_style)
        self.exit_button.setCursor(Qt.PointingHandCursor)

        self.add_button.clicked.connect(self.add_customer)
        self.exit_button.clicked.connect(self.exit_customers)
        self.search_button.clicked.connect(self.search_customers)
        self.clear_button.clicked.connect(self.clear_customers)

        #Header label
        header_label = QLabel("""<b>Customer's Unit</b>""", self)
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

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        buttons_layout = QHBoxLayout(buttons_container)
        buttons_layout.setContentsMargins(0,0,0,0)
        buttons_layout.setSpacing(0)

        search_bar = QLineEdit()
        search_bar.setPlaceholderText("Search Customers")
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
        search_bar.setMaximumWidth(300)
        search_bar.returnPressed.connect(self.search_customers)
        self.search_field = search_bar

        buttons_layout.addWidget(search_bar)
        buttons_layout.addWidget(self.search_button)
        buttons_layout.addWidget(self.clear_button)
        buttons_layout.addWidget(self.add_button)
        buttons_layout.addWidget(self.update_button)
        buttons_layout.addWidget(self.exit_button)

        main_layout.addWidget(header_label)

        main_layout.addWidget(buttons_container)
        main_layout.addWidget(self.table_view)

        self.setLayout(main_layout)
        self.load_db()
        self.search_field.setFocus()

    def load_db(self, keyword: str = ""):
        headers = ["ID", "Name", "Phone", "Gender", "Registered On", "Timestamp"]
        records = []
        customer: Query = Query()
        if keyword == "":       
            records = self.db.all()
        else:
            records = self.db.search(
                (customer.name.matches(f".*{keyword}.*", flags=re.IGNORECASE)) |
                (customer.mobile.matches(f".*{keyword}.*", flags=re.IGNORECASE))
                )
        records = sorted(records, key=lambda x: x.get("timestamp", 0), reverse=True)
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(headers)
        if records:
            header_key = list(records[0].keys())
            for row_data in records:
                items = [QStandardItem(str(row_data.get(col, ""))) for col in header_key]
                model.appendRow(items)
        else:
            model.setColumnCount(len(headers))
            model.appendRow([QStandardItem("No Matching Records Found")])
            if re.match(r"^[6-9]\d{9}$", keyword):
                self.add_customer()
        self.table_view.setModel(model)
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_view.verticalHeader().setVisible(False)

    def search_customers(self):
        self.search_field.setFocus()
        keyword = self.search_field.text().strip()
        self.load_db(keyword)

    def clear_customers(self):
        self.search_field.clear()
        self.init_db()
        self.search_customers()

    def exit_customers(self):
        self.close()

    def add_customer(self):
        self.new_customer_window = NewCustomer(self.search_field.text().strip())
        self.new_customer_window.shared_data.connect(self.execute_new_customer)
        self.new_customer_window.show()

    def execute_new_customer(self, response):
        if response:
            self.load_db()

    def update_customer(self):
        pass

