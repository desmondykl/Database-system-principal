from PyQt5.QtWidgets import *


class QDMNodeContentWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.wdg_label = QLabel("Some Title")
        self.textbox = QTextEdit("foo")
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)
        self.setLayout(self.layout)

        #self.wdg_label = QLabel("Some Title")
        self.wdg_label.setWordWrap(True)
        #self.layout.addWidget(self.wdg_label)
        self.textbox.setReadOnly(True)
        self.layout.addWidget(self.textbox)
