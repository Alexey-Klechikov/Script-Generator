from PyQt5 import QtCore, QtGui, QtWidgets
import os, math
import numpy as np

import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

import FrontEnd

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

matplotlib.rcParams.update({'font.size': 7, })

class Canvas(FigureCanvas):

    def __init__(self, parent, width, height):

        self.figure = Figure(figsize=(width, height))
        FigureCanvas.__init__(self, self.figure)
        self.canvas = FigureCanvas(self.figure)
        self.setParent(parent)

        self.plot = self.figure.add_subplot(111)


    def draw_new_plot(self, x, y, size, title):
        self.plot.clear()
        self.plot.scatter(x, y, size)
        self.plot.set_title(title, fontname="Calibri", fontweight="bold")

    def add_to_plot(self, x, y, size):
        self.plot.scatter(x, y, size)

class step:
    def __init__(self, th, s1hg, s1hg_temp, s2hg, s2hg_temp, time):
        self.th = th
        self.s1hg = s1hg
        self.s1hg_temp = s1hg_temp
        self.s2hg = s2hg
        self.s2hg_temp = s2hg_temp
        self.time = time

class GUI(FrontEnd.Ui_MainWindow):
    def __init__(self, parent=None):
        #super(self.__class__, self).__init__()
        super(GUI, self).__init__(parent)
        self.setupUi(self)

        # Graphs
        self.canvas_th_time = Canvas(self, 3.48, 2)
        self.canvas_th_time.move(7, 174)
        self.canvas_th_time.draw_new_plot(np.array([0, 1, 2]), np.array([0, 0, 0]), size=1, title="th (degrees) vs Time per step (s)")

        self.canvas_th_s1hg_s2hg = Canvas(self, 3.48, 2)
        self.canvas_th_s1hg_s2hg.move(7, 386)
        self.canvas_th_s1hg_s2hg.draw_new_plot(np.array([0, 1, 2]), np.array([0, 0, 0]), size=1, title="th (degrees) vs s1hg (mm), s2hg (mm)")

        # Triggers
        self.pushButton_create.clicked.connect(self.create_button_click)
        self.toolButton_save_at.clicked.connect(self.button_SaveDir)

        self.actionVersion.triggered.connect(self.menu_info)

    def button_SaveDir(self):
        saveAt = QtWidgets.QFileDialog().getExistingDirectory()
        if not saveAt: return
        self.lineEdit_save_at.setText(str(saveAt) + "/Script.dat")
        self.lineEdit_save_at.setText(self.lineEdit_save_at.text().replace("//", "/"))

    def create_button_click(self):

        plot_time.clear()
        plot_th.clear()
        plot_s1hg.clear()
        plot_s2hg.clear()

        last_values = [99, 0, 0, 0]  # th s1hg s2hg total_time - this is needed to "connect" segments if more than 1 is needed

        if not self.lineEdit_save_at.text(): self.lineEdit_save_at.setText(current_dir + "/Script.dat")
        self.lineEdit_save_at.setText(self.lineEdit_save_at.text().replace("//", "/"))

        # write the first line with motor names and erase file if required
        script_file = open(self.lineEdit_save_at.text(), "w")
        script_file.write("#M th tth s1hg s2hg \n")
        script_file.close()

        # same for direct beam file
        script_file_DB = open(self.lineEdit_save_at.text()[:-4] + "_DB.dat", "w")
        script_file_DB.write("#M th tth s1hg s2hg \n")
        script_file_DB.close()

        # continue to write to the files
        script_file = open(self.lineEdit_save_at.text(), "a")
        script_file_DB = open(self.lineEdit_save_at.text()[:-4] + "_DB.dat", "a")

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
            os.rename(self.lineEdit_save_at.text()[:-4] + "_DB.dat",
                      self.lineEdit_save_at.text()[:-4] + "_" + str(round(last_values[3] / 60, 2)) + "min_DB.dat")
        except WindowsError:  # check if there already is a file with the same name in the folder -> overwrite then
            os.remove(self.lineEdit_save_at.text()[:-4] + "_" + str(round(last_values[3] / 60, 2)) + "min_DB.dat")
            os.rename(self.lineEdit_save_at.text()[:-4] + "_DB.dat",
                      self.lineEdit_save_at.text()[:-4] + "_" + str(round(last_values[3] / 60, 2)) + "min_DB.dat")


        try:
            os.rename(self.lineEdit_save_at.text(), self.lineEdit_save_at.text()[:-4] + "_" + str(round(last_values[3] / 60, 2)) + "min.dat")

        except WindowsError:  # check if there already is a file with the same name in the folder -> overwrite then
            os.remove(self.lineEdit_save_at.text()[:-4] + "_" + str(round(last_values[3] / 60, 2)) + "min.dat")
            os.rename(self.lineEdit_save_at.text(), self.lineEdit_save_at.text()[:-4] + "_" + str(round(last_values[3] / 60, 2)) + "min.dat")

        self.draw()

        self.statusbar.showMessage("Total time to execute script is approximately: " + str(round(last_values[3] / 60, 2)) + "min")

    def draw(self):

        self.canvas_th_time.draw_new_plot(x=plot_th, y=plot_time, size=1, title="th (degrees) vs Time per step (s)")
        self.canvas_th_time.draw()

        self.canvas_th_s1hg_s2hg.draw_new_plot(x=plot_th, y=plot_s1hg, size=1, title="th (degrees) vs s1hg (mm), s2hg (mm)")
        self.canvas_th_s1hg_s2hg.draw()

        self.canvas_th_s1hg_s2hg.add_to_plot(x=plot_th, y=plot_s2hg, size=1)
        self.canvas_th_s1hg_s2hg.draw()

    def menu_info(self):

        msgBox = QtWidgets.QMessageBox()
        msgBox.setWindowIcon(QtGui.QIcon(current_dir + "\icon.png"))
        msgBox.setText("SuperADAM Script generator V. 190511\n\n"
                       "Alexey.Klechikov@gmail.com")
        msgBox.exec_()

if __name__ == "__main__":
    import sys

    QtWidgets.QApplication.setStyle("Fusion")
    app = QtWidgets.QApplication(sys.argv)
    prog = GUI()
    prog.show()
    sys.exit(app.exec_())

