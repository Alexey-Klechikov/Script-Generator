from PyQt5 import QtCore, QtGui, QtWidgets
import os, math
import pyqtgraph as pg

# min steps for slits and motors
s1hg_minimum_step = 0.05
s2hg_minimum_step = 0.01
th_minimum_step = 0.005

plot_time = []
plot_th = []
plot_s1hg = []
plot_s2hg = []

class step:
    def __init__(self, th, s1hg, s1hg_temp, s2hg, s2hg_temp, time):
        self.th = th
        self.s1hg = s1hg
        self.s1hg_temp = s1hg_temp
        self.s2hg = s2hg
        self.s2hg_temp = s2hg_temp
        self.time = time

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(699, 830)
        MainWindow.setMinimumSize(QtCore.QSize(699, 830))
        MainWindow.setMaximumSize(QtCore.QSize(699, 830))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Dropbox/Work. ILL/Python/Project - Script Generator/Icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(10, 10, 671, 180))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableWidget.sizePolicy().hasHeightForWidth())
        self.tableWidget.setSizePolicy(sizePolicy)
        self.tableWidget.setMinimumSize(QtCore.QSize(1, 1))
        self.tableWidget.setMaximumSize(QtCore.QSize(911, 180))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.tableWidget.setFont(font)
        self.tableWidget.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.tableWidget.setAutoFillBackground(False)
        self.tableWidget.setInputMethodHints(QtCore.Qt.ImhNone)
        self.tableWidget.setFrameShape(QtWidgets.QFrame.Box)
        self.tableWidget.setFrameShadow(QtWidgets.QFrame.Raised)
        self.tableWidget.setMidLineWidth(0)
        self.tableWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tableWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tableWidget.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
        self.tableWidget.setTextElideMode(QtCore.Qt.ElideMiddle)
        self.tableWidget.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerItem)
        self.tableWidget.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerItem)
        self.tableWidget.setShowGrid(True)
        self.tableWidget.setGridStyle(QtCore.Qt.SolidLine)
        self.tableWidget.setWordWrap(False)
        self.tableWidget.setCornerButtonEnabled(True)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setRowCount(5)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        item.setText("time per step (s)")
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(0, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(0, 1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(0, 2, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(0, 3, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(0, 4, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(1, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(1, 1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(1, 2, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(1, 3, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(1, 4, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(2, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(2, 1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(2, 2, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(2, 3, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(2, 4, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(3, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(3, 1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(3, 2, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(3, 3, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(3, 4, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(4, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(4, 1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(4, 2, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(4, 3, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(4, 4, item)
        self.tableWidget.horizontalHeader().setVisible(True)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(120)
        self.tableWidget.horizontalHeader().setHighlightSections(True)
        self.tableWidget.horizontalHeader().setMinimumSectionSize(1)
        self.tableWidget.horizontalHeader().setSortIndicatorShown(True)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.verticalHeader().setVisible(True)
        self.tableWidget.verticalHeader().setCascadingSectionResizes(True)
        self.tableWidget.verticalHeader().setDefaultSectionSize(30)
        self.tableWidget.verticalHeader().setHighlightSections(True)
        self.tableWidget.verticalHeader().setMinimumSectionSize(30)
        self.tableWidget.verticalHeader().setSortIndicatorShown(False)
        self.tableWidget.verticalHeader().setStretchLastSection(False)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(570, 195, 115, 61))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(10, 200, 411, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lineEdit_2.setFont(font)
        self.lineEdit_2.setText("")
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.toolButton = QtWidgets.QToolButton(self.centralwidget)
        self.toolButton.setGeometry(QtCore.QRect(430, 200, 31, 31))
        self.toolButton.setObjectName("toolButton")
        self.graphicsView_1 = pg.PlotWidget(self.centralwidget)
        self.graphicsView_1.setGeometry(QtCore.QRect(10, 280, 671, 241))
        self.graphicsView_1.setObjectName("graphicsView_1")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(240, 250, 251, 20))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.graphicsView_2 = pg.PlotWidget(self.centralwidget)
        self.graphicsView_2.setGeometry(QtCore.QRect(10, 560, 671, 241))
        self.graphicsView_2.setObjectName("graphicsView_2")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(230, 520, 301, 41))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 699, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "SuperADAM Script Generator"))
        item = self.tableWidget.verticalHeaderItem(0)
        item.setText(_translate("MainWindow", "1"))
        item = self.tableWidget.verticalHeaderItem(1)
        item.setText(_translate("MainWindow", "2"))
        item = self.tableWidget.verticalHeaderItem(2)
        item.setText(_translate("MainWindow", "3"))
        item = self.tableWidget.verticalHeaderItem(3)
        item.setText(_translate("MainWindow", "4"))
        item = self.tableWidget.verticalHeaderItem(4)
        item.setText(_translate("MainWindow", "5"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "th (degrees)"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "s1hg (mm)"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "s2hg (mm)"))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "number of points"))
        __sortingEnabled = self.tableWidget.isSortingEnabled()
        self.tableWidget.setSortingEnabled(False)
        item = self.tableWidget.item(0, 0)
        item.setText(_translate("MainWindow", "0:2"))
        item = self.tableWidget.item(0, 1)
        item.setText(_translate("MainWindow", "0.5:1"))
        item = self.tableWidget.item(0, 2)
        item.setText(_translate("MainWindow", "1"))
        item = self.tableWidget.item(0, 3)
        item.setText(_translate("MainWindow", "5:60"))
        item = self.tableWidget.item(0, 4)
        item.setText(_translate("MainWindow", "50"))
        self.tableWidget.setSortingEnabled(__sortingEnabled)
        self.pushButton.setText(_translate("MainWindow", "Create"))
        self.lineEdit_2.setPlaceholderText(_translate("MainWindow", "Save directory and file name"))
        self.toolButton.setText(_translate("MainWindow", "..."))
        self.label.setText(_translate("MainWindow", "th (degrees) vs Time per step (s)"))
        self.label_2.setText(_translate("MainWindow", "th (degrees) vs s1hg (mm), s2hg (mm)"))

         # Status bar
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        self.statusbar.showMessage("Total time to execute script is approximately: ")
        MainWindow.setStatusBar(self.statusbar)

        self.pushButton.clicked.connect(self.create_button_click)
        self.toolButton.clicked.connect(self.button_SaveDir)

    def button_SaveDir(self):
        saveAt = QtWidgets.QFileDialog().getExistingDirectory()
        if not saveAt: return
        self.lineEdit_2.setText(str(saveAt) + "/Script.dat")
        self.lineEdit_2.setText(self.lineEdit_2.text().replace("//", "/"))

    def create_button_click(self):
        self.graphicsView_1.getPlotItem().clear()
        self.graphicsView_2.getPlotItem().clear()
        plot_time.clear()
        plot_th.clear()
        plot_s1hg.clear()
        plot_s2hg.clear()

        last_values = [99, 0, 0, 0]  # th s1hg s2hg total_time - this is needed to "connect" segments if more than 1 is needed

        if not self.lineEdit_2.text(): return

        # write the first line with motor names and erase file if required
        script_file = open(self.lineEdit_2.text(), "w")
        script_file.write("#M th tth s1hg s2hg \n")
        script_file.close()

        # same for direct beam file
        script_file_DB = open(self.lineEdit_2.text()[:-4] + "_DB.dat", "w")
        script_file_DB.write("#M th tth s1hg s2hg \n")
        script_file_DB.close()

        # continue to write to the files
        script_file = open(self.lineEdit_2.text(), "a")
        script_file_DB = open(self.lineEdit_2.text()[:-4] + "_DB.dat", "a")

        # check number of filled segments
        notEmpty_segments = 0
        for col in range(0, 5):
            if self.tableWidget.item(col,0).text().find(":") > 0:
                notEmpty_segments += 1

        for segment_number in range(0, notEmpty_segments):

            th = self.tableWidget.item(segment_number,0).text()
            s1hg = self.tableWidget.item(segment_number,1).text()
            s2hg = self.tableWidget.item(segment_number,2).text()
            time_per_step = self.tableWidget.item(segment_number,3).text()
            number_of_points = self.tableWidget.item(segment_number,4).text()
            segment = []

            step.th = float(th[:th.find(":")])
            th_step = (float(th[th.find(":") + 1:]) - step.th) / float(number_of_points)
            if abs(th_step) <= th_minimum_step:  # adjust number of points and th step if required th step is less than minimum possible
                th_step = math.copysign(th_minimum_step, th_step)
                number_of_points = (float(th[th.find(":") + 1:]) - step.th) / th_minimum_step  #

            if s1hg.find(":") >= 0:
                step.s1hg = step.s1hg_temp = float(s1hg[:s1hg.find(":")])
                s1hg_step = (float(s1hg[s1hg.find(":") + 1:]) - step.s1hg) / float(number_of_points)
            else:
                step.s1hg = step.s1hg_temp = float(s1hg)
                s1hg_step = 0

            if s2hg.find(":") >= 0:
                step.s2hg = step.s2hg_temp = float(s2hg[:s2hg.find(":")])
                s2hg_step = (float(s2hg[s2hg.find(":") + 1:]) - step.s2hg) / float(number_of_points)
            else:
                step.s2hg = step.s2hg_temp = float(s2hg)
                s2hg_step = 0

            if time_per_step.find(":") >= 0:
                step.time = round(float(time_per_step[:time_per_step.find(":")]), 1)
                time_per_step_step = (float(time_per_step[time_per_step.find(":") + 1:]) - step.time) / float(number_of_points)
            else:
                step.time = round(float(time_per_step), 1)
                time_per_step_step = 0

            if round(last_values[0], 2) != round(step.th, 2): segment.append(
                [step.th, 2 * step.th, step.s1hg, step.s2hg, step.time])  # connect 2 segments without repeat the same th angle

            i = 0
            while i != int(number_of_points):  # create 2dimentional list for current segment
                step.th = step.th + th_step
                step.time = step.time + time_per_step_step
                step.s1hg_temp = step.s1hg_temp + s1hg_step
                # if step size for s1hg is less than minimum possible for motor, than we need skip this move
                if abs(step.s1hg_temp - step.s1hg) > s1hg_minimum_step: step.s1hg = step.s1hg_temp
                step.s2hg_temp = step.s2hg_temp + s2hg_step
                # if step size for s2hg is less than minimum possible for motor, than we need skip this move
                if abs(step.s2hg_temp - step.s2hg) > s2hg_minimum_step: step.s2hg = step.s2hg_temp
                # add new line for scanning
                segment.append([round(step.th, 3), 2 * round(step.th, 3), round(step.s1hg, 2), round(step.s2hg, 2), round(step.time, 1)])

                last_values[3] += segment[i][4] + 4  # total time for the scan
                i += 1

            for segment_record in segment:
                # write to script file
                script_file.write(
                    str(segment_record[0]) + " " + str(segment_record[1]) + " " + str(segment_record[2]) + " " + str(segment_record[3]) + " " + str(segment_record[4]) + "\n")
                # write to DB script file
                if segment_record[2] != last_values[1] or segment_record[3] != last_values[2]:
                    script_file_DB.write("0 0 " + str(segment_record[2]) + " " + str(segment_record[3]) + " 10" + "\n")
                    last_values[1] = segment_record[2]  # s1hg
                    last_values[2] = segment_record[3]  # s2hg
                last_values[0] = segment_record[0]  # th

                plot_time.append(segment_record[4])
                plot_th.append(segment_record[0])
                plot_s1hg.append(segment_record[2])
                plot_s2hg.append(segment_record[3])

        script_file.close()
        script_file_DB.close()

        try:
            os.rename(self.lineEdit_2.text()[:-4] + "_DB.dat",
                      self.lineEdit_2.text()[:-4] + "_" + str(round(last_values[3] / 60, 2)) + "min_DB.dat")
        except WindowsError:  # check if there already is a file with the same name in the folder -> overwrite then
            os.remove(self.lineEdit_2.text()[:-4] + "_" + str(round(last_values[3] / 60, 2)) + "min_DB.dat")
            os.rename(self.lineEdit_2.text()[:-4] + "_DB.dat",
                      self.lineEdit_2.text()[:-4] + "_" + str(round(last_values[3] / 60, 2)) + "min_DB.dat")


        try:
            os.rename(self.lineEdit_2.text(), self.lineEdit_2.text()[:-4] + "_" + str(round(last_values[3] / 60, 2)) + "min.dat")

        except WindowsError:  # check if there already is a file with the same name in the folder -> overwrite then
            os.remove(self.lineEdit_2.text()[:-4] + "_" + str(round(last_values[3] / 60, 2)) + "min.dat")
            os.rename(self.lineEdit_2.text(), self.lineEdit_2.text()[:-4] + "_" + str(round(last_values[3] / 60, 2)) + "min.dat")

        self.draw()

        self.statusbar.showMessage("Total time to execute script is approximately: " + str(round(last_values[3] / 60, 2)) + "min")

    def draw(self):
        s1 = pg.ScatterPlotItem(x=plot_th, y=plot_time, symbol="o", size=5, pen=pg.mkPen(0.2), brush=pg.mkBrush(0.7))
        self.graphicsView_1.addItem(s1)
        s2 = pg.ScatterPlotItem(x=plot_th, y=plot_s1hg, symbol="o", size=5, pen=pg.mkPen(0.8), brush=pg.mkBrush(0.1))
        self.graphicsView_2.addItem(s2)
        s3 = pg.ScatterPlotItem(x=plot_th, y=plot_s2hg, symbol="o", size=5, pen=pg.mkPen(0.2), brush=pg.mkBrush(0.7))
        self.graphicsView_2.addItem(s3)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

