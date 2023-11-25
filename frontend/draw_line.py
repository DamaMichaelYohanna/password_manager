from PySide6 import QtWidgets


class QHSeparationLine(QtWidgets.QFrame):
    """draw a horizontal line"""

    def __init__(self):
        super(QHSeparationLine, self).__init__()
        self.setMinimumWidth(1)
        self.setFixedHeight(20)
        self.setFrameShape(QtWidgets.QFrame.HLine)
        self.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        return


class QVSeparationLine(QtWidgets.QFrame):
    """draw a vertical line"""

    def __init__(self):
        super(QVSeparationLine, self).__init__()
        self.setFixedHeight(20)
        self.setMinimumHeight(1)
        self.setFrameShape(QtWidgets.QFrame.VLine)
        self.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        return
