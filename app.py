# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMessageBox, QAction, qApp, QMenu, QApplication, QDialog, QSystemTrayIcon, QStyle
from processor import Processor
import win10toast
import threading
import geoip2.database
import init
import sys  
import resourse_rc
import widget

class Scanner(QtWidgets.QMainWindow, widget.Ui_MainWindow):    # Main Processor ui class...

    def __init__(self):    # Main Processor ui class...
        super().__init__()
        
        self.setupUi(self)        
        self.index = 0      
        self.works = 0
        self.toaster = win10toast.ToastNotifier()
        self.toaster.show_toast("Proxy Ranger в сети", "Загрузите список прокси для проверки...", icon_path = "logo.ico", duration = 5, threaded = True)
    
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/img/logo.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

        self.tray = QSystemTrayIcon(self)
        self.tray.setToolTip("Proxy Ranger в сети...") 
        self.tray.setIcon(icon)
    
        act_01 = QAction(QIcon(":/img/up.png"), "Восстановить", self)
        act_02 = QAction(QIcon(":/img/down.png"), "Свернуть", self)
        act_03 = QAction(QIcon(":/img/settings.png"), "Настройки приложения...", self)
        act_04 = QAction(QIcon(":/img/exit.png"), "Выход", self)

        act_01.triggered.connect(self.show)
        act_02.triggered.connect(self.hide)
        act_04.triggered.connect(qApp.quit)
                

        menu = QMenu()
        menu.addAction(act_01)
        menu.addAction(act_02)
        menu.addAction(act_03)
        menu.addSeparator()
        menu.addAction(act_04)

        self.tray.setContextMenu(menu)
        self.tray.activated.connect(self.show)
        self.tray.show()

        header = self.tableWidget.horizontalHeader()    
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        
        self.statusBar().addPermanentWidget(self.label_08)
        self.statusBar().addPermanentWidget(self.label_05) 
        self.statusBar().addPermanentWidget(self.label_04)
        self.statusBar().addPermanentWidget(self.label_07)
        self.statusBar().addPermanentWidget(self.label_10)
        self.statusBar().addPermanentWidget(self.label_11) 
        self.statusBar().addPermanentWidget(self.label_12)
        self.statusBar().addPermanentWidget(self.label_09) 
        
        xloadAction = QAction("Загрузить список", self)
        xloadAction.setShortcut("Ctrl+F")
        xloadAction.setStatusTip("Загрузить список...")
        xloadAction.triggered.connect(self.select)
        
        xstartAction = QAction("Запустить", self)
        xstartAction.setShortcut("F5")
        xstartAction.setStatusTip("Запустить проверку...")
        xstartAction.triggered.connect(self.start)    

        xstopAction = QAction("Остановить", self)
        xstopAction.setShortcut("Esc")
        xstopAction.setStatusTip("Остановить проверку...")
        xstopAction.triggered.connect(self.stop)
        
        xclearAction = QAction("Очистить", self)
        xclearAction.setShortcut("Ctrl+C")
        xclearAction.setStatusTip("Очистить все...")
        xclearAction.triggered.connect(self.clear)
        
        xsetAction = QAction("Настройки", self)
        xsetAction.setShortcut("Ctrl+P")
        xsetAction.setStatusTip("Настройки...")
        xsetAction.triggered.connect(self.dialog)
        
        xtoolAction = QAction("Инструменты", self)
        xtoolAction.setShortcut("Ctrl+P")
        xtoolAction.setStatusTip("Инструменты...")
        xtoolAction.triggered.connect(self.dialog)

        
        loadAction = QAction(QIcon(":/img/add.png"), "Загрузить список", self)
        loadAction.setShortcut("Ctrl+F")
        loadAction.setStatusTip("Загрузить список...")
        loadAction.triggered.connect(self.select)
        
        startAction = QAction(QIcon(":/img/start.png"), "Запустить", self)
        startAction.setShortcut("F5")
        startAction.setStatusTip("Запустить проверку...")
        startAction.triggered.connect(self.start)    

        stopAction = QAction(QIcon(":/img/stop.png"), "Остановить", self)
        stopAction.setShortcut("Esc")
        stopAction.setStatusTip("Остановить проверку...")
        stopAction.triggered.connect(self.stop)
        
        clearAction = QAction(QIcon(":/img/clear.png"), "Очистить", self)
        clearAction.setShortcut("Ctrl+C")
        clearAction.setStatusTip("Очистить все...")
        clearAction.triggered.connect(self.clear)
        
        setAction = QAction(QIcon(":/img/settings.png"), "Настройки", self)
        setAction.setShortcut("Ctrl+P")
        setAction.setStatusTip("Настройки...")
        setAction.triggered.connect(self.dialog)
        
        toolAction = QAction(QIcon(":/img/tools.png"), "Инструменты", self)
        toolAction.setShortcut("Ctrl+P")
        toolAction.setStatusTip("Инструменты...")
        toolAction.triggered.connect(self.dialog)

        exitAction = QAction(QIcon(":/img/exit.png"), "Выход", self)
        exitAction.setShortcut("Ctrl+E")
        exitAction.setStatusTip("Выход из приложения...")
        exitAction.triggered.connect(qApp.quit)


        fileMenu = self.menuBar.addMenu("File")
        fileMenu.addAction(xloadAction)
        fileMenu.addAction(xstartAction)
        fileMenu.addAction(xstopAction)
        
        fileMenu.addSeparator()
        fileMenu.addAction(exitAction)

        editMenu = self.menuBar.addMenu("Edit")
        editMenu.addAction(xclearAction)
        
        optiMenu = self.menuBar.addMenu("Options")
        optiMenu.addAction(xsetAction)
        
        toolMenu = self.menuBar.addMenu("Tools")
        toolMenu.addAction(xtoolAction)
  
        self.toolbar = self.addToolBar("Toolbar")   # Add toolbar...
        self.toolbar.addAction(loadAction)
        self.toolbar.addAction(startAction)
        self.toolbar.addAction(stopAction)
        self.toolbar.addAction(setAction)
        self.toolbar.addAction(clearAction)
        self.toolbar.addAction(toolAction)
    
    
    
    def progress(self, size):    # Progress bar metod...
        self.text = self.lineEdit.text()
        
        with  open(self.text, encoding = 'iso-8859-1') as file:
            self.spase = len(file.readlines())
            self.bars = size / self.spase * 100
            
            self.progressBar.setValue(self.bars)

     
                
    def append(self, background, ipaddress, enaddress, types, sessions, response):    # Append stream metod...
    
        try: 
            locat = geoip2.database.Reader("../country/country.mmdb")
            c = locat.country(ipaddress)
            country = c.country.name
            
        except geoip2.errors.AddressNotFoundError:
            c = locat.country("162.162.162.162")
            country = c.country.name
            
        except ValueError:
            c = locat.country("162.162.162.162")
            country = c.country.name
       
        index = 0
        self.index = self.index + 1

        index = self.index - 1
        self.progress(self.index)    # Progress bar metod...

        rcount = self.label_05.text()
        rres = self.label_07.text()
        rcount = int(rcount)
        rres = int(rres)
        r = rcount - rres
        print(r)
        self.label_07.setText(str(index))
        self.label_09.setText(str(r))

        check = QtWidgets.QCheckBox()
        self.tableWidget.setCellWidget(index, 0, check)        
      
        item = QtWidgets.QTableWidgetItem(ipaddress)
        self.tableWidget.setItem(index, 1, item) 
        
        item = QtWidgets.QTableWidgetItem(enaddress)
        item.setBackground(QtGui.QColor(237, 237, 237))
        self.tableWidget.setItem(index, 2, item)               

        item = QtWidgets.QTableWidgetItem(country)
        item.setForeground(QtGui.QColor(177, 177, 177))
        self.tableWidget.setItem(index, 3, item)               

        titem = QtWidgets.QTableWidgetItem(types)
        self.tableWidget.setItem(index, 4, titem)               

        sitem = QtWidgets.QTableWidgetItem(sessions)
        self.tableWidget.setItem(index, 5, sitem)               

        item = QtWidgets.QTableWidgetItem(response)
        self.tableWidget.setItem(index, 6, item)               
        
 
        if background != 0:
            self.works = self.works + 1
            self.label_11.setText(str(self.works))
            check.setStyleSheet("QCheckBox::indicator {background-image: url(:/img/accept.png); background-repeat: no-repeat; background-position: center; width: 14px; height: 14px;}" "QCheckBox {margin: 8px;}")
            titem.setForeground(QtGui.QColor(77, 187, 85))
      
            sitem.setBackground(QtGui.QColor(126, 224, 120))
            sitem.setForeground(QtGui.QColor(255, 255, 255))
           
            self.writer(ipaddress, enaddress)

        else:

            check.setStyleSheet("QCheckBox::indicator {background-image: url(:/img/delete.png); background-repeat: no-repeat; background-position: center; width: 14px; height: 14px;}" "QCheckBox {margin: 8px;}")
            
        self.tableWidget.repaint()
        self.tableWidget.scrollToItem(item)

        

    def writer(self, ipaddress, enaddress):    # Write data file metod...
    
        with open("e_output.txt", "a") as files:
            files.write(ipaddress + ":" + enaddress + "\n")    
            

    def start(self):    # Start stream metod...
        
        value = self.spinBox.value() 
        files = self.lineEdit.text()
        delay = self.spinBox_2.text()
        timeout = self.spinBox_3.text()
        
        delay = int(delay)
        delay = delay / 10

        self.th = Processor(files, value, timeout, delay)
        self.th.length.connect(self.append)
        threading.Thread(target = self.th.running).start()
        
        print("Started...")


    def dialog(self):    # Settings dialog  metod...
    
        self.dialog = QDialog()
        self.dialog.resize(300, 300)
        self.dialog.setWindowIcon(QtGui.QIcon(":/img/settings.png")) 
        self.dialog.setWindowTitle("Настройки")
        
        self.cbox = QtWidgets.QCheckBox("Save works", self.dialog)
        self.cbox.setGeometry(QtCore.QRect(20, 20, 150, 20))

        self.buttonBox = QtWidgets.QDialogButtonBox(self.dialog)
        self.buttonBox.setGeometry(QtCore.QRect(30, 200, 200, 30))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.dialog.setWindowModality(QtCore.Qt.ApplicationModal)
        self.dialog.exec_()
	
    
    def clear(self):    # Clear data app metod...
    
        self.tableWidget.setRowCount(0)
        self.tableWidget.setRowCount(12)
        self.label_05.setText("0")
        self.label_07.setText("0")
        self.label_09.setText("0")
        self.label_11.setText("0")       
        self.statusBar().showMessage("Reset data...")
        
    
    def stop(self):    # Stop stream metod...
        self.th.stop()
        
        print("Stoped...")
        
   
    def select(self):    # Select list metod...
    
        self.file = QtWidgets.QFileDialog.getOpenFileName(self, "Select file", "C:",  "(*.txt)")[0]
        if self.file != "":
            self.lineEdit.setText(self.file)
            self.count = open(self.file, encoding = "iso-8859-1").readlines()
            self.count = len(self.count)
            self.count = int(self.count)
            self.label_05.setText(str(self.count))
            self.tableWidget.setRowCount(self.count)
            self.statusBar().showMessage("List add...")
        else:
            pass
            

       

def main():
    app = QtWidgets.QApplication(sys.argv)    # Main window start metod...
    window = Scanner()
    window.show()
    app.exec_()

if __name__ == '__main__':    # App start metod...
    main()