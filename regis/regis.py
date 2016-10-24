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
        regisFont = regisLabel.font()
        regisFont.setPointSize(20)
        regisLabel.setFont(regisFont)
        procLabel = QLabel("Procedural Chorale Generator")
        procLabel.setAlignment(PyQt5.QtCore.Qt.AlignCenter)

        newButton = QPushButton("New Chorale")
        exerciseButton = QPushButton("Exercise Mode")
        quitButton = QPushButton ("Quit")

        exerciseButton.clicked.connect(self.click_exercise)
        quitButton.clicked.connect(self.close)

        grid = QGridLayout()

        grid.addWidget(regisLabel, 0, 1)
        grid.addWidget(procLabel, 1, 1)
        grid.addWidget(newButton, 2, 1)
        grid.addWidget(exerciseButton, 3, 1)
        grid.addWidget(quitButton, 4, 1)

        self.setLayout(grid)

        self.setWindowTitle('Regis')
        self.resize(340, 220)
        self.show()

    @PyQt5.QtCore.pyqtSlot()
    def click_exercise(self):
        self.hide()
        self.exercise = ExerciseWindow(self)
        self.exercise.exec()

class ExerciseWindow(QWidget):

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.initUI()

    def initUI(self):
        size = 5
        mainVBox = QVBoxLayout()
        sheet = QLabel('SHEET MUSIC HERE')
        mainVBox.addWidget(sheet)

        labels = [''] * size
        dropdowns = [''] * size
        checks = [''] * size
        hboxes = [''] * size
        dropdownsVBox = QVBoxLayout()
        mainVBox.addLayout(dropdownsVBox)
        for i in range(size):
            hboxes[i] = QHBoxLayout()
            labels[i] = QLabel("<b>{}</b>".format(i+1))
            labels[i].setFixedWidth(10)
            labels[i].setAlignment(PyQt5.QtCore.Qt.AlignRight | PyQt5.QtCore.Qt.AlignVCenter)
            hboxes[i].addWidget(labels[i])
            dropdowns[i] = QComboBox(self)
            hboxes[i].addWidget(dropdowns[i])
            checks[i] = QLabel('C')
            hboxes[i].addWidget(checks[i])
            dropdownsVBox.addLayout(hboxes[i])

        buttonsHBox = QHBoxLayout()
        gradeButton = QPushButton('Grade')
        buttonsHBox.addWidget(gradeButton)
        newButton = QPushButton('New')
        buttonsHBox.addWidget(newButton)
        backButton = QPushButton('Back')
        buttonsHBox.addWidget(backButton)
        backButton.clicked.connect(self.click_back)
        mainVBox.addLayout(buttonsHBox)

        self.setLayout(mainVBox)
        self.setWindowTitle('Regis: Exercise Mode')
        self.show()

    def click_back(self):
        self.hide()
        self.parent.show()

class NewChoraleWindow(QWidget):

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.initUI()

    def initUI(self):
        vbox = QVBoxLayout()
        sheet = QLabel('SHEET MUSIC HERE')
        vbox.addWidget(sheet)

        hbox = QHBoxLayout()
        newButton = QPushButton('New')
        playButton = QPushButton('Play')
        stopButton = QPushButton('Stop')
        saveButton = QPushButton('Save')
        backButton = QPushButton('Back')
        hbox.addWidget(newButton)
        hbox.addWidget(playButton)
        hbox.addWidget(stopButton)
        hbox.addWidget(saveButton)
        hbox.addWidget(backButton)
        vbox.addLayout(hbox)

        self.setLayout(vbox)
        self.setWindowTitle('Regis: New Chorale')
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = StartWindow()
    sys.exit(app.exec())
