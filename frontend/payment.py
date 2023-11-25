from functools import partial

from PySide6 import QtCore
from PySide6.QtWidgets import QPushButton, QLabel, \
    QLineEdit, QComboBox, QFrame, QVBoxLayout, QHBoxLayout, \
    QHeaderView, QTableWidget, QTableWidgetItem, QMessageBox, QDialog, QCheckBox, QGridLayout, QPlainTextEdit, \
    QScrollArea

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QIcon

from backend import encryptor
from draw_line import QHSeparationLine, QVSeparationLine
from frontend import draw_line


class PaymentInfo(QFrame):
    def __init__(self, database_util, user):
        super(PaymentInfo, self).__init__()
        self.database_util = database_util
        self.user = user
        self.setStyleSheet("QFrame{background:white;}")
        self.main_layout = QVBoxLayout()
        menu_layout = QHBoxLayout()

        add_new = QPushButton(" New Payment Pin")
        add_new.clicked.connect(self.add_new_payment)
        # add_new.setIcon(QIcon("../images/add.png"))
        add_new.setStyleSheet("padding:8px;border-radius:3px;"
                              "color:rgba(41, 128, 140,1);"
                              "background:white;font-weight:bold;"
                              "border:1px solid rgba(41, 128, 140,1);"
                              )
        refresh_btn = QPushButton("Refresh")
        refresh_btn.clicked.connect(self.refresh_btn)
        refresh_btn.setStyleSheet("padding:8px;border-radius:3px;"
                                  "background:white;color:rgba(41, 128, 140,1);"
                                  "font-weight:bold;border:1px solid rgba(41, 128, 140,1);")

        menu_layout.addWidget(add_new)
        menu_layout.addWidget(refresh_btn)
        menu_layout.addStretch()
        # menu_layout.addWidget()
        name_label = QLabel("NAME")
        created_on = QLabel("CREATED ON")

        self.note_layout = QGridLayout()
        self.note_layout.addWidget(name_label, 0, 0)
        self.note_layout.addWidget(created_on, 0, 1)
        self.record = self.database_util.fetch_data("Payments", self.user[0]).fetchall()
        if self.record:

            index = 0
            for logins in self.record:
                note_title = QLabel(logins[1])
                note_title.setStyleSheet("font-size:20px; font-weight:bold;")
                note_title.setFixedWidth(275)

                self.note_layout.addWidget(note_title, index + 2, 0)

                self.note_layout.addWidget(QLabel("Two Days Ago"), index + 2, 1)
                self.view_button = QPushButton(f"view")
                self.view_button.setStyleSheet("background:white;color:rgba(41, 128, 140,1);"
                                               "font-weight:bold;border:1px solid rgba(41, 128, 140,1);"
                                               "border-radius:4px;padding:5px;")
                self.view_button.clicked.connect(partial(self.view_callback, logins[0]))
                self.update_button = QPushButton("Update")
                self.update_button.setStyleSheet("background:white;color:rgba(41, 128, 140,1);"
                                                 "font-weight:bold;border:1px solid rgba(41, 128, 140,1);"
                                                 "border-radius:4px;padding:5px;")
                self.update_button.clicked.connect(partial(self.update_callback, logins[0]))

                self.delete_button = QPushButton(f"Delete")
                self.delete_button.setStyleSheet("background:red;color:white;"
                                                 "font-weight:bold;padding:5px;"
                                                 "border-radius:4px")
                self.delete_button.clicked.connect(partial(self.delete_callback, logins[0]))

                self.view_button.setFixedWidth(40)
                self.note_layout.addWidget(self.view_button, index + 2, 2)
                self.note_layout.addWidget(self.update_button, index + 2, 3)
                self.note_layout.addWidget(self.delete_button, index + 2, 4)
                self.note_layout.addWidget(draw_line.QHSeparationLine(), index + 3, 0, 1, 3, Qt.AlignLeft)
                index += 2

        else:
            self.note_layout = QVBoxLayout()
            image = QPixmap("../images/empty.jpg")  # load image
            image_label = QLabel()
            image_label.setPixmap(image)  # display image using label
            image_label.setAlignment(QtCore.Qt.AlignCenter)
            self.note_layout.addStretch()
            self.note_layout.addWidget(image_label)
            self.note_layout.addStretch()

        self.main_layout.addLayout(menu_layout)
        self.main_layout.addWidget(QHSeparationLine())
        self.main_layout.addLayout(self.note_layout)
        self.main_layout.addStretch()

        self.setLayout(self.main_layout)

    def add_new_payment(self):
        app = NewOrUpdatePayment(self, self.database_util, self.user)
        app.open()

    def refresh_btn(self):
        for i in reversed(range(1, self.note_layout.rowCount() + 1)):
            for j in reversed(range(1, self.note_layout.columnCount() + 1)):
                print(f"i-={i} j={j}")
                item = self.note_layout.itemAt(i)
                if item and item.widget():
                    pass
                    item.widget().setParent(None)  # remove widget from the layout

        self.record = self.database_util.fetch_data("Payments", self.user[0]).fetchall()
        index = 0
        for logins in self.record:
            note_title = QLabel(logins[1])
            note_title.setFixedWidth(275)
            note_title.setStyleSheet("font-size:20px; font-weight:bold;")

            self.note_layout.addWidget(note_title, index + 2, 0)

            self.note_layout.addWidget(QLabel("Two Days Ago"), index + 2, 1)
            self.view_button = QPushButton(f"view")
            self.view_button.setStyleSheet("background:white;color:rgba(41, 128, 140,1);"
                                           "font-weight:bold;border:1px solid rgba(41, 128, 140,1);"
                                           "border-radius:4px;padding:5px;")
            self.view_button.clicked.connect(partial(self.view_callback, logins[0]))
            self.update_button = QPushButton("Update")
            self.update_button.setStyleSheet("background:white;color:rgba(41, 128, 140,1);"
                                             "font-weight:bold;border:1px solid rgba(41, 128, 140,1);"
                                             "border-radius:4px;padding:5px;")
            self.update_button.clicked.connect(partial(self.update_callback, logins[0]))

            self.delete_button = QPushButton(f"Delete")
            self.delete_button.setStyleSheet("background:red;color:white;"
                                             "font-weight:bold;padding:5px;"
                                             "border-radius:4px")
            self.delete_button.clicked.connect(partial(self.delete_callback, logins[0]))

            self.view_button.setFixedWidth(40)
            self.note_layout.addWidget(self.view_button, index + 2, 2)
            self.note_layout.addWidget(self.update_button, index + 2, 3)
            self.note_layout.addWidget(self.delete_button, index + 2, 4)
            self.note_layout.addWidget(draw_line.QHSeparationLine(), index + 3, 0, 1, 3, Qt.AlignLeft)
            index += 2

    def view_callback(self, pk):
        return_value = self.database_util.fetch_data("Payments", self.user[0], pk=pk).fetchone()
        app = PaymentDetail(self, return_value)
        app.open()

    def update_callback(self, pk):
        return_value = self.database_util.fetch_data("Payments", self.user[0], pk=pk).fetchone()
        app = NewOrUpdatePayment(self, self.database_util,
                                 self.user, bank_name=return_value[1],
                                 bank_pin=return_value[2],
                                 account_number=return_value[3],
                                 pk=return_value[0])
        app.open()

    def delete_callback(self, pk):
        if QMessageBox.question(self, "Delete Note!", "Are you sure you want to delete this note?") == 16384:
            self.database_util.delete_record("Payments", pk, self.user[0])
            QMessageBox.information(self, "Deleted Successfully!", "Your name has been deleted success. Kindly refresh")


class NewOrUpdatePayment(QDialog):
    """Dialog window for adding new password"""

    def __init__(self, parent, database_util, user,
                 bank_name: str | None = None,
                 bank_pin: str | None = None,
                 account_number: str | None = None,
                 pk: int | None = None):
        super(NewOrUpdatePayment, self).__init__(parent)
        self.user = user
        self.pk = pk
        self.database_util = database_util
        self.setFixedWidth(400)
        self.setFixedHeight(400)
        self.setWindowTitle("New Note")
        self.setStyleSheet("QDialog{background:white;}")
        # create widget and layout
        layout = QVBoxLayout()
        self.bank_name = QLineEdit()
        self.bank_name.setObjectName('entry')
        if bank_name:
            self.bank_name.setText(bank_name)
        self.bank_name.setPlaceholderText("Enter Bank Name")
        self.bank_name.setStyleSheet("QLineEdit{color:rgba(41, 128, 140,1);"
                                     "font-size:18px;padding:4px;margin:10px 0px;}")
        self.bank_pin = QLineEdit()
        self.bank_pin.setObjectName('entry')
        self.bank_pin.setPlaceholderText("Enter Bank Pin")
        self.bank_pin.setStyleSheet("QLineEdit{color:rgba(41, 128, 140,1);"
                                    "font-size:18px;}")
        if bank_pin:
            bank_pin = encryptor.Encryptor().decrypt(bank_pin)
            self.bank_pin.setText(bank_pin)
            submit_btn = QPushButton("Update Details")
            submit_btn.clicked.connect(lambda: self.add_or_update_payment(True))
        else:
            submit_btn = QPushButton("Add Details")
            submit_btn.clicked.connect(self.add_or_update_payment)

        self.account_number = QLineEdit()
        if account_number:
            self.account_number.setText(account_number)
        self.account_number.setObjectName('entry')
        self.account_number.setPlaceholderText("Enter Account Number (optional)")
        self.account_number.setStyleSheet("QLineEdit{color:rgba(41, 128, 140,1);"
                                          "font-size:18px;margin:15px 0px;}")

        submit_btn.setObjectName("Add Login")
        submit_btn.setStyleSheet("padding:8px;border-radius:3px;"
                                 "background:rgba(41, 128, 140,1);"
                                 "color:white;"
                                 "font-weight:bold;")
        layout.addWidget(self.bank_name)
        layout.addWidget(self.bank_pin)
        layout.addWidget(self.account_number)
        layout.addWidget(submit_btn)
        layout.addStretch()
        self.setLayout(layout)

    def add_or_update_payment(self, update: bool | None = None):
        bank_name = self.bank_name.text()
        bank_pin = self.bank_pin.text()
        account_number: str | None = self.account_number.text()
        if bank_name and bank_pin:
            if not update:
                self.database_util.insert_payment(bank_name, bank_pin,
                                                  account_number,
                                                  owner=self.user[0])
            else:
                self.database_util.update_payment(bank_name,
                                                  bank_pin, account_number,
                                                  owner=self.user[0],
                                                  pk=self.pk)

            QMessageBox.information(self, 'Success', "Payment Details Added successfully")

        else:
            QMessageBox.warning(self, 'Error Occurred', "All fields most be filled!")
        self.hide()


class PaymentDetail(QDialog):
    """Dialog window for viewing details of note"""

    def __init__(self, parent, payment_detail):
        super(PaymentDetail, self).__init__(parent)
        print(payment_detail)
        self.setFixedWidth(400)
        self.setFixedHeight(400)
        self.setWindowTitle("Note Details")

        # create widget and layout
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        heading = QLabel("Payment Details")
        heading.setStyleSheet("QLabel{color:white;font-size:20px;padding:10px;"
                              "background:rgba(41, 128, 140,1);font-weight:bold;};")
        bank_name: QLabel = QLabel(f'Bank Name: {payment_detail[1]}')
        bank_name.setStyleSheet("QLabel{padding:0px 10px;font-size:15px;"
                                "font-weight:bold;line-height:2;};")
        decrypt_text: str = encryptor.Encryptor().decrypt(payment_detail[2])
        bank_pin: QLabel = QLabel(f"Bank Pin: {decrypt_text}")
        bank_pin.setStyleSheet("QLabel{padding:0px 10px;font-size:15px;"
                               "font-weight:bold;line-height:2;};")
        account_number: QLabel = QLabel(f"Account Number: {payment_detail[3]}")
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
