# -*- coding: utf-8 -*-
"""
Created on Tue Jul 10 00:52:47 2018

@author: CHARLES ADEDOYIN
"""

from PyQt4.QtCore import SIGNAL, QDate, Qt, QSize
from PyQt4.QtGui import  QWidget, QFileDialog, QPixmap, QTabWidget, QComboBox, QRadioButton, QDateEdit, QTextEdit, QCheckBox, QHBoxLayout, QGroupBox, QGridLayout, QDialog, QApplication, QPushButton, QLineEdit, QFormLayout, QLabel, QVBoxLayout, QSizePolicy
from connect import Db
from PIL import Image
import cv2

class StudentForm(QDialog):
    
    def __init__(self, parent=None):
        super(StudentForm, self).__init__(parent)
        #self.setGeometry(50, 50, 820, 530)
        self.resize(530, 430)
        
        self.tabz = QTabWidget(self)
        self.tab1 = QWidget(self)
        self.tab2 = QWidget(self)
        self.tab3 = QWidget(self)
        self.tab4 = QWidget(self)
        
        #main form
        self.schno = QLabel("School Number")
        self.schnoData = QLineEdit()
        self.schnoData.setObjectName("schno")
        self.schnoData.setPlaceholderText("00000000")
        
        self.surname = QLabel("Surname")
        self.surnameData = QLineEdit()
        self.surnameData.setObjectName("surname")
        self.surnameData.setPlaceholderText("Surname")
        
        self.firstname = QLabel("Firstname")
        self.firstnameData = QLineEdit()
        self.firstnameData.setObjectName("firstname")
        self.firstnameData.setPlaceholderText("Firstname")
        
        self.middlename = QLabel("Middlename")
        self.middlenameData = QLineEdit()
        self.middlenameData.setObjectName("middlename")
        self.middlenameData.setPlaceholderText("middlename")
        
        self.soo = QLabel("State/Region of Origin")
        self.sooData = QLineEdit()
        self.sooData.setObjectName("soo")
        self.sooData.setPlaceholderText("Lagos")
        
        self.lga = QLabel("LGA/District")
        self.lgaData = QLineEdit()
        self.lgaData.setObjectName("lga")
        self.lgaData.setPlaceholderText("Ikeja")
        
        self.addr = QLabel("House Address")
        self.addrData = QTextEdit()
        self.addrData.setObjectName("addr")
        #self.addrData.setPlaceholderText("No. 12 Harrrison For Str., Ney York")
        
        self.dob = QLabel("Date of Birth")
        self.dobData = QDateEdit()
        self.dobData.setObjectName("dob")
        
        self.admit = QLabel("Date Admitted")
        self.admitData = QDateEdit()
        self.admitData.setObjectName("admit")
        
        self.pb = QPushButton()
        self.pb.setObjectName("Submit")
        self.pb.setText("Submit")
        
        self.pb1 = QPushButton()
        self.pb1.setObjectName("Cancel")
        self.pb1.setText("Cancel")
        
        hbo = QHBoxLayout()
        self.gender = QLabel('Gender')
        self.r1 = QRadioButton('Male')
        self.r2 = QRadioButton('Female')
        hbo.addWidget(self.r1)
        hbo.addWidget(self.r2)
        
        Formlayout = QFormLayout()
        Formlayout.addRow(self.schno, self.schnoData)
        Formlayout.addRow(self.surname, self.surnameData)
        Formlayout.addRow(self.firstname, self.firstnameData)
        Formlayout.addRow(self.middlename, self.middlenameData)
        Formlayout.addRow(self.gender, hbo)
        Formlayout.addRow(self.dob, self.dobData)
        Formlayout.addRow(self.admit, self.admitData)
        Formlayout.addRow(self.soo, self.sooData)
        Formlayout.addRow(self.lga, self.lgaData)
        Formlayout.addRow(self.addr, self.addrData)
        
        grid = QGridLayout()
        grid.addWidget(self.pb1,0,1)
        grid.addWidget(self.pb,0,0)
        
        groupBox = QGroupBox('BIODATA')
        groupBox.setLayout(Formlayout)
        
        vbox = QVBoxLayout()
        vbox.addWidget(groupBox)
        vbox.addStretch()
        vbox.addLayout(grid)
        
        #self.setLayout(vbox)
        self.connect(self.pb, SIGNAL("clicked()"), lambda: self.button_click(1))
        self.connect(self.pb1, SIGNAL("clicked()"), self.close)
        self.setWindowTitle("Student Data")
        #self.setTabText(0, 'BioData')
        self.tab1.setLayout(vbox)
        
        #guardian data
        relations = ['Father', 'Mother', 'Aunt', 'Uncle', 'Grand Parent', 'Guardian', 'Others']
        
        #first guardian details
        self.g1name = QLabel("First Guardian")
        self.g1Data = QLineEdit()
        self.g1Data.setObjectName("g1name")
        self.g1Data.setPlaceholderText("Fullname")
        
        self.g1rel = QLabel('Relationship')
        self.g1relData = QComboBox()
        self.g1relData.addItems(relations)
        
        self.g1p1 = QLabel("Phone Number")
        self.g1p1Data = QLineEdit()
        self.g1p1Data.setObjectName("g1p1")
        self.g1p1Data.setPlaceholderText("08000000000")
        
        self.g1p2 = QLabel("Alt. Phone Number")
        self.g1p2Data = QLineEdit()
        self.g1p2Data.setObjectName("g1p2")
        self.g1p2Data.setPlaceholderText("08000000000")
        
        self.g1email = QLabel("Email")
        self.g1emailData = QLineEdit()
        self.g1emailData.setObjectName("g1email")
        self.g1emailData.setPlaceholderText("info@somethingmail.com")
        
        self.g1addr = QLabel("Address")
        self.g1addrData = QTextEdit()
        self.g1addrData.setObjectName("g1add")
        #self.g1addrData.setPlaceholderText("No. 12 Harrrison For Str., Ney York")
         #second guardian details
        self.g2name = QLabel("Second Guardian")
        self.g2Data = QLineEdit()
        self.g2Data.setObjectName("g2name")
        self.g2Data.setPlaceholderText("Mr. Surname Lastname")
        
        self.g2rel = QLabel('Relationship')
        self.g2relData = QComboBox()
        self.g2relData.addItems(relations)
        
        self.g2p1 = QLabel("Phone Number")
        self.g2p1Data = QLineEdit()
        self.g2p1Data.setObjectName("g2p1")
        self.g2p1Data.setPlaceholderText("08000000000")
        
        self.g2p2 = QLabel("Alt. Phone Number")
        self.g2p2Data = QLineEdit()
        self.g2p2Data.setObjectName("g2p2")
        self.g2p2Data.setPlaceholderText("08000000000")
        
        self.g2email = QLabel("Email")
        self.g2emailData = QLineEdit()
        self.g2emailData.setObjectName("g2email")
        self.g2emailData.setPlaceholderText("info@somethingmail.com")
        
        self.g2addr = QLabel("Address")
        self.g2addrData = QTextEdit()
        self.g2addrData.setObjectName("g2add")
        #self.g2addrData.setPlaceholderText("No. 12 Harrrison For Str., Ney York")

        self.pb = QPushButton()
        self.pb.setObjectName("Submit")
        self.pb.setText("Submit")
        
        self.pb1 = QPushButton()
        self.pb1.setObjectName("Cancel")
        self.pb1.setText("Cancel")
        
        hbo = QHBoxLayout()
        
        self.gender = QLabel('Gender')
        self.r1 = QRadioButton('Male')
        self.r2 = QRadioButton('Female')
        hbo.addWidget(self.r1)
        hbo.addWidget(self.r2)
        
        
        Formlayout1 = QFormLayout()
        Formlayout1.addRow(self.g1name, self.g1Data)
        Formlayout1.addRow(self.g1rel, self.g1relData)
        Formlayout1.addRow(self.g1p1, self.g1p1Data)
        Formlayout1.addRow(self.g1p2, self.g1p2Data)
        Formlayout1.addRow(self.g1email, self.g1emailData)
        Formlayout1.addRow(self.g1addr, self.g1addrData)
        
        Formlayout2 = QFormLayout()
        Formlayout2.addRow(self.g2name, self.g2Data)
        Formlayout2.addRow(self.g2rel, self.g2relData)
        Formlayout2.addRow(self.g2p1, self.g2p1Data)
        Formlayout2.addRow(self.g2p2, self.g2p2Data)
        Formlayout2.addRow(self.g2email, self.g2emailData)
        Formlayout2.addRow(self.g2addr, self.g2addrData)
        
        grid1 = QGridLayout()
        grid1.addWidget(self.pb,0,0)
        grid1.addWidget(self.pb1,0,1)
        
        hbox1 = QHBoxLayout()
        hbox1.addLayout(Formlayout1)
        hbox1.addLayout(Formlayout2)
        
        groupBox2 = QGroupBox('GUARDIAN')
        groupBox2.setLayout(hbox1)
        
        vbox1 = QVBoxLayout()
        vbox1.addWidget(groupBox2)
        vbox1.addStretch()
        vbox1.addLayout(grid1)
        
        
        #photo
        self.pic1 = QLabel()
        image1 = Image.open('img/studentz.png')
        self.pic1.resize(100, 150)
        self.pic1.setLabel(image1)
        
        self.pic2 = QLabel()
        image2 = Image.open('img/studentz.png')
        self.pic2.resize(100, 150)
        self.pic2.setPixmap(image2)
        
        self.pic3 = QLabel()
        image3 = Image.open('img/studentz.png')
        self.pic3.resize(100, 150)
        self.pic3.setPixmap(image3)
        
        self.picBtn1 = QPushButton('Select Image')
        self.picBtn1.clicked.connect(self.getFilez)
        
        self.picBtn2 = QPushButton('Select Image')
        self.picBtn2.clicked.connect(self.getFilez)
        
        self.picBtn3 = QPushButton('Select Image')
        self.picBtn3.clicked.connect(self.getFilez)
        
        picGrid = QGridLayout()
        
        picGrid.addWidget(self.pic1, 0, 1)
        picGrid.addWidget(self.pic2, 0, 2)
        picGrid.addWidget(self.pic3, 0, 3)
        
        picGrid.addWidget(self.picBtn1, 1, 1)
        picGrid.addWidget(self.picBtn2, 2, 2)
        picGrid.addWidget(self.picBtn3, 3, 3)

        self.tabz.addTab(self.tab1, 'Bio-Data')
        self.tabz.addTab(self.tab2, 'Contact Details')
        self.tabz.addTab(self.tab3, 'Passports')
        
        #self.tabz.setTabEnabled(1, False)
        #self.tabz.setTabEnabled(2, False)
        
        self.setWindowTitle("Add Student Data")
        self.show()
        
    def getFile(self, a):
        fname = QFileDialog.getOpenFileName(self, 'Open', 'c:\\', "Image File (*.jpg *.png)")
        if a == 1:
            self.pic1.setPixmap(QPixmap(fname))
        elif a == 2:
            self.pic2.setPixmap(QPixmap(fname))
        elif a == 2:
            self.pic3.setPixmap(QPixmap(fname))
            
    def getFilez(self):
         fname = QFileDialog.getOpenFileName(self, 'Open', 'c:\\', "Image File (*.jpg *.png)")
         self.pic1.setPixmap(QPixmap(fname))
        
        
    def contFill(self, a):
        
        sid = a
        data = self.pullStudents(a)
        self.resize(430, 530)
        
        #self.tabz = QTabWidget(self)
        self.tabz.clear()
      
        self.tab1 = QWidget(self)
        self.tab2 = QWidget(self)
        self.tab3 = QWidget(self)
        
        self.schno = QLabel("School Number")
        self.schnoData = QLineEdit()
        self.schnoData.setObjectName("schno")
        if(data['schno'] and  len(data['schno']) > 1):
            self.schnoData.setText(data['schno'])
        else:
            self.schnoData.setPlaceholderText("00000000")
        
        
        self.surname = QLabel("Surname")
        self.surnameData = QLineEdit()
        self.surnameData.setObjectName("surname")
        if(data['surname'] and len(data['surname']) > 1):
            tx = data['surname'] 
            self.surnameData.setText(tx.title())
        else:
            self.surnameData.setPlaceholderText("Surname")
        
        
        self.firstname = QLabel("Firstname")
        self.firstnameData = QLineEdit()
        self.firstnameData.setObjectName("firstname")
        if(data['firstname'] and  len(data['firstname'])):
            tx = data['firstname'] 
            self.firstnameData.setText(tx.title())
        else:
            self.firstnameData.setPlaceholderText("Firstname")
       
        
        self.middlename = QLabel("Middlename")
        self.middlenameData = QLineEdit()
        self.middlenameData.setObjectName("middlename")
        if(data['othername'] and  len(data['othername']) > 1):
            tx = data['othername'] 
            self.middlenameData.setText(tx.title())
        else:
            self.middlenameData.setPlaceholderText("othername")
        
        
        self.soo = QLabel("State/Region of Origin")
        self.sooData = QLineEdit()
        self.sooData.setObjectName("soo")
        if(data['soo'] and  len(data['soo']) > 1):
            tx = data['soo'] 
            self.sooData.setText(tx.title())
        else:
            self.sooData.setPlaceholderText("Lagos")
        
        
        self.lga = QLabel("LGA/District")
        self.lgaData = QLineEdit()
        self.lgaData.setObjectName("lga")
        if(data['lga'] and  len(data['lga'])):
            tx = data['lga'] 
            self.lgaData.setText(tx.title())
        else:
            self.lgaData.setPlaceholderText("Ikeja")
        
        
        self.addr = QLabel("House Address")
        self.addrData = QTextEdit()
        self.addrData.setObjectName("addr")
        if(data['addr'] and  len(data['addr'])):
            tx = data['addr'] 
            self.addrData.setText(tx)
        else:
            pass
       
        self.dob = QLabel("Date of Birth")
        self.dobData = QDateEdit()
        self.dobData.setObjectName("dob")
        tx =  QDate.fromString(data['dob'], 'yyyy-MM-dd')
        self.dobData.setDate(QDate(tx.year(), tx.month(), tx.day()))
        
        self.admit = QLabel("Date Admitted")
        self.admitData = QDateEdit()
        self.admitData.setObjectName("admit")
        tx =  QDate.fromString(data['admit'], 'yyyy-MM-dd')
        self.admitData.setDate(QDate(tx.year(), tx.month(), tx.day()))
        
        self.pb4 = QPushButton()
        self.pb4.setObjectName("Submit")
        self.pb4.setText("Submit")
        
        self.pb5 = QPushButton()
        self.pb5.setObjectName("Cancel")
        self.pb5.setText("Cancel")
        
        hbo = QHBoxLayout()
        self.gender = QLabel('Gender')
        self.r1 = QRadioButton('Male')
        self.r2 = QRadioButton('Female')
        if(data['gender'] == 'Male'):
            self.r1.setChecked(True)
        elif(data['gender'] == 'Female'):
            self.r2.setChecked(True)
            
        hbo.addWidget(self.r1)
        hbo.addWidget(self.r2)
        
        Formlayout = QFormLayout()
        Formlayout.addRow(self.schno, self.schnoData)
        Formlayout.addRow(self.surname, self.surnameData)
        Formlayout.addRow(self.firstname, self.firstnameData)
        Formlayout.addRow(self.middlename, self.middlenameData)
        Formlayout.addRow(self.gender, hbo)
        Formlayout.addRow(self.dob, self.dobData)
        Formlayout.addRow(self.admit, self.admitData)
        Formlayout.addRow(self.soo, self.sooData)
        Formlayout.addRow(self.lga, self.lgaData)
        Formlayout.addRow(self.addr, self.addrData)
        
        grid = QGridLayout()
        grid.addWidget(self.pb1,0,1)
        grid.addWidget(self.pb,0,0)
        
        groupBox = QGroupBox('BIODATA')
        groupBox.setLayout(Formlayout)
        
        vbox = QVBoxLayout()
        vbox.addWidget(groupBox)
        vbox.addStretch()
        vbox.addLayout(grid)
        
        #self.setLayout(vbox)
        self.connect(self.pb4, SIGNAL("clicked()"), lambda: self.button1_click(sid))
        self.connect(self.pb5, SIGNAL("clicked()"), self.close)
        self.tab1.setLayout(vbox)
        
        
        relations = ['Father', 'Mother', 'Aunt', 'Uncle', 'Grand Parent', 'Guardian', 'Others']
        
        #first guardian details
        self.g1name = QLabel("First Guardian")
        self.g1Data = QLineEdit()
        self.g1Data.setObjectName("g1name")
        if(data['g1'] and len(data['g1']) > 1):
            tx = data['g1'] 
            self.g1Data.setText(tx.title())
        else:
            self.g1Data.setPlaceholderText("Mr. Surname Lastname")
        
        self.g1rel = QLabel('Relationship')
        self.g1relData = QComboBox()
        self.g1relData.addItems(relations)
        if data['g1rel'] and  len(data['g1rel']) > 0:
            index1 = self.g1relData.findText(data['g1rel'], Qt.QtMatchFixedString)
            if index1 >= 0:
                self.g1relData.setCurrentIndex(index1)
            
        
        self.g1p1 = QLabel("Phone Number")
        self.g1p1Data = QLineEdit()
        self.g1p1Data.setObjectName("g1p1")
        if(data['g1p1'] and  len(data['g1p1']) > 1):
            tx = data['g1p1'] 
            self.g1p1Data.setText(tx.title())
        else:
            self.g1p1Data.setPlaceholderText("08000000000")
        
        self.g1p2 = QLabel("Alt. Phone Number")
        self.g1p2Data = QLineEdit()
        self.g1p2Data.setObjectName("g1p2")
        if(data['g1p2'] and  len(data['g1p2']) > 1):
            tx = data['g1p2'] 
            self.g1p2Data.setText(tx.title())
        else:
            self.g1p2Data.setPlaceholderText("08000000000")
        
        
        self.g1email = QLabel("Email")
        self.g1emailData = QLineEdit()
        self.g1emailData.setObjectName("g1email")
        if(data['g1email'] and  len(data['g1email']) > 1):
            tx = data['g1email'] 
            self.g1Data.setText(tx.title())
        else:
            self.g1Data.setPlaceholderText("info@email.com")
        
        self.g1addr = QLabel("Address")
        self.g1addrData = QTextEdit()
        self.g1addrData.setObjectName("g1add")
        if(data['g1addr'] and len(data['g1addr']) > 1):
            tx = data['g1addr'] 
            self.g1Data.setText(tx.title())
        else:
            pass
        
         #second guardian details
        self.g2name = QLabel("Second Guardian")
        self.g2Data = QLineEdit()
        self.g2Data.setObjectName("g2name")
        if(data['g2'] and  len(data['g2']) > 1):
            tx = data['g2'] 
            self.g2Data.setText(tx.title())
        else:
            self.g2Data.setPlaceholderText("Title. Surname Lastname")
            
        
        self.g2rel = QLabel('Relationship')
        self.g2relData = QComboBox()
        self.g2relData.addItems(relations)
        if data['g2rel'] and  len(data['g2rel']) > 0:
            index2 = self.g2relData.findText(data['g2rel'], Qt.QtMatchFixedString)
            if index2 >= 0:
                self.g2relData.setCurrentIndex(index2)
                
        
        self.g2p1 = QLabel("Phone Number")
        self.g2p1Data = QLineEdit()
        self.g2p1Data.setObjectName("g2p1")
        if(data['g2p1'] and  len(data['g2p1']) > 1):
            tx = data['g2p1'] 
            self.g2p1Data.setText(tx.title())
        else:
            self.g2p1Data.setPlaceholderText("08000000000")
            
        
        self.g2p2 = QLabel("Alt. Phone Number")
        self.g2p2Data = QLineEdit()
        self.g2p2Data.setObjectName("g2p2")
        if(data['g2p2'] and  len(data['g2p2']) > 1):
            tx = data['g2p2'] 
            self.g2p2Data.setText(tx.title())
        else:
            self.g2p2Data.setPlaceholderText("0800000000")
            
        
        self.g2email = QLabel("Email")
        self.g2emailData = QLineEdit()
        self.g2emailData.setObjectName("g2email")
        if(data['g2email'] and  len(data['g2email']) > 1):
            tx = data['g2email'] 
            self.g2emailData.setText(tx.title())
        else:
            self.g2emailData.setPlaceholderText("info@email.com")
            
        
        self.g2addr = QLabel("Address")
        self.g2addrData = QTextEdit()
        self.g2addrData.setObjectName("g2add")
        if(data['g2addr'] and len(data['g2addr']) > 1):
            tx = data['g2addr'] 
            self.g2Data.setText(tx.title())
        else:
            pass


        self.pb = QPushButton()
        self.pb.setObjectName("Submit")
        self.pb.setText("Submit")
        
        self.pb1 = QPushButton()
        self.pb1.setObjectName("Cancel")
        self.pb1.setText("Cancel")
        
        hbo = QHBoxLayout()
        
        self.gender = QLabel('Gender')
        self.r1 = QRadioButton('Male')
        self.r2 = QRadioButton('Female')
        hbo.addWidget(self.r1)
        hbo.addWidget(self.r2)
        
        
        Formlayout1 = QFormLayout()
        Formlayout1.addRow(self.g1name, self.g1Data)
        Formlayout1.addRow(self.g1rel, self.g1relData)
        Formlayout1.addRow(self.g1p1, self.g1p1Data)
        Formlayout1.addRow(self.g1p2, self.g1p2Data)
        Formlayout1.addRow(self.g1email, self.g1emailData)
        Formlayout1.addRow(self.g1addr, self.g1addrData)
        
        Formlayout2 = QFormLayout()
        Formlayout2.addRow(self.g2name, self.g2Data)
        Formlayout2.addRow(self.g2rel, self.g2relData)
        Formlayout2.addRow(self.g2p1, self.g2p1Data)
        Formlayout2.addRow(self.g2p2, self.g2p2Data)
        Formlayout2.addRow(self.g2email, self.g2emailData)
        Formlayout2.addRow(self.g2addr, self.g2addrData)
        
        grid1 = QGridLayout()
        grid1.addWidget(self.pb,0,0)
        grid1.addWidget(self.pb1,0,1)
        
        hbox1 = QHBoxLayout()
        hbox1.addLayout(Formlayout1)
        hbox1.addStretch()
        hbox1.addLayout(Formlayout2)
        
        groupBox2 = QGroupBox('GUARDIAN')
        groupBox2.setLayout(hbox1)
        
        vbox1 = QVBoxLayout()
        vbox1.addWidget(groupBox2)
        vbox1.addStretch()
        vbox1.addLayout(grid1)
        
        self.tab2.setLayout(vbox1)
        
        #photo
        picstyle = QSize(120, 180)
        picstyle1 = Qt.KeepAspectRatio
        
        self.pic1Lbl = QLabel('YEAR 1 & 2')
        self.pic2Lbl = QLabel('YEAR 3 & 4')
        self.pic3Lbl = QLabel('YEAR 5 & 6')
        
        
        self.pic1 = QLabel()
        pixmap1 = QPixmap('img/studentz.png').scaled(picstyle, picstyle1)
        self.pic1.setPixmap(pixmap1)
        
        self.pic2 = QLabel()
        pixmap2 = QPixmap('img/studentz.png').scaled(picstyle, picstyle1)
        self.pic2.setPixmap(pixmap2)
        
        self.pic3 = QLabel()
        pixmap3 = QPixmap('img/studentz.png').scaled(picstyle, picstyle1)
        self.pic3.setPixmap(pixmap3)
        
        self.picBtn1 = QPushButton('Select Image')
        self.picBtn1.clicked.connect(self.getFilez)
        
        self.picBtn2 = QPushButton('Select Image')
        self.picBtn2.clicked.connect(self.getFilez)
        
        self.picBtn3 = QPushButton('Select Image')
        self.picBtn3.clicked.connect(self.getFilez)
    
        self.pic1Lbl.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.pic2Lbl.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.pic3Lbl.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        
        self.picBtn1.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.picBtn2.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.picBtn3.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        
        h1pic  = QVBoxLayout()
        h2pic  = QVBoxLayout()
        h3pic  = QVBoxLayout()
        vpic  = QHBoxLayout()
        
        h1pic.addWidget(self.pic1Lbl)
        h1pic.addStretch(0)
        h1pic.addWidget(self.pic1)
        h1pic.addStretch(0)
        h1pic.addWidget(self.picBtn1)
        h1pic.setContentsMargins(0,0,0,0)
        h1pic.setSpacing(0)
        h1pic.setMargin(0)
        
        
        h2pic.addWidget(self.pic2Lbl)
        h2pic.addStretch(0)
        h2pic.addWidget(self.pic2)
        h2pic.addStretch(0)
        h2pic.addWidget(self.picBtn2)
        h2pic.setContentsMargins(0,0,0,0)
        h2pic.setSpacing(0)
        h2pic.setMargin(0)
        
        h3pic.addWidget(self.pic3Lbl)
        h3pic.addStretch(0)
        h3pic.addWidget(self.pic3)
        h3pic.addStretch(0)
        h3pic.addWidget(self.picBtn3)
        h3pic.setContentsMargins(0,0,0,0)
        h3pic.setSpacing(0)
        h3pic.setMargin(0)
        
        vpic.addLayout(h1pic)
        vpic.addStretch(0)
        vpic.addLayout(h2pic)
        vpic.addStretch(0)
        vpic.addLayout(h3pic)
        vpic.setSpacing(0)
        vpic.setMargin(0)
        vpic.setContentsMargins(0,0,0,0)
        
        
        self.tab3.setLayout(vpic)
        self.tab3.resize(100, 100)
        #self.tab3.setStyleSheet("background-color: red; margin:5px; border:1px solid red;")

        self.tabz.addTab(self.tab1, 'Bio-Data')
        self.tabz.addTab(self.tab2, 'Contact Details')
        self.tabz.addTab(self.tab3, 'Passports')
        
        self.setWindowTitle("Add Student Data")
        self.show()    
        
    def eContFill(self, a):
        
        sid = 23
        data = self.pullStudents(a)
        self.resize(430, 530)
        
        #self.tabz = QTabWidget(self)
        self.tabz.clear()
      
        self.tab1 = QWidget(self)
        self.tab2 = QWidget(self)
        self.tab3 = QWidget(self)
        
        self.schno = QLabel("School Number")
        self.schnoData = QLineEdit()
        self.schnoData.setObjectName("schno")
        if(data['schno'] and  len(data['schno']) > 1):
            self.schnoData.setText(data['schno'])
        else:
            self.schnoData.setPlaceholderText("00000000")
        
        
        self.surname = QLabel("Surname")
        self.surnameData = QLineEdit()
        self.surnameData.setObjectName("surname")
        if(data['surname'] and len(data['surname']) > 1):
            tx = data['surname'] 
            self.surnameData.setText(tx.title())
        else:
            self.surnameData.setPlaceholderText("Surname")
        
        
        self.firstname = QLabel("Firstname")
        self.firstnameData = QLineEdit()
        self.firstnameData.setObjectName("firstname")
        if(data['firstname'] and  len(data['firstname'])):
            tx = data['firstname'] 
            self.firstnameData.setText(tx.title())
        else:
            self.firstnameData.setPlaceholderText("Firstname")
       
        
        self.middlename = QLabel("Middlename")
        self.middlenameData = QLineEdit()
        self.middlenameData.setObjectName("middlename")
        if(data['othername'] and  len(data['othername']) > 1):
            tx = data['othername'] 
            self.middlenameData.setText(tx.title())
        else:
            self.middlenameData.setPlaceholderText("othername")
        
        
        self.soo = QLabel("State/Region of Origin")
        self.sooData = QLineEdit()
        self.sooData.setObjectName("soo")
        if(data['soo'] and  len(data['soo']) > 1):
            tx = data['soo'] 
            self.sooData.setText(tx.title())
        else:
            self.sooData.setPlaceholderText("Lagos")
        
        
        self.lga = QLabel("LGA/District")
        self.lgaData = QLineEdit()
        self.lgaData.setObjectName("lga")
        if(data['lga'] and  len(data['lga'])):
            tx = data['lga'] 
            self.lgaData.setText(tx.title())
        else:
            self.lgaData.setPlaceholderText("Ikeja")
        
        
        self.addr = QLabel("House Address")
        self.addrData = QTextEdit()
        self.addrData.setObjectName("addr")
        if(data['addr'] and  len(data['addr'])):
            tx = data['addr'] 
            self.addrData.setText(tx)
        else:
            pass
       
        self.dob = QLabel("Date of Birth")
        self.dobData = QDateEdit()
        self.dobData.setObjectName("dob")
        tx =  QDate.fromString(data['dob'], 'yyyy-MM-dd')
        self.dobData.setDate(QDate(tx.year(), tx.month(), tx.day()))
        
        self.admit = QLabel("Date Admitted")
        self.admitData = QDateEdit()
        self.admitData.setObjectName("admit")
        tx =  QDate.fromString(data['admit'], 'yyyy-MM-dd')
        self.admitData.setDate(QDate(tx.year(), tx.month(), tx.day()))
        
        self.pb4 = QPushButton()
        self.pb4.setObjectName("Submit")
        self.pb4.setText("Submit")
        
        self.pb5 = QPushButton()
        self.pb5.setObjectName("Cancel")
        self.pb5.setText("Cancel")
        
        hbo = QHBoxLayout()
        self.gender = QLabel('Gender')
        self.r1 = QRadioButton('Male')
        self.r2 = QRadioButton('Female')
        if(data['gender'] == 'Male'):
            self.r1.setChecked(True)
        elif(data['gender'] == 'Female'):
            self.r2.setChecked(True)
            
        hbo.addWidget(self.r1)
        hbo.addWidget(self.r2)
        
        Formlayout = QFormLayout()
        Formlayout.addRow(self.schno, self.schnoData)
        Formlayout.addRow(self.surname, self.surnameData)
        Formlayout.addRow(self.firstname, self.firstnameData)
        Formlayout.addRow(self.middlename, self.middlenameData)
        Formlayout.addRow(self.gender, hbo)
        Formlayout.addRow(self.dob, self.dobData)
        Formlayout.addRow(self.admit, self.admitData)
        Formlayout.addRow(self.soo, self.sooData)
        Formlayout.addRow(self.lga, self.lgaData)
        Formlayout.addRow(self.addr, self.addrData)
        
        grid = QGridLayout()
        grid.addWidget(self.pb1,0,1)
        grid.addWidget(self.pb,0,0)
        
        groupBox = QGroupBox('BIODATA')
        groupBox.setLayout(Formlayout)
        
        vbox = QVBoxLayout()
        vbox.addWidget(groupBox)
        vbox.addStretch()
        vbox.addLayout(grid)
        
        #self.setLayout(vbox)
        self.connect(self.pb4, SIGNAL("clicked()"), lambda: self.button1_click(sid))
        self.connect(self.pb5, SIGNAL("clicked()"), self.close)
        self.tab1.setLayout(vbox)
        
        
        relations = ['Father', 'Mother', 'Aunt', 'Uncle', 'Grand Parent', 'Guardian', 'Others']
        
        #first guardian details
        self.g1name = QLabel("First Guardian")
        self.g1Data = QLineEdit()
        self.g1Data.setObjectName("g1name")
        if(data['g1'] and len(data['g1']) > 1):
            tx = data['g1'] 
            self.g1Data.setText(tx.title())
        else:
            self.g1Data.setPlaceholderText("Mr. Surname Lastname")
        
        self.g1rel = QLabel('Relationship')
        self.g1relData = QComboBox()
        self.g1relData.addItems(relations)
        if data['g1rel'] and  len(data['g1rel']) > 0:
            index1 = self.g1relData.findText(data['g1rel'], Qt.QtMatchFixedString)
            if index1 >= 0:
                self.g1relData.setCurrentIndex(index1)
            
        
        self.g1p1 = QLabel("Phone Number")
        self.g1p1Data = QLineEdit()
        self.g1p1Data.setObjectName("g1p1")
        if(data['g1p1'] and  len(data['g1p1']) > 1):
            tx = data['g1p1'] 
            self.g1p1Data.setText(tx.title())
        else:
            self.g1p1Data.setPlaceholderText("08000000000")
        
        self.g1p2 = QLabel("Alt. Phone Number")
        self.g1p2Data = QLineEdit()
        self.g1p2Data.setObjectName("g1p2")
        if(data['g1p2'] and  len(data['g1p2']) > 1):
            tx = data['g1p2'] 
            self.g1p2Data.setText(tx.title())
        else:
            self.g1p2Data.setPlaceholderText("08000000000")
        
        
        self.g1email = QLabel("Email")
        self.g1emailData = QLineEdit()
        self.g1emailData.setObjectName("g1email")
        if(data['g1email'] and  len(data['g1email']) > 1):
            tx = data['g1email'] 
            self.g1Data.setText(tx.title())
        else:
            self.g1Data.setPlaceholderText("info@email.com")
        
        self.g1addr = QLabel("Address")
        self.g1addrData = QTextEdit()
        self.g1addrData.setObjectName("g1add")
        if(data['g1addr'] and len(data['g1addr']) > 1):
            tx = data['g1addr'] 
            self.g1Data.setText(tx.title())
        else:
            pass
        
         #second guardian details
        self.g2name = QLabel("Second Guardian")
        self.g2Data = QLineEdit()
        self.g2Data.setObjectName("g2name")
        if(data['g2'] and  len(data['g2']) > 1):
            tx = data['g2'] 
            self.g2Data.setText(tx.title())
        else:
            self.g2Data.setPlaceholderText("Title. Surname Lastname")
            
        
        self.g2rel = QLabel('Relationship')
        self.g2relData = QComboBox()
        self.g2relData.addItems(relations)
        if data['g2rel'] and  len(data['g2rel']) > 0:
            index2 = self.g2relData.findText(data['g2rel'], Qt.QtMatchFixedString)
            if index2 >= 0:
                self.g2relData.setCurrentIndex(index2)
                
        
        self.g2p1 = QLabel("Phone Number")
        self.g2p1Data = QLineEdit()
        self.g2p1Data.setObjectName("g2p1")
        if(data['g2p1'] and  len(data['g2p1']) > 1):
            tx = data['g2p1'] 
            self.g2p1Data.setText(tx.title())
        else:
            self.g2p1Data.setPlaceholderText("08000000000")
            
        
        self.g2p2 = QLabel("Alt. Phone Number")
        self.g2p2Data = QLineEdit()
        self.g2p2Data.setObjectName("g2p2")
        if(data['g2p2'] and  len(data['g2p2']) > 1):
            tx = data['g2p2'] 
            self.g2p2Data.setText(tx.title())
        else:
            self.g2p2Data.setPlaceholderText("0800000000")
            
        
        self.g2email = QLabel("Email")
        self.g2emailData = QLineEdit()
        self.g2emailData.setObjectName("g2email")
        if(data['g2email'] and  len(data['g2email']) > 1):
            tx = data['g2email'] 
            self.g2emailData.setText(tx.title())
        else:
            self.g2emailData.setPlaceholderText("info@email.com")
            
        
        self.g2addr = QLabel("Address")
        self.g2addrData = QTextEdit()
        self.g2addrData.setObjectName("g2add")
        if(data['g2addr'] and len(data['g2addr']) > 1):
            tx = data['g2addr'] 
            self.g2Data.setText(tx.title())
        else:
            pass


        self.pb = QPushButton()
        self.pb.setObjectName("Submit")
        self.pb.setText("Submit")
        
        self.pb1 = QPushButton()
        self.pb1.setObjectName("Cancel")
        self.pb1.setText("Cancel")
        
        hbo = QHBoxLayout()
        
        self.gender = QLabel('Gender')
        self.r1 = QRadioButton('Male')
        self.r2 = QRadioButton('Female')
        hbo.addWidget(self.r1)
        hbo.addWidget(self.r2)
        
        
        Formlayout1 = QFormLayout()
        Formlayout1.addRow(self.g1name, self.g1Data)
        Formlayout1.addRow(self.g1rel, self.g1relData)
        Formlayout1.addRow(self.g1p1, self.g1p1Data)
        Formlayout1.addRow(self.g1p2, self.g1p2Data)
        Formlayout1.addRow(self.g1email, self.g1emailData)
        Formlayout1.addRow(self.g1addr, self.g1addrData)
        
        Formlayout2 = QFormLayout()
        Formlayout2.addRow(self.g2name, self.g2Data)
        Formlayout2.addRow(self.g2rel, self.g2relData)
        Formlayout2.addRow(self.g2p1, self.g2p1Data)
        Formlayout2.addRow(self.g2p2, self.g2p2Data)
        Formlayout2.addRow(self.g2email, self.g2emailData)
        Formlayout2.addRow(self.g2addr, self.g2addrData)
        
        grid1 = QGridLayout()
        grid1.addWidget(self.pb,0,0)
        grid1.addWidget(self.pb1,0,1)
        
        hbox1 = QHBoxLayout()
        hbox1.addLayout(Formlayout1)
        hbox1.addStretch()
        hbox1.addLayout(Formlayout2)
        
        groupBox2 = QGroupBox('GUARDIAN')
        groupBox2.setLayout(hbox1)
        
        vbox1 = QVBoxLayout()
        vbox1.addWidget(groupBox2)
        vbox1.addStretch()
        vbox1.addLayout(grid1)
        
        self.tab2.setLayout(vbox1)
        
        #photo
        picstyle = QSize(120, 180)
        picstyle1 = Qt.KeepAspectRatio
        
        self.pic1Lbl = QLabel('YEAR 1 & 2')
        self.pic2Lbl = QLabel('YEAR 3 & 4')
        self.pic3Lbl = QLabel('YEAR 5 & 6')
        
        
        self.pic1 = QLabel()
        pixmap1 = QPixmap('img/studentz.png').scaled(picstyle, picstyle1)
        self.pic1.setPixmap(pixmap1)
        
        self.pic2 = QLabel()
        pixmap2 = QPixmap('img/studentz.png').scaled(picstyle, picstyle1)
        self.pic2.setPixmap(pixmap2)
        
        self.pic3 = QLabel()
        pixmap3 = QPixmap('img/studentz.png').scaled(picstyle, picstyle1)
        self.pic3.setPixmap(pixmap3)
        
        self.picBtn1 = QPushButton('Select Image')
        self.picBtn1.clicked.connect(self.getFilez)
        
        self.picBtn2 = QPushButton('Select Image')
        self.picBtn2.clicked.connect(self.getFilez)
        
        self.picBtn3 = QPushButton('Select Image')
        self.picBtn3.clicked.connect(self.getFilez)
    
        self.pic1Lbl.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.pic2Lbl.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.pic3Lbl.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        
        self.picBtn1.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.picBtn2.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.picBtn3.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        
        h1pic  = QVBoxLayout()
        h2pic  = QVBoxLayout()
        h3pic  = QVBoxLayout()
        vpic  = QHBoxLayout()
        
        h1pic.addWidget(self.pic1Lbl)
        h1pic.addStretch(0)
        h1pic.addWidget(self.pic1)
        h1pic.addStretch(0)
        h1pic.addWidget(self.picBtn1)
        h1pic.setContentsMargins(0,0,0,0)
        h1pic.setSpacing(0)
        h1pic.setMargin(0)
        
        
        h2pic.addWidget(self.pic2Lbl)
        h2pic.addStretch(0)
        h2pic.addWidget(self.pic2)
        h2pic.addStretch(0)
        h2pic.addWidget(self.picBtn2)
        h2pic.setContentsMargins(0,0,0,0)
        h2pic.setSpacing(0)
        h2pic.setMargin(0)
        
        h3pic.addWidget(self.pic3Lbl)
        h3pic.addStretch(0)
        h3pic.addWidget(self.pic3)
        h3pic.addStretch(0)
        h3pic.addWidget(self.picBtn3)
        h3pic.setContentsMargins(0,0,0,0)
        h3pic.setSpacing(0)
        h3pic.setMargin(0)
        
        vpic.addLayout(h1pic)
        vpic.addStretch(0)
        vpic.addLayout(h2pic)
        vpic.addStretch(0)
        vpic.addLayout(h3pic)
        vpic.setSpacing(0)
        vpic.setMargin(0)
        vpic.setContentsMargins(0,0,0,0)
        
        
        self.tab3.setLayout(vpic)
        self.tab3.resize(100, 100)
        self.tab3.setStyleSheet("background-color: red; margin:5px; border:1px solid red;")

        self.tabz.addTab(self.tab1, 'Bio-Data')
        self.tabz.addTab(self.tab2, 'Contact Details')
        self.tabz.addTab(self.tab3, 'Passports')
        
        self.setWindowTitle("Add Student Data")
        self.show()    
        
    def button_click(self, a):
        # shost is a QString object
        arr = {}
        arr['schno'] = self.schnoData.text()
        arr['surname'] = self.surnameData.text()
        arr['firstname'] = self.firstnameData.text()
        arr['othername'] = self.middlenameData.text()
        arr['soo'] = self.sooData.text()
        arr['lga'] = self.lgaData.text()
        arr['addr'] = self.addrData.toPlainText()
        dob = self.dobData.date()
        arr['dob'] = dob.toPyDate()
        admit = self.admitData.date()
        arr['admit'] = admit.toPyDate()
        arr['active'] = 0
        if self.r1.isChecked():
           arr['gender'] = 0 
        else:
           arr['gender'] = 1
            
        self.a = a
        
        g = Db()
        if((arr['surname']) and (arr['firstname']) and (arr['schno'])):
            h = g.insert('students', arr)
            
        self.contFill(h)
    
    def button1_click(self, a):
        # shost is a QString object
        arr = {}
        arr['schno'] = self.schnoData.text()
        arr['surname'] = self.surnameData.text()
        arr['firstname'] = self.firstnameData.text()
        arr['othername'] = self.middlenameData.text()
        arr['soo'] = self.sooData.text()
        arr['lga'] = self.lgaData.text()
        arr['addr'] = self.addrData.toPlainText()
        dob = self.dobData.date()
        arr['dob'] = dob.toPyDate()
        admit = self.admitData.date()
        arr['admit'] = admit.toPyDate()
        arr['active'] = 0
        
        arr['g1'] = self.g1Data.text()
        arr['g1rel'] = self.g1relData.itemData(self.g1relData.currentIndex())
        arr['g1p1'] = self.g1p1Data.text()
        arr['g1p2'] = self.g1p2Data.text()
        arr['g1email'] = self.g1emailData.text()
        arr['g1addr'] = self.g1addData.text()
        arr['g2'] = self.g2Data.text()
        arr['g2rel'] = self.g2relData.itemData(self.g2relData.currentIndex())
        arr['g2p1'] = self.g2p1Data.text()
        arr['g2p2'] = self.g2p2Data.text()
        arr['g2email'] = self.g2emailData.text()
        arr['g2addr'] = self.g2addData.text()
        
        self.a = a
        print(arr)
        g = Db()
        if((arr['surname']) and (arr['firstname']) and (arr['schno'])):
            r = g.update('students', arr, {'id':self.a})
        print(r)
        self.close()

    def button_click1(self, a):
        # shost is a QString object
        s1 = self.le.text()
        s2 = self.le2.text()
        self.a = a
        g = Db()
        if(len(s1) > 0):
            y = { 'name':s1, 'subID': self.a, 'abbrv':s2}
            j = g.insert('datas', y)
            return j 
        
    def pullClass(self, a):
        self.a = a
        cn = Db()
        students = cn.select('datas', '' , '', {'subID':self.a})
        arr = {}
        
        for j in students:
            arr[j[0]] = j[2]
        return arr
    
    def pullStudents(self, a):
        self.a = a
        cn = Db()
        students = cn.selectn('students', '' , 1, {'id':self.a})
        return students
    
    def lunchUnitForm(self, a):
        self.a = a
        
        self.form = UnitForm(self.a)
        self.form.show()
        #form.exec_()
        


