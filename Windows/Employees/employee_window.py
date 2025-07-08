import re
from PySide6.QtCore import Qt
from PySide6.QtGui import QStandardItemModel, QStandardItem, QShortcut, QKeySequence
from PySide6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QVBoxLayout, QTableView, QLineEdit, QLabel, QSizePolicy, QAbstractItemView, QHeaderView
from tinydb import TinyDB, Query
from .new_employee import NewEmployee


class Employee(QWidget):
    def __init__(self, file_path: str):
        super().__init__()
        self.setWindowTitle("Good Vibes - Employee")
        self.file_path = file_path
        self.db = None
        self.init_db()
        self.setWindowFlags(Qt.Window | Qt.CustomizeWindowHint | Qt.WindowTitleHint)
        self.init_shortcuts()
        self.init_widgets()

    def init_db(self):
        if self.db is not None:
            self.db.close()
        self.db = TinyDB(self.file_path + "/employee_db.json")

    def init_shortcuts(self):
        esc_shortcut = QShortcut(QKeySequence("Ctrl+X"), self)
        esc_shortcut.setContext(Qt.WindowShortcut)
        esc_shortcut.activated.connect(self.close)

        f1_shortcut = QShortcut(QKeySequence("Ctrl+N"), self)
        f1_shortcut.setContext(Qt.WindowShortcut)
        f1_shortcut.activated.connect(self.add_employee)

        f2_shortcut = QShortcut(QKeySequence("Ctrl+E"), self)
        f2_shortcut.setContext(Qt.WindowShortcut)
        f2_shortcut.activated.connect(self.update_employee)

        f4_shortcut = QShortcut(QKeySequence("Ctrl+S"), self)
        f4_shortcut.setContext(Qt.WindowShortcut)
        f4_shortcut.activated.connect(self.search_employee)

        f5_shortcut = QShortcut(QKeySequence("Ctrl+R"), self)
        f5_shortcut.setContext(Qt.WindowShortcut)
        f5_shortcut.activated.connect(self.clear_employees)

    def init_widgets(self):
        # main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # header layout
        main_layout.addWidget(self.init_header())

        # button layout
        main_layout.addWidget(self.init_menu())

        # table view
        self.employee_view = self.init_table_view()
        main_layout.addWidget(self.employee_view)

        self.setLayout(main_layout)
        self.load_db()

    def init_header(self):
        header_label = QLabel("""<b>Employee Unit</b>""", self)
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

    def init_search_bar(self):
        search_bar: QLineEdit = QLineEdit()
        search_bar.setPlaceholderText("Search Employees")
        search_bar.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                font-size: 16px;
                background-color: #FFFFFF;
                font-weight: bold;
                color: #7851a9;
                border: 1px solid #7851a9;
            }
        """)
        search_bar.setMaximumWidth(300)
        search_bar.returnPressed.connect(self.search_employee)
        return search_bar

    def init_menu(self):
        button_container = QWidget()
        button_container.setStyleSheet("background-color: #C0C0C0;")

        button_layout = QHBoxLayout(button_container)
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.setSpacing(0)

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

        search_button = QPushButton("Search [Ctrl+S]")
        search_button.setStyleSheet(buttons_style)
        search_button.setCursor(Qt.PointingHandCursor)

        clear_button = QPushButton("Reload [Ctrl+R]")
        clear_button.setStyleSheet(buttons_style)
        clear_button.setCursor(Qt.PointingHandCursor)

        add_button = QPushButton("New [Ctrl+N]")
        add_button.setStyleSheet(buttons_style)
        add_button.setCursor(Qt.PointingHandCursor)

        update_button = QPushButton("Update [Ctrl+E]")
        update_button.setStyleSheet(buttons_style)
        update_button.setCursor(Qt.PointingHandCursor)

        exit_button = QPushButton("Exit [Ctrl+X]")
        exit_button.setStyleSheet(buttons_style)
        exit_button.setCursor(Qt.PointingHandCursor)

        search_button.clicked.connect(self.search_employee)
        clear_button.clicked.connect(self.clear_employees)
        add_button.clicked.connect(self.add_employee)
        update_button.clicked.connect(self.update_employee)
        exit_button.clicked.connect(self.exit)

        self.search_bar = self.init_search_bar()
        button_layout.addWidget(self.search_bar)
        button_layout.addWidget(search_button)
        button_layout.addWidget(clear_button)
        button_layout.addWidget(add_button)
        button_layout.addWidget(update_button)
        button_layout.addWidget(exit_button)

        return button_container

    def init_table_view(self):
        table_view = QTableView()
        table_view.setStyleSheet("""
            QTableView {
                background-color: #ffffff;
                color: #7851a9;
                gridline-color: #7851a9;
                font-size: 14px;
            }
            QHeaderView::Section {
                background-color: #2c2c2c;
                font-weight: bold;
                color: #c0c0c0;
            }
        """)
        table_view.setEditTriggers(QTableView.NoEditTriggers)
        table_view.setSelectionBehavior(QAbstractItemView.SelectRows)
        table_view.setSelectionMode(QAbstractItemView.SingleSelection)
        table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table_view.verticalHeader().setVisible(False)
        return table_view

    def load_db(self, keyword: str = ""):
        headers = ["ID", "Name", "Phone"]
        records = []
        model: QStandardItemModel = QStandardItemModel()
        model.setHorizontalHeaderLabels(headers)
        employee: Query = Query()
        if keyword == "":
            records = self.db.all()
        else:
            records = self.db.search(
                employee.name.matches(f".*{keyword}.*", flags=re.IGNORECASE)
            )
        if records:
            header_key = list(records[0].keys())
            for items in records:
                item = [QStandardItem(str(items.get(col, ""))) for col in header_key]
                model.appendRow(item)
        else:
            model.setColumnCount(len(headers))
            model.appendRow([QStandardItem("No matching Employees found.")])
        self.employee_view.setModel(model)
        self.employee_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.employee_view.verticalHeader().setVisible(False)

    def exit(self):
        self.close()

    def search_employee(self):
        keyword = self.search_bar.text().strip()
        self.load_db(keyword)

    def add_employee(self):
        self.add_employee_window = NewEmployee(self.db)
        self.add_employee_window.shared_data.connect(self.execute_add_employee)
        self.add_employee_window.show()

    def execute_add_employee(self, response):
        if response:
            self.load_db()

    def update_employee(self):
        pass

    def clear_employees(self):
        self.search_bar.clear()
        self.init_db()
        self.search_employee()