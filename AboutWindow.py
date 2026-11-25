from PySide6.QtWidgets import QWidget, QLabel, QPushButton
from PySide6.QtGui import QPixmap


class AboutWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        self.setWindowTitle("About")
        self.setGeometry(200, 200, 420, 360)
        self.setStyleSheet("background-color: whitesmoke;")

        self.title_label = QLabel("Heat Transfer Simulation", self)
        self.title_label.setGeometry(60, 20, 300, 35)
        self.title_label.setStyleSheet("font-size: 20px; font-weight: bold; color: navy;")

        self.image_label = QLabel(self)
        self.image_label.setGeometry(85, 65, 250, 140)
        self.image_label.setScaledContents(True)
        pixmap = QPixmap("about_image.png")
        self.image_label.setPixmap(pixmap)

        self.desc_label = QLabel("Physics simulation of heat conduction between two bodies.", self)
        self.desc_label.setGeometry(40, 220, 340, 30)
        self.desc_label.setStyleSheet("font-size: 13px; color: black;")

        self.link_label = QLabel(
            '<a href="https://github.com/sharabi-stud/HeatTransfer">Project GitHub Repository</a>',
            self
        )
        self.link_label.setGeometry(120, 255, 200, 30)
        self.link_label.setOpenExternalLinks(True)
        self.link_label.setStyleSheet("font-size: 14px;")

        self.close_button = QPushButton("Close", self)
        self.close_button.setGeometry(160, 300, 100, 35)
        self.close_button.setStyleSheet("background-color: steelblue; color: white; font-weight: bold;")
        self.close_button.clicked.connect(self.close)