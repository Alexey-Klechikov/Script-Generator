from PyQt5 import QtCore, QtGui, QtWidgets
import os, math, re
import pyqtgraph as pg

QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

current_dir = os.path.dirname(os.path.realpath(__file__)).replace("\\", "/")

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

class Ui_MainWindow(QtGui.QMainWindow):

    def setupUi(self, MainWindow):

        # Fonts
        font_headline = QtGui.QFont()
        font_headline.setPointSize(10)
        font_headline.setBold(True)

        font_graphs = QtGui.QFont()
        font_graphs.setPixelSize(10)
        font_graphs.setBold(False)

        font_graphs_2 = QtGui.QFont()
        font_graphs_2.setPixelSize(1)
        font_graphs_2.setBold(False)

        font_ee = QtGui.QFont()
        font_ee.setPointSize(9)
        font_ee.setBold(False)

        # Background and foreground for graphs
        pg.setConfigOption('background', (255, 255, 255))
        pg.setConfigOption('foreground', 'k')

        # Main Window
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(500, 810)
        MainWindow.setMinimumSize(QtCore.QSize(500, 810))
        MainWindow.setMaximumSize(QtCore.QSize(500, 810))
        MainWindow.setWindowTitle("pySAgen")
        MainWindow.setWindowIcon(QtGui.QIcon(self.current_dir + "\icon.png"))
        MainWindow.setIconSize(QtCore.QSize(30, 30))

        # Block: Table
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(5, 5, 490, 118))
        self.tableWidget.setFont(font_ee)
        self.tableWidget.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.tableWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tableWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setRowCount(5)
        for i in range(0, 5):
            item = QtWidgets.QTableWidgetItem()
            item.setText(str(i+1))
            self.tableWidget.setVerticalHeaderItem(i, item)
            item = QtWidgets.QTableWidgetItem()
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            if i == 0:
                item.setText("th (degrees)")
                self.tableWidget.setColumnWidth(i, 80)
            elif i == 1:
                item.setText("s1hg (mm)")
                self.tableWidget.setColumnWidth(i, 85)
            elif i == 2:
                item.setText("s2hg (mm)")
                self.tableWidget.setColumnWidth(i, 85)
            elif i == 3:
                item.setText("time per step (s)")
                self.tableWidget.setColumnWidth(i, 110)
            elif i == 4:
                item.setText("number of points")
                self.tableWidget.setColumnWidth(i, int(self.tableWidget.width()) - int(self.tableWidget.columnWidth(0)) - int(self.tableWidget.columnWidth(1)) - int(self.tableWidget.columnWidth(2)) - int(self.tableWidget.columnWidth(3)) - 13)
            self.tableWidget.setHorizontalHeaderItem(i, item)

            for j in range(0, 5):
                item = QtWidgets.QTableWidgetItem()
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                if i == 0:
                    if j == 0: item.setText("0:2")
                    elif j == 1: item.setText("0.5:1")
                    elif j == 2: item.setText("1")
                    elif j == 3: item.setText("5:60")
                    elif j == 4: item.setText("50")
                self.tableWidget.setItem(i, j, item)

            self.tableWidget.setRowHeight(i, 15)

        # Button: Create
        self.pushButton_create = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_create.setGeometry(QtCore.QRect(425, 150, 70, 22))
        self.pushButton_create.setFont(font_headline)
        self.pushButton_create.setObjectName("pushButton_create")
        self.pushButton_create.setText("Create")

        # Button: Preview
        self.pushButton_preview = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_preview.setGeometry(QtCore.QRect(425, 127, 70, 22))
        self.pushButton_preview.setFont(font_headline)
        self.pushButton_preview.setObjectName("pushButton_preview")
        self.pushButton_preview.setText("Preview")

        # Graph: th vs time
        self.label_th_vs_time = QtWidgets.QLabel(self.centralwidget)
        self.label_th_vs_time.setGeometry(QtCore.QRect(160, 158, 219, 31))
        self.label_th_vs_time.setFont(font_headline)
        self.label_th_vs_time.setObjectName("label_th_vs_time")
        self.label_th_vs_time.setText("th (degrees) vs Time per step (s)")
        self.groupBox_th_vs_time = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_th_vs_time.setGeometry(QtCore.QRect(5, 170, 490, 290))
        self.groupBox_th_vs_time.setTitle("")
        self.groupBox_th_vs_time.setObjectName("groupBox_th_vs_time")
        self.graphicsView_th_vs_time = pg.PlotWidget(self.centralwidget, viewBox=pg.ViewBox())
        self.graphicsView_th_vs_time.setGeometry(QtCore.QRect(7, 189, 487, 270))
        self.graphicsView_th_vs_time.setObjectName("graphicsView_th_vs_time")
        self.graphicsView_th_vs_time.getAxis("bottom").tickFont = font_graphs
        self.graphicsView_th_vs_time.getAxis("bottom").setStyle(tickTextOffset=10)
        self.graphicsView_th_vs_time.getAxis("left").tickFont = font_graphs
        self.graphicsView_th_vs_time.getAxis("left").setStyle(tickTextOffset=10)
        self.graphicsView_th_vs_time.showAxis("top")
        self.graphicsView_th_vs_time.getAxis("top").setTicks([])
        self.graphicsView_th_vs_time.showAxis("right")
        self.graphicsView_th_vs_time.getAxis("right").setTicks([])

        # Graph: tv vs s1hg, s2hg
        self.label_th_vs_s1hg_s2hg = QtWidgets.QLabel(self.centralwidget)
        self.label_th_vs_s1hg_s2hg.setGeometry(QtCore.QRect(140, 465, 261, 31))
        self.label_th_vs_s1hg_s2hg.setFont(font_headline)
        self.label_th_vs_s1hg_s2hg.setObjectName("label_th_vs_s1hg_s2hg")
        self.label_th_vs_s1hg_s2hg.setText("th (degrees) vs s1hg (mm), s2hg (mm)")
        self.groupBox_th_vs_s1hg_s2hg = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_th_vs_s1hg_s2hg.setGeometry(QtCore.QRect(5, 477, 490, 290))
        self.groupBox_th_vs_s1hg_s2hg.setTitle("")
        self.groupBox_th_vs_s1hg_s2hg.setObjectName("groupBox_th_vs_s1hg_s2hg")
        self.graphicsView_th_vs_s1hg_s2hg = pg.PlotWidget(self.centralwidget, viewBox=pg.ViewBox())
        self.graphicsView_th_vs_s1hg_s2hg.setGeometry(QtCore.QRect(7, 496, 487, 270))
        self.graphicsView_th_vs_s1hg_s2hg.setObjectName("graphicsView_th_vs_s1hg_s2hg")
        self.graphicsView_th_vs_s1hg_s2hg.getAxis("bottom").tickFont = font_graphs
        self.graphicsView_th_vs_s1hg_s2hg.getAxis("bottom").setStyle(tickTextOffset=10)
        self.graphicsView_th_vs_s1hg_s2hg.getAxis("left").tickFont = font_graphs
        self.graphicsView_th_vs_s1hg_s2hg.getAxis("left").setStyle(tickTextOffset=10)
        self.graphicsView_th_vs_s1hg_s2hg.showAxis("top")
        self.graphicsView_th_vs_s1hg_s2hg.getAxis("top").setTicks([])
        self.graphicsView_th_vs_s1hg_s2hg.showAxis("right")
        self.graphicsView_th_vs_s1hg_s2hg.getAxis("right").setTicks([])
        self.graphicsView_th_vs_s1hg_s2hg.getViewBox().setXLink(self.graphicsView_th_vs_time)

        # MenuBar
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 699, 21))
        self.menubar.setObjectName("menubar")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        self.menuHelp.setTitle("Help")
        MainWindow.setMenuBar(self.menubar)
        self.actionAlgorithm_info = QtWidgets.QAction(MainWindow)
        self.actionAlgorithm_info.setObjectName("actionAlgorithm_info")
        self.actionVersion = QtWidgets.QAction(MainWindow)
        self.actionVersion.setObjectName("actionVersion")
        self.actionVersion.setText("Version 1.0.1")
        self.menuHelp.addAction(self.actionVersion)
        self.menubar.addAction(self.menuHelp.menuAction())

        # StatusBar
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.statusbar.showMessage("Total time to execute script is approximately: ")

class GUI(Ui_MainWindow):

    current_dir = os.getcwd().replace("\\", "/") + "/"

    def __init__(self):

        super(GUI, self).__init__()
        self.setupUi(self)

        #self.buttons_click()

        # Triggers
        self.pushButton_create.clicked.connect(self.buttons_click)
        self.pushButton_preview.clicked.connect(self.buttons_click)

        self.actionVersion.triggered.connect(self.menu_info)

    def buttons_click(self):

        plot_time.clear()
        plot_th.clear()
        plot_s1hg.clear()
        plot_s2hg.clear()

        try:
            self.graphicsView_th_vs_time.removeItem(self.s1)
            self.graphicsView_th_vs_s1hg_s2hg.removeItem(self.s2)
            self.graphicsView_th_vs_s1hg_s2hg.removeItem(self.s3)
        except:
            a = 1

        # th s1hg s2hg total_time - this is needed to "connect" segments if more than 1 is needed
        last_values = [99, 0, 0, 0]

        # check users input and number of filled segments
        not_allowed_symbols = re.compile(r'[^0-9:.]')

        notEmpty_segments = 0
        for col in range(0, 5):

            notEmpty_segments += [1 if self.tableWidget.item(col, 0).text().find(":") > 0 else 0][0]

            for row in range(0, 5):
                if not_allowed_symbols.findall(self.tableWidget.item(col, row).text()):
                    self.statusbar.showMessage("Recheck your input for typos in the segment " + str(col+1) + ".")
                    return

        for segment_number in range(0, notEmpty_segments):

            th = self.tableWidget.item(segment_number, 0).text()
            s1hg = self.tableWidget.item(segment_number, 1).text()
            s2hg = self.tableWidget.item(segment_number, 2).text()
            time_per_step = self.tableWidget.item(segment_number, 3).text()
            number_of_points = self.tableWidget.item(segment_number, 4).text()

            segment = []

            step.th = float(th[:th.find(":")])
            th_step = (float(th[th.find(":") + 1:]) - step.th) / float(number_of_points)
            if abs(
                    th_step) <= th_minimum_step:  # adjust number of points and th step if required th step is less than minimum possible
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
                time_per_step_step = (float(time_per_step[time_per_step.find(":") + 1:]) - step.time) / float(
                    number_of_points)
            else:
                step.time = round(float(time_per_step), 1)
                time_per_step_step = 0

            if round(last_values[0], 2) != round(step.th, 2): segment.append(
                [step.th, 2 * step.th, step.s1hg, step.s2hg,
                 step.time])  # connect 2 segments without repeat the same th angle

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
                segment.append([round(step.th, 3), 2 * round(step.th, 3), round(step.s1hg, 2), round(step.s2hg, 2),
                                round(step.time, 1)])

                last_values[3] += segment[i][4] + 4  # total time for the scan
                i += 1

            for segment_record in segment:
                plot_time.append(segment_record[4])
                plot_th.append(segment_record[0])
                plot_s1hg.append(segment_record[2])
                plot_s2hg.append(segment_record[3])

        self.s1 = pg.ScatterPlotItem(x=plot_th, y=plot_time, symbol="o", size=5, pen=pg.mkPen(0.2), brush=pg.mkBrush(0.7))
        self.graphicsView_th_vs_time.addItem(self.s1)
        self.s2 = pg.ScatterPlotItem(x=plot_th, y=plot_s1hg, symbol="o", size=5, pen=pg.mkPen(0.8), brush=pg.mkBrush(0.1))
        self.graphicsView_th_vs_s1hg_s2hg.addItem(self.s2)
        self.s3 = pg.ScatterPlotItem(x=plot_th, y=plot_s2hg, symbol="o", size=5, pen=pg.mkPen(0.2), brush=pg.mkBrush(0.7))
        self.graphicsView_th_vs_s1hg_s2hg.addItem(self.s3)

        if not self.statusbar.currentMessage() == "Recheck your input for typos.":
            self.statusbar.showMessage(
                "Total time to execute script is approximately: " + str(round(last_values[3] / 60, 2)) + "min")

        if self.sender().objectName() == "pushButton_create":

            last_values = [99, 0, 0, last_values[3]]

            saveAt_dir = QtWidgets.QFileDialog().getExistingDirectory()
            if not saveAt_dir: return

            # write the first line with motor names and erase file if required
            FILE_SCRIPT = open(saveAt_dir + "/Script_" + str(round(last_values[3] / 60, 2)) + "_min.dat", "w")
            FILE_SCRIPT.write("#M th tth s1hg s2hg \n")

            # same for direct beam file
            FILE_DB = open(saveAt_dir + "/Script_" + str(round(last_values[3] / 60, 2)) + "_min_DB.dat", "w")
            FILE_DB.write("#M th tth s1hg s2hg \n")

            for i, plot_th_i in enumerate(plot_th):

                # write to script file
                FILE_SCRIPT.write(
                    str(plot_th_i) + " " + str(plot_th_i*2) + " " + str(plot_s1hg[i]) + " " + str(plot_s2hg[i]) + " " + str(plot_time[i]) + "\n")

                # write to DB script file
                if not plot_s1hg[i] == last_values[1] or not plot_s2hg[i] == last_values[2]:
                    FILE_DB.write("0 0 " + str(plot_s1hg[i]) + " " + str(plot_s2hg[i]) + " 10" + "\n")

                last_values[1] = plot_s1hg[i]  # s1hg
                last_values[2] = plot_s2hg[i]  # s2hg

            FILE_SCRIPT.close()
            FILE_DB.close()

    def menu_info(self):

        msgBox = QtWidgets.QMessageBox()
        msgBox.setWindowIcon(QtGui.QIcon(current_dir + "\icon.png"))
        msgBox.setText("pySAgen V1.0.1\n\n"
                       "Alexey.Klechikov@gmail.com\n\n"
                       "Check new version at https://github.com/Alexey-Klechikov/pySAgen/releases")
        msgBox.exec_()

if __name__ == "__main__":
    import sys

    QtWidgets.QApplication.setStyle("Fusion")
    app = QtWidgets.QApplication(sys.argv)
    prog = GUI()
    prog.show()
    sys.exit(app.exec_())

