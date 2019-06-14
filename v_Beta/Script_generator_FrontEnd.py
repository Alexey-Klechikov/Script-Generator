from PyQt5 import QtCore, QtGui, QtWidgets
import pyqtgraph as pg

class Ui_MainWindow(QtWidgets.QMainWindow):

    def setupUi(self, MainWindow, parent_path):

        # Fonts
        font_headline = QtGui.QFont()
        font_headline.setPointSize(8)
        font_headline.setBold(True)

        font_graphs = QtGui.QFont()
        font_graphs.setPixelSize(10)
        font_graphs.setBold(False)

        font_graphs_2 = QtGui.QFont()
        font_graphs_2.setPixelSize(1)
        font_graphs_2.setBold(False)

        font_ee = QtGui.QFont()
        font_ee.setPointSize(7)
        font_ee.setBold(False)

        # Background and foreground for graphs
        pg.setConfigOption('background', (255, 255, 255))
        pg.setConfigOption('foreground', 'k')

        # Main Window
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(361, 640)
        MainWindow.setMinimumSize(QtCore.QSize(361, 640))
        MainWindow.setMaximumSize(QtCore.QSize(361, 640))
        MainWindow.setWindowTitle("Script Generator")
        MainWindow.setWindowIcon(QtGui.QIcon(parent_path + "\icon.png"))
        MainWindow.setIconSize(QtCore.QSize(30, 30))

        # Block: Table
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(5, 5, 351, 98))
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
                self.tableWidget.setColumnWidth(i, 70)
            elif i == 1:
                item.setText("s1hg (mm)")
                self.tableWidget.setColumnWidth(i, 55)
            elif i == 2:
                item.setText("s2hg (mm)")
                self.tableWidget.setColumnWidth(i, 55)
            elif i == 3:
                item.setText("time per step (s)")
                self.tableWidget.setColumnWidth(i, 80)
            elif i == 4:
                item.setText("number of points")
                self.tableWidget.setColumnWidth(i, 80)
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
        self.pushButton_create.setGeometry(QtCore.QRect(286, 130, 70, 20))
        self.pushButton_create.setFont(font_headline)
        self.pushButton_create.setObjectName("pushButton_create")
        self.pushButton_create.setText("Create")

        # Button: Preview
        self.pushButton_preview = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_preview.setGeometry(QtCore.QRect(286, 107, 70, 20))
        self.pushButton_preview.setFont(font_headline)
        self.pushButton_preview.setObjectName("pushButton_preview")
        self.pushButton_preview.setText("Preview")

        # Block: Save at
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 105, 171, 16))
        self.label.setFont(font_headline)
        self.label.setObjectName("label")
        self.label.setText("Save script file at")
        self.lineEdit_save_at = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_save_at.setGeometry(QtCore.QRect(5, 123, 211, 20))
        self.lineEdit_save_at.setFont(font_ee)
        self.lineEdit_save_at.setText("")
        self.lineEdit_save_at.setObjectName("lineEdit_save_at")
        self.lineEdit_save_at.setPlaceholderText(parent_path)
        self.toolButton_save_at = QtWidgets.QToolButton(self.centralwidget)
        self.toolButton_save_at.setGeometry(QtCore.QRect(220, 123, 20, 20))
        self.toolButton_save_at.setObjectName("toolButton_save_at")
        self.toolButton_save_at.setText("...")

        # Graph: th vs time
        self.label_th_vs_time = QtWidgets.QLabel(self.centralwidget)
        self.label_th_vs_time.setGeometry(QtCore.QRect(90, 148, 231, 20))
        self.label_th_vs_time.setFont(font_headline)
        self.label_th_vs_time.setObjectName("label_th_vs_time")
        self.label_th_vs_time.setText("th (degrees) vs Time per step (s)")
        self.groupBox_th_vs_time = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_th_vs_time.setGeometry(QtCore.QRect(5, 150, 351, 220))
        self.groupBox_th_vs_time.setTitle("")
        self.groupBox_th_vs_time.setObjectName("groupBox_th_vs_time")
        self.graphicsView_th_vs_time = pg.PlotWidget(self.centralwidget)
        self.graphicsView_th_vs_time.setGeometry(QtCore.QRect(7, 169, 348, 200))
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
        self.label_th_vs_s1hg_s2hg.setGeometry(QtCore.QRect(80, 365, 261, 41))
        self.label_th_vs_s1hg_s2hg.setFont(font_headline)
        self.label_th_vs_s1hg_s2hg.setObjectName("label_th_vs_s1hg_s2hg")
        self.label_th_vs_s1hg_s2hg.setText("th (degrees) vs s1hg (mm), s2hg (mm)")
        self.groupBox_th_vs_s1hg_s2hg = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_th_vs_s1hg_s2hg.setGeometry(QtCore.QRect(5, 377, 351, 220))
        self.groupBox_th_vs_s1hg_s2hg.setTitle("")
        self.groupBox_th_vs_s1hg_s2hg.setObjectName("groupBox_th_vs_s1hg_s2hg")
        self.graphicsView_th_vs_s1hg_s2hg = pg.PlotWidget(self.centralwidget)
        self.graphicsView_th_vs_s1hg_s2hg.setGeometry(QtCore.QRect(7, 396, 348, 200))
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
        self.actionVersion.setText("Version 1906")
        self.menuHelp.addAction(self.actionVersion)
        self.menubar.addAction(self.menuHelp.menuAction())

        # StatusBar
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.statusbar.showMessage("Total time to execute script is approximately: ")
