from PySide6.QtWidgets import QVBoxLayout, QWidget, QLabel, QHBoxLayout, QPushButton
from PySide6.QtCore import Qt

class AccountsItemWidget(QWidget):

    def __init__(self, job_details):
        super().__init__()
        self.job = job_details
        self.setMouseTracking(True)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5,5,5,5)
        layout.setSpacing(0)
        layout.addWidget(self.init_header())

    def init_header(self):
        header_container = QWidget()
        header_container.setContentsMargins(0, 0, 0, 0)
        layout = QHBoxLayout(header_container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        completed_lbl_style = """
            QLabel {
                font-size: 24px;
                font-weight: bold;
                color: #FF0800;
            }
        """

        progress_lbl_style = """
            QLabel {
                font-size: 24px;
                font-weight: bold;
                color: #2E6f40;
            }
        """

        lbl_style = """
            QLabel {
                font-size: 24px;
                font-weight: bold;
                color: #7851a9;
            }
        """
        customer = f"{self.job['customer'].get('name', "")} - {self.job['customer'].get('phone', "")}"
        job_txt = QLabel(self.job.get("_id", ""))
        job_txt.setStyleSheet(lbl_style)
        customer_txt = QLabel(customer)
        customer_txt.setStyleSheet(lbl_style)
        status = "In Progress" if self.job['isComplete'] == False else "Completed"
        status_txt = QLabel(status)
        if status == 'Completed':
            status_txt.setStyleSheet(completed_lbl_style)
        else:
            status_txt.setStyleSheet(progress_lbl_style)
        layout.addWidget(job_txt)
        layout.addWidget(customer_txt)
        layout.addWidget(status_txt)

        return header_container