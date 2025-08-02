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
        self.expenses = self.init_expenses()
        self.init_widgets()

    def init_jobs(self):
        db = TinyDB(self.file_path + "/jobs_db.json")
        Jobs = Query()
        result = db.search((Jobs.isComplete == False) & (Jobs.date == date.today().isoformat()))
        db.close()
        return result

    def init_expenses(self):
        db = TinyDB(self.file_path + "/accounts_db.json")
        Accounts = Query()
        today = date.today()
        first_day = today.replace(day=1).isoformat()
        today = today.isoformat()
        results = db.search((Accounts.date >= first_day) & (Accounts.date <= today))
        db.close()
        return results

    def init_widgets(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        main_layout.addWidget(self.init_header())

        dashboard_layout = QHBoxLayout()

        #Add Jobs Layout
        dashboard_layout.addWidget(self.init_jobs_layout(), alignment=Qt.AlignTop)
        #Add Expense Layout
        dashboard_layout.addLayout(self.init_accounts())
        dashboard_layout.setStretch(0, 1)
        dashboard_layout.setStretch(1, 1)
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
            background-color: #7851a9;
            font-size: 22px;
            font-weight: bold;
            color: #FFFFFF;
            border: 1px solid #C0C0C0;
            padding: 10px;
        """
        new_job = QPushButton("[+] New Job")
        new_job.setCursor(Qt.PointingHandCursor)
        new_job.setStyleSheet(btn_style)
        new_job.clicked.connect(lambda checked = False, details=None: self.initate_job(details))
        jobs_layout.addWidget(new_job)
        for index, job in enumerate(self.job_details):
            row = (index + 1) // 2
            col = (index + 1) % 2
            btn_text = job['_id']

            btn = QPushButton(btn_text)
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

    def init_accounts(self):
        expense_layout = QVBoxLayout()
        expense_layout.setContentsMargins(0, 0, 0, 0)
        expense_layout.setSpacing(0)
        self.accounts_list = QListWidget()
        self.accounts_list.setStyleSheet("""
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

        for expense in self.expenses:
            if expense['type'] == 'debit':
                self.revenue -= float(expense['amount'])
            else:
                self.revenue += float(expense['amount'])
            self.add_amount_to_account(expense)
        expense_layout.addWidget(self.accounts_list)

        revenue_styles = """
            QLabel {
                color: #FFFFFF;
                font-size: 30px;
                padding: 5px;
                margin: 5px;
                border: 1px solid #FFFFFF;
                font-weight: bold;
            }
        """
        revenue_layout = QHBoxLayout()
        lbl_revenue = QLabel("Total Revenue")
        lbl_revenue.setStyleSheet(revenue_styles)
        revenue_lbl = QLabel("{:.2f}".format(float(self.revenue)))
        revenue_lbl.setStyleSheet(revenue_styles)
        revenue_lbl.setAlignment(Qt.AlignRight)
        revenue_layout.addWidget(lbl_revenue)
        revenue_layout.addWidget(revenue_lbl)

        expense_layout.addLayout(revenue_layout)
        return expense_layout

    def add_amount_to_account(self, expense):
        item = QListWidgetItem()
        widget = AccountsItemWidget(expense)
        widget.adjustSize()
        item.setSizeHint(widget.sizeHint())
        self.accounts_list.addItem(item)
        self.accounts_list.setItemWidget(item, widget)


