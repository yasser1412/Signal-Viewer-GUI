from PyQt5 import QtCore, QtGui, QtWidgets
import pyqtgraph as pg
import pyqtgraph.exporters
from pyqtgraph import PlotWidget, plot
from PyQt5.QtWidgets import QMessageBox
import pandas as pd
import numpy as np
from scipy.fft import fftshift
from scipy import signal
import matplotlib.pyplot as plt
from scipy.io import loadmat
from fpdf import FPDF
import os

class Ui_mainWindow(object):
    #dictinary stores files with its format
    filenames = dict()
    #dictinary stores files with its graph widget
    Current_File = dict()
    #a list of images of the graphs (use for create_pdf)
    image_list = []
    #a list of images of the spectrograms (use for create_pdf)
    spectroImg_list=[None,None,None] 
    #flags for pause and stop functions
    isPaused = False
    isStoped = False
    #the length of data on a file
    dataLength = 0
    #pens colors for the graph
    pen1 = [255,0,0]
    pen2 = [0,255,0]
    pen3 = [0,0,255]
    # a list for pens to used in plot function
    pens = [pen1, pen2, pen3]
    #stores number of the selected widget
    current_widget = int
    #intial graph range 
    graph_rangeMin = [0,0,0]
    graph_rangeMax = [1000,1000,1000]
    
    
    def setupUi(self, mainWindow):

        mainWindow.setObjectName("mainWindow")
        mainWindow.setEnabled(True)
        mainWindow.resize(637, 600)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("images/window.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        mainWindow.setWindowIcon(icon)
        mainWindow.setAutoFillBackground(False)
        mainWindow.setStyleSheet("font: 12pt \"Franklin Gothic Demi Cond\";")
        mainWindow.setIconSize(QtCore.QSize(30, 30))
        self.centralwidget = QtWidgets.QWidget(mainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(520, 10, 101, 31))
        self.comboBox.setStyleSheet("font: 8pt \"Arial Narrow\";\n" "font: 12pt \"MS Shell Dlg 2\";")
        self.comboBox.setEditable(False)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.widget = pg.PlotWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(60, 50, 511, 150))
        self.widget.setAutoFillBackground(False)
        self.widget.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.widget.setObjectName("widget")
        self.widget_2 = pg.PlotWidget(self.centralwidget)
        self.widget_2.setGeometry(QtCore.QRect(60, 220, 511, 150))
        self.widget_2.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.widget_2.setObjectName("widget_2")
        self.widget_3 = pg.PlotWidget(self.centralwidget)
        self.widget_3.setGeometry(QtCore.QRect(60, 390, 511, 150))
        self.widget_3.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.widget_3.setObjectName("widget_3")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(280, 30, 61, 21))
        self.label.setStyleSheet("\n" "font: 12pt \"Arial Narrow\";")
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(280, 200, 61, 21))
        self.label_2.setStyleSheet("font: 12pt \"Arial Narrow\";\n" "")
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(280, 370, 61, 21))
        self.label_3.setStyleSheet("font: 12pt \"Arial Narrow\";\n" "")
        self.label_3.setObjectName("label_3")
        mainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(mainWindow)
        self.statusbar.setObjectName("statusbar")
        mainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(mainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toolBar.sizePolicy().hasHeightForWidth())
        self.toolBar.setSizePolicy(sizePolicy)
        self.toolBar.setAutoFillBackground(False)
        self.toolBar.setStyleSheet("background-color: rgb(220, 220, 220);\n" "selection-background-color: rgb(255, 255, 255);")
        self.toolBar.setIconSize(QtCore.QSize(28, 28))
        self.toolBar.setObjectName("toolBar")
        mainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        mainWindow.insertToolBarBreak(self.toolBar)
        self.actionLoad = QtWidgets.QAction(mainWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("images/browse.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionLoad.setIcon(icon1)
        self.actionLoad.setObjectName("actionLoad")
        self.actionX_axis = QtWidgets.QAction(mainWindow)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("images/x axis.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionX_axis.setIcon(icon2)
        self.actionX_axis.setObjectName("actionX_axis")
        self.actionY_axis = QtWidgets.QAction(mainWindow)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("images/y axis.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionY_axis.setIcon(icon3)
        self.actionY_axis.setObjectName("actionY_axis")
        self.actionmove = QtWidgets.QAction(mainWindow)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("images/move.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionmove.setIcon(icon4)
        self.actionmove.setObjectName("actionmove")
        self.actionPlay = QtWidgets.QAction(mainWindow)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("images/play.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionPlay.setIcon(icon5)
        self.actionPlay.setObjectName("actionPlay")
        self.actionPause = QtWidgets.QAction(mainWindow)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("images/pause.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionPause.setIcon(icon6)
        self.actionPause.setObjectName("actionPause")
        self.actionStop = QtWidgets.QAction(mainWindow)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap("images/stop.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionStop.setIcon(icon7)
        self.actionStop.setObjectName("actionStop")
        self.actionSave = QtWidgets.QAction(mainWindow)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap("images/save1.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSave.setIcon(icon8)
        self.actionSave.setObjectName("actionSave")
        self.actionclear = QtWidgets.QAction(mainWindow)
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap("images/clear.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionclear.setIcon(icon9)
        self.actionclear.setObjectName("actionclear")
        self.actionLeft = QtWidgets.QAction(mainWindow)
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap("images/left.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionLeft.setIcon(icon10)
        self.actionLeft.setObjectName("actionLeft")
        self.actionRight = QtWidgets.QAction(mainWindow)
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap("images/right.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionRight.setIcon(icon11)
        self.actionRight.setObjectName("actionRight")
        self.actionZoom_in = QtWidgets.QAction(mainWindow)
        icon12 = QtGui.QIcon()
        icon12.addPixmap(QtGui.QPixmap("images/zoom-in.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionZoom_in.setIcon(icon12)
        self.actionZoom_in.setObjectName("actionZoom_in")
        self.actionZoom_out = QtWidgets.QAction(mainWindow)
        icon13 = QtGui.QIcon()
        icon13.addPixmap(QtGui.QPixmap("images/zoom-out.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionZoom_out.setIcon(icon13)
        self.actionZoom_out.setObjectName("actionZoom_out")
        self.toolBar.addAction(self.actionLoad)
        self.toolBar.addAction(self.actionPlay)
        self.toolBar.addAction(self.actionPause)
        self.toolBar.addAction(self.actionStop)
        self.toolBar.addAction(self.actionX_axis)
        self.toolBar.addAction(self.actionY_axis)
        self.toolBar.addAction(self.actionmove)
        self.toolBar.addAction(self.actionLeft)
        self.toolBar.addAction(self.actionRight)
        self.toolBar.addAction(self.actionZoom_in)
        self.toolBar.addAction(self.actionZoom_out)
        self.toolBar.addAction(self.actionSave)
        self.toolBar.addAction(self.actionclear)
        

        self.retranslateUi(mainWindow)
        QtCore.QMetaObject.connectSlotsByName(mainWindow)

        #connecting each button by its function
        self.actionLoad.triggered.connect(self.load_file)
        self.actionX_axis.triggered.connect(self.only_x)
        self.actionY_axis.triggered.connect(self.only_y)
        self.actionmove.triggered.connect(self.zoom)
        self.actionSave.triggered.connect(self.export)
        self.actionclear.triggered.connect(self.clear)
        self.actionPlay.triggered.connect(self.start)
        self.actionPause.triggered.connect(self.pause)
        self.actionStop.triggered.connect(self.stop)
        self.actionZoom_in.triggered.connect(self.zoom_in)
        self.actionZoom_out.triggered.connect(self.zoom_out)
        self.actionRight.triggered.connect(self.move_right)
        self.actionLeft.triggered.connect(self.move_left)
        
        self.widget.setBackground("w")
        self.widget_2.setBackground("w")
        self.widget_3.setBackground("w")
        
        #a list of widgets on the program used in selecting a widget
        self.widgets = [self.widget,self.widget_2,self.widget_3]

    def retranslateUi(self, mainWindow):
        _translate = QtCore.QCoreApplication.translate
        mainWindow.setWindowTitle(_translate("mainWindow", "Signal Viewer"))
        
        self.comboBox.setItemText(0, _translate("mainWindow", "Widget1"))
        self.comboBox.setItemText(1, _translate("mainWindow", "Widget2"))
        self.comboBox.setItemText(2, _translate("mainWindow", "Widget3"))
        self.label.setText(_translate("mainWindow", "Widget 1"))
        self.label_2.setText(_translate("mainWindow", "Widget 2"))
        self.label_3.setText(_translate("mainWindow", "Widget 3"))
        self.toolBar.setWindowTitle(_translate("mainWindow", "toolBar"))
        self.actionLoad.setText(_translate("mainWindow", ""))
        self.actionLoad.setShortcut(_translate("MainWindow", "Ctrl+L"))
        self.actionX_axis.setText(_translate("mainWindow", ""))
        self.actionX_axis.setShortcut(_translate("MainWindow", "Ctrl+X"))
        self.actionY_axis.setText(_translate("mainWindow", ""))
        self.actionY_axis.setShortcut(_translate("MainWindow", "Ctrl+Y"))
        self.actionmove.setText(_translate("mainWindow", "move"))
        self.actionmove.setShortcut(_translate("MainWindow", "Ctrl+M"))
        self.actionPlay.setText(_translate("mainWindow", "Play"))
        self.actionPlay.setShortcut(_translate("MainWindow", "Ctrl+P"))
        self.actionPause.setText(_translate("mainWindow", "Pause"))
        self.actionPause.setShortcut(_translate("MainWindow", "Ctrl+Shift+P"))
        self.actionStop.setText(_translate("mainWindow", "Stop"))
        self.actionStop.setShortcut(_translate("MainWindow", "Ctrl+Shift+S"))
        self.actionSave.setText(_translate("mainWindow", "Save"))
        self.actionSave.setShortcut(_translate("MainWindow", "Ctrl+S"))
        self.actionclear.setText(_translate("mainWindow", "clear"))
        self.actionclear.setShortcut(_translate("MainWindow", "Delete"))
        self.actionLeft.setText(_translate("mainWindow", "Left"))
        self.actionLeft.setShortcut(_translate("MainWindow", "Left"))
        self.actionRight.setText(_translate("mainWindow", "Right"))
        self.actionRight.setShortcut(_translate("MainWindow", "Right"))
        self.actionZoom_in.setText(_translate("mainWindow", "Zoom-in"))
        self.actionZoom_in.setShortcut(_translate("MainWindow", "Up"))
        self.actionZoom_out.setText(_translate("mainWindow", "Zoom-out"))
        self.actionZoom_out.setShortcut(_translate("MainWindow", "Down"))

    def load_file(self):
        #a function that loads the files data
        
        self.check_widget()
        self.filename, self.format = QtWidgets.QFileDialog.getOpenFileName(None, "Load Signal File", "", "*.csv;;" " *.txt;;" "*.mat")
        #checks if no file selected
        if self.filename == "":
            pass
        else:
            #checks if the file already existed in another widget
            if self.filename in self.filenames:
                self.show_popup("File Already Existed", "This file already uploaded before")
            else:
                #load the file for the first time
                self.clear()
                
                self.filenames[self.filename] = self.format
                self.Current_File[self.current_widget] = self.filename
                
                self.checkFileEXT(self.filename)
    
    def checkFileEXT(self, file):
        #a function that checks file extintions 
        if file.endswith(".csv"):
            csv_file = pd.read_csv(file).iloc[:,1]
            #saves data length of the file
            self.widgets[self.current_widget].dataLength = csv_file.__len__()
                
            self.plot_here(csv_file, file)
            self.plot_spectro(csv_file)
                
        elif file.endswith(".txt"):
            txt_file = pd.read_csv(file).iloc[:,2]
            #saves data length of the file
            self.widgets[self.current_widget].dataLength = txt_file.__len__()
                
            self.plot_here(txt_file, file)
            self.plot_spectro(txt_file)
            
        elif file.endswith(".mat"):
            mat = loadmat(file)
            mat_file = pd.DataFrame(mat["F"]).iloc[:,1]
            #saves data length of the file
            self.widgets[self.current_widget].dataLength = mat_file.__len__()
                
            self.plot_here(mat_file, file)
            self.plot_spectro(mat_file)

    def clear(self):
        #a functions that clears a graph and delete its file
        
        self.check_widget()
        self.widgets[self.current_widget].clear()
        self.stop()
        self.widgets[self.current_widget].plotItem.showGrid(False,False)
        
        if self.current_widget in self.Current_File:
        #delete the file from filenames dict and current_file dict
            del self.filenames[self.Current_File[self.current_widget]]
            del self.Current_File[self.current_widget]
    
    def only_y(self):
        # only move and zoom in y-axis
        self.check_widget()
        self.widgets[self.current_widget].plotItem.setMouseEnabled(x=False,y=True)
    
    def only_x(self):
        # only move and zoom in x-axis
        self.check_widget()
        self.widgets[self.current_widget].plotItem.setMouseEnabled(y=False,x=True)
    
    def zoom(self):
        #u can zoom and move in any direction
        self.check_widget()
        self.widgets[self.current_widget].plotItem.setMouseEnabled(y=True,x=True)
    
    def export(self):
        #a function that creates a pictures of the drawn graphs
        
        exporter1 = pg.exporters.ImageExporter(self.widget.plotItem)
        exporter1.export('fileName1.png')
        exporter2 = pg.exporters.ImageExporter(self.widget_2.plotItem)
        exporter2.export('fileName2.png')
        exporter3 = pg.exporters.ImageExporter(self.widget_3.plotItem)
        exporter3.export('fileName3.png')
        
        #stores the pictures files in image list
        self.image_list = ['fileName1.png','fileName2.png','fileName3.png']
        
        self.create_pdf()
        
    
    def check_widget(self):
        #a function checks the selected widget
        
        if self.comboBox.currentText() == "Widget1":
            self.current_widget = 0
            
        elif self.comboBox.currentText() == "Widget2":
            self.current_widget = 1
            
        elif self.comboBox.currentText() == "Widget3":
            self.current_widget = 2
    
    def plot_here (self, file, fileName):
        # the function that plot the graphs on the selected widget
        
        self.check_widget()
        self.widgets[self.current_widget].clear()
        name = fileName.split("/")[-1]
        self.widgets[self.current_widget].plotItem.setTitle("Channel " + str(self.current_widget + 1))
        self.widgets[self.current_widget].plotItem.addLegend(size=(1, 2))
        self.widgets[self.current_widget].plotItem.showGrid(True, True, alpha=1)
        self.widgets[self.current_widget].setXRange(0, 1000)
        self.widgets[self.current_widget].plotItem.setLabel("bottom", text="Time (ms)")
        self.widgets[self.current_widget].plot(file, name=name, pen = self.pens[self.current_widget])
        self.widgets[self.current_widget].plotItem.getViewBox().enableAutoRange(axis='y')            

    def plot_spectro(self,file):
        # the function that plot spectrogram of the selected signal

        self.check_widget
        plt.specgram(file,Fs=10)
        plt.xlabel('Time')
        plt.ylabel('Frequency')
        plt.savefig('images/spectro'+str(self.current_widget + 1)+'.png')
        self.spectroImg_list[self.current_widget] = 'images/spectro'+str(self.current_widget + 1)+'.png'
        plt.show()
        
        print("spectro")

    def start(self):
        # the function that makes the graph starts to move
        
        self.check_widget()
        self.isPaused = False
        self.isStoped = False
        data_length = self.widgets[self.current_widget].dataLength
        
        for x in range(0,data_length, 2):
            #increasing the x-axis range by x
            self.widgets[self.current_widget].setXRange(self.graph_rangeMin[self.current_widget] + x, self.graph_rangeMax[self.current_widget] + x)
            QtWidgets.QApplication.processEvents()

            if self.isPaused == True:
                #saving the new x-axis ranges
                self.graph_rangeMin[self.current_widget] = self.graph_rangeMin[self.current_widget] + x
                self.graph_rangeMax[self.current_widget] = self.graph_rangeMax[self.current_widget] + x
                break
            if self.isStoped == True:
                break

    def pause(self):
        self.check_widget()
        self.isPaused = True

    def stop(self):
        #the function that stops the graph
        
        self.check_widget()
        self.isStoped = True
        # reset the graph ranges
        self.widgets[self.current_widget].setXRange(0, 1000)
        self.graph_rangeMin[self.current_widget] = 0
        self.graph_rangeMax[self.current_widget] = 1000
        
    def create_pdf(self):
        #the function that creates the pdf report
        
        pdf = FPDF()
        
        for x in range(3):
            #try-except for handling errors
            try:
                # set pdf title
                pdf.add_page()
                pdf.set_font('Arial', 'B', 15)
                pdf.cell(70)
                pdf.cell(60, 10, 'Siganl Viewer Report', 1, 0, 'C')
                pdf.ln(20)
                # put the graphs on the pdf
                pdf.image(self.image_list[x], 10, 50, 190, 50)
                os.remove(self.image_list[x])
                pdf.image(self.spectroImg_list[x], 10, 110, 190, 100)
                os.remove(self.spectroImg_list[x])
            except:
                pass

        pdf.output("report.pdf", "F") 
        print("Report PDF is ready")    
    
    def zoom_in(self):
        self.check_widget
        self.widgets[self.current_widget].plotItem.getViewBox().scaleBy(x = 0.5, y = 1)
    
    def zoom_out(self):
        self.check_widget
        self.widgets[self.current_widget].plotItem.getViewBox().scaleBy(x = 2, y = 1)
    
    def move_right(self):
        self.check_widget
        self.widgets[self.current_widget].setXRange(self.graph_rangeMin[self.current_widget] + 100, self.graph_rangeMax[self.current_widget] + 100)

        self.graph_rangeMin[self.current_widget] = self.graph_rangeMin[self.current_widget] + 100
        self.graph_rangeMax[self.current_widget] = self.graph_rangeMax[self.current_widget] + 100
    
    def move_left(self):
        self.check_widget
        self.widgets[self.current_widget].setXRange(self.graph_rangeMin[self.current_widget] - 100, self.graph_rangeMax[self.current_widget] - 100)

        self.graph_rangeMin[self.current_widget] = self.graph_rangeMin[self.current_widget] - 100
        self.graph_rangeMax[self.current_widget] = self.graph_rangeMax[self.current_widget] - 100
        
    def show_popup(self, message, information):
        msg = QMessageBox()
        msg.setWindowTitle("Message")
        msg.setText(message)
        msg.setIcon(QMessageBox.Warning)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.setDefaultButton(QMessageBox.Ok)
        msg.setInformativeText(information)
        x = msg.exec_()
        

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = QtWidgets.QMainWindow()
    ui = Ui_mainWindow()
    ui.setupUi(mainWindow)
    mainWindow.show()
    sys.exit(app.exec_())
