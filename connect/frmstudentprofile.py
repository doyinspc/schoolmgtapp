# -*- coding: utf-8 -*-
"""
Created on Sat Nov 17 05:44:29 2018

@author: CHARLES
"""
from PyQt4.QtCore import SIGNAL, QDate, Qt, QSize
from PyQt4.QtGui import  QPrintPreviewDialog, QLayout, QScrollArea, QMenuBar, QAction, QStackedWidget, QFont, QWidget, QSplitter, QFileDialog, QPixmap, QTabWidget, QComboBox, QRadioButton, QDateEdit, QTextEdit, QCheckBox, QHBoxLayout, QGroupBox, QGridLayout, QDialog, QApplication, QPushButton, QLineEdit, QFormLayout, QLabel, QVBoxLayout, QSizePolicy
from connect import Db
from connectstudents import Con
from datetime import datetime
from jinja2 import Template
from dateutil.relativedelta import relativedelta
import cv2
import datetime
import math
import numpy as np

class StudentProfile(QDialog):
    
    def __init__(self, sids, es, parent=None):
        super(StudentProfile, self).__init__(parent)
      
        red = 50 + es
        reds = 50 + es
        
        self.setGeometry(red, reds, 700, 700)
        self.textStyle = "background-color: white; color:black; border: 3px ridge #ccc"
        self.minW = 670
        self.maxW = 700
        
        self.sid = sids
        self.student =  sids
        cn = Db()
        self.myterms = cn.getTermClass(self.sid)
        menu = self.menuUi()
        data = self.pullStudents(self.sid)
        
        fullnamex = data['surname']+' '+data['firstname']+' '+data['othername']
        self.fullname = fullnamex.title()
        self.schno = str(data['schno']).upper()
        
        if data['gender'] == 0:
            self.gender = 'Male'
        elif data['gender'] == 1:
            self.gender = 'Female'
        else:
            self.gender = 'None Stated'
         
        now = datetime.datetime.today()
        
        dob = data['dob']
        dt = datetime.datetime.strptime(dob, '%d/%m/%Y').date()
        dt1 = now.date()
        diff = (dt1 - dt).days   
        age1 = int(diff)/365.25
        agey = round(int(diff)/365.25, 0)
        agem = age1 - agey
        months = round(agem * 12)
        self.dob = "{:%d, %b %Y}".format(dt)
        self.age = str(math.floor(agey))+' yrs '+str(math.floor(months))+' months '
        
        admit = data['admit']
        dt2 = datetime.datetime.strptime(admit, '%d/%m/%Y').date()
        dt3 = now.date()
        diff1 = (dt3 - dt2).days
        admit1 = int(diff1)/365.25
        admity = round(int(diff1)/365.25, 0)
        admitm = admit1 - admity
        amonths = round(admitm * 12)
        self.admit = "{:%d, %b %Y}".format(dt2)
        self.admit_dur = str(math.floor(admity))+' yrs '+str(math.floor(amonths))+' months '
        
        self.data = data
        
        self.h1_box = QVBoxLayout()
        self.h2_box = QVBoxLayout()
        self.h3_box = QVBoxLayout()
        self.h4_box = QVBoxLayout()
        self.h5_box = QVBoxLayout()
        
        self.profileStack = QStackedWidget()
        
        bioText = QTextEdit(self)
        bioText.setMinimumWidth(self.minW)
        bioText.setMinimumHeight(self.maxW)
        bioText.setMaximumHeight(self.maxW)
        btext = self.buildBio()
        bioText.insertHtml(btext)
        bioText.setStyleSheet(self.textStyle)
        self.profileStack.setCurrentIndex(0)
        self.h1_box.addWidget(bioText)
        self.h1_box.setSizeConstraint(QLayout.SetFixedSize)
        self.doc1 = bioText
        
        self.academicText = QTextEdit()
        self.academicText.setMinimumWidth(self.minW)
        self.academicText.setMinimumHeight(self.maxW)
        self.academicText.setMaximumHeight(self.maxW)
        actext = self.buildBio()
        self.academicText.insertHtml(actext)
        self.academicText.setStyleSheet(self.textStyle)
        self.h2_box.addWidget(self.academicText)
        self.h2_box.setSizeConstraint(QLayout.SetFixedSize)
        self.doc2 = self.academicText
        
        self.affectiveText = QTextEdit()
        self.affectiveText.setMinimumWidth(self.minW)
        self.affectiveText.setMinimumHeight(self.maxW)
        self.affectiveText.setMaximumHeight(self.maxW)
        aftext = self.buildBio()
        self.affectiveText.insertHtml(aftext)
        self.affectiveText.setStyleSheet(self.textStyle)
        self.h3_box.addWidget(self.affectiveText)
        self.h3_box.setSizeConstraint(QLayout.SetFixedSize)
        self.doc3 = self.affectiveText
        
        self.psychomotorText = QTextEdit()
        self.psychomotorText.setMinimumWidth(self.minW)
        self.psychomotorText.setMinimumHeight(self.maxW)
        self.psychomotorText.setMaximumHeight(self.maxW)
        pstext = self.buildBio()
        self.psychomotorText.insertHtml(pstext)
        self.psychomotorText.setStyleSheet(self.textStyle)
        self.h4_box.addWidget(self.psychomotorText)
        self.h4_box.setSizeConstraint(QLayout.SetFixedSize)
        self.doc4 = self.psychomotorText
        
        self.feeText = QTextEdit()
        self.feeText.setMinimumWidth(self.minW)
        self.feeText.setMinimumHeight(self.maxW)
        self.feeText.setMaximumHeight(self.maxW)
        fetext = self.buildBio()
        self.feeText.insertHtml(fetext)
        self.feeText.setStyleSheet(self.textStyle)
        self.h5_box.addWidget(self.feeText)
        self.h5_box.setSizeConstraint(QLayout.SetFixedSize)
        self.doc5 = self.feeText
        
        scrollArea = QScrollArea(self)
        scrollArea.setWidgetResizable(True)
        scrollArea.setFixedHeight(700)
        scrollArea.setFixedWidth(700)
        
        bioProfileWidget = QWidget()
        academicProfileWidget = QWidget()
        affectiveProfileWidget = QWidget()
        psychomotorProfileWidget = QWidget()
        feeProfileWidget = QWidget()
             
        self.profileStack.addWidget(bioProfileWidget)
        self.profileStack.addWidget(academicProfileWidget)
        self.profileStack.addWidget(affectiveProfileWidget)
        self.profileStack.addWidget(psychomotorProfileWidget)
        self.profileStack.addWidget(feeProfileWidget)
        
        bioProfileWidget.setLayout(self.h1_box)
        academicProfileWidget.setLayout(self.h2_box)
        affectiveProfileWidget.setLayout(self.h3_box)
        psychomotorProfileWidget.setLayout(self.h4_box)
        feeProfileWidget.setLayout(self.h5_box)
        #Main layout
        Hbox = QVBoxLayout()
        Hbox.addWidget(menu)
        Hbox.addStretch()
        Hbox.addWidget(self.profileStack)
        Hbox.setContentsMargins(0, 0, 0, 0)
       
        #Create central widget, add layout and set
        central_widget = QWidget(scrollArea)
        scrollArea.setWidget(central_widget)
        central_widget.setContentsMargins(0, 0, 0, 0)
        central_widget.setGeometry(0, 0, 650, 700)
        central_widget.setStyleSheet("background-color: #ccc; color:#000")
        central_widget.setLayout(Hbox)
       
        self.setWindowTitle(fullnamex.title())
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
    
    def pullResults(self, term):
        cn = Db()
        students = cn.selectn('datas', '' , '', {'subID':term, 'pubID':'rep'})
        return students
    
    def pullResult(self, row):
        cn = Db()
        students = cn.selectn('datas', '' , 1, {'id':row})
        return students
    
    def pullStudents(self, a):
        self.a = a
        cn = Db()
        students = cn.selectn('students', '' , 1, {'id':self.a})
        return students
    
    def lunchUnitForm(self, a):
        self.a = a
        
    def lunchPrintForm(self, a):
        self.item = a
        self.lunchPrintPreview()
        #form.exec_()
        
    def handlePaintRequest(self, printer):
        _item = self.item
        if _item == 1:
            document = self.doc1
        elif _item == 2:
            document = self.doc1
        elif _item == 3:
            document = self.doc1
        elif _item == 4:
            document = self.doc1
        else:
            document = None
        
        if document != None:
            document.print_(printer)
            
    def lunchReport(self, a, b, c = None):
        _item = a
        if _item == 1:
            self.profileStack.setCurrentIndex(0)
            self.bioText = QTextEdit()
            self.bioText.setMinimumWidth(self.minW)
            self.bioText.setMinimumHeight(self.maxW)
            self.bioText.setMaximumHeight(self.maxW)
            btext = self.buildBio()
            self.bioText.insertHtml(btext)
            self.bioText.setStyleSheet(self.textStyle)
        elif _item == 2:
            self.profileStack.setCurrentIndex(1)
            self.academicText.close()
            self.academicText = QTextEdit()
            self.academicText.setMinimumWidth(self.minW)
            self.academicText.setMinimumHeight(self.maxW)
            self.academicText.setMaximumHeight(self.maxW)
            actext = self.buildAca(b, c)
            self.academicText.insertHtml(actext)
            self.academicText.setStyleSheet(self.textStyle)
            self.h2_box.addWidget(self.academicText)
            self.academicText.show()
        elif _item == 3:
            self.profileStack.setCurrentIndex(2)
            self.affectiveText.close()
            self.affectiveText = QTextEdit()
            self.affectiveText.setMinimumWidth(self.minW)
            self.affectiveText.setMinimumHeight(self.maxW)
            self.affectiveText.setMaximumHeight(self.maxW)
            aftext = self.buildAff(b)
            self.affectiveText.insertHtml(aftext)
            self.affectiveText.setStyleSheet(self.textStyle)
        elif _item == 4:
            self.profileStack.setCurrentIndex(3)
            self.psychomotorText.close()
            self.psychomotorText = QTextEdit()
            self.psychomotorText.setMinimumWidth(self.minW)
            self.psychomotorText.setMinimumHeight(self.maxW)
            self.psychomotorText.setMaximumHeight(self.maxW)
            pstext = self.buildPsy(b)
            self.psychomotorText.insertHtml(pstext)
            self.psychomotorText.setStyleSheet(self.textStyle)
        elif _item == 5:
            self.profileStack.setCurrentIndex(4)
            self.feeText.close()
            self.feeText = QTextEdit()
            self.feeText.setMinimumWidth(self.minW)
            self.feeText.setMinimumHeight(self.maxW)
            self.feeText.setMaximumHeight(self.maxW)
            fetext = self.buildFee(b)
            self.feeText.insertHtml(fetext)
            self.feeText.setStyleSheet(self.textStyle)
        else:
            self.profileStack.setCurrentIndex(0)

            
        
    def lunchPrintPreview(self):
        dialog = QPrintPreviewDialog()
        dialog.paintRequested.connect(self.handlePaintRequest)
        dialog.exec_()
        
    def menuUi(self):
        extractQuit = QAction(self) 
        extractQuit.setStatusTip('File')
          
        mainMenu = QMenuBar()
        
        fileMenu = mainMenu.addMenu('&File')
        exitMenu = QAction('&Exit', self)
        exitMenu.setShortcut('CTRL+Q')
        exitMenu.setStatusTip('Close Dialog')
        exitMenu.triggered.connect(self.lunchUnitForm)
        fileMenu.addAction(exitMenu)
    
        #settings menu
        ViewMenu = mainMenu.addMenu('&Veiws')
        ## student menu static items
        bioMenu = QAction('Biodata', self)
        bioMenu.setStatusTip('Bio and Contact data')
        bioMenu.triggered.connect(lambda state, x = 1, y = 'k': self.lunchReport(x, y))
        ViewMenu.addAction(bioMenu)
        
        academicMenu =  ViewMenu.addMenu('Academic')
        dumpClass1 = {}
        for k in self.myterms:
           act = str(list(self.myterms[k])[0])
           getResult = self.pullResults(k)
           studs = academicMenu.addMenu(act)
           for w in getResult:
               getRes = w['name'].split(',')
               getDat = w['description'].split(':::')
               if list(self.myterms[k])[1] in getRes:
                   stud = QAction(getDat[0], studs)
                   dumpClass1[k] = stud
                   stud.triggered.connect(lambda state, x = 2, term = k, rep= w['id']: self.lunchReport(x, term, rep))
                   studs.addAction(stud)
        
        affectiveMenu =  ViewMenu.addMenu('Affective')
        dumpClass2 = {}
        for k in self.myterms:
           act = str(self.myterms[k])
           stud = QAction(act, self)
           dumpClass2[k] = stud
           stud.triggered.connect(lambda state, x = 3, y = k: self.lunchReport(x, y))
           affectiveMenu.addAction(stud)
        
        psychomotorMenu =  ViewMenu.addMenu('Psychomotor')
        dumpClass3 = {}
        for k in self.myterms:
           act = str(self.myterms[k])
           stud = QAction(act, self)
           dumpClass3[k] = stud
           stud.triggered.connect(lambda state, x = 4, y = k: self.lunchReport(x, y))
           psychomotorMenu.addAction(stud)
        
        feeMenu =  ViewMenu.addMenu('Fees')
        dumpClass4 = {}
        for k in self.myterms:
           act = str(self.myterms[k])
           stud = QAction(act, self)
           dumpClass4[k] = stud
           stud.triggered.connect(lambda state, x = 5, y = k: self.lunchReport(x, y))
           feeMenu.addAction(stud)
        
        
        
        printMenu = mainMenu.addMenu('&Print')
        exitMenu1 = QAction('&Exit', self)
        exitMenu1.setShortcut('CTRL+Q')
        exitMenu1.setStatusTip('Close Dialog')
        exitMenu1.triggered.connect(lambda state, x = 1:self.lunchPrintForm(x))
        printMenu.addAction(exitMenu1)
        #printMenu.triggered.connect(lambda state, x = 1:self.lunchPrintForm(x))
        

        
        return mainMenu
        
    def buildBio(self):
        table = '''<html><head>
        <link rel ='stylesheet' type="text/css" href='static/stylesheets/invoice-print.css'/>
        <link rel ='stylesheet' type="text/css" href='static/stylesheets/theme.css'/>
        </head>
        <style>
        body{
            font: "Century Gothic";
        }
        table
        {
        
        }
        tbody, th, td{
        padding:2px;
         
        }
        td{ align:left}
        .tch{
                align: left !important;
                background-color:teal; 
                color:white;
                text-transform: uppercase;
                font-family: "Century Gothic";
        }
        .tch1{
                color:black;
                text-transform: uppercase;
                font-family: "Century Gothic";
                font-weight:bold;
                width: 300px;
        }
        .item-tab{
                display:inline-block;
        }
        td img{
        max-width: 100px;
        height:150px;
        }
        </style>
        <body>
            <div width='100%'>
                <div width="100%" style="background-color:teal; color:white; text-transform:uppercase; text-align:center">
                    <h3>Bio-Data and Contact Information</h3>
                </div>
                <div style='display:flex'>
                    <div class="item-tab" width='600px' >
                    <table width="500px " cellspacing="0" cellpadding="2px"  style="border-width:1px; border-color: teal; padding:2px" >
                        <tbody>
                            <tr><th class="tch" style="align:right">SCHOOL NUMBER</th><td class="tch1" width="40%">{{dat.schno}}</td>
                            <td rowspan="13" width="40%" style="background-color:green"><img src="img/studentz.png" width="250" height="340" /></td></tr>
                            <tr><th class="tch" style="align:right">SURNAME</th><td class="tch1" width="40%">{{dat.surname | upper}}</td></tr>
                            <tr><th class="tch" style="align:right">FIRSTNAME</th><td class="tch1" width="40%">{{dat.firstname | upper}}</td></tr>
                            <tr><th class="tch" style="align:right" >MIDDLENAME</th><td class="tch1" width="40%">{{dat.othername | upper}}</td></tr>
                            <tr><th class="tch" style="align:right">SEX</th><td class="tch1" width="40%">{{gender}}</td></tr>
                            <tr><th class="tch" style="align:right">DATE OF BIRTH</th><td class="tch1" width="40%">{{dob }}</td></tr>
                            <tr><th class="tch" style="align:right">AGE</th><td class="tch1" width="40%">{{age}}</td></tr>
                            <tr><th class="tch" style="align:right">LGA/District</th><td class="tch1" width="40%">{{dat.lga | upper}}</td></tr>
                            <tr><th class="tch" style="align:right">State/Region</th><td class="tch1" width="40%">{{dat.soo | upper}}</td></tr>
                            <tr><th class="tch" style="align:right">Nationality</th><td class="tch1" width="40%">{{dat.nation | upper}}</td></tr>
                            <tr><th class="tch" style="align:right">Date Started</th><td class="tch1" width="40%">{{admit}}  ( {{admit_dur}})</td></tr>
                            <tr><th class="tch" style="align:right">Status</th><td class="tch1" width="40%">{{dat.schno}}<.td></tr>
                            <tr><th class="tch" style="align:right">Address</th><td class="tch1" width="40%" style="word-wrap:break-word;overflow:none">{{dat.addr}}</td></tr>
                        </tbody>
                    </table>
                </div>
                </div>
                <div width="100%" style="background-color:teal; color:white; text-transform:uppercase; align:center">
                    <h3>Guradians/Primary Care Giver</h3>
                </div>
                <div>
                <table width="100% " cellspacing="0" cellpadding="2px"  style="border-width:1px; border-color: teal; padding:2px" >
                <tbody style='align:left'>
                    <tr><td class="tch1" width="100%"><ul><li>{{dat.g1 | upper}}({{dat.g1rel | upper}}) </li><li> {{dat.g1p1}} | {{dat.g1p2}} </li><li> {{dat.g1addr | upper}} </li> <li>{{dat.g1email}}</li></ul></td></tr>
                    <tr><td class="tch1" width="100%"><ul><li>{{dat.g2 | upper}}({{dat.g2rel | upper}}) </li><li> {{dat.g2p1}} | {{dat.g2p2}} </li><li> {{dat.g2addr | upper}} </li> <li>{{dat.g2email}}</li></ul></td></tr>
                </tbody>
                </table>
                
                </div></body></html>'''
               
            
        h = Template(table).render(gender= self.gender, dob = self.dob, age=self.age, admit =self.admit, admit_dur=self.admit_dur, dat = self.data)
        return h
        
    def buildAff(self, a):
        table = '''<html><head>
        <link rel ='stylesheet' type="text/css" href='static/stylesheets/invoice-print.css'/>
        <link rel ='stylesheet' type="text/css" href='static/stylesheets/theme.css'/>
        </head>
        <style>
        body{
            font: "Century Gothic";
        }
        table
        {
        
        }
        tbody, th, td{
        padding:2px;
         
        }
        td{ align:left}
        .tch{
                align: left !important;
                background-color:teal; 
                color:white;
                text-transform: uppercase;
                font-family: "Century Gothic";
        }
        .tch1{
                color:black;
                text-transform: uppercase;
                font-family: "Century Gothic";
                font-weight:bold;
                width: 300px;
        }
        .item-tab{
                display:inline-block;
        }
        td img{
        max-width: 100px;
        height:150px;
        }
        </style>
        <body>
            <div width='100%'>
                <div width="100%" style="background-color:teal; color:white; text-transform:uppercase; text-align:center">
                    <h3>Bio-Data and Contact Information</h3>
                </div>
                <div style='display:flex'>
                    <div class="item-tab" width='600px' >
                    <table width="100% " cellspacing="0" cellpadding="2px"  style="border-width:1px; border-color: teal; padding:2px" >
                        <tbody>
                        '''
                            
        table = ''' </tbody>
                    </table>
                </div>
                </div>
               </body></html>'''
               
            
        h = Template(table).render(gender= self.gender, dob = self.dob, age=self.age, admit =self.admit, admit_dur=self.admit_dur, dat = self.data)
        return h
    
    def buildAca(self, term, report):
        con = Con()
        result = self.pullResult(report)
        f_all = result['description']
        d = f_all.split(':::')
        _title = d[0]
        _theme = d[1]
        _font = d[2]
        _ass = d[3]
        _gra = d[4]
        _set = d[5]
        
        _ass_list =_ass.split('::') 
        _ass_list = [int(x) for x in _ass_list]
        _gra_list =_gra.split('::')
        grade = con.pullGrade(_gra_list[0])
        _set_list =_set.split('::')
      
        
        _data = con.academicReportData(term, self.sid, _ass_list )
        _d = _data[0]
        _c = _data[1]
        _s = _data[2]
        
        subjects = {}
        for s in _s:
           ss = _s[s][0]
           subjects[s] = ss.upper()  
           
        cas = {}
        for c in _c:
           cc = _c[c][1]
           cas[c] =  cc.upper()
           
        std = Con()
        avgs = std.subjectAverage(term, self.student, cas.keys(), subjects.keys())
        pos = std.studentAverage(term, self.student, cas.keys(), subjects.keys())
        posUnit = std.studentAverageUnit(term, self.student, cas.keys(), subjects.keys())
        t = self.buildWriter(subjects, cas, _d, avgs, _set_list, grade)
        
        
        table = '''<html><head>
        <link rel ='stylesheet' type="text/css" href='static/stylesheets/invoice-print.css'/>
       
        </head>
        <style>
        body{
            font: "Century Gothic";
        }
        @font-face
        {
               
        }
        h1{
                font-family: "Poiret One";
                font-size:30px;
        }
        h2{
                font-family: "Sarala";
                font-size:20px;
        }
        h3{
                font-family: "Sarala";
                font-size:20px;
               
        }
        tbody, th, td{
        padding:2px;
         
        }
        td{ align:center}
        .tch{
                align: left !important;
                background-color:teal; 
                color:white;
                text-transform: uppercase;
                font-family: "Century Gothic";
        }
        .tch1{
                color:black;
                text-transform: uppercase;
                font-family: "Century Gothic";
                font-weight:bold;
                width: 300px;
        }
        .item-tab{
                display:inline-block;
        }
        td img{
        max-width: 100px;
        height:150px;
        }
        .xtable{ display:block;}
        .xrow{ display:block;}
        .xcell{ display:inline-block;}
        
        .xtable{ display:table;}
        .xrow{ display:table-row;}
        .xcell{ display:table-cell;}
        .xcell-10{ width:100px !important;}
        </style>
        <body>
            <div>
            
            <div width='100%' style="background-color:teal; color:white; padding:4px; display:block">
            <h1>{{name}}</h1>
            </div>
            <tr>
            <td width='20%'>
              <img src="img/studentz.png" width="80" height="80" />  
            </td>
            <td>
            <table class="xtable" width='100%' style="font-weight:bold">
                <tr class="xrow">
                    <td class="xcell xcell-10">SCHOOL NUMBER</td>
                    <td class="xcell">{{schno}}</td>
                    <td class="xcell"></td>
                    <td class="xcell"></td>
                </tr>
                <tr class="xrow">
                    <td class="xcell xcell-10">POSITION IN CLASS</td>
                    <td class="xcell">{{pos[2]}} of {{pos[1]}}</td>
                    <td class="xcell">CLASS AVERAGE</td>
                    <td class="xcell">{{pos[0]}}</td>
                </tr>
                 <tr class="xrow">
                    <td class="xcell xcell-10">POSITION IN CLASS UNIT</td>
                    <td class="xcell">{{posUnit[2]}} of {{posUnit[1]}}</td>
                    <td class="xcell">CLASS UNIT AVERAGE</td>
                    <td class="xcell">{{posUnit[0]}}</td>
                </tr>
                <tr class="xrow">
                    <td class="xcell xcell-10">ATTENDANCE</td>
                    <td class="xcell">234.300</td>
                    <td class="xcell">80%</td>
                    <td class="xcell"></td>
                </tr>
                <tr class="xrow">
                    <td class="xcell xcell-10">FEES</td>
                    <td class="xcell">PREV. DEBT:</td>
                    <td class="xcell">NEXT FEE: </td>
                    <td class="xcell">Total: </td>
                </tr>
            </table>
            </td>
            </tr>
            </table>
            </div>
            <div width='100%'>
                <div width='100%' style="background-color:teal; color:white; padding:4px;display:block">
                    
                        <h1>{{title}}</h1>
                    
                </div>
                <div style='display:flex'>
                    <div class="item-tab" width='600px' >
                    
                        {{text}}
                    
                </div>
                </div>
        </body>
        </html>'''
               
            
        h = Template(table).render(text= t, title=_title, name=self.fullname, schno=self.schno, pos = pos, posUnit = posUnit)
        return h
    
    def buildWriter(self, subjects, cas,  data, avgs, sets, grade):
        subject = subjects.keys()
        cal = cas.keys()
        cal.sort()
        table = '<table  width="100%" cellspacing="0" cellpadding="2px"  style="border-width:1px; border-color: teal; padding:2px; color:black; font-family: Century Gothic">'
        table += "<thead>"
        table += "<tr style='background-color:teal; color:white'>"
        table += "<th>"
        table += "SUBJECTS"
        table += "</th>"
        arr = {}
        arrca = {}
        summed_arr = []
        aummed_arr = []
         
        for ca in cal:
            arrca[ca] = []
            if str(16) in sets:
                table += "<th>"
                table += str(cas[ca])
                table += "</th>"
        if str(5) in sets: 
            #total 
            table += "<th>"
            table += "TOTAL<BR>"
            table += "</th>"
        if str(4) in sets: 
            #total 100%
            table += "<th>"
            table += "TOTAL<BR>100%"
            table += "</th>"
        if str(6) in sets:
            #total 100%
            table += "<th>"
            table += "GRADE"
            table += "</th>"
        if str(7) in sets: 
            #subject Average
            table += "<th width='80px'>"
            table += "SUBJECT<BR>AVERAGE"
            table += "</th>"
        if str(8) in sets: 
            #ranking only
            table += "<th width='80px'>"
            table += "CLASS<BR>RANKING"
            table += "</th>"
        if str(9) in sets: 
            #ranking and population
            table += "<th width='80px'>"
            table += "CLASS<BR>RANKING"
            table += "</th>"
        table += "</tr>"
        table += "</thead>"
        table += "<tbody>"
        for sub in subject:
            arr[sub] = []
            table += "<tr>"
            table += "<td >"
            table += str(subjects[sub])
            table += "</td>"
            for ca in cal:
                nm ='AB'+str(sub)+'CD'+str(ca)
                if nm in data:
                    arr[sub].append(data[nm])
                    arrca[ca].append(data[nm])
                    tdd = str(data[nm])
                else:
                    tdd = str('-.-')
                if str(16) in sets:
                    table += "<td align='center'>"
                    table += tdd
                    table += "</td>" 
            summed = sum(arr[sub])
            summed_arr.append(summed)
            if str(5) in sets:
                table += "<td align='center'>"
                table += str(round(summed, 1))
                table += "</td>"
            if str(4) in sets:
                table += "<td align='center'>"
                table += str(round(summed, 1))
                table += "</td>"
                
            aummed_arr.append(avgs[sub][0])
            if str(6) in sets:
                table += "<td align='center' style='width:80px'>"
                table += str(avgs[sub][0])
                table += "</td>"
            if str(7) in sets:
                table += "<td align='center' style='width:80px'>"
                table += 'Excellent'
                table += "</td>"
            if str(8) in sets:   
                table += "<td align='center'style='width:80px'>"
                table += str(avgs[sub][2])
                table += "</td>"
            if str(9) in sets:   
                table += "<td align='center'style='width:80px'>"
                table += str(avgs[sub][2])+' of '+str(avgs[sub][1])
                table += "</td>"
        table += "</tr>"
        table += "</tbody>"
        table += "<tfoot>"
        table += "<tr style='background-color:teal; color:white'>"
        table += "<th>"
        table += "SUBJECTS"
        table += "</th>"
        for ca in cal:
            if len(arrca[ca]) > 0:
                cammed = sum(arrca[ca])/float(len(arrca[ca]))
                cammed = str(round(cammed, 1))
            else:
                cammed = '-.-'
            if str(16) in sets:
                table += "<th>"
                table +=cammed
                table += "</th>"
        if str(5) in sets:
            table += "<th>"
            if len(summed_arr) > 0:
                total = sum(summed_arr)/float(len(summed_arr))
            else:
                total = '-.-'
                table += str(round(total,1))
            table += "</th>"
        if str(4) in sets:
            table += "<th>"
            if len(summed_arr) > 0:
                total = sum(summed_arr)/float(len(summed_arr))
            else:
                total = '-.-'
                table += str(round(total,1))
            table += "</th>"
        if str(6) in sets:
            table += "<th>"
            #Grading
            table += "</th>"
        if str(7) in sets:
            table += "<th>"
            if len(aummed_arr) > 0:
                totals = sum(aummed_arr)/float(len(aummed_arr))
            else:
                totals = '-.-'
            table += str(round(totals,1))
            table += "</th>"
        if str(8) in sets:
            table += "<th>"
            #table += str(subjects[sub])
            table += "</th>"
        if str(9) in sets:
            table += "<th>"
            #table += str(subjects[sub])
            table += "</th>"
        table += "</tr>"
        table += "</tfoot>"
        table += "<table>"
        return table
    
    def buildFee(self, a):
        table = '''<html><head>
        <link rel ='stylesheet' type="text/css" href='static/stylesheets/invoice-print.css'/>
        <link rel ='stylesheet' type="text/css" href='static/stylesheets/theme.css'/>
        </head>
        <style>
        body{
            font: "Century Gothic";
        }
        table
        {
        
        }
        tbody, th, td{
        padding:2px;
         
        }
        td{ align:left}
        .tch{
                align: left !important;
                background-color:teal; 
                color:white;
                text-transform: uppercase;
                font-family: "Century Gothic";
        }
        .tch1{
                color:black;
                text-transform: uppercase;
                font-family: "Century Gothic";
                font-weight:bold;
                width: 300px;
        }
        .item-tab{
                display:inline-block;
        }
        td img{
        max-width: 100px;
        height:150px;
        }
        </style>
        <body>
            <div width='100%'>
                <div width="100%" style="background-color:teal; color:white; text-transform:uppercase; text-align:center">
                    <h3>Bio-Data and Contact Information</h3>
                </div>
                <div style='display:flex'>
                    <div class="item-tab" width='600px' >
                    <table width="500px " cellspacing="0" cellpadding="2px"  style="border-width:1px; border-color: teal; padding:2px" >
                        <tbody>
                            <tr><th class="tch" style="align:right">SCHOOL NUMBER</th><td class="tch1" width="40%">{{dat.schno}}</td>
                            <td rowspan="13" width="40%" style="background-color:green"><img src="img/studentz.png" width="250" height="340" /></td></tr>
                            <tr><th class="tch" style="align:right">SURNAME</th><td class="tch1" width="40%">{{dat.surname | upper}}</td></tr>
                            <tr><th class="tch" style="align:right">FIRSTNAME</th><td class="tch1" width="40%">{{dat.firstname | upper}}</td></tr>
                            <tr><th class="tch" style="align:right" >MIDDLENAME</th><td class="tch1" width="40%">{{dat.othername | upper}}</td></tr>
                            <tr><th class="tch" style="align:right">SEX</th><td class="tch1" width="40%">{{gender}}</td></tr>
                            <tr><th class="tch" style="align:right">DATE OF BIRTH</th><td class="tch1" width="40%">{{dob }}</td></tr>
                            <tr><th class="tch" style="align:right">AGE</th><td class="tch1" width="40%">{{age}}</td></tr>
                            <tr><th class="tch" style="align:right">LGA/District</th><td class="tch1" width="40%">{{dat.lga | upper}}</td></tr>
                            <tr><th class="tch" style="align:right">State/Region</th><td class="tch1" width="40%">{{dat.soo | upper}}</td></tr>
                            <tr><th class="tch" style="align:right">Nationality</th><td class="tch1" width="40%">{{dat.nation | upper}}</td></tr>
                            <tr><th class="tch" style="align:right">Date Started</th><td class="tch1" width="40%">{{admit}}  ( {{admit_dur}})</td></tr>
                            <tr><th class="tch" style="align:right">Status</th><td class="tch1" width="40%">{{dat.schno}}<.td></tr>
                            <tr><th class="tch" style="align:right">Address</th><td class="tch1" width="40%" style="word-wrap:break-word;overflow:none">{{dat.addr}}</td></tr>
                        </tbody>
                    </table>
                </div>
                </div>
                <div width="100%" style="background-color:teal; color:white; text-transform:uppercase; align:center">
                    <h3>Guradians/Primary Care Giver</h3>
                </div>
                <div>
                <table width="100% " cellspacing="0" cellpadding="2px"  style="border-width:1px; border-color: teal; padding:2px" >
                <tbody style='align:left'>
                    <tr><td class="tch1" width="100%"><ul><li>{{dat.g1 | upper}}({{dat.g1rel | upper}}) </li><li> {{dat.g1p1}} | {{dat.g1p2}} </li><li> {{dat.g1addr | upper}} </li> <li>{{dat.g1email}}</li></ul></td></tr>
                    <tr><td class="tch1" width="100%"><ul><li>{{dat.g2 | upper}}({{dat.g2rel | upper}}) </li><li> {{dat.g2p1}} | {{dat.g2p2}} </li><li> {{dat.g2addr | upper}} </li> <li>{{dat.g2email}}</li></ul></td></tr>
                </tbody>
                </table>
                
                </div></body></html>'''
               
            
        h = Template(table).render(gender= self.gender, dob = self.dob, age=self.age, admit =self.admit, admit_dur=self.admit_dur, dat = self.data)
        return h
    
    def buildPsy(self, a):
        table = '''<html><head>
        <link rel ='stylesheet' type="text/css" href='static/stylesheets/invoice-print.css'/>
        <link rel ='stylesheet' type="text/css" href='static/stylesheets/theme.css'/>
        </head>
        <style>
        body{
            font: "Century Gothic";
        }
        table
        {
        
        }
        tbody, th, td{
        padding:2px;
         
        }
        td{ align:left}
        .tch{
                align: left !important;
                background-color:teal; 
                color:white;
                text-transform: uppercase;
                font-family: "Century Gothic";
        }
        .tch1{
                color:black;
                text-transform: uppercase;
                font-family: "Century Gothic";
                font-weight:bold;
                width: 300px;
        }
        .item-tab{
                display:inline-block;
        }
        td img{
        max-width: 100px;
        height:150px;
        }
        </style>
        <body>
            </body></html>'''
               
            
        h = Template(table).render(gender= self.gender, dob = self.dob, age=self.age, admit =self.admit, admit_dur=self.admit_dur, dat = self.data)
        return h