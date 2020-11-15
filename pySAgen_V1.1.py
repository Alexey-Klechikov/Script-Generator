'''
Install with:
* Windows - pyinstaller --onefile --noconsole -i"C:\icon.ico" --add-data C:\icon.ico;images C:\pySAgen_V1.1.py
* MacOS - sudo pyinstaller --onefile --windowed pySAgen_V1.1.py

Requirements for a nice interface:
* PyQt<=5.12.2
'''

from PyQt5 import QtCore, QtGui, QtWidgets
import os, math, re, sys, pkgutil, platform
import pyqtgraph as pg

QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

dir_current = os.path.dirname(os.path.realpath(__file__)).replace("\\", "/")

# min steps for slits and motors
s1hg_stepMinimum = 0.05
s2hg_stepMinimum = 0.01
th_stepMinimum = 0.005

time_plot, th_plot, s1hg_plot, s2hg_plot = [], [], [], []

class step:
    def __init__(self, th, s1hg, s1hg_temp, s2hg, s2hg_temp, time):
        self.th = th
        self.s1hg = s1hg
        self.s1hg_temp = s1hg_temp
        self.s2hg = s2hg
        self.s2hg_temp = s2hg_temp
        self.time = time

class Ui_MainWindow(QtWidgets.QMainWindow):

    # PyQt version/OS fix
    dir_current = ""
    if platform.system() == 'Windows': dir_current, offset_os = os.getcwd().replace("\\", "/") + "/", 0
    else:
        for i in sys.argv[0].split("/")[:-4]: dir_current += i + "/"
        offset_os = 2

    def __create_element(self, object, geometry, objectName, text=None, font=None, placeholder=None, visible=None, stylesheet=None, checked=None, checkable=None, title=None, combo=None, enabled=None):

        object.setObjectName(objectName)

        if not geometry == [999, 999, 999, 999]:
            object.setGeometry(QtCore.QRect(geometry[0], geometry[1], geometry[2], geometry[3]))

        if not text == None: object.setText(text)
        if not title == None: object.setTitle(title)
        if not font == None: object.setFont(font)
        if not placeholder == None: object.setPlaceholderText(placeholder)
        if not visible == None: object.setVisible(visible)
        if not checked == None: object.setChecked(checked)
        if not checkable == None: object.setCheckable(checked)
        if not enabled == None: object.setEnabled(enabled)

        if not stylesheet == None: object.setStyleSheet(stylesheet)

        if not combo == None:
            for i in combo: object.addItem(str(i))


    def setupUi(self, MainWindow):

        # Fonts
        font_headline = QtGui.QFont()
        font_headline.setPointSize(10 if platform.system() == 'Windows' else 13)
        font_headline.setBold(True)

        font_graphs = QtGui.QFont()
        font_graphs.setPixelSize(10)
        font_graphs.setBold(False)

        font_ee = QtGui.QFont()
        font_ee.setPointSize(9 if platform.system() == 'Windows' else 11)
        font_ee.setBold(False)

        # Background and foreground for graphs
        pg.setConfigOption('background', (255, 255, 255))
        pg.setConfigOption('foreground', 'k')

        # Main Window
        MainWindow_size = [500, 811] if platform.system() == 'Windows' else [500, 790]
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(MainWindow_size[0], MainWindow_size[1])
        MainWindow.setMinimumSize(QtCore.QSize(MainWindow_size[0], MainWindow_size[1]))
        MainWindow.setMaximumSize(QtCore.QSize(MainWindow_size[0], MainWindow_size[1]))
        MainWindow.setWindowTitle("pySAgen")
        # when we create .exe with pyinstaller, we need to store icon inside it. Then we find it inside unpacked temp directory.
        for i in pkgutil.iter_importers():
            path = str(i).split("'")[1].replace("\\\\", "\\") if str(i).find('FileFinder')>=0 else None
            if path != None: self.iconpath = path + "\\images\\icon.ico"
        MainWindow.setWindowIcon(QtGui.QIcon(self.iconpath))
        MainWindow.setIconSize(QtCore.QSize(30, 30))

        # Block: Table
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.__create_element(self.tableWidget, [5, 5, 490, 116], "tableWidget", font=font_ee)
        self.tableWidget.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.tableWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tableWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tableWidget.setRowCount(5)

        # Checkboxes
        self.checkBox_createDBfile = QtWidgets.QCheckBox(self.centralwidget)
        self.__create_element(self.checkBox_createDBfile, [5, 147, 150, 16], "checkBox_createDBfile", text="Create script for DB", visible=False, checked=False, font=font_ee)
        self.checkBox_slits_s1hg = QtWidgets.QCheckBox(self.centralwidget)
        self.__create_element(self.checkBox_slits_s1hg, [5, 127, 120, 16], "checkBox_slits_s1hg", text="s1hg", checked=False, font=font_ee)
        self.checkBox_slits_s2hg = QtWidgets.QCheckBox(self.centralwidget)
        self.__create_element(self.checkBox_slits_s2hg, [60, 127, 120, 16], "checkBox_slits_s2hg", text="s2hg", checked=False, font=font_ee)

        # Button: Create
        self.pushButton_create = QtWidgets.QPushButton(self.centralwidget)
        self.__create_element(self.pushButton_create, [425, 150, 70, 22], "pushButton_create", text="Create", font=font_headline)

        # Button: Preview
        self.pushButton_preview = QtWidgets.QPushButton(self.centralwidget)
        self.__create_element(self.pushButton_preview, [425, 127, 70, 22], "pushButton_preview", text="Preview", font=font_headline)

        # Graph: th vs time
        self.label_thVsTime = QtWidgets.QLabel(self.centralwidget)
        self.__create_element(self.label_thVsTime, [140, 158, 219, 31], "label_thVsTime", text="th (degrees) vs Time per step (s)", font=font_headline, stylesheet="QLabel { color : blue; }")
        self.groupBox_thVsTime = QtWidgets.QGroupBox(self.centralwidget)
        self.__create_element(self.groupBox_thVsTime, [5, 170-self.offset_os, 490, 290+self.offset_os], "groupBox_thVsTime", title="")
        self.graphicsView_thVsTime = pg.PlotWidget(self.centralwidget, view=pg.PlotItem(viewBox=pg.ViewBox()))
        self.__create_element(self.graphicsView_thVsTime, [7, 189, 487, 270], "graphicsView_thVsTime")
        self.graphicsView_thVsTime.getAxis("bottom").tickFont = font_graphs
        self.graphicsView_thVsTime.getAxis("bottom").setStyle(tickTextOffset=10)
        self.graphicsView_thVsTime.getAxis("left").tickFont = font_graphs
        self.graphicsView_thVsTime.getAxis("left").setStyle(tickTextOffset=10)
        self.graphicsView_thVsTime.showAxis("top")
        self.graphicsView_thVsTime.getAxis("top").setTicks([])
        self.graphicsView_thVsTime.showAxis("right")
        self.graphicsView_thVsTime.getAxis("right").setTicks([])

        # Graph: tv vs s1hg, s2hg
        self.label_thVsS1hgS2hg = QtWidgets.QLabel(self.centralwidget)
        self.__create_element(self.label_thVsS1hgS2hg, [140, 465, 261, 31], "label_thVsS1hgS2hg", text="th (degrees) vs s1hg (mm), s2hg (mm)", font=font_headline, stylesheet="QLabel { color : blue; }")
        self.groupBox_thVsS1hgS2hg = QtWidgets.QGroupBox(self.centralwidget)
        self.__create_element(self.groupBox_thVsS1hgS2hg, [5, 477-self.offset_os, 490, 290+self.offset_os], "groupBox_thVsS1hgS2hg", title="")
        self.graphicsView_thVsS1hgS2hg = pg.PlotWidget(self.centralwidget, view=pg.PlotItem(viewBox=pg.ViewBox()))
        self.__create_element(self.graphicsView_thVsS1hgS2hg, [7, 496, 487, 270], "graphicsView_thVsS1hgS2hg")
        self.graphicsView_thVsS1hgS2hg.getAxis("bottom").tickFont = font_graphs
        self.graphicsView_thVsS1hgS2hg.getAxis("bottom").setStyle(tickTextOffset=10)
        self.graphicsView_thVsS1hgS2hg.getAxis("left").tickFont = font_graphs
        self.graphicsView_thVsS1hgS2hg.getAxis("left").setStyle(tickTextOffset=10)
        self.graphicsView_thVsS1hgS2hg.showAxis("top")
        self.graphicsView_thVsS1hgS2hg.getAxis("top").setTicks([])
        self.graphicsView_thVsS1hgS2hg.showAxis("right")
        self.graphicsView_thVsS1hgS2hg.getAxis("right").setTicks([])
        self.graphicsView_thVsS1hgS2hg.getViewBox().setXLink(self.graphicsView_thVsTime)

        # MenuBar
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.__create_element(self.menubar, [0, 0, 699, 21], "menubar")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.__create_element(self.menuHelp, [999, 999, 999, 999], "menuHelp", title="Help")
        MainWindow.setMenuBar(self.menubar)
        self.action_algorithmInfo = QtWidgets.QAction(MainWindow)
        self.__create_element(self.action_algorithmInfo, [999, 999, 999, 999], "action_algorithmInfo")
        self.action_version = QtWidgets.QAction(MainWindow)
        self.__create_element(self.action_version, [999, 999, 999, 999], "action_version", text="Version 1.1")
        self.menuHelp.addAction(self.action_version)
        self.menubar.addAction(self.menuHelp.menuAction())

        # StatusBar
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.statusbar.showMessage("Total time to execute the script is approximately: ")

class GUI(Ui_MainWindow):
    dir_current = os.getcwd().replace("\\", "/") + "/"

    def __init__(self):
        super(GUI, self).__init__()
        self.setupUi(self)

        self.f_interface_change()

        # Triggers
        self.pushButton_create.clicked.connect(self.f_buttons_click)
        self.pushButton_preview.clicked.connect(self.f_buttons_click)

        self.checkBox_slits_s1hg.stateChanged.connect(self.f_interface_change)
        self.checkBox_slits_s2hg.stateChanged.connect(self.f_interface_change)

        self.action_version.triggered.connect(self.f_menu_info)

    def f_buttons_click(self):

        time_plot.clear()
        th_plot.clear()
        s1hg_plot.clear()
        s2hg_plot.clear()

        for i in self.graphicsView_thVsTime.getPlotItem().listDataItems(): self.graphicsView_thVsTime.getPlotItem().removeItem(i)
        for i in self.graphicsView_thVsS1hgS2hg.getPlotItem().listDataItems(): self.graphicsView_thVsS1hgS2hg.getPlotItem().removeItem(i)

        # th s1hg s2hg total_time - this is needed to "connect" segments if more than 1 is needed
        values_last = [99, 0, 0, 0]
        motors_last_string = ""
        # check users input and number of filled segments
        notAllowedSymbols = re.compile(r'[^0-9:.-]')

        notEmptySegments = 0
        for col in range(0, self.tableWidget.columnCount()):

            notEmptySegments += [1 if self.tableWidget.item(col, 0).text().find(":") > 0 else 0][0]

            for row in range(0, self.tableWidget.rowCount()-2):
                if notAllowedSymbols.findall(self.tableWidget.item(col, row).text()):
                    self.statusbar.showMessage("Recheck your input for typos in the segment " + str(col+1) + ".")
                    return

        scriptDescription = f"#C pySAgen table \n#C th|{'s1hg' if self.checkBox_slits_s1hg.isChecked() else ''}|{'s2hg' if self.checkBox_slits_s2hg.isChecked() else ''}|time|steps\n"

        for segmentNumber in range(0, notEmptySegments):
            th = self.tableWidget.item(segmentNumber, 0).text()

            columnNumberIfSlits = 0
            if self.checkBox_slits_s1hg.isChecked():
                s1hg, columnNumberIfSlits = self.tableWidget.item(segmentNumber, 1).text(), 1
                if self.checkBox_slits_s2hg.isChecked(): s2hg, columnNumberIfSlits = self.tableWidget.item(segmentNumber, 2).text(), 2
            elif self.checkBox_slits_s2hg.isChecked(): s2hg, columnNumberIfSlits = self.tableWidget.item(segmentNumber, 1).text(), 1

            timePerStep = self.tableWidget.item(segmentNumber, columnNumberIfSlits + 1).text()
            numberOfPoints = self.tableWidget.item(segmentNumber, columnNumberIfSlits + 2).text()

            scriptDescription += f"#C {str(th)}|{str(s1hg) if self.checkBox_slits_s1hg.isChecked() else ''}|{str(s2hg) if self.checkBox_slits_s2hg.isChecked() else ''}|{str(timePerStep)}|{str(numberOfPoints)} \n"

            segment = []

            step.th = float(th[:th.find(":")])
            th_step = (float(th[th.find(":") + 1:]) - step.th) / float(numberOfPoints)
            if abs(th_step) <= th_stepMinimum:  # adjust number of points and th step if required th step is less than minimum possible
                th_step = math.copysign(th_stepMinimum, th_step)
                numberOfPoints = (float(th[th.find(":") + 1:]) - step.th) / th_stepMinimum  #

            step.s1hg, s1hg_step = 0, 0
            if self.checkBox_slits_s1hg.isChecked():
                if s1hg.find(":") >= 0:
                    step.s1hg = step.s1hg_temp = float(s1hg[:s1hg.find(":")])
                    s1hg_step = (float(s1hg[s1hg.find(":") + 1:]) - step.s1hg) / float(numberOfPoints)
                else: step.s1hg = step.s1hg_temp = float(s1hg)

            step.s2hg, s2hg_step = 0, 0
            if self.checkBox_slits_s2hg.isChecked():
                if s2hg.find(":") >= 0:
                    step.s2hg = step.s2hg_temp = float(s2hg[:s2hg.find(":")])
                    s2hg_step = (float(s2hg[s2hg.find(":") + 1:]) - step.s2hg) / float(numberOfPoints)
                else: step.s2hg = step.s2hg_temp = float(s2hg)

            timePerStep_step = 0
            if timePerStep.find(":") >= 0:
                step.time = round(float(timePerStep[:timePerStep.find(":")]), 1)
                timePerStep_step = (float(timePerStep[timePerStep.find(":") + 1:]) - step.time) / float(numberOfPoints)
            else: step.time = round(float(timePerStep), 1)

            if not round(values_last[0], 2) == round(step.th, 2): segment.append([step.th, 2 * step.th, step.s1hg, step.s2hg, step.time])  # connect 2 segments without repeat the same th angle

            i = 0
            while i != int(numberOfPoints):  # create 2D list for current segment
                step.th += th_step
                step.time += timePerStep_step
                if self.checkBox_slits_s1hg.isChecked():
                    step.s1hg_temp += s1hg_step
                    # if step size for s1hg is less than minimum possible for motor, than we need skip this move
                    if abs(step.s1hg_temp - step.s1hg) > s1hg_stepMinimum: step.s1hg = step.s1hg_temp
                if self.checkBox_slits_s2hg.isChecked():
                    step.s2hg_temp += s2hg_step
                    # if step size for s2hg is less than minimum possible for motor, than we need skip this move
                    if abs(step.s2hg_temp - step.s2hg) > s2hg_stepMinimum: step.s2hg = step.s2hg_temp
                # add new line for scanning
                segment.append([round(step.th, 3), 2 * round(step.th, 3), round(step.s1hg, 2), round(step.s2hg, 2), round(step.time, 1)])

                values_last[3] += segment[i][4] + 4  # total time for the scan
                i += 1

            for segment_record in segment:
                time_plot.append(segment_record[4])
                th_plot.append(segment_record[0])
                if self.checkBox_slits_s1hg.isChecked(): s1hg_plot.append(segment_record[2])
                if self.checkBox_slits_s2hg.isChecked(): s2hg_plot.append(segment_record[3])

        self.s1 = pg.ScatterPlotItem(x=th_plot, y=time_plot, symbol="o", size=5, pen=pg.mkPen(0.2), brush=pg.mkBrush(0.7))
        self.graphicsView_thVsTime.addItem(self.s1)
        if self.checkBox_slits_s1hg.isChecked():
            self.s2 = pg.ScatterPlotItem(x=th_plot, y=s1hg_plot, symbol="o", size=5, pen=pg.mkPen(0.8), brush=pg.mkBrush(0.1))
            self.graphicsView_thVsS1hgS2hg.addItem(self.s2)
        if self.checkBox_slits_s2hg.isChecked():
            self.s3 = pg.ScatterPlotItem(x=th_plot, y=s2hg_plot, symbol="o", size=5, pen=pg.mkPen(0.2), brush=pg.mkBrush(0.7))
            self.graphicsView_thVsS1hgS2hg.addItem(self.s3)

        if int((round(values_last[3] // 3600, 2))) == 0: time = str(int(round(values_last[3] / 60))) + " min."
        else: time = str(int(round(values_last[3] // 3600))) + "h " + str(int(round((values_last[3] % 3600)/60))) + "min (" + (str(int(round(values_last[3] / 60)))) + " min)."

        self.statusbar.showMessage("Total time to execute the script is approximately: " + time)

        if self.sender().objectName() == "pushButton_create":

            values_last = [99, 0, 0, values_last[3]]

            saveAt_dir = QtWidgets.QFileDialog().getExistingDirectory()
            if not saveAt_dir: return

            # write the first line with motor names and erase file if required
            FILE_SCRIPT = open(saveAt_dir + "/Script_" + str(int(round(values_last[3] // 60))) + "_min.dat", "w")

            motorsString_header = f"#M th tth{' s1hg' if self.checkBox_slits_s1hg.isChecked() else ''}{' s2hg' if self.checkBox_slits_s2hg.isChecked() else ''}\n"

            FILE_SCRIPT.write(scriptDescription + "#C\n" + motorsString_header)

            # same for direct beam file (if required)
            if self.checkBox_createDBfile.isChecked():
                FILE_DB = open(saveAt_dir + "/Script_" + str(int(round(values_last[3] // 60, 2))) + "_min_DB.dat", "w")
                FILE_DB.write(motorsString_header)

            for i, th_plot_i in enumerate(th_plot):

                # write to script file
                if self.checkBox_slits_s1hg.isChecked() and self.checkBox_slits_s2hg.isChecked():
                    motors_string = str(th_plot_i) + " " + str(th_plot_i*2) + " " + str(s1hg_plot[i]) + " " + str(s2hg_plot[i]) + " " + str(time_plot[i]) + "\n"
                    motors_string_DB = "0 0 " + str(s1hg_plot[i]) + " " + str(s2hg_plot[i]) + " 10" + "\n"
                elif self.checkBox_slits_s1hg.isChecked():
                    motors_string = str(th_plot_i) + " " + str(th_plot_i*2) + " " + str(s1hg_plot[i]) + " " +  str(time_plot[i]) + "\n"
                    motors_string_DB = "0 0 " + str(s1hg_plot[i]) + " 10" + "\n"
                elif self.checkBox_slits_s2hg.isChecked():
                    motors_string = str(th_plot_i) + " " + str(th_plot_i*2) + " " + str(s2hg_plot[i]) + " " + str(time_plot[i]) + "\n"
                    motors_string_DB = "0 0 " + str(s2hg_plot[i]) + " 10" + "\n"
                else: motors_string = str(th_plot_i) + " " + str(th_plot_i*2) + " " + str(time_plot[i]) + "\n"

                if not motors_last_string == motors_string: FILE_SCRIPT.write(motors_string)
                motors_last_string = motors_string

                # write to DB script file
                if self.checkBox_createDBfile.isChecked() and (not s1hg_plot[i] == values_last[1] or not s2hg_plot[i] == values_last[2]):
                    FILE_DB.write(motors_string_DB)
                    values_last[1], values_last[2] = s1hg_plot[i], s2hg_plot[i]  # s1hg s2hg

            FILE_SCRIPT.close()
            if self.checkBox_createDBfile.isChecked(): FILE_DB.close()

    def f_interface_change(self):

        self.statusbar.showMessage("")

        if self.checkBox_slits_s1hg.isChecked():
            self.tableWidget.setColumnCount(4)

            column_names = ["th (degree)", "s1hg (mm)", "time per step (s)", "number of points"]
            column_widths = [105, 105, 130, 137]
            default_line = ["0:2", "0.5:1", "5:60", "50"]

            self.MW_size = 811 if platform.system() == 'Windows' else 790
            self.label_thVsS1hgS2hg.setText("th (degrees) vs s1hg (mm)")
            self.label_thVsS1hgS2hg.setGeometry(QtCore.QRect(165, 465, 261, 31))
            self.checkBox_createDBfile.setVisible(True)

        if self.checkBox_slits_s2hg.isChecked():
            self.tableWidget.setColumnCount(4)

            column_names = ["th (degree)", "s2hg (mm)", "time per step (s)", "number of points"]
            column_widths = [105, 105, 130, 137]
            default_line = ["0:2", "0.5:1", "5:60", "50"]

            self.MW_size = 811 if platform.system() == 'Windows' else 790
            self.label_thVsS1hgS2hg.setText("th (degrees) vs s2hg (mm)")
            self.label_thVsS1hgS2hg.setGeometry(QtCore.QRect(165, 465, 261, 31))
            self.checkBox_createDBfile.setVisible(True)

        if self.checkBox_slits_s1hg.isChecked() and self.checkBox_slits_s2hg.isChecked():
            self.tableWidget.setColumnCount(5)

            column_names = ["th (degree)", "s1hg (mm)", "s2hg (mm)", "time per step (s)", "number of points"]
            column_widths = [80, 85, 85, 110, 117]
            default_line = ["0:2", "0.5:1", "1", "5:60", "50"]

            self.MW_size = 811 if platform.system() == 'Windows' else 790
            self.label_thVsS1hgS2hg.setText("th (degree) vs s1hg (mm), s2hg (mm)")
            self.label_thVsS1hgS2hg.setGeometry(QtCore.QRect(130, 465, 261, 31))
            self.checkBox_createDBfile.setVisible(True)

        if not self.checkBox_slits_s1hg.isChecked() and not self.checkBox_slits_s2hg.isChecked():
            self.tableWidget.setColumnCount(3)

            column_names = ["th (degrees)", "time per step (s)", "number of points"]
            column_widths = [143, 163, 171]
            default_line = ["0:2", "5:60", "50"]

            self.MW_size = 503 if platform.system() == 'Windows' else 482
            self.checkBox_createDBfile.setVisible(False)

        self.resize(500, self.MW_size)
        self.setMinimumSize(QtCore.QSize(500, self.MW_size))
        self.setMaximumSize(QtCore.QSize(500, self.MW_size))

        for i in range(0, self.tableWidget.rowCount()):
            item = QtWidgets.QTableWidgetItem()
            item.setText(str(i + 1))
            self.tableWidget.setVerticalHeaderItem(i, item)
            item = QtWidgets.QTableWidgetItem()
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget.setRowHeight(i, 1 if platform.system=="Windows" else 20)

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

    def f_menu_info(self):

        msgBox = QtWidgets.QMessageBox()
        msgBox.setWindowIcon(QtGui.QIcon(self.iconpath))
        msgBox.setText("pySAgen V1.1\n\n"
                       "Alexey.Klechikov@gmail.com\n\n"
                       "Check new version at https://github.com/Alexey-Klechikov/pySAgen/releases")
        msgBox.exec_()

if __name__ == "__main__":
    QtWidgets.QApplication.setStyle("Fusion")
    app = QtWidgets.QApplication(sys.argv)
    prog = GUI()
    prog.show()
    sys.exit(app.exec_())

