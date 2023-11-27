import pyperclip
from PySide6 import QtCore
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtWidgets import QPushButton, QLabel, \
    QLineEdit, QFrame, QVBoxLayout, QHBoxLayout, QMessageBox

from backend import password_utility
from draw_line import QHSeparationLine
from frontend.password import NewOrUpdatePassword


class PasswordGenerator(QFrame):
    def __init__(self, database_util, user):
        super(PasswordGenerator, self).__init__()
        self.generator_object = password_utility.PasswordManager()
        self.database_util = database_util
        self.user = user
        self.generated_password = None

        self.setStyleSheet("QFrame{background:white;}")
        self.main_layout = QVBoxLayout()
        image_label = QLabel()
        image = QPixmap("../images/pass_gen.png")
        image_label.setPixmap(image)
        image_label.setAlignment(QtCore.Qt.AlignCenter)
        descr = QLabel("Password Are Generated to Meet Industry standard.")
        descr.setWordWrap(True)
        descr.setStyleSheet("QLabel{font-size:18px; color:white;"
                            "background:rgba(41, 128, 140,1);padding:10px;}"
                            "font-weight:bold;")

        self.main_layout.addWidget(descr)
        self.main_layout.addWidget(image_label)

        self.password_label = QLineEdit()
        self.password_label.setPlaceholderText("Your Password will Appear here")
        self.password_label.setAlignment(QtCore.Qt.AlignCenter)
        self.password_label.setStyleSheet("QLineEdit{font-size:18px;"
                                          "padding:5px;color:rgba(41, 128, 140,1);"
                                          "border:none;}")
        copy_btn = QPushButton()
        copy_icon = QIcon("../images/copy.png")
        copy_btn.setIcon(copy_icon)
        copy_btn.setToolTip("Copy Password")
        copy_btn.clicked.connect(self.copy_btn_callback)
        # create layout for password area and copy button
        password_label_frame = QHBoxLayout()
        password_label_frame.addWidget(self.password_label)
        password_label_frame.addWidget(copy_btn)

        action_btn_frame = QHBoxLayout() # create layout for generate and save btn
        self.generate_btn = QPushButton("Generate Password")
        self.generate_btn.setStyleSheet("padding:8px;border-radius:3px;"
                                        "background:white;font-weight:bold;"
                                        "border:1px solid rgba(41, 128, 140,1);"
                                        "color:rgb(41, 128, 140)"
                                        )
        self.generate_btn.clicked.connect(self.generate_btn_callback)

        self.save_btn = QPushButton("Save Password")
        self.save_btn.setStyleSheet("padding:8px;border-radius:3px;"
                                    "background:white;font-weight:bold;"
                                    "border:1px solid rgba(41, 128, 140,1);"
                                    "color:rgb(41, 128, 140)"
                                    )
        self.save_btn.setDisabled(True)
        self.save_btn.clicked.connect(self.save_btn_callback)

        action_btn_frame.addWidget(self.generate_btn)
        action_btn_frame.addWidget(self.save_btn)
        # refresh_btn = QPushButton("Refresh")
        # refresh_btn.setStyleSheet("padding:8px;border-radius:3px;"
        #                           "background:white;color:rgba(41, 128, 140,1);"
        #                           "font-weight:bold;border:1px solid rgba(41, 128, 140,1);")

        self.main_layout.addStretch()
        self.main_layout.addLayout(password_label_frame)
        self.main_layout.addWidget(QHSeparationLine())
        self.main_layout.addLayout(action_btn_frame)
        self.main_layout.addStretch()
        self.main_layout.setAlignment(QtCore.Qt.AlignCenter)

        self.setLayout(self.main_layout)

    def generate_btn_callback(self):
        self.generated_password = self.generator_object.return_generated_password()
        self.password_label.setText(self.generated_password)
        self.save_btn.setDisabled(False)

    def save_btn_callback(self):
        if self.generated_password:
            app = NewOrUpdatePassword(self, self.database_util, self.user, password=self.generated_password)
            app.open()
            self.password_label.setText("")
            self.generated_password = None
        else:
            QMessageBox.information(self,"Information", "No password generated")

    def copy_btn_callback(self):
        if self.generated_password:
            pyperclip.copy(self.generated_password)
            QMessageBox.information(self, "Success", "Password has been copied to clipboard")



