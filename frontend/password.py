from functools import partial

from PySide6 import QtCore, QtGui
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QPushButton, QLabel, \
    QLineEdit, QComboBox, QFrame, QVBoxLayout, QHBoxLayout, \
    QHeaderView, QTableWidget, QTableWidgetItem, QMessageBox, QDialog, QCheckBox, QGridLayout

from PySide6.QtCore import Qt

from backend import encryptor
from draw_line import QHSeparationLine, QVSeparationLine
from frontend import draw_line


class PasswordList(QFrame):
    def __init__(self, database_util, user):
        super(PasswordList, self).__init__()
        self.database_util = database_util
        self.user = user
        self.setStyleSheet("QFrame{background:white;}")
        self.setContentsMargins(0, 0, 0, 0)
        main_layout = QVBoxLayout()
        menu_layout = QHBoxLayout()

        add_new = QPushButton("+ Add New")
        add_new.clicked.connect(self.add_new_login)
        add_new.setStyleSheet("padding:8px;border-radius:0px;"
                              "background:rgba(41, 128, 140,1);color:white;font-weight:bold;")
        change_pass = QPushButton("Change Password")
        change_pass.clicked.connect(self.update_password)
        change_pass.setIcon(QIcon('../images/password.png'))
        change_pass.setStyleSheet("padding:8px;border-radius:3px;"
                                  "background:white;color:rgba(41, 128, 140,1);"
                                  "font-weight:bold;border:1px solid rgba(41, 128, 140,1);")

        refresh_btn = QPushButton("Refresh")
        refresh_btn.clicked.connect(self.refresh_btn)
        refresh_btn.setIcon(QIcon('../images/refresh.png'))
        refresh_btn.setStyleSheet("padding:8px;border-radius:3px;"
                                  "background:white;color:rgba(41, 128, 140,1);"
                                  "font-weight:bold;border:1px solid rgba(41, 128, 140,1);")

        menu_layout.addWidget(add_new)
        menu_layout.addWidget(change_pass)
        menu_layout.addWidget(refresh_btn)
        menu_layout.addStretch()
        # menu_layout.addWidget()
        name_label = QLabel("NAME")
        created_on = QLabel("CREATED ON")

        record = self.database_util.fetch_data("Login", user[0])
        if record:
            self.password_layout = QGridLayout()
            self.password_layout.addWidget(name_label, 0, 0)
            self.password_layout.addWidget(created_on, 0, 1)
            index: int = 0
            for logins in record:
                note_title = QLabel(logins[1])
                note_title.setStyleSheet("font-size:20px; font-weight:bold;")
                note_title.setFixedWidth(275)

                self.password_layout.addWidget(note_title, index + 2, 0)

                self.password_layout.addWidget(QLabel("Two Days Ago"), index + 2, 1)
                self.view_button = QPushButton(f"view")
                self.view_button.setStyleSheet("background:white;color:rgba(41, 128, 140,1);"
                                               "font-weight:bold;border:1px solid rgba(41, 128, 140,1);"
                                               "border-radius:4px;padding:5px;")
                self.view_button.clicked.connect(partial(self.view_callback, logins[0]))
                self.update_button = QPushButton("Update")
                self.update_button.setStyleSheet("background:white;color:rgba(41, 128, 140,1);"
                                                 "font-weight:bold;border:1px solid rgba(41, 128, 140,1);"
                                                 "border-radius:4px;padding:5px;")
                self.update_button.clicked.connect(partial(self.update_password_callback, logins[0]))

                self.delete_button = QPushButton(f"Delete")
                self.delete_button.setStyleSheet("background:red;color:white;"
                                                 "font-weight:bold;padding:5px;"
                                                 "border-radius:4px")
                self.delete_button.clicked.connect(partial(self.delete_callback, logins[0]))

                self.view_button.setFixedWidth(40)
                self.password_layout.addWidget(self.view_button, index + 2, 2)
                self.password_layout.addWidget(self.update_button, index + 2, 3)
                self.password_layout.addWidget(self.delete_button, index + 2, 4)
                self.password_layout.addWidget(draw_line.QHSeparationLine(), index + 3, 0, 1, 3, Qt.AlignLeft)
                index += 2

        else:
            password = QVBoxLayout()
            image = QtGui.QPixmap("../images/empty.jpg")  # load image
            image_label = QLabel()
            image_label.setPixmap(image)  # display image using label
            image_label.setAlignment(QtCore.Qt.AlignCenter)
            self.password_layout.addStretch()
            self.password_layout.addWidget(image_label)
            self.password_layout.addStretch()

        main_layout.addLayout(menu_layout)
        main_layout.addWidget(QHSeparationLine())
        main_layout.addLayout(self.password_layout)
        main_layout.addStretch()

        self.setLayout(main_layout)

    def add_new_login(self):
        app = NewOrUpdatePassword(self, self.database_util, self.user)
        app.open()

    def update_password(self):
        win = ChangePasswordOnly(self, self.database_util, self.user)
        win.open()

    def update_password_callback(self, pk: str):
        return_value = self.database_util.fetch_data("Login", self.user[0], pk=pk).fetchone()
        win = NewOrUpdatePassword(self, self.database_util, self.user,
                                  site_name=return_value[1],
                                  username=return_value[2],
                                  password=return_value[3],
                                  pk=return_value[0])
        win.open()

    def view_callback(self, pk):
        return_value = self.database_util.fetch_data("Login", self.user[0], pk=pk).fetchone()
        app = PasswordDetail(self, return_value)
        app.open()

    def delete_callback(self, pk):
        if QMessageBox.question(
                self, "Delete Password!",
                "Are you sure you want to delete this Password?") == 16384:
            self.database_util.delete_record("Login", pk, self.user[0])
            QMessageBox.information(self,
                                    "Deleted Successfully!",
                                    "Password has been deleted successfully. Kindly refresh")

    def refresh_btn(self):
        for i in reversed(range(1, self.password_layout.rowCount() + 1)):
            for j in reversed(range(1, self.password_layout.columnCount() + 1)):
                item = self.password_layout.itemAt(i)
                if item and item.widget():
                    item.widget().setParent(None)  # remove widget from the layout

        self.record = self.database_util.fetch_data("Login", self.user[0]).fetchall()
        index: int = 0
        for logins in self.record:
            note_title = QLabel(logins[1])
            note_title.setFixedWidth(275)
            note_title.setStyleSheet("font-size:20px; font-weight:bold;")

            self.password_layout.addWidget(note_title, index + 2, 0)

            self.password_layout.addWidget(QLabel("Two Days Ago"), index + 2, 1)
            self.view_button = QPushButton(f"view")
            self.view_button.setStyleSheet("background:white;color:rgba(41, 128, 140,1);"
                                           "font-weight:bold;border:1px solid rgba(41, 128, 140,1);"
                                           "border-radius:4px;padding:5px;")
            self.view_button.clicked.connect(partial(self.view_callback, logins[0]))
            self.update_button = QPushButton("Update")
            self.update_button.setStyleSheet("background:white;color:rgba(41, 128, 140,1);"
                                             "font-weight:bold;border:1px solid rgba(41, 128, 140,1);"
                                             "border-radius:4px;padding:5px;")
            self.update_button.clicked.connect(partial(self.update_password_callback, logins[0]))

            self.delete_button = QPushButton(f"Delete")
            self.delete_button.setStyleSheet("background:red;color:white;"
                                             "font-weight:bold;padding:5px;"
                                             "border-radius:4px")
            self.delete_button.clicked.connect(partial(self.delete_callback, logins[0]))

            self.view_button.setFixedWidth(40)
            self.password_layout.addWidget(self.view_button, index + 2, 2)
            self.password_layout.addWidget(self.update_button, index + 2, 3)
            self.password_layout.addWidget(self.delete_button, index + 2, 4)
            self.password_layout.addWidget(draw_line.QHSeparationLine(), index + 3, 0, 1, 3, Qt.AlignLeft)
            index += 2


class NewOrUpdatePassword(QDialog):
    """Dialog window for adding new password"""

    def __init__(self, parent, database_util, user,
                 site_name: str | None = None,
                 username: str | None = None,
                 password: str | None = None,
                 pk: int | None = None):
        super(NewOrUpdatePassword, self).__init__(parent)
        self.database_util = database_util
        self.user = user
        self.login_pk = pk
        self.setFixedWidth(320)
        self.setWindowTitle("New Password")
        self.setStyleSheet("QDialog{background:white;}")
        # create widget and layout
        layout = QVBoxLayout()
        self.sitename = QLineEdit()
        self.sitename.setObjectName('entry')
        self.sitename.setPlaceholderText("Enter Site Name")
        self.sitename.setStyleSheet("QLineEdit{color:rgba(41, 128, 140,1);"
                                    "font-size:18px;padding:4px;margin:10px 0px;}")

        self.username = QLineEdit()
        self.username.setPlaceholderText("Enter Username")
        self.username.setObjectName('entry')
        self.username.setStyleSheet("QLineEdit{color:rgba(41, 128, 140,1);"
                                    "font-size:18px;padding:4px;margin:10px 0px;}")

        self.password = QLineEdit()
        self.password.setPlaceholderText("Enter Password")
        self.password.setObjectName('entry')
        self.password.setStyleSheet("QLineEdit{color:rgba(41, 128, 140,1);"
                                    "font-size:18px;padding:4px;margin:10px 0px;}")
        if site_name and username and password:
            self.sitename.setText(site_name)
            self.username.setText(username)
            self.password.setText(password)

            submit_btn = QPushButton("Update Password")
            submit_btn.clicked.connect(lambda: self.add_or_update_password_callback(True))

        elif password:
            self.password.setText(password)
            submit_btn = QPushButton("Add Password")
            submit_btn.clicked.connect(lambda: self.add_or_update_password_callback(False))
        else:
            submit_btn = QPushButton("Add Password")
            submit_btn.clicked.connect(lambda: self.add_or_update_password_callback(False))

        submit_btn.setObjectName("Add Login")
        submit_btn.setStyleSheet("padding:8px;border-radius:3px;"
                                 "background:white;color:rgba(41, 128, 140,1);"
                                 "font-weight:bold;border:1px solid rgba(41, 128, 140,1);")
        stat_frame = QHBoxLayout()
        layout.addWidget(self.sitename)
        layout.addWidget(self.username)
        layout.addWidget(self.password)
        # layout.addWidget(self.sitename)

        layout.addLayout(stat_frame)
        layout.addWidget(submit_btn)
        self.setLayout(layout)

    def add_or_update_password_callback(self, update: bool | None = None):
        site_name = self.sitename.text()
        username = self.username.text()
        password = self.password.text()
        if site_name and username and password:
            if update:
                self.database_util.update_password(site_name, password,
                                                   owner=self.user[0],
                                                   username=username,
                                                   pk=self.login_pk)
                QMessageBox.information(self, 'Success', "Password Updated successfully")
            else:
                self.database_util.insert_password(site_name, username, password, owner=self.user[0])
                QMessageBox.information(self, 'Success', "Password Added successfully")

        else:
            QMessageBox.warning(self, 'Error Occurred', "All fields most be filled!")
        self.hide()


class ChangePasswordOnly(QDialog):
    """Dialog window for Updating current term"""

    def __init__(self, parent, database_util, user):
        super(ChangePasswordOnly, self).__init__(parent)
        self.database_util = database_util
        self.user = user
        self.setFixedWidth(320)
        self.setWindowTitle("Change Password")
        self.setStyleSheet("QDialog{background:white;}")
        # create widget and layout
        layout = QVBoxLayout()
        self.login_selection = QComboBox()
        record = self.database_util.fetch_data("Login", user[0])
        for logins in record:
            self.login_selection.addItem(logins[1])
        self.login_selection.setStyleSheet("padding:3px;font-size:15px;color:rgba(41, 128, 140,1);"
                                           "margin-top:10px;"
                                           "border-radius:1px;border:1px solid grey;")
        self.login_selection.setPlaceholderText("Select Site To Update")
        self.password = QLineEdit()
        self.password.setObjectName('entry')
        self.password.setPlaceholderText("Enter New Password")
        self.password.setStyleSheet("padding:4px;border-radius:2px;color:rgba(41, 128, 140,1);")
        submit_btn = QPushButton("Change Password")
        submit_btn.setObjectName("submit")
        submit_btn.clicked.connect(self.change_just_password)
        layout.addWidget(self.login_selection)
        layout.addWidget(self.password)
        layout.addWidget(submit_btn)
        style = """QPushButton#submit{padding:8px;border-radius:2px;
                            background:white;color:rgba(41, 128, 140,1);
                            font-weight:bold;border:1px solid rgba(41, 128, 140,1);}"""
        self.setStyleSheet(style)
        self.setLayout(layout)

    def change_just_password(self):
        site_name = self.login_selection.currentText()
        password = self.password.text()
        if not password:
            QMessageBox.warning(self, 'Warning', "Password field cannot be empty")
            return
        self.database_util.update_password(site_name=site_name,
                                           password=password,
                                           owner=self.user[0])
        QMessageBox.information(self, 'Success', "Password Updated Successfully")
        self.hide()


class PasswordDetail(QDialog):
    """Dialog window for viewing details of note"""

    def __init__(self, parent, login_detail):
        super(PasswordDetail, self).__init__(parent)
        print(login_detail)
        self.setFixedWidth(400)
        self.setFixedHeight(400)
        self.setWindowTitle("Note Details")

        # create widget and layout
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        heading = QLabel("Login Details")
        heading.setStyleSheet("QLabel{color:white;font-size:20px;padding:10px;"
                              "background:rgba(41, 128, 140,1);font-weight:bold;};")
        bank_name: QLabel = QLabel(f'Website Name: {login_detail[1]}')
        bank_name.setStyleSheet("QLabel{padding:0px 10px;font-size:15px;"
                                "font-weight:bold;line-height:2;};")
        decrypt_text: str = encryptor.Encryptor().decrypt(login_detail[2])
        bank_pin: QLabel = QLabel(f"Username/ID: {decrypt_text}")
        bank_pin.setStyleSheet("QLabel{padding:0px 10px;font-size:15px;"
                               "font-weight:bold;line-height:2;};")
        account_number: QLabel = QLabel(f"Current Password: {login_detail[3]}")
        account_number.setStyleSheet("QLabel{padding:0px 10px;font-size:15px;"
                                     "font-weight:bold;line-height:2;};")

        layout.addWidget(heading)
        layout.addWidget(bank_name)
        layout.addWidget(draw_line.QHSeparationLine())
        layout.addWidget(bank_pin)
        layout.addWidget(draw_line.QHSeparationLine())
        layout.addWidget(account_number)
        layout.addWidget(draw_line.QHSeparationLine())
        layout.addStretch()
        self.setLayout(layout)
        self.setStyleSheet("QDialog{background:white;};"
                           "QPushButton{background:red;border:none;"
                           "color:rgba(41, 128, 140,1);}")
