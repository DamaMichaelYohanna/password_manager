import sys
from PySide6 import QtWidgets as widget
from PySide6 import QtGui, QtCore
from PySide6.QtWidgets import QMainWindow, QStackedWidget

from backend import database, database_utils
from frontend import draw_line
from frontend.dashboard import MainMenu
from frontend.register import Register


class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Password Warehouse")
        self.setWindowIcon(QtGui.QIcon("images/icon.png"))
        self.setFixedSize(800, 550)
        self.setStyleSheet("QMainWindow{background:white;}")
        self.init_ui()
        self.show()

    def init_ui(self):
        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)

        self.login_screen = LoginPage(self)

        self.central_widget.addWidget(self.login_screen)
        # self.central_widget.addWidget(self.main_screen)

        self.central_widget.setCurrentWidget(self.login_screen)


class LoginPage(widget.QWidget):
    def __init__(self, parent):
        super(LoginPage, self).__init__()
        self.parent = parent
        self.database_util = database_utils.DatabaseUtility()
        main_layout = widget.QVBoxLayout(self)  # main layout

        image = QtGui.QPixmap("../images/lock.jfif") # load image
        image_label = widget.QLabel()
        image_label.setPixmap(image)  # display image using label
        image_label.setAlignment(QtCore.Qt.AlignCenter)

        login_center = widget.QVBoxLayout() # create layout for form
        # ---------------------------------------------------------------

        self.entry1 = widget.QLineEdit()
        self.entry1.setFixedWidth(400)
        self.entry1.setPlaceholderText("Enter Username")
        self.entry1.setObjectName('entry')

        self.entry2 = widget.QLineEdit()
        self.entry2.setPlaceholderText("Enter Your Password")
        self.entry2.setEchoMode(widget.QLineEdit.Password)
        self.entry2.setObjectName('entry')
        self.entry2.setFixedWidth(400)

        login_btn = widget.QPushButton("Login")
        login_btn.clicked.connect(self.validate_login)
        login_btn.setObjectName('login')

        sub_layout = widget.QHBoxLayout()  # sub layout for buttons
        forgot_pass = widget.QPushButton("Recover Password")
        forgot_pass.setObjectName("little")
        register = widget.QPushButton("Register Here")
        register.clicked.connect(self.register_btn_callback)
        register.setObjectName('little')
        sub_layout.addWidget(forgot_pass)
        sub_layout.addWidget(register)
        #  Position widgets
        login_center.addWidget(self.entry1)
        login_center.addWidget(self.entry2)
        login_center.addWidget(login_btn)
        login_center.addWidget(draw_line.QHSeparationLine())
        login_center.addLayout(sub_layout)
        login_center.setAlignment(QtCore.Qt.AlignCenter)

        # right part of the login body
        # ------------------------------------------------------------------
        # add head and body layout to the main layout

        main_layout.addWidget(image_label)
        main_layout.addStretch(1)
        main_layout.addLayout(login_center)
        main_layout.addStretch(2)
        style = """
            QPushButton#login{padding:10px;font-size:15px;
            margin-top:10px;background:rgba(41, 128, 140,1);
            color:white;border-radius:5px;border:1px solid rgba(41, 128, 140,1);
            font-weight:bold;}
            
            QLineEdit#entry{padding:5px;font-size:20px;
            color:rgba(41, 128, 140,1);margin-top:10px;
            border-radius:5px;border:1px solid grey;}
            
            QPushButton#little{color:rgba(41, 128, 140,1);padding:5px}
            """
        self.setStyleSheet(style)
        self.setLayout(main_layout)  # set main layout

    def validate_login(self):
        username = self.entry1.text()
        password = self.entry2.text()
        if not username or not password:
            widget.QMessageBox.warning(self, "Error", "Fields can't be empty")
        else:
            user = self.database_util.login(username, password)
            if user:
                print(user)
                widget.QMessageBox.information(self, "Success", f"Login Successful, {user[1]}")
                self.parent.central_widget.addWidget(MainMenu(user))
                self.parent.central_widget.setCurrentIndex(1)

            else:
                widget.QMessageBox.warning(self, "Error", "Incorrect Login Details. Try Again!")

    def register_btn_callback(self):
        app = Register(self, self.database_util)
        app.open()

win = widget.QApplication(sys.argv)
my_app = MainApp()
my_app.resize(600, 200)
my_app.show()
win.exec()
