from PySide6.QtWidgets import (QMessageBox, QHBoxLayout, QPushButton,
                               QLineEdit, QVBoxLayout, QDialog, QComboBox)

from backend.database_utils import DatabaseUtility


class Register(QDialog):
    """Dialog window for adding new password"""

    def __init__(self, parent, database_util):
        super(Register, self).__init__(parent)
        self.database_util: DatabaseUtility = database_util
        self.setFixedWidth(420)
        self.setWindowTitle("Registration section")
        self.setStyleSheet("QDialog{background:white;}")
        # create widget and layout
        layout = QVBoxLayout()
        self.username = QLineEdit()
        self.username.setObjectName('entry')
        self.username.setPlaceholderText("Enter Your Username/ID")
        self.username.setStyleSheet("QLineEdit{color:rgba(41, 128, 140,1);"
                                    "font-size:18px;padding:4px;margin:10px 0px;}")

        self.password = QLineEdit()
        self.password.setPlaceholderText("Enter your password. Password has to be secure.")
        self.password.setObjectName('entry')
        self.password.setStyleSheet("QLineEdit{color:rgba(41, 128, 140,1);"
                                    "font-size:18px;padding:4px;margin:10px 0px;}")
        self.security_question = QComboBox()
        self.security_question.setPlaceholderText("Select Security Question")
        security_question_list = ["What city were you born in?",
                                  "In what city or town did your parent meet?",
                                  "First concert you attended?",
                                  "How much you paid for your first car?"]
        self.security_question.addItems(security_question_list)
        self.security_question.setStyleSheet("QComboBox{color:rgba(41, 128, 140,1);"
                                             "font-size:18px;padding:4px;margin:10px 0px;}")

        self.security_answer = QLineEdit()
        self.security_answer.setPlaceholderText("Answer To Security question")
        self.security_answer.setObjectName('entry')
        self.security_answer.setStyleSheet("QLineEdit{color:rgba(41, 128, 140,1);"
                                           "font-size:18px;padding:4px;margin:10px 0px;}")

        submit_btn = QPushButton("Register")
        submit_btn.clicked.connect(self.register_btn_callback)

        submit_btn.setObjectName("Add Login")
        submit_btn.setStyleSheet("padding:8px;border-radius:3px;"
                                 "background:white;color:rgba(41, 128, 140,1);"
                                 "font-weight:bold;border:1px solid rgba(41, 128, 140,1);")
        stat_frame = QHBoxLayout()
        layout.addWidget(self.username)
        layout.addWidget(self.password)
        layout.addWidget(self.security_question)
        layout.addWidget(self.security_answer)
        # layout.addWidget(self.sitename)

        layout.addLayout(stat_frame)
        layout.addWidget(submit_btn)
        self.setLayout(layout)

    def register_btn_callback(self):
        username: str = self.username.text()
        password: str = self.password.text()
        security_question: str = self.security_question.currentText()
        security_answer: str = self.security_answer.text()
        if username and password and security_answer:
            if not self.database_util.insert_user_login(
                    username, password, security_question, security_answer
            ):
                QMessageBox.information(self, 'Success', "Account Created Successfully")
            else:
                QMessageBox.warning(self, 'Error Occurred', "Username already exist")

        else:
            QMessageBox.warning(self, 'Error Occurred', "Fields can not be empty")
