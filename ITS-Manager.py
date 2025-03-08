import sys
import os
import json, csv
from datetime import datetime

from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget,
                             QHBoxLayout, QTableWidget, QTableWidgetItem,
                             QToolBar,QAction, QSplitter, QFrame,
                             QStatusBar, QDialog, QHeaderView, QLabel,
                             QSizePolicy, QPushButton, QVBoxLayout,
                             QComboBox,
                             QHBoxLayout, QStackedWidget, QAbstractItemView,
                             QLineEdit, QDesktopWidget, QShortcut)
from PyQt5.QtGui import QIcon, QFont, QColor, QPalette, QKeySequence
from PyQt5.Qt import Qt
from PyQt5 import QtCore
from PyQt5.QtCore import QTimer

class MainWindow(QMainWindow):
    
    def __init__(self, parent):
        super().__init__()
        
        self.master = parent
        self.setWindowTitle('Intensivstation DRK Krankenhaus Neustrelitz')
        self.path = self.getPath()
        self.setWindowIcon(QIcon(self.path + 'ITS-Manager.png'))
        self.initUI()
        self.initComboBox()
        
        # load all tables
        self.loadTable1()
        self.loadTable2()
        self.loadTable3()
        self.loadTable4()
        self.loadTable5()
        self.loadTable6()
        self.loadTable7()
        self.loadTable8()
    
    def getPath(self):
        try:
            base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.patch.abspath(__file__)))
            base_path += '/'
        except Exception:
            base_path = os.path.dirname(__file__) + "/"

        if '\\' in base_path:
            base_path = base_path.replace('\\', '/')
        
        return base_path
    
    def updateDateTime(self):
        date = datetime.today().strftime("%d-%m-%Y")
        self.datum_label.setText(date)
        time = datetime.today().strftime("%H:%M")
        self.time_label.setText(time)
    
    def toggleFullScreen(self):

        if self.isFullScreen() or self.showMaximized():
            self.showMaximized()
        else:
            self.showFullScreen()
        
        self.saveAll()
        self.clearSelections()
        
    
    def clearSelections(self):
        self.table1.clearSelection()
        self.table2.clearSelection()
        self.table3.clearSelection()
        self.table4.clearSelection()
        self.table5.clearSelection()
        self.table6.clearSelection()
        self.table7.clearSelection()
        self.table8.clearSelection()
    
    def initUI(self):
        
        #avGeom = QDesktopWidget().availableGeometry()
        #self.setGeometry(avGeom)
        
        #self.screenSize = self.master.primaryScreen().size()
        self.setGeometry(100, 100, 1700, 900)
        self.showMaximized()
        
        self.setFullscreen = QShortcut(QKeySequence("F5"), self)
        self.setFullscreen.activated.connect(self.toggleFullScreen)
        
        font = QFont("Arial", 18)
        
        self.timer1 = QTimer()
        self.timer1.setInterval(1000) # 1000 ms
        self.timer1.timeout.connect(self.updateDateTime)
        self.timer1.start()
        
        self.datum_label = QLabel()
        self.datum_label.setAlignment(Qt.AlignCenter)
        self.datum_label.setFont(font)
        self.time_label = QLabel()
        self.time_label.setAlignment(Qt.AlignCenter)
        self.time_label.setFont(font)
        self.updateDateTime()
        self.drk_label = QLabel()
        self.drk_label.setAlignment(Qt.AlignCenter)
        self.drk_label.setFont(font)
        self.drk_label.setText('Intensivstation DRK Krankenhaus Neustrelitz')
        
        self.button = QPushButton("OK")
        self.button.setFont(font)
        self.button.setStyleSheet("background-color : lightblue")
        self.button.clicked.connect(self.button_ok)  
         
        layout1 = QHBoxLayout()
        layout2 = QVBoxLayout()
        layout3 = QVBoxLayout()  
        layout4 = QVBoxLayout()
        
        splitter1 = QSplitter(Qt.Horizontal)
        splitter2 = QSplitter(Qt.Vertical)
        splitter3 = QSplitter(Qt.Vertical)
        
        # get list data
        self.aerzte = self.loadFromJson(self.path + 'aerzte.json')
        self.pflege = self.loadFromJson(self.path + 'pflege.json')
        self.abteilung = self.loadFromJson(self.path + 'abteilung.json')
        self.aufgaben = self.loadFromJson(self.path + 'aufgaben.json')
        self.CAVE = self.loadFromJson(self.path + 'cave.json')
        self.notfall = self.loadFromJson(self.path + 'notfall.json')
        self.aufnahme = self.loadFromJson(self.path + 'aufnahme.json')
        self.kostform = self.loadFromJson(self.path + 'kostform.json')
        self.raum = self.loadFromJson(self.path + 'raum.json')
        
        ##
        # self.table1 -> splitter1 (Qt.Horizontal)
        ##
        
        self.table1 = QTableWidget()

        self.table1.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table1.setFont(font)
        
        self.table1.setRowCount(24);
        self.table1.setColumnCount(7);
        
        header_labels = ['        CAVE        ', 'Abteilung', 'Pflegekraft', '        Arzt       ', 'Fon', '       Aufgaben       ', '     Kostform     ']
        self.table1.setHorizontalHeaderLabels(header_labels)
        
        self.table1.resizeRowsToContents();
        self.table1.resizeColumnsToContents();
        #self.table1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        vertical_labels = [' 1 ', '', '', '2.1', '', '', '2.2', '', '', ' 3 ', '', '', '4.1', '', '', '4.2', '', '', ' 5 ', '', '', ' 6 ', '', '']
        self.table1.setVerticalHeaderLabels(vertical_labels)
        #self.table1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        # colorize gray
        for i in range(7):
            self.set_BG_Gray(self.table1, 0, i)
            self.set_BG_Gray(self.table1, 1, i)
            self.set_BG_Gray(self.table1, 2, i)
            
            self.set_BG_Gray(self.table1, 6, i)
            self.set_BG_Gray(self.table1, 7, i)
            self.set_BG_Gray(self.table1, 8, i)

            self.set_BG_Gray(self.table1, 12, i)
            self.set_BG_Gray(self.table1, 13, i)
            self.set_BG_Gray(self.table1, 14, i)
            
            self.set_BG_Gray(self.table1, 18, i)
            self.set_BG_Gray(self.table1, 19, i)
            self.set_BG_Gray(self.table1, 20, i)

        # colorize white
        for i in range(7):
            self.set_BG_White(self.table1, 3, i)
            self.set_BG_White(self.table1, 4, i)
            self.set_BG_White(self.table1, 5, i)
            
            self.set_BG_White(self.table1, 9, i)
            self.set_BG_White(self.table1, 10, i)
            self.set_BG_White(self.table1, 11, i)
            
            self.set_BG_White(self.table1, 15, i)
            self.set_BG_White(self.table1, 16, i)
            self.set_BG_White(self.table1, 17, i)
            
            self.set_BG_White(self.table1, 21, i)
            self.set_BG_White(self.table1, 22, i)
            self.set_BG_White(self.table1, 23, i)
        
        # colorize CAVE in yellow
        for i in range(25):
            if (i == 0) or (i == 3) or (i == 6) or (i == 9) or (i == 12) or \
                (i == 15) or (i == 18) or (i == 21):
                self.set_BG_Yellow_FG_Red(self.table1, i,0)
            else:
                continue
        
        self.table1.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        self.table1.setShowGrid(False)
        
        ##
        # self.table2 
        ##
        
        self.table2 = QTableWidget()
        self.table2.setFont(font)
        self.table2.setRowCount(3);
        self.table2.setColumnCount(2);
        header_labels2 = ['  Akut-Aufnahmen  ', ' Uhrzeit ']
        self.table2.setHorizontalHeaderLabels(header_labels2)
        
        self.table2.resizeRowsToContents();
        self.table2.resizeColumnsToContents();
        self.table2.verticalHeader().hide()
        self.table2.setShowGrid(False)

        self.table2.setSelectionMode(QAbstractItemView.SingleSelection)
        
        # set Color
        for i in range(3):
            for j in range(2):
                self.set_BG_Color(self.table2, i, j, (255,102,102))
        ##
        # self.table3 
        ##
        
        self.table3 = QTableWidget()
        self.table3.setFont(font)
        self.table3.setRowCount(6);
        self.table3.setColumnCount(2);
        
        header_labels3 = ['Geplante Aufnahmen', ' Uhrzeit ']
        self.table3.setHorizontalHeaderLabels(header_labels3)
        
        self.table3.resizeRowsToContents();
        self.table3.resizeColumnsToContents();
        self.table3.verticalHeader().hide()
        self.table3.setShowGrid(False)
        self.table3.setSelectionMode(QAbstractItemView.SingleSelection)
        
        # set Color
        for i in range(6):
            for j in range(2):
                self.set_BG_Color(self.table3, i, j, (255,255, 153))
        
        ##
        # self.table4 
        ##
        self.table4 = QTableWidget()
        self.table4.setFont(font)
        self.table4.setRowCount(6);
        self.table4.setColumnCount(2);
        header_labels4 = ['   Verlegungen    ', ' Uhrzeit ']
        self.table4.setHorizontalHeaderLabels(header_labels4)
        
        self.table4.resizeRowsToContents();
        self.table4.resizeColumnsToContents();
        self.table4.verticalHeader().hide()  
        self.table4.setShowGrid(False) 
        self.table4.setSelectionMode(QAbstractItemView.SingleSelection)
        
        # set Color
        for i in range(7):
            for j in range(2):
                self.set_BG_Color(self.table4, i, j, (153,255, 153))
        
        ##
        # self.table5 
        ## 
        self.table5 = QTableWidget()
        self.table5.setFont(font)
        self.table5.setRowCount(3);
        self.table5.setColumnCount(1);
        header_labels5 = ['       Notfall-Team       ']
        self.table5.setHorizontalHeaderLabels(header_labels5)
        
        self.table5.resizeRowsToContents();
        self.table5.resizeColumnsToContents();
        vertical_labels5 = [' Früh ', ' Spät ', 'Nacht']  
        #self.table5.verticalHeader().hide()  
        self.table5.setVerticalHeaderLabels(vertical_labels5)
        self.table5.setShowGrid(False) 
        self.table5.setSelectionMode(QAbstractItemView.SingleSelection)
        
        # set Color
        for i in range(3):
            for j in range(1):
                self.set_BG_Color(self.table5, i, j, (255,102,102))
        
        ##
        # self.table6
        ## 
        self.table6 = QTableWidget()
        self.table6.setFont(font)
        self.table6.setRowCount(3);
        self.table6.setColumnCount(1);
        header_labels6 = [' Schichtleitung Pflege ']
        self.table6.setHorizontalHeaderLabels(header_labels6)
        vertical_labels6 = [' Früh ', ' Spät ', 'Nacht']
        self.table6.setVerticalHeaderLabels(vertical_labels6)
        self.table6.resizeRowsToContents();
        self.table6.resizeColumnsToContents(); 
        self.table6.setShowGrid(False) 
        self.table6.setSelectionMode(QAbstractItemView.SingleSelection)
        
        # set Color
        for i in range(3):
            for j in range(1):
                self.set_BG_Color(self.table6, i, j, (255,255, 153))
        
        ##
        # self.table7 
        ## 
        self.table7 = QTableWidget()
        self.table7.setFont(font)
        self.table7.setRowCount(1);
        self.table7.setColumnCount(2);
        header_labels7 = ['  Schichtleitung Arzt  ', ' Fon ']
        self.table7.setHorizontalHeaderLabels(header_labels7)
        
        self.table7.resizeRowsToContents();
        self.table7.resizeColumnsToContents();
        self.table7.verticalHeader().hide()  
        self.table7.setShowGrid(False) 
        self.table7.setSelectionMode(QAbstractItemView.SingleSelection)
        
        # set Color
        for i in range(1):
            for j in range(2):
                self.set_BG_Color(self.table7, i, j, (153,255, 153))
        

        ##
        # self.table8 
        ## 
        self.table8 = QTableWidget()
        self.table8.setFont(font)
        self.table8.setRowCount(2);
        self.table8.setColumnCount(2);
        header_labels8 = ['Ärztl. Dienst / Rufdienst', ' Fon ']
        self.table8.setHorizontalHeaderLabels(header_labels8)
        
        self.table8.resizeRowsToContents();
        self.table8.resizeColumnsToContents();
        self.table8.verticalHeader().hide()  
        self.table8.setShowGrid(False) 
        self.table8.setSelectionMode(QAbstractItemView.SingleSelection)
        
        # set Color
        for i in range(2):
            for j in range(2):
                self.set_BG_Color(self.table8, i, j, (153,153, 255))
        
        
        ###
        ## arrange all
        ###
        
        layout2.addWidget(self.datum_label)
        layout2.addWidget(self.table2)
        layout2.addWidget(self.table3)
        layout2.addWidget(self.table4)
        layout2.addWidget(self.button)

        layout3.addWidget(self.time_label)
        layout3.addWidget(self.table5)
        layout3.addWidget(self.table6)
        layout3.addWidget(self.table7)
        layout3.addWidget(self.table8)
        
        widget1 = QFrame()
        widget2 = QFrame()
        widget2.setLayout(layout2)
        widget3 = QFrame()
        widget3.setLayout(layout3)
        
        splitter1.addWidget(self.table1)
        layout1.addWidget(splitter1, 55)
        layout1.addWidget(widget2, 23)
        layout1.addWidget(widget3, 22)
        widget1.setLayout(layout1)
        
        widget1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        widget2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        widget3.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.setCentralWidget(widget1)
    
    def label_vertical_table1(self, row, column, text):
        i = self.table1.item(row, column)
        i.setText(text)
    
    def set_BG_Yellow_FG_Red(self, table, x, y):
        item = QTableWidgetItem()
        item.setBackground(QColor(255, 255, 153))
        item.setTextAlignment(Qt.AlignHCenter)
        item.setForeground(QColor(255, 0, 0))
        table.setItem(x,y,item)

    def set_BG_Gray(self, table, x, y):
        item = QTableWidgetItem()
        item.setBackground(QColor(238, 238, 238))
        item.setTextAlignment(Qt.AlignHCenter)
        table.setItem(x,y,item)
    
    def set_BG_White(self, table, x, y):
        item = QTableWidgetItem()
        item.setBackground(QColor(255, 255, 255))
        item.setTextAlignment(Qt.AlignHCenter)
        table.setItem(x,y,item)
    
    def set_BG_Color(self, table, x, y, color):
        r,g,b = color
        item = QTableWidgetItem()
        item.setBackground(QColor(r,g,b))
        item.setTextAlignment(Qt.AlignHCenter)
        table.setItem(x,y,item)
    
    def makeComboBox(self, liste, color, fgcolor=(0,0,0)):
        r,g,b = color
        r2,g2,b2 = fgcolor
        combobox = QComboBox()
        combobox.setEditable(True)
        backColor = QColor(r, g, b)
        forecolor = QColor(r2, g2, b2)
        lineEditor = combobox.lineEdit()
        pal = lineEditor.palette()
        pal.setColor(QPalette.Base, backColor)
        pal.setColor(QPalette.Text, forecolor)
        lineEditor.setPalette(pal)
        lineEditor.setAlignment(Qt.AlignCenter)
        combobox.addItems(liste)

        return combobox
    
    def initComboBox(self):
        
        ###
        #  self.table1 
        ##
        
        ## -> color ComboBox / init with json data
        
        ##
        # Raum 1
        ##
        self.combo_cave_1_01 = self.makeComboBox(self.CAVE, (255, 255, 153), (255,0,0))
        self.table1.setCellWidget(0, 0, self.combo_cave_1_01)

        self.combo_cave_1_02 = self.makeComboBox(self.CAVE, (255, 255, 153), (255,0,0))
        self.table1.setCellWidget(1, 0, self.combo_cave_1_02)
        
        self.combo_abteilung_1 = self.makeComboBox(self.abteilung, (238,238, 238))
        self.table1.setCellWidget(0, 1, self.combo_abteilung_1)
        
        self.combo_pflege_1 = self.makeComboBox(self.pflege, (238,238, 238))
        self.table1.setCellWidget(0, 2, self.combo_pflege_1)
        
        self.combo_arzt_1 = self.makeComboBox(self.aerzte, (238,238, 238))
        self.table1.setCellWidget(0, 3, self.combo_arzt_1)
        
        self.combo_aufgaben_01 = self.makeComboBox(self.aufgaben, (238,238,238), (0,0,255))
        self.table1.setCellWidget(0, 5, self.combo_aufgaben_01)   
        
        self.combo_aufgaben_02 = self.makeComboBox(self.aufgaben, (238,238,238), (0,0,255))
        self.table1.setCellWidget(1, 5, self.combo_aufgaben_02)   

        self.combo_kostform_01 = self.makeComboBox(self.kostform, (238,238,238))
        self.table1.setCellWidget(0, 6, self.combo_kostform_01)            
        
        
        ##
        # Raum 2.1
        ##
        self.combo_cave_21_01 = self.makeComboBox(self.CAVE, (255, 255, 153), (255,0,0))
        self.table1.setCellWidget(3, 0, self.combo_cave_21_01)
        
        self.combo_cave_21_02 = self.makeComboBox(self.CAVE, (255, 255, 153), (255,0,0))
        self.table1.setCellWidget(4, 0, self.combo_cave_21_02)
        
        self.combo_abteilung_21 = self.makeComboBox(self.abteilung, (255,255, 255))
        self.table1.setCellWidget(3, 1, self.combo_abteilung_21)
        
        self.combo_pflege_21 = self.makeComboBox(self.pflege, (255,255, 255))
        self.table1.setCellWidget(3, 2, self.combo_pflege_21)
        
        self.combo_arzt_21 = self.makeComboBox(self.aerzte, (255,255, 255))
        self.table1.setCellWidget(3, 3, self.combo_arzt_21)

        self.combo_aufgaben_21_01 = self.makeComboBox(self.aufgaben, (255,255,255), (0,0,255))
        self.table1.setCellWidget(3, 5, self.combo_aufgaben_21_01)
        
        self.combo_aufgaben_21_02 = self.makeComboBox(self.aufgaben, (255,255,255), (0,0,255))
        self.table1.setCellWidget(4, 5, self.combo_aufgaben_21_02)

        self.combo_kostform_21 = self.makeComboBox(self.kostform, (255,255,255))
        self.table1.setCellWidget(3, 6, self.combo_kostform_21)            
        
        ## ---- to do ----
        
        ##
        # Raum 2.2
        ##
        self.combo_cave_22_01 = self.makeComboBox(self.CAVE, (255, 255, 153), (255,0,0))
        self.table1.setCellWidget(6, 0, self.combo_cave_22_01)

        self.combo_cave_22_02 = self.makeComboBox(self.CAVE, (255, 255, 153), (255,0,0))
        self.table1.setCellWidget(7, 0, self.combo_cave_22_02)
        
        self.combo_abteilung_22 = self.makeComboBox(self.abteilung, (238,238, 238))
        self.table1.setCellWidget(6, 1, self.combo_abteilung_22)
        
        self.combo_pflege_22 = self.makeComboBox(self.pflege, (238,238, 238))
        self.table1.setCellWidget(6, 2, self.combo_pflege_22)
        
        self.combo_arzt_22 = self.makeComboBox(self.aerzte, (238,238, 238))
        self.table1.setCellWidget(6, 3, self.combo_arzt_22)

        self.combo_aufgaben_22_01 = self.makeComboBox(self.aufgaben, (238,238, 238), (0,0,255))
        self.table1.setCellWidget(6, 5, self.combo_aufgaben_22_01)

        self.combo_aufgaben_22_02 = self.makeComboBox(self.aufgaben, (238,238, 238), (0,0,255))
        self.table1.setCellWidget(7, 5, self.combo_aufgaben_22_02)

        self.combo_kostform_22 = self.makeComboBox(self.kostform, (238,238,238))
        self.table1.setCellWidget(6, 6, self.combo_kostform_22)            

        ##
        # Raum 3
        ##
        self.combo_cave_3_01 = self.makeComboBox(self.CAVE, (255, 255, 153), (255,0,0))
        self.table1.setCellWidget(9, 0, self.combo_cave_3_01)

        self.combo_cave_3_02 = self.makeComboBox(self.CAVE, (255, 255, 153), (255,0,0))
        self.table1.setCellWidget(10, 0, self.combo_cave_3_02)
  
        self.combo_abteilung_3 = self.makeComboBox(self.abteilung, (255,255, 255))
        self.table1.setCellWidget(9, 1, self.combo_abteilung_3)
        
        self.combo_pflege_3 = self.makeComboBox(self.pflege, (255,255, 255))
        self.table1.setCellWidget(9, 2, self.combo_pflege_3)
        
        self.combo_arzt_3 = self.makeComboBox(self.aerzte, (255,255, 255))
        self.table1.setCellWidget(9, 3, self.combo_arzt_3)

        self.combo_aufgaben_3_01 = self.makeComboBox(self.aufgaben, (255,255,255), (0,0,255))
        self.table1.setCellWidget(9, 5, self.combo_aufgaben_3_01)

        self.combo_aufgaben_3_02 = self.makeComboBox(self.aufgaben, (255,255,255), (0,0,255))
        self.table1.setCellWidget(10, 5, self.combo_aufgaben_3_02)
        
        self.combo_kostform_3 = self.makeComboBox(self.kostform, (255,255,255))
        self.table1.setCellWidget(9, 6, self.combo_kostform_3)  

        ##
        # Raum 4.1
        ##
        self.combo_cave_41_01 = self.makeComboBox(self.CAVE, (255, 255, 153), (255,0,0))
        self.table1.setCellWidget(12, 0, self.combo_cave_41_01)

        self.combo_cave_41_02 = self.makeComboBox(self.CAVE, (255, 255, 153), (255,0,0))
        self.table1.setCellWidget(13, 0, self.combo_cave_41_02)
        
        self.combo_abteilung_41 = self.makeComboBox(self.abteilung, (238,238, 238))
        self.table1.setCellWidget(12, 1, self.combo_abteilung_41)
        
        self.combo_pflege_41 = self.makeComboBox(self.pflege, (238,238, 238))
        self.table1.setCellWidget(12, 2, self.combo_pflege_41)
        
        self.combo_arzt_41 = self.makeComboBox(self.aerzte, (238,238, 238))
        self.table1.setCellWidget(12, 3, self.combo_arzt_41)

        self.combo_aufgaben_41_01 = self.makeComboBox(self.aufgaben, (238,238, 238), (0,0,255))
        self.table1.setCellWidget(12, 5, self.combo_aufgaben_41_01)

        self.combo_aufgaben_41_02 = self.makeComboBox(self.aufgaben, (238,238, 238), (0,0,255))
        self.table1.setCellWidget(13, 5, self.combo_aufgaben_41_02)

        self.combo_kostform_41 = self.makeComboBox(self.kostform, (238,238,238))
        self.table1.setCellWidget(12, 6, self.combo_kostform_41)  

        ##
        # Raum 4.2
        ##
        self.combo_cave_42_01 = self.makeComboBox(self.CAVE, (255, 255, 153), (255,0,0))
        self.table1.setCellWidget(15, 0, self.combo_cave_42_01)

        self.combo_cave_42_02 = self.makeComboBox(self.CAVE, (255, 255, 153), (255,0,0))
        self.table1.setCellWidget(16, 0, self.combo_cave_42_02)
        
        self.combo_abteilung_42 = self.makeComboBox(self.abteilung, (255,255, 255))
        self.table1.setCellWidget(15, 1, self.combo_abteilung_42)
        
        self.combo_pflege_42 = self.makeComboBox(self.pflege, (255,255, 255))
        self.table1.setCellWidget(15, 2, self.combo_pflege_42)
        
        self.combo_arzt_42 = self.makeComboBox(self.aerzte, (255,255, 255))
        self.table1.setCellWidget(15, 3, self.combo_arzt_42)

        self.combo_aufgaben_42_01 = self.makeComboBox(self.aufgaben, (255,255,255), (0,0,255))
        self.table1.setCellWidget(15, 5, self.combo_aufgaben_42_01)

        self.combo_aufgaben_42_02 = self.makeComboBox(self.aufgaben, (255,255,255), (0,0,255))
        self.table1.setCellWidget(16, 5, self.combo_aufgaben_42_02)

        self.combo_kostform_42 = self.makeComboBox(self.kostform, (255,255,255))
        self.table1.setCellWidget(15, 6, self.combo_kostform_42) 

        ##
        # Raum 5
        ##
        self.combo_cave_5_01 = self.makeComboBox(self.CAVE, (255, 255, 153), (255,0,0))
        self.table1.setCellWidget(18, 0, self.combo_cave_5_01)

        self.combo_cave_5_02 = self.makeComboBox(self.CAVE, (255, 255, 153), (255,0,0))
        self.table1.setCellWidget(19, 0, self.combo_cave_5_02)
        
        self.combo_abteilung_5 = self.makeComboBox(self.abteilung, (238,238, 238))
        self.table1.setCellWidget(18, 1, self.combo_abteilung_5)
        
        self.combo_pflege_5 = self.makeComboBox(self.pflege, (238,238, 238))
        self.table1.setCellWidget(18, 2, self.combo_pflege_5)
        
        self.combo_arzt_5 = self.makeComboBox(self.aerzte, (238,238, 238))
        self.table1.setCellWidget(18, 3, self.combo_arzt_5)

        self.combo_aufgaben_5_01 = self.makeComboBox(self.aufgaben, (238,238, 238), (0,0,255))
        self.table1.setCellWidget(18, 5, self.combo_aufgaben_5_01)

        self.combo_aufgaben_5_02 = self.makeComboBox(self.aufgaben, (238,238, 238), (0,0,255))
        self.table1.setCellWidget(19, 5, self.combo_aufgaben_5_02)

        self.combo_kostform_5 = self.makeComboBox(self.kostform, (238,238,238))
        self.table1.setCellWidget(18, 6, self.combo_kostform_5)  

        ##
        # Raum 6
        ##
        self.combo_cave_6_01 = self.makeComboBox(self.CAVE, (255, 255, 153), (255,0,0))
        self.table1.setCellWidget(21, 0, self.combo_cave_6_01)

        self.combo_cave_6_02 = self.makeComboBox(self.CAVE, (255, 255, 153), (255,0,0))
        self.table1.setCellWidget(22, 0, self.combo_cave_6_02)
   
        self.combo_abteilung_6 = self.makeComboBox(self.abteilung, (255,255, 255))
        self.table1.setCellWidget(21, 1, self.combo_abteilung_6)
        
        self.combo_pflege_6 = self.makeComboBox(self.pflege, (255,255, 255))
        self.table1.setCellWidget(21, 2, self.combo_pflege_6)
        
        self.combo_arzt_6 = self.makeComboBox(self.aerzte, (255,255, 255))
        self.table1.setCellWidget(21, 3, self.combo_arzt_6)

        self.combo_aufgaben_6_01 = self.makeComboBox(self.aufgaben, (255,255,255), (0,0,255))
        self.table1.setCellWidget(21, 5, self.combo_aufgaben_6_01)

        self.combo_aufgaben_6_02 = self.makeComboBox(self.aufgaben, (255,255,255), (0,0,255))
        self.table1.setCellWidget(22, 5, self.combo_aufgaben_6_02)

        self.combo_kostform_6 = self.makeComboBox(self.kostform, (255,255,255))
        self.table1.setCellWidget(21, 6, self.combo_kostform_6) 

        ###
        # self.table2
        ##
        
        self.combo_notfall_1 = self.makeComboBox(self.notfall, (255,102,102))
        self.table2.setCellWidget(0, 0, self.combo_notfall_1)
        
        self.combo_notfall_2 = self.makeComboBox(self.notfall, (255,102,102))
        self.table2.setCellWidget(1, 0, self.combo_notfall_2)

        self.combo_notfall_3 = self.makeComboBox(self.notfall, (255,102,102))
        self.table2.setCellWidget(2, 0, self.combo_notfall_3)
        
        ###
        # self.table3
        ##
        
        self.combo_aufnahme_1 = self.makeComboBox(self.aufnahme, (255,255, 153))
        self.table3.setCellWidget(0, 0, self.combo_aufnahme_1)
        
        self.combo_aufnahme_2 = self.makeComboBox(self.aufnahme, (255,255, 153))
        self.table3.setCellWidget(1, 0, self.combo_aufnahme_2)

        self.combo_aufnahme_3 = self.makeComboBox(self.aufnahme, (255,255, 153))
        self.table3.setCellWidget(2, 0, self.combo_aufnahme_3)

        self.combo_aufnahme_4 = self.makeComboBox(self.aufnahme, (255,255, 153))
        self.table3.setCellWidget(3, 0, self.combo_aufnahme_4)
        
        self.combo_aufnahme_5 = self.makeComboBox(self.aufnahme, (255,255, 153))
        self.table3.setCellWidget(4, 0, self.combo_aufnahme_5)

        self.combo_aufnahme_6 = self.makeComboBox(self.aufnahme, (255,255, 153))
        self.table3.setCellWidget(5, 0, self.combo_aufnahme_6)
        
        ###
        # self.table4
        ##
        
        self.combo_verlegung_1 = self.makeComboBox(self.raum, (153,255, 153))
        self.table4.setCellWidget(0, 0, self.combo_verlegung_1)
        
        self.combo_verlegung_2 = self.makeComboBox(self.raum, (153,255, 153))
        self.table4.setCellWidget(1, 0, self.combo_verlegung_2)
        
        self.combo_verlegung_3 = self.makeComboBox(self.raum, (153,255, 153))
        self.table4.setCellWidget(2, 0, self.combo_verlegung_3)

        self.combo_verlegung_4 = self.makeComboBox(self.raum, (153,255, 153))
        self.table4.setCellWidget(3, 0, self.combo_verlegung_4)
        
        self.combo_verlegung_5 = self.makeComboBox(self.raum, (153,255, 153))
        self.table4.setCellWidget(4, 0, self.combo_verlegung_5)

        self.combo_verlegung_6 = self.makeComboBox(self.raum, (153,255, 153))
        self.table4.setCellWidget(5, 0, self.combo_verlegung_6)       
 
        ###
        # self.table5
        ##

        self.combo_pflegeNotfall_FD = self.makeComboBox(self.pflege, (255,102,102))
        self.table5.setCellWidget(0, 0, self.combo_pflegeNotfall_FD)
        
        self.combo_pflegeNotfall_SD = self.makeComboBox(self.pflege, (255,102,102))
        self.table5.setCellWidget(1, 0, self.combo_pflegeNotfall_SD)
        
        self.combo_pflegeNotfall_ND = self.makeComboBox(self.pflege, (255,102,102))
        self.table5.setCellWidget(2, 0, self.combo_pflegeNotfall_ND)

        ###
        # self.table6
        ##

        self.combo_pflegeLeitung_FD = self.makeComboBox(self.pflege, (255,255, 153))
        self.table6.setCellWidget(0, 0, self.combo_pflegeLeitung_FD)
        
        self.combo_pflegeLeitung_SD = self.makeComboBox(self.pflege, (255,255, 153))
        self.table6.setCellWidget(1, 0, self.combo_pflegeLeitung_SD)

        self.combo_pflegeLeitung_ND = self.makeComboBox(self.pflege, (255,255, 153))
        self.table6.setCellWidget(2, 0, self.combo_pflegeLeitung_ND)

        ###
        # self.table7
        ##
        
        self.combo_arztLeitung = self.makeComboBox(self.aerzte, (153,255, 153))
        self.table7.setCellWidget(0, 0, self.combo_arztLeitung)

        ###
        # self.table8
        ##

        self.combo_arztDienst = self.makeComboBox(self.aerzte, (153,153, 255))
        self.table8.setCellWidget(0, 0, self.combo_arztDienst)
        
        self.combo_arztRufdienst = self.makeComboBox(self.aerzte, (153,153, 255))
        self.table8.setCellWidget(1, 0, self.combo_arztRufdienst)
        

    def button_ok(self):
        self.clearSelections()
        self.saveAll()
        self.updateDateTime()
    
    def saveAll(self):
        self.saveTable1()
        self.saveTable2()
        self.saveTable3()
        self.saveTable4()
        self.saveTable5()
        self.saveTable6()
        self.saveTable7()
        self.saveTable8()
    
    def saveToJson(self, filename, liste):
        with open(filename, 'w') as f:
            json.dump(liste, f, indent=2)
    
    def loadFromJson(self, filename):
        with open(filename, 'r') as f:
            liste = json.load(f)
    
        return liste
    
    def saveTable8(self):

        l = []
        l_0 = []
        
        ##
        # l_0 -> saveTable8
        ##
        
        text = self.combo_arztDienst.lineEdit().text()
        if text:
            l_0.append(text)
        else:
            l_0.append('')
        
        item = self.table8.item(0, 1)
        text = item.text()
        if text:
            l_0.append(text)
        else:
            l_0.append('')  

        ##
        # l_1
        ##
        
        l_1 = []
        text = self.combo_arztRufdienst.lineEdit().text()
        if text:
            l_1.append(text)
        else:
            l_1.append('')         
        
        item = self.table8.item(1, 1)
        text = item.text()
        if text:
            l_1.append(text)
        else:
            l_1.append('')  
        
        l.extend([l_0, l_1])
        self.saveToJson(self.path + 'tabelle8.json', l)

    
    def loadTable8(self):

        tab = self.loadFromJson(self.path + 'tabelle8.json')
        tab0 = tab[0]
        tab1 = tab[1]
        
        ##
        # tab0 -> loadTable8
        ##
        self.combo_arztDienst.lineEdit().setText(tab0[0])
        item = self.table8.item(0, 1)
        item.setText(tab0[1])
        ##
        # tab1 
        ##
        self.combo_arztRufdienst.lineEdit().setText(tab1[0])
        item = self.table8.item(1, 1)
        item.setText(tab1[1])
        
    
    def saveTable7(self):

        l = []
        l_0 = []
        
        ##
        # l_0 -> saveTable7
        ##
        
        text = self.combo_arztLeitung.lineEdit().text()
        if text:
            l_0.append(text)
        else:
            l_0.append('')
        
        item = self.table7.item(0, 1)
        text = item.text()
        if text:
            l_0.append(text)
        else:
            l_0.append('')  
        
        l.extend([l_0])
        self.saveToJson(self.path + 'tabelle7.json', l)
    
    def loadTable7(self):

        tab = self.loadFromJson(self.path + 'tabelle7.json')
        tab0 = tab[0]
        
        ##
        # tab0 -> loadTable7
        ##
        self.combo_arztLeitung.lineEdit().setText(tab0[0])
        item = self.table7.item(0, 1)
        item.setText(tab0[1])
    
    def saveTable6(self):

        l = []
        l_0 = []
        
        ##
        # l_0 -> saveTable6
        ##
        
        text = self.combo_pflegeLeitung_FD.lineEdit().text()
        if text:
            l_0.append(text)
        else:
            l_0.append('')
        
        ##
        # l_1 
        ##

        l_1 = []
        text = self.combo_pflegeLeitung_SD.lineEdit().text()
        if text:
            l_1.append(text)
        else:
            l_1.append('') 

        ##
        # l_2 -> saveTable2
        ##

        l_2 = []
        text = self.combo_pflegeLeitung_ND.lineEdit().text()
        if text:
            l_2.append(text)
        else:
            l_2.append('')  
        
        l.extend([l_0, l_1, l_2])
        self.saveToJson(self.path + 'tabelle6.json', l)
    
    def loadTable6(self):

        tab = self.loadFromJson(self.path + 'tabelle6.json')
        tab0 = tab[0]
        tab1 = tab[1]
        tab2 = tab[2]
        
        ##
        # tab0 -> loadTable6
        ##
        self.combo_pflegeLeitung_FD.lineEdit().setText(tab0[0])

        ##
        # tab1 
        ##
        self.combo_pflegeLeitung_SD.lineEdit().setText(tab1[0])
        
        ##
        # tab2 
        ##
        self.combo_pflegeLeitung_ND.lineEdit().setText(tab2[0])
    
    
    def saveTable5(self):

        l = []
        l_0 = []
        
        ##
        # l_0 -> saveTable5
        ##
        
        text = self.combo_pflegeNotfall_FD.lineEdit().text()
        if text:
            l_0.append(text)
        else:
            l_0.append('')
        
        ##
        # l_1 
        ##

        l_1 = []
        text = self.combo_pflegeNotfall_SD.lineEdit().text()
        if text:
            l_1.append(text)
        else:
            l_1.append('') 

        ##
        # l_2 
        ##

        l_2 = []
        text = self.combo_pflegeNotfall_ND.lineEdit().text()
        if text:
            l_2.append(text)
        else:
            l_2.append('')  
        
        ##
        # make list self.table5
        ##
        
        l.extend([l_0, l_1, l_2])
        self.saveToJson(self.path + 'tabelle5.json', l)

    
    def loadTable5(self):

        tab = self.loadFromJson(self.path + 'tabelle5.json')
        tab0 = tab[0]
        tab1 = tab[1]
        tab2 = tab[2]
        
        ##
        # tab0 -> loadTable5
        ##
        self.combo_pflegeNotfall_FD.lineEdit().setText(tab0[0])

        ##
        # tab1 
        ##
        self.combo_pflegeNotfall_SD.lineEdit().setText(tab1[0])
        
        ##
        # tab2 
        ##
        self.combo_pflegeNotfall_ND.lineEdit().setText(tab2[0])
    
    def saveTable4(self):
    
        l = []
        l_0 = []
        
        ##
        # l_0 -> saveTable4
        ##
        text = self.combo_verlegung_1.lineEdit().text()
        if text:
            l_0.append(text)
        else:
            l_0.append('')
        
        item = self.table4.item(0, 1)
        text = item.text()
        if text:
            l_0.append(text)
        else:
            l_0.append('')  

        ##
        # l_1 
        ##

        l_1 = []
        text = self.combo_verlegung_2.lineEdit().text()
        if text:
            l_1.append(text)
        else:
            l_1.append('')
        
        item = self.table4.item(1, 1)
        text = item.text()
        if text:
            l_1.append(text)
        else:
            l_1.append('')   

        ##
        # l_2 
        ##

        l_2 = []
        text = self.combo_verlegung_3.lineEdit().text()
        if text:
            l_2.append(text)
        else:
            l_2.append('')
        
        item = self.table4.item(2, 1)
        text = item.text()
        if text:
            l_2.append(text)
        else:
            l_2.append('')   

        ##
        # l_3 
        ##

        l_3 = []
        text = self.combo_verlegung_4.lineEdit().text()
        if text:
            l_3.append(text)
        else:
            l_3.append('')
        
        item = self.table4.item(3, 1)
        text = item.text()
        if text:
            l_3.append(text)
        else:
            l_3.append('')   

        ##
        # l_4 
        ##

        l_4 = []
        text = self.combo_verlegung_5.lineEdit().text()
        if text:
            l_4.append(text)
        else:
            l_4.append('')
        
        item = self.table4.item(4, 1)
        text = item.text()
        if text:
            l_4.append(text)
        else:
            l_4.append('')  

        ##
        # l_5 
        ##

        l_5 = []
        text = self.combo_verlegung_6.lineEdit().text()
        if text:
            l_5.append(text)
        else:
            l_5.append('')
        
        item = self.table4.item(5, 1)
        text = item.text()
        if text:
            l_5.append(text)
        else:
            l_5.append('')   
    
        
        l.extend([l_0, l_1, l_2, l_3, l_4, l_5])
        self.saveToJson(self.path + 'tabelle4.json', l)
        
    
    def loadTable4(self):
        tab = self.loadFromJson(self.path + 'tabelle4.json')
        tab0 = tab[0]
        tab1 = tab[1]
        tab2 = tab[2]
        tab3 = tab[3]
        tab4 = tab[4]
        tab5 = tab[5]
        
        ##
        # tab0 -> loadTable4
        ##
        self.combo_verlegung_1.lineEdit().setText(tab0[0])
        item = self.table4.item(0, 1)
        item.setText(tab0[1])

        ##
        # tab1 
        ##
        self.combo_verlegung_2.lineEdit().setText(tab1[0])
        item = self.table4.item(1, 1)
        item.setText(tab1[1])
 
        ##
        # tab2 
        ##
        self.combo_verlegung_3.lineEdit().setText(tab2[0])
        item = self.table4.item(2, 1)
        item.setText(tab2[1])       

        ##
        # tab3 
        ##
        self.combo_verlegung_4.lineEdit().setText(tab3[0])
        item = self.table4.item(3, 1)
        item.setText(tab3[1])

        ##
        # tab4 
        ##
        self.combo_verlegung_5.lineEdit().setText(tab4[0])
        item = self.table4.item(4, 1)
        item.setText(tab4[1])


    
    def saveTable3(self):
        l = []
        l_0 = []
        
        ##
        # l_0 -> saveTable3
        ##
        text = self.combo_aufnahme_1.lineEdit().text()
        if text:
            l_0.append(text)
        else:
            l_0.append('')
        
        item = self.table3.item(0, 1)
        text = item.text()
        if text:
            l_0.append(text)
        else:
            l_0.append('')  

        ##
        # l_1
        ##

        l_1 = []
        text = self.combo_aufnahme_2.lineEdit().text()
        if text:
            l_1.append(text)
        else:
            l_1.append('')
        
        item = self.table3.item(1, 1)
        text = item.text()
        if text:
            l_1.append(text)
        else:
            l_1.append('')   

        ##
        # l_2 
        ##

        l_2 = []
        text = self.combo_aufnahme_3.lineEdit().text()
        if text:
            l_2.append(text)
        else:
            l_2.append('')
        
        item = self.table3.item(2, 1)
        text = item.text()
        if text:
            l_2.append(text)
        else:
            l_2.append('')   

        ##
        # l_3 
        ##

        l_3 = []
        text = self.combo_aufnahme_4.lineEdit().text()
        if text:
            l_3.append(text)
        else:
            l_3.append('')
        
        item = self.table3.item(3, 1)
        text = item.text()
        if text:
            l_3.append(text)
        else:
            l_3.append('')   

        ##
        # l_4 
        ##

        l_4 = []
        text = self.combo_aufnahme_5.lineEdit().text()
        if text:
            l_4.append(text)
        else:
            l_4.append('')
        
        item = self.table3.item(4, 1)
        text = item.text()
        if text:
            l_4.append(text)
        else:
            l_4.append('')  

        ##
        # l_5 
        ##

        l_5 = []
        text = self.combo_aufnahme_6.lineEdit().text()
        if text:
            l_5.append(text)
        else:
            l_5.append('')
        
        item = self.table3.item(5, 1)
        text = item.text()
        if text:
            l_5.append(text)
        else:
            l_5.append('')   
    
        
        l.extend([l_0, l_1, l_2, l_3, l_4, l_5])
        self.saveToJson(self.path + 'tabelle3.json', l)

    
    def loadTable3(self):

        tab = self.loadFromJson(self.path + 'tabelle3.json')
        tab0 = tab[0]
        tab1 = tab[1]
        tab2 = tab[2]
        tab3 = tab[3]
        tab4 = tab[4]
        tab5 = tab[5]
        
        ##
        # tab0 -> loadTable3
        ##
        self.combo_aufnahme_1.lineEdit().setText(tab0[0])
        item = self.table3.item(0, 1)
        item.setText(tab0[1])

        ##
        # tab1 
        ##
        self.combo_aufnahme_2.lineEdit().setText(tab1[0])
        item = self.table3.item(1, 1)
        item.setText(tab1[1])
 
        ##
        # tab2 
        ##
        self.combo_aufnahme_3.lineEdit().setText(tab2[0])
        item = self.table3.item(2, 1)
        item.setText(tab2[1])       

        ##
        # tab3 
        ##
        self.combo_aufnahme_4.lineEdit().setText(tab3[0])
        item = self.table3.item(3, 1)
        item.setText(tab3[1])

        ##
        # tab4 
        ##
        self.combo_aufnahme_5.lineEdit().setText(tab4[0])
        item = self.table3.item(4, 1)
        item.setText(tab4[1])

        ##
        # tab5 
        ##
        self.combo_aufnahme_6.lineEdit().setText(tab5[0])
        item = self.table3.item(5, 1)
        item.setText(tab5[1])

    
    def saveTable2(self):
        l = []
        l_0 = []
        
        ##
        # l_0 -> saveTable2
        ##
        
        text = self.combo_notfall_1.lineEdit().text()
        if text:
            l_0.append(text)
        else:
            l_0.append('')
        
        item = self.table2.item(0, 1)
        text = item.text()
        if text:
            l_0.append(text)
        else:
            l_0.append('')    
        
        ##
        # l_1 
        ##

        l_1 = []
        text = self.combo_notfall_2.lineEdit().text()
        if text:
            l_1.append(text)
        else:
            l_1.append('')
        
        item = self.table2.item(1, 1)
        text = item.text()
        if text:
            l_1.append(text)
        else:
            l_1.append('')   

        ##
        # l_2 
        ##

        l_2 = []
        text = self.combo_notfall_3.lineEdit().text()
        if text:
            l_2.append(text)
        else:
            l_2.append('')
        
        item = self.table2.item(2, 1)
        text = item.text()
        if text:
            l_2.append(text)
        else:
            l_2.append('')    
        
        ##
        # make list self.table2
        ##
        
        l.extend([l_0, l_1, l_2])
        self.saveToJson(self.path + 'tabelle2.json', l)
            
    def loadTable2(self):
        tab = self.loadFromJson(self.path + 'tabelle2.json')
        tab0 = tab[0]
        tab1 = tab[1]
        tab2 = tab[2]
        
        ##
        # tab0 -> loadTable2
        ##
        self.combo_notfall_1.lineEdit().setText(tab0[0])
        item = self.table2.item(0, 1)
        item.setText(tab0[1])
        
        ##
        # tab1 
        ##
        self.combo_notfall_2.lineEdit().setText(tab1[0])
        item = self.table2.item(1, 1)
        item.setText(tab1[1])
        
        ##
        # tab2 
        ##
        self.combo_notfall_3.lineEdit().setText(tab2[0])
        item = self.table2.item(2, 1)
        item.setText(tab2[1])
        
    def saveTable1(self):
        ###              ###
        ## -> saveTable1  ##
        #####          #####
        
        ##
        # Raum 1
        ##
        l = []
        l_0 = []
        
        text = self.combo_cave_1_01.lineEdit().text()
        if text:
            l_0.append(text)
        else:
            l_0.append('')
        
        text = self.combo_abteilung_1.lineEdit().text()
        if text:
            l_0.append(text)
        else:
            l_0.append('')
        
        text = self.combo_pflege_1.lineEdit().text()
        if text:
            l_0.append(text)
        else:
            l_0.append('')
        
        text = self.combo_arzt_1.lineEdit().text()
        if text:
            l_0.append(text)
        else:
            l_0.append('')
    
        
        item = self.table1.item(0, 4)
        text = item.text()
        if text:
            l_0.append(text)
        else:
            l_0.append('')    
    
        text = self.combo_aufgaben_01.lineEdit().text()
        if text:
            l_0.append(text)
        else:
            l_0.append('')
        
        text = self.combo_kostform_01.lineEdit().text()
        if text:
            l_0.append(text)
        else:
            l_0.append('')
        
        ## every three rows -> self.combo_kostform ...
       

        l_1 = []

        
        text = self.combo_cave_1_02.lineEdit().text()
        if text:
            l_1.append(text)
        else:
            l_1.append('')
        
        item = self.table1.item(1, 1)
        text = item.text()
        if text:
            l_1.append(text)
        else:
            l_1.append('')   
        
        item = self.table1.item(1, 2)
        text = item.text()
        if text:
            l_1.append(text)
        else:
            l_1.append('')   
       
        item = self.table1.item(1, 3)
        text = item.text()
        if text:
            l_1.append(text)
        else:
            l_1.append('')   
        
        item = self.table1.item(1, 4)
        text = item.text()
        if text:
            l_1.append(text)
        else:
            l_1.append('')    
        
        text = self.combo_aufgaben_02.lineEdit().text()
        if text:
            l_1.append(text)
        else:
            l_1.append('')
        

        l_2 = []

        
        item = self.table1.item(2, 0)
        text = item.text()
        if text:
            l_2.append(text)
        else:
            l_2.append('')   

        item = self.table1.item(2, 1)
        text = item.text()
        if text:
            l_2.append(text)
        else:
            l_2.append('')   

        item = self.table1.item(2, 2)
        text = item.text()
        if text:
            l_2.append(text)
        else:
            l_2.append('')   

        item = self.table1.item(2, 3)
        text = item.text()
        if text:
            l_2.append(text)
        else:
            l_2.append('')   
            
        item = self.table1.item(2, 4)
        text = item.text()
        if text:
            l_2.append(text)
        else:
            l_2.append('')   
            
        item = self.table1.item(2, 5)
        text = item.text()
        if text:
            l_2.append(text)
        else:
            l_2.append('')   


        ##
        # Raum 2.1
        ##
        
        l_3 = []
        
        text = self.combo_cave_21_01.lineEdit().text()
        if text:
            l_3.append(text)
        else:
            l_3.append('')
        
        text = self.combo_abteilung_21.lineEdit().text()
        if text:
            l_3.append(text)
        else:
            l_3.append('')
        
        text = self.combo_pflege_21.lineEdit().text()
        if text:
            l_3.append(text)
        else:
            l_3.append('')
        
        text = self.combo_arzt_21.lineEdit().text()
        if text:
            l_3.append(text)
        else:
            l_3.append('')
    
        
        item = self.table1.item(3, 4)
        text = item.text()
        if text:
            l_3.append(text)
        else:
            l_3.append('')    
    
        text = self.combo_aufgaben_21_01.lineEdit().text()
        if text:
            l_3.append(text)
        else:
            l_3.append('')
        
        text = self.combo_kostform_21.lineEdit().text()
        if text:
            l_3.append(text)
        else:
            l_3.append('')
       
        ###
        
        l_4 = []
        
        
        text = self.combo_cave_21_02.lineEdit().text()
        if text:
            l_4.append(text)
        else:
            l_4.append('')
        
        item = self.table1.item(4, 1)
        text = item.text()
        if text:
            l_4.append(text)
        else:
            l_4.append('')   
        
        item = self.table1.item(4, 2)
        text = item.text()
        if text:
            l_4.append(text)
        else:
            l_4.append('')   
       
        item = self.table1.item(4, 3)
        text = item.text()
        if text:
            l_4.append(text)
        else:
            l_4.append('')   
        
        item = self.table1.item(4, 4)
        text = item.text()
        if text:
            l_4.append(text)
        else:
            l_4.append('')    
        
        text = self.combo_aufgaben_21_02.lineEdit().text()
        if text:
            l_4.append(text)
        else:
            l_4.append('')
        

        l_5 = []

        
        item = self.table1.item(5, 0)
        text = item.text()
        if text:
            l_5.append(text)
        else:
            l_5.append('')   

        item = self.table1.item(5, 1)
        text = item.text()
        if text:
            l_5.append(text)
        else:
            l_5.append('')   

        item = self.table1.item(5, 2)
        text = item.text()
        if text:
            l_5.append(text)
        else:
            l_5.append('')   

        item = self.table1.item(5, 3)
        text = item.text()
        if text:
            l_5.append(text)
        else:
            l_5.append('')   
            
        item = self.table1.item(5, 4)
        text = item.text()
        if text:
            l_5.append(text)
        else:
            l_5.append('')   
            
        item = self.table1.item(5, 5)
        text = item.text()
        if text:
            l_5.append(text)
        else:
            l_5.append('') 

        ##
        # Raum 2.2
        ##
        
        l_6 = []
        
        text = self.combo_cave_22_01.lineEdit().text()
        if text:
            l_6.append(text)
        else:
            l_6.append('')
        
        text = self.combo_abteilung_22.lineEdit().text()
        if text:
            l_6.append(text)
        else:
            l_6.append('')
        
        text = self.combo_pflege_22.lineEdit().text()
        if text:
            l_6.append(text)
        else:
            l_6.append('')
        
        text = self.combo_arzt_22.lineEdit().text()
        if text:
            l_6.append(text)
        else:
            l_6.append('')
    
        
        item = self.table1.item(6, 4)
        text = item.text()
        if text:
            l_6.append(text)
        else:
            l_6.append('')    
    
        text = self.combo_aufgaben_22_01.lineEdit().text()
        if text:
            l_6.append(text)
        else:
            l_6.append('')
       
        text = self.combo_kostform_22.lineEdit().text()
        if text:
            l_6.append(text)
        else:
            l_6.append('')

        l_7 = []
        
        
        text = self.combo_cave_22_02.lineEdit().text()
        if text:
            l_7.append(text)
        else:
            l_7.append('')
        
        item = self.table1.item(7, 1)
        text = item.text()
        if text:
            l_7.append(text)
        else:
            l_7.append('')   
        
        item = self.table1.item(7, 2)
        text = item.text()
        if text:
            l_7.append(text)
        else:
            l_7.append('')   
       
        item = self.table1.item(7, 3)
        text = item.text()
        if text:
            l_7.append(text)
        else:
            l_7.append('')   
        
        item = self.table1.item(7, 4)
        text = item.text()
        if text:
            l_7.append(text)
        else:
            l_7.append('')    
        
        text = self.combo_aufgaben_22_02.lineEdit().text()
        if text:
            l_7.append(text)
        else:
            l_7.append('')
        

        l_8 = []

        
        item = self.table1.item(8, 0)
        text = item.text()
        if text:
            l_8.append(text)
        else:
            l_8.append('')   

        item = self.table1.item(8, 1)
        text = item.text()
        if text:
            l_8.append(text)
        else:
            l_8.append('')   

        item = self.table1.item(8, 2)
        text = item.text()
        if text:
            l_8.append(text)
        else:
            l_8.append('')   

        item = self.table1.item(8, 3)
        text = item.text()
        if text:
            l_8.append(text)
        else:
            l_8.append('')   
            
        item = self.table1.item(8, 4)
        text = item.text()
        if text:
            l_8.append(text)
        else:
            l_8.append('')   
            
        item = self.table1.item(8, 5)
        text = item.text()
        if text:
            l_8.append(text)
        else:
            l_8.append('') 


        ##
        # Raum 3
        ##
        
        l_9 = []
        
        text = self.combo_cave_3_01.lineEdit().text()
        if text:
            l_9.append(text)
        else:
            l_9.append('')
        
        text = self.combo_abteilung_3.lineEdit().text()
        if text:
            l_9.append(text)
        else:
            l_9.append('')
        
        text = self.combo_pflege_3.lineEdit().text()
        if text:
            l_9.append(text)
        else:
            l_9.append('')
        
        text = self.combo_arzt_3.lineEdit().text()
        if text:
            l_9.append(text)
        else:
            l_9.append('')
    
        
        item = self.table1.item(9, 4)
        text = item.text()
        if text:
            l_9.append(text)
        else:
            l_9.append('')    
    
        text = self.combo_aufgaben_3_01.lineEdit().text()
        if text:
            l_9.append(text)
        else:
            l_9.append('')
		
        text = self.combo_kostform_3.lineEdit().text()
        if text:
            l_9.append(text)
        else:
            l_9.append('')

        l_10 = []
        
        
        text = self.combo_cave_3_02.lineEdit().text()
        if text:
            l_10.append(text)
        else:
            l_10.append('')
        
        item = self.table1.item(10, 1)
        text = item.text()
        if text:
            l_10.append(text)
        else:
            l_10.append('')   
        
        item = self.table1.item(10, 2)
        text = item.text()
        if text:
            l_10.append(text)
        else:
            l_10.append('')   
       
        item = self.table1.item(10, 3)
        text = item.text()
        if text:
            l_10.append(text)
        else:
            l_10.append('')   
        
        item = self.table1.item(10, 4)
        text = item.text()
        if text:
            l_10.append(text)
        else:
            l_10.append('')    
        
        text = self.combo_aufgaben_3_02.lineEdit().text()
        if text:
            l_10.append(text)
        else:
            l_10.append('')
        

        l_11 = []

        
        item = self.table1.item(11, 0)
        text = item.text()
        if text:
            l_11.append(text)
        else:
            l_11.append('')   

        item = self.table1.item(11, 1)
        text = item.text()
        if text:
            l_11.append(text)
        else:
            l_11.append('')   

        item = self.table1.item(11, 2)
        text = item.text()
        if text:
            l_11.append(text)
        else:
            l_11.append('')   

        item = self.table1.item(11, 3)
        text = item.text()
        if text:
            l_11.append(text)
        else:
            l_11.append('')   
            
        item = self.table1.item(11, 4)
        text = item.text()
        if text:
            l_11.append(text)
        else:
            l_11.append('')   
            
        item = self.table1.item(11, 5)
        text = item.text()
        if text:
            l_11.append(text)
        else:
            l_11.append('')    

        ##
        # Raum 4.1
        ##
        
        l_12 = []
        
        text = self.combo_cave_41_01.lineEdit().text()
        if text:
            l_12.append(text)
        else:
            l_12.append('')
        
        text = self.combo_abteilung_41.lineEdit().text()
        if text:
            l_12.append(text)
        else:
            l_12.append('')
        
        text = self.combo_pflege_41.lineEdit().text()
        if text:
            l_12.append(text)
        else:
            l_12.append('')
        
        text = self.combo_arzt_41.lineEdit().text()
        if text:
            l_12.append(text)
        else:
            l_12.append('')
    
        
        item = self.table1.item(12, 4)
        text = item.text()
        if text:
            l_12.append(text)
        else:
            l_12.append('')    
    
        text = self.combo_aufgaben_41_01.lineEdit().text()
        if text:
            l_12.append(text)
        else:
            l_12.append('')
        
        text = self.combo_kostform_41.lineEdit().text()
        if text:
            l_12.append(text)
        else:
            l_12.append('')       

        l_13 = []
        
        
        text = self.combo_cave_41_02.lineEdit().text()
        if text:
            l_13.append(text)
        else:
            l_13.append('')
        
        item = self.table1.item(13, 1)
        text = item.text()
        if text:
            l_13.append(text)
        else:
            l_13.append('')   
        
        item = self.table1.item(13, 2)
        text = item.text()
        if text:
            l_13.append(text)
        else:
            l_13.append('')   
       
        item = self.table1.item(13, 3)
        text = item.text()
        if text:
            l_13.append(text)
        else:
            l_13.append('')   
        
        item = self.table1.item(13, 4)
        text = item.text()
        if text:
            l_13.append(text)
        else:
            l_13.append('')    
        
        text = self.combo_aufgaben_41_02.lineEdit().text()
        if text:
            l_13.append(text)
        else:
            l_13.append('')
        

        l_14 = []

        
        item = self.table1.item(14, 0)
        text = item.text()
        if text:
            l_14.append(text)
        else:
            l_14.append('')   

        item = self.table1.item(14, 1)
        text = item.text()
        if text:
            l_14.append(text)
        else:
            l_14.append('')   

        item = self.table1.item(14, 2)
        text = item.text()
        if text:
            l_14.append(text)
        else:
            l_14.append('')   

        item = self.table1.item(14, 3)
        text = item.text()
        if text:
            l_14.append(text)
        else:
            l_14.append('')   
            
        item = self.table1.item(14, 4)
        text = item.text()
        if text:
            l_14.append(text)
        else:
            l_14.append('')   
            
        item = self.table1.item(14, 5)
        text = item.text()
        if text:
            l_14.append(text)
        else:
            l_14.append('')

        ##
        # Raum 4.2
        ##
        
        l_15 = []
        
        text = self.combo_cave_42_01.lineEdit().text()
        if text:
            l_15.append(text)
        else:
            l_15.append('')
        
        text = self.combo_abteilung_42.lineEdit().text()
        if text:
            l_15.append(text)
        else:
            l_15.append('')
        
        text = self.combo_pflege_42.lineEdit().text()
        if text:
            l_15.append(text)
        else:
            l_15.append('')
        
        text = self.combo_arzt_42.lineEdit().text()
        if text:
            l_15.append(text)
        else:
            l_15.append('')
    
        
        item = self.table1.item(15, 4)
        text = item.text()
        if text:
            l_15.append(text)
        else:
            l_15.append('')    
    
        text = self.combo_aufgaben_42_01.lineEdit().text()
        if text:
            l_15.append(text)
        else:
            l_15.append('')
		
        text = self.combo_kostform_42.lineEdit().text()
        if text:
            l_15.append(text)
        else:
            l_15.append('')

        l_16 = []
        
        
        text = self.combo_cave_42_02.lineEdit().text()
        if text:
            l_16.append(text)
        else:
            l_16.append('')
        
        item = self.table1.item(16, 1)
        text = item.text()
        if text:
            l_16.append(text)
        else:
            l_16.append('')   
        
        item = self.table1.item(16, 2)
        text = item.text()
        if text:
            l_16.append(text)
        else:
            l_16.append('')   
       
        item = self.table1.item(16, 3)
        text = item.text()
        if text:
            l_16.append(text)
        else:
            l_16.append('')   
        
        item = self.table1.item(16, 4)
        text = item.text()
        if text:
            l_16.append(text)
        else:
            l_16.append('')    
        
        text = self.combo_aufgaben_42_02.lineEdit().text()
        if text:
            l_16.append(text)
        else:
            l_16.append('')
        

        l_17 = []

        
        item = self.table1.item(17, 0)
        text = item.text()
        if text:
            l_17.append(text)
        else:
            l_17.append('')   

        item = self.table1.item(17, 1)
        text = item.text()
        if text:
            l_17.append(text)
        else:
            l_17.append('')   

        item = self.table1.item(17, 2)
        text = item.text()
        if text:
            l_17.append(text)
        else:
            l_17.append('')   

        item = self.table1.item(17, 3)
        text = item.text()
        if text:
            l_17.append(text)
        else:
            l_17.append('')   
            
        item = self.table1.item(17, 4)
        text = item.text()
        if text:
            l_17.append(text)
        else:
            l_17.append('')   
            
        item = self.table1.item(17, 5)
        text = item.text()
        if text:
            l_17.append(text)
        else:
            l_17.append('')

        ##
        # Raum 5
        ##
        
        l_18 = []
        
        text = self.combo_cave_5_01.lineEdit().text()
        if text:
            l_18.append(text)
        else:
            l_18.append('')
        
        text = self.combo_abteilung_5.lineEdit().text()
        if text:
            l_18.append(text)
        else:
            l_18.append('')
        
        text = self.combo_pflege_5.lineEdit().text()
        if text:
            l_18.append(text)
        else:
            l_18.append('')
        
        text = self.combo_arzt_5.lineEdit().text()
        if text:
            l_18.append(text)
        else:
            l_18.append('')
    
        
        item = self.table1.item(18, 4)
        text = item.text()
        if text:
            l_18.append(text)
        else:
            l_18.append('')    
    
        text = self.combo_aufgaben_5_01.lineEdit().text()
        if text:
            l_18.append(text)
        else:
            l_18.append('')
		
        text = self.combo_kostform_5.lineEdit().text()
        if text:
            l_18.append(text)
        else:
            l_18.append('')
		
        l_19 = []
        
        
        text = self.combo_cave_5_02.lineEdit().text()
        if text:
            l_19.append(text)
        else:
            l_19.append('')
        
        item = self.table1.item(19, 1)
        text = item.text()
        if text:
            l_19.append(text)
        else:
            l_19.append('')   
        
        item = self.table1.item(19, 2)
        text = item.text()
        if text:
            l_19.append(text)
        else:
            l_19.append('')   
       
        item = self.table1.item(19, 3)
        text = item.text()
        if text:
            l_19.append(text)
        else:
            l_19.append('')   
        
        item = self.table1.item(19, 4)
        text = item.text()
        if text:
            l_19.append(text)
        else:
            l_19.append('')    
        
        text = self.combo_aufgaben_5_02.lineEdit().text()
        if text:
            l_19.append(text)
        else:
            l_19.append('')
        

        l_20 = []

        
        item = self.table1.item(20, 0)
        text = item.text()
        if text:
            l_20.append(text)
        else:
            l_20.append('')   

        item = self.table1.item(20, 1)
        text = item.text()
        if text:
            l_20.append(text)
        else:
            l_20.append('')   

        item = self.table1.item(20, 2)
        text = item.text()
        if text:
            l_20.append(text)
        else:
            l_20.append('')   

        item = self.table1.item(20, 3)
        text = item.text()
        if text:
            l_20.append(text)
        else:
            l_20.append('')   
            
        item = self.table1.item(20, 4)
        text = item.text()
        if text:
            l_20.append(text)
        else:
            l_20.append('')   
            
        item = self.table1.item(20, 5)
        text = item.text()
        if text:
            l_20.append(text)
        else:
            l_20.append('')

        ##
        # Raum 6
        ##
        
        l_21 = []
        
        text = self.combo_cave_6_01.lineEdit().text()
        if text:
            l_21.append(text)
        else:
            l_21.append('')
        
        text = self.combo_abteilung_6.lineEdit().text()
        if text:
            l_21.append(text)
        else:
            l_21.append('')
        
        text = self.combo_pflege_6.lineEdit().text()
        if text:
            l_21.append(text)
        else:
            l_21.append('')
        
        text = self.combo_arzt_6.lineEdit().text()
        if text:
            l_21.append(text)
        else:
            l_21.append('')
    
        
        item = self.table1.item(21, 4)
        text = item.text()
        if text:
            l_21.append(text)
        else:
            l_21.append('')    
    
        text = self.combo_aufgaben_6_01.lineEdit().text()
        if text:
            l_21.append(text)
        else:
            l_21.append('')
		
        text = self.combo_kostform_6.lineEdit().text()
        if text:
            l_21.append(text)
        else:
            l_21.append('')

        l_22 = []
        
        
        text = self.combo_cave_6_02.lineEdit().text()
        if text:
            l_22.append(text)
        else:
            l_22.append('')
        
        item = self.table1.item(22, 1)
        text = item.text()
        if text:
            l_22.append(text)
        else:
            l_22.append('')   
        
        item = self.table1.item(22, 2)
        text = item.text()
        if text:
            l_22.append(text)
        else:
            l_22.append('')   
       
        item = self.table1.item(22, 3)
        text = item.text()
        if text:
            l_22.append(text)
        else:
            l_22.append('')   
        
        item = self.table1.item(22, 4)
        text = item.text()
        if text:
            l_22.append(text)
        else:
            l_22.append('')    
        
        text = self.combo_aufgaben_6_02.lineEdit().text()
        if text:
            l_22.append(text)
        else:
            l_22.append('')
        

        l_23 = []

        
        item = self.table1.item(23, 0)
        text = item.text()
        if text:
            l_23.append(text)
        else:
            l_23.append('')   

        item = self.table1.item(23, 1)
        text = item.text()
        if text:
            l_23.append(text)
        else:
            l_23.append('')   

        item = self.table1.item(23, 2)
        text = item.text()
        if text:
            l_23.append(text)
        else:
            l_23.append('')   

        item = self.table1.item(23, 3)
        text = item.text()
        if text:
            l_23.append(text)
        else:
            l_23.append('')   
            
        item = self.table1.item(23, 4)
        text = item.text()
        if text:
            l_23.append(text)
        else:
            l_23.append('')   
            
        item = self.table1.item(23, 5)
        text = item.text()
        if text:
            l_23.append(text)
        else:
            l_23.append('')
        
        
        ##
        # make list self.table1
        ## 
        
        l.extend([l_0, l_1, l_2, l_3, l_4, l_5, l_6, l_7, l_8, l_9,
                  l_10, l_11, l_12, l_13, l_14, l_15, l_16, l_17, l_18, l_19,
                  l_20, l_21, l_22, l_23])
        
        self.saveToJson(self.path + 'tabelle1.json', l)
        
        
    def loadTable1(self):
        ###              ###
        ## -> loadTable1  ##
        #####          #####

        tab = self.loadFromJson(self.path + 'tabelle1.json')
        tab0 = tab[0]
        tab1 = tab[1]
        tab2 = tab[2]
        tab3 = tab[3]
        tab4 = tab[4]
        tab5 = tab[5]
        tab6 = tab[6]
        tab7 = tab[7]
        tab8 = tab[8]
        tab9 = tab[9]
        tab10 = tab[10]
        tab11 = tab[11]
        tab12 = tab[12]
        tab13 = tab[13]
        tab14 = tab[14]
        tab15 = tab[15]
        tab16 = tab[16]
        tab17 = tab[17]
        tab18 = tab[18]
        tab19 = tab[19]
        tab20 = tab[20]
        tab21 = tab[21]
        tab22 = tab[22]
        tab23 = tab[23]
        
        ##
        # tab0
        ##
        self.combo_cave_1_01.lineEdit().setText(tab0[0])
        self.combo_abteilung_1.lineEdit().setText(tab0[1])
        self.combo_pflege_1.lineEdit().setText(tab0[2])
        self.combo_arzt_1.lineEdit().setText(tab0[3])
        item = self.table1.item(0, 4)
        item.setText(tab0[4])
        self.combo_aufgaben_01.lineEdit().setText(tab0[5])
        self.combo_kostform_01.lineEdit().setText(tab0[6])
        
        ##
        # tab1
        ##
        self.combo_cave_1_02.lineEdit().setText(tab1[0])
        item = self.table1.item(1, 1)
        item.setText(tab1[1])
        item = self.table1.item(1, 2)
        item.setText(tab1[2])
        item = self.table1.item(1, 3)
        item.setText(tab1[3])
        item = self.table1.item(1, 4)
        item.setText(tab1[4])
        self.combo_aufgaben_02.lineEdit().setText(tab1[5])
        
        ##
        # tab2
        ##
        item = self.table1.item(2, 0)
        item.setText(tab2[0])
        item = self.table1.item(2, 1)
        item.setText(tab2[1])        
        item = self.table1.item(2, 2)
        item.setText(tab2[2])
        item = self.table1.item(2, 3)
        item.setText(tab2[3])
        item = self.table1.item(2, 4)
        item.setText(tab2[4])
        item = self.table1.item(2, 5)
        item.setText(tab2[5])

        ##
        # tab3
        ##
        self.combo_cave_21_01.lineEdit().setText(tab3[0])
        self.combo_abteilung_21.lineEdit().setText(tab3[1])
        self.combo_pflege_21.lineEdit().setText(tab3[2])
        self.combo_arzt_21.lineEdit().setText(tab3[3])
        item = self.table1.item(3, 4)
        item.setText(tab3[4])
        self.combo_aufgaben_21_01.lineEdit().setText(tab3[5])
        self.combo_kostform_21.lineEdit().setText(tab3[6])
        
        ##
        # tab4
        ##
        self.combo_cave_21_02.lineEdit().setText(tab4[0])
        item = self.table1.item(4, 1)
        item.setText(tab4[1])
        item = self.table1.item(4, 2)
        item.setText(tab4[2])
        item = self.table1.item(4, 3)
        item.setText(tab4[3])
        item = self.table1.item(4, 4)
        item.setText(tab4[4])
        self.combo_aufgaben_21_02.lineEdit().setText(tab4[5])
        ##
        # tab5
        ##
        item = self.table1.item(5, 0)
        item.setText(tab5[0])
        item = self.table1.item(5, 1)
        item.setText(tab5[1])        
        item = self.table1.item(5, 2)
        item.setText(tab5[2])
        item = self.table1.item(5, 3)
        item.setText(tab5[3])
        item = self.table1.item(5, 4)
        item.setText(tab5[4])
        item = self.table1.item(5, 5)
        item.setText(tab5[5])

        ##
        # tab6
        ##
        self.combo_cave_22_01.lineEdit().setText(tab6[0])
        self.combo_abteilung_22.lineEdit().setText(tab6[1])
        self.combo_pflege_22.lineEdit().setText(tab6[2])
        self.combo_arzt_22.lineEdit().setText(tab6[3])
        item = self.table1.item(6, 4)
        item.setText(tab6[4])
        self.combo_aufgaben_22_01.lineEdit().setText(tab6[5])
        self.combo_kostform_22.lineEdit().setText(tab6[6])
        
        ##
        # tab7
        ##
        self.combo_cave_22_02.lineEdit().setText(tab7[0])
        item = self.table1.item(7, 1)
        item.setText(tab7[1])
        item = self.table1.item(7, 2)
        item.setText(tab7[2])
        item = self.table1.item(7, 3)
        item.setText(tab7[3])
        item = self.table1.item(7, 4)
        item.setText(tab7[4])
        self.combo_aufgaben_22_02.lineEdit().setText(tab7[5])
        ##
        # tab8
        ##
        item = self.table1.item(8, 0)
        item.setText(tab8[0])
        item = self.table1.item(8, 1)
        item.setText(tab8[1])        
        item = self.table1.item(8, 2)
        item.setText(tab8[2])
        item = self.table1.item(8, 3)
        item.setText(tab8[3])
        item = self.table1.item(8, 4)
        item.setText(tab8[4])
        item = self.table1.item(8, 5)
        item.setText(tab8[5])

        ##
        # tab9
        ##
        self.combo_cave_3_01.lineEdit().setText(tab9[0])
        self.combo_abteilung_3.lineEdit().setText(tab9[1])
        self.combo_pflege_3.lineEdit().setText(tab9[2])
        self.combo_arzt_3.lineEdit().setText(tab9[3])
        item = self.table1.item(9, 4)
        item.setText(tab9[4])
        self.combo_aufgaben_3_01.lineEdit().setText(tab9[5])
        self.combo_kostform_3.lineEdit().setText(tab9[6])
        
        ##
        # tab10
        ##
        self.combo_cave_3_02.lineEdit().setText(tab10[0])
        item = self.table1.item(10, 1)
        item.setText(tab10[1])
        item = self.table1.item(10, 2)
        item.setText(tab10[2])
        item = self.table1.item(10, 3)
        item.setText(tab10[3])
        item = self.table1.item(10, 4)
        item.setText(tab10[4])
        self.combo_aufgaben_3_02.lineEdit().setText(tab10[5])
        ##
        # tab11
        ##
        item = self.table1.item(11, 0)
        item.setText(tab11[0])
        item = self.table1.item(11, 1)
        item.setText(tab11[1])        
        item = self.table1.item(11, 2)
        item.setText(tab11[2])
        item = self.table1.item(11, 3)
        item.setText(tab11[3])
        item = self.table1.item(11, 4)
        item.setText(tab11[4])
        item = self.table1.item(11, 5)
        item.setText(tab11[5])

        ##
        # tab12
        ##
        self.combo_cave_41_01.lineEdit().setText(tab12[0])
        self.combo_abteilung_41.lineEdit().setText(tab12[1])
        self.combo_pflege_41.lineEdit().setText(tab12[2])
        self.combo_arzt_41.lineEdit().setText(tab12[3])
        item = self.table1.item(12, 4)
        item.setText(tab12[4])
        self.combo_aufgaben_41_01.lineEdit().setText(tab12[5])
        self.combo_kostform_41.lineEdit().setText(tab12[6])
        
        ##
        # tab13
        ##
        self.combo_cave_41_02.lineEdit().setText(tab13[0])
        item = self.table1.item(13, 1)
        item.setText(tab13[1])
        item = self.table1.item(13, 2)
        item.setText(tab13[2])
        item = self.table1.item(13, 3)
        item.setText(tab13[3])
        item = self.table1.item(13, 4)
        item.setText(tab13[4])
        self.combo_aufgaben_41_02.lineEdit().setText(tab13[5])
        ##
        # tab14
        ##
        item = self.table1.item(14, 0)
        item.setText(tab14[0])
        item = self.table1.item(14, 1)
        item.setText(tab14[1])        
        item = self.table1.item(14, 2)
        item.setText(tab14[2])
        item = self.table1.item(14, 3)
        item.setText(tab14[3])
        item = self.table1.item(14, 4)
        item.setText(tab14[4])
        item = self.table1.item(14, 5)
        item.setText(tab14[5])

        ##
        # tab15
        ##
        self.combo_cave_42_01.lineEdit().setText(tab15[0])
        self.combo_abteilung_42.lineEdit().setText(tab15[1])
        self.combo_pflege_42.lineEdit().setText(tab15[2])
        self.combo_arzt_42.lineEdit().setText(tab15[3])
        item = self.table1.item(15, 4)
        item.setText(tab15[4])
        self.combo_aufgaben_42_01.lineEdit().setText(tab15[5])
        self.combo_kostform_42.lineEdit().setText(tab15[6])
        
        ##
        # tab16
        ##
        self.combo_cave_42_02.lineEdit().setText(tab16[0])
        item = self.table1.item(16, 1)
        item.setText(tab16[1])
        item = self.table1.item(16, 2)
        item.setText(tab16[2])
        item = self.table1.item(16, 3)
        item.setText(tab16[3])
        item = self.table1.item(16, 4)
        item.setText(tab16[4])
        self.combo_aufgaben_42_02.lineEdit().setText(tab16[5])
        ##
        # tab17
        ##
        item = self.table1.item(17, 0)
        item.setText(tab17[0])
        item = self.table1.item(17, 1)
        item.setText(tab17[1])        
        item = self.table1.item(17, 2)
        item.setText(tab17[2])
        item = self.table1.item(17, 3)
        item.setText(tab17[3])
        item = self.table1.item(17, 4)
        item.setText(tab17[4])
        item = self.table1.item(17, 5)
        item.setText(tab17[5])

        ##
        # tab18
        ##
        self.combo_cave_5_01.lineEdit().setText(tab18[0])
        self.combo_abteilung_5.lineEdit().setText(tab18[1])
        self.combo_pflege_5.lineEdit().setText(tab18[2])
        self.combo_arzt_5.lineEdit().setText(tab18[3])
        item = self.table1.item(18, 4)
        item.setText(tab18[4])
        self.combo_aufgaben_5_01.lineEdit().setText(tab18[5])
        self.combo_kostform_5.lineEdit().setText(tab18[6])
        
        ##
        # tab19
        ##
        self.combo_cave_5_02.lineEdit().setText(tab19[0])
        item = self.table1.item(19, 1)
        item.setText(tab19[1])
        item = self.table1.item(19, 2)
        item.setText(tab19[2])
        item = self.table1.item(19, 3)
        item.setText(tab19[3])
        item = self.table1.item(19, 4)
        item.setText(tab19[4])
        self.combo_aufgaben_5_02.lineEdit().setText(tab19[5])
        ##
        # tab20
        ##
        item = self.table1.item(20, 0)
        item.setText(tab20[0])
        item = self.table1.item(20, 1)
        item.setText(tab20[1])        
        item = self.table1.item(20, 2)
        item.setText(tab20[2])
        item = self.table1.item(20, 3)
        item.setText(tab20[3])
        item = self.table1.item(20, 4)
        item.setText(tab20[4])
        item = self.table1.item(20, 5)
        item.setText(tab20[5])

        ##
        # tab21
        ##
        self.combo_cave_6_01.lineEdit().setText(tab21[0])
        self.combo_abteilung_6.lineEdit().setText(tab21[1])
        self.combo_pflege_6.lineEdit().setText(tab21[2])
        self.combo_arzt_6.lineEdit().setText(tab21[3])
        item = self.table1.item(21, 4)
        item.setText(tab21[4])
        self.combo_aufgaben_6_01.lineEdit().setText(tab21[5])
        self.combo_kostform_6.lineEdit().setText(tab21[6])
        
        ##
        # tab22
        ##
        self.combo_cave_6_02.lineEdit().setText(tab22[0])
        item = self.table1.item(22, 1)
        item.setText(tab22[1])
        item = self.table1.item(22, 2)
        item.setText(tab22[2])
        item = self.table1.item(22, 3)
        item.setText(tab22[3])
        item = self.table1.item(22, 4)
        item.setText(tab22[4])
        self.combo_aufgaben_6_02.lineEdit().setText(tab22[5])
        ##
        # tab23
        ##
        item = self.table1.item(23, 0)
        item.setText(tab23[0])
        item = self.table1.item(23, 1)
        item.setText(tab23[1])        
        item = self.table1.item(23, 2)
        item.setText(tab23[2])
        item = self.table1.item(23, 3)
        item.setText(tab23[3])
        item = self.table1.item(23, 4)
        item.setText(tab23[4])
        item = self.table1.item(23, 5)
        item.setText(tab23[5])

    
    def closeEvent(self, event):
        self.saveAll()
        event.accept()
        
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    window = MainWindow(app)
    window.show()
    app.exec_()

            
