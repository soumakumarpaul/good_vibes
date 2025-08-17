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
        dashboard_layout.addWidget(self.init_jobs_layout(), alignment=Qt.AlignTop)
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
        jobs_layout = QGridLayout(jobs_container)
        jobs_layout.setSpacing(0)
        jobs_layout.setContentsMargins(0, 0, 0, 0)

        btn_style = """
            QPushButton {
                background-color: #FFFFFF;
                font-size: 18px;
                font-weight: bold;
                color: #7851a9;
                border: 1px solid #C0C0C0;
                padding: 10px;
                margin: 10px;
            }
            QPushButton:hover {
                color: #FFFFFF;
                background-color: #7851a9;
                border: 1px solid #C0C0C0;
            }
        """

        disabled_btn = """
            QPushButton {
                background-color: #C0C0C0;
                font-size: 18px;
                font-weight: bold;
                color: #2c2c2c;
                border: 1px solid #FFFFFF;
                padding: 10px;
                margin: 10px;
            }   
        """
        new_job = QPushButton("[+] New Job")
        new_job.setCursor(Qt.PointingHandCursor)
        new_job.setMaximumWidth(350)
        new_job.setStyleSheet(btn_style)
        new_job.clicked.connect(lambda checked = False, details=None: self.initate_job(details))
        jobs_layout.addWidget(new_job)
        for index, job in enumerate(self.job_details):
            row = (index + 1) // 3
            col = (index + 1) % 3
            btn_text = job['_id'] if not job['customer'] else f"{job['customer'].get('name', '')}"

            btn = QPushButton(btn_text)
            btn.setMaximumWidth(350)
            if job['isComplete'] == True:
                btn.setEnabled(False)
            if job.get('customer'):
                btn.setToolTip(f"{job['customer'].get('name', '')} - {job['customer'].get('phone', '')}")
            btn.setStyleSheet(btn_style)
            btn.setCursor(Qt.PointingHandCursor)
            btn.clicked.connect(lambda checked = False, details=job: self.initate_job(details))
            jobs_layout.addWidget(btn, row, col)
        
        return jobs_container
    
    def initate_job(self, job_details = None):
        self.dashboard_response.emit(job_details)
        self.close()