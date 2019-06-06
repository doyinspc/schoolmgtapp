# -*- coding: utf-8 -*-
"""
Created on Sat Nov 17 05:44:29 2018

@author: CHARLES
"""

from PyQt4.QtCore import SIGNAL, QDate, Qt, QSize
from PyQt4.QtGui import QAction, QScrollArea, QTableWidget, QTableWidgetItem,  QToolBar,  QMenuBar, QStatusBar, QTextListFormat, QTextCharFormat, QFontComboBox, QColorDialog, QPrintDialog, QPrintPreviewDialog, QMenu, QSplitter, QFrame, QIcon, QTreeWidgetItem, QTreeWidget, QWidget, QTextDocument, QTextCursor, QImage, QFileDialog, QFont, QPixmap, QTabWidget, QComboBox, QRadioButton, QDateEdit, QTextEdit, QPlainTextEdit, QCheckBox, QHBoxLayout, QGroupBox, QGridLayout, QDialog, QApplication, QPushButton, QLineEdit, QFormLayout, QLabel, QVBoxLayout, QSizePolicy
from connect import Db
from validate import Valid, Buttons, Settingz, Arrayz
from PIL import Image
from PIL.ImageQt import ImageQt
import os
from datetime import datetime
import time
import sip
from frmstudentclasssubject import FormClassSubject, FormStudentMedical, FormStudentConduct, FormStudentMisconduct

class StaffForm(QDialog):
    
    def __init__(self, parent=None):
        super(StaffForm, self).__init__(parent)
        stylesheet = Valid().background() + Valid().font()
        self.pagetitle = 'Add Staff'
        self.titleIcon = ''

        currentDate = QDate()
        
        self.empno = QLabel("Employment Number")
        self.empnoData = QLineEdit()
        self.empnoData.setObjectName("emp")
        self.empnoData.setPlaceholderText("00000000")
        
        self.title = QLabel("Title")
        self.titleData = QLineEdit()
        self.titleData.setObjectName("title")
        self.titleData.setPlaceholderText("Mr., Miss., Dr.")
        

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
        self.middlenameData.setPlaceholderText("Middlename")
        
        
        self.soo = QLabel("State/Region of Origin")
        self.sooData = QLineEdit()
        self.sooData.setObjectName("soo")
        self.sooData.setPlaceholderText("Lagos")
        
        
        self.lga = QLabel("LGA/District")
        self.lgaData = QLineEdit()
        self.lgaData.setObjectName("lga")
        self.lgaData.setPlaceholderText("Ikeja")
            
        self.nation = QLabel("Nationality")
        self.nationData = QLineEdit()
        self.nationData.setObjectName("nation")
        self.nationData.setPlaceholderText("Nigeria")
        
        self.phone1 = QLabel("Phone Number")
        self.phone1Data = QLineEdit()
        self.phone1Data.setObjectName("phone1")
        self.phone1Data.setPlaceholderText("XXXXXXXXXX")
            
        self.phone2 = QLabel("Alt. Phone Number")
        self.phone2Data = QLineEdit()
        self.phone2Data.setObjectName("phone2")
        self.phone2Data.setPlaceholderText("XXXXXXXXXX")
        
        self.email = QLabel("Email")
        self.emailData = QLineEdit()
        self.emailData.setObjectName("email")
        self.emailData.setPlaceholderText("..xxxxx@xxx.xx")
        
        self.addr = QLabel("House Address")
        self.addrData = QTextEdit()
        self.addrData.setObjectName("addr")
        
       
        self.dob = QLabel("Date of Birth")
        self.dobData = QDateEdit()
        self.dobData.setObjectName("dob")
        self.dobData.setCalendarPopup(True)
        self.dobData.setDate(currentDate.currentDate())
        
        self.admit = QLabel("Date Employed")
        self.admitData = QDateEdit()
        self.admitData.setObjectName("admit")
        self.admitData.setCalendarPopup(True)
        self.admitData.setDate(currentDate.currentDate())
        
        
        relations = Arrayz().arrayz(1)
        #first guardian details
        self.g1name = QLabel("Fullname and Title")
        self.g1Data = QLineEdit()
        self.g1Data.setObjectName("g1name")
        self.g1Data.setPlaceholderText("Mr. Surname Lastname")
        
        self.g1rel = QLabel('Relationship')
        self.g1relData = QComboBox()
        for d in relations:
            self.g1relData.addItem(str(relations[d]).upper(), d)
        
        self.g1p1 = QLabel("Phone")
        self.g1p1Data = QLineEdit()
        self.g1p1Data.setObjectName("g1p1")
        self.g1p1Data.setPlaceholderText("XXXXXXXXXX")
        
        self.g1p2 = QLabel("Alt. Phone")
        self.g1p2Data = QLineEdit()
        self.g1p2Data.setObjectName("g1p2")
        self.g1p2Data.setPlaceholderText("XXXXXXXXXX")
        
        
        self.g1email = QLabel("Email")
        self.g1emailData = QLineEdit()
        self.g1emailData.setObjectName("g1email")
        self.g1emailData.setPlaceholderText("..xxxxx@xxx.xx")
            
        
        self.g1addr = QLabel("Address")
        self.g1addrData = QLineEdit()
        self.g1addrData.setObjectName("g1add")
        
         #second guardian details
        self.g2name = QLabel("Alt. Next of Kin")
        self.g2Data = QLineEdit()
        self.g2Data.setObjectName("g2name")
        self.g2Data.setPlaceholderText("Title. Surname Lastname")
            
        self.g2rel = QLabel('Relationship')
        self.g2relData = QComboBox()
        for d in relations:
            self.g2relData.addItem(str(relations[d]).upper(), d)                
        
        self.g2p1 = QLabel("Phone")
        self.g2p1Data = QLineEdit()
        self.g2p1Data.setObjectName("g2p1")
        self.g2p1Data.setPlaceholderText("XXXXXXXXXXX")
            
        
        self.g2p2 = QLabel("Alt. Phone")
        self.g2p2Data = QLineEdit()
        self.g2p2Data.setObjectName("g2p2")
        self.g2p2Data.setPlaceholderText("XXXXXXXXXXX")
            
        
        self.g2email = QLabel("Email")
        self.g2emailData = QLineEdit()
        self.g2emailData.setObjectName("g2email")
        self.g2emailData.setPlaceholderText("..xxxxx@xxx.xx")
            
        
        self.g2addr = QLabel("Address")
        self.g2addrData = QLineEdit()
        self.g2addrData.setObjectName("g2addr")
        
        
        self.bank = QLabel("Bank Account")
        self.bankData = QComboBox()
        self.pullCombo(self.bankData, 20)
        self.bankData.setObjectName("bank")
        
            
        self.account = QLabel("Account Number")
        self.accountData = QLineEdit()
        self.accountData.setObjectName("account")
        self.accountData.setPlaceholderText("XXXXXXXXXXX")
        
        
        self.sort = QLabel("Sort Code")
        self.sortData = QLineEdit()
        self.sortData.setObjectName("sort")
        self.sortData.setPlaceholderText("XXXXXXXXXX")
        
        
        self.pen = QLabel("Pension Manager")
        self.penData = QComboBox()
        self.pullCombo(self.penData, 28)
        self.penData.setObjectName("pen")
        
        
        self.pencode = QLabel("Pension Code")
        self.pencodeData = QLineEdit()
        self.pencodeData.setObjectName("pencode")
        self.pencodeData.setPlaceholderText("XXXXXXXXXX")
           
           
        self.health = QLabel("Health Insurance Manager")
        self.healthData = QComboBox()
        self.pullCombo(self.healthData, 2)
        self.healthData.setObjectName("health")
         
        
        self.healthcode = QLabel("Health Insurance Code")
        self.healthcodeData = QLineEdit()
        self.healthcodeData.setObjectName("healthcode")
        self.healthcodeData.setPlaceholderText("XXXXXXXXXX")
        
        
        self.socialcode = QLabel("Social Insurance Code")
        self.socialcodeData = QLineEdit()
        self.socialcodeData.setObjectName("socialcode")
        self.socialcodeData.setPlaceholderText("XXXXXXXXXX")
        
        
        self.tin = QLabel("T.I.N.")
        self.tinData = QLineEdit()
        self.tinData.setObjectName("tin")
        self.tinData.setPlaceholderText("XXXXXXXXXX")
        
        
        self.nin = QLabel("N.I.N")
        self.ninData = QLineEdit()
        self.ninData.setObjectName("nin")
        self.ninData.setPlaceholderText("XXXXXXXXXX")
            
       
        users = Arrayz().arrayz(2)
        self.user = QLabel('Permission')
        self.userData = QComboBox()
        for d in users:
            self.userData.addItem(str(users[d]).upper(), d)
        
                
        usersaccess = Arrayz().arrayz(3)
        self.access = QLabel('Access Level')
        self.accessData = QComboBox()
        for d in usersaccess:
            self.accessData.addItem(str(usersaccess[d]).upper(), d)

        
        self.userspassword = QLabel("Password")
        self.userspasswordData = QLineEdit()
        self.userspasswordData.setObjectName("password")
        self.userspasswordData.setPlaceholderText("XXXXXXXXXX")
            
            
        reasons = Arrayz().arrayz(4)
        self.reason = QLabel('Reason for leaving')
        self.reasonData = QComboBox()
        for d in reasons:
            self.reasonData.addItem(str(reasons[d]).upper(), d)
        
                
        self.dol = QLabel("Date of Leaving")
        self.dolData = QDateEdit()
        self.dolData.setObjectName("dol")
        self.dolData.setCalendarPopup(True)
        self.dolData.setDate(currentDate.currentDate())
        
        
        self.dolinfo = QLabel("Details")
        self.dolinfoData = QTextEdit()
        self.dolinfoData.setObjectName("dolinfo")
            
        
        gender = Arrayz().arrayz(5)
        self.gender = QLabel('Gender')
        self.genderData = QComboBox()
        for d in gender:
            self.genderData.addItem(str(gender[d]).upper(), d)
   
                
        marital = Arrayz().arrayz(6)
        self.marital = QLabel('Marital Status')
        self.maritalData = QComboBox()
        for d in marital:
            self.maritalData.addItem(str(marital[d]).upper(), d)
    
                
        religion = Arrayz().arrayz(7)
        self.religion = QLabel('Religion')
        self.religionData = QComboBox()
        for d in religion:
            self.religionData.addItem(str(religion[d]).upper(), d)

                
        self.noc = QLabel("No of Children")
        self.nocData = QLineEdit()
        self.nocData.setObjectName("noc")
        vals1 = Valid().fullNum()
        self.nocData.setValidator(vals1)

                 
        self.department = QLabel('Department')
        self.departmentData = QComboBox()
        self.pullCombo(self.departmentData, 27)
        
        
        self.unit = QLabel('Unit')
        self.unitData = QComboBox()
        self.pullCombo(self.unitData, 27)
        
        
        #photo
        self.pic1 = QLabel()
        image1 = Image.open('img/stdpic.png')
        imageQ1 = ImageQt(image1)
        imagep1 = QPixmap(QPixmap.fromImage(QImage(imageQ1).scaled(130, 130, Qt.IgnoreAspectRatio)))
        self.pic1.resize(130, 130)
        self.pic1.setPixmap(imagep1)
        self.pic1.setMaximumHeight(130)
        self.pic1.setMaximumWidth(130)
        self.picBtn1 = QPushButton('Select Image')
        self.picBtn1.setMaximumHeight(30)
        self.picBtn1.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.picLink = ''
        self.picBtn1.clicked.connect(lambda:self.getFilez(1, 1))
        
        self.pic2 = QLabel()
        image2 = Image.open('img/stdpic.png')
        imageQ2 = ImageQt(image2)
        imagep2 = QPixmap(QPixmap.fromImage(QImage(imageQ2).scaled(80, 80, Qt.IgnoreAspectRatio)))
        self.pic2.resize(80, 80)
        self.pic2.setPixmap(imagep2)
        self.pic2.setMaximumWidth(80)
        self.picBtn2 = QPushButton('Select')
        self.picBtn2.setMaximumHeight(30)
        self.picBtn2.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.g1picLink = ''
        self.picBtn2.clicked.connect(lambda:self.getFilez(2,1))
        
        self.pic3 = QLabel()
        image3 = Image.open('img/stdpic.png')
        imageQ3 = ImageQt(image3)
        imagep3 = QPixmap(QPixmap.fromImage(QImage(imageQ3).scaled(80, 80, Qt.IgnoreAspectRatio)))
        self.pic3.resize(80, 80)
        self.pic3.setPixmap(imagep3)
        self.pic3.setMaximumWidth(80)
        self.picBtn3 = QPushButton('Select')
        self.picBtn3.setMaximumHeight(30)
        self.picBtn3.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.g2picLink = ''
        self.picBtn3.clicked.connect(lambda:self.getFilez(3, 1))
        
        picGrid = QGridLayout()
        picGrid.addWidget(self.pic1, 0, 0)
        picGrid.addWidget(self.picBtn1, 1, 0)
        
        picGrid1 = QGridLayout()
        picGrid1.addWidget(self.pic2, 0, 0)
        picGrid1.addWidget(self.picBtn2, 1, 0)
        
        picGrid2 = QGridLayout()
        picGrid2.addWidget(self.pic3, 0, 0)
        picGrid2.addWidget(self.picBtn3, 1, 0)
        
        gridWidget = QWidget()
        gridWidget.setLayout(picGrid)
        gridWidget.setMaximumWidth(150)
        gridWidget.setMaximumHeight(150)
        gridWidget.setContentsMargins(0, 0, 0, 0)
        
        gridWidget1 = QWidget()
        gridWidget1.setLayout(picGrid1)
        gridWidget1.setMaximumWidth(80)
        gridWidget1.setMaximumHeight(100)
        gridWidget1.setContentsMargins(0, 0, 0, 0)
        
        gridWidget2 = QWidget()
        gridWidget2.setLayout(picGrid2)
        gridWidget2.setMaximumWidth(80)
        gridWidget2.setMaximumHeight(100)
        gridWidget2.setContentsMargins(0, 0, 0, 0)
        
        g_1 = QGridLayout()
        g_1.addWidget(self.title, 0, 0)
        g_1.addWidget(self.titleData, 0, 1)
        g_1.addWidget(self.surname,1,0)
        g_1.addWidget(self.surnameData,1,1)
        g_1.addWidget(self.firstname,2,0)
        g_1.addWidget(self.firstnameData,2,1)
        g_1.addWidget(self.middlename,3,0)
        g_1.addWidget(self.middlenameData,3,1)
        g_1.addWidget(self.dob,4,0)
        g_1.addWidget(self.dobData,4,1)
        g_1.addWidget(self.gender,5,0)
        g_1.addWidget(self.genderData,5,1)
        g_1.addWidget(self.marital,0,2)
        g_1.addWidget(self.maritalData,0,3)
        g_1.addWidget(self.noc,1,2)
        g_1.addWidget(self.nocData,1,3)
        g_1.addWidget(self.religion,2,2)
        g_1.addWidget(self.religionData,2,3)
        g_1.addWidget(self.lga,3,2)
        g_1.addWidget(self.lgaData,3,3)
        g_1.addWidget(self.soo,4,2)
        g_1.addWidget(self.sooData,4,3)
        g_1.addWidget(self.nation,5,2)
        g_1.addWidget(self.nationData,5,3)
        g_1.addWidget(self.phone1, 0, 4)
        g_1.addWidget(self.phone1Data,0,5)
        g_1.addWidget(self.phone2,1,4)
        g_1.addWidget(self.phone2Data,1,5)
        g_1.addWidget(self.email, 2, 4)
        g_1.addWidget(self.emailData,2,5)
        g_1.addWidget(self.addr, 3, 4, 1, 2)
        g_1.addWidget(self.addrData, 4, 4, 2, 2)
        
        Formlayout1 = QGridLayout()
        Formlayout1.addWidget(self.g1name, 0, 0)
        Formlayout1.addWidget(self.g1Data, 0, 1, 1, 3)
        Formlayout1.addWidget(self.g1rel, 1, 0)
        Formlayout1.addWidget(self.g1relData,1 , 1)
        Formlayout1.addWidget(self.g1email, 1, 2)
        Formlayout1.addWidget(self.g1emailData, 1, 3)
        Formlayout1.addWidget(self.g1p1,2,0)
        Formlayout1.addWidget(self.g1p1Data,2,1)
        Formlayout1.addWidget(self.g1p2,2,2)
        Formlayout1.addWidget(self.g1p2Data,2,3)
        Formlayout1.addWidget(self.g1addr, 3, 0)
        Formlayout1.addWidget(self.g1addrData, 3, 1, 1, 3)
        
        Formlayout2 = QGridLayout()
        Formlayout2.addWidget(self.g2name, 0, 0)
        Formlayout2.addWidget(self.g2Data, 0, 1, 1, 3)
        Formlayout2.addWidget(self.g2rel, 1, 0)
        Formlayout2.addWidget(self.g2relData,1 , 1)
        Formlayout2.addWidget(self.g2email, 1, 2)
        Formlayout2.addWidget(self.g2emailData, 1, 3)
        Formlayout2.addWidget(self.g2p1,2,0)
        Formlayout2.addWidget(self.g2p1Data,2,1)
        Formlayout2.addWidget(self.g2p2,2,2)
        Formlayout2.addWidget(self.g2p2Data,2,3)
        Formlayout2.addWidget(self.g2addr, 3, 0)
        Formlayout2.addWidget(self.g2addrData, 3, 1, 1, 3)
        
        Formlayout3 = QFormLayout()
        Formlayout3.addRow(self.bank, self.bankData)
        Formlayout3.addRow(self.account, self.accountData)
        Formlayout3.addRow(self.sort, self.sortData)
        Formlayout3.addRow(self.pen, self.penData)
        Formlayout3.addRow(self.pencode, self.pencodeData)
        Formlayout3.addRow(self.tin, self.tinData)
        Formlayout3.addRow(self.health, self.healthData)
        Formlayout3.addRow(self.healthcode, self.healthcodeData)
        Formlayout3.addRow(self.socialcode, self.socialcodeData)
        
        Formlayout4 = QFormLayout()
        Formlayout4.addRow(self.user, self.userData)
        Formlayout4.addRow(self.access, self.accessData)
        Formlayout4.addRow(self.userspassword, self.userspasswordData)
        Formlayout4.addRow(self.nin, self.ninData)
        
        Formlayout5 = QFormLayout()
        Formlayout5.addRow(self.reason, self.reasonData)
        Formlayout5.addRow(self.dol, self.dolData)
        Formlayout5_grid = QGridLayout()
        Formlayout5_grid.addWidget(self.dolinfo, 0, 0)
        Formlayout5_grid.addWidget(self.dolinfoData, 1, 0)
        reasonInt = QLabel('Only for staff leaving the institution')
        
        Formlayout6 = QFormLayout()
        Formlayout6.addRow(self.empno, self.empnoData)
        Formlayout6.addRow(self.admit, self.admitData)
        Formlayout6.addRow(self.department, self.departmentData)
        Formlayout6.addRow(self.unit, self.unitData)
        
        a_hbox1 = QVBoxLayout()
        a_hbox1.addLayout(Formlayout4)
        
        r_hbox1 = QVBoxLayout()
        r_hbox1.addWidget(reasonInt)
        r_hbox1.addStretch()
        r_hbox1.addLayout(Formlayout5)
        r_hbox1.addLayout(Formlayout5_grid)
        
        bio_box = QHBoxLayout()
        bio_box.addLayout(g_1)
        bio_box.addWidget(gridWidget)
      
        kin_grid1 = QGridLayout()
        kin_grid1.addLayout(Formlayout1, 0, 0)
        kin_grid1.addWidget(gridWidget1, 0, 1)
        kin_grid2 = QGridLayout()
        kin_grid2.addLayout(Formlayout2, 0 ,0)
        kin_grid2.addWidget(gridWidget2, 0, 1)
        
        self.pb = QPushButton()
        self.pb.setObjectName("Submit")
        self.pb.setText("Submit")
        
        self.pb1 = QPushButton()
        self.pb1.setObjectName("Cancel")
        self.pb1.setText("Cancel")
        
        grid_button = QGridLayout()
        grid_button.addWidget(self.pb,0,0)
        grid_button.addWidget(self.pb1,0,1)
        
        vbox1 = QVBoxLayout()
        vbox1.addLayout(Formlayout1)
        vbox1.addStretch()
        vbox1.addLayout(Formlayout2)
        
        groupBox1 = QGroupBox('Bio-Data')
        groupBox1.setLayout(bio_box)
        groupBox1.setMaximumHeight(180)
        groupBox1.setContentsMargins(1,1,1,1)
        
        groupBox2a = QGroupBox('Next of Kins')
        groupBox2a.setLayout(kin_grid1)
        groupBox2a.setMaximumHeight(140)
        groupBox2a.setContentsMargins(1,1,1,1)
        groupBox2b = QGroupBox(' Alternate Next of Kins')
        groupBox2b.setLayout(kin_grid2)
        groupBox2b.setMaximumHeight(140)
        groupBox2b.setContentsMargins(1,1,1,1)
        groupBox2_h = QHBoxLayout()
        groupBox2_h.addWidget(groupBox2a)
        groupBox2_h.addWidget(groupBox2b)
        
        groupBox3 = QGroupBox('Financial')
        groupBox3.setLayout(Formlayout3)
        groupBox3.setContentsMargins(1,1,1,1)
        
        groupBox4 = QGroupBox('Account')
        groupBox4.setLayout(a_hbox1)
        groupBox4.setMaximumWidth(250)
        
        groupBox5 = QGroupBox('Discontinuation of Service')
        groupBox5.setLayout(r_hbox1)
        groupBox5.setMaximumWidth(250)
        
        groupBox6 = QGroupBox('Administrative')
        groupBox6.setLayout(Formlayout6)
        groupBox6.setMaximumWidth(250)
        
        v_groupBox = QVBoxLayout()
        v_groupBox.addWidget(groupBox6)
        v_groupBox.addWidget(groupBox4)
        
        h_groupBox = QHBoxLayout()
        h_groupBox.addLayout(v_groupBox)
        h_groupBox.addWidget(groupBox3)
        h_groupBox.addWidget(groupBox5)
        
        main_h = QVBoxLayout()
        main_h.addWidget(groupBox1)
        main_h.addLayout(groupBox2_h)
        main_h.addLayout(h_groupBox)
        main_h.addLayout(grid_button)
        
        self.pb.clicked.connect(lambda:self.button1_click())
        self.pb1.clicked.connect(lambda:self.button1_click())
        
        self.setLayout(main_h)
        self.setStyleSheet(stylesheet)
        self.setWindowIcon(QIcon(self.titleIcon))
        self.setWindowTitle(self.pagetitle)
            
        
     
    def pullCombo(self, combo, sid):
        combo.clear()
        data = Valid().pullData('datas', 200000, {'pubID': sid})
        if data:
            for d  in data:
                combo.addItem(str(d['name']).upper(), d['id'])

        
    def getSave(self, sid, a):
        sid = sid
        file1 = 'pic_thumb/'
        file2 = 'pic_main/'
        
        arr = {}
        if a == 1:
             fname = self.picLink
             im1 = fname
             lnk = "staff_"+str(sid)+'_'+str(a)+".png"
             im1.thumbnail((128, 128))
             im1.save(file1 + lnk, "PNG" )
             im1.thumbnail((1000, 1000))
             im1.save(file2 + lnk, "PNG")
             arr['pix'] = lnk
        elif a == 2:
             fname = self.g1picLink
             im1 = fname
             lnk = "kin1_"+str(sid)+'_'+str(a)+".png"
             im1.thumbnail((128, 128))
             im1.save(file1 + lnk, "PNG" )
             im1.thumbnail((700, 700))
             im1.save(file2 + lnk, "PNG")
             arr['g1pix'] = lnk
        elif a == 3:
             fname = self.g2picLink
             im1 = fname
             lnk = "kin2_"+str(sid)+'_'+str(a)+".png"
             im1.thumbnail((128, 128))
             im1.save(file1 + lnk, "PNG" )
             im1.thumbnail((700, 700))
             im1.save(file2 + lnk, "PNG")
             arr['g2pix'] = lnk
             
        g = Db()
        g.update('staffs', arr, {'id':sid})
           
        
         
    def getFilez(self, a, pos):
         fname = QFileDialog.getOpenFileName(self, 'Open', 'c:\\')
         image1 = Image.open(fname)
         imageQ1 = ImageQt(image1)
         imagep1 = QPixmap(QPixmap.fromImage(QImage(imageQ1).scaled(130, 130, Qt.IgnoreAspectRatio)))
         self.pic1.resize(130, 130)
         
         if a == 1:
             self.pic1.setPixmap(imagep1)
             self.picLink =image1
         elif a == 2:
             self.pic2.setPixmap(imagep1)
             self.g1picLink = image1
         elif a == 3:
             self.pic3.setPixmap(imagep1)
             self.g2picLink = image1
             
      
        
    
    def button1_click(self):
        # shost is a QString object
        #biodata
        arr = {}
        arr['title'] = self.titleData.text()
        arr['surname'] = self.surnameData.text()
        arr['firstname'] = self.firstnameData.text()
        arr['othername'] = self.middlenameData.text()
        arr['soo'] = self.sooData.text()
        arr['lga'] = self.lgaData.text()
        arr['nation'] = self.nationData.text()
        arr['noc'] = self.nocData.text()
        arr['phone1'] = self.phone1Data.text()
        arr['phone2'] = self.phone2Data.text()
        arr['email'] = self.emailData.text()
        arr['addr'] = self.addrData.toPlainText().encode('utf-8').strip()
        arr['marital'] = self.maritalData.itemData(self.maritalData.currentIndex())
        arr['religion'] = self.religionData.itemData(self.religionData.currentIndex())
        dob = self.dobData.date().toPyDate()
        arr['dob'] = time.mktime(dob.timetuple())
        
        #admistrative
        arr['empno'] = self.empnoData.text()
        arr['department']  = self.departmentData.itemData(self.departmentData.currentIndex())
        arr['unit'] = self.unitData.itemData(self.unitData.currentIndex())
        admit = self.admitData.date().toPyDate()
        arr['admit'] = time.mktime(admit.timetuple())
        #account
        arr['user'] = self.userData.itemData(self.userData.currentIndex())
        arr['access'] = self.accessData.itemData(self.accessData.currentIndex())
        arr['userpassword'] = self.userspasswordData.text()
        dol = self.dolData.date().toPyDate()
        arr['dol'] = time.mktime(dol.timetuple())
        arr['reason'] = self.reasonData.itemData(self.reasonData.currentIndex())
        arr['dolinfo'] = self.dolinfoData.toPlainText().encode('utf-8').strip()
        #finance
        arr['bank'] = self.bankData.itemData(self.bankData.currentIndex())
        arr['account'] = self.accountData.text()
        arr['sort'] = self.sortData.text()
        arr['pension'] = self.penData.itemData(self.penData.currentIndex())
        arr['pensioncode'] = self.pencodeData.text()
        arr['tin'] = self.tinData.text()
        arr['nin'] = self.ninData.text()
        arr['health'] = self.healthData.itemData(self.healthData.currentIndex())
        arr['healthcode'] = self.healthcodeData.text()
        arr['socialcode'] = self.socialcodeData.text()
        #kin
        arr['g1'] = self.g1Data.text()
        arr['g1rel'] = self.g1relData.itemData(self.g1relData.currentIndex())
        arr['g1p1'] = self.g1p1Data.text()
        arr['g1p2'] = self.g1p2Data.text()
        arr['g1email'] = self.g1emailData.text()
        arr['g1addr'] = self.g1addrData.text()
        arr['g2'] = self.g2Data.text()
        arr['g2rel'] = self.g2relData.itemData(self.g2relData.currentIndex())
        arr['g2p1'] = self.g2p1Data.text()
        arr['g2p2'] = self.g2p2Data.text()
        arr['g2email'] = self.g2emailData.text()
        arr['g2addr'] = self.g2addrData.text()

        g = Db()
        chk = g.select('staffs','', 1, {'empno':arr['empno']}) 
        if chk and chk['id'] > 0:
            pass
        else:
            if((arr['surname']) and (arr['firstname']) and (arr['empno'])):
                h = g.insert('staffs', arr)
                if h > 0:
                    self.getSave(h, 1)
                    
                
                    try:
                        self.getSave(h, 2)
                    except:
                        pass
                    try:
                        self.getSave(h, 3)
                    except:
                        pass
      
        self.close()
        
        
class StaffFormEdit(QDialog):
    
    def __init__(self, sid,  parent=None):
        super(StaffFormEdit, self).__init__(parent)
        stylesheet = Valid().background() + Valid().font()
        self.pagetitle = 'Staff'
        self.titleIcon = ''
        self.sid = sid
        
        
        g = Db()
        data = g.selectn('staffs', '', 1, {'id':self.sid})
        currentDate = QDate()
        
        self.empno = QLabel("Employment Number")
        self.empnoData = QLineEdit()
        self.empnoData.setObjectName("emp")
        if(data and 'empno' in data and len(str(data['empno'])) > 1):
            self.empnoData.setText(str(data['empno']))
        else:
            self.empnoData.setPlaceholderText("XXXXXXXXXX")
        
        self.title = QLabel("Title")
        self.titleData = QLineEdit()
        self.titleData.setObjectName("title")
        if(data and 'title' in data  and len(str(data['title'])) > 0):
            tx = str(data['title']) 
            self.titleData.setText(tx)
        else:
            self.titleData.setPlaceholderText("Mr., Miss., Dr.")
        

        self.surname = QLabel("Surname")
        self.surnameData = QLineEdit()
        self.surnameData.setObjectName("surname")
        if(data and 'surname' in data and len(str(data['surname'])) > 0):
            tx = str(data['surname']) 
            self.surnameData.setText(tx)
        else:
            self.surnameData.setPlaceholderText("Surname")
        
        
        self.firstname = QLabel("Firstname")
        self.firstnameData = QLineEdit()
        self.firstnameData.setObjectName("firstname")
        if(data and 'firstname' in data  and len(str(data['firstname'])) > 0):
            tx = str(data['firstname']) 
            self.firstnameData.setText(tx)
        else:
            self.firstnameData.setPlaceholderText("Firstname")
       
        
        self.middlename = QLabel("Middlename")
        self.middlenameData = QLineEdit()
        self.middlenameData.setObjectName("middlename")
        if(data and 'othername' in data  and len(str(data['othername'])) > 0):
            tx = str(data['othername']) 
            self.middlenameData.setText(tx)
        else:
            self.middlenameData.setPlaceholderText("Middlename")
        
        
        self.soo = QLabel("State/Region of Origin")
        self.sooData = QLineEdit()
        self.sooData.setObjectName("soo")
        if(data and 'soo' in data and  len(str(data['soo'])) > 0):
            tx = str(data['soo']) 
            self.sooData.setText(tx)
        else:
            self.sooData.setPlaceholderText("Lagos")
        
        
        self.lga = QLabel("LGA/District")
        self.lgaData = QLineEdit()
        self.lgaData.setObjectName("lga")
        if(data and 'lga' in data and  len(data['lga']) > 0):
            tx = str(data['lga']) 
            self.lgaData.setText(tx)
        else:
            self.lgaData.setPlaceholderText("Ikeja")
            
        self.nation = QLabel("Nationality")
        self.nationData = QLineEdit()
        self.nationData.setObjectName("nation")
        if(data and 'nation' in  data):
            tx = str(data['nation'])
            self.nationData.setText(tx)
        else:
            self.nationData.setPlaceholderText("Nigeria")
        
        self.phone1 = QLabel("Phone Number")
        self.phone1Data = QLineEdit()
        self.phone1Data.setObjectName("phone1")
        if(data and 'phone1' in  data and len(str(data['phone2'])) > 0):
            tx = str(data['phone1']) 
            self.phone1Data.setText(tx)
        else:
            self.phone1Data.setPlaceholderText("XXXXXXXXXX")
            
        self.phone2 = QLabel("Alt. Phone Number")
        self.phone2Data = QLineEdit()
        self.phone2Data.setObjectName("phone2")
        if(data and 'phone2' in  data and len(str(data['phone2'])) > 0):
            tx = str(data['phone2']) 
            self.phone2Data.setText(tx)
        else:
            self.phone2Data.setPlaceholderText("XXXXXXXXXX")
        
        self.email = QLabel("Email")
        self.emailData = QLineEdit()
        self.emailData.setObjectName("email")
        if(data and 'email' in  data and len(str(data['email'])) > 0):
            tx = str(data['email']) 
            self.emailData.setText(tx)
        else:
            self.emailData.setPlaceholderText("..xxxxx@xxx.com")
        
        self.addr = QLabel("House Address")
        self.addrData = QTextEdit()
        self.addrData.setObjectName("addr")
        if data and 'addr' in data:
            tx = str(data['addr']) 
            self.addrData.setText(tx)
        else:
            pass
       
        self.dob = QLabel("Date of Birth")
        self.dobData = QDateEdit()
        self.dobData.setObjectName("dob")
        self.dobData.setCalendarPopup(True)
        if data and 'dob' in data and data['dob']:
            try:
                tx =  datetime.fromtimestamp(float(data['dob']))
                self.dobData.setDate(tx)
            except:
                self.dobData.setDate(currentDate.currentDate())
        else:
            self.dobData.setDate(currentDate.currentDate())
        
        self.admit = QLabel("Date Employed")
        self.admitData = QDateEdit()
        self.admitData.setObjectName("admit")
        self.admitData.setCalendarPopup(True)
        if data and 'admit' in data and data['dob']:
            try:
                tx =  datetime.fromtimestamp(float(data['admit']))
                self.admitData.setDate(tx)
            except:
                self.admitData.setDate(currentDate.currentDate())
        else:
            self.admitData.setDate(currentDate.currentDate())
        
        
        relationship = Arrayz().arrayz(1)
        
        #first guardian details
        self.g1name = QLabel("Fullname and Title")
        self.g1Data = QLineEdit()
        self.g1Data.setObjectName("g1name")
        if(data and 'g1' in data and len(data['g1']) > 1):
            tx = str(data['g1']) 
            self.g1Data.setText(tx.title())
        else:
            self.g1Data.setPlaceholderText("Mr. Surname Lastname")
        
        self.g1rel = QLabel('Relationship')
        self.g1relData = QComboBox()
        for d in relationship:
            self.g1relData.addItem(str(relationship[d]).upper(), d)
        if data and 'g1rel' in data:
            index2 = self.g1relData.findData(data['g1rel'])
            if index2 >= 0:
                self.g1relData.setCurrentIndex(index2)
            
        
        self.g1p1 = QLabel("Phone")
        self.g1p1Data = QLineEdit()
        self.g1p1Data.setObjectName("g1p1")
        if data and 'g1p1' in data and  len(str(data['g1p1'])) > 0:
            tx = str(data['g1p1']) 
            self.g1p1Data.setText(tx)
        else:
            self.g1p1Data.setPlaceholderText("XXXXXXXXXXX")
        
        
        self.g1p2 = QLabel("Alt. Phone")
        self.g1p2Data = QLineEdit()
        self.g1p2Data.setObjectName("g1p2")
        if data and 'g1p2' in data and  len(str(data['g1p2'])) > 0:
            tx = str(data['g1p2']) 
            self.g1p2Data.setText(tx)
        else:
            self.g1p2Data.setPlaceholderText("XXXXXXXXXXXX")
        
        
        self.g1email = QLabel("Email")
        self.g1emailData = QLineEdit()
        self.g1emailData.setObjectName("g1email")
        if(data and 'g1email' in data and  len(data['g1email']) > 1):
            tx = str(data['g1email']) 
            self.g1emailData.setText(tx)
        else:
            self.g1emailData.setPlaceholderText("..xxxx@xxxx.xx")
            
        
        self.g1addr = QLabel("Address")
        self.g1addrData = QLineEdit()
        self.g1addrData.setObjectName("g1add")
        if(data and 'g1addr'in data  and len(data['g1addr']) > 1):
            tx = str(data['g1addr']) 
            self.g1addrData.setText(tx)
        else:
            pass
        
         #second guardian details
        self.g2name = QLabel("Alt. Next of Kin")
        self.g2Data = QLineEdit()
        self.g2Data.setObjectName("g2name")
        if(data and 'g2' in data and  len(data['g2']) > 1):
            tx = str(data['g2']) 
            self.g2Data.setText(tx)
        else:
            self.g2Data.setPlaceholderText("Title. Surname Lastname")
            
        
        self.g2rel = QLabel('Relationship')
        self.g2relData = QComboBox()
        for d in relationship:
            self.g2relData.addItem(str(relationship[d]).upper(), d)
        if data and 'g2rel' in data:
            index2 = self.g2relData.findData(data['g2rel'])
            if index2 >= 0:
                self.g2relData.setCurrentIndex(index2)
                
        
        self.g2p1 = QLabel("Phone")
        self.g2p1Data = QLineEdit()
        self.g2p1Data.setObjectName("g2p1")
        if data and 'g2p1' in data and  len(str(data['g2p1'])) > 0:
            tx = str(data['g2p1']) 
            self.g2p1Data.setText(tx)
        else:
            self.g2p1Data.setPlaceholderText("08000000000")
            
        
        self.g2p2 = QLabel("Alt. Phone")
        self.g2p2Data = QLineEdit()
        self.g2p2Data.setObjectName("g2p2")
        if data and 'g2p2' in data and  len(str(data['g2p2'])) > 0:
            tx = str(data['g2p2']) 
            self.g2p2Data.setText(tx)
        else:
            self.g2p2Data.setPlaceholderText("0800000000")
            
        
        self.g2email = QLabel("Email")
        self.g2emailData = QLineEdit()
        self.g2emailData.setObjectName("g2email")
        if(data and 'g2email'  in data  and  len(data['g2email']) > 1):
            tx = data['g2email'] 
            self.g2emailData.setText(tx)
        else:
            self.g2emailData.setPlaceholderText("..xxxx@xxx.xxx")
            
        
        self.g2addr = QLabel("Address")
        self.g2addrData = QLineEdit()
        self.g2addrData.setObjectName("g2addr")
        if(data and 'g2addr' in data and len(data['g2addr']) > 1):
            tx = data['g2addr'] 
            self.g2addrData.setText(tx)
        else:
            pass

        
        self.bank = QLabel("Bank Account")
        self.bankData = QComboBox()
        self.pullCombo(self.bankData, 20)
        if data and 'bank' in data:
            index2 = self.bankData.findData(data['bank'])
            if index2 >= 0:
                self.bankData.setCurrentIndex(index2)
            
        self.account = QLabel("Account Number")
        self.accountData = QLineEdit()
        self.accountData.setObjectName("account")
        if(data and 'account' in  data):
            tx = str(data['account']) 
            self.accountData.setText(tx)
        else:
            pass
        
        self.sort = QLabel("Sort Code")
        self.sortData = QLineEdit()
        self.sortData.setObjectName("sort")
        if(data and 'sort' in  data):
           tx = str(data['sort']) 
           self.sortData.setText(tx)
        else:
           self.sortData.setPlaceholderText("XXXXXXXXXX")
        
        
        self.pen = QLabel("Pension Manager")
        self.penData = QComboBox()
        self.pullCombo(self.penData, 28)
        if data and 'pension' in data:
            index2 = self.penData.findData(data['pension'])
            if index2 >= 0:
                self.penData.setCurrentIndex(index2)
        
        
        self.pencode = QLabel("Pension Code")
        self.pencodeData = QLineEdit()
        self.pencodeData.setObjectName("pencode")
        if(data and 'pensioncode' in  data):
           tx = str(data['pensioncode']) 
           self.pencodeData.setText(tx)
        else:
           self.pencodeData.setPlaceholderText("XXXXXXXXXX")
           
           
        self.health = QLabel("Health Insurance Manager")
        self.healthData = QComboBox()
        self.pullCombo(self.healthData, 29)
        self.healthData.setObjectName("health")
        if data and 'health' in data:
            index2 = self.healthData.findData(data['health'])
            if index2 >= 0:
                self.healthData.setCurrentIndex(index2)
        
        self.healthcode = QLabel("Health Insurance Code")
        self.healthcodeData = QLineEdit()
        self.healthcodeData.setObjectName("healthcode")
        if(data and 'healthcode' in  data):
           tx = str(data['healthcode']) 
           self.healthcodeData.setText(tx)
        else:
           self.healthcodeData.setPlaceholderText("XXXXXXXXXX")
        
        self.socialcode = QLabel("Social Insurance Code")
        self.socialcodeData = QLineEdit()
        self.socialcodeData.setObjectName("socialcode")
        if(data and 'socialcode' in  data):
           tx = str(data['socialcode']) 
           self.socialcodeData.setText(tx)
        else:
           self.socialcodeData.setPlaceholderText("XXXXXXXXXX")
        
        self.tin = QLabel("T.I.N.")
        self.tinData = QLineEdit()
        self.tinData.setObjectName("tin")
        if(data and 'tin' in  data):
            tx = str(data['tin']) 
            self.tinData.setText(tx)
        else:
            self.tinData.setPlaceholderText("XXXXXXXXXX")
        
        self.nin = QLabel("N.I.N")
        self.ninData = QLineEdit()
        self.ninData.setObjectName("nin")
        if(data and 'nin' in  data):
            tx = str(data['nin']) 
            self.ninData.setText(tx)
        else:
            self.ninData.setPlaceholderText("XXXXXXXXXX")
            
       
        users = Arrayz().arrayz(2)
        self.user = QLabel('Permission')
        self.userData = QComboBox()
        for d in users:
            self.userData.addItem(str(users[d]).upper(), d)
        if data and 'user' in data:
            index2 = self.userData.findData(data['user'])
            if index2 >= 0:
                self.userData.setCurrentIndex(index2)
                
        usersaccess = Arrayz().arrayz(3)
        self.access = QLabel('Access Level')
        self.accessData = QComboBox()
        for d in usersaccess:
            self.accessData.addItem(str(usersaccess[d]).upper(), d)
        if data and 'access' in data:
            index2 = self.accessData.findData(data['access'])
            if index2 >= 0:
                self.accessData.setCurrentIndex(index2)
        
        
        self.userspassword = QLabel("Password")
        self.userspasswordData = QLineEdit()
        self.userspasswordData.setObjectName("tin")
        if(data and 'userpassword' in  data):
            tx = str(data['userpassword']) 
            self.userspasswordData.setText(tx)
        else:
            self.userspasswordData.setPlaceholderText("XXXXXXXXXX")
            
            
        reasons = Arrayz().arrayz(4)
        self.reason = QLabel('Reason for leaving')
        self.reasonData = QComboBox()
        for d in reasons:
            self.reasonData.addItem(str(reasons[d]).upper(), d)
        if data and 'reason' in data:
            index2 = self.reasonData.findData(data['reason'])
            if index2 >= 0:
                self.reasonData.setCurrentIndex(index2)
                
        self.dol = QLabel("Date of Leaving")
        self.dolData = QDateEdit()
        self.dolData.setObjectName("dol")
        if data and 'dol' in data and data['dol']:
            try:
                tx =  datetime.fromtimestamp(float(data['dol']))
                self.dolData.setDate(tx)
            except:
                self.dolData.setDate(currentDate.currentDate())
        else:
            self.dolData.setDate(currentDate.currentDate())
        
        self.dolinfo = QLabel("Details")
        self.dolinfoData = QTextEdit()
        self.dolinfoData.setObjectName("dolinfo")
        if(data and 'dolinfo' in  data):
            tx = str(data['dolinfo']) 
            self.dolinfoData.setText(tx)
            
        
        gender = Arrayz().arrayz(5)
        self.gender = QLabel('Gender')
        self.genderData = QComboBox()
        for d in gender:
            self.genderData.addItem(str(gender[d]).upper(), d)
        if data and 'gender' in data:
            index2 = self.genderData.findData(data['gender'])
            if index2 >= 0:
                self.genderData.setCurrentIndex(index2)   
                
        marital = Arrayz().arrayz(6)
        self.marital = QLabel('Marital Sataus')
        self.maritalData = QComboBox()
        for d in marital:
            self.maritalData.addItem(str(marital[d]).upper(), d)
        if data and 'marital' in data:
            index2 = self.maritalData.findData(data['marital'])
            if index2 >= 0:
                self.maritalData.setCurrentIndex(index2) 
                
        religion = Arrayz().arrayz(7)
        self.religion = QLabel('Religion')
        self.religionData = QComboBox()
        for d in religion:
            self.religionData.addItem(str(religion[d]).upper(), d)
        if data and 'religion' in data:
            index2 = self.religionData.findData(data['religion'])
            if index2 >= 0:
                self.religionData.setCurrentIndex(index2)
                
        self.noc = QLabel("Children")
        self.nocData = QLineEdit()
        self.nocData.setObjectName("noc")
        if(data and 'noc' in  data):
            tx = str(data['noc']) 
            self.nocData.setText(tx)
        else:
            self.nocData.setText(str(0))
                 
        self.department = QLabel('Department')
        self.departmentData = QComboBox()
        self.pullCombo(self.departmentData, 27)
        if data and 'department' in data:
            index2 = self.departmentData.findData(data['department'])
            if index2 >= 0:
                self.departmentData.setCurrentIndex(index2)
        
        self.unit = QLabel('Unit')
        self.unitData = QComboBox()
        self.pullCombo(self.unitData, 27)
        if data and 'unit' in data:
            index2 = self.unitData.findData(data['unit'])
            if index2 >= 0:
                self.unitData.setCurrentIndex(index2)
        
        #photo
        self.pic1 = QLabel()
        if(data and 'pix' in  data and len(str(data['pix'])) > 0):
            if os.path.isfile('./pic_main/'+str(data['pix'])):
                image1 = Image.open('pic_main/'+str(data['pix']))
            else:
                image1 = Image.open('img/stdpic.png')
        else:
            image1 = Image.open('img/stdpic.png')
        imageQ1 = ImageQt(image1)
        imagep1 = QPixmap(QPixmap.fromImage(QImage(imageQ1).scaled(130, 130, Qt.IgnoreAspectRatio)))
        self.pic1.resize(130, 130)
        self.pic1.setPixmap(imagep1)
        self.pic1.setMaximumHeight(130)
        self.pic1.setMaximumWidth(130)
        self.picBtn1 = QPushButton('Select Image')
        self.picBtn1.setMaximumHeight(30)
        self.picBtn1.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.picLink = ''
        self.picBtn1.clicked.connect(lambda:self.getFilez(1, 1))
        
        self.pic2 = QLabel()
        if(data and 'g1pix' in  data and len(str(data['g1pix'])) > 0):
            if os.path.isfile('./pic_main/'+str(data['g1pix'])):
                image2 = Image.open('pic_main/'+str(data['g1pix']))
            else:
                image2 = Image.open('img/stdpic.png')
        else:
            image2 = Image.open('img/stdpic.png')
        imageQ2 = ImageQt(image2)
        imagep2 = QPixmap(QPixmap.fromImage(QImage(imageQ2).scaled(80, 80, Qt.IgnoreAspectRatio)))
        self.pic2.resize(80, 80)
        self.pic2.setPixmap(imagep2)
        #self.pic2.setMaximumHeight(80)
        self.pic2.setMaximumWidth(80)
        self.picBtn2 = QPushButton('Select')
        self.picBtn2.setMaximumHeight(30)
        self.picBtn2.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.g1picLink = ''
        self.picBtn2.clicked.connect(lambda:self.getFilez(2,1))
        
        self.pic3 = QLabel()
        if(data and 'g2pix' in data and len(str(data['g2pix'])) > 0 ):
            if os.path.isfile('./pic_main/'+str(data['g2pix'])):
                image3 = Image.open('pic_main/'+str(data['g2pix']))
            else:
                image3 = Image.open('img/stdpic.png')
        else:
            image3 = Image.open('img/stdpic.png')
        imageQ3 = ImageQt(image3)
        imagep3 = QPixmap(QPixmap.fromImage(QImage(imageQ3).scaled(80, 80, Qt.IgnoreAspectRatio)))
        self.pic3.resize(80, 80)
        self.pic3.setPixmap(imagep3)
        #self.pic3.setMaximumHeight(80)
        self.pic3.setMaximumWidth(80)
        self.picBtn3 = QPushButton('Select')
        self.picBtn3.setMaximumHeight(30)
        self.picBtn3.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.g2picLink = ''
        self.picBtn3.clicked.connect(lambda:self.getFilez(3, 1))
        
        picGrid = QGridLayout()
        picGrid.addWidget(self.pic1, 0, 0)
        picGrid.addWidget(self.picBtn1, 1, 0)
        
        picGrid1 = QGridLayout()
        picGrid1.addWidget(self.pic2, 0, 0)
        picGrid1.addWidget(self.picBtn2, 1, 0)
        
        picGrid2 = QGridLayout()
        picGrid2.addWidget(self.pic3, 0, 0)
        picGrid2.addWidget(self.picBtn3, 1, 0)
        
        gridWidget = QWidget()
        gridWidget.setLayout(picGrid)
        gridWidget.setMaximumWidth(150)
        gridWidget.setMaximumHeight(150)
        gridWidget.setContentsMargins(0, 0, 0, 0)
        
        gridWidget1 = QWidget()
        gridWidget1.setLayout(picGrid1)
        gridWidget1.setMaximumWidth(80)
        gridWidget1.setMaximumHeight(100)
        gridWidget1.setContentsMargins(0, 0, 0, 0)
        
        gridWidget2 = QWidget()
        gridWidget2.setLayout(picGrid2)
        gridWidget2.setMaximumWidth(80)
        gridWidget2.setMaximumHeight(100)
        gridWidget2.setContentsMargins(0, 0, 0, 0)
        
        g_1 = QGridLayout()
        g_1.addWidget(self.title, 0, 0)
        g_1.addWidget(self.titleData, 0, 1)
        g_1.addWidget(self.surname,1,0)
        g_1.addWidget(self.surnameData,1,1)
        g_1.addWidget(self.firstname,2,0)
        g_1.addWidget(self.firstnameData,2,1)
        g_1.addWidget(self.middlename,3,0)
        g_1.addWidget(self.middlenameData,3,1)
        g_1.addWidget(self.dob,4,0)
        g_1.addWidget(self.dobData,4,1)
        g_1.addWidget(self.gender,5,0)
        g_1.addWidget(self.genderData,5,1)
        g_1.addWidget(self.marital,0,2)
        g_1.addWidget(self.maritalData,0,3)
        g_1.addWidget(self.noc,1,2)
        g_1.addWidget(self.nocData,1,3)
        g_1.addWidget(self.religion,2,2)
        g_1.addWidget(self.religionData,2,3)
        g_1.addWidget(self.lga,3,2)
        g_1.addWidget(self.lgaData,3,3)
        g_1.addWidget(self.soo,4,2)
        g_1.addWidget(self.sooData,4,3)
        g_1.addWidget(self.nation,5,2)
        g_1.addWidget(self.nationData,5,3)
        g_1.addWidget(self.phone1, 0, 4)
        g_1.addWidget(self.phone1Data,0,5)
        g_1.addWidget(self.phone2,1,4)
        g_1.addWidget(self.phone2Data,1,5)
        g_1.addWidget(self.email, 2, 4)
        g_1.addWidget(self.emailData,2,5)
        g_1.addWidget(self.addr, 3, 4, 1, 2)
        g_1.addWidget(self.addrData, 4, 4, 2, 2)
        
        Formlayout1 = QGridLayout()
        Formlayout1.addWidget(self.g1name, 0, 0)
        Formlayout1.addWidget(self.g1Data, 0, 1, 1, 3)
        Formlayout1.addWidget(self.g1rel, 1, 0)
        Formlayout1.addWidget(self.g1relData,1 , 1)
        Formlayout1.addWidget(self.g1email, 1, 2)
        Formlayout1.addWidget(self.g1emailData, 1, 3)
        Formlayout1.addWidget(self.g1p1,2,0)
        Formlayout1.addWidget(self.g1p1Data,2,1)
        Formlayout1.addWidget(self.g1p2,2,2)
        Formlayout1.addWidget(self.g1p2Data,2,3)
        Formlayout1.addWidget(self.g1addr, 3, 0)
        Formlayout1.addWidget(self.g1addrData, 3, 1, 1, 3)
        
        Formlayout2 = QGridLayout()
        Formlayout2.addWidget(self.g2name, 0, 0)
        Formlayout2.addWidget(self.g2Data, 0, 1, 1, 3)
        Formlayout2.addWidget(self.g2rel, 1, 0)
        Formlayout2.addWidget(self.g2relData,1 , 1)
        Formlayout2.addWidget(self.g2email, 1, 2)
        Formlayout2.addWidget(self.g2emailData, 1, 3)
        Formlayout2.addWidget(self.g2p1,2,0)
        Formlayout2.addWidget(self.g2p1Data,2,1)
        Formlayout2.addWidget(self.g2p2,2,2)
        Formlayout2.addWidget(self.g2p2Data,2,3)
        Formlayout2.addWidget(self.g2addr, 3, 0)
        Formlayout2.addWidget(self.g2addrData, 3, 1, 1, 3)
        
        Formlayout3 = QFormLayout()
        Formlayout3.addRow(self.bank, self.bankData)
        Formlayout3.addRow(self.account, self.accountData)
        Formlayout3.addRow(self.sort, self.sortData)
        Formlayout3.addRow(self.pen, self.penData)
        Formlayout3.addRow(self.pencode, self.pencodeData)
        Formlayout3.addRow(self.tin, self.tinData)
        Formlayout3.addRow(self.health, self.healthData)
        Formlayout3.addRow(self.healthcode, self.healthcodeData)
        Formlayout3.addRow(self.socialcode, self.socialcodeData)
        
        Formlayout4 = QFormLayout()
        Formlayout4.addRow(self.user, self.userData)
        Formlayout4.addRow(self.access, self.accessData)
        Formlayout4.addRow(self.userspassword, self.userspasswordData)
        Formlayout4.addRow(self.nin, self.ninData)
        
        Formlayout5 = QFormLayout()
        Formlayout5.addRow(self.reason, self.reasonData)
        Formlayout5.addRow(self.dol, self.dolData)
        Formlayout5_grid = QGridLayout()
        Formlayout5_grid.addWidget(self.dolinfo, 0, 0)
        Formlayout5_grid.addWidget(self.dolinfoData, 1, 0)
        reasonInt = QLabel('For staff leaving the institution')
        
        Formlayout6 = QFormLayout()
        Formlayout6.addRow(self.empno, self.empnoData)
        Formlayout6.addRow(self.admit, self.admitData)
        Formlayout6.addRow(self.department, self.departmentData)
        Formlayout6.addRow(self.unit, self.unitData)
        
        
        a_hbox1 = QVBoxLayout()
        a_hbox1.addLayout(Formlayout4)
        
        r_hbox1 = QVBoxLayout()
        r_hbox1.addWidget(reasonInt)
        r_hbox1.addStretch()
        r_hbox1.addLayout(Formlayout5)
        r_hbox1.addLayout(Formlayout5_grid)
        
        bio_box = QHBoxLayout()
        bio_box.addLayout(g_1)
        bio_box.addWidget(gridWidget)
      
        kin_grid1 = QGridLayout()
        kin_grid1.addLayout(Formlayout1, 0, 0)
        kin_grid1.addWidget(gridWidget1, 0, 1)
        kin_grid2 = QGridLayout()
        kin_grid2.addLayout(Formlayout2, 0 ,0)
        kin_grid2.addWidget(gridWidget2, 0, 1)
        
        self.pb = QPushButton()
        self.pb.setObjectName("Submit")
        self.pb.setText("Submit")
        
        self.pb1 = QPushButton()
        self.pb1.setObjectName("Cancel")
        self.pb1.setText("Cancel")
        
        grid_button = QGridLayout()
        grid_button.addWidget(self.pb,0,0)
        grid_button.addWidget(self.pb1,0,1)
        
        vbox1 = QVBoxLayout()
        vbox1.addLayout(Formlayout1)
        vbox1.addStretch()
        vbox1.addLayout(Formlayout2)
        
        groupBox1 = QGroupBox('Bio-Data')
        groupBox1.setLayout(bio_box)
        groupBox1.setMaximumHeight(180)
        groupBox1.setContentsMargins(1,1,1,1)
        
        groupBox2a = QGroupBox('Next of Kins')
        groupBox2a.setLayout(kin_grid1)
        groupBox2a.setMaximumHeight(140)
        groupBox2a.setContentsMargins(1,1,1,1)
        groupBox2b = QGroupBox(' Alternate Next of Kins')
        groupBox2b.setLayout(kin_grid2)
        groupBox2b.setMaximumHeight(140)
        groupBox2b.setContentsMargins(1,1,1,1)
        groupBox2_h = QHBoxLayout()
        groupBox2_h.addWidget(groupBox2a)
        groupBox2_h.addWidget(groupBox2b)
        
        groupBox3 = QGroupBox('Financial')
        groupBox3.setLayout(Formlayout3)
        #groupBox3.setMaximumHeight(240)
        #groupBox3.setMaximumWidth(250)
        groupBox3.setContentsMargins(1,1,1,1)
        
        groupBox4 = QGroupBox('Account')
        groupBox4.setLayout(a_hbox1)
        groupBox4.setMaximumWidth(250)
        
        groupBox5 = QGroupBox('Discontinuaton of Service')
        groupBox5.setLayout(r_hbox1)
        groupBox5.setMaximumWidth(250)
        
        groupBox6 = QGroupBox('Administrative')
        groupBox6.setLayout(Formlayout6)
        groupBox6.setMaximumWidth(250)
        
        v_groupBox = QVBoxLayout()
        v_groupBox.addWidget(groupBox6)
        v_groupBox.addWidget(groupBox4)
        
        h_groupBox = QHBoxLayout()
        h_groupBox.addLayout(v_groupBox)
        h_groupBox.addWidget(groupBox3)
        h_groupBox.addWidget(groupBox5)
        
        main_h = QVBoxLayout()
        main_h.addWidget(groupBox1)
        main_h.addLayout(groupBox2_h)
        main_h.addLayout(h_groupBox)
        main_h.addLayout(grid_button)
        
        self.pb.clicked.connect(lambda:self.button1_click())
        self.pb1.clicked.connect(lambda:self.button1_click())
        
        self.setLayout(main_h)
        self.setStyleSheet(stylesheet)
        self.setWindowIcon(QIcon(self.titleIcon))
        self.setWindowTitle(self.pagetitle)
            
        
    def pullData(self, db, sid, arr):
        pass
     
    def pullCombo(self, combo, sid):
        combo.clear()
        data = Valid().pullData('datas', 200000, {'pubID': sid})
        if data:
            for d  in data:
                combo.addItem(str(d['name']).upper(), d['id'])
        
    def getSave(self, sid, a):
        sid = sid
        file1 = 'pic_thumb/'
        file2 = 'pic_main/'
        
        arr = {}
        if a == 1:
             fname = self.picLink
             im1 = fname
             lnk = "staff_"+str(sid)+'_'+str(a)+".png"
             im1.thumbnail((128, 128))
             im1.save(file1 + lnk, "PNG" )
             im1.thumbnail((700, 700))
             im1.save(file2 + lnk, "PNG")
             arr['pix'] = lnk
        elif a == 2:
             fname = self.g1picLink
             im1 = fname
             lnk = "kin1_"+str(sid)+'_'+str(a)+".png"
             im1.thumbnail((128, 128))
             im1.save(file1 + lnk, "PNG" )
             im1.thumbnail((700, 700))
             im1.save(file2 + lnk, "PNG")
             arr['g1pix'] = lnk
        elif a == 3:
             fname = self.g2picLink
             im1 = fname
             lnk = "kin2_"+str(sid)+'_'+str(a)+".png"
             im1.thumbnail((128, 128))
             im1.save(file1 + lnk, "PNG" )
             im1.thumbnail((700, 700))
             im1.save(file2 + lnk, "PNG")
             arr['g2pix'] = lnk
             
        g = Db()
        g.update('staffs', arr, {'id':sid})
           
        
         
    def getFilez(self, a, pos):
         fname = QFileDialog.getOpenFileName(self, 'Open', 'c:\\')
         image1 = Image.open(fname)
         imageQ1 = ImageQt(image1)
         imagep1 = QPixmap(QPixmap.fromImage(QImage(imageQ1).scaled(130, 130, Qt.IgnoreAspectRatio)))
         self.pic1.resize(150, 150)
         
         if a == 1:
             self.pic1.setPixmap(imagep1)
             self.picLink =image1
         elif a == 2:
             self.pic2.setPixmap(imagep1)
             self.g1picLink = image1
         elif a == 3:
             self.pic3.setPixmap(imagep1)
             self.g2picLink = image1
             
      
        
    
    def button1_click(self):
        # shost is a QString object
        #biodata
        arr = {}
        arr = {}
        arr['title'] = self.titleData.text()
        arr['surname'] = self.surnameData.text()
        arr['firstname'] = self.firstnameData.text()
        arr['othername'] = self.middlenameData.text()
        arr['soo'] = self.sooData.text()
        arr['lga'] = self.lgaData.text()
        arr['nation'] = self.nationData.text()
        arr['noc'] = self.nocData.text()
        arr['phone1'] = self.phone1Data.text()
        arr['phone2'] = self.phone2Data.text()
        arr['email'] = self.emailData.text()
        arr['addr'] = self.addrData.toPlainText().encode('utf-8').strip()
        arr['gender'] = self.genderData.itemData(self.genderData.currentIndex())
        arr['marital'] = self.maritalData.itemData(self.maritalData.currentIndex())
        arr['religion'] = self.religionData.itemData(self.religionData.currentIndex())
        dob = self.dobData.date().toPyDate()
        arr['dob'] = time.mktime(dob.timetuple())
        
        #admistrative
        arr['empno'] = self.empnoData.text()
        arr['department']  = self.departmentData.itemData(self.departmentData.currentIndex())
        arr['unit'] = self.unitData.itemData(self.unitData.currentIndex())
        admit = self.admitData.date().toPyDate()
        arr['admit'] = time.mktime(admit.timetuple())
        #account
        arr['user'] = self.userData.itemData(self.userData.currentIndex())
        arr['access'] = self.accessData.itemData(self.accessData.currentIndex())
        arr['userpassword'] = self.userspasswordData.text()
        dol = self.dolData.date().toPyDate()
        arr['dol'] = time.mktime(dol.timetuple())
        arr['reason'] = self.reasonData.itemData(self.reasonData.currentIndex())
        arr['dolinfo'] = self.dolinfoData.toPlainText().encode('utf-8').strip()
        #finance
        arr['bank'] = self.bankData.itemData(self.bankData.currentIndex())
        arr['account'] = self.accountData.text()
        arr['sort'] = self.sortData.text()
        arr['pension'] = self.penData.itemData(self.penData.currentIndex())
        arr['pensioncode'] = self.pencodeData.text()
        arr['tin'] = self.tinData.text()
        arr['nin'] = self.ninData.text()
        arr['health'] = self.healthData.itemData(self.healthData.currentIndex())
        arr['healthcode'] = self.healthcodeData.text()
        arr['socialcode'] = self.socialcodeData.text()
        #kin
        arr['g1'] = self.g1Data.text()
        arr['g1rel'] = self.g1relData.itemData(self.g1relData.currentIndex())
        arr['g1p1'] = self.g1p1Data.text()
        arr['g1p2'] = self.g1p2Data.text()
        arr['g1email'] = self.g1emailData.text()
        arr['g1addr'] = self.g1addrData.text()
        arr['g2'] = self.g2Data.text()
        arr['g2rel'] = self.g2relData.itemData(self.g2relData.currentIndex())
        arr['g2p1'] = self.g2p1Data.text()
        arr['g2p2'] = self.g2p2Data.text()
        arr['g2email'] = self.g2emailData.text()
        arr['g2addr'] = self.g2addrData.text()

        g = Db()
        chk = g.selectn('staffs', '', 1, {'empno':arr['empno']}) 
        if((arr['surname']) and (arr['firstname']) and (arr['empno'])):
            if self.sid > 0:
                g.update('staffs', arr, {'id':self.sid})
                try:
                    self.getSave(self.sid, 1)
                except:
                    pass
                try:
                    self.getSave(self.sid, 2)
                except:
                    pass
                try:
                    self.getSave(self.sid, 3)
                except:
                    pass
      
        self.close()
       
        
class StaffFormDetails(QDialog):
    
    def __init__(self, sid, parent=None):
        super(StaffFormDetails, self).__init__(parent)
        stylesheet = Valid().background() + Valid().font()
        self.pagetitle = 'Staff'
        self.titleIcon = ''
        self.resize(500, 700)
        self.setFixedHeight(500)
        self.setFixedWidth(700)
        self.tableFont = QFont()
        self.tableFont.setFamily('Century Gothic')
        self.sid = sid
        
        menu = self.menuUi()
        
        self.tabz = QTabWidget(self)
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tab4 = QWidget()
        self.tab5 = QWidget()
        self.tab6 = QWidget()
        self.tab7 = QWidget()
        g= Db()
        data = g.selectn('staffs', '', 1, {'id':self.sid})
        currentDate = QDate()
        
        #academic
        self.school = QLabel("Name of Institution")
        self.schoolData = QLineEdit()
        self.schoolData.setObjectName("sch")
        self.schoolData.setPlaceholderText("Federal Univerity of Technology, Minna, Niger State, Nigeria")
        
        self.course = QLabel("Course Studied")
        self.courseData = QLineEdit()
        self.courseData.setObjectName("course")
        self.courseData.setPlaceholderText("Chemistry Education")
        
        self.degree = QLabel("Class of Degree")
        self.degreeData = QLineEdit()
        self.degreeData.setObjectName("deg")
        self.degreeData.setPlaceholderText("B.Ed.")
        
        self.grade = QLabel("Grade")
        self.gradeData = QLineEdit()
        self.gradeData.setObjectName("grade")
        self.gradeData.setPlaceholderText("Second Class Upper Division")
        
        self.doc = QLabel("Grade")
        self.docData = QPushButton('No File')
        self.docData.setObjectName("grade")
        #self.docData.setPlaceholderText("Second Class Upper Division")
        self.startdate = QLabel("Started")
        self.startdateData = QDateEdit()
        self.startdateData.setObjectName("startdate")
        self.startdateData.setCalendarPopup(True)

        self.enddate = QLabel("Ended")
        self.enddateData = QDateEdit()
        self.enddateData.setObjectName("enddate")
        self.enddateData.setCalendarPopup(True)
        
                #professional
        self.institute = QLabel("Organization")
        self.instituteData = QLineEdit()
        self.instituteData.setObjectName("org")
        self.instituteData.setPlaceholderText("Teachers Registration Council")
        
        self.course1 = QLabel("Course Studied")
        self.course1Data = QLineEdit()
        self.course1Data.setObjectName("course1")
        self.course1Data.setPlaceholderText("Graduate Member")
        
        self.degree1 = QLabel("Area of Specification")
        self.degree1Data = QLineEdit()
        self.degree1Data.setObjectName("deg1")
        self.degree1Data.setPlaceholderText("Child Education")
        
        self.doc1 = QLabel("Grade")
        self.doc1Data = QPushButton('No File')
        self.doc1Data.setObjectName("Upload File")

        self.startdate1 = QLabel("Started")
        self.startdate1Data = QDateEdit()
        self.startdate1Data.setObjectName("startdate1")
        self.startdate1Data.setCalendarPopup(True)
        #work
        self.company = QLabel("Organization")
        self.companyData = QLineEdit()
        self.companyData.setObjectName("com")
        self.companyData.setPlaceholderText("Organization's Name and Address")

        self.position = QLabel("Position Held")
        self.positionData = QLineEdit()
        self.positionData.setObjectName("pos")
        self.positionData.setPlaceholderText("Head Teacher")

        self.job = QLabel("Organization")
        self.jobData = QPlainTextEdit()
        self.jobData.setObjectName("job")

        self.startdate2 = QLabel("Started")
        self.startdate2Data = QDateEdit()
        self.startdate2Data.setObjectName("startdate2")
        self.startdate2Data.setCalendarPopup(True)

        self.enddate2 = QLabel("Ended")
        self.enddate2Data = QDateEdit()
        self.enddate2Data.setObjectName("enddate2")
        self.enddate2Data.setCalendarPopup(True)

        #seminar
        self.seminar = QLabel("Organized By:")
        self.seminarData = QLineEdit()
        self.seminarData.setObjectName("orgby")
        self.seminarData.setPlaceholderText("Organization's Name and Address")

        self.seminartitle = QLabel("Theme/Title")
        self.seminartitleData = QLineEdit()
        self.seminartitleData.setObjectName("seminartitle")
        self.seminartitleData.setPlaceholderText("...")

        self.seminargrade = QLabel("Qualification Received")
        self.seminargradeData = QLineEdit()
        self.seminargradeData.setObjectName("seminargrade")
        self.seminargradeData.setPlaceholderText("...")

        self.seminarcontent = QLabel("Training Content")
        self.seminarcontentData = QPlainTextEdit()
        self.seminarcontentData.setObjectName("trainingcontent")

        self.startdate3 = QLabel("Started")
        self.startdate3Data = QDateEdit()
        self.startdate3Data.setObjectName("startdate3")
        self.startdate3Data.setCalendarPopup(True)

        self.enddate3 = QLabel("Ended")
        self.enddate3Data = QDateEdit()
        self.enddate3Data.setObjectName("enddate3")
        self.enddate3Data.setCalendarPopup(True)

        #discipline 
        self.act1 = QLabel("Reprehensible Action")
        self.act1Data = QPlainTextEdit()
        self.act1Data.setObjectName("rep")

        self.react1 = QLabel("Disciplinary Action")
        self.react1Data = QPlainTextEdit()
        self.react1Data.setObjectName("discipline")

        self.supervisor1 = QLabel("Issued By:")
        self.supervisor1Data = QLineEdit()
        self.supervisor1Data.setObjectName("supervisor1")

        self.startdate4 = QLabel("Started")
        self.startdate4Data = QDateEdit()
        self.startdate4Data.setObjectName("startdate4")
        self.startdate4Data.setCalendarPopup(True)

        #commendation 
        self.act2 = QLabel("Commendable Action")
        self.act2Data = QPlainTextEdit()
        self.act2Data.setObjectName("commendation")

        self.react2 = QLabel("Award/Commendation Received")
        self.react2Data = QPlainTextEdit()
        self.react2Data.setObjectName("award")

        self.supervisor2 = QLabel("Issued By:")
        self.supervisor2Data = QLineEdit()
        self.supervisor2Data.setObjectName("supervisor2")

        self.startdate5 = QLabel("Started")
        self.startdate5Data = QDateEdit()
        self.startdate5Data.setObjectName("startdate5")
        self.startdate5Data.setCalendarPopup(True)

        #duties
        self.group = QLabel("Title/Committee")
        self.groupData = QLineEdit()
        self.groupData.setObjectName("pos")
        self.groupData.setPlaceholderText("eg. Management, Sports Committee etc")

        self.office = QLabel("Office/Position")
        self.officeData = QLineEdit()
        self.officeData.setObjectName("off")
        self.officeData.setPlaceholderText("Committee Chairman, Principal, Games Master etc.")

        self.mandate = QLabel("Mandate")
        self.mandateData = QPlainTextEdit()
        self.mandateData.setObjectName("mandate")

        self.startdate6 = QLabel("Start")
        self.startdate6Data = QDateEdit()
        self.startdate6Data.setObjectName("startdate6")
        self.startdate6Data.setCalendarPopup(True)

        self.enddate6 = QLabel("Ends")
        self.enddate6Data = QDateEdit()
        self.enddate6Data.setObjectName("enddate6")
        self.enddate6Data.setCalendarPopup(True)

        #academic
        grid1 = QGridLayout()
        grid1.addWidget(self.school, 0, 0)
        grid1.addWidget(self.schoolData, 0, 1, 1, 3)
        grid1.addWidget(self.degree, 1, 0)
        grid1.addWidget(self.degreeData, 1, 1)
        grid1.addWidget(self.course, 1, 2)
        grid1.addWidget(self.courseData, 1, 3)
        grid1.addWidget(self.grade, 2, 0)
        grid1.addWidget(self.gradeData, 2, 1)
        grid1.addWidget(self.doc, 2, 2)
        grid1.addWidget(self.docData, 2, 3)
        grid1.addWidget(self.startdate, 3, 0)
        grid1.addWidget(self.startdateData, 3, 1)
        grid1.addWidget(self.enddate, 3, 2)
        grid1.addWidget(self.enddateData, 3, 3)

        #professional
        grid2 = QGridLayout()
        grid2.addWidget(self.institute, 0, 0)
        grid2.addWidget(self.instituteData, 0, 1, 1, 3)
        grid2.addWidget(self.degree1, 1, 0)
        grid2.addWidget(self.degree1Data, 1, 1)
        grid2.addWidget(self.course1, 1, 2)
        grid2.addWidget(self.course1Data, 1, 3)
        grid2.addWidget(self.doc1, 2, 0)
        grid2.addWidget(self.doc1Data, 2, 1)
        grid2.addWidget(self.startdate1, 2, 2)
        grid2.addWidget(self.startdate1Data, 2, 3)
        
        #work
        grid3 = QGridLayout()
        grid3.addWidget(self.company, 0, 0)
        grid3.addWidget(self.companyData, 0, 1, 1, 3)
        grid3.addWidget(self.position, 1, 0)
        grid3.addWidget(self.positionData, 1, 1, 1, 3)
        grid3.addWidget(self.job, 2, 0)
        grid3.addWidget(self.jobData, 2, 1, 1, 3)
        grid3.addWidget(self.startdate2, 3, 0)
        grid3.addWidget(self.startdate2Data, 3, 1)
        grid3.addWidget(self.enddate2, 3, 2)
        grid3.addWidget(self.enddate2Data, 3, 3)

        #seminar
        grid4 = QGridLayout()
        grid4.addWidget(self.seminar, 0, 0)
        grid4.addWidget(self.seminarData, 0, 1, 1, 3)
        grid4.addWidget(self.seminartitle, 1, 0)
        grid4.addWidget(self.seminartitleData, 1, 1, 1, 3)
        grid4.addWidget(self.seminarcontent, 2, 0)
        grid4.addWidget(self.seminarcontentData, 2, 1, 1, 3)
        grid4.addWidget(self.seminargrade, 3, 0)
        grid4.addWidget(self.seminargradeData, 3, 1, 1, 3)
        grid4.addWidget(self.startdate3, 4, 0)
        grid4.addWidget(self.startdate3Data, 4, 1)
        grid4.addWidget(self.enddate3, 4, 2)
        grid4.addWidget(self.enddate3Data, 4, 3)

        #discipline
        grid5 = QFormLayout()
        grid5.addRow(self.act1, self.act1Data)
        grid5.addRow(self.react1, self.react1Data)
        grid5.addRow(self.supervisor1, self.supervisor1Data)
        grid5.addRow(self.startdate4, self.startdate4Data)
        #commendation
        grid6 = QFormLayout()
        grid6.addRow(self.act2, self.act2Data)
        grid6.addRow(self.react2, self.react2Data)
        grid6.addRow(self.supervisor2, self.supervisor2Data)
        grid6.addRow(self.startdate5, self.startdate5Data)
        #duties
        grid7 = QFormLayout()
        grid7.addRow(self.group, self.groupData)
        grid7.addRow(self.office, self.officeData)
        grid7.addRow(self.mandate, self.mandateData)
        grid7.addRow(self.startdate6, self.startdate6Data)
        grid7.addRow(self.enddate6, self.enddate6Data)

        #academic
        self.pb1 = QPushButton()
        self.pb1.setObjectName("Submit")
        self.pb1.setText("Submit")
        
        self.pbc1 = QPushButton()
        self.pbc1.setObjectName("Close")
        self.pbc1.setText("Close")
        
        nadd = Buttons().addButton()
        self.pbs1 = QPushButton()
        self.pbs1.setIcon(QIcon(nadd))
        
        nprint = Buttons().printButton()
        self.pbp1 = QPushButton()
        self.pbp1.setIcon(QIcon(nprint))
        
        grid_button1 = QGridLayout()
        grid_button1.addWidget(self.pbc1,0,0)
        grid_button1.addWidget(self.pb1,0,1)
        #professional
        self.pb2 = QPushButton()
        self.pb2.setObjectName("Submit")
        self.pb2.setText("Submit")
        
        self.pbc2 = QPushButton()
        self.pbc2.setObjectName("Close")
        self.pbc2.setText("Close")
        
        self.pbs2 = QPushButton()
        self.pbs2.setObjectName("Add")
        self.pbs2.setText("Add")
        
        nadd = Buttons().addButton()
        self.pbs2 = QPushButton()
        self.pbs2.setIcon(QIcon(nadd))
        
        nprint = Buttons().printButton()
        self.pbp2 = QPushButton()
        self.pbp2.setIcon(QIcon(nprint))
        
        grid_button2 = QGridLayout()
        grid_button2.addWidget(self.pbc2,0,0)
        grid_button2.addWidget(self.pb2,0,1)
        #work
        self.pb3 = QPushButton()
        self.pb3.setObjectName("Submit")
        self.pb3.setText("Submit")
        
        self.pbc3 = QPushButton()
        self.pbc3.setObjectName("Close")
        self.pbc3.setText("Close")
        
        nadd = Buttons().addButton()
        self.pbs3 = QPushButton()
        self.pbs3.setIcon(QIcon(nadd))
        
        nprint = Buttons().printButton()
        self.pbp3 = QPushButton()
        self.pbp3.setIcon(QIcon(nprint))
        
        grid_button3 = QGridLayout()
        grid_button3.addWidget(self.pbc3,0,0)
        grid_button3.addWidget(self.pb3,0,1)
        #seminar
        self.pb4 = QPushButton()
        self.pb4.setObjectName("Submit")
        self.pb4.setText("Submit")
        
        self.pbc4 = QPushButton()
        self.pbc4.setObjectName("Close")
        self.pbc4.setText("Close")
        
        nadd = Buttons().addButton()
        self.pbs4 = QPushButton()
        self.pbs4.setIcon(QIcon(nadd))
        
        nprint = Buttons().printButton()
        self.pbp4 = QPushButton()
        self.pbp4.setIcon(QIcon(nprint))
        
        grid_button4 = QGridLayout()
        grid_button4.addWidget(self.pbc4,0,0)
        grid_button4.addWidget(self.pb4,0,1)
        #discipline
        self.pb5 = QPushButton()
        self.pb5.setObjectName("Submit")
        self.pb5.setText("Submit")
        
        self.pbc5 = QPushButton()
        self.pbc5.setObjectName("Close")
        self.pbc5.setText("Close")
        
        nadd = Buttons().addButton()
        self.pbs5 = QPushButton()
        self.pbs5.setIcon(QIcon(nadd))
        
        nprint = Buttons().printButton()
        self.pbp5 = QPushButton()
        self.pbp5.setIcon(QIcon(nprint))
        
        grid_button5 = QGridLayout()
        grid_button5.addWidget(self.pbc5,0,0)
        grid_button5.addWidget(self.pb5,0,1)

        #commendation
        self.pb6 = QPushButton()
        self.pb6.setObjectName("Submit")
        self.pb6.setText("Submit")
        
        self.pbc6 = QPushButton()
        self.pbc6.setObjectName("Close")
        self.pbc6.setText("Close")
        
        nadd = Buttons().addButton()
        self.pbs6 = QPushButton()
        self.pbs6.setIcon(QIcon(nadd))
        
        nprint = Buttons().printButton()
        self.pbp6 = QPushButton()
        self.pbp6.setIcon(QIcon(nprint))
        
        grid_button6 = QGridLayout()
        grid_button6.addWidget(self.pbc6,0,0)
        grid_button6.addWidget(self.pb6,0,6)
        
        #duties
        self.pb7 = QPushButton()
        self.pb7.setObjectName("Submit")
        self.pb7.setText("Submit")
        
        self.pbc7 = QPushButton()
        self.pbc7.setObjectName("Close")
        self.pbc7.setText("Close")
        
        nadd = Buttons().addButton()
        self.pbs7 = QPushButton()
        self.pbs7.setIcon(QIcon(nadd))
        
        nprint = Buttons().printButton()
        self.pbp7 = QPushButton()
        self.pbp7.setIcon(QIcon(nprint))
        
        grid_button7 = QGridLayout()
        grid_button7.addWidget(self.pbc7,0,0)
        grid_button7.addWidget(self.pb7,0,1)

        #1
        self.v_grid1 = QVBoxLayout()
        self.v_grid1.addLayout(grid1)
        self.v_grid1.addLayout(grid_button1)
        self.v_gridWid1 = QWidget()
        self.v_gridWid1.setLayout(self.v_grid1)
        self.v_gridWid1.hide()
        
        
        self.v_tab1 = QVBoxLayout()
        self.body1 = QWidget()
        self.scrollArea1 = QScrollArea()
        self.scrollArea1.setContentsMargins(0,0,0,0)
        self.scrollArea1.setWidgetResizable(True)
        self.scrollArea1.setMaximumHeight(200)
        
        vin1 = g.selectn('stafffile', '' ,'', {'state':1, 'staffID':self.sid})
        self.hb1 = QVBoxLayout()
        self.body_arr1 = {}
        for v in vin1:
            st = v['startdate']
            en = v['enddate']
            damz = float(st)
            damt = datetime.utcfromtimestamp(damz).strftime('%b %Y')
            damz1 = float(en)
            damt1 = datetime.utcfromtimestamp(damz1).strftime('%b %Y')
            f1 = QLabel('<b>'+str(v['school']).upper()+'</b><br><i>'+str(v['degree']).upper()+' </i><span>'+str(v['course']).upper()+'</span> ('+str(v['grade']).upper() +')')
            f2 = QLabel(str(damt)+' ' + str(damt1)+'  ')
            f3 = QLabel('<hr>')
            
            nImg5 = Buttons().editButton()
            edt = QPushButton()
            edt.setFlat(True)
            edt.setIcon(QIcon(nImg5))
            edt.setMaximumHeight(10)
            edt.setMaximumWidth(10)
            
            nImg6 = Buttons().deleteButton()
            det = QPushButton()
            det.setFlat(True)
            det.setIcon(QIcon(nImg6))
            det.setMaximumHeight(10)
            det.setMaximumWidth(10)
            
            self.connect(edt, SIGNAL("clicked()"), lambda x = 1, y = v['id'] : self.button_edit(x, y))
            self.connect(det, SIGNAL("clicked()"), lambda x = 1, y = v['id']: self.button_delete(x, y))
            
            wh = QHBoxLayout()
            wh.addWidget(f2)
            wh.addWidget(edt)
            wh.addWidget(det)
            
            self.body_arr1[v['id']] = []
            self.body_arr1[v['id']].append(f1)
            self.body_arr1[v['id']].append(f2)
            self.body_arr1[v['id']].append(f3)
            self.body_arr1[v['id']].append(edt)
            self.body_arr1[v['id']].append(det)
            self.body_arr1[v['id']].append(wh)
            
            self.hb1.addWidget(f1)
            self.hb1.addLayout(wh)
            self.hb1.addWidget(f3)
            
        btn_layout1 = QHBoxLayout() 
        btn_layout1.addWidget(self.pbs1)
        btn_layout1.addWidget(self.pbp1)
        btn_layout1.addStretch()
        
        self.body1.setLayout(self.hb1)
        self.scrollArea1.setWidget(self.body1)
        
        self.v_tab1.addWidget(self.v_gridWid1)
        self.v_tab1.addLayout(btn_layout1)
        self.v_tab1.addWidget(self.scrollArea1)
        self.v_tab1.addStretch()

        #2
        self.v_grid2 = QVBoxLayout()
        self.v_grid2.addLayout(grid2)
        self.v_grid2.addLayout(grid_button2)
        self.v_gridWid2 = QWidget()
        self.v_gridWid2.setLayout(self.v_grid2)
        self.v_gridWid2.hide()
        
        
        self.v_tab2 = QVBoxLayout()
        self.body2 = QWidget()
        self.scrollArea2 = QScrollArea()
        self.scrollArea2.setContentsMargins(0,0,0,0)
        self.scrollArea2.setWidgetResizable(True)
        self.scrollArea2.setMaximumHeight(200)
        
        vin2 = g.selectn('stafffile', '' ,'', {'state':2, 'staffID':self.sid})
        self.hb2 = QVBoxLayout()
        for v in vin2:
            st = v['startdate']
            damz = float(st)
            damt = datetime.utcfromtimestamp(damz).strftime('%b %Y')
            f1 = QLabel('<b>'+str(v['course']).upper()+'</b> <i>'+str(v['school']).upper()+' </i> ('+ str(damt).upper() +')')
            f2 = QLabel(str(v['degree']))
            f3 = QLabel('<hr>')
            
            nImg5 = Buttons().editButton()
            edt = QPushButton()
            edt.setFlat(True)
            edt.setIcon(QIcon(nImg5))
            edt.setMaximumHeight(10)
            edt.setMaximumWidth(10)
            
            nImg6 = Buttons().deleteButton()
            det = QPushButton()
            det.setFlat(True)
            det.setIcon(QIcon(nImg6))
            det.setMaximumHeight(10)
            det.setMaximumWidth(10)
            
            self.connect(edt, SIGNAL("clicked()"), lambda x =2, y = v['id'] : self.button_edit(x, y))
            self.connect(det, SIGNAL("clicked()"), lambda x =2, y =  v['id']: self.button_delete(x, y))
            
            wh = QHBoxLayout()
            wh.addWidget(f2)
            wh.addWidget(edt)
            wh.addWidget(det)
            
            self.body_arr1[v['id']] = []
            self.body_arr1[v['id']].append(f1)
            self.body_arr1[v['id']].append(f2)
            self.body_arr1[v['id']].append(f3)
            self.body_arr1[v['id']].append(edt)
            self.body_arr1[v['id']].append(det)
            self.body_arr1[v['id']].append(wh)
            
            self.hb2.addWidget(f1)
            self.hb2.addLayout(wh)
            self.hb2.addWidget(f3)
            
        btn_layout2 = QHBoxLayout() 
        btn_layout2.addWidget(self.pbs2)
        btn_layout2.addWidget(self.pbp2)
        btn_layout2.addStretch()
        
        self.body2.setLayout(self.hb2)
        self.scrollArea2.setWidget(self.body2)
        
        self.v_tab2.addWidget(self.v_gridWid2)
        self.v_tab2.addLayout(btn_layout2)
        self.v_tab2.addWidget(self.scrollArea2)
        self.v_tab2.addStretch()

        #3
        self.v_grid3 = QVBoxLayout()
        self.v_grid3.addLayout(grid3)
        self.v_grid3.addLayout(grid_button3)
        self.v_gridWid3 = QWidget()
        self.v_gridWid3.setLayout(self.v_grid3)
        self.v_gridWid3.hide()
        
        self.v_tab3 = QVBoxLayout()
        self.body3 = QWidget()
        self.scrollArea3 = QScrollArea()
        self.scrollArea3.setContentsMargins(0,0,0,0)
        self.scrollArea3.setWidgetResizable(True)
        self.scrollArea3.setMaximumHeight(200)
        
        vin3 = g.selectn('stafffile', '' ,'', {'state':3, 'staffID':self.sid})
        self.hb3 = QVBoxLayout()
        for v in vin3:
            st = v['startdate']
            en = v['enddate']
            damz = float(st)
            damt = datetime.utcfromtimestamp(damz).strftime('%b %Y')
            damz1 = float(en)
            damt1 = datetime.utcfromtimestamp(damz1).strftime('%b %Y')
            f1 = QLabel('<b>'+str(v['school']).upper()+'</b><br><i>'+str(v['course']).upper()+' </i> ')
            f1x = QLabel(v['description'].encode('utf-8').strip())
            f1x.setWordWrap(True)
            f2 = QLabel(str(damt)+' ' + str(damt1)+'  ')
            f3 = QLabel('<hr>')
            
            nImg5 = Buttons().editButton()
            edt = QPushButton()
            edt.setFlat(True)
            edt.setIcon(QIcon(nImg5))
            edt.setMaximumHeight(10)
            edt.setMaximumWidth(10)
            
            nImg6 = Buttons().deleteButton()
            det = QPushButton()
            det.setFlat(True)
            det.setIcon(QIcon(nImg6))
            det.setMaximumHeight(10)
            det.setMaximumWidth(10)
            
            self.connect(edt, SIGNAL("clicked()"), lambda x = 3, y = v['id'] : self.button_edit(x, y))
            self.connect(det, SIGNAL("clicked()"), lambda x = 3, y=  v['id']: self.button_delete(x, y))
            
            wh = QHBoxLayout()
            wh.addWidget(f2)
            wh.addWidget(edt)
            wh.addWidget(det)
            
            self.body_arr1[v['id']] = []
            self.body_arr1[v['id']].append(f1)
            self.body_arr1[v['id']].append(f1x)
            self.body_arr1[v['id']].append(f2)
            self.body_arr1[v['id']].append(f3)
            self.body_arr1[v['id']].append(edt)
            self.body_arr1[v['id']].append(det)
            self.body_arr1[v['id']].append(wh)
            
            self.hb3.addWidget(f1)
            self.hb3.addWidget(f1x)
            self.hb3.addLayout(wh)
            self.hb3.addWidget(f3)
            
        btn_layout3 = QHBoxLayout() 
        btn_layout3.addWidget(self.pbs3)
        btn_layout3.addWidget(self.pbp3)
        btn_layout3.addStretch()
        
        self.body3.setLayout(self.hb3)
        self.scrollArea3.setWidget(self.body3)
        
        self.v_tab3.addWidget(self.v_gridWid3)
        self.v_tab3.addLayout(btn_layout3)
        self.v_tab3.addWidget(self.scrollArea3)
        self.v_tab3.addStretch()

        #4
        self.v_grid4 = QVBoxLayout()
        self.v_grid4.addLayout(grid4)
        self.v_grid4.addLayout(grid_button4)
        self.v_gridWid4 = QWidget()
        self.v_gridWid4.adjustSize()
        self.v_gridWid4.setLayout(self.v_grid4)
        self.v_gridWid4.hide()
        
        self.v_tab4 = QVBoxLayout()
        self.body4 = QWidget()
        self.scrollArea4 = QScrollArea()
        self.scrollArea4.setContentsMargins(0,0,0,0)
        self.scrollArea4.setWidgetResizable(True)
        self.scrollArea4.setMaximumHeight(200)
        
        vin4 = g.selectn('stafffile', '' ,'', {'state':4, 'staffID':self.sid})
        self.hb4 = QVBoxLayout()
        for v in vin4:
            st = v['startdate']
            en = v['enddate']
            damz = float(st)
            damt = datetime.utcfromtimestamp(damz).strftime('%b %Y')
            damz1 = float(en)
            damt1 = datetime.utcfromtimestamp(damz1).strftime('%b %Y')
            f1 = QLabel('<b>'+str(v['school']).upper()+'</b> <br><i>'+str(v['course']).upper()+' </i> ('+str(v['grade']).upper() +')')
            f1x = QLabel(v['description'].encode('utf-8').strip())
            f1x.setWordWrap(True)
            f2 = QLabel(str(damt)+' ' + str(damt1)+'  ')
            f3 = QLabel('<hr>')
            
            nImg5 = Buttons().editButton()
            edt = QPushButton()
            edt.setFlat(True)
            edt.setIcon(QIcon(nImg5))
            edt.setMaximumHeight(10)
            edt.setMaximumWidth(10)
            
            nImg6 = Buttons().deleteButton()
            det = QPushButton()
            det.setFlat(True)
            det.setIcon(QIcon(nImg6))
            det.setMaximumHeight(10)
            det.setMaximumWidth(10)
            
            self.connect(edt, SIGNAL("clicked()"), lambda x = 4, y = v['id'] : self.button_edit(x, y))
            self.connect(det, SIGNAL("clicked()"), lambda x = 4, y=  v['id']: self.button_delete(x, y))
            
            wh = QHBoxLayout()
            wh.addWidget(f2)
            wh.addWidget(edt)
            wh.addWidget(det)
            
            self.body_arr1[v['id']] = []
            self.body_arr1[v['id']].append(f1)
            self.body_arr1[v['id']].append(f1x)
            self.body_arr1[v['id']].append(f2)
            self.body_arr1[v['id']].append(f3)
            self.body_arr1[v['id']].append(edt)
            self.body_arr1[v['id']].append(det)
            self.body_arr1[v['id']].append(wh)
            
            self.hb4.addWidget(f1)
            self.hb4.addWidget(f1x)
            self.hb4.addLayout(wh)
            self.hb4.addWidget(f3)
            
        btn_layout4 = QHBoxLayout() 
        btn_layout4.addWidget(self.pbs4)
        btn_layout4.addWidget(self.pbp4)
        btn_layout4.addStretch()
        
        self.body4.setLayout(self.hb4)
        self.scrollArea4.setWidget(self.body4)
        
        self.v_tab4.addWidget(self.v_gridWid4)
        self.v_tab4.addLayout(btn_layout4)
        self.v_tab4.addWidget(self.scrollArea4)
        self.v_tab4.addStretch()

        #5
        self.v_grid5 = QVBoxLayout()
        self.v_grid5.addLayout(grid5)
        self.v_grid5.addLayout(grid_button5)
        self.v_gridWid5 = QWidget()
        self.v_gridWid5.setLayout(self.v_grid5)
        self.v_gridWid5.hide()
        
        self.v_tab5 = QVBoxLayout()
        self.body5 = QWidget()
        self.scrollArea5 = QScrollArea()
        self.scrollArea5.setContentsMargins(0,0,0,0)
        self.scrollArea5.setWidgetResizable(True)
        self.scrollArea5.setMaximumHeight(200)
        
        vin5 = g.selectn('stafffile', '' ,'', {'state':5, 'staffID':self.sid})
        self.hb5 = QVBoxLayout()
        for v in vin5:
            st = v['startdate']
            damz = float(st)
            damt = datetime.utcfromtimestamp(damz).strftime('%b %Y')
            f1 = QLabel(v['school'].encode('utf-8').strip())
            f1x = QLabel(v['course'].encode('utf-8').strip())
            f1.setWordWrap(True)
            f1x.setWordWrap(True)
            f2 = QLabel(str(v['degree'])+' ' + str(damt)+'  ')
            f3 = QLabel('<hr>')
            
            nImg5 = Buttons().editButton()
            edt = QPushButton()
            edt.setFlat(True)
            edt.setIcon(QIcon(nImg5))
            edt.setMaximumHeight(10)
            edt.setMaximumWidth(10)
            
            nImg6 = Buttons().deleteButton()
            det = QPushButton()
            det.setFlat(True)
            det.setIcon(QIcon(nImg6))
            det.setMaximumHeight(10)
            det.setMaximumWidth(10)
            
            self.connect(edt, SIGNAL("clicked()"), lambda x = 5, y = v['id'] : self.button_edit(x, y))
            self.connect(det, SIGNAL("clicked()"), lambda x = 5, y=  v['id']: self.button_delete(x, y))
            
            wh = QHBoxLayout()
            wh.addWidget(f2)
            wh.addWidget(edt)
            wh.addWidget(det)
            
            self.body_arr1[v['id']] = []
            self.body_arr1[v['id']].append(f1)
            self.body_arr1[v['id']].append(f1x)
            self.body_arr1[v['id']].append(f2)
            self.body_arr1[v['id']].append(f3)
            self.body_arr1[v['id']].append(edt)
            self.body_arr1[v['id']].append(det)
            self.body_arr1[v['id']].append(wh)
            
            self.hb5.addWidget(f1)
            self.hb5.addWidget(f1x)
            self.hb5.addLayout(wh)
            self.hb5.addWidget(f3)
            
        btn_layout5 = QHBoxLayout() 
        btn_layout5.addWidget(self.pbs5)
        btn_layout5.addWidget(self.pbp5)
        btn_layout5.addStretch()
        
        self.body5.setLayout(self.hb5)
        self.scrollArea5.setWidget(self.body5)
        
        self.v_tab5.addWidget(self.v_gridWid5)
        self.v_tab5.addLayout(btn_layout5)
        self.v_tab5.addWidget(self.scrollArea5)
        self.v_tab5.addStretch()

        #6
        self.v_grid6 = QVBoxLayout()
        self.v_grid6.addLayout(grid6)
        self.v_grid6.addLayout(grid_button6)
        self.v_gridWid6 = QWidget()
        self.v_gridWid6.setLayout(self.v_grid6)
        self.v_gridWid6.hide()
        
        self.v_tab6 = QVBoxLayout()
        self.body6 = QWidget()
        self.scrollArea6 = QScrollArea()
        self.scrollArea6.setContentsMargins(0,0,0,0)
        self.scrollArea6.setWidgetResizable(True)
        self.scrollArea6.setMaximumHeight(200)
        
        vin6 = g.selectn('stafffile', '' ,'', {'state':6, 'staffID':self.sid})
        self.hb6 = QVBoxLayout()
        for v in vin6:
            st = v['startdate']
            damz = float(st)
            damt = datetime.utcfromtimestamp(damz).strftime('%b %Y')
            f1 = QLabel(v['school'].encode('utf-8').strip())
            f1x = QLabel(v['course'].encode('utf-8').strip())
            f1.setWordWrap(True)
            f1x.setWordWrap(True)
            f2 = QLabel(str(v['degree'])+' ' + str(damt)+'  ')
            f3 = QLabel('<hr>')
            
            nImg5 = Buttons().editButton()
            edt = QPushButton()
            edt.setFlat(True)
            edt.setIcon(QIcon(nImg5))
            edt.setMaximumHeight(10)
            edt.setMaximumWidth(10)
            
            nImg6 = Buttons().deleteButton()
            det = QPushButton()
            det.setFlat(True)
            det.setIcon(QIcon(nImg6))
            det.setMaximumHeight(10)
            det.setMaximumWidth(10)
            
            self.connect(edt, SIGNAL("clicked()"), lambda x = 6, y = v['id'] : self.button_edit(x, y))
            self.connect(det, SIGNAL("clicked()"), lambda x = 6, y=  v['id']: self.button_delete(x, y))
            
            wh = QHBoxLayout()
            wh.addWidget(f2)
            wh.addWidget(edt)
            wh.addWidget(det)
            
            self.body_arr1[v['id']] = []
            self.body_arr1[v['id']].append(f1)
            self.body_arr1[v['id']].append(f1x)
            self.body_arr1[v['id']].append(f2)
            self.body_arr1[v['id']].append(f3)
            self.body_arr1[v['id']].append(edt)
            self.body_arr1[v['id']].append(det)
            self.body_arr1[v['id']].append(wh)
            
            self.hb6.addWidget(f1)
            self.hb6.addWidget(f1x)
            self.hb6.addLayout(wh)
            self.hb6.addWidget(f3)
            
        btn_layout6 = QHBoxLayout() 
        btn_layout6.addWidget(self.pbs6)
        btn_layout6.addWidget(self.pbp6)
        btn_layout6.addStretch()
        
        self.body6.setLayout(self.hb6)
        self.scrollArea6.setWidget(self.body6)
        
        self.v_tab6.addWidget(self.v_gridWid6)
        self.v_tab6.addLayout(btn_layout6)
        self.v_tab6.addWidget(self.scrollArea6)
        self.v_tab6.addStretch()

        #7
        self.v_grid7 = QVBoxLayout()
        self.v_grid7.addLayout(grid7)
        self.v_grid7.addLayout(grid_button7)
        self.v_gridWid7 = QWidget()
        self.v_gridWid7.setLayout(self.v_grid7)
        self.v_gridWid7.hide()
        
        self.v_tab7 = QVBoxLayout()
        self.body7 = QWidget()
        self.scrollArea7 = QScrollArea()
        self.scrollArea7.setContentsMargins(0,0,0,0)
        self.scrollArea7.setWidgetResizable(True)
        self.scrollArea7.setMaximumHeight(200)
        
        vin7 = g.selectn('stafffile', '' ,'', {'state':7, 'staffID':self.sid})
        self.hb7 = QVBoxLayout()
        for v in vin7:
            st = v['startdate']
            en = v['enddate']
            damz = float(st)
            damt = datetime.utcfromtimestamp(damz).strftime('%b %Y')
            damz1 = float(en)
            damt1 = datetime.utcfromtimestamp(damz1).strftime('%b %Y')
            f1 = QLabel('<b>'+str(v['school']).upper()+'</b><br><i>'+str(v['course']).upper()+' </i> ')
            f1x = QLabel(v['description'].encode('utf-8').strip())
            f1x.setWordWrap(True)
            f2 = QLabel(str(damt)+' ' + str(damt1)+'  ')
            f3 = QLabel('<hr>')
            
            nImg5 = Buttons().editButton()
            edt = QPushButton()
            edt.setFlat(True)
            edt.setIcon(QIcon(nImg5))
            edt.setMaximumHeight(10)
            edt.setMaximumWidth(10)
            
            nImg6 = Buttons().deleteButton()
            det = QPushButton()
            det.setFlat(True)
            det.setIcon(QIcon(nImg6))
            det.setMaximumHeight(10)
            det.setMaximumWidth(10)
            
            self.connect(edt, SIGNAL("clicked()"), lambda x = 7, y = v['id'] : self.button_edit(x, y))
            self.connect(det, SIGNAL("clicked()"), lambda x = 7, y=  v['id']: self.button_delete(x, y))
            
            wh = QHBoxLayout()
            wh.addWidget(f2)
            wh.addWidget(edt)
            wh.addWidget(det)
            
            self.body_arr1[v['id']] = []
            self.body_arr1[v['id']].append(f1)
            self.body_arr1[v['id']].append(f1x)
            self.body_arr1[v['id']].append(f2)
            self.body_arr1[v['id']].append(f3)
            self.body_arr1[v['id']].append(edt)
            self.body_arr1[v['id']].append(det)
            self.body_arr1[v['id']].append(wh)
            
            self.hb7.addWidget(f1)
            self.hb7.addWidget(f1x)
            self.hb7.addLayout(wh)
            self.hb7.addWidget(f3)
            
        btn_layout7 = QHBoxLayout() 
        btn_layout7.addWidget(self.pbs7)
        btn_layout7.addWidget(self.pbp7)
        btn_layout7.addStretch()
        
        self.body7.setLayout(self.hb7)
        self.scrollArea7.setWidget(self.body7)
        
        self.v_tab7.addWidget(self.v_gridWid7)
        self.v_tab7.addLayout(btn_layout7)
        self.v_tab7.addWidget(self.scrollArea7)
        self.v_tab7.addStretch()
        
        self.editAction = 0
        self.editID = 0
        #1
        self.pb1.clicked.connect(lambda:self.button_submit(1))
        self.pbc1.clicked.connect(lambda:self.button_min(1))
        self.pbs1.clicked.connect(lambda:self.button_max(1))
        #2
        self.pb2.clicked.connect(lambda:self.button_submit(2))
        self.pbc2.clicked.connect(lambda:self.button_min(2))
        self.pbs2.clicked.connect(lambda:self.button_max(2))
        #3
        self.pb3.clicked.connect(lambda:self.button_submit(3))
        self.pbc3.clicked.connect(lambda:self.button_min(3))
        self.pbs3.clicked.connect(lambda:self.button_max(3))
        #4
        self.pb4.clicked.connect(lambda:self.button_submit(4))
        self.pbc4.clicked.connect(lambda:self.button_min(4))
        self.pbs4.clicked.connect(lambda:self.button_max(4))
        #5
        self.pb5.clicked.connect(lambda:self.button_submit(5))
        self.pbc5.clicked.connect(lambda:self.button_min(5))
        self.pbs5.clicked.connect(lambda:self.button_max(5))
        #6
        self.pb6.clicked.connect(lambda:self.button_submit(6))
        self.pbc6.clicked.connect(lambda:self.button_min(6))
        self.pbs6.clicked.connect(lambda:self.button_max(6))
        #1
        self.pb7.clicked.connect(lambda:self.button_submit(7))
        self.pbc7.clicked.connect(lambda:self.button_min(7))
        self.pbs7.clicked.connect(lambda:self.button_max(7))
        
        
        
        self.tab1.setLayout(self.v_tab1)#academic
        self.tab2.setLayout(self.v_tab2)#professional
        self.tab3.setLayout(self.v_tab3)#work
        self.tab4.setLayout(self.v_tab4)#sponsored training/semiars
        self.tab5.setLayout(self.v_tab5)#Disciplne
        self.tab6.setLayout(self.v_tab6)#Commendation
        self.tab7.setLayout(self.v_tab7)#Duties/Resposibilities
        
        self.tabz.addTab(self.tab1, 'Academic')
        self.tabz.addTab(self.tab2, 'Professional')
        self.tabz.addTab(self.tab3, "Work Experience")
        self.tabz.addTab(self.tab4, "Trainings/Workshops")
        self.tabz.addTab(self.tab5, "Discipline")
        self.tabz.addTab(self.tab6, "Commendations")
        self.tabz.addTab(self.tab7, "Duties/Resposibilities")
        
        
        fullname = str(data['empno'])+" "+ str(data['surname']+" "+data['firstname']+" "+data['othername']).title()
        fullnameLbl = QLabel(fullname)
        fullnameLbl.setMaximumHeight(50)
        fullnameLbl.setFont(QFont("Candara", 14, QFont.Bold))
        addrLbl = QLabel('ADDRESS: '+data['addr'])
        phoneLbl = QLabel('PHONE: '+data['phone1']+' '+data['phone2'])
        emailLbl = QLabel('EMAIL: '+data['email'])
        statusLbl = QLabel('STATUS: IN-SERVICE')
        
        top_grid = QHBoxLayout()
        top_pics = QLabel()
        if os.path.isfile('./pic_thumb/'+str(data['pix'])):
            image1 = Image.open('pic_thumb/'+str(data['pix']))
        else:
            image1 = Image.open('img/stdpic.png')
        imageQ1 = ImageQt(image1)
        imagep1 = QPixmap(QPixmap.fromImage(QImage(imageQ1).scaled(100, 100, Qt.IgnoreAspectRatio)))
        top_pics.resize(100, 100)
        top_pics.setPixmap(imagep1)
        top_pics.setFixedHeight(100)
        top_pics.setFixedWidth(100)
        top_text = QVBoxLayout()
        top_text.addWidget(fullnameLbl)
        top_text.addWidget(addrLbl)
        top_text.addWidget(phoneLbl)
        top_text.addWidget(emailLbl)
        top_text.addWidget(statusLbl)
        top_grid.addLayout(top_text)
        top_grid.addWidget(top_pics)
        
        main_h = QVBoxLayout()
        main_h.addWidget(menu)
        main_h.addLayout(top_grid)
        main_h.addWidget(self.tabz)
        
        self.setLayout(main_h)
        self.setStyleSheet(stylesheet)
        self.setWindowIcon(QIcon(self.titleIcon))
        self.setWindowTitle(self.pagetitle)
        
    def button_edit(self, a, b):
        if a and a > 0:
            self.button_editrow(a, b)
    
    def button_delete(self, a, b):
        g = Db()
        g.delete('stafffile', {'id':b})
        self.button_remove(a, b)
           
    def button_remove(self, a, b):
        arr = self.body_arr1[b]
        for r in arr:
            try:
                if a == 1:
                    self.hb1.removeWidget(r)
                if a == 2:
                    self.hb2.removeWidget(r)
                if a == 3:
                    self.hb3.removeWidget(r)
                if a == 4:
                    self.hb4.removeWidget(r)
                if a == 5:
                    self.hb5.removeWidget(r)
                if a == 6:
                    self.hb6.removeWidget(r)
                if a == 7:
                    self.hb7.removeWidget(r)
            except:
                pass
            try:
                sip.delete(r)
            except:
                pass
            
            r = None
            
    def button_clear(self, a):
        self.button_min(a)
        if a == 1:
            self.schoolData.clear()
            self.courseData.clear()
            self.degreeData.clear()
            self.gradeData.clear()
            
        if a == 2:
            self.instituteData.clear()
            self.course1Data.clear()
            self.degree1Data.clear()
            
        if a == 3:
            self.companyData.clear()
            self.positionData.clear()
            self.jobData.clear()
        
        if a == 4:
            self.seminarData.clear()
            self.seminartitleData.clear()
            self.seminargradeData.clear()
            self.seminarcontentData.clear()
        
        if a == 5:
            self.act1Data.clear()
            self.react1Data.clear()
            self.supervisor1Data.clear()
        
        if a == 6:
            self.act2Data.clear()
            self.react2Data.clear()
            self.supervisor2Data.clear()
            
        if a == 7:
            self.groupData.clear()
            self.officeData.clear()
            self.mandateData.clear()
            
    def button_editrow(self, a, b):
        g = Db()
        data = g.selectn('stafffile', '', 1, {'id':b})
        self.button_max(a)
        if a == 1:
            self.editID = data['id']
            self.editAction = a
            self.schoolData.setText(data['school'])
            self.courseData.setText(data['course'])
            self.degreeData.setText(data['degree'])
            self.gradeData.setText(data['grade'])
        
        if a == 2:
            self.editID = data['id']
            self.editAction = a
            self.instituteData.setText(data['school'])
            self.course1Data.setText(data['course'])
            self.degree1Data.setText(data['degree'])
            
        if a == 3:
            self.editID = data['id']
            self.editAction = a
            self.companyData.setText(data['school'])
            self.positionData.setText(data['course'])
            self.jobData.insertPlainText(data['description'].encode('utf-8').strip())
            
        if a == 4:
            self.editID = data['id']
            self.editAction = a
            self.seminarData.setText(data['school'])
            self.seminartitleData.setText(data['course'])
            self.seminargradeData.setText(data['grade'])
            self.seminarcontentData.insertPlainText(data['description'].encode('utf-8').strip())
            
        if a == 5:
            self.editID = data['id']
            self.editAction = a
            self.act1Data.insertPlainText(data['school'].encode('utf-8').strip())
            self.react1Data.insertPlainText(data['course'].encode('utf-8').strip())
            self.supervisor1Data.setText(data['degree'])
            
        if a == 6:
            self.editID = data['id']
            self.editAction = a
            self.act2Data.insertPlainText(data['school'].encode('utf-8').strip())
            self.react2Data.insertPlainText(data['course'].encode('utf-8').strip())
            self.supervisor2Data.setText(data['degree'])
            
        if a == 7:
            self.editID = data['id']
            self.editAction = a
            self.groupData.setText(data['school'])
            self.officeData.setText(data['course'])
            self.mandateData.insertPlainText(data['description'].encode('utf-8').strip())
            
            
    def button_submit(self, a):
        arr = {}
        err = {}
        if a == 1:
            arr['school'] = self.schoolData.text()
            arr['course'] = self.courseData.text()
            arr['degree'] = self.degreeData.text()
            arr['grade'] = self.gradeData.text()
            _dates = self.startdateData.date().toPyDate()
            _dates = time.mktime(_dates.timetuple())
            arr['startdate'] = _dates
            _datee = self.enddateData.date().toPyDate()
            _datee = time.mktime(_datee.timetuple())
            arr['enddate'] = _datee
            arr['state'] = 1
            arr['staffID'] = self.sid
            #check
            if arr['school'] and len(arr['school']) > 0:
                pass
            else:
                err[1] = 1
            if arr['course'] and len(arr['course']) > 0:
                 pass
            else:
                err[2] = 'Course'
            if arr['degree'] and len(arr['degree']) > 0:
                 pass
            else:
                err[3] = 'Type of Degree'
        
        if a == 2:
            arr['school'] = self.instituteData.text()
            arr['course'] = self.course1Data.text()
            arr['degree'] = self.degree1Data.text()
            _dates = self.startdate1Data.date().toPyDate()
            _dates = time.mktime(_dates.timetuple())
            arr['startdate'] = _dates
            arr['state'] = 2
            arr['staffID'] = self.sid
            #check
            if arr['school'] and len(arr['school']) > 0:
                pass
            else:
                err[1] = 'Institute'
            if arr['course'] and len(arr['course']) > 0:
                 pass
            else:
                err[2] = 'Programme'
            if arr['degree'] and len(arr['degree']) > 0:
                 pass
            else:
                err[3] = 'Grade'
        
        if a == 3:
            arr['school'] = self.companyData.text()
            arr['course'] = self.positionData.text()
            arr['description'] = self.jobData.toPlainText().encode('utf-8').strip()
            _dates = self.startdateData.date().toPyDate()
            _dates = time.mktime(_dates.timetuple())
            arr['startdate'] = _dates
            _datee = self.enddateData.date().toPyDate()
            _datee = time.mktime(_datee.timetuple())
            arr['enddate'] = _datee
            arr['state'] = a
            arr['staffID'] = self.sid
            #check
            if arr['school'] and len(arr['school']) > 0:
                pass
            else:
                err[1] = 1
            if arr['course'] and len(arr['course']) > 0:
                 pass
            else:
                err[2] = 'Course'
       
        if a == 4:
            arr['school'] = self.seminarData.text()
            arr['course'] = self.seminartitleData.text()
            arr['description'] = self.seminarcontentData.toPlainText().encode('utf-8').strip()
            arr['grade'] = self.seminargradeData.text()
            _dates = self.startdate3Data.date().toPyDate()
            _dates = time.mktime(_dates.timetuple())
            arr['startdate'] = _dates
            _datee = self.enddate3Data.date().toPyDate()
            _datee = time.mktime(_datee.timetuple())
            arr['enddate'] = _datee
            arr['state'] = 4
            arr['staffID'] = self.sid
            #check
            if arr['school'] and len(arr['school']) > 0:
                pass
            else:
                err[1] = 'Organized by'
            if arr['course'] and len(arr['course']) > 0:
                 pass
            else:
                err[2] = 'Title'
                
        if a == 5:
            arr['school'] = self.act1Data.toPlainText().encode('utf-8').strip()
            arr['course'] = self.react1Data.toPlainText().encode('utf-8').strip()
            arr['degree'] = self.supervisor1Data.text()
            _dates = self.startdate4Data.date().toPyDate()
            _dates = time.mktime(_dates.timetuple())
            arr['startdate'] = _dates
            arr['state'] = a
            arr['staffID'] = self.sid
            #check
            if arr['school'] and len(arr['school']) > 0:
                pass
            else:
                err[1] = 'State Offence'
            if arr['course'] and len(arr['course']) > 0:
                 pass
            else:
                err[2] = 'Disciplinary Action'
            if arr['degree'] and len(arr['degree']) > 0:
                 pass
            else:
                err[3] = 'Issued By:'
                
        if a == 6:
            arr['school'] = self.act2Data.toPlainText().encode('utf-8').strip()
            arr['course'] = self.react2Data.toPlainText().encode('utf-8').strip()
            arr['degree'] = self.supervisor2Data.text()
            _dates = self.startdate5Data.date().toPyDate()
            _dates = time.mktime(_dates.timetuple())
            arr['startdate'] = _dates
            arr['state'] = a
            arr['staffID'] = self.sid
            #check
            if arr['school'] and len(arr['school']) > 0:
                pass
            else:
                err[1] = 'Commendable Action'
            if arr['course'] and len(arr['course']) > 0:
                 pass
            else:
                err[2] = 'Award, Reward'
            if arr['degree'] and len(arr['degree']) > 0:
                 pass
            else:
                err[3] = 'Issued By'
            
        if a == 7:
            arr['school'] = self.groupData.text()
            arr['course'] = self.officeData.text()
            arr['description'] = self.mandateData.toPlainText().encode('utf-8').strip()
            _dates = self.startdate6Data.date().toPyDate()
            _dates = time.mktime(_dates.timetuple())
            arr['startdate'] = _dates
            _datee = self.enddate6Data.date().toPyDate()
            _datee = time.mktime(_datee.timetuple())
            arr['enddate'] = _datee
            arr['state'] = a
            arr['staffID'] = self.sid
            #check
            if arr['school'] and len(arr['school']) > 0:
                pass
            else:
                err[1] = 'Team/Group/Committee'
            if arr['course'] and len(arr['course']) > 0:
                 pass
            else:
                err[2] = 'Course'
            
                
        if len(err) > 0:
            #error
            pass
        else:
            self.post(a, arr)
            
    def post(self, a, arr):
        g = Db()
        db = 'stafffile'
        if self.editID == 0:
            h = g.insert(db, arr)
        elif self.editID > 0:
            g.update(db, arr, {'id':self.editID})
            h = self.editID
            self.editID = 0
            self.editAction = 0
            self.button_remove(a, h)
            
        if h and h > 0:
            self.reloads(a, h)
            self.button_clear(a)
            
      
    def button_min(self, a):
        if a == 1:
            self.v_gridWid1.hide()
            self.pbs1.show()
        if a == 2:
            self.v_gridWid2.hide()
            self.pbs2.show()
        if a == 3:
            self.v_gridWid3.hide()
            self.pbs3.show()
        if a == 4:
            self.v_gridWid4.hide()
            self.pbs4.show()
        if a == 5:
            self.v_gridWid5.hide()
            self.pbs5.show()
        if a == 6:
            self.v_gridWid6.hide()
            self.pbs6.show()
        if a == 7:
            self.v_gridWid7.hide()
            self.pbs7.show()
        
    def button_max(self, a):
        if a == 1:
            self.v_gridWid1.show()
            self.pbs1.hide()
        if a == 2:
            self.v_gridWid2.show()
            self.pbs2.hide()
        if a == 3:
            self.v_gridWid3.show()
            self.pbs3.hide()
        if a == 4:
            self.v_gridWid4.show()
            self.pbs4.hide()
        if a == 5:
            self.v_gridWid5.show()
            self.pbs5.hide()
        if a == 6:
            self.v_gridWid6.show()
            self.pbs6.hide()
        if a == 7:
            self.v_gridWid7.show()
            self.pbs7.hide()
        
    def reload_data(self, a):
        pass
        
    def reloads(self, a, b):
        g = Db()
        v = g.selectn('stafffile', '' , 1, {'id': b})
        
        if a == 1:
            st = v['startdate']
            en = v['enddate']
            damz = float(st)
            damt = datetime.utcfromtimestamp(damz).strftime('%b %Y')
            damz1 = float(en)
            damt1 = datetime.utcfromtimestamp(damz1).strftime('%b %Y')
            f1 = QLabel('<b>'+str(v['school']).upper()+'</b><br><i>'+str(v['degree']).upper()+' </i><span>'+str(v['course']).upper()+'</span> ('+str(v['grade']).upper() +')')
            f2 = QLabel(str(damt)+' ' + str(damt1)+'  ')
            f3 = QLabel('<hr>')
        
        if a == 2:
            st = v['startdate']
            damz = float(st)
            damt = datetime.utcfromtimestamp(damz).strftime('%b %Y')
            f1 = QLabel('<b>'+str(v['course']).upper()+'</b> <i>'+str(v['school']).upper()+' </i> ('+ str(damt) +')')
            f2 = QLabel(str(v['degree']))
            f3 = QLabel('<hr>')
            
        if a == 3:
            st = v['startdate']
            en = v['enddate']
            damz = float(st)
            damt = datetime.utcfromtimestamp(damz).strftime('%b %Y')
            damz1 = float(en)
            damt1 = datetime.utcfromtimestamp(damz1).strftime('%b %Y')
            f1 = QLabel('<b>'+str(v['school']).upper()+'</b><br><i>'+str(v['course']).upper()+' </i>')
            f1x = QPlainTextEdit(v['description'])
            f2 = QLabel(str(damt)+' ' + str(damt1)+'  ')
            f3 = QLabel('<hr>')
        
        if a == 4:
            st = v['startdate']
            en = v['enddate']
            damz = float(st)
            damt = datetime.utcfromtimestamp(damz).strftime('%b %Y')
            damz1 = float(en)
            damt1 = datetime.utcfromtimestamp(damz1).strftime('%b %Y')
            f1 = QLabel('<b>'+str(v['school']).upper()+'</b> <br><i>'+str(v['course']).upper()+' </i> ('+str(v['grade']).upper() +')')
            f1x = QPlainTextEdit(v['description'])
            f2 = QLabel(str(damt)+' ' + str(damt1)+'  ')
            f3 = QLabel('<hr>')
            
        if a == 5:
            st = v['startdate']
            damz = float(st)
            damt = datetime.utcfromtimestamp(damz).strftime('%b %Y')
            f1 = QPlainTextEdit(v['school'])
            f1x = QPlainTextEdit(v['course'])
            f2 = QLabel(str(v['degree'])+' ' + str(damt)+'  ')
            f3 = QLabel('<hr>')
            
        if a == 6:
            st = v['startdate']
            damz = float(st)
            damt = datetime.utcfromtimestamp(damz).strftime('%b %Y')
            f1 = QPlainTextEdit(v['school'])
            f1x = QPlainTextEdit(v['course'])
            f2 = QLabel(str(v['degree'])+' ' + str(damt)+'  ')
            f3 = QLabel('<hr>')
            
        if a == 7:
            st = v['startdate']
            en = v['enddate']
            damz = float(st)
            damt = datetime.utcfromtimestamp(damz).strftime('%b %Y')
            damz1 = float(en)
            damt1 = datetime.utcfromtimestamp(damz1).strftime('%b %Y')
            f1 = QLabel('<b>'+str(v['school']).upper()+'</b><br><i>'+str(v['course']).upper()+' </i> ')
            f1x = QPlainTextEdit(v['description'])
            f2 = QLabel(str(damt)+' ' + str(damt1)+'  ')
            f3 = QLabel('<hr>')
            
        nImg5 = Buttons().editButton()
        edt = QPushButton()
        edt.setFlat(True)
        edt.setIcon(QIcon(nImg5))
        edt.setMaximumHeight(10)
        edt.setMaximumWidth(10)
        
        nImg6 = Buttons().deleteButton()
        det = QPushButton()
        det.setFlat(True)
        det.setIcon(QIcon(nImg6))
        det.setMaximumHeight(10)
        det.setMaximumWidth(10)
        
        self.connect(edt, SIGNAL("clicked()"), lambda x =2, y = v['id']: self.button_edit(x, y))
        self.connect(det, SIGNAL("clicked()"), lambda x =2, y = v['id']: self.button_delete(x, y))
        
        wh = QHBoxLayout()
        wh.addWidget(f2)
        wh.addWidget(edt)
        wh.addWidget(det)
        
        self.body_arr1[v['id']] = []
        self.body_arr1[v['id']].append(f1)
        self.body_arr1[v['id']].append(f2)
        self.body_arr1[v['id']].append(f3)
        self.body_arr1[v['id']].append(edt)
        self.body_arr1[v['id']].append(det)
        self.body_arr1[v['id']].append(wh)
        
        if a == 1:
            self.hb1.addWidget(f1)
            self.hb1.addLayout(wh)
            self.hb1.addWidget(f3)
        if a == 2:
            self.hb2.addWidget(f1)
            self.hb2.addLayout(wh)
            self.hb2.addWidget(f3)
        if a == 3:
            self.body_arr1[v['id']].append(f1x)
            self.hb3.addWidget(f1)
            self.hb3.addWidget(f1x)
            self.hb3.addLayout(wh)
            self.hb3.addWidget(f3)
        if a == 4:
            self.body_arr1[v['id']].append(f1x)
            self.hb4.addWidget(f1)
            self.hb4.addWidget(f1x)
            self.hb4.addLayout(wh)
            self.hb4.addWidget(f3)
        if a == 5:
            self.body_arr1[v['id']].append(f1x)
            self.hb5.addWidget(f1)
            self.hb5.addWidget(f1x)
            self.hb5.addLayout(wh)
            self.hb5.addWidget(f3)
        if a == 6:
            self.body_arr1[v['id']].append(f1x)
            self.hb6.addWidget(f1)
            self.hb6.addWidget(f1x)
            self.hb6.addLayout(wh)
            self.hb6.addWidget(f3)
        if a == 7:
            self.body_arr1[v['id']].append(f1x)
            self.hb7.addWidget(f1)
            self.hb7.addWidget(f1x)
            self.hb7.addLayout(wh)
            self.hb7.addWidget(f3)
       
    def menuUi(self):
        extractQuit = QAction(self) 
        extractQuit.setStatusTip('File')
          
        mainMenu = QMenuBar()
        
        fileMenu = mainMenu.addMenu('&File')
        exitMenu = QAction('&Exit', self)
        exitMenu.setShortcut('CTRL+Q')
        exitMenu.setStatusTip('Close Dialog')
        #exitMenu.triggered.connect(self.lunchUnitForm)
        fileMenu.addAction(exitMenu)
    
        editMenu = mainMenu.addMenu('Edit')
        editBioMenu = QAction('Bio-Data and Contact Information', self)
        editBioMenu.setStatusTip('Bio-Data & Contact Information')
        editMenu.addAction(editBioMenu)
    
        editAccessMenu = QAction('Access', self)
        editAccessMenu.setStatusTip('Control information a staff can manage')
        editMenu.addAction(editAccessMenu)
        
        printMenu = mainMenu.addMenu('Print')
        printBioMenu = QAction('Bio-Data & Contact Information', self)
        printBioMenu.setStatusTip('Print Bio-Data and Contact Information')
        printBioMenu.triggered.connect(lambda x = 1: self.lunchPrint(x))
        printMenu.addAction(printBioMenu)
        
        printAcaMenu = QAction('Academic', self)
        printAcaMenu.setStatusTip('Print Academic History')
        printAcaMenu.triggered.connect(lambda x = 2: self.lunchPrint(x))
        printMenu.addAction(printAcaMenu)
        
        printProMenu = QAction('Professional History', self)
        printProMenu.setStatusTip('Print Professional Data')
        printProMenu.triggered.connect(lambda x = 3: self.lunchPrint(x))
        printMenu.addAction(printProMenu)
        
        printWrkMenu = QAction('Past Working Experience', self)
        printWrkMenu.setStatusTip('Print Past Work History')
        printWrkMenu.triggered.connect(lambda x = 4: self.lunchPrint(x))
        printMenu.addAction(printWrkMenu)
        
        printTrnMenu = QAction('Workshops & Seminars', self)
        printTrnMenu.setStatusTip('Print Workshops/Seminar Attended')
        printTrnMenu.triggered.connect(lambda x = 5: self.lunchPrint(x))
        printMenu.addAction(printTrnMenu)
        
        printComMenu = QAction('Commendations/Awards', self)
        printComMenu.setStatusTip('Print all commendations $ Awards')
        printComMenu.triggered.connect(lambda x = 6: self.lunchPrint(x))
        printMenu.addAction(printComMenu)
        
        printDutMenu = QAction('Current Duties & Responsibilitites', self)
        printDutMenu.setStatusTip('Print Current Duties & Responsibilitites')
        printDutMenu.triggered.connect(lambda x = 7: self.lunchPrint(x))
        printMenu.addAction(printDutMenu)
        
        printDut1Menu = QAction('All Duties & Responsibilities', self)
        printDut1Menu.setStatusTip('print all Duties & Responsibilities, both Past and present')
        printDut1Menu.triggered.connect(lambda x = 8: self.lunchPrint(x))
        printMenu.addAction(printDut1Menu)
        
        printCusMenu = QAction('Customize Selection', self)
        printCusMenu.setStatusTip('Print Selected Items')
        printCusMenu.triggered.connect(lambda x = 9: self.lunchPrint(x))
        printMenu.addAction(printCusMenu)
    
        printAllMenu = QAction('All', self)
        printAllMenu.setStatusTip('Print all')
        printAllMenu.triggered.connect(lambda x = 10: self.lunchPrint(x))
        printMenu.addAction(printAllMenu)
        
        return mainMenu
        
    def lunchPrint(self, a):
        pass
        
class StaffAccess(QDialog):
    
    def __init__(self, parent=None):
       super(StaffAccess, self).__init__(parent)
       stylesheet = Valid().background() + Valid().font()
       self.pagetitle = 'Staff'
       self.titleIcon = ''
       self.sid = 23
       g = Db()
       clasz = g.selectn('datas','', '', {'pubID':1, 'active':0})
       
       main = {}
       main[1] = {}
       main[1]['name'] = 'Settings'
       main[1]['data'] = {}
       main[1]['data'][30] = 'Session & Term'
       main[1]['data'][1] = 'Class'
       main[1]['data'][3] = 'Subject'
       main[1]['data'][20] = 'Accounts'
       main[1]['data'][15] = 'Expenses'
       main[1]['data'][23] = 'Stock'
       main[1]['data'][17] = 'Fees'
       main[1]['data'][11] = 'Affective'
       main[1]['data'][9] = 'Psychomotor'
       main[1]['data'][7] = 'Assessments'
       main[1]['data'][27] = 'Departments'
       main[1]['data'][28] = 'Pension Managers'
       
       main[2] = {}
       main[2]['name'] = 'Students'
       main[2]['datas'] = {}
       for s in clasz:
           f = g.selectn('datas', '', '', {'subID':s['id']})
           for c in f:
               main[2]['datas'][c['id']] = {}
               main[2]['datas'][c['id']]['name'] = str(s['abbrv'])+' '+str(c['abbrv']) 
               main[2]['datas'][c['id']]['data'] = {}
               main[2]['datas'][c['id']]['data'][1] = 'Bio-Data'
               main[2]['datas'][c['id']]['data'][2] = 'Academic'
               main[2]['datas'][c['id']]['data'][3] = 'Psychomotor'
               main[2]['datas'][c['id']]['data'][4] = 'Affective'
               main[2]['datas'][c['id']]['data'][5] = 'Fees'
       
       
       main[3] = {}
       main[3]['name'] = 'Staff'
       main[3]['data'] = {}
        
         #items
       self.tree = QTreeWidget()
       self.tree.setHeaderLabel("Access")
       self.tree.headerItem().setText(0, 'Name')
       self.tree.headerItem().setText(1, 'View')
       self.tree.headerItem().setText(2, 'Add.Edit')
       self.tree.headerItem().setText(3, 'Delete')
       
       
       for a in main:
           child = QTreeWidgetItem(self.tree)
           child.setFlags(child.flags() | Qt.ItemIsTristate | Qt.ItemIsUserCheckable)
           child.setText(0, str(main[a]['name']))
           child.setCheckState(1, Qt.Checked)
           child.setCheckState(2, Qt.Checked)
           child.setCheckState(3, Qt.Checked)
           if 'data' in main[a]:
               for b in main[a]['data']:
                   child1 = QTreeWidgetItem(child)
                   child1.setFlags(child1.flags() | Qt.ItemIsTristate | Qt.ItemIsUserCheckable)
                   child1.setText(0, str(main[a]['data'][b]))
                   child1.setCheckState(1, Qt.Checked)
                   child1.setCheckState(2, Qt.Checked)
                   child1.setCheckState(3, Qt.Checked)
           if 'datas' in main[a]:
               for b in main[a]['datas']:
                   child1 = QTreeWidgetItem(child)
                   child1.setFlags(child1.flags() | Qt.ItemIsTristate | Qt.ItemIsUserCheckable)
                   child1.setText(0, str(main[a]['datas'][b]['name']))
                   child1.setCheckState(1, Qt.Checked)
                   child1.setCheckState(2, Qt.Checked)
                   child1.setCheckState(3, Qt.Checked)
                   if 'data' in main[a]['datas'][b]:
                       for c in main[a]['datas'][b]['data']:
                           child2 = QTreeWidgetItem(child1)
                           child2.setFlags(child2.flags() | Qt.ItemIsTristate | Qt.ItemIsUserCheckable)
                           child2.setText(0, str(main[a]['datas'][b]['data'][c]))
                           child2.setCheckState(1, Qt.Checked)
                           child2.setCheckState(2, Qt.Checked)
                           child2.setCheckState(3, Qt.Checked)
   
       
       
       
       self.pb = QPushButton()
       self.pb.setObjectName("Submit")
       self.pb.setText("Submit")
        
       self.pb1 = QPushButton()
       self.pb1.setObjectName("Cancel")
       self.pb1.setText("Cancel")
       
       grid_button = QGridLayout()
       grid_button.addWidget(self.pb,0,0)
       grid_button.addWidget(self.pb1,0,1)
       
       main_h = QVBoxLayout()
       main_h.addWidget(self.tree)
       main_h.addLayout(grid_button)
       
       self.pb.clicked.connect(lambda:self.button1_click())
       self.pb1.clicked.connect(lambda:self.button1_click())
       
       self.setLayout(main_h)
       self.setStyleSheet(stylesheet)
       self.setWindowIcon(QIcon(self.titleIcon))
       self.setWindowTitle(self.pagetitle)
        
       
        
        
        
        
