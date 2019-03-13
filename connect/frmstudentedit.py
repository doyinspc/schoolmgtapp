# -*- coding: utf-8 -*-
"""
Created on Sat Nov 17 05:44:29 2018

@author: CHARLES
"""

from PyQt4.QtCore import SIGNAL, QDate, Qt, QSize
from PyQt4.QtGui import QAction, QToolBar,  QMenuBar, QStatusBar, QTextListFormat, QTextCharFormat, QFontComboBox, QColorDialog, QPrintDialog, QPrintPreviewDialog, QMenu, QSplitter, QFrame, QIcon, QTreeWidgetItem, QTreeWidget, QWidget, QTextDocument, QTextCursor, QImage, QFileDialog, QFont, QPixmap, QTabWidget, QComboBox, QRadioButton, QDateEdit, QTextEdit, QCheckBox, QHBoxLayout, QGroupBox, QGridLayout, QDialog, QApplication, QPushButton, QLineEdit, QFormLayout, QLabel, QVBoxLayout, QSizePolicy
from connect import Db
from jinja2 import Template
from PIL import Image
from PIL.ImageQt import ImageQt
import cv2
import os
from datetime import datetime
from ext import find
import time
from frmstudentclasssubject import FormClassSubject, FormStudentMedical, FormStudentConduct, FormStudentMisconduct

class StudentEditForm(QDialog):
    
    def __init__(self, sids, es, parent=None):
        super(StudentEditForm, self).__init__(parent)
        
        sid = sids
        self.sid = sid
        data = self.pullStudents(sid)
        cn = Db()
        self.myterms = cn.getTermClass(self.sid)
        activeTerm = self.pullData('terms', 1,{'active':1})
        self.term = activeTerm['id']
        self.sessionID  = activeTerm['sessionID']
        session = self.pullData('session', 1 , {'id':activeTerm['sessionID']})
        self.session = str(str(session['name'])+" "+str(activeTerm['name']+" Term")).title()
        
        self.tabz = QTabWidget(self)
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tab4 = QWidget()
        self.tab5 = QWidget()
        self.tab6 = QWidget()
        self.tab7 = QWidget()
        self.tab8 = QWidget()
        self.tab9 = QWidget()
        
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
        grid.addWidget(self.pb5,0,1)
        grid.addWidget(self.pb4,0,0)
        
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
            index1 = self.g1relData.findText(data['g1rel'])
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
            index2 = self.g2relData.findText(data['g2rel'])
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
        
        #photo
        self.pic1 = QLabel()
        if os.path.isfile('./pic_main/'+str(data['pix1'])):
            image1 = Image.open('pic_main/'+str(data['pix1']))
        else:
            image1 = Image.open('img/stdpic.png')
            
        imageQ1 = ImageQt(image1)
        imagep1 = QPixmap(QPixmap.fromImage(QImage(imageQ1).scaled(130, 130, Qt.IgnoreAspectRatio)))
        self.pic1.resize(150, 150)
        self.pic1.setPixmap(imagep1)
       
        
        self.pic2 = QLabel()
        if os.path.isfile('./pic_main/'+str(data['pix2'])):
            image2 = Image.open('pic_main/'+str(data['pix2']))
        else:
            image2 = Image.open('img/stdpic.png')
        imageQ2 = ImageQt(image2)
        imagep2 = QPixmap(QPixmap.fromImage(QImage(imageQ2).scaled(130, 130, Qt.IgnoreAspectRatio)))
        self.pic2.resize(150, 150)
        self.pic2.setPixmap(imagep2)
        
        
        self.pic3 = QLabel()
        if os.path.isfile('./pic_main/'+str(data['pix3'])):
            image3 = Image.open('pic_main/'+str(data['pix3']))
        else:
            image3 = Image.open('img/stdpic.png')
            
        imageQ3 = ImageQt(image3)
        imagep3 = QPixmap(QPixmap.fromImage(QImage(imageQ3).scaled(130, 130, Qt.IgnoreAspectRatio)))
        self.pic3.resize(150, 150)
        self.pic3.setPixmap(imagep3)
        
        self.pic1Lbl.setMaximumHeight(30)
        self.pic2Lbl.setMaximumHeight(30)
        self.pic3Lbl.setMaximumHeight(30)
        
        self.pic1.setMaximumHeight(130)
        self.pic2.setMaximumHeight(130)
        self.pic3.setMaximumHeight(130)
        self.pic1.setMaximumWidth(130)
        self.pic2.setMaximumWidth(130)
        self.pic3.setMaximumWidth(130)
        
        self.picBtn1 = QPushButton('Select Image')
        self.picBtn2 = QPushButton('Select Image')
        self.picBtn3 = QPushButton('Select Image')
        
        self.picRad1 = QRadioButton('Set as active passport')
        self.picRad2 = QRadioButton('Set as active passport')
        self.picRad3 = QRadioButton('Set as active passport')
        
        self.picRad1.clicked.connect(lambda:self.changeStates(1))
        self.picRad2.clicked.connect(lambda:self.changeStates(2))
        self.picRad3.clicked.connect(lambda:self.changeStates(3))
        
        self.picBtn1.clicked.connect(lambda:self.getFilez(1))
        self.picBtn2.clicked.connect(lambda:self.getFilez(2))
        self.picBtn3.clicked.connect(lambda:self.getFilez(3))
        
        self.picBtnx1 = QPushButton('Save')
        self.picBtnx2 = QPushButton('Save')
        self.picBtnx3 = QPushButton('Save')
        
        self.picBtnx1.clicked.connect(lambda:self.getSave(1))
        self.picBtnx2.clicked.connect(lambda:self.getSave(2))
        self.picBtnx3.clicked.connect(lambda:self.getSave(3))
        
        self.picBtn1.setMaximumHeight(30)
        self.picBtn2.setMaximumHeight(30)
        self.picBtn3.setMaximumHeight(30)
        
        self.picBtnx1.setMaximumHeight(30)
        self.picBtnx2.setMaximumHeight(30)
        self.picBtnx3.setMaximumHeight(30)
        
        picGrid = QGridLayout()
        
        picGrid.addWidget(self.pic1Lbl, 0, 0)
        picGrid.addWidget(self.pic2Lbl, 0, 1)
        picGrid.addWidget(self.pic3Lbl, 0, 2)
        
        picGrid.addWidget(self.pic1, 1, 0)
        picGrid.addWidget(self.pic2, 1, 1)
        picGrid.addWidget(self.pic3, 1, 2)
        
        picGrid.addWidget(self.picBtn1, 2, 0)
        picGrid.addWidget(self.picBtn2, 2, 1)
        picGrid.addWidget(self.picBtn3, 2, 2)
        
        picGrid.addWidget(self.picBtnx1, 3, 0)
        picGrid.addWidget(self.picBtnx2, 3, 1)
        picGrid.addWidget(self.picBtnx3, 3, 2)
        
        picGrid.addWidget(self.picRad1, 4, 0)
        picGrid.addWidget(self.picRad2, 4, 1)
        picGrid.addWidget(self.picRad3, 4, 2)
        
        self.pic1Lbl.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.pic2Lbl.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.pic3Lbl.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        
        self.picBtn1.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.picBtn2.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.picBtn3.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        
        gridWidget = QWidget()
        gridWidget.setLayout(picGrid)
        gridWidget.setMaximumHeight(250)
        gridWidget.setContentsMargins(0, 0, 0, 0)
        
        currentPics = QVBoxLayout()
        
        self.picMain = QLabel()
        if data['pix'] and int(data['pix']) == 1:
            imgg = data['pix1']
            self.picRad1.setChecked(True)
        elif data['pix'] and int(data['pix']) == 2:
            imgg = data['pix2']
            self.picRad2.setChecked(True)
        elif data['pix'] and int(data['pix']) == 3:
            imgg = data['pix3']
            self.picRad3.setChecked(True)
        else:
            imgg = ''
        
        if os.path.isfile('./pic_main/'+str(imgg)):
            imageMain = Image.open('pic_main/'+str(imgg))
        else:
            imageMain = Image.open('img/stdpic.png')
     
        imageQMain = ImageQt(imageMain)
        imagepMain = QPixmap(QPixmap.fromImage(QImage(imageQMain).scaled(250, 300, Qt.IgnoreAspectRatio)))
        self.picMain.resize(250, 300)
        self.picMain.setPixmap(imagepMain)
        self.picMain.setAlignment(Qt.AlignCenter)
        currentPics.addWidget(self.picMain)
        
        h1pic  = QVBoxLayout()
        h1pic.addWidget(gridWidget)
        h1pic.addLayout(currentPics)
        
        groupBox3 = QGroupBox('PASSPORTS')
        groupBox3.setLayout(h1pic)
        
        mbox = QHBoxLayout()
        mbox.addWidget(groupBox3)
        
        self.tab3.setLayout(mbox)
        
        # class subject
        class_head_box_lbl1 = QLabel('SESSION: ')
        class_head_box_lbl2 = QLabel(self.session)
        class_head_box_btn = QPushButton('Add')
        class_head_box_btn.clicked.connect(lambda:self.lunchMedical())
        
        class_head_box = QHBoxLayout()
        class_head_box.addWidget(class_head_box_lbl1)
        class_head_box.addWidget(class_head_box_lbl2)
        class_head_box.addStretch()
        class_head_box.addWidget(class_head_box_btn)
        
        class_head_box_widget = QWidget()
        class_head_box_widget.setMaximumHeight(50)
        class_head_box_widget.setContentsMargins(0, 0, 0, 0)
        class_head_box_widget.setLayout(class_head_box)
        
        class_text_box = QHBoxLayout()
        self.doc = QTextEdit()
        self.doc.setText('okjhbvjhbhbhjbbjbjhbjj')
        
        #self.reloadStudentMedical()
        
        #tb = QTextTable()
            
        class_text_box.addWidget(self.doc)
        class_text_box_widget = QWidget()
        class_text_box_widget.setContentsMargins(0, 0, 0, 0)
        #class_text_box_widget.setStyleSheet('background-color: #022140')
        class_text_box_widget.setLayout(class_text_box)
        
        class_main_box = QVBoxLayout()
        class_main_box.addWidget(class_head_box_widget)
        class_main_box.addWidget(class_text_box_widget)
        self.tab4.setLayout(class_main_box)
        
        # medical
        medical_head_box_lbl1 = QLabel('SESSION: ')
        medical_head_box_lbl2 = QLabel(self.session)
        medical_head_box_btn = QPushButton('Add')
        medical_head_box_btnEdit = QPushButton('Edit Number')
        medical_head_box_btnDelete = QPushButton('Delete Number')
        medical_head_box_btn.clicked.connect(lambda:self.lunchMedical())
        
        medical_head_box = QHBoxLayout()
        medical_head_box.addWidget(medical_head_box_lbl1)
        medical_head_box.addWidget(medical_head_box_lbl2)
        medical_head_box.addStretch()
        medical_head_box.addWidget(medical_head_box_btn)
        medical_head_box.addWidget(medical_head_box_btnEdit)
        medical_head_box.addWidget(medical_head_box_btnDelete)
        
        medical_head_box_widget = QWidget()
        medical_head_box_widget.setMaximumHeight(50)
        medical_head_box_widget.setContentsMargins(0, 0, 0, 0)
        medical_head_box_widget.setLayout(medical_head_box)
        
        medical_text_box = QHBoxLayout()
        self.docMedical = QTextEdit()
        self.docMedical.setText('aa')
        
        rollz = self.reloadStudentMedical()
        menu = QMenu()
        for a in rollz:
            menu.addAction('No.'+str(a), lambda x = a :self.lunchMedical(x))
        
        menu1 = QMenu()
        for a in rollz:
            menu1.addAction('No.'+str(a), lambda x = a :self.lunchMedical(x))
        #tb = QTextTable()
        
        medical_head_box_btnEdit.setMenu(menu)
        medical_head_box_btnDelete.setMenu(menu)
        
        medical_text_box.addWidget(self.docMedical)
        medical_text_box_widget = QWidget()
        medical_text_box_widget.setContentsMargins(0, 0, 0, 0)
        #class_text_box_widget.setStyleSheet('background-color: #022140')
        medical_text_box_widget.setLayout(medical_text_box)
        
        medical_main_box = QVBoxLayout()
        medical_main_box.addWidget(medical_head_box_widget)
        medical_main_box.addWidget(medical_text_box_widget)
        self.tab5.setLayout(medical_main_box)
        
        # conduct
        conduct_head_box_lbl1 = QLabel('SESSION: ')
        conduct_head_box_lbl2 = QLabel(self.session)
        conduct_head_box_btn = QPushButton('Add')
        conduct_head_box_btnEdit = QPushButton('Edit Number')
        conduct_head_box_btnDelete = QPushButton('Delete Number')
        conduct_head_box_btn.clicked.connect(lambda:self.lunchConduct())
        
        conduct_head_box = QHBoxLayout()
        conduct_head_box.addWidget(conduct_head_box_lbl1)
        conduct_head_box.addWidget(conduct_head_box_lbl2)
        conduct_head_box.addStretch()
        conduct_head_box.addWidget(conduct_head_box_btn)
        conduct_head_box.addWidget(conduct_head_box_btnEdit)
        conduct_head_box.addWidget(conduct_head_box_btnDelete)
        
        conduct_head_box_widget = QWidget()
        conduct_head_box_widget.setMaximumHeight(50)
        conduct_head_box_widget.setContentsMargins(0, 0, 0, 0)
        conduct_head_box_widget.setLayout(conduct_head_box)
        
        conduct_text_box = QHBoxLayout()
        self.docConduct = QTextEdit()
        self.docConduct.setText('aa')
        
        rollz = self.reloadStudentConduct()
        menu = QMenu()
        for a in rollz:
            menu.addAction('No.'+str(a), lambda x = a :self.lunchConduct(x))
        
        menu1 = QMenu()
        for a in rollz:
            menu1.addAction('No.'+str(a), lambda x = a :self.lunchConduct(x))
        #tb = QTextTable()
        
        conduct_head_box_btnEdit.setMenu(menu)
        conduct_head_box_btnDelete.setMenu(menu)
        
        conduct_text_box.addWidget(self.docConduct)
        conduct_text_box_widget = QWidget()
        conduct_text_box_widget.setContentsMargins(0, 0, 0, 0)
        #class_text_box_widget.setStyleSheet('background-color: #022140')
        conduct_text_box_widget.setLayout(conduct_text_box)
        
        conduct_main_box = QVBoxLayout()
        conduct_main_box.addWidget(conduct_head_box_widget)
        conduct_main_box.addWidget(conduct_text_box_widget)
        self.tab6.setLayout(conduct_main_box)
        
        #misconduct
        misconduct_head_box_lbl1 = QLabel('SESSION: ')
        misconduct_head_box_lbl2 = QLabel(self.session)
        misconduct_head_box_btn = QPushButton('Add')
        misconduct_head_box_btnEdit = QPushButton('Edit Number')
        misconduct_head_box_btnDelete = QPushButton('Delete Number')
        misconduct_head_box_btn.clicked.connect(lambda:self.lunchMisconduct())
        
        misconduct_head_box = QHBoxLayout()
        misconduct_head_box.addWidget(misconduct_head_box_lbl1)
        misconduct_head_box.addWidget(misconduct_head_box_lbl2)
        misconduct_head_box.addStretch()
        misconduct_head_box.addWidget(misconduct_head_box_btn)
        misconduct_head_box.addWidget(misconduct_head_box_btnEdit)
        misconduct_head_box.addWidget(misconduct_head_box_btnDelete)
        
        misconduct_head_box_widget = QWidget()
        misconduct_head_box_widget.setMaximumHeight(50)
        misconduct_head_box_widget.setContentsMargins(0, 0, 0, 0)
        misconduct_head_box_widget.setLayout(misconduct_head_box)
        
        misconduct_text_box = QHBoxLayout()
        self.docMisconduct = QTextEdit()
        self.docMisconduct.setText('aa')
        
        rollz = self.reloadStudentMisconduct()
        menu = QMenu()
        for a in rollz:
            menu.addAction('No.'+str(a), lambda x = a :self.lunchMisconduct(x))
        
        menu1 = QMenu()
        for a in rollz:
            menu1.addAction('No.'+str(a), lambda x = a :self.lunchMisconduct(x))
        #tb = QTextTable()
        
        misconduct_head_box_btnEdit.setMenu(menu)
        misconduct_head_box_btnDelete.setMenu(menu)
        
        misconduct_text_box.addWidget(self.docMisconduct)
        misconduct_text_box_widget = QWidget()
        misconduct_text_box_widget.setContentsMargins(0, 0, 0, 0)
        #class_text_box_widget.setStyleSheet('background-color: #022140')
        misconduct_text_box_widget.setLayout(misconduct_text_box)
        
        misconduct_main_box = QVBoxLayout()
        misconduct_main_box.addWidget(misconduct_head_box_widget)
        misconduct_main_box.addWidget(misconduct_text_box_widget)
        self.tab7.setLayout(misconduct_main_box)
        
        #mail
        mailtabz = QTabWidget()
        mailtabz.setTabPosition(QTabWidget.West)
        mailtab1 = QWidget() #sends
        mailtab2 = QWidget() #outbox
        mailtab3 = QWidget() #pending
        
        send_mail_main_Lbl = QLabel('Send Email')
        send_mail_Lbl = QLabel('Email Address(es): ')
        send_mail_email_Lbl = QLabel('Email Adress(es): ')
        send_mail_title_Lbl = QLabel('Mail Title')
        self.send_mail_title_Data = QLineEdit()
        self.send_mail_title_Data.setPlaceholderText('Title')
        self.send_mail_attach_Lbl = QLineEdit()
        self.send_mail_attach_Btn = QPushButton()
        self.send_mail_attach_Btn.setText('Attache File')

        self.send_mail_close_Btn = QPushButton()
        self.send_mail_close_Btn.setText('Close')
        self.send_mail_send_Btn = QPushButton()
        self.send_mail_send_Btn.setText('Send Mail')
        self.send_mail_send_Btn.clicked.connect(lambda:self.sendMail())
        
        send_h1_box = QHBoxLayout()
        send_h1_box.addWidget(send_mail_main_Lbl)
        
        send_h2_box = QHBoxLayout()
        send_h2_box.addWidget(send_mail_Lbl)
        send_h2_box.addWidget(send_mail_email_Lbl)
        
        send_h3_box = QHBoxLayout()
        send_h3_box.addWidget(send_mail_title_Lbl)
        send_h3_box.addWidget(self.send_mail_title_Data)
        
        send_h4_box = QHBoxLayout()
        send_h4_box.addWidget(self.send_mail_attach_Btn)
        send_h4_box.addWidget(self.send_mail_attach_Lbl)
        self.send_h5x_box = QVBoxLayout()
        #self.send_h5x_widget = QWidget()
        self.initUIMain()
        self.send_h5x_box.addWidget(self.menubar)
        self.send_h5x_box.addWidget(self.toolbar)
        self.send_h5x_box.addWidget(self.formatbar)
        self.send_h5x_box.addWidget(self.text)
        #self.send_h5x_box.addLayout(self.layout)
        
        send_h5_box = QHBoxLayout()
        send_h5_box.addWidget(self.send_mail_close_Btn)
        send_h5_box.addStretch()
        send_h5_box.addWidget(self.send_mail_send_Btn)
        
        send_v_box = QVBoxLayout()
        send_v_box.addLayout(send_h1_box)
        send_v_box.addLayout(send_h2_box)
        send_v_box.addLayout(send_h3_box)
        send_v_box.addLayout(send_h4_box)
        send_v_box.addLayout(self.send_h5x_box)
        send_v_box.addLayout(send_h5_box)
        mailtab1.setLayout(send_v_box)
        
        self.splitter = QSplitter(Qt.Horizontal)
        self.splitter.setContentsMargins(0, 0, 0, 0)
        
        self.outbox_mailtitle_tree = QTreeWidget()
        self.outbox_mailtitle_tree.setMaximumWidth(200)
        self.outbox_mailtitle_tree.setWordWrap(True)
        self.outbox_mailtitle_tree.setHeaderLabel("Mail Titles")
        self.m_arr = {}
        #parent = QTreeWidgetItem(self.outbox_mailtitle_tree)
        #parent.setText(0, "Subjects")
        #parent.setFlags(parent.flags() | Qt.ItemIsTristate | Qt.ItemIsUserCheckable)
        self.reloadStudentMail()
                
        self.outbox_mailmessage = QTextEdit()
        self.outbox_mailheader = QLabel('')
        self.outbox_maildate = QLabel('23 May, 2016')
        self.outbox_btn_delete = QPushButton()
        self.outbox_btn_delete.setText('Delete')
        self.outbox_btn_resend = QPushButton()
        self.outbox_btn_resend.setText('Resend')
        outbox_btn = QHBoxLayout()
        outbox_btn.addStretch()
        outbox_btn.addWidget(self.outbox_btn_delete)
        outbox_btn.addWidget(self.outbox_btn_resend)
        outbox_v_box = QVBoxLayout()
        outbox_v_box.addWidget(self.outbox_mailheader)
        outbox_v_box.addWidget(self.outbox_maildate)
        outbox_v_box.addWidget(self.outbox_mailmessage)
        outbox_v_box.addLayout(outbox_btn)
        outbox_v_widget = QWidget()
        outbox_v_widget.setLayout(outbox_v_box)
        
        
        self.splitter.addWidget(self.outbox_mailtitle_tree)
        self.splitter.addWidget(outbox_v_widget)
        layout= QVBoxLayout()
        layout.addWidget(self.splitter)
        layout.setContentsMargins(0, 0, 0, 0)
        mailtab2.setLayout(layout)
        
        mailtabz.addTab(mailtab1, 'Send Email')
        mailtabz.addTab(mailtab2, 'Outbox')
        mailtabz.addTab(mailtab3, 'Pending')
        
        mail_main_box = QVBoxLayout()
        mail_main_box.addWidget(mailtabz)
        self.tab8.setLayout(mail_main_box)

        self.tabz.addTab(self.tab1, 'Bio-Data')
        self.tabz.addTab(self.tab2, 'Contact Details')
        self.tabz.addTab(self.tab3, "Passports")
        self.tabz.addTab(self.tab4, "Class/Subject")
        self.tabz.addTab(self.tab5, "Medical Data")
        self.tabz.addTab(self.tab6, "Commendations/Awards")
        self.tabz.addTab(self.tab7, "Misconduct")
        self.tabz.addTab(self.tab8, "Email")
        self.tabz.addTab(self.tab9, "SMS")
        
        fullname = str(data['schno'])+" "+ str(data['surname']+" "+data['firstname']+" "+data['othername']).title()
        fullnameLbl = QLabel(fullname)
        fullnameLbl.setMaximumHeight(50)
        fullnameLbl.setFont(QFont("Candara", 14, QFont.Bold))
        
        grid = QGridLayout()
        grid.addWidget(fullnameLbl, 0, 0)
        grid.addWidget(self.tabz, 1, 0)
        
        self.setLayout(grid)
        self.setWindowTitle("Add Student Data")
            
        
    def pullData(self, db, sid, arr):
         g = Db()
         data = g.selectn(db, '', sid, arr)
         return data
        
    def getSave(self, a):
        sid = self.sid
        fname = self.mainLink
        im1 = fname
        file1 = 'pic_thumb/'
        file2 = 'pic_main/'
        lnk = "pic_"+str(sid)+'_'+str(a)+".png"
      
        im1.thumbnail((128, 128))
        im1.save(file1 + lnk, "PNG" )
        
        im1.thumbnail((700, 700))
        im1.save(file2 + lnk, "PNG")
        arr = {}
        if a == 1:
             arr['pix1'] = lnk
             arr['pix'] = 1
        elif a == 2:
             arr['pix2'] = lnk
             arr['pix'] = 2
        elif a == 3:
             arr['pix3'] = lnk
             arr['pix'] = 3
             
        g = Db()
        g.update('students', arr, {'id':sid})
        self.setCurrentPix()   
        
        
    def changeStates(self, a):
        sid = self.sid
        arr = {}
        if a == 1:
             arr['pix'] = 1
             self.picRad1.setChecked(True)
        elif a == 2:
             arr['pix'] = 2
             self.picRad2.setChecked(True)
        elif a == 3:
             arr['pix'] = 3
             self.picRad3.setChecked(True)
        else:
            self.picRad1.setChecked(True)
             
        g = Db()
        g.update('students', arr, {'id':sid})
        self.setCurrentPix()   
         
    def getFilez(self, a):
         fname = QFileDialog.getOpenFileName(self, 'Open', 'c:\\')
         image1 = Image.open(fname)
         imageQ1 = ImageQt(image1)
         imagep1 = QPixmap(QPixmap.fromImage(QImage(imageQ1).scaled(130, 130, Qt.IgnoreAspectRatio)))
         self.pic1.resize(150, 150)
         
         if a == 1:
             self.pic1.setPixmap(imagep1)
         elif a == 2:
             self.pic2.setPixmap(imagep1)
         elif a == 3:
             self.pic3.setPixmap(imagep1)
         
         self.mainLink = image1
        
    
    def setCurrentPix(self):
        file1 = "pic_main/"
         
        g = Db()
        f = g.selectn('students', '', 1, {'id':self.sid})
        
        num = int(f['pix'])
        img = ''
        if num == 1:
             img = str(file1)+str(f['pix1'])
             self.picRad1.setChecked(True)
        elif num == 2:
             img = str(file1)+str(f['pix2'])
             self.picRad2.setChecked(True)
        elif num == 3:
             img = str(file1)+str(f['pix3'])
             self.picRad3.setChecked(True)
             
        image1 = Image.open(img)
        imageQ1 = ImageQt(image1)
        imagep1 = QPixmap(QPixmap.fromImage(QImage(imageQ1).scaled(250, 300, Qt.IgnoreAspectRatio)))
        self.pic1.resize(250, 300)
        self.picMain.setPixmap(imagep1)
        
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
     
        g = Db()
        if((arr['surname']) and (arr['firstname']) and (arr['schno'])):
            g.update('students', arr, {'id':self.a})
      
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
    
    def pullStudentClass(self):
        terms = self.myterms
        all_terms = []
        
        for a in terms:
            db ='student_class'+str(a)
            
    def pullStudentMail(self):
        terms = self.myterms
        all_terms = {}
        g = Db()
        for a in terms:
            db ='school_mails'+str(terms[a][2])
            sels = g.selectn(db, '', '', {'studentID':self.sid})
            if sels and len(sels) > 0:
                for sel in sels:
                    tid = str(terms[a][2])+'_'+str(sel['id'])
                    arr = {}
                    arr['datepaid'] = sel['datepaid']
                    arr['subject'] = sel['subject']
                    arr['message'] = sel['message']
                    arr['session'] = terms[a][2]
                    arr['id'] = sel['id']
                    all_terms[tid] = arr
        return all_terms
    
    def pullStudentMedical(self):
        terms = self.myterms
        all_terms = {}
        g = Db()
        for a in terms:
            db ='school_medicals'+str(terms[a][2])
            sels = g.selectn(db, '', '', {'studentID':self.sid})
            if sels and len(sels) > 0:
                for sel in sels:
                    tid = str(terms[a][2])+'_'+str(sel['id'])
                    arr = {}
                    arr['datepaid'] = sel['datepaid']
                    arr['ailment'] = sel['ailment']
                    arr['treatment'] = sel['treatment']
                    arr['session'] = terms[a][2]
                    arr['id'] = sel['id']
                    all_terms[tid] = arr
        return all_terms
    
    def pullStudentConduct(self):
        terms = self.myterms
        all_terms = {}
        g = Db()
        for a in terms:
            db ='school_conducts'+str(terms[a][2])
            sels = g.selectn(db, '', '', {'studentID':self.sid, 'state':0})
            if sels and len(sels) > 0:
                for sel in sels:
                    tid = str(terms[a][2])+'_'+str(sel['id'])
                    arr = {}
                    arr['datepaid'] = sel['datepaid']
                    arr['action'] = sel['action']
                    arr['reaction'] = sel['reaction']
                    arr['staff'] = sel['staffname']
                    arr['session'] = terms[a][2]
                    arr['id'] = sel['id']
                    all_terms[tid] = arr
        return all_terms
    
    def pullStudentMisconduct(self):
        terms = self.myterms
        all_terms = {}
        g = Db()
        for a in terms:
            db ='school_conducts'+str(terms[a][2])
            sels = g.selectn(db, '', '', {'studentID':self.sid, 'state':1})
            if sels and len(sels) > 0:
                for sel in sels:
                    tid = str(terms[a][2])+'_'+str(sel['id'])
                    arr = {}
                    arr['datepaid'] = sel['datepaid']
                    arr['action'] = sel['action']
                    arr['reaction'] = sel['reaction']
                    arr['staff'] = sel['staffname']
                    arr['session'] = terms[a][2]
                    arr['id'] = sel['id']
                    all_terms[tid] = arr
        return all_terms
    
    def reloadStudentMail(self):
        self.outbox_mailtitle_tree.clear()
        filz = self.pullStudentMail()
        self.mail_arr = {}
        self.sub_arr = {}
        ko = 1
        if filz and len(filz) > 0:
            for fi in sorted(filz.keys(), reverse = True):
                dt = datetime.utcfromtimestamp(int(float(filz[fi]['datepaid']))).strftime('%d %b %Y')
                #html = '<div>'+filz[fi]['subject'].upper() +'<br> '+ dt+'</div>' 
                html = filz[fi]['subject'].upper() + dt
                self.mail_arr[ko] = fi
                child = QTreeWidgetItem(self.outbox_mailtitle_tree)
                child.setFlags(child.flags() | Qt.ItemIsUserCheckable)
                child.setText(0, str(html).upper())
                child.setIcon(0, QIcon("img/email.png"))
                self.sub_arr[filz[fi]['id']] = child
                self.mail_arr[ko] = fi
                ko += 1
            
        return self.mail_arr
    
    def reloadStudentMedical(self):
        self.docMedical.clear()
        filz = self.pullStudentMedical()
        doc = QTextDocument()
        self.docMedical.setDocument(doc)
        cursor= QTextCursor(doc)
        self.medical_arr = {}
        k = 1
        for fi in sorted(filz.keys(), reverse = True):
            dt = datetime.utcfromtimestamp(int(float(filz[fi]['datepaid']))).strftime('%d %a %B %Y')
            self.medical_arr[k] = fi
            html = '<div width="100%"><tr><td><b style="font-family:candara; margin-right:4px;font-size:13px">'+ str(k) +'. ) '+ dt + '</b></td><td><div style="margin:8px; margin-top:10px">'+ filz[fi]['ailment'].upper() +'</div></td><tr> <td></td><td><div style="margin:8px"><i>'+ filz[fi]['treatment']+'</span></i></div><br></td></tr></div>'
            cursor.insertHtml(html)
            k += 1
            
        return self.medical_arr
            
    def reloadStudentConduct(self):
        self.docConduct.clear()
        filz = self.pullStudentConduct()
        doc = QTextDocument()
        self.docConduct.setDocument(doc)
        cursor= QTextCursor(doc)
        self.conduct_arr = {}
        k = 1
        for fi in sorted(filz.keys(), reverse = True):
            dt = datetime.utcfromtimestamp(int(float(filz[fi]['datepaid']))).strftime('%d %a %B %Y')
            self.conduct_arr[k] = fi
            html = '<div width="100%"><tr><td><b style="font-family:candara; margin-right:4px;font-size:13px">'+ str(k) +'. ) '+ dt + '</b></td><td><div style="margin:8px; margin-top:10px; color:green">'+ filz[fi]['action'].upper() +'</div></td></tr><tr> <td></td><td><div style="margin:8px; display:block"><i>'+ filz[fi]['reaction']+'</span></i></div></td></tr><tr><td></td><td><div style="margin:4px; display:block"><b> From: '+ filz[fi]['staff']+'</b></div></td></tr></div>'
            cursor.insertHtml(html)
            k += 1
            
        return self.conduct_arr
    
    def reloadStudentMisconduct(self):
        self.docMisconduct.clear()
        filz = self.pullStudentMisconduct()
        doc = QTextDocument()
        self.docMisconduct.setDocument(doc)
        cursor= QTextCursor(doc)
        self.misconduct_arr = {}
        k = 1
        for fi in sorted(filz.keys(), reverse = True):
            dt = datetime.utcfromtimestamp(int(float(filz[fi]['datepaid']))).strftime('%d %a %B %Y')
            self.misconduct_arr[k] = fi
            html = '<div width="100%"><tr><td><b style="font-family:candara; margin-right:4px;font-size:13px">'+ str(k) +'. ) '+ dt + '</b></td><td><div style="margin:8px; margin-top:10px; color:red">'+ filz[fi]['action'].upper() +'</div></td></tr><tr> <td></td><td><div style="margin:8px"><i>'+ filz[fi]['reaction']+'</span></i></div><br></td><td><div style="margin:4px"><b> From:'+ filz[fi]['staff']+'</span></b></div><br></td></</tr></div>'
            cursor.insertHtml(html)
            k += 1
            
        return self.misconduct_arr
            
    def pullStudents(self, a):
        self.a = a
        cn = Db()
        students = cn.selectn('students', '' , 1, {'id':self.a})
        return students
    
    def lunchClass(self):
        post = FormClassSubject(self.sid, self.term)
        post.show()
        if post.exec_() == QDialog.Accepted:
               rtt = post.getValue()
        else:
            rtt = ''
        return rtt
    
    
    def lunchMedical(self, a = None):
        if a and a > 0:
            a1 = self.medical_arr[a]
            post = FormStudentMedical(self.sid, self.term, a1)
        else:
            post = FormStudentMedical(self.sid, self.term)
        post.show()
        if post.exec_() == QDialog.Accepted:
               rtt = post.getValue()
        else:
            rtt = ''
            
        self.reloadStudentMedical()
        return rtt
    
    def lunchConduct(self, a = None):
        if a and a > 0:
            a1 = self.conduct_arr[a]
            post = FormStudentConduct(self.sid, self.term, a1)
        else:
            post = FormStudentConduct(self.sid, self.term)
        post.show()
        if post.exec_() == QDialog.Accepted:
               rtt = post.getValue()
        else:
            rtt = ''
            
        self.reloadStudentConduct()
        return rtt
    
    def lunchMisconduct(self, a = None):
        if a and a > 0:
            a1 = self.misconduct_arr[a]
            post = FormStudentMisconduct(self.sid, self.term, a1)
        else:
            post = FormStudentMisconduct(self.sid, self.term)
        post.show()
        if post.exec_() == QDialog.Accepted:
               rtt = post.getValue()
        else:
            rtt = ''
        self.reloadStudentMisconduct()
        return rtt
   
    def sendMail(self):
        subject = self.send_mail_title_Data.text()
        email = 'doyinspc2@gmail.com'  
        message = self.text.toPlainText()
        dates = datetime.now()
        _date = time.mktime(dates.timetuple())
        db = 'school_mails'+str(self.sessionID)
        g = Db()
        c = ''
        e = g.insert(db, {'subject': subject, 'message':message, 'studentID':self.sid, 'datepaid':_date, 'active':0 })
        if e > 0:
            c = g.sendMail(email, subject, message)
            
        print(c)
    
    def initToolbar(self):
      self.newAction = QAction(QIcon("icons/new.png"),"New",self)
      self.newAction.setStatusTip("Create a new document from scratch.")
      self.newAction.setShortcut("Ctrl+N")
      self.newAction.triggered.connect(self.open)
     
      self.openAction = QAction(QIcon("icons/open.png"),"Open file",self)
      self.openAction.setStatusTip("Open existing document")
      self.openAction.setShortcut("Ctrl+O")
      self.openAction.triggered.connect(self.open)
     
      self.saveAction = QAction(QIcon("icons/save.png"),"Save",self)
      self.saveAction.setStatusTip("Save document")
      self.saveAction.setShortcut("Ctrl+S")
      self.saveAction.triggered.connect(self.save)
      
      self.printAction = QAction(QIcon("icons/print.png"),"Print document",self)
      self.printAction.setStatusTip("Print document")
      self.printAction.setShortcut("Ctrl+P")
      self.printAction.triggered.connect(self.printc)
     
      self.previewAction = QAction(QIcon("icons/preview.png"),"Page view",self)
      self.previewAction.setStatusTip("Preview page before printing")
      self.previewAction.setShortcut("Ctrl+Shift+P")
      self.previewAction.triggered.connect(self.preview)
      
      self.cutAction = QAction(QIcon("icons/cut.png"),"Cut to clipboard",self)
      self.cutAction.setStatusTip("Delete and copy text to clipboard")
      self.cutAction.setShortcut("Ctrl+X")
      self.cutAction.triggered.connect(self.text.cut)
         
      self.copyAction = QAction(QIcon("icons/copy.png"),"Copy to clipboard",self)
      self.copyAction.setStatusTip("Copy text to clipboard")
      self.copyAction.setShortcut("Ctrl+C")
      self.copyAction.triggered.connect(self.text.copy)
         
      self.pasteAction = QAction(QIcon("icons/paste.png"),"Paste from clipboard",self)
      self.pasteAction.setStatusTip("Paste text from clipboard")
      self.pasteAction.setShortcut("Ctrl+V")
      self.pasteAction.triggered.connect(self.text.paste)
         
      self.undoAction = QAction(QIcon("icons/undo.png"),"Undo last action",self)
      self.undoAction.setStatusTip("Undo last action")
      self.undoAction.setShortcut("Ctrl+Z")
      self.undoAction.triggered.connect(self.text.undo)
         
      self.redoAction = QAction(QIcon("icons/redo.png"),"Redo last undone thing",self)
      self.redoAction.setStatusTip("Redo last undone thing")
      self.redoAction.setShortcut("Ctrl+Y")
      self.redoAction.triggered.connect(self.text.redo)
      
      bulletAction = QAction(QIcon("icons/bullet.png"),"Insert bullet List",self)
      bulletAction.setStatusTip("Insert bullet list")
      bulletAction.setShortcut("Ctrl+Shift+B")
      bulletAction.triggered.connect(self.bulletList)
         
      numberedAction = QAction(QIcon("icons/number.png"),"Insert numbered List",self)
      numberedAction.setStatusTip("Insert numbered list")
      numberedAction.setShortcut("Ctrl+Shift+L")
      numberedAction.triggered.connect(self.numberList)
      # Toggling actions for the various bars
      self.toolbarAction = QAction("Toggle Toolbar",self)
      self.toolbarAction.triggered.connect(self.toggleToolbar)
     
      self.formatbarAction = QAction("Toggle Formatbar",self)
      self.formatbarAction.triggered.connect(self.toggleFormatbar)
     
      self.statusbarAction = QAction("Toggle Statusbar",self)
      self.statusbarAction.triggered.connect(self.toggleStatusbar)
      
      self.findAction = QAction(QIcon("icons/find.png"),"Find and replace",self)
      self.findAction.setStatusTip("Find and replace words in your document")
      self.findAction.setShortcut("Ctrl+F")
      self.findAction.triggered.connect(find.Find(self).show)
         
      self.toolbar = QToolBar("Options")
      self.toolbar.addAction(self.newAction)
      self.toolbar.addAction(self.openAction)
      self.toolbar.addAction(self.saveAction)
      self.toolbar.addSeparator()
      self.toolbar.addAction(self.printAction)
      self.toolbar.addAction(self.previewAction)
      self.toolbar.addSeparator()
      self.toolbar.addAction(bulletAction)
      self.toolbar.addAction(numberedAction)
      # Makes the next toolbar appear underneath this one
      #self.toolbar.addToolBarBreak()
      self.toolbar.addAction(self.cutAction)
      self.toolbar.addAction(self.copyAction)
      self.toolbar.addAction(self.pasteAction)
      self.toolbar.addAction(self.undoAction)
      self.toolbar.addAction(self.redoAction)
      self.toolbar.addSeparator()
      self.toolbar.addAction(self.findAction)
      # Makes the next toolbar appear underneath this one
      #self.toolbar.addToolBarBreak()
     
    def initFormatbar(self):
        
        self.formatbar = QToolBar("Format")
        fontBox = QFontComboBox(self)
        fontBox.currentFontChanged.connect(self.fontFamily)
        fontSize = QComboBox(self)
        fontSize.setEditable(True)
        # Minimum number of chars displayed
        fontSize.setMinimumContentsLength(3)
        fontSize.activated.connect(self.fontSize)
        # Typical font sizes
        fontSizes = ['6','7','8','9','10','11','12','13','14',
                     '15','16','18','20','22','24','26','28',
                     '32','36','40','44','48','54','60','66',
                     '72','80','88','96']
         
        for i in fontSizes:
            fontSize.addItem(i)
         
        fontColor = QAction(QIcon("icons/font-color.png"),"Change font color",self)
        fontColor.triggered.connect(self.fontColor)
         
        backColor = QAction(QIcon("icons/highlight.png"),"Change background color",self)
        backColor.triggered.connect(self.highlight)
        
        boldAction = QAction(QIcon("icons/bold.png"),"Bold",self)
        boldAction.triggered.connect(self.bold)
         
        italicAction = QAction(QIcon("icons/italic.png"),"Italic",self)
        italicAction.triggered.connect(self.italic)
         
        underlAction = QAction(QIcon("icons/underline.png"),"Underline",self)
        underlAction.triggered.connect(self.underline)
         
        strikeAction = QAction(QIcon("icons/strike.png"),"Strike-out",self)
        strikeAction.triggered.connect(self.strike)
         
        superAction = QAction(QIcon("icons/superscript.png"),"Superscript",self)
        superAction.triggered.connect(self.superScript)
         
        subAction = QAction(QIcon("icons/subscript.png"),"Subscript",self)
        subAction.triggered.connect(self.subScript)
        
        alignLeft = QAction(QIcon("icons/align-left.png"),"Align left",self)
        alignLeft.triggered.connect(self.alignLeft)
         
        alignCenter = QAction(QIcon("icons/align-center.png"),"Align center",self)
        alignCenter.triggered.connect(self.alignCenter)
         
        alignRight = QAction(QIcon("icons/align-right.png"),"Align right",self)
        alignRight.triggered.connect(self.alignRight)
         
        alignJustify = QAction(QIcon("icons/align-justify.png"),"Align justify",self)
        alignJustify.triggered.connect(self.alignJustify)
        
        indentAction = QAction(QIcon("icons/indent.png"),"Indent Area",self)
        indentAction.setShortcut("Ctrl+Tab")
        indentAction.triggered.connect(self.indent)
         
        dedentAction = QAction(QIcon("icons/dedent.png"),"Dedent Area",self)
        dedentAction.setShortcut("Shift+Tab")
        dedentAction.triggered.connect(self.dedent)
         

        self.formatbar.addWidget(fontBox)
        self.formatbar.addWidget(fontSize)
        self.formatbar.addSeparator()
        self.formatbar.addAction(fontColor)
        self.formatbar.addAction(backColor)
        self.formatbar.addSeparator()
        self.formatbar.addAction(boldAction)
        self.formatbar.addAction(italicAction)
        self.formatbar.addAction(underlAction)
        self.formatbar.addAction(strikeAction)
        self.formatbar.addAction(superAction)
        self.formatbar.addAction(subAction)
        self.formatbar.addSeparator()
        self.formatbar.addAction(alignLeft)
        self.formatbar.addAction(alignCenter)
        self.formatbar.addAction(alignRight)
        self.formatbar.addAction(alignJustify)
        self.formatbar.addSeparator()
        self.formatbar.addAction(indentAction)
        self.formatbar.addAction(dedentAction)
        
      
     
    def initMenubar(self):
     
      self.menubar = QMenu()
      file = self.menubar.addMenu("File")
      edit = self.menubar.addMenu("Edit")
      view = self.menubar.addMenu("View")
      
      file.addAction(self.newAction)
      file.addAction(self.openAction)
      file.addAction(self.saveAction)
      file.addAction(self.printAction)
      file.addAction(self.previewAction)
      
      edit.addAction(self.undoAction)
      edit.addAction(self.redoAction)
      edit.addAction(self.cutAction)
      edit.addAction(self.copyAction)
      edit.addAction(self.pasteAction)
      edit.addAction(self.findAction)
      
      view.addAction(self.toolbarAction)
      view.addAction(self.formatbarAction)
      view.addAction(self.statusbarAction)
     
    def initUIMain(self):
        
        self.text = QTextEdit(self)
        self.text.setTabStopWidth(33)
        self.text.cursorPositionChanged.connect(self.cursorPosition)
        self.initToolbar()
        self.initFormatbar()
        self.initMenubar()
     
        # Button to search the document for something
        findButton = QPushButton("Find",self)
        #findButton.clicked.connect(self.find)
        
        # Button to replace the last finding
        replaceButton = QPushButton("Replace",self)
        #replaceButton.clicked.connect(self.replace)
        
        # Button to remove all findings
        allButton = QPushButton("Replace all",self)
        #allButton.clicked.connect(self.replaceAll)
        # Initialize a statusbar for the window
        # Normal mode - radio button
        self.normalRadio = QRadioButton("Normal",self)
        #self.normalRadio.toggled.connect(self.normalMode)
        
        # Regular Expression Mode - radio button
        self.regexRadio = QRadioButton("RegEx",self)
        #self.regexRadio.toggled.connect(self.regexMode)
        
        # The field into which to type the query
        self.findField = QTextEdit(self)
        self.findField.resize(250,50)
        
        # The field into which to type the text to replace the
        # queried text
        self.replaceField = QTextEdit(self)
        self.replaceField.resize(250,50)
        
        optionsLabel = QLabel("Options: ",self)
        # Case Sensitivity option
        self.caseSens = QCheckBox("Case sensitive",self)
        # Whole Words option
        self.wholeWords = QCheckBox("Whole words",self)
        # Layout the objects on the screen
        self.layout = QGridLayout()
        self.layout.addWidget(self.findField,1,0,1,4)
        self.layout.addWidget(self.normalRadio,2,2)
        self.layout.addWidget(self.regexRadio,2,3)
        self.layout.addWidget(findButton,2,0,1,2)
        
        self.layout.addWidget(self.replaceField,3,0,1,4)
        self.layout.addWidget(replaceButton,4,0,1,2)
        self.layout.addWidget(allButton,4,2,1,2)
        
        # Add some spacing
        spacer = QWidget(self)
        spacer.setFixedSize(0,10)
        
        self.layout.addWidget(spacer,5,0)
        self.layout.addWidget(optionsLabel,6,0)
        self.layout.addWidget(self.caseSens,6,1)
        self.layout.addWidget(self.wholeWords,6,2)
        
        self.statusbar = QStatusBar()
        #return self.text
    
    def new(self):
        #spawn = Main(self)
        #spawn.show()
        pass
     
    def open(self):
     
        # Get filename and show only .writer files
        self.filename = QFileDialog.getOpenFileName(self, 'Open File',".","(*.writer)")
     
        if self.filename:
            with open(self.filename,"rt") as file:
                self.text.setText(file.read())
     
    def save(self):
     
        # Only open dialog if there is no filename yet
        if not self.filename:
            self.filename = QFileDialog.getSaveFileName(self, 'Save File')
     
        # Append extension if not there yet
        if not self.filename.endswith(".writer"):
            self.filename += ".writer"
     
        # We just store the contents of the text file along with the
        # format in html, which Qt does in a very nice way for us
        with open(self.filename,"wt") as file:
            file.write(self.text.toHtml())

    def preview(self):
        # Open preview dialog
        preview = QPrintPreviewDialog()
        # If a print is requested, open print dialog
        preview.paintRequested.connect(lambda p: self.text.print_(p))
        preview.exec_()
     
    def printc(self):
        # Open printing dialog
        dialog = QPrintDialog()
        if dialog.exec_() == QDialog.Accepted:
            self.text.document().print_(dialog.printer())
            
    def bulletList(self):
        cursor = self.text.textCursor()
        # Insert bulleted list
        cursor.insertList(QTextListFormat.ListDisc)
     
    def numberList(self):
        cursor = self.text.textCursor()
        # Insert list with numbers
        cursor.insertList(QTextListFormat.ListDecimal)
        
    def cursorPosition(self): 
        cursor = self.text.textCursor()     
        # Mortals like 1-indexed things
        line = cursor.blockNumber() + 1
        col = cursor.columnNumber()
     
        self.statusbar.showMessage("Line: {} | Column: {}".format(line,col))
        
    def fontFamily(self,font):
        self.text.setCurrentFont(font)
     
    def fontSize(self, fontsize):
        self.text.setFontPointSize(int(fontsize))
     
    def fontColor(self):
        # Get a color from the text dialog
        color = QColorDialog.getColor()
        # Set it as the new text color
        self.text.setTextColor(color)
     
    def highlight(self):
        color = QColorDialog.getColor()
        self.text.setTextBackgroundColor(color)
        
    def bold(self):
 
        if self.text.fontWeight() == QFont.Bold:
            self.text.setFontWeight(QFont.Normal)
        else:
            self.text.setFontWeight(QFont.Bold)
     
    def italic(self):
     
        state = self.text.fontItalic()
     
        self.text.setFontItalic(not state)
     
    def underline(self):
     
        state = self.text.fontUnderline()
     
        self.text.setFontUnderline(not state)
     
    def strike(self):
     
        # Grab the text's format
        fmt = self.text.currentCharFormat()
     
        # Set the fontStrikeOut property to its opposite
        fmt.setFontStrikeOut(not fmt.fontStrikeOut())
     
        # And set the next char format
        self.text.setCurrentCharFormat(fmt)
     
    def superScript(self):
     
        # Grab the current format
        fmt = self.text.currentCharFormat()
     
        # And get the vertical alignment property
        align = fmt.verticalAlignment()
     
        # Toggle the state
        if align == QTextCharFormat.AlignNormal:
     
            fmt.setVerticalAlignment(QTextCharFormat.AlignSuperScript)
     
        else:
     
            fmt.setVerticalAlignment(QTextCharFormat.AlignNormal)
     
        # Set the new format
        self.text.setCurrentCharFormat(fmt)
     
    def subScript(self):
     
        # Grab the current format
        fmt = self.text.currentCharFormat()
     
        # And get the vertical alignment property
        align = fmt.verticalAlignment()
     
        # Toggle the state
        if align == QTextCharFormat.AlignNormal:
     
            fmt.setVerticalAlignment(QTextCharFormat.AlignSubScript)
     
        else:
     
            fmt.setVerticalAlignment(QTextCharFormat.AlignNormal)
     
        # Set the new format
        self.text.setCurrentCharFormat(fmt)
        
    def alignLeft(self):
        self.text.setAlignment(Qt.AlignLeft)
     
    def alignRight(self):
        self.text.setAlignment(Qt.AlignRight)
     
    def alignCenter(self):
        self.text.setAlignment(Qt.AlignCenter)
     
    def alignJustify(self):
        self.text.setAlignment(Qt.AlignJustify)
        
    def indent(self):
        # Grab the cursor
        cursor = self.text.textCursor()
     
        if cursor.hasSelection():
     
            # Store the current line/block number
            temp = cursor.blockNumber()
     
            # Move to the selection's last line
            cursor.setPosition(cursor.selectionEnd())
     
            # Calculate range of selection
            diff = cursor.blockNumber() - temp
     
            # Iterate over lines
            for n in range(diff + 1):
     
                # Move to start of each line
                cursor.movePosition(QTextCursor.StartOfLine)
     
                # Insert tabbing
                cursor.insertText("\t")
     
                # And move back up
                cursor.movePosition(QTextCursor.Up)
     
        # If there is no selection, just insert a tab
        else:
     
            cursor.insertText("\t")
     
    def dedent(self):
     
        cursor = self.text.textCursor()
     
        if cursor.hasSelection():
            # Store the current line/block number
            temp = cursor.blockNumber()
            # Move to the selection's last line
            cursor.setPosition(cursor.selectionEnd())
            # Calculate range of selection
            diff = cursor.blockNumber() - temp
     
            # Iterate over lines
            for n in range(diff + 1):
                self.handleDedent(cursor)
                # Move up
                cursor.movePosition(QTextCursor.Up)
     
        else:
            self.handleDedent(cursor)
     
     
    def handleDedent(self, cursor):
        cursor.movePosition(QTextCursor.StartOfLine)
        # Grab the current line
        line = cursor.block().text()
     
        # If the line starts with a tab character, delete it
        if line.startswith("\t"):
            # Delete next character
            cursor.deleteChar()
     
        # Otherwise, delete all spaces until a non-space character is met
        else:
            for char in line[:8]:
     
                if char != " ":
                    break
     
                cursor.deleteChar()
                
    def toggleToolbar(self):
         state = self.toolbar.isVisible()
          # Set the visibility to its inverse
         self.toolbar.setVisible(not state)
     
    def toggleFormatbar(self):
        state = self.formatbar.isVisible()
        # Set the visibility to its inverse
        self.formatbar.setVisible(not state)
     
    def toggleStatusbar(self):
        state = self.statusbar.isVisible()
        # Set the visibility to its inverse
        self.statusbar.setVisible(not state)