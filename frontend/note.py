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


class NoteList(QFrame):
    def __init__(self, database_util, user):
        super(NoteList, self).__init__()
        self.database_util = database_util
        self.user = user
        self.setStyleSheet("QFrame{background:white;}")
        self.main_layout = QVBoxLayout()
        menu_layout = QHBoxLayout()

        add_new = QPushButton(" ADD NEW NOTE")
        add_new.clicked.connect(self.add_new_login)
        add_new.setIcon(QIcon("../images/add.png"))
        add_new.setStyleSheet("padding:8px;border-radius:3px;"
                              "background:white;font-weight:bold;border:1px solid rgba(41, 128, 140,1);"
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
        self.record = self.database_util.fetch_data("Notes", self.user[0]).fetchall()
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

    def add_new_login(self):
        app = NewOrUpdateNote(self, self.database_util, self.user)
        app.open()

    def refresh_btn(self):
        for i in reversed(range(1, self.note_layout.rowCount() + 1)):
            for j in reversed(range(1, self.note_layout.columnCount() + 1)):
                print(f"i-={i} j={j}")
                item = self.note_layout.itemAt(i)
                if item and item.widget():
                    pass
                    item.widget().setParent(None)  # remove widget from the layout

        self.record = self.database_util.fetch_data("Notes", self.user[0]).fetchall()
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
        return_value = self.database_util.fetch_data("Notes", self.user[0], pk=pk).fetchone()
        app = NoteDetail(self, return_value)
        app.open()

    def update_callback(self, pk):
        return_value = self.database_util.fetch_data("Notes", self.user[0], pk=pk).fetchone()
        app = NewOrUpdateNote(self, self.database_util,
                              self.user, note_title=return_value[1],
                              note_content=return_value[2], pk=return_value[0])
        app.open()

    def delete_callback(self, pk):
        print("called", pk)
        if QMessageBox.question(self, "Delete Note!", "Are you sure you want to delete this note?") == 16384:
            self.database_util.delete_record("Notes", pk, self.user[0])
            QMessageBox.information(self, "Deleted Successfully!", "Your name has been deleted success. Kindly refresh")


class NewOrUpdateNote(QDialog):
    """Dialog window for adding new password"""

    def __init__(self, parent, database_util, user,
                 note_title: str | None = None,
                 note_content: str | None = None,
                 pk: int | None = None):
        super(NewOrUpdateNote, self).__init__(parent)
        self.user = user
        self.pk = pk
        self.database_util = database_util
        self.setFixedWidth(400)
        self.setFixedHeight(400)
        self.setWindowTitle("New Note")
        self.setStyleSheet("QDialog{background:white;}")
        # create widget and layout
        layout = QVBoxLayout()
        self.title = QLineEdit()
        self.title.setObjectName('entry')
        if note_title:
            self.title.setText(note_title)
        self.title.setPlaceholderText("Enter Title Of Note")
        self.title.setStyleSheet("QLineEdit{color:rgba(41, 128, 140,1);"
                                 "font-size:15px;padding:4px;}")
        self.note = QPlainTextEdit()
        self.note.setObjectName('entry')
        self.note.setPlaceholderText("Type your note here")
        self.note.setStyleSheet("QPlainTextEdit{color:rgba(41, 128, 140,1);font-size:15px;}")
        if note_content:
            note_content = encryptor.Encryptor().decrypt(note_content)
            self.note.insertPlainText(note_content)
            submit_btn = QPushButton("Update Note")
            submit_btn.clicked.connect(lambda: self.add_or_update_note(True))
        else:
            submit_btn = QPushButton("Add Note")
            submit_btn.clicked.connect(self.add_or_update_note)
        submit_btn.setObjectName("Add Login")
        submit_btn.setStyleSheet("padding:8px;border-radius:3px;"
                                 "background:white;color:rgba(41, 128, 140,1);"
                                 "font-weight:bold;border:1px solid rgba(41, 128, 140,1);")
        layout.addWidget(self.title)
        layout.addWidget(self.note)
        # layout.addWidget(self.sitename)

        layout.addWidget(submit_btn)
        self.setLayout(layout)

    def add_or_update_note(self, update: bool | None=None):
        note_title = self.title.text()
        note_content = self.note.toPlainText()
        if note_title and note_content:
            if not update:
                self.database_util.insert_note(note_title, note_content, owner=self.user[0])
            else:
                self.database_util.update_note(note_title, note_content,
                                               owner=self.user[0], pk=self.pk)

            QMessageBox.information(self, 'Success', "Note Added successfully")

        else:
            QMessageBox.warning(self, 'Error Occurred', "All fields most be filled!")
        self.hide()


class NoteDetail(QDialog):
    """Dialog window for viewing details of note"""

    def __init__(self, parent, note):
        super(NoteDetail, self).__init__(parent)
        self.setFixedWidth(400)
        self.setFixedHeight(400)
        self.setWindowTitle("Note Details")

        # create widget and layout
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        note_title = QLabel(note[1])
        note_title.setWordWrap(True)
        note_title.setStyleSheet("QLabel{color:white;font-size:20px;padding:10px;"
                                 "background:rgba(41, 128, 140,1);font-weight:bold;};")
        decrypt_text = encryptor.Encryptor().decrypt(note[2])
        note_content = QLabel(decrypt_text)
        note_content.setWordWrap(True)
        note_content.setStyleSheet("QLabel{padding:0px 10px;font-size:15px;"
                                   "font-weight:bold;line-height:2;};")
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(note_content)
        layout.addWidget(note_title)
        layout.addWidget(scroll_area)
        self.setLayout(layout)
        self.setStyleSheet("QDialog{background:white;};"
                           "QPushButton{background:red;border:none;"
                           "color:rgba(41, 128, 140,1);}")
