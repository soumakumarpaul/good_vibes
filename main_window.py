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
        self.init_widgets()
        self.init_shortcuts()
        self.customer_window = None
        self.employee_window = None
        self.catalog_window = None
        self.job_window = None

    def init_shortcuts(self):
        job_shortcut = QShortcut(QKeySequence("Ctrl+N"), self)
        job_shortcut.setContext(Qt.WindowShortcut)
        job_shortcut.activated.connect(self.new_job)

        esc_shortcut = QShortcut(QKeySequence(Qt.Key_Escape), self)
        esc_shortcut.setContext(Qt.WindowShortcut)
        esc_shortcut.activated.connect(self.exit)

        customers_shortcut = QShortcut(QKeySequence(Qt.Key_F1), self)
        customers_shortcut.setContext(Qt.WindowShortcut)
        customers_shortcut.activated.connect(self.open_customers)

        catalog_shortcut = QShortcut(QKeySequence(Qt.Key_F2), self)
        catalog_shortcut.setContext(Qt.WindowShortcut)
        catalog_shortcut.activated.connect(self.open_catalog)

        employee_shortcut = QShortcut(QKeySequence(Qt.Key_F3), self)
        employee_shortcut.setContext(Qt.WindowShortcut)
        employee_shortcut.activated.connect(self.open_employee)

        settings_shortcut = QShortcut(QKeySequence(Qt.Key_F5), self)
        settings_shortcut.setContext(Qt.WindowShortcut)
        settings_shortcut.activated.connect(self.select_db)

    def init_widgets(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)
        header_label = QLabel("""
            Hello!!! <b>Good Vibes</b> - 
            The <span style='font-family: "Carattere"'>Feels</span> 
            Salon Application""", self)
        header_label.setTextFormat(Qt.RichText)
        header_label.setStyleSheet("""
            QLabel {
                background-color: #7851a9;
                color: #ffffff;
                font-size: 30px;
                padding: 20px;
                text-align: center;
                }
            """)
        header_label.setAlignment(Qt.AlignCenter)
        header_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        # get DB configuration
        self.settings_lbl: QLabel = self.get_db_conf()
        layout.addWidget(header_label)
        layout.addWidget(self.init_buttons())
        layout.addStretch(1)
        layout.addWidget(self.settings_lbl)
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
        self.job_button = QPushButton("Jobs [Ctrl+N]")
        self.job_button.setStyleSheet(buttons_style)
        self.job_button.setCursor(Qt.PointingHandCursor)
        self.job_button.clicked.connect(self.new_job)

        self.customers_button = QPushButton("Customers [F1]")
        self.customers_button.setStyleSheet(buttons_style)
        self.customers_button.setCursor(Qt.PointingHandCursor)
        self.customers_button.clicked.connect(self.open_customers)

        self.catalog_button = QPushButton("Services [F2]")
        self.catalog_button.setStyleSheet(buttons_style)
        self.catalog_button.setCursor(Qt.PointingHandCursor)
        self.catalog_button.clicked.connect(self.open_catalog)

        self.employees_button = QPushButton("Employees [F3]")
        self.employees_button.setStyleSheet(buttons_style)
        self.employees_button.setCursor(Qt.PointingHandCursor)
        self.employees_button.clicked.connect(self.open_employee)

        self.payments_button = QPushButton("Payments [F4]")
        self.payments_button.setStyleSheet(buttons_style)
        self.payments_button.setCursor(Qt.PointingHandCursor)

        self.settings_button = QPushButton("Settings [F5]")
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
            self.settings_lbl.setText("DB_Path: " + self.folder_path)

    def open_employee(self):
        if self.employee_window is None:
            self.employee_window = Employee(self.folder_path)
        self.employee_window.show()

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

        

        
