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

class Ui_MainWindow(QtWidgets.QMainWindow):

    def setupUi(self, MainWindow):

        # Fonts
        font_headline = QtGui.QFont()
        font_headline.setPointSize(13)
        font_headline.setBold(True)

        font_graphs = QtGui.QFont()
        font_graphs.setPixelSize(10)
        font_graphs.setBold(False)

        font_ee = QtGui.QFont()
        font_ee.setPointSize(11)
        font_ee.setBold(False)

        # Background and foreground for graphs
        pg.setConfigOption('background', (255, 255, 255))
        pg.setConfigOption('foreground', 'k')

        # Main Window
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(500, 790)
        MainWindow.setMinimumSize(QtCore.QSize(500, 790))
        MainWindow.setMaximumSize(QtCore.QSize(500, 790))
        MainWindow.setWindowTitle("pySAgen")
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
        self.tableWidget.setRowCount(5)

        # Checkboxes
        self.checkBox_Create_DB_file = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_Create_DB_file.setFont(font_ee)
        self.checkBox_Create_DB_file.setGeometry(QtCore.QRect(5, 147, 150, 16))
        self.checkBox_Create_DB_file.setObjectName("checkBox_Create_DB_file")
        self.checkBox_Create_DB_file.setText("Create script for DB")
        self.checkBox_Create_DB_file.setVisible(False)
        self.checkBox_Create_DB_file.setChecked(False)
        self.checkBox_Slits_s1hg = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_Slits_s1hg.setFont(font_ee)
        self.checkBox_Slits_s1hg.setGeometry(QtCore.QRect(5, 127, 120, 16))
        self.checkBox_Slits_s1hg.setObjectName("checkBox_Slits_s1hg")
        self.checkBox_Slits_s1hg.setText("s1hg")
        self.checkBox_Slits_s1hg.setChecked(False)
        self.checkBox_Slits_s2hg = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_Slits_s2hg.setFont(font_ee)
        self.checkBox_Slits_s2hg.setGeometry(QtCore.QRect(60, 127, 120, 16))
        self.checkBox_Slits_s2hg.setObjectName("checkBox_Slits_s2hg")
        self.checkBox_Slits_s2hg.setText("s2hg")
        self.checkBox_Slits_s2hg.setChecked(False)

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
        self.label_th_vs_time.setGeometry(QtCore.QRect(140, 158, 219, 31))
        self.label_th_vs_time.setFont(font_headline)
        self.label_th_vs_time.setObjectName("label_th_vs_time")
        self.label_th_vs_time.setText("th (degrees) vs Time per step (s)")
        self.groupBox_th_vs_time = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_th_vs_time.setGeometry(QtCore.QRect(5, 170, 490, 290))
        self.groupBox_th_vs_time.setTitle("")
        self.groupBox_th_vs_time.setObjectName("groupBox_th_vs_time")
        self.graphicsView_th_vs_time = pg.PlotWidget(self.centralwidget, view=pg.PlotItem(viewBox=pg.ViewBox()))
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
        self.graphicsView_th_vs_s1hg_s2hg = pg.PlotWidget(self.centralwidget, view=pg.PlotItem(viewBox=pg.ViewBox()))
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
        self.actionVersion.setText("Version 1.1")
        self.menuHelp.addAction(self.actionVersion)
        self.menubar.addAction(self.menuHelp.menuAction())

        # StatusBar
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.statusbar.showMessage("Total time to execute script is approximately: ")

class GUI(Ui_MainWindow):

    current_dir = ""
    for i in sys.argv[0].split("/")[:-4]: current_dir += i + "/"

    def __init__(self):
        super(GUI, self).__init__()
        self.setupUi(self)

        self.change_interface()

        # Triggers
        self.pushButton_create.clicked.connect(self.buttons_click)
        self.pushButton_preview.clicked.connect(self.buttons_click)

        self.checkBox_Slits_s1hg.stateChanged.connect(self.change_interface)
        self.checkBox_Slits_s2hg.stateChanged.connect(self.change_interface)

        self.actionVersion.triggered.connect(self.menu_info)

    def buttons_click(self):

        plot_time.clear()
        plot_th.clear()
        plot_s1hg.clear()
        plot_s2hg.clear()

        for i in self.graphicsView_th_vs_time.getPlotItem().listDataItems(): self.graphicsView_th_vs_time.getPlotItem().removeItem(i)
        for i in self.graphicsView_th_vs_s1hg_s2hg.getPlotItem().listDataItems(): self.graphicsView_th_vs_s1hg_s2hg.getPlotItem().removeItem(i)

        # th s1hg s2hg total_time - this is needed to "connect" segments if more than 1 is needed
        last_values = [99, 0, 0, 0]
        motors_string_last = ""
        # check users input and number of filled segments
        not_allowed_symbols = re.compile(r'[^0-9:.-]')

        notEmpty_segments = 0
        for col in range(0, self.tableWidget.columnCount()):

            notEmpty_segments += [1 if self.tableWidget.item(col, 0).text().find(":") > 0 else 0][0]

            for row in range(0, self.tableWidget.rowCount()-2):
                if not_allowed_symbols.findall(self.tableWidget.item(col, row).text()):
                    self.statusbar.showMessage("Recheck your input for typos in the segment " + str(col+1) + ".")
                    return

        for segment_number in range(0, notEmpty_segments):

            th = self.tableWidget.item(segment_number, 0).text()

            column_number_if_slits = 0
            if self.checkBox_Slits_s1hg.isChecked():
                s1hg, column_number_if_slits = self.tableWidget.item(segment_number, 1).text(), 1
                if self.checkBox_Slits_s2hg.isChecked(): s2hg, column_number_if_slits = self.tableWidget.item(segment_number, 2).text(), 2
            elif self.checkBox_Slits_s2hg.isChecked(): s2hg, column_number_if_slits = self.tableWidget.item(segment_number, 1).text(), 1

            time_per_step = self.tableWidget.item(segment_number, column_number_if_slits + 1).text()
            number_of_points = self.tableWidget.item(segment_number, column_number_if_slits + 2).text()

            segment = []

            step.th = float(th[:th.find(":")])
            th_step = (float(th[th.find(":") + 1:]) - step.th) / float(number_of_points)
            if abs(th_step) <= th_minimum_step:  # adjust number of points and th step if required th step is less than minimum possible
                th_step = math.copysign(th_minimum_step, th_step)
                number_of_points = (float(th[th.find(":") + 1:]) - step.th) / th_minimum_step  #

            if self.checkBox_Slits_s1hg.isChecked():
                if s1hg.find(":") >= 0:
                    step.s1hg = step.s1hg_temp = float(s1hg[:s1hg.find(":")])
                    s1hg_step = (float(s1hg[s1hg.find(":") + 1:]) - step.s1hg) / float(number_of_points)
                else:
                    step.s1hg = step.s1hg_temp = float(s1hg)
                    s1hg_step = 0
            else:
                step.s1hg, s1hg_step = 0, 0

            if self.checkBox_Slits_s2hg.isChecked():
                if s2hg.find(":") >= 0:
                    step.s2hg = step.s2hg_temp = float(s2hg[:s2hg.find(":")])
                    s2hg_step = (float(s2hg[s2hg.find(":") + 1:]) - step.s2hg) / float(number_of_points)
                else:
                    step.s2hg = step.s2hg_temp = float(s2hg)
                    s2hg_step = 0
            else:
                step.s2hg, s2hg_step = 0, 0

            if time_per_step.find(":") >= 0:
                step.time = round(float(time_per_step[:time_per_step.find(":")]), 1)
                time_per_step_step = (float(time_per_step[time_per_step.find(":") + 1:]) - step.time) / float(number_of_points)
            else:
                step.time = round(float(time_per_step), 1)
                time_per_step_step = 0

            if not round(last_values[0], 2) == round(step.th, 2): segment.append([step.th, 2 * step.th, step.s1hg, step.s2hg, step.time])  # connect 2 segments without repeat the same th angle

            i = 0
            while i != int(number_of_points):  # create 2D list for current segment
                step.th += th_step
                step.time += time_per_step_step
                if self.checkBox_Slits_s1hg.isChecked():
                    step.s1hg_temp += s1hg_step
                    # if step size for s1hg is less than minimum possible for motor, than we need skip this move
                    if abs(step.s1hg_temp - step.s1hg) > s1hg_minimum_step: step.s1hg = step.s1hg_temp
                if self.checkBox_Slits_s2hg.isChecked():
                    step.s2hg_temp += s2hg_step
                    # if step size for s2hg is less than minimum possible for motor, than we need skip this move
                    if abs(step.s2hg_temp - step.s2hg) > s2hg_minimum_step: step.s2hg = step.s2hg_temp
                # add new line for scanning
                segment.append([round(step.th, 3), 2 * round(step.th, 3), round(step.s1hg, 2), round(step.s2hg, 2), round(step.time, 1)])

                last_values[3] += segment[i][4] + 4  # total time for the scan
                i += 1

            for segment_record in segment:
                plot_time.append(segment_record[4])
                plot_th.append(segment_record[0])
                if self.checkBox_Slits_s1hg.isChecked(): plot_s1hg.append(segment_record[2])
                if self.checkBox_Slits_s2hg.isChecked(): plot_s2hg.append(segment_record[3])

        self.s1 = pg.ScatterPlotItem(x=plot_th, y=plot_time, symbol="o", size=5, pen=pg.mkPen(0.2), brush=pg.mkBrush(0.7))
        self.graphicsView_th_vs_time.addItem(self.s1)
        if self.checkBox_Slits_s1hg.isChecked():
            self.s2 = pg.ScatterPlotItem(x=plot_th, y=plot_s1hg, symbol="o", size=5, pen=pg.mkPen(0.8), brush=pg.mkBrush(0.1))
            self.graphicsView_th_vs_s1hg_s2hg.addItem(self.s2)
        if self.checkBox_Slits_s2hg.isChecked():
            self.s3 = pg.ScatterPlotItem(x=plot_th, y=plot_s2hg, symbol="o", size=5, pen=pg.mkPen(0.2), brush=pg.mkBrush(0.7))
            self.graphicsView_th_vs_s1hg_s2hg.addItem(self.s3)


        if int((round(last_values[3] // 3600, 2))) == 0:
            time = str(int(round(last_values[3] / 60))) + " min."
        else: time = str(int(round(last_values[3] // 3600))) + "h " + str(int(round((last_values[3] % 3600)/60))) + "min (" + (str(int(round(last_values[3] / 60)))) + " min)."

        self.statusbar.showMessage("Total time to execute script is approximately: " + time)

        if self.sender().objectName() == "pushButton_create":

            last_values = [99, 0, 0, last_values[3]]

            saveAt_dir = QtWidgets.QFileDialog().getExistingDirectory()
            if not saveAt_dir: return

            # write the first line with motor names and erase file if required
            FILE_SCRIPT = open(saveAt_dir + "/Script_" + str(int(round(last_values[3] // 60))) + "_min.dat", "w")
            if self.checkBox_Slits_s1hg.isChecked() and self.checkBox_Slits_s2hg.isChecked(): motors_string_header = "#M th tth s1hg s2hg \n"
            elif self.checkBox_Slits_s1hg.isChecked(): motors_string_header = "#M th tth s1hg \n"
            elif self.checkBox_Slits_s2hg.isChecked(): motors_string_header = "#M th tth s2hg \n"
            else: motors_string_header = "#M th tth \n"
            FILE_SCRIPT.write(motors_string_header)

            # same for direct beam file (if required)
            if self.checkBox_Create_DB_file.isChecked():
                FILE_DB = open(saveAt_dir + "/Script_" + str(int(round(last_values[3] // 60, 2))) + "_min_DB.dat", "w")
                FILE_DB.write(motors_string_header)

            for i, plot_th_i in enumerate(plot_th):

                # write to script file
                if self.checkBox_Slits_s1hg.isChecked() and self.checkBox_Slits_s2hg.isChecked():
                    motors_string = str(plot_th_i) + " " + str(plot_th_i*2) + " " + str(plot_s1hg[i]) + " " + str(plot_s2hg[i]) + " " + str(plot_time[i]) + "\n"
                    motors_string_DB = "0 0 " + str(plot_s1hg[i]) + " " + str(plot_s2hg[i]) + " 10" + "\n"
                elif self.checkBox_Slits_s1hg.isChecked():
                    motors_string = str(plot_th_i) + " " + str(plot_th_i*2) + " " + str(plot_s1hg[i]) + " " +  str(plot_time[i]) + "\n"
                    motors_string_DB = "0 0 " + str(plot_s1hg[i]) + " 10" + "\n"
                elif self.checkBox_Slits_s2hg.isChecked():
                    motors_string = str(plot_th_i) + " " + str(plot_th_i*2) + " " + str(plot_s2hg[i]) + " " + str(plot_time[i]) + "\n"
                    motors_string_DB = "0 0 " + str(plot_s2hg[i]) + " 10" + "\n"
                else: motors_string = str(plot_th_i) + " " + str(plot_th_i*2) + " " + str(plot_time[i]) + "\n"

                if not motors_string_last == motors_string:
                    FILE_SCRIPT.write(motors_string)
                motors_string_last = motors_string

                # write to DB script file
                if self.checkBox_Create_DB_file.isChecked() and (not plot_s1hg[i] == last_values[1] or not plot_s2hg[i] == last_values[2]):
                    FILE_DB.write(motors_string_DB)
                    last_values[1], last_values[2] = plot_s1hg[i], plot_s2hg[i]  # s1hg s2hg

            FILE_SCRIPT.close()
            if self.checkBox_Create_DB_file.isChecked(): FILE_DB.close()

    def change_interface(self):

        self.statusbar.showMessage("")

        if self.checkBox_Slits_s1hg.isChecked():
            self.tableWidget.setColumnCount(4)

            column_names = ["th (degree)", "s1hg (mm)", "time per step (s)", "number of points"]
            column_widths = [105, 105, 130, 137]
            default_line = ["0:2", "0.5:1", "5:60", "50"]

            self.MW_size = 790
            self.label_th_vs_s1hg_s2hg.setText("th (degrees) vs s1hg (mm)")
            self.label_th_vs_s1hg_s2hg.setGeometry(QtCore.QRect(165, 465, 261, 31))
            self.checkBox_Create_DB_file.setVisible(True)

        if self.checkBox_Slits_s2hg.isChecked():
            self.tableWidget.setColumnCount(4)

            column_names = ["th (degree)", "s2hg (mm)", "time per step (s)", "number of points"]
            column_widths = [105, 105, 130, 137]
            default_line = ["0:2", "0.5:1", "5:60", "50"]

            self.MW_size = 790
            self.label_th_vs_s1hg_s2hg.setText("th (degrees) vs s2hg (mm)")
            self.label_th_vs_s1hg_s2hg.setGeometry(QtCore.QRect(165, 465, 261, 31))
            self.checkBox_Create_DB_file.setVisible(True)

        if self.checkBox_Slits_s1hg.isChecked() and self.checkBox_Slits_s2hg.isChecked():
            self.tableWidget.setColumnCount(5)

            column_names = ["th (degree)", "s1hg (mm)", "s2hg (mm)", "time per step (s)", "number of points"]
            column_widths = [80, 85, 85, 110, 117]
            default_line = ["0:2", "0.5:1", "1", "5:60", "50"]

            self.MW_size = 790
            self.label_th_vs_s1hg_s2hg.setText("th (degree) vs s1hg (mm), s2hg (mm)")
            self.label_th_vs_s1hg_s2hg.setGeometry(QtCore.QRect(130, 465, 261, 31))
            self.checkBox_Create_DB_file.setVisible(True)

        if not self.checkBox_Slits_s1hg.isChecked() and not self.checkBox_Slits_s2hg.isChecked():
            self.tableWidget.setColumnCount(3)

            column_names = ["th (degrees)", "time per step (s)", "number of points"]
            column_widths = [143, 163, 171]
            default_line = ["0:2", "5:60", "50"]

            self.MW_size = 500
            self.checkBox_Create_DB_file.setVisible(False)

        self.resize(500, self.MW_size)
        self.setMinimumSize(QtCore.QSize(500, self.MW_size))
        self.setMaximumSize(QtCore.QSize(500, self.MW_size))

        for i in range(0, self.tableWidget.rowCount()):
            item = QtWidgets.QTableWidgetItem()
            item.setText(str(i + 1))
            self.tableWidget.setVerticalHeaderItem(i, item)
            item = QtWidgets.QTableWidgetItem()
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget.setRowHeight(i, 1)

            for j in range(0, self.tableWidget.columnCount()):
                item = QtWidgets.QTableWidgetItem()
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                item.setText(column_names[j])
                self.tableWidget.setColumnWidth(j, column_widths[j])
                self.tableWidget.setHorizontalHeaderItem(j, item)

                item = QtWidgets.QTableWidgetItem()
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                if i == 0: item.setText(default_line[j])
                self.tableWidget.setItem(i, j, item)

    def menu_info(self):

        msgBox = QtWidgets.QMessageBox()
        msgBox.setText("pySAgen V1.1\n\n"
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

