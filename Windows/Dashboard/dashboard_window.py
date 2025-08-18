from PySide6.QtWidgets import (QWidget, QPushButton, 
                               QVBoxLayout, QListWidget, QListWidgetItem,
                               QHBoxLayout, QGridLayout, QLabel, QSizePolicy)
from PySide6.QtCore import Qt, Signal
from tinydb import TinyDB, Query
from datetime import date
from .accounts_list_item import AccountsItemWidget

class Dashboard(QWidget):
    dashboard_response = Signal(object)
    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path
        self.job_details = self.init_jobs()
        self.revenue = 0
        self.init_widgets()

    def init_jobs(self):
        db = TinyDB(self.file_path + "/jobs_db.json")
        Jobs = Query()
        result = db.search((Jobs.date == date.today().isoformat()))
        db.close()
        return result

    def init_widgets(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        main_layout.addWidget(self.init_header())

        dashboard_layout = QHBoxLayout()

        #Add Jobs Layout
        dashboard_layout.addWidget(self.init_jobs_layout(), alignment=Qt.AlignTop, stretch=1)
        main_layout.addLayout(dashboard_layout)
        self.setLayout(main_layout)

    def init_header(self):
        header_label = QLabel("""<b>Dashboard</b>""", self)
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

    def init_jobs_layout(self):
        jobs_container = QWidget()
        jobs_container.setMinimumWidth(400)
        jobs_layout = QVBoxLayout(jobs_container)
        jobs_layout.setSpacing(0)
        jobs_layout.setContentsMargins(0, 0, 0, 0)

        btn_style = """
            QPushButton {
                background-color: #C0C0C0;
                font-size: 18px;
                font-weight: bold;
                color: #7851a9;
                border: 5px solid #FFFFFF;
                padding: 10px;
            }
            QPushButton:hover {
                color: #FFFFFF;
                background-color: #7851a9;
                border: 5px solid #C0C0C0;
            }
        """
        new_job = QPushButton("[+] New Job [Ctrl+N]")
        new_job.setCursor(Qt.PointingHandCursor)
        new_job.setStyleSheet(btn_style)
        new_job.clicked.connect(lambda checked = False, details=None: self.initiate_job(details))
        jobs_layout.addWidget(new_job)
        jobs_layout.addWidget(self.list_jobs(), 1)
        
        return jobs_container
    
    def list_jobs(self):
        self.job_list = QListWidget()
        self.job_list.setStyleSheet("""
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
        for job in self.job_details:
            self.add_jobs_to_list(job)
        self.job_list.itemClicked.connect(self.initiate_job)
        return self.job_list

    def add_jobs_to_list(self, job):
        item = QListWidgetItem()
        widget = AccountsItemWidget(job_details=job)
        widget.adjustSize()
        item.setSizeHint(widget.sizeHint())
        self.job_list.addItem(item)
        self.job_list.setItemWidget(item, widget)

    def initiate_job(self, item = None):
        job = self.job_list.itemWidget(item).job if item else None
        if job:
            if job['isComplete'] == True:
                return
        self.dashboard_response.emit(job)
        self.close()