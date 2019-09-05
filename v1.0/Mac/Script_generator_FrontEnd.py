from PyQt5 import QtCore, QtGui, QtWidgets
import pyqtgraph as pg

class Ui_MainWindow(QtWidgets.QMainWindow):

    def setupUi(self, MainWindow, parent_path):

        # Fonts
        font_headline = QtGui.QFont()
        font_headline.setPointSize(13)
        font_headline.setBold(True)

        font_graphs = QtGui.QFont()
        font_graphs.setPixelSize(10)
        font_graphs.setBold(False)

        font_graphs_2 = QtGui.QFont()
        font_graphs_2.setPixelSize(1)
        font_graphs_2.setBold(False)

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
        MainWindow.setWindowTitle("Script Generator")
        MainWindow.setWindowIcon(QtGui.QIcon(parent_path + "\icon.png"))
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
                self.tableWidget.setColumnWidth(i, int(self.tableWidget.width()) - int(self.tableWidget.columnWidth(0)) - int(self.tableWidget.columnWidth(2)) - int(self.tableWidget.columnWidth(2)) - int(self.tableWidget.columnWidth(3)) - 2)
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
        self.graphicsView_th_vs_time = pg.PlotWidget(self.centralwidget)
        self.graphicsView_th_vs_time.setGeometry(QtCore.QRect(7, 189, 487, 270))
        self.graphicsView_th_vs_time.setObjectName("graphicsView_th_vs_time")
        self.graphicsView_th_vs_time.getAxis("bottom").tickFont = font_graphs
        self.graphicsView_th_vs_time.getAxis("bottom").setStyle(tickTextOffset=10)
        self.graphicsView_th_vs_time.getAxis("left").tickFont = font_graphs
        self.graphicsView_th_vs_time.getAxis("left").setStyle(tickTextOffset=10)
        self.graphicsView_th_vs_time.showAxis("top")
        self.graphicsView_th_vs_time.getAxis("top").tickFont = font_graphs_2
        self.graphicsView_th_vs_time.getAxis("top").setStyle(tickTextOffset=-2)
        self.graphicsView_th_vs_time.showAxis("right")
        self.graphicsView_th_vs_time.getAxis("right").tickFont = font_graphs_2
        self.graphicsView_th_vs_time.getAxis("right").setStyle(tickTextOffset=-2)

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
        self.graphicsView_th_vs_s1hg_s2hg = pg.PlotWidget(self.centralwidget)
        self.graphicsView_th_vs_s1hg_s2hg.setGeometry(QtCore.QRect(7, 496, 487, 270))
        self.graphicsView_th_vs_s1hg_s2hg.setObjectName("graphicsView_th_vs_s1hg_s2hg")
        self.graphicsView_th_vs_s1hg_s2hg.getAxis("bottom").tickFont = font_graphs
        self.graphicsView_th_vs_s1hg_s2hg.getAxis("bottom").setStyle(tickTextOffset=10)
        self.graphicsView_th_vs_s1hg_s2hg.getAxis("left").tickFont = font_graphs
        self.graphicsView_th_vs_s1hg_s2hg.getAxis("left").setStyle(tickTextOffset=10)
        self.graphicsView_th_vs_s1hg_s2hg.showAxis("top")
        self.graphicsView_th_vs_s1hg_s2hg.getAxis("top").tickFont = font_graphs_2
        self.graphicsView_th_vs_s1hg_s2hg.getAxis("top").setStyle(tickTextOffset=-2)
        self.graphicsView_th_vs_s1hg_s2hg.showAxis("right")
        self.graphicsView_th_vs_s1hg_s2hg.getAxis("right").tickFont = font_graphs_2
        self.graphicsView_th_vs_s1hg_s2hg.getAxis("right").setStyle(tickTextOffset=-2)

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
        self.actionVersion.setText("Version 1.0")
        self.menuHelp.addAction(self.actionVersion)
        self.menubar.addAction(self.menuHelp.menuAction())

        # StatusBar
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.statusbar.showMessage("Total time to execute script is approximately: ")
