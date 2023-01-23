import cv2
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import pyqtgraph as pg
import ResizeImage

# Global parameters
file_name = ""
image = [[0]]
sized_image = [[0]]
width_factor = 0
height_factor = 0


def plot_image(image, graphicsView):
    figure = Figure(figsize=(3.5, 3.5))
    canvas = FigureCanvasQTAgg(figure)
    ax = figure.subplots()
    ax.imshow(image, cmap='gray')
    scene = QtWidgets.QGraphicsScene()
    scene.addWidget(canvas)
    graphicsView.setScene(scene)
    graphicsView.show()


def graph_histogram(graphicsView, image):
    graphWidget = pg.PlotWidget()
    histogram = cv2.calcHist([image.astype('float32')], [0], None, [256], [0, 256])
    graphWidget.plot(list(range(histogram.size)), histogram[:, 0])
    graphWidget.setGeometry(0, 455, 395, 383)
    graphWidget.show()
    scene = QtWidgets.QGraphicsScene()
    scene.addWidget(graphWidget)
    graphicsView.setScene(scene)
    graphicsView.show()


class Ui_Dialog(object):
    #Create UI elements
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1118, 864)
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(70, 50, 151, 41))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(lambda: self.open_dialog(Dialog, self.graphicsView_3, self.graphicsView_4))
        self.gridLayoutWidget = QtWidgets.QWidget(Dialog)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(299, 10, 801, 841))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.graphicsView_2 = QtWidgets.QGraphicsView(self.gridLayoutWidget)
        self.graphicsView_2.setObjectName("graphicsView_2")
        self.gridLayout.addWidget(self.graphicsView_2, 1, 1, 1, 1)
        self.graphicsView_3 = QtWidgets.QGraphicsView(self.gridLayoutWidget)
        self.graphicsView_3.setObjectName("graphicsView_3")
        self.gridLayout.addWidget(self.graphicsView_3, 1, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 1, 1, 1)
        self.graphicsView_4 = QtWidgets.QGraphicsView(self.gridLayoutWidget)
        self.graphicsView_4.setObjectName("graphicsView_4")
        self.gridLayout.addWidget(self.graphicsView_4, 3, 0, 1, 1)
        self.graphicsView = QtWidgets.QGraphicsView(self.gridLayoutWidget)
        self.graphicsView.setObjectName("graphicsView")
        self.gridLayout.addWidget(self.graphicsView, 3, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setMouseTracking(False)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 2, 1, 1, 1)
        self.formLayoutWidget = QtWidgets.QWidget(Dialog)
        self.formLayoutWidget.setGeometry(QtCore.QRect(30, 130, 251, 71))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.label_5 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_5.setObjectName("label_5")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_5)
        self.label_6 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_6.setObjectName("label_6")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_6)
        self.spinBox_2 = QtWidgets.QDoubleSpinBox(self.formLayoutWidget)
        self.spinBox_2.setObjectName("spinBox_2")
        self.spinBox_2.setValue(1)
        self.spinBox_2.setMinimum(0.01)
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.spinBox_2)
        self.spinBox = QtWidgets.QDoubleSpinBox(self.formLayoutWidget)
        self.spinBox.setObjectName("spinBox")
        self.spinBox.setValue(1)
        self.spinBox.setMinimum(0.01)
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.spinBox)
        self.comboBox = QtWidgets.QComboBox(Dialog)
        self.comboBox.setGeometry(QtCore.QRect(30, 240, 241, 31))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItems(['Pixel replication', 'Bicubic Interpolation'])
        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(70, 300, 151, 41))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(lambda: self.scaleImage(self.graphicsView_2, self.graphicsView))
        self.label_7 = QtWidgets.QLabel(Dialog)
        self.label_7.setGeometry(QtCore.QRect(50, 530, 211, 51))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.lcdNumber = QtWidgets.QLCDNumber(Dialog)
        self.lcdNumber.setGeometry(QtCore.QRect(40, 600, 221, 101))
        self.lcdNumber.setObjectName("lcdNumber")
        self.pushButton_3 = QtWidgets.QPushButton(Dialog)
        self.pushButton_3.setGeometry(QtCore.QRect(70, 480, 151, 41))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.clicked.connect(lambda: self.rescaleImage(self.graphicsView_2, self.graphicsView))

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "PNI Project"))
        self.pushButton.setText(_translate("Dialog", "Select image"))
        self.label_2.setText(_translate("Dialog", "Scaled Image"))
        self.label.setText(_translate("Dialog", "Original Image"))
        self.label_3.setText(_translate("Dialog", "Histogram of the original image"))
        self.label_4.setText(_translate("Dialog", "Histogram of the scaled image"))
        self.label_5.setText(_translate("Dialog", "Width factor"))
        self.label_6.setText(_translate("Dialog", "Height factor"))
        self.pushButton_2.setText(_translate("Dialog", "Size Image"))
        self.label_7.setText(_translate("Dialog", "Mean Squared Error"))
        self.pushButton_3.setText(_translate("Dialog", "Resize Image"))

    def open_dialog(self, Dialog, graphicsView1, graphicsView2):
        file_path = QtWidgets.QFileDialog.getOpenFileName(
            Dialog,
            "Open File",
            "${HOME}",
            "PNG Files (*.png)",
        )
        global file_name, image
        file_name = file_path[0].split('/').pop()
        # verify if any png image was selected
        if file_name.find('.png') == -1:
            return
        image = cv2.imread(file_name, 0)
        plot_image(image, graphicsView1)

        # Plot histogram
        graph_histogram(graphicsView2, image)

    def scaleImage(self, graphicsView1, graphicsView2):
        global file_name, width_factor, height_factor, sized_image, image
        if file_name == "":
            return
        image = cv2.imread(file_name, 0)
        width_factor = self.spinBox.value()
        height_factor = self.spinBox_2.value()
        method = self.comboBox.currentText()
        resizeImage = ResizeImage.ResizeImage(height_factor, width_factor, image)
        if method == 'Pixel replication':
            sized_image = resizeImage.pixelReplication()
        else:
            sized_image = resizeImage.bicubicInterpolation()

        # Plot sized image
        plot_image(sized_image, graphicsView1)

        # Plot histogram
        graph_histogram(graphicsView2, sized_image)

        # Save image
        cv2.imwrite('sized_' + file_name, sized_image)

    def rescaleImage(self, graphicsView1, graphicsView2):
        global width_factor, height_factor, sized_image
        if sized_image[0][0] == 0:
            return
        resize_image = ResizeImage.ResizeImage(1 / height_factor, 1 / width_factor, sized_image)
        method = self.comboBox.currentText()
        if method == 'Pixel replication':
            rescaled_image = resize_image.pixelReplication()
        else:
            rescaled_image = resize_image.bicubicInterpolation()

        # Plot rescaled image
        plot_image(rescaled_image, graphicsView1)

        # Plot histogram
        graph_histogram(graphicsView2, rescaled_image)

        # calculate MSE
        mse = np.square(np.subtract(image, rescaled_image)).mean()
        self.lcdNumber.display(mse)

        # Save image
        cv2.imwrite('resized_' + file_name, rescaled_image)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
