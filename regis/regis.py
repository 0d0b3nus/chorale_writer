import sys
from PyQt5.QtWidgets import (QWidget, QPushButton, QHBoxLayout, QVBoxLayout,
        QApplication)

class StartWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        newButton = QPushButton("New Chorale")
        exerciseButton = QPushButton("Exercise Mode")
        quitButton = QPushButton ("Quit")

        quitButton.clicked.connect(self.close)

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addWidget(newButton)
        vbox.addWidget(exerciseButton)
        vbox.addWidget(quitButton)

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addLayout(vbox)

        self.setLayout(hbox)

        self.setGeometry(300, 300, 300, 150)
        self.setWindowTitle('Regis')
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = StartWindow()
    sys.exit(app.exec())
