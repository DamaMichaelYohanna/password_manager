from PySide6 import QtCore
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QPushButton, QLabel, \
    QLineEdit, QFrame, QVBoxLayout, QProgressBar

from backend.password_utility import PasswordManager
from draw_line import QHSeparationLine, QVSeparationLine
from frontend.password import NewOrUpdatePassword


class PasswordTester(QFrame):
    def __init__(self):
        super(PasswordTester, self).__init__()
        self.password_util: PasswordManager = PasswordManager()

        self.setStyleSheet("QFrame{background:white;}")
        self.main_layout = QVBoxLayout()
        image_label = QLabel()
        image = QPixmap("../images/pass_test.png")
        image_label.setPixmap(image)
        image_label.setAlignment(QtCore.Qt.AlignCenter)
        descr = QLabel("You doubt the strength of your Password? Let's help you check.")
        descr.setWordWrap(True)
        descr.setStyleSheet("QLabel{font-size:18px; color:white;"
                            "background:rgba(41, 128, 140,1);padding:10px;}"
                            "font-weight:bold;")
        extra_heading = QLabel("Below are point to note regard password strength")
        extra_heading.setStyleSheet("QLabel{font-size:16px}")

        extra_info = QLabel(
                            "1. Password should be made up of mixed letter, upper and lower\n"
                            "2. Password should contain at least a digit\n"
                            "3. Password should also contain at least a special Character\n"
                            "4. Password length should be at least eight(8) character")
        extra_info.setStyleSheet("QLabel{padding:5px;font-size:16px;}")

        self.main_layout.addWidget(descr)
        self.main_layout.addWidget(extra_heading)
        self.main_layout.addWidget(QHSeparationLine())
        self.main_layout.addWidget(extra_info)
        self.main_layout.addWidget(image_label)

        self.password_label = QLineEdit()
        self.password_label.setPlaceholderText("Type Your Password Here")
        self.password_label.setAlignment(QtCore.Qt.AlignCenter)
        self.password_label.textChanged.connect(self.keystroke_callback)
        self.password_label.setStyleSheet("QLineEdit{font-size:18px;"
                                          "padding:5px;color:rgba(41, 128, 140,1);"
                                          "border:none;}")

        self.progress = QProgressBar(self)
        self.progress.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.progress.setMinimum(0)
        self.progress.setMaximum(10)

        self.main_layout.addStretch()
        self.main_layout.addWidget(self.password_label)
        self.main_layout.addWidget(QHSeparationLine())
        self.main_layout.addWidget(self.progress)
        self.main_layout.addStretch()
        self.main_layout.setAlignment(QtCore.Qt.AlignCenter)

        self.setLayout(self.main_layout)

    def keystroke_callback(self):
        password = self.password_label.text()
        strength = self.password_util.password_strength_check(password)
        self.progress.setValue(strength)
        print(strength)
        if strength <= 2:
            self.progress.setStyleSheet(
                "QProgressBar::chunk {"
                "background-color: red;}")
            self.progress.setFormat("Poor Password")
        elif 3 <= strength <= 5:
            self.progress.setStyleSheet(
                "QProgressBar::chunk {"
                "background-color: orange;}")
            self.progress.setFormat("Fair Password")

        elif 6 <= strength <= 7:
            self.progress.setStyleSheet(
                "QProgressBar::chunk {"
                "background-color: lime;}")
            self.progress.setFormat("Medium Password")

        elif 8 <= strength <= 10:
            self.progress.setStyleSheet(
                "QProgressBar::chunk {background:rgba(41, 128, 140,1);padding:10px;color:white;}")
            self.progress.setFormat("Strong Password")
