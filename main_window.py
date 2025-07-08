from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QSizePolicy, QPushButton, QGridLayout, QFileDialog, QHBoxLayout
from PySide6.QtCore import Qt
from PySide6.QtGui import QShortcut, QKeySequence
from Utilities.environments import Environment
from Windows.Customers.customer_window import Customers
from Windows.Employees.employee_window import Employee
from Windows.Catalog.catalog_window import CatalogWindow
from Windows.Jobs.jobs_window import Jobs

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.env = Environment()
        self.setWindowTitle("Good Vibes - The Feels Salon Application")
        self.showFullScreen()
        self.get_db_conf()
        self.init_widgets()
        self.init_shortcuts()
        self.customer_window = None
        self.employee_window = None
        self.catalog_window = None
        self.job_window = None

    def init_shortcuts(self):
        job_shortcut = QShortcut(QKeySequence(Qt.Key_F1), self)
        job_shortcut.setContext(Qt.ApplicationShortcut)
        job_shortcut.activated.connect(self.new_job)

        esc_shortcut = QShortcut(QKeySequence(Qt.Key_Escape), self)
        esc_shortcut.setContext(Qt.ApplicationShortcut)
        esc_shortcut.activated.connect(self.exit)

        customers_shortcut = QShortcut(QKeySequence(Qt.Key_F2), self)
        customers_shortcut.setContext(Qt.ApplicationShortcut)
        customers_shortcut.activated.connect(self.open_customers)

        catalog_shortcut = QShortcut(QKeySequence(Qt.Key_F3), self)
        catalog_shortcut.setContext(Qt.ApplicationShortcut)
        catalog_shortcut.activated.connect(self.open_catalog)

        employee_shortcut = QShortcut(QKeySequence(Qt.Key_F4), self)
        employee_shortcut.setContext(Qt.ApplicationShortcut)
        employee_shortcut.activated.connect(self.open_employee)

        settings_shortcut = QShortcut(QKeySequence(Qt.Key_F6), self)
        settings_shortcut.setContext(Qt.ApplicationShortcut)
        settings_shortcut.activated.connect(self.select_db)

    def init_widgets(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)

        # get DB configuration
        layout.addWidget(self.init_buttons())

        window_container = QWidget()
        self.window_layout = QVBoxLayout()
        self.window_layout.setContentsMargins(0, 0, 0, 0)
        self.window_layout.setSpacing(0)
        window_container.setLayout(self.window_layout)
        window_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        window_container.setMinimumHeight(1)
        layout.addWidget(window_container)
        layout.setStretch(0, 0)
        layout.setStretch(1, 1)
        self.setLayout(layout)

    def init_buttons(self):
        buttons_container = QWidget()
        buttons_container.setStyleSheet("background-color: #7851a9")
        layout = QHBoxLayout(buttons_container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        buttons_style = """
            QPushButton {
                font-size: 14px;
                font-weight: bold;
                color: "#FFFFFF";
                padding: 20px;
                background-color: #9c65e0;
                border:1px solid #FFFFFF;
            }
        """
        self.job_button = QPushButton("Jobs [F1]")
        self.job_button.setStyleSheet(buttons_style)
        self.job_button.setCursor(Qt.PointingHandCursor)
        self.job_button.clicked.connect(self.new_job)

        self.customers_button = QPushButton("Customers [F2]")
        self.customers_button.setStyleSheet(buttons_style)
        self.customers_button.setCursor(Qt.PointingHandCursor)
        self.customers_button.clicked.connect(self.open_customers)

        self.catalog_button = QPushButton("Services [F3]")
        self.catalog_button.setStyleSheet(buttons_style)
        self.catalog_button.setCursor(Qt.PointingHandCursor)
        self.catalog_button.clicked.connect(self.open_catalog)

        self.employees_button = QPushButton("Employees [F4]")
        self.employees_button.setStyleSheet(buttons_style)
        self.employees_button.setCursor(Qt.PointingHandCursor)
        self.employees_button.clicked.connect(self.open_employee)

        self.payments_button = QPushButton("Payments [F5]")
        self.payments_button.setStyleSheet(buttons_style)
        self.payments_button.setCursor(Qt.PointingHandCursor)

        self.settings_button = QPushButton("Settings [F6]")
        self.settings_button.setStyleSheet(buttons_style)
        self.settings_button.setCursor(Qt.PointingHandCursor)
        self.settings_button.clicked.connect(self.select_db)
        
        self.exit_button = QPushButton("Exit [Esc]")
        self.exit_button.setStyleSheet(buttons_style)
        self.exit_button.setCursor(Qt.PointingHandCursor)
        self.exit_button.clicked.connect(self.exit)

        layout.addWidget(self.job_button)
        layout.addWidget(self.customers_button)
        layout.addWidget(self.catalog_button)
        layout.addWidget(self.employees_button)
        layout.addWidget(self.payments_button)
        layout.addWidget(self.settings_button)
        layout.addWidget(self.exit_button)

        return buttons_container
            
    def select_db(self):
        self.folder_path = QFileDialog.getExistingDirectory(self, "Select Database Folder")
        if self.folder_path:
            self.env.set_db(self.folder_path)

    def open_employee(self):
        self.clear_layout()
        if self.employee_window is None:
            self.employee_window = Employee(self.folder_path)
        self.window_layout.addWidget(self.employee_window)

    def get_db_conf(self):
        db_path = self.env.get_db()
        self.folder_path = db_path
        settings_lbl = QLabel("DB_Path: " + db_path)
        settings_lbl.setStyleSheet("""
        QLabel {
            font-weight: bold;
            font-size: 14px;
            color: #FFFFFF;
            border: 1px solid #FFFFFF;
            padding: 10px;
            margin: 15px;
        }
        """)
        return settings_lbl
    
    def open_customers(self):
        if self.customer_window is None:
            self.customer_window = Customers(self.folder_path)
        self.customer_window.show()

    def open_catalog(self):
        if self.catalog_window is None:
            self.catalog_window = CatalogWindow(self.folder_path)
        self.catalog_window.show()

    def exit(self):
        self.close()

    def new_job(self):
        if self.job_window is None:
            self.job_window = Jobs(self.folder_path)
        self.job_window.show()

    def clear_layout(self):
        if self.window_layout.count():
            item = self.window_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)

        

        
