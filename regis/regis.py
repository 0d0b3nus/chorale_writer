import sys
from PyQt5.QtWidgets import (QWidget, QPushButton, QHBoxLayout, QVBoxLayout,
        QLabel, QComboBox, QGridLayout, QApplication)
import PyQt5.QtCore

class StartWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        regisLabel = QLabel("<b>Regis</b>")
        regisLabel.setAlignment(PyQt5.QtCore.Qt.AlignCenter)
        procLabel = QLabel("Procedural Chorale Generator")
        procLabel.setAlignment(PyQt5.QtCore.Qt.AlignCenter)

        newButton = QPushButton("New Chorale")
        exerciseButton = QPushButton("Exercise Mode")
        quitButton = QPushButton ("Quit")

        exerciseButton.clicked.connect(self.close)
        quitButton.clicked.connect(self.close)

        grid = QGridLayout()

        grid.addWidget(regisLabel, 0, 1)
        grid.addWidget(procLabel, 1, 1)
        grid.addWidget(newButton, 2, 1)
        grid.addWidget(exerciseButton, 3, 1)
        grid.addWidget(quitButton, 4, 1)

        self.setLayout(grid)

        self.setWindowTitle('Regis')
        self.show()

class ExerciseWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        size = 5
        grid = QGridLayout()

        labels = [''] * size
        dropdowns = [''] * size
        checks = [''] * size
        for i in range(size):
            labels[i] = QLabel("{}".format(i+1))
            grid.addWidget(labels[i], i+1, 0)
            dropdowns[i] = QComboBox(self)
            grid.addWidget(dropdowns[i], i+1, 2)

        gradeButton = QPushButton('Grade')
        grid.addWidget(gradeButton, i+size+1, 0)
        newButton = QPushButton('New')
        grid.addWidget(newButton, i+size+1, 2)
        backButton = QPushButton('Back')
        grid.addWidget(backButton, i+size+1, 4)

        self.setLayout(grid)

        self.setWindowTitle('Regis: Exercise Mode')
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = StartWindow()
    exs = ExerciseWindow()
    sys.exit(app.exec())
