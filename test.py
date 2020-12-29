from PyQt5 import QtCore, QtGui, QtChart, QtWidgets, uic
from PyQt5.QtChart import *
from PyQt5.Qt import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QGraphicsDropShadowEffect
from inference_model import getPredictions
import sys

preds = getPredictions()

class Demo(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('../UI Files/demo2.ui', self)
        self.setFixedSize(1191, 771)
        
        shadow = QGraphicsDropShadowEffect()  
        shadow.setBlurRadius(-5)
        self.CentrePanel.setGraphicsEffect(shadow) 
    
        self.dashBtn.clicked.connect(lambda: self.changePage("Dashboard"))
        self.workBtn.clicked.connect(lambda: self.changePage("Workspace"))
        self.dataBtn.clicked.connect(lambda: self.changePage("Dataset"))
        self.libBtn.clicked.connect(lambda: self.changePage("Library"))

        label1 = QLabel("Pitted:")
        label1.setStyleSheet("color: white; font-size: 18px; font-family: 'Garamond'; font-weight: bold")
        label1End = QLabel("92%")
        label1End.setStyleSheet("color: cyan; font-size: 15px")
        label2 = QLabel("Patches:")
        label2.setStyleSheet("color: white; font-size: 18px; font-family: 'Garamond'; font-weight: bold")
        label2End = QLabel("78%")
        label2End.setStyleSheet("color: cyan; font-size: 15px")
        label3 = QLabel("Surface:")
        label3.setStyleSheet("color: white; font-size: 18px; font-family: 'Garamond'; font-weight: bold")
        label3End = QLabel("64%")
        label3End.setStyleSheet("color: cyan; font-size: 15px")
        label4 = QLabel("Scratches:")
        label4.setStyleSheet("color: white; font-size: 18px; font-family: 'Garamond'; font-weight: bold")
        label4End = QLabel("42%")
        label4End.setStyleSheet("color: cyan; font-size: 15px")
        label5 = QLabel("Something:")
        label5.setStyleSheet("color: white; font-size: 18px; font-family: 'Garamond'; font-weight: bold")
        label5End = QLabel("31%")
        label5End.setStyleSheet("color: cyan; font-size: 15px")
        label6 = QLabel("Another:")
        label6.setStyleSheet("color: white; font-size: 18px; font-family: 'Garamond'; font-weight: bold")
        label6End = QLabel("12%")
        label6End.setStyleSheet("color: cyan; font-size: 15px")
        self.gridLayout.addWidget(label1, 0, 0)
        self.gridLayout.addWidget(label1End, 0, 1)
        self.gridLayout.addWidget(label2, 1, 0)
        self.gridLayout.addWidget(label2End, 1, 1)
        self.gridLayout.addWidget(label3, 2, 0)
        self.gridLayout.addWidget(label3End, 2, 1)
        self.gridLayout.addWidget(label4, 3, 0)
        self.gridLayout.addWidget(label4End, 3, 1)
        self.gridLayout.addWidget(label5, 4, 0)
        self.gridLayout.addWidget(label5End, 4, 1)
        self.gridLayout.addWidget(label6, 5, 0)
        self.gridLayout.addWidget(label6End, 5, 1)

    def changePage(self, text):
        if text == 'Workspace':
            self.stackedWidget.setCurrentIndex(0)
        elif text == 'Dataset':
            self.stackedWidget.setCurrentIndex(3)
        elif text == 'Library':
            self.stackedWidget.setCurrentIndex(1)
        else:
            self.stackedWidget.setCurrentIndex(2)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    demo = Demo()
    demo.show()
    sys.exit(app.exec_())
