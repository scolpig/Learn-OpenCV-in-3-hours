import sys
import cv2
import numpy as np
from PyQt5.QtWidgets import *
from PyQt5 import QtGui
from PyQt5 import QtCore



from PyQt5 import uic

form_window = uic.loadUiType('./mainwidget.ui')[0]

class Exam(QWidget, form_window):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.CIRCLE = 0
        self.RECTANGLE = 1
        self.ELLIPSE = 2
        self.paintcolor = (255, 0, 0)
        self.brush = 2
        self.setWindowTitle('painter Ver 1.0.0')
        self.setMouseTracking(True)
        self.figure = self.CIRCLE
        self.start_pos = None
        self.radius = 3
        self.src = np.full((500, 500, 3), 255, dtype=np.uint8)
        self.img_to_label(self.src)
        self.btn_red.clicked.connect(self.setRed)
        self.btn_blue.clicked.connect(self.setBlue)
        self.btn_green.clicked.connect(self.setGreen)
        self.cmb_figure.currentIndexChanged.connect(self.setFigure)
        self.btn_color.clicked.connect(self.user_color)
        self.sb_thickness.valueChanged.connect(self.user_brush)

    def user_brush(self, thick):
        self.brush = thick

    def user_color(self):
        p_color = QColorDialog.getColor()
        self.paintcolor = (p_color.red(), p_color.green(), p_color.blue())

    def setFigure(self):
        figure = self.cmb_figure.currentText()
        if figure == 'Circle':
            self.figure = self.CIRCLE
        elif figure == 'Rectangle':
            self.figure = self.RECTANGLE

        elif figure == 'Ellipse':
            self.figure = self.ELLIPSE
    def setRed(self):
        self.paintcolor = (255, 0, 0)
    def setBlue(self):
        self.paintcolor = (0, 0, 255)
    def setGreen(self):
        self.paintcolor = (0, 255, 0)

    def img_to_label(self, src):
        h, w, c = self.src.shape
        qImg = QtGui.QImage(src, w, h, w * c, QtGui.QImage.Format_RGB888)
        pixmap = QtGui.QPixmap.fromImage(qImg)
        self.lbl_img.setPixmap(pixmap)
    def mousePressEvent(self, e):  # e ; QMouseEvent
        if e.buttons() & QtCore.Qt.LeftButton:
            self.start_pos = (e.x(), e.y())

    def mouseMoveEvent(self, e):  # e ; QMouseEvent
        if isinstance(self.start_pos, tuple):
            new_img = self.src.copy()
            if self.figure == self.CIRCLE:
                cv2.circle(new_img, self.start_pos,
                       max(abs(self.start_pos[0]-e.x()), abs(self.start_pos[1]-e.y())),
                       self.paintcolor, self.brush)
            elif self.figure == self.RECTANGLE:
                cv2.rectangle(new_img, self.start_pos,
                       (e.x(), e.y()),
                       self.paintcolor, self.brush)
            elif self.figure == self.ELLIPSE:
                cv2.ellipse(new_img,
                ((self.start_pos[0] - (self.start_pos[0] - e.x()) // 2,
                 self.start_pos[1] - (self.start_pos[1] - e.y()) // 2),
                (abs(self.start_pos[0]-e.x()), abs(self.start_pos[1]-e.y())), 0),
                     self.paintcolor, self.brush)
            self.img_to_label(new_img)


    def mouseReleaseEvent(self, e):

        if self.figure == self.CIRCLE:
            cv2.circle(self.src, self.start_pos,
                   max(abs(self.start_pos[0] - e.x()), abs(self.start_pos[1] - e.y())),
                   self.paintcolor, self.brush)
        elif self.figure == self.RECTANGLE:
            cv2.rectangle(self.src, self.start_pos,
                          (e.x(), e.y()),
                          self.paintcolor, self.brush)
        elif self.figure == self.ELLIPSE:
                cv2.ellipse(self.src,
                ((self.start_pos[0]-(self.start_pos[0]-e.x())//2,
                  self.start_pos[1]-(self.start_pos[1]-e.y())//2),
                (abs(self.start_pos[0]-e.x()), abs(self.start_pos[1]-e.y())), 0),
                        self.paintcolor, self.brush)
        self.img_to_label(self.src)
        self.start_pos = None


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = Exam()
    mainWindow.show()
    sys.exit(app.exec_())