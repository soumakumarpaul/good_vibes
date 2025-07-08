from PySide6.QtWidgets import (QWidget, QLabel, QSizePolicy, QVBoxLayout, 
                            QPushButton, QHBoxLayout, QGridLayout, QTableView,
                            QAbstractItemView, QHeaderView, QLineEdit)
from PySide6.QtCore import Qt
from PySide6.QtGui import QKeySequence, QShortcut, QStandardItemModel, QStandardItem
from tinydb import TinyDB
from functools import partial

class CatalogWindow(QWidget):

    def __init__(self, file_path: str):
        super().__init__()
        self.file_path = file_path
        self.db = None
        self.records = []
        self.search_results = []
        self.init_db()
        self.load_db()
        self.setWindowFlags(Qt.Window | Qt.CustomizeWindowHint | Qt.WindowTitleHint)
        self.init_shortcuts()
        self.init_widgets()

    def init_db(self):
        if self.db is not None:
            self.db.close()
        self.db = TinyDB(self.file_path + "/catalog_db.json")

    def init_shortcuts(self):
        f4_shortcut = QShortcut(QKeySequence("Ctrl+S"), self)
        f5_shortcut = QShortcut(QKeySequence("Ctrl+R"), self)
        f1_shortcut = QShortcut(QKeySequence("Ctrl+N"), self)
        f2_shortcut = QShortcut(QKeySequence("Ctrl+E"), self)
        esc_shortcut = QShortcut(QKeySequence("Ctrl+X"), self)

        f4_shortcut.setContext(Qt.WindowShortcut)
        f4_shortcut.activated.connect(self.search_catalog)
        
        f5_shortcut.setContext(Qt.WindowShortcut)
        f5_shortcut.activated.connect(self.clear_catalog)
        
        f1_shortcut.setContext(Qt.WindowShortcut)
        f1_shortcut.activated.connect(self.add_service)

        f2_shortcut.setContext(Qt.WindowShortcut)
        f2_shortcut.activated.connect(self.update_service)

        esc_shortcut.setContext(Qt.WindowShortcut)
        esc_shortcut.activated.connect(self.exit_catalog)

    def init_widgets(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        #initialize Header
        main_layout.addWidget(self.init_header())

        self.scroll_style = """
            QScrollArea {
                border: 2px solid #C0C0C0;
                border-radius: 6px;
                margin: 10px;
            }
            QScrollBar:vertical, QScrollBar:horizontal {
                width: 0px;
                height: 0px;
            }
        """

        # initialize Dashboard
        dashboard_layout = QHBoxLayout()
        dashboard_layout.setContentsMargins(0,0,0,0)
        dashboard_layout.setSpacing(0)
        dashboard_layout.addLayout(self.init_service_catalog())

        #initialize sub category layout
        sub_cat_container = QWidget()
        sub_cat_container.setFixedWidth(300)
        self.sub_cat_layout = QGridLayout(sub_cat_container)
        self.sub_cat_layout.setContentsMargins(0, 0, 0, 0)
        self.sub_cat_layout.setSpacing(0)

        dashboard_layout.addWidget(sub_cat_container)

        dashboard_layout.addLayout(self.init_services())

        main_layout.addLayout(dashboard_layout)
        self.setLayout(main_layout)
        
    def init_header(self):
        header_label = QLabel("""<b>Catalog Unit</b>""", self)
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

    def init_service_catalog(self):
        catalog_layout = QHBoxLayout()
        catalog_layout.addWidget(self.init_service_category())
        catalog_layout.setContentsMargins(0, 0, 0, 0)
        catalog_layout.setSpacing(0)
        
        return catalog_layout

    def init_service_category(self):
        category_container = QWidget()
        category_layout = QVBoxLayout(category_container)
        category_layout.setContentsMargins(0, 0, 0, 0)
        category_layout.setSpacing(0)

        button_styles = """
            QPushButton{
            font-size: 20px;
            font-weight: bold;
            color: #FFFFFF;
            background-color: #2c2c2c;
            border: 1px solid #FFFFFF;
            padding: 10px;
            }
        """
        for category in self.records:
            category_name = category.get("category", "").replace(" ", "\n")
            button = QPushButton(category_name)
            
            button.setStyleSheet(button_styles)
            button.clicked.connect(partial(self.on_category_selected, category.get("catalog", [])))
            button.setFixedWidth(150)
            button.setCursor(Qt.PointingHandCursor)
            button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
            category_layout.addWidget(button, stretch=1)
        return category_container

    def on_category_selected(self, catalog = []):
        self.init_sub_category(catalog)

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
            button.clicked.connect(partial(self.on_service_selected, category.get("services")))
            button.setFixedWidth(150)
            button.setCursor(Qt.PointingHandCursor)
            button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
            row = index // 2
            col = index % 2
            self.sub_cat_layout.addWidget(button, row, col)

    def clear_sub_layout(self):
        while self.sub_cat_layout.count():
            item = self.sub_cat_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)
        
    def init_services(self):
        table_layout = QVBoxLayout()
        table_layout.setContentsMargins(0, 0, 0, 0)
        table_layout.setSpacing(0)

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
        search_bar.textEdited.connect(self.search_catalog)

        table_view = QTableView()
        table_view.setStyleSheet("""
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

        table_view.setEditTriggers(QTableView.NoEditTriggers)
        table_view.setSelectionBehavior(QAbstractItemView.SelectRows)
        table_view.setSelectionMode(QAbstractItemView.SingleSelection)
        table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table_view.verticalHeader().setVisible(False)
        self.catalog_view = table_view
        table_layout.addWidget(search_bar)
        table_layout.addWidget(table_view)
        self.search_catalog()
        return table_layout

    def load_db(self):
        self.records = self.db.all()
        self.db.close()

    def on_service_selected(self, services = []):
        self.search_results = services
        self.search_catalog()

    def search_catalog(self, search_keyword = ""):
        headers = [ "Item", "Price"]
        keyword = search_keyword.strip().lower().split()
        items = [item for item in self.search_results
                 if all(word in item.get("name", "").lower() for word in keyword)]
        model: QStandardItemModel = QStandardItemModel()
        model.setHorizontalHeaderLabels(headers)
        if len(items) == 0:
            txt = QStandardItem(str(""))
            model.appendRow([txt, txt])
        else:
            for item in items:
                name = QStandardItem(str(item.get("name", "")))
                price = QStandardItem("₹" + str(item.get("price", "")))
                price.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)

                model.appendRow([name, price])
        self.catalog_view.setModel(model)
        self.catalog_view.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.catalog_view.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.catalog_view.verticalHeader().setVisible(False)

    def clear_catalog(self):
        pass

    def add_service(self):
        pass

    def update_service(self):
        pass

    def exit_catalog(self):
        self.close()