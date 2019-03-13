# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
from PyQt4 import QtCore, QtGui
from PyQt4.QtWebKit import QWebView
from connect import Db
from connectdata import Dat
from frmstudent import StudentForm
from frmstudentedit import StudentEditForm
from frmstudentprofile import StudentProfile
from frmgrade import GradeForm
from frmaccount import SettingsManager, SessionsManager
from studenttable import StudentTable
from dialogtermfee import TermFeeDialog
from dialogtermpay import TermPayDialog
from dialogsubject import SubjectCaDialog
from dialogaffective import AffectiveCaDialog
from dialogpsychomoto import PsychomotoCaDialog
from dialogchangeclass import ChangeClassDialog, RemoveClassDialog, SubjectClassDialog
from dialogexpenses import ExpensesDialog
from dialogstore import StoreDialog
from printtable import PrintTable
from tablereport import TableProfile
from collections import defaultdict
from jinja2 import Template
import numbers
import sys
import sip
from datetime import datetime
#import spec
class Window(QtGui.QMainWindow):
    
    def __init__(self, ):
        super(Window, self).__init__()  
        
    def main(self, ):
        super(Window, self).__init__()   
        font_db = QtGui.QFontDatabase()
        quicksand = font_db.addApplicationFont('static/quicksand/Quicksand-Light.ttf')
        quicksand_families = font_db.applicationFontFamilies(quicksand)
        poiretone = font_db.addApplicationFont('static/poiretone/PoiretOne-Regular.ttf')
        poiretone_families = font_db.applicationFontFamilies(poiretone)
        sarala = font_db.addApplicationFont('static/sarala/Sarala-Regular.ttf')
        sarala_families = font_db.applicationFontFamilies(sarala)
        self.quicksand = QtGui.QFont('Quicksand-Light', 17)
        self.poiretone = QtGui.QFont('PoiretOne-Regular', 20)
        self.sarala = QtGui.QFont('Sarala-Regular', 15)
        
        self.report_table_holder = []
        #table font and header
        self.tableFont = QtGui.QFont()
        self.tableFont.setFamily('Century Gothic')
        self.tableHeaderStyle = "::section {""background-color: teal; color:white}"
        
        self.hc1_box = QtGui.QVBoxLayout()
        self.f_boxx = QtGui.QVBoxLayout()
        self.f_boxx.addLayout(self.hc1_box)
        self.hold_checkbox = {}
        
                
        # wnidow property
        self.setGeometry(50, 50, 915, 600)
        self.resize(915, 600)
        self.showMaximized()
        self.setWindowTitle('Main Window')
        self.bioTable = []
        self.conTable = []
        self.mainMenu = self.menuUi()
        self.tbx1 = self.titleToolbar()
        self.tbx = self.mainToolbar()
        self.central = self.centralBody()
        self.tabz = self.mainBody()
        
        
        self.show()

    def classLoading(self):
        itz = self.pullClass(1)
        all_class_students = {}
        for i in itz:
            all_class_students[i] = {}
            all_class_students[i]['name'] = itz[i] 
            all_class_students[i]['subs'] = {}
            itz1 = self.pullClass(i)
            for j in itz1:
                all_class_students[i]['subs'][j] = itz1[j]       
        return all_class_students
    
    def menuSession(self):
        ses = self.pullSession()
        self.sessionMenu.clear()
        for k in ses:
           act = str(ses[k])
           stud = self.sessionMenu.addMenu(QtGui.QIcon("icons/calendar.png"), act)
           arr = self.pullTerm(k)
           for j in arr:
               act1 = str(arr[j]).upper()
               studs = stud.addMenu(QtGui.QIcon("icons/calendar1.png"),act1)
    
               st = QtGui.QAction(QtGui.QIcon("icons/building.png"),'Class', self)
               st.triggered.connect(lambda state, x = j: self.myTableClassUnit(0, x))
               studs.addAction(st)
               
               fe = QtGui.QAction(QtGui.QIcon("icons/fees.png"),'Fees', self)
               fe.triggered.connect(lambda state, x = j: self.myTableClassUnitFee(0, x))
               studs.addAction(fe)
               
               ex = QtGui.QAction(QtGui.QIcon("icons/expenses.png"), 'Expenses', self)
               ex.triggered.connect(lambda state, x = j: self.getSessionData(1, x))
               studs.addAction(ex)
               
               ac = QtGui.QAction(QtGui.QIcon("icons/banks.png"), 'Accounts', self)
               ac.triggered.connect(lambda state, x = j: self.getSessionData(2, x))
               studs.addAction(ac)
               
               ma = QtGui.QAction(QtGui.QIcon("icons/mail.png"), 'Mails', self)
               ma.triggered.connect(lambda state, x = j: self.getSessionData(3, x))
               studs.addAction(ma)
               
               co = QtGui.QAction(QtGui.QIcon("icons/mail.png"), 'Good Conducts', self)
               co.triggered.connect(lambda state, x = j: self.getSessionData(4, x))
               studs.addAction(co)
               
               mc = QtGui.QAction(QtGui.QIcon("icons/mail.png"), 'Misconducts', self)
               mc.triggered.connect(lambda state, x = j: self.getSessionData(5, x))
               studs.addAction(mc)
               
               fc = QtGui.QAction(QtGui.QIcon("icons/store.png"), 'Stock', self)
               fc.triggered.connect(lambda state, x = j: self.getSessionData(6, x))
               studs.addAction(fc)
               
    def menuStudent(self):
        sess = self.activeTerm()
        self.studentMenu.clear()
        ## student menu static items
        studentAddMenu = QtGui.QAction(QtGui.QIcon("icons/addstudent.png"), '&Add Student', self)
        studentAddMenu.setShortcut('CTRL+A')
        studentAddMenu.setStatusTip('Add Students')
        studentAddMenu.triggered.connect(self.studentLunchForm)
        
        studentAllMenu = QtGui.QAction(QtGui.QIcon("icons/users.png"),'&All Students', self)
        studentAllMenu.setStatusTip('All Students')
        studentAllMenu.triggered.connect(lambda: self.genTable(0))
        
        studentExMenu = QtGui.QAction(QtGui.QIcon("icons/users.png"),'&Ex. Students', self)
        studentExMenu.setStatusTip('All Ex-Students')
        studentExMenu.triggered.connect(lambda:self.genTable(1))
        
        studentCrMenu = QtGui.QAction(QtGui.QIcon("icons/users.png"),'&Current Students', self)
        studentCrMenu.setStatusTip('Current Students')
        studentCrMenu.triggered.connect(lambda: self.genTable(2))
        
        self.studentMenu.addAction(studentAddMenu)
        self.studentMenu.addAction(studentAllMenu)
        self.studentMenu.addAction(studentExMenu)
        self.studentMenu.addAction(studentCrMenu)
        self.studentMenu.addSeparator()
        
        ## student menu dynamic items
        all_class_students = self.classLoading()

        for k in all_class_students:
            act = str(all_class_students[k]['name']).upper()
            stud = self.studentMenu.addMenu(QtGui.QIcon("icons/users.png"), act)
            
            act1 = 'All'
            st = stud.addMenu(QtGui.QIcon("icons/users.png"), act1)
            #all
            aact1 = 'All Sex'
            sta = QtGui.QAction(QtGui.QIcon("icons/users.png"), aact1, self)
            sta.triggered.connect(lambda state, w = k, x = 'xx', y = sess[2], z = 0: self.lunchClassTable(w, x, y, z))
            st.addAction(sta)
            #male
            mact1 = 'Males'
            stm = QtGui.QAction(QtGui.QIcon("icons/users.png"), mact1, self)
            stm.triggered.connect(lambda state, w = k, x = 'xx', y = sess[2], z = 1: self.lunchClassTable(w, x, y, z))
            st.addAction(stm)
            #females
            fact1 = 'Females'
            stf = QtGui.QAction(QtGui.QIcon("icons/users.png"), fact1, self)
            stf.triggered.connect(lambda state, w = k, x = 'xx', y = sess[2], z = 2: self.lunchClassTable(w, x, y, z))
            st.addAction(stf)
            
            for k1 in  all_class_students[k]['subs']:
                act1 = str(all_class_students[k]['subs'][k1]).upper()
                st = stud.addMenu(QtGui.QIcon("icons/users.png"), act1)
                               
                #all
                aact1 = 'All Sex'
                sta = QtGui.QAction(QtGui.QIcon("icons/users.png"), aact1, self)
                sta.triggered.connect(lambda state, w = k, x = k1, y = sess[2], z = 0: self.lunchClassTable(w, x, y, z))
                st.addAction(sta)
                #male
                mact1 = 'Males'
                stm = QtGui.QAction(QtGui.QIcon("icons/users.png"), mact1, self)
                stm.triggered.connect(lambda state, w = k, x = k1, y = sess[2], z = 1: self.lunchClassTable(w, x, y, z))
                st.addAction(stm)
                #females
                fact1 = 'Females'
                stf = QtGui.QAction(QtGui.QIcon("icons/users.png"), fact1, self)
                stf.triggered.connect(lambda state, w = k, x = k1, y = sess[2], z = 2: self.lunchClassTable(w, x, y, z))
                st.addAction(stf)
            
                
    def dropdownSession(self):
        self.d_sessionData.clear()
        sessionss = self.getTerm()
        for k in sessionss:
            self.d_sessionData.addItem(sessionss[k], k)
          
    def dropdownStudent(self):
        clasz = self.classLoading()
        self.d_classData.clear()
        for k in clasz:
            self.d_classData.addItem(clasz[k]['name'], str(k)+',xx')
            for k1 in clasz[k]['subs']:
                self.d_classData.addItem(str(clasz[k]['name']).upper()+' '+str(clasz[k]['subs'][k1]).upper(), str(k1)+','+str(k))   
    
    def menuUi(self): 
        extractQuit = QtGui.QAction(self) 
        extractQuit.setStatusTip('File')
          
        self.statusBar()
        
        mainMenu = self.menuBar()
        
        #file menu
        sessionIcon = QtGui.QIcon("icons/four-black-squares.png")
        fileMenu = mainMenu.addMenu(sessionIcon, '&File')
        
        schoolMenu = QtGui.QAction(QtGui.QIcon("icons/building.png"), 'School Info.', self)
        schoolMenu.setShortcut('CTRL+L')
        schoolMenu.setStatusTip('School Data')
        schoolMenu.triggered.connect(self.lunchForm)
        
        backupOffMenu = QtGui.QAction(QtGui.QIcon("icons/upload.png"), '&Backup to Offline Storage', self)
        backupOffMenu.setShortcut('CTRL+B+O')
        backupOffMenu.setStatusTip('offlineb')
        backupOffMenu.triggered.connect(self.lunchForm)
        
        restoreOffMenu = QtGui.QAction(QtGui.QIcon("icons/download.png"), '&Restore from Storage', self)
        restoreOffMenu.setShortcut('CTRL+B+R')
        restoreOffMenu.setStatusTip('offlinec')
        restoreOffMenu.triggered.connect(self.lunchForm)
        
        backupOnMenu = QtGui.QAction(QtGui.QIcon("icons/cloud-upload.png"), '&Cloud Backup.', self)
        backupOnMenu.setShortcut('CTRL+B+C')
        backupOnMenu.setStatusTip('onlineb')
        backupOnMenu.triggered.connect(self.lunchForm)
        
        restoreOnMenu = QtGui.QAction(QtGui.QIcon("icons/cloud-download.png"), '&Restore from Cloud', self)
        restoreOnMenu.setShortcut('CTRL+B+L')
        restoreOnMenu.setStatusTip('onliner')
        restoreOnMenu.triggered.connect(self.lunchForm)
        
        userMenu = QtGui.QAction(QtGui.QIcon("icons/user.png"), '&Users', self)
        userMenu.setShortcut('CTRL+U')
        userMenu.setStatusTip('user')
        userMenu.triggered.connect(self.lunchForm)
        
        schoolMenu = QtGui.QAction(QtGui.QIcon("icons/building.png"),'Sc&hool Info.', self)
        schoolMenu.setShortcut('CTRL+L')
        schoolMenu.setStatusTip('School Data')
        schoolMenu.triggered.connect(self.lunchForm)
        
        exitMenu = QtGui.QAction(QtGui.QIcon("icons/remove-button.png"), '&Exit', self)
        exitMenu.setShortcut('CTRL+Q')
        exitMenu.setStatusTip('Close Application')
        exitMenu.triggered.connect(self.lunchForm)
        
        fileMenu.addAction(schoolMenu)
        fileMenu.addAction(backupOffMenu)
        fileMenu.addAction(restoreOffMenu)
        fileMenu.addAction(backupOnMenu)
        fileMenu.addAction(restoreOnMenu)
        fileMenu.addAction(userMenu)
        fileMenu.addAction(exitMenu)
        
        #session menu
        sessionIcon = QtGui.QIcon("img/msession.png")
        self.sessionMenu = mainMenu.addMenu(QtGui.QIcon("icons/calendar.png"), '')
        self.menuSession()
        ## student menu dynamic items

              
        #student menu
        self.studentMenu = mainMenu.addMenu(QtGui.QIcon("icons/users.png"), '')
        self.menuStudent()
        
        #staff menu
        #staffIcon = QtGui.QIcon("img/mstudent.png")
        #staffMenu = mainMenu.addMenu(staffIcon, '&Staff')
        #staffMenu.addAction(extractQuit)

        #1 account
        #2 subjects
        #3 class
        #4 expenses
        #5 stock
        #6 fees
        #7 affective
        #8 psycomotor
        #9 assessment
        #settings menu
        settingIcon = QtGui.QIcon("icons/settings.png")
        settingMenu = mainMenu.addMenu(settingIcon,'')
        ## student menu static items
        sessionIcon = QtGui.QIcon("img/icosession.png") 
        sessionMenu = QtGui.QAction(sessionIcon,'&Session Manager', self)
        sessionMenu.setStatusTip('Manage Academic Session')
        sessionMenu.triggered.connect(self.lunchSessionForm)
        
        classIcon = QtGui.QIcon("img/icoclass.png")
        classMenu = QtGui.QAction(classIcon, '&Class Manager', self)
        classMenu.setStatusTip('Manage Class settings')
        classMenu.triggered.connect(lambda: self.lunchSettings(3))
        
        assessIcon = QtGui.QIcon("img/icoassess.png")
        assessMenu = QtGui.QAction(assessIcon, 'Assess&ment', self)
        assessMenu.setStatusTip('Manage assessment')
        assessMenu.triggered.connect(lambda: self.lunchSettings(9))
        
        affectIcon = QtGui.QIcon("img/icoaffect.png")
        affectMenu = QtGui.QAction(affectIcon, '&Affective/Attitude', self)
        affectMenu.setStatusTip('Manage Affective domain')
        affectMenu.triggered.connect(lambda: self.lunchSettings(7))
        
        psycoIcon = QtGui.QIcon("img/icopsyco.png")
        psycoMenu = QtGui.QAction(psycoIcon, '&Psychomotor/Skills', self)
        psycoMenu.setStatusTip('Manage skills')
        psycoMenu.triggered.connect(lambda: self.lunchSettings(8))
        
        subjectIcon = QtGui.QIcon("img/icosubject.png")
        subjectMenu = QtGui.QAction(subjectIcon,'&Subject Manager', self)
        subjectMenu.setStatusTip('Manage subjects taught')
        subjectMenu.triggered.connect(lambda: self.lunchSettings(2))
        
        gradeIcon = QtGui.QIcon("img/icograde.png")
        gradeMenu = QtGui.QAction(gradeIcon, '&Grades Manager', self)
        gradeMenu.setStatusTip('Manage grading system')
        gradeMenu.triggered.connect(self.lunchGradeForm)
        
        feeIcon = QtGui.QIcon("img/icofee.png")
        feeMenu = QtGui.QAction(feeIcon, '&Fees Manager', self)
        feeMenu.setStatusTip('Manage fees type')
        feeMenu.triggered.connect(lambda: self.lunchSettings(6))
        
        accountIcon = QtGui.QIcon("img/icoaccount.png")
        accountMenu = QtGui.QAction(accountIcon, '&Accounts Manager', self)
        accountMenu.setStatusTip('Manage Accounts')
        accountMenu.triggered.connect(lambda: self.lunchSettings(1))
        
        expenseIcon = QtGui.QIcon("img/icoexpenses.png")
        expenseMenu = QtGui.QAction(expenseIcon,'&Expenses Manager', self)
        expenseMenu.setStatusTip('Expense type')
        expenseMenu.triggered.connect(lambda: self.lunchSettings(4))
        
        storeIcon = QtGui.QIcon("img/icostore.png")
        storeMenu = QtGui.QAction(storeIcon, '&Stores Manager', self)
        storeMenu.setStatusTip('set Store items')
        storeMenu.triggered.connect(lambda: self.lunchSettings(5))
        
        settingMenu.addAction(accountMenu)
        settingMenu.addAction(affectMenu)
        settingMenu.addAction(assessMenu)
        settingMenu.addAction(classMenu)
        settingMenu.addAction(psycoMenu)
        settingMenu.addAction(expenseMenu)
        settingMenu.addAction(feeMenu)
        settingMenu.addAction(gradeMenu)
        settingMenu.addAction(sessionMenu)
        settingMenu.addAction(storeMenu)
        settingMenu.addAction(subjectMenu)
        
    
    def mainToolbar(self):
        #main display items
        
        sessionAction = QtGui.QAction(QtGui.QIcon('img/session.png'), 'Session', self)
        sessionAction.triggered.connect(lambda state, x = 0: self.changeCentralBody(x))
        
        studentAction = QtGui.QAction(QtGui.QIcon('img/student.png'), 'Student', self)
        studentAction.triggered.connect(lambda state, x= 1: self.changeCentralBody(x))
        
        staffAction = QtGui.QAction(QtGui.QIcon('img/staff.png'), 'Staff', self)
        staffAction.triggered.connect(lambda state, x = 2: self.changeCentralBody(x))
        
        feeAction = QtGui.QAction(QtGui.QIcon('img/fee.png'), 'fees', self)
        feeAction.triggered.connect(lambda state, x = 3: self.changeCentralBody(x))
        
        expenseAction = QtGui.QAction(QtGui.QIcon('img/expense.png'), 'Expenses', self)
        expenseAction.triggered.connect(lambda state,  x = 4: self.changeCentralBody(x))
        
        exitAction = QtGui.QAction(QtGui.QIcon('img/exit.png'), 'Exit', self)
        exitAction.triggered.connect(QtGui.qApp.quit)
        
        
        self.toolbarMain = self.addToolBar('Main')
        self.addToolBar(QtCore.Qt.LeftToolBarArea, self.toolbarMain )
        self.toolbarMain.addAction(sessionAction)
        self.toolbarMain.addAction(studentAction)
        self.toolbarMain.addAction(staffAction)
        self.toolbarMain.addAction(feeAction)
        spacer = QtGui.QWidget(self)
        spacer.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self.toolbarMain.addWidget(spacer)
        self.toolbarMain.addAction(exitAction)
        self.toolbarMain.setFloatable(False)
        self.toolbarMain.setOrientation(QtCore.Qt.Vertical)
        self.toolbarMain.resize(self.toolbarMain.sizeHint())
        self.toolbarMain.setStyleSheet("background-color: #022140")
        
        
    def activeTerm(self):
        term = self.callTerm()
        session = self.callSession(term[2])
        self.mainTermSession = term[0]
        self.mainSession = session[0]
        self.mainTerm = term[1]
        return [session[0], session[1], term[0], term[1]]

    def titleToolbar(self):
        session = self.activeTerm()
        activeTerm = str(session[1])+' SESSION '+str(session[3])+' TERM'
        self.majorSession = session[2];
        self.lbl = QtGui.QLabel(activeTerm)
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        #font.setWeight(75)
        self.lbl.setFont(self.poiretone)
        self.lbl.setStyleSheet("QLabel {color: darkblue}")
        #self.lbl.setFont(QtGui.QFont('Century Gothic', 17))
        self.toolbar1 = self.addToolBar('Title')
        self.toolbar1.setStyleSheet("background-color: white")
        self.toolbar1.addWidget(self.lbl)
        
        
    def studentToolbar(self):
        self.d_session = QtGui.QLabel('Quick Selection')
        
        self.d_sessionData = QtGui.QComboBox()
        self.dropdownSession()
        
        self.d_classData = QtGui.QComboBox()
        self.dropdownStudent()
        
        displayInfo = {}
        displayInfo.update({1: 'BioData'})
        displayInfo.update({2: 'Contact Information'})
        displayInfo.update({3: 'Photo Gallery'})
        displayInfo.update({11: 'Subjects'})
        displayInfo.update({4: 'Academic'})
        displayInfo.update({5: 'Affective'})
        displayInfo.update({6: 'Psychomotor'})
        displayInfo.update({7: 'Report Card'})
        displayInfo.update({8: 'Fees and payments'})
        displayInfo.update({9: 'Fees'})
        displayInfo.update({10: 'Payments'})
        
        self.d_displayData = QtGui.QComboBox()
        for dd in displayInfo:
            self.d_displayData.addItem(str(displayInfo[dd]).upper(), dd)
            
            
        self.d_pb1 = QtGui.QPushButton()
        self.d_pb1.setObjectName("Query")
        self.d_pb1.setText("Query")
        self.d_pb1.setFlat(False)
        bntstyle = "background-color: green; font-size: 12px; border:0px; padding:3px; margin:0px; font:Century Gothic;  text-align: left; color: white"
        self.d_pb1.setStyleSheet(bntstyle)  
        self.connect(self.d_pb1, QtCore.SIGNAL("clicked()"), lambda:  self.quickTable())
        
        self.toolbar = self.addToolBar('Main')
        self.toolbar.setStyleSheet("background-color: white")
           
        spacer = QtGui.QWidget(self)
        spacer.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self.toolbar.addWidget(spacer)
        self.toolbar.addWidget(self.d_session)
        self.toolbar.addWidget(self.d_sessionData)
        self.toolbar.addWidget(self.d_classData)
        self.toolbar.addWidget(self.d_displayData)
        self.toolbar.addWidget(self.d_pb1)
        
        self.show()
        
    def centralBody(self):
        self.mainStack = QtGui.QStackedWidget()
        
        self.welcomeStack = QtGui.QWidget()
        self.studentStack = QtGui.QWidget()
        self.staffStack = QtGui.QWidget()
        self.expenseStack = QtGui.QWidget()
        self.mainStack.addWidget(self.welcomeStack)
        self.mainStack.addWidget(self.staffStack)
        self.mainStack.addWidget(self.studentStack)
        
        self.mainStack.addWidget(self.expenseStack)
        
        self.windowMain()
        self.mainStack.setCurrentIndex(0)
        self.setCentralWidget(self.mainStack)
        
    def changeCentralBody(self, a):
        if a == 0:
            self.mainStack.setCurrentIndex(a)
        elif a == 1:
            self.mainStack.setCurrentIndex(a)
        elif a == 2:
            self.mainStack.setCurrentIndex(a)
        elif a == 3:
            #self.mainStack.setCurrentIndex(a)
            self.stackLeftBar.setCurrentIndex(2)
        else:
            pass
            
    def genTable(self, a):
        _session = self.mainTermSession
        if a == 0:
            studentsIDs = self.getClassAllStudents(_session, 0)
            self.tabletitle.setText('All Students Recorded')
        elif a == 1:
            studentsIDs = self.getClassAllStudents(_session, 1)
            self.tabletitle.setText('ALL Ex-Students')
        elif a == 2:
            studentsIDs = self.getClassAllStudents(_session, 2)
            self.tabletitle.setText('Current Students')
            
            
        student_id = []
        
        for dx in studentsIDs :
            student_id.append(dx['id'])
            
        #self.form.className('All')    
        self.tabl.close()
        self.tabl = self.myTable1(0, studentsIDs)
        self.hbox2.addWidget(self.tabl)
        self.tabl.show()
        
        
    def quickTable(self):
        _session = self.d_sessionData.itemData(self.d_sessionData.currentIndex())
        _clasz = self.d_classData.itemData(self.d_classData.currentIndex())
        _display = self.d_displayData.itemData(self.d_displayData.currentIndex())
        realClass = _clasz.split(',')
        
        
        if(realClass[1] and realClass[1] == 'xx'):
            studentsIDs = self.getClassStudents(_session , realClass[0], 0)
        else:
            studentsIDs = self.getClassStudents(_session, realClass[0], 1)
            
        
        student_id = []
        for dx in studentsIDs :
            student_id.append(dx[0]) 
                
        
        if(_display == 1):
            #bio information
            try:
                self.tabl.close()
                self.stackRightBar.setCurrentIndex(0)
                self.stackLeftBar.setCurrentIndex(0)
                self.checkBoxStack.setCurrentIndex(0)
                self.tabl = self.myTable1(0, studentsIDs)
                self.tabletitle.setText('Tiiii')
                self.hbox2.addWidget(self.tabl)
                self.tabl.show()
            except:
                pass
            
            
        elif(_display == 2): 
            #contact info
            try:
                self.tabl.close()
                self.stackRightBar.setCurrentIndex(0)
                self.stackLeftBar.setCurrentIndex(0)
                self.checkBoxStack.setCurrentIndex(1)
                self.tabl = self.myTable2(0, studentsIDs)
                self.hbox2.addWidget(self.tabl)
                self.tabl.show()
            except:
                pass
            
        elif(_display == 3): 
            #photo
            pass
        
        elif(_display == 4): 
            #academic
            self.academicData(_session, student_id, studentsIDs)
 
        elif(_display == 5): 
            #affective
            self.affectiveData(_session, student_id, studentsIDs)
        
        elif(_display == 6): 
            #affective
            self.psychoData(_session, student_id, studentsIDs)
            
        elif(_display == 7): 
            #report card
            pass          
            
        elif(_display == 8): 
            #fees and payments
            if(realClass[1] and realClass[1] == 'xx'):
                self.myTableClassUnitFee(1, _session, realClass[0], None)
            else:
                self.myTableClassUnitFee(4, _session, None, realClass[0])
            
        elif(_display == 9):
            if(realClass[1] and realClass[1] == 'xx'):
                self.myTableClassUnitFee(2, _session, realClass[0], None)
            else:
                self.myTableClassUnitFee(5, _session, None, realClass[0])
        
        elif(_display == 10):
            if(realClass[1] and realClass[1] == 'xx'):
                self.myTableClassUnitFee(3, _session, realClass[0], None)
            else:
                self.myTableClassUnitFee(6, _session, None, realClass[0])
                
        elif(_display == 11):
            #bio information
            if(realClass[1] and realClass[1] == 'xx'):
                self.myTableSubject(1, _session, realClass[0], None)
            else:
                self.myTableSubject(2, _session, None, realClass[0])
        else:
            pass
            #analysis
        
        
    
    def quickReport(self):
        _session = self.d_sessionData.itemData(self.d_sessionData.currentIndex())
        _clasz = self.d_classData.itemData(self.d_classData.currentIndex())
        realClass = _clasz.split(',')
        
        if(realClass[1] and realClass[1] == 'xx'):
            studentsIDs = self.getClassStudents(_session , realClass[0], 0)
        else:
            studentsIDs = self.getClassStudents(_session, realClass[0], 1)
            
        
        student_id = []
        for dx in studentsIDs :
            student_id.append(dx[0]) 
                
        
        try:
            self.document.close()
            self.document = QtGui.QTextEdit()
            doc = self.myTable1(1, self.students)
            self.document.insertHtml(doc)
            
            #self.document.setText(doc)
            self.stackRightBar.setCurrentIndex(1)
            self.hbox2x.addWidget(self.document)
            self.document.show()
        except:
            pass
            #bio information
            
 
        
    def pageDisplay(self):
        self.document.close()
        post = PrintTable(self.tabl)
        doc = post.makeTable()
        self.document = QtGui.QTextEdit()
        self.document.insertHtml(doc)
        self.stackRightBar.setCurrentIndex(1)
        self.hbox2x.addWidget(self.document)
        self.document.show()
        #return self.document
       
    def printReportPdf(self):
        report = self.report_table_holder
        lastRep = self.tableHeadersSelectorAction1()
       
        self.form = TableProfile(report[0], report[1], report[2], report[3], report[4], lastRep)
        #self.form = AccountForm()
        self.form.show()
        #rep.show()
    
    def printReportPreview(self):
        dialog = QtGui.QPrintPreviewDialog()
        dialog.setStyleSheet("table {border:1px; border-color:teal}")
        dialog.setWindowTitle('Adedoyin Adetunji')
        #dialog.showMaximized()
        #dialog.setMaximumSize(True)
        #dialog.setResolution(96)
        #dialog.setPageSize(QtGui.QPrinter.Letter)
        #dialog.setPageMargins(5, 5, 5, 10, QtGui.QPrinter.Millimeter)
        dialog.paintRequested.connect(self.handlePaintRequest)
        dialog.exec_()
    
    def handlePaintRequest(self, printer):
        document = self.document
        document.print_(printer)
        
    def lunchPrintPreview(self):
        dialog = QtGui.QPrintPreviewDialog()
        dialog.paintRequested.connect(self.handlePaintRequest)
        dialog.exec_()
        
    def lunchPrintPdf(self):
        printer = QtGui.QPrinter()
        pdffile =',,/test.pdf'
        printer.setResolution(200)
        printer.setPageSize(QtGui.QPrinter.Letter)
        printer.setOutputFormat(QtGui.QPrinter.PdfFormat)
        printer.setOutputFileName(pdffile)
        printer.setPageMargins(5, 5, 5, 10, QtGui.QPrinter.Millimeter)
        document = self.document
        #document.setPageSize(QtGui.QSizeF(printer.pageRect().size()))
        document.print_(printer)
    
    def lunchPrintCsv(self):
        #document = self.document
        pass
    
    def lunchPrintExcel(self):
        #document = self.document
        pass
        
    def lunchBack(self):
        self.stackLeftBar.setCurrentIndex(1)
        
    def lunchForward(self):
        self.stackLeftBar.setCurrentIndex(0)
        
    def mainBody(self):
        #Widgets
        self.studentToolbar()
        
        #Set button fonts
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHeightForWidth(True)
        bntstyle = "QPushButton{background-color: white; font-size: 12px; border:0px; padding:3px; margin:0px; font:Century Gothic;  text-align: left; color: darkblue}"
        picstyle = QtCore.QSize(30, 80)
        picstyle1 = QtCore.Qt.KeepAspectRatio
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        font.setFamily('Century Gothic')
        
        self.tabl = self.myTable1(0, []) #hold all tables
        self.document = QtGui.QTextEdit() #hold all reports
        
        self.f_box = QtGui.QGridLayout()  #hold primary menu
        self.f_box1 = QtGui.QGridLayout() #hold print menu
        self.f_box2 = QtGui.QGridLayout()
        self.f_box1M = QtGui.QWidget() #hold fee menu
        self.f_box1M.resize(100, 200)
        self.f_box1M.setSizePolicy(sizePolicy)
        self.f_box1M.setStyleSheet("background-color: black; color:teal")
        self.f_box1M.setLayout(self.f_box1)
        #Keep table titles
        #text
        self.tabletitle = QtGui.QLabel()
        self.tabletitle.setGeometry(QtCore.QRect(70, 80, 100, 100))
        self.tabletitle.setText('None Selected')
        self.tabletitle.setFont(QtGui.QFont('SansSerif', 18))
        self.tabletitle.setStyleSheet("background-color: white; color:teal")
        #keep button for refrsh
        #button
        self.tablerefresh = QtGui.QPushButton()
        self.tablerefresh.setFont(QtGui.QFont('SansSerif', 18))
        self.tablerefresh.setStyleSheet("background-color: white; color:white")
        refreshImg = 'img/selectall.png'
        self.tablerefresh.setIcon(QtGui.QIcon(refreshImg))
        self.connect(self.tablerefresh, QtCore.SIGNAL("clicked()"), self.tableSelectAll)
        #Keep report title
        #text
        self.reportTitle = QtGui.QLabel()
        self.reportTitle.setGeometry(QtCore.QRect(70, 80, 100, 100))
        self.reportTitle.setText('None Selected')
        self.reportTitle.setFont(QtGui.QFont('SansSerif', 18))
        self.reportTitle.setStyleSheet("background-color: white; color:teal")
        #Keep report refresh button
        #button
        self.reportRefresh = QtGui.QPushButton()
        self.reportRefresh.setFont(QtGui.QFont('SansSerif', 18))
        self.reportRefresh.setStyleSheet("background-color: white; color:white")
        self.reportRefresh.setIcon(QtGui.QIcon(refreshImg))
        self.connect(self.reportRefresh, QtCore.SIGNAL("clicked()"), self.printReportPreview)
        #Keep report print
        #button
        self.reportPrint = QtGui.QPushButton()
        self.reportPrint.setFont(QtGui.QFont('SansSerif', 18))
        self.reportPrint.setStyleSheet("background-color: white; color:white")
        printImg = 'img/printer.png'
        self.reportPrint.setIcon(QtGui.QIcon(printImg))
        self.connect(self.reportPrint, QtCore.SIGNAL("clicked()"), self.printReportPdf)
        #search table
        self.search_table = QtGui.QLineEdit()
        self.search_table.setTextMargins(5, 5, 3, 3)
        #self.search_table.setContentsMargins(10, 10, 5, 5)
        self.search_table.setFixedWidth(220)
        self.search_table.textChanged.connect(self.pullSearchTable)
        self.search_table.setPlaceholderText('Search Table ..')
        #create the Right and left stack for srudents page
        self.stackRightBar = QtGui.QStackedWidget()
        self.stackLeftBar = QtGui.QStackedWidget()
        self.checkBoxStack = QtGui.QStackedWidget()
        
        self.leftReportTable = QtGui.QWidget()  #for tables students
        self.leftReportText = QtGui.QWidget()   #for students reports
        self.rightPrimaryMenu = QtGui.QWidget() #for main students menu
        self.rightPrintMenu = QtGui.QWidget()
        self.rightFeeMenu = QtGui.QWidget()
        
        self.rightPrintMenu.setFixedHeight(180) #for print menu
        scrollArea = QtGui.QScrollArea()
        scrollArea.setWidgetResizable(True)
        scrollArea.setFixedHeight(300)
        self.rightListMenu = QtGui.QWidget(scrollArea)
        scrollArea.setWidget(self.rightListMenu)
        self.rightPrintListMenu = QtGui.QWidget() 
        
        
        #Bind students widget to stacks
        self.stackRightBar.addWidget(self.leftReportTable)
        self.stackRightBar.addWidget(self.leftReportText)
        #self.stackLeftBar.addWidget(self.rightPrimaryMenu)
        #self.stackLeftBar.addWidget(self.rightPrintListMenu)
        #self.stackLeftBar.addWidget(self.rightFeeMenu)
        
        self.hbox4 = QtGui.QHBoxLayout()
        self.hbox4.addWidget(self.tabletitle)
        self.hbox4.addStretch()
        self.hbox4.addWidget(self.search_table)
        self.hbox4.addWidget(self.reportPrint)
        self.hbox4.addWidget(self.tablerefresh)
        
        self.hbox4x = QtGui.QHBoxLayout()   
        self.hbox4x.addWidget(self.reportTitle)
        self.hbox4x.addStretch()
        #self.hbox4x.addWidget(self.reportPrint)
        self.hbox4x.addWidget(self.reportRefresh)
        
        self.hbox2 = QtGui.QVBoxLayout()
        self.hbox2.setSpacing(0)
        self.hbox2.setMargin(0)
        self.hbox2.addLayout(self.hbox4)
        self.hbox2.addWidget(self.tabl)
        
        self.hbox2x = QtGui.QVBoxLayout()
        self.hbox2x.setSpacing(0)
        self.hbox2x.setMargin(0)
        self.hbox2x.addLayout(self.hbox4x)
        
        self.hbox3 = QtGui.QHBoxLayout()
        self.hbox3.setSpacing(0)
        self.hbox3.setMargin(0)
        self.hbox3.addWidget(self.stackRightBar)
        
        self.hbox3x = QtGui.QHBoxLayout()
        self.hbox3x.setSpacing(0)
        self.hbox3x.setMargin(0)
        self.hbox3x.addWidget(self.stackLeftBar)
        
        self.leftReportTable.setLayout(self.hbox2)
        self.leftReportText.setLayout(self.hbox2x)
           
        self.Frame1 = QtGui.QFrame()
        self.Frame1.setFrameShape(QtGui.QFrame.StyledPanel)
        self.Frame1.setLayout(self.hbox3)
     
        self.b1_box = QtGui.QVBoxLayout()
        self.b2_box = QtGui.QVBoxLayout()
        self.b3_box = QtGui.QVBoxLayout()
             
        self.pbAdd = QtGui.QPushButton()
        self.pbAdd.setObjectName('Add')
        self.pbAdd.setText('Add New Student')
        self.pbAdd.setFont(font)
        self.pbAdd.setStyleSheet(bntstyle)
        self.pbAdd.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        
        self.pbProfile = QtGui.QPushButton()
        self.pbProfile.setObjectName('Profile')
        self.pbProfile.setText("Student Profile")
        self.pbProfile.setStyleSheet(bntstyle)
        self.pbProfile.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        
        self.pbEdit = QtGui.QPushButton()
        self.pbEdit.setObjectName('Edit')
        self.pbEdit.setText("Edit student data")
        self.pbEdit.setStyleSheet(bntstyle)
        self.pbEdit.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        
        self.pbMove = QtGui.QPushButton()
        self.pbMove.setObjectName('Change')
        self.pbMove.setText("Student Class")
        self.pbMove.setStyleSheet(bntstyle)
        self.pbMove.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        
        self.pbSubject = QtGui.QPushButton()
        self.pbSubject.setObjectName('Subject')
        self.pbSubject.setText("Student Subject")
        self.pbSubject.setStyleSheet(bntstyle)
        self.pbSubject.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        
        self.pbRemove = QtGui.QPushButton()
        self.pbRemove.setObjectName('Remove ')
        self.pbRemove.setText("Remove Student(s) from Class")
        self.pbRemove.setStyleSheet(bntstyle)
        self.pbRemove.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        
        self.pbPay = QtGui.QPushButton()
        self.pbPay.setObjectName('Payfees')
        self.pbPay.setText("Pay Fees")
        self.pbPay.setStyleSheet(bntstyle)
        self.pbPay.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        
        self.pbEmail = QtGui.QPushButton()
        self.pbEmail.setObjectName('email ')
        self.pbEmail.setText("Send Email")
        self.pbEmail.setStyleSheet(bntstyle)
        self.pbEmail.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        
        self.pbAcademic = QtGui.QPushButton()
        self.pbAcademic.setObjectName('academic ')
        self.pbAcademic.setText("Academic Report")
        self.pbAcademic.setStyleSheet(bntstyle)
        self.pbAcademic.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        
        self.pbAffective = QtGui.QPushButton()
        self.pbAffective.setObjectName('affective')
        self.pbAffective.setText("Affective Report")
        self.pbAffective.setStyleSheet(bntstyle)
        self.pbAffective.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        
        self.pbPsyco = QtGui.QPushButton()
        self.pbPsyco.setObjectName('psyco')
        self.pbPsyco.setText("Psychomoto Report")
        self.pbPsyco.setStyleSheet(bntstyle)
        self.pbPsyco.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        
        self.pbPhoto = QtGui.QPushButton()
        self.pbPhoto.setObjectName('Photo')
        self.pbPhoto.setText("Photo gallery")
        self.pbPhoto.setStyleSheet(bntstyle)
        self.pbPhoto.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        
        self.pbPrint = QtGui.QPushButton()
        self.pbPrint.setObjectName('print')
        self.pbPrint.setText("Print Table")
        self.pbPrint.setStyleSheet(bntstyle)
        self.pbPrint.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        
        #Print Menu Items
        self.pbPrintPrev = QtGui.QPushButton()
        self.pbPrintPrev.setObjectName('printprev')
        self.pbPrintPrev.setText("Print")
        self.pbPrintPrev.setStyleSheet(bntstyle)
        self.pbPrintPrev.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        
        self.pbPrintPdf = QtGui.QPushButton()
        self.pbPrintPdf.setObjectName('printpdf')
        self.pbPrintPdf.setText("PDF")
        self.pbPrintPdf.setStyleSheet(bntstyle)
        self.pbPrintPdf.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        
        self.pbPrintCsv = QtGui.QPushButton()
        self.pbPrintCsv.setObjectName('printcsv')
        self.pbPrintCsv.setText("CSV")
        self.pbPrintCsv.setStyleSheet(bntstyle)
        self.pbPrintCsv.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        
        self.pbPrintExcel = QtGui.QPushButton()
        self.pbPrintExcel.setObjectName('printexcel')
        self.pbPrintExcel.setText("EXCEL")
        self.pbPrintExcel.setStyleSheet(bntstyle)
        self.pbPrintExcel.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        
        self.pbBack = QtGui.QPushButton()
        self.pbBack.setObjectName('back')
        self.pbBack.setText("Menu")
        self.pbBack.setStyleSheet(bntstyle)
        self.pbBack.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        
        #general stack 
        self.pbFeeSet = QtGui.QPushButton()
        self.pbFeeSet.setObjectName('setfees')
        self.pbFeeSet.setText("Fees")
        self.pbFeeSet.setStyleSheet(bntstyle)
        self.pbFeeSet.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        
        self.pbExpenseSet = QtGui.QPushButton()
        self.pbExpenseSet.setObjectName('setexpenses')
        self.pbExpenseSet.setText("Expenses")
        self.pbExpenseSet.setStyleSheet(bntstyle)
        self.pbExpenseSet.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        
        self.pbStoreSet = QtGui.QPushButton()
        self.pbStoreSet.setObjectName('setstores')
        self.pbStoreSet.setText("Stores")
        self.pbStoreSet.setStyleSheet(bntstyle)
        self.pbStoreSet.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        
        self.pbBack1 = QtGui.QPushButton()
        self.pbBack1.setObjectName('back')
        self.pbBack1.setText("Back")
        self.pbBack1.setStyleSheet(bntstyle)
        self.pbBack1.resize(50, 100)
        
        self.connect(self.pbAdd, QtCore.SIGNAL("clicked()"), self.lunchStudentAddForm)
        self.connect(self.pbEdit, QtCore.SIGNAL("clicked()"), self.lunchStudentEditForm)
        self.connect(self.pbProfile, QtCore.SIGNAL("clicked()"), self.lunchStudentProfile)
        self.connect(self.pbMove, QtCore.SIGNAL("clicked()"), self.lunchChangeClass)
        self.connect(self.pbRemove, QtCore.SIGNAL("clicked()"), self.lunchRemoveClass)
        self.connect(self.pbSubject, QtCore.SIGNAL("clicked()"), self.lunchSubjectClass)
        self.connect(self.pbPhoto, QtCore.SIGNAL("clicked()"), self.lunchStudentAddForm)
        self.connect(self.pbPrint, QtCore.SIGNAL("clicked()"), self.lunchBack)
        self.connect(self.pbPrintPrev, QtCore.SIGNAL("clicked()"), self.printReportPdf)
        self.connect(self.pbPrintPdf, QtCore.SIGNAL("clicked()"), self.lunchPrintPreview)
        self.connect(self.pbPrintCsv, QtCore.SIGNAL("clicked()"), self.lunchPrintCsv)
        self.connect(self.pbPrintExcel, QtCore.SIGNAL("clicked()"), self.lunchPrintExcel)
        self.connect(self.pbPay, QtCore.SIGNAL("clicked()"), self.lunchPayDialog)
        self.connect(self.pbEmail, QtCore.SIGNAL("clicked()"), self.lunchStudentAddForm)
        self.connect(self.pbAcademic, QtCore.SIGNAL("clicked()"), self.academicDataPlus)
        self.connect(self.pbAffective, QtCore.SIGNAL("clicked()"), self.affectiveDataPlus)
        self.connect(self.pbPsyco, QtCore.SIGNAL("clicked()"), self.psychoDataPlus)
        self.connect(self.pbBack, QtCore.SIGNAL("clicked()"), self.lunchForward)
        self.connect(self.pbFeeSet, QtCore.SIGNAL("clicked()"), self.lunchFeeDialog)
        self.connect(self.pbExpenseSet, QtCore.SIGNAL("clicked()"), self.lunchExpenseDialog)
        self.connect(self.pbStoreSet, QtCore.SIGNAL("clicked()"), self.lunchStoreDialog)
        self.connect(self.pbBack1, QtCore.SIGNAL("clicked()"), self.lunchForward)
        
        addImg = QtGui.QPixmap('img/add.png').scaled(picstyle, picstyle1)
        editImg = QtGui.QPixmap('img/edit.png').scaled(picstyle, picstyle1)
        profileImg = QtGui.QPixmap('img/profile.png').scaled(picstyle, picstyle1)
        moveImg = QtGui.QPixmap('img/change.png').scaled(picstyle, picstyle1)
        removeImg = QtGui.QPixmap('img/remove.png').scaled(picstyle, picstyle1)
        subjectImg = QtGui.QPixmap('img/remove.png').scaled(picstyle, picstyle1)
        payImg = QtGui.QPixmap('img/pay.png').scaled(picstyle, picstyle1)
        emailImg = QtGui.QPixmap('img/email.png').scaled(picstyle, picstyle1)
        academicImg = QtGui.QPixmap('img/academic.png').scaled(picstyle, picstyle1)
        affectiveImg = QtGui.QPixmap('img/affective.png').scaled(picstyle, picstyle1)
        psycoImg = QtGui.QPixmap('img/psyco.png').scaled(picstyle, picstyle1)
        photoImg = QtGui.QPixmap('img/users.png').scaled(picstyle, picstyle1)
        printImg = QtGui.QPixmap('img/printer.png').scaled(picstyle, picstyle1)
        printPrevImg = QtGui.QPixmap('img/printer.png').scaled(picstyle, picstyle1)
        printPdfImg = QtGui.QPixmap('img/printer.png').scaled(picstyle, picstyle1)
        printCsvImg = QtGui.QPixmap('img/printer.png').scaled(picstyle, picstyle1)
        printExcelImg = QtGui.QPixmap('img/printer.png').scaled(picstyle, picstyle1)
        backImg = QtGui.QPixmap('img/printer.png').scaled(picstyle, picstyle1)
        setFeeImg = QtGui.QPixmap('img/money.png').scaled(picstyle, picstyle1)
        setExpenseImg = QtGui.QPixmap('img/debit-card.png').scaled(picstyle, picstyle1)
        setStoreImg = QtGui.QPixmap('img/warehouse.png').scaled(picstyle, picstyle1)
        backImg1 = QtGui.QPixmap('img/printer.png').scaled(picstyle, picstyle1)
       
        
        self.picAdd = QtGui.QLabel()
        self.picAdd.setPixmap(addImg)
        self.picEdit = QtGui.QLabel()
        self.picEdit.setPixmap(editImg)
        self.picProfile = QtGui.QLabel()
        self.picProfile.setPixmap(profileImg)
        self.picMove = QtGui.QLabel()
        self.picMove.setPixmap(moveImg)
        self.picRemove = QtGui.QLabel()
        self.picRemove.setPixmap(removeImg)
        self.picSubject = QtGui.QLabel()
        self.picSubject.setPixmap(subjectImg)
        self.picPay = QtGui.QLabel()
        self.picPay.setPixmap(payImg)
        self.picEmail = QtGui.QLabel()
        self.picEmail.setPixmap(emailImg)
        self.picAcademic = QtGui.QLabel()
        self.picAcademic.setPixmap(academicImg)
        self.picAffective = QtGui.QLabel()
        self.picAffective.setPixmap(affectiveImg)
        self.picPsyco = QtGui.QLabel()
        self.picPsyco.setPixmap(psycoImg)
        self.picPrint = QtGui.QLabel()
        self.picPrint.setPixmap(printImg)
        self.picPrevPrint = QtGui.QLabel()
        self.picPrevPrint.setPixmap(printPrevImg)
        self.picPdfPrint = QtGui.QLabel()
        self.picPdfPrint.setPixmap(printPdfImg)
        self.picCsvPrint = QtGui.QLabel()
        self.picCsvPrint.setPixmap(printCsvImg)
        self.picExcelPrint = QtGui.QLabel()
        self.picExcelPrint.setPixmap(printExcelImg)
        self.picPhoto = QtGui.QLabel()
        self.picPhoto.setPixmap(photoImg)
        self.picBack = QtGui.QLabel()
        self.picBack.setPixmap(backImg)
        self.picFeeSet = QtGui.QLabel()
        self.picFeeSet.setPixmap(setFeeImg)
        self.picExpenseSet = QtGui.QLabel()
        self.picExpenseSet.setPixmap(setExpenseImg)
        self.picStoreSet = QtGui.QLabel()
        self.picStoreSet.setPixmap(setStoreImg)
        self.picBack1 = QtGui.QLabel()
        self.picBack1.setPixmap(backImg1)
        
        
        #Left main menu
        self.f_box.addWidget(self.picProfile, 1, 0)
        self.f_box.addWidget(self.pbProfile, 1, 1)
        self.f_box.addWidget(self.picAdd, 0, 0)
        self.f_box.addWidget(self.pbAdd, 0, 1)
        self.f_box.addWidget(self.picEdit, 2, 0)
        self.f_box.addWidget(self.pbEdit, 2, 1)
        self.f_box.addWidget(self.picMove, 3, 0)
        self.f_box.addWidget(self.pbMove, 3, 1)
        self.f_box.addWidget(self.picSubject, 4, 0)
        self.f_box.addWidget(self.pbSubject, 4, 1)
        self.f_box.addWidget(self.picPhoto, 5, 0)
        self.f_box.addWidget(self.pbPhoto, 5, 1)
        self.f_box.addWidget(self.picPay, 6, 0)
        self.f_box.addWidget(self.pbPay, 6, 1)
        self.f_box.addWidget(self.picEmail, 7, 0)
        self.f_box.addWidget(self.pbEmail, 7, 1)
        self.f_box.addWidget(self.picAcademic, 8, 0)
        self.f_box.addWidget(self.pbAcademic, 8, 1)
        self.f_box.addWidget(self.picAffective, 9, 0)
        self.f_box.addWidget(self.pbAffective, 9, 1)
        self.f_box.addWidget(self.picPsyco, 10, 0)
        self.f_box.addWidget(self.pbPsyco, 10, 1)
        #self.f_box.addWidget(self.picPrevPrint, 11, 0)
        #self.f_box.addWidget(self.pbPrintPrev, 11, 1)
        #self.f_box.addWidget(self.picPrint, 12, 0)
        #self.f_box.addWidget(self.pbPrint, 12, 1)
        
        #Left print menu
        #self.f_box1.addWidget(self.picBack, 0, 0)
        #self.f_box1.addWidget(self.pbBack, 0, 1)
        
        #Left print menu
        self.f_box2.addWidget(self.picFeeSet, 0, 0)
        self.f_box2.addWidget(self.pbFeeSet, 0, 1)
        self.f_box2.addWidget(self.picExpenseSet, 1, 0)
        self.f_box2.addWidget(self.pbExpenseSet, 1, 1)
        self.f_box2.addWidget(self.picStoreSet, 2, 0)
        self.f_box2.addWidget(self.pbStoreSet, 2, 1)
        #self.f_box2.addWidget(self.picBack1, 3, 0)
        #self.f_box2.addWidget(self.pbBack1, 3, 1)
        
        self.b_box = QtGui.QHBoxLayout()
        self.b_box.addLayout(self.b1_box)
        self.b_box.addLayout(self.b2_box)
        self.b_box.addLayout(self.b3_box)
        
        frm_search  = QtGui.QHBoxLayout()
        self.search_box = QtGui.QLineEdit()
        self.search_box.setTextMargins(5, 5, 5, 5)
        self.search_box.setContentsMargins(10, 10, 5, 5)
        self.search_box.textChanged.connect(self.pullSearch)
        self.search_box.setPlaceholderText('Search Student ..')
        frm_search.addWidget(self.search_box)
        
        #Table titles
        self.bioTable = ['id','Sch.No.', 'FullName', 'Class','Gender', 'Birth Date', 'Nationality', 'State/LGA', 'Address']
        self.conTable  = ['id','Sch.No.', 'Fullname', 'Class', 'First Guardian', 'Phone No.', 'Second Gurdian', 'Phone No.']
        self.acaTable  = ['id','Sch.No.', 'Fullname', 'Class']
        self.affTable  = ['id','Sch.No.', 'Fullname', 'Class']
        self.psyTable  = ['id','Sch.No.', 'Fullname', 'Class']
        self.classUnitTable  = ['id','Class', 'Unit', 'Male', 'Female', 'Total']
        self.classTable  = ['id','Class', 'Male', 'Female', 'Total']
        self.classUnitFeeTable  = ['id','Class', 'Unit', 'Male', 'Female', 'Population', 'Fee', 'Amount', 'Total Amount', 'Total Paid', 'Balance' ]
        self.classFeeTable  = ['id','Class','Students', 'Fees', 'Paid', 'Balance' ]
        
         
        self.hc1_box = QtGui.QVBoxLayout()
        self.f_boxx = QtGui.QVBoxLayout()
        self.f_boxx.addLayout(self.hc1_box)
        
        self.f_box1MM = QtGui.QVBoxLayout()
        self.f_box1MM.addWidget(self.f_box1M)
        self.rightPrintMenu.setLayout(self.f_box1MM) #for print menu
        self.rightListMenu.setLayout(self.f_boxx)
        
        sub_box = QtGui.QVBoxLayout()
        sub_box.addWidget(self.rightPrintMenu)
        sub_box.addWidget(scrollArea)
        
        self.rightPrimaryMenu.setLayout(self.f_box)
        self.rightPrimaryMenu.setSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed )
        self.rightPrintListMenu.setLayout(sub_box)
        
        self.rightFeeMenu.setLayout(self.f_box2)
        self.rightFeeMenu.setMaximumHeight(200)
        self.rightFeeMenu.setSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum )
        
        self.Frame2 = QtGui.QVBoxLayout()
        #self.Frame2.addLayout(frm_search)
        search_Widget = QtGui.QWidget()
        search_Widget.setContentsMargins(0, 0, 0, 0)
        search_Widget.setLayout(frm_search)
        
        self.t_box = QtGui.QToolBox()
        self.t_box.setMinimumHeight(600)
        self.t_box.setContentsMargins(0, 0, 0, 0)
        self.t_box.addItem(self.rightPrimaryMenu, 'Student')
        self.t_box.addItem(self.rightPrintListMenu, 'Format Table')
        self.t_box.addItem(self.rightFeeMenu, 'Fees')
        
        self.Frame2.addWidget(search_Widget)
        self.Frame2.addWidget(self.t_box)
        self.Frame2.addLayout(self.hbox3x)
        self.Frame2.addLayout(self.b_box)
        
        v_widget = QtGui.QWidget()
        v_widget.setFixedWidth(220)
        v_widget.setStyleSheet("background-color: white")
        v_widget.setContentsMargins(0, 0, 0, 0)
        v_widget.setFont(font)
        v_widget.setLayout(self.Frame2)
        
        self.Splitter1 = QtGui.QSplitter(QtCore.Qt.Horizontal)
        self.Splitter1.setStyleSheet("background-color: #fff")
        self.Splitter1.setContentsMargins(0, 0, 0, 0)
        self.Splitter1.addWidget(v_widget)
        self.Splitter1.addWidget(self.Frame1)
        
        h_box = QtGui.QHBoxLayout(self)
        h_box.addWidget(self.Splitter1)
        h_box.setContentsMargins(0, 0, 0, 0)
        
        self.mainStack.setCurrentIndex(0)
        self.stackRightBar.setCurrentIndex(0)
        self.stackLeftBar.setCurrentIndex(0)
        #Create central widget, add layout and set
        self.studentStack.setStyleSheet("background-color: white")
        self.studentStack.setLayout(h_box)
        
        #full bar
        tree_id = 0
        tree1 = QtGui.QTreeWidget()
        tree1.setHeaderLabel("Quick Menu")
        tree1.setContentsMargins(0, 0, 0, 0)
        tree1.setMinimumHeight(600)
        parent1 = QtGui.QTreeWidgetItem(tree1)
        parent1.setText(0, "Classes")
        parent1.setFlags(parent1.flags() | QtCore.Qt.ItemIsTristate | QtCore.Qt.ItemIsUserCheckable)
        self.hold_tree = {}
        self.post_tree = {}
        self.hold_tree[tree_id] = parent1
        self.post_tree[tree_id] = 'c-x'
        tree_id += 1
        itz = self.pullClass(1)
        for k in itz:
           act = str(itz[k])
           child = QtGui.QTreeWidgetItem(parent1)
           child.setFlags(child.flags() | QtCore.Qt.ItemIsTristate | QtCore.Qt.ItemIsUserCheckable) 
           child.setText(0, str(act).upper())
           self.hold_tree[tree_id] = child
           self.post_tree[tree_id] = 'cl-'+str(k)
           tree_id += 1
           #child.setCheckState(0, QtCore.Qt.Checked)
           arr = self.pullClass(k)
           for j in arr:
               act1 = str(arr[j])
               child1 = QtGui.QTreeWidgetItem(child)
               child1.setFlags(child1.flags()) 
               child1.setText(0, str(act1).upper())
               self.hold_tree[tree_id] = child1
               self.post_tree[tree_id] = 'cls-'+str(j)
               tree_id += 1
               
               
        parent2 = QtGui.QTreeWidgetItem(tree1)
        parent2.setText(0, "Staff")
        parent2.setFlags(parent2.flags() | QtCore.Qt.ItemIsTristate | QtCore.Qt.ItemIsUserCheckable)
        self.hold_tree[tree_id] = parent2
        self.post_tree[tree_id] = 'st-x'
        tree_id += 1
        
        parent3 = QtGui.QTreeWidgetItem(tree1)
        parent3.setText(0, "Expenses")
        parent3.setFlags(parent1.flags() | QtCore.Qt.ItemIsTristate | QtCore.Qt.ItemIsUserCheckable)
        self.hold_tree[tree_id] = parent3
        self.post_tree[tree_id] = 'ex-x'
        tree_id += 1
        tree1.itemClicked.connect(lambda state: self.getTree())
        
        
        s_v_widget1 = QtGui.QWidget()
        s_v_widget1.setFixedWidth(200)
        s_v_widget1.setStyleSheet("background-color: white")
        s_v_widget1.setContentsMargins(0, 0, 0, 0)
        s_v_widget1.setFont(font)
        #s_v_widget1.setLayout(self.s_frame1)
        
        s_v_widget2 = QtGui.QWidget()
        s_v_widget2.setStyleSheet("background-color: grey")
        s_v_widget2.setContentsMargins(0, 0, 0, 0)
        s_v_widget2.setFont(font)
        s_v_widget2.setSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed )
        s_v_widget2_hbox = QtGui.QVBoxLayout()
        s_v_widget2_hbox.setContentsMargins(2, 8, 0, 0)
        s_v_widget2_hbox_title = QtGui.QLabel("<span style='color:white; padding-top:10px'><b>Administrative Management Tools</b></span>")
        s_v_widget2_hbox_title.setFixedHeight(20)
        s_v_widget2_hbox_body = QtGui.QFrame()
        s_v_widget2_hbox_body.setFrameShape(QtGui.QFrame.StyledPanel)
        s_v_widget2_hbox_body.setFrameShadow(QtGui.QFrame.Sunken)
        s_v_widget2_hbox_body.setStyleSheet("background-color: dimgray")
        s_v_widget2_hbox.addWidget(s_v_widget2_hbox_title)
        s_v_widget2_hbox.addWidget(s_v_widget2_hbox_body)
        s_v_widget2.setLayout(s_v_widget2_hbox)
        
        s_v_widget3 = QtGui.QWidget()
        s_v_widget3.setFixedWidth(300)
        s_v_widget3.setStyleSheet("background-color: #101010")
        s_v_widget3.setContentsMargins(0, 0, 0, 0)
        s_v_widget3.setFont(font)
       # s_v_widget3.setLayout(self.s_frame3)
        
        self.s_frame1 = QtGui.QFrame(s_v_widget1)
        self.s_frame1.setFrameShape(QtGui.QFrame.StyledPanel)
        self.s_frame1.setFrameShadow(QtGui.QFrame.Sunken)
        self.s_frame1.setContentsMargins(0, 0, 0, 0)
        
        s_hh_b = QtGui.QHBoxLayout()
        s_hh_b.setContentsMargins(0, 0, 0, 0)
        s_hh_b.addWidget(tree1)
        self.s_frame1.setLayout(s_hh_b)
        #s_f_header = QtGui.QHeaderView(QtCore.Qt.Horizontal, self.s_frame1)
    
        
        #s_w = QtGui.QWidget()
        nImg = QtGui.QImage('img/add.png')
        
        self.scrollArea1 = QtGui.QScrollArea()
        self.scrollArea1.setWidgetResizable(True)
        self.scrollArea1.setMinimumHeight(100)
        self.scrollArea1.setFixedSize(300, 620)
        self.scrollArea1.setContentsMargins(0, 0, 0, 0)
   
        
        self.scrollContent = QtGui.QWidget()
        self.s_grid = QtGui.QGridLayout()
        self.scrollContent.setLayout(self.s_grid)
        #self.s_grid.setStyleSheet("backgound-color: green; ")
        self.s_grid_header = QtGui.QLabel("JSS 3")
        #s_grid.addWidget(s_grid_header, 0, 0, 2)
        for i in range(0):
            p = QtGui.QPainter()
            p.setPen(QtCore.Qt.white)
            p.drawText(nImg.rect(), QtCore.Qt.AlignCenter, "Adedoyin Charles Adetunji")
            p.setFont(QtGui.QFont("Arial", 12))
            lb1 = QtGui.QLabel()
            lb1.setPixmap(QtGui.QPixmap.fromImage(nImg.scaled(30, 30, QtCore.Qt.IgnoreAspectRatio)))
            lb1.setAlignment(QtCore.Qt.AlignLeft)
            lb1.setMaximumHeight(30)
            lb1.setMaximumWidth(31)
            lb2 = QtGui.QLabel("<html><span color='white'>Adedoyin Charles  </span><br><span style='color:#4C4D4F'> Male</span></html>")
            lb2.setFont(QtGui.QFont("Tahoma", 9))
            lb2.setStyleSheet("color: white; border-bottom:1px inset #4C4D4F")
            lb2.setFixedWidth(270)
            lb2.setFixedHeight(30)
            self.s_grid.addWidget(lb1, i+1, 0)
            self.s_grid.addWidget(lb2, i+1, 1)
        #s_grid.addWidget(p, 0, 1)
        self.scrollContent.setSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed )
        self.scrollArea1.setWidget(self.scrollContent)
        
        
        self.scroll_h_box = QtGui.QVBoxLayout()
        self.scroll_h_box.addWidget(self.scrollArea1)
        self.scroll_h_box.setContentsMargins(0, 0, 0, 0)
        
        self.s_frame3 = QtGui.QFrame(s_v_widget3)
        self.s_frame3.setMaximumHeight(620)
        self.s_frame3.setLayout(self.scroll_h_box)
         
        self.staff_Splitter1 = QtGui.QSplitter(QtCore.Qt.Horizontal)
        self.staff_Splitter1.setStyleSheet("background-color: grey")
        self.staff_Splitter1.setContentsMargins(0, 0, 0, 0)
        self.staff_Splitter1.addWidget(s_v_widget1)
        self.staff_Splitter1.addWidget(s_v_widget2)
        self.staff_Splitter1.addWidget(s_v_widget3)
        
        staff_main_box = QtGui.QHBoxLayout(self)
        staff_main_box.addWidget(self.staff_Splitter1)
        staff_main_box.setContentsMargins(0, 0, 0, 0)
        
        #self.staffStack.setStyleSheet("background-color: white")
        self.staffStack.setLayout(staff_main_box)
   
    def getTree(self):
        trees = self.hold_tree
        post = self.post_tree
        
        for a in trees:
            if trees[a].isSelected():
                val = post[a]
            
        v = val.split('-')
        v_name = v[0] #tag name
        v_id = v[1] #tag code
        
        
        if str(v_name) == 'cl':
            '''
            select all students from this class
            '''
            cn = StudentTable(self.mainTermSession, [None],[v_id], [None])
            raw_students = cn.classStudent()
            cl = self.getDataById(v_id)
            title = str(cl['name']).upper()+" Class"
            self.getTreeStudents(raw_students, title)
            
        if str(v_name) == 'cls':
            '''
            select all students from this class unit
            '''
            cn = StudentTable(self.mainTermSession, [None], [None], [v_id])
            raw_students = cn.classUnitStudent()
            cl = self.getDataById(v_id)
            cl1 =self.getDataById(cl['subID'])
            title = str(cl1['name']).upper()+str(cl['abbrv']).upper()+" Class"
            self.getTreeStudents(raw_students, title)
            
            
    def getTreeStudents(self, persons, title):
        '''
        put all persons in coloumn (dark column)
        photo, name, sex
        '''
        for i in reversed(range(self.s_grid.count())):
            self.s_grid.takeAt(i).widget().deleteLater()
            
        s_grid_header = QtGui.QLabel("<h2 style='color:white'>"+ title +"</h2>")
        self.s_grid.addWidget(s_grid_header, 0, 0, 1, 2)
        k = 1
        for i in persons:
            fullname = str(i[1])+" "+ str(i[2])+" "+ str(i[3])+" "+str(i[4])
            if i[6] == 0:
                sex = 'Male'
            else:
                sex = 'Female'
            nImg ='img/add.png'
            lb1 = QtGui.QPushButton()
            lb1.setIcon(QtGui.QIcon(nImg))
            lb1.setMaximumHeight(30)
            lb1.setMaximumWidth(31)
            lb1.setContentsMargins(0 ,0, 0, 0)
            lb1.setStyleSheet("border:none; padding:0px;marging:0px")
            lb2 = QtGui.QLabel("<html><span color='white'>"+ fullname.title() +"  </span><br><span style='color:#4C4D4F'>"+ sex +"</span></html>")
            lb2.setFont(QtGui.QFont("Tahoma", 9))
            lb2.setStyleSheet("color: white; border-bottom:1px inset #4C4D4F")
            lb2.setFixedWidth(270)
            lb2.setFixedHeight(30)
            self.s_grid.addWidget(lb1, k, 0)
            self.s_grid.addWidget(lb2, k, 1)
            k += 1
        #s_grid.addWidget(p, 0, 1)
        #self.s_frame3.setLayout(self.s_grid)
        #self.s_frame3.show()
        
    def windowMain(self):
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        font.setFamily('Tahoma')
        
        self.winBox = QtGui.QVBoxLayout(self)
        self.winBox.setContentsMargins(0, 0, 0, 0)
        #self.welcomeStack.setStyleSheet("background-image: url(img/win1.jpg); background-position:center;  background-size:contain; background-repeat:no-repeat")
        hHtml = '''<html><body><h2>Miracle College</h2></body></html>
        '''
        topWidget = QtGui.QWidget()
        topWidget.setContentsMargins(0, 0, 0, 0)
        topWidget.setMinimumHeight(250)
        topWidget.setStyleSheet("background-image: url(img/win1.jpg); background-position:center;  background-size:contain; background-repeat:no-repeat")
        
        topLabel = QtGui.QLabel(hHtml)
        topLabel.move(40, 100)
        
        bottomWidget = QtGui.QWidget()
        bottomWidget.setContentsMargins(0, 0, 0, 0)
        bottomWidget.setStyleSheet("background-color: white")
        bottom_box = QtGui.QHBoxLayout()
        bottomWidget.setLayout(bottom_box)
        
        cardWidget = QtGui.QWidget()
        cardWidgetBox = QtGui.QVBoxLayout()
        cardWidgetBox.setContentsMargins(0, 0, 0, 0)
        cardWidget.setFixedHeight(320)
        cardWidget.setFixedWidth(200)
        cardWidget.move(40, 40)
        cardWidget.setStyleSheet("background-color:rgb(250,250,255); border-size: 2px;border-color: darkblue  ")
        cardWidget.setLayout(cardWidgetBox)
        
        
        cardWidgetImg = QtGui.QWidget()
        cardWidgetImg.setFixedHeight(120)
        cardWidgetImg.setFixedWidth(200)
        cardWidgetImg.setContentsMargins(0, 0, 0, 0)
        #cardWidgetImg.setStyleSheet("background-color: skyblue")
        cardWidgetImg.setStyleSheet("background: rgb(2,0,36); background-image: url(img/studentcartoon.png); background-position:center;  background-size:contain; background-repeat:no-repeat")

        cardWidgetImg.move(0, 0)
        cardWidgetLbl = QtGui.QLabel('Male')
        cardWidgetBox.addWidget(cardWidgetImg)
        cardWidgetBox.addStretch()
        cardWidgetBox.addWidget(cardWidgetLbl)
        
        cardWidget1 = QtGui.QWidget()
        cardWidget1.setFixedHeight(320)
        cardWidget1.setFixedWidth(200)
        cardWidget1.move(40, 40)
        cardWidget1.setStyleSheet("background-color: darkblue")
        
        cardWidget2 = QtGui.QWidget()
        cardWidget2.setFixedHeight(320)
        cardWidget2.setFixedWidth(200)
        cardWidget2.move(40, 40)
        cardWidget2.setStyleSheet("background-color: darkblue")
        
        cardWidget3 = QtGui.QWidget()
        cardWidget3.setFixedHeight(320)
        cardWidget3.setFixedWidth(200)
        cardWidget3.move(40, 40)
        cardWidget3.setStyleSheet("background-color: darkblue")
        
        bottom_box.addWidget(cardWidget)
        bottom_box.addWidget(cardWidget1)
        bottom_box.addWidget(cardWidget2)
        bottom_box.addWidget(cardWidget3)
        
        self.winBox.addWidget(topWidget)
        self.winBox.addWidget(bottomWidget)
        
        self.welcomeStack.setLayout(self.winBox)
        self.wBox = QtGui.QWidget()
        self.wBox.setFixedWidth(220)
        self.wBox.setStyleSheet("background-color: white")
        self.wBox.setFont(font)
        #self.wBox.setLayout(self.Frame2)
        self.wBox.setStyleSheet("background-color: white; width:300px; height:200px")
        self.winBox.addWidget(self.wBox)     
        self.wBox.show()
        
    def tableHeadersSelector(self, primecol, state = None):
        try:
            self.f_boxx.removeWidget(self.tree1)
        except:
            pass
        
        self.tree1 = QtGui.QTreeWidget()
        self.tree1.clear()
        self.tree1.setHeaderLabel("Add/Remove Column")
        self.hold_checkbox = {}
        parent1 = QtGui.QTreeWidgetItem(self.tree1)
        parent1.setText(0, "Select")
        parent1.setFlags(parent1.flags() | QtCore.Qt.ItemIsTristate | QtCore.Qt.ItemIsUserCheckable)
        if primecol and len(primecol) > -1:
            ko = 0
            if state and state == 1: 
                for val in primecol:
                    if isinstance(primecol[val], dict):
                        child = QtGui.QTreeWidgetItem(parent1)
                        child.setFlags(child.flags() | QtCore.Qt.ItemIsTristate | QtCore.Qt.ItemIsUserCheckable) 
                        child.setText(0, str(val).upper())                        
                        child.setCheckState(0, QtCore.Qt.Checked)
                        for v in primecol[val]:
                            child2 = QtGui.QTreeWidgetItem(child)
                            child2.setFlags(child2.flags() | QtCore.Qt.ItemIsTristate | QtCore.Qt.ItemIsUserCheckable)
                            child2.setText(0, primecol[val][v])
                            self.hold_checkbox[v] = child2
                            ko += 1
                            #self.hold_checkbox[ko] = child
                            child2.setCheckState(0, QtCore.Qt.Checked)
                        
                    else:
                        child = QtGui.QTreeWidgetItem(parent1)
                        child.setFlags(child.flags() | QtCore.Qt.ItemIsUserCheckable) 
                        child.setText(0, str(primecol[val]).upper())                        
                        self.hold_checkbox[ko] = child
                        child.setCheckState(0, QtCore.Qt.Checked)
                        
                        ko += 1
            
            else:
                for val in primecol:
                        child = QtGui.QTreeWidgetItem(parent1)
                        child.setFlags(child.flags() | QtCore.Qt.ItemIsUserCheckable) 
                        child.setText(0, str(val).upper())                        
                        self.hold_checkbox[ko] = child
                        child.setCheckState(0, QtCore.Qt.Checked)
                        ko += 1
            
            self.tree1.itemClicked.connect(self.tableHeadersSelectorAction)
            self.f_boxx.addWidget(self.tree1)
    
    
    def tableHeadersSelectorAction(self):
        '''
        show or hide column from side bar
        '''
        for i in self.hold_checkbox:
            if self.hold_checkbox[i].checkState(0) == QtCore.Qt.Checked:
                self.table.showColumn(i)
            else:
                self.table.hideColumn(i)
     
        self.table.hideColumn(0)
        
    def tableHeadersSelectorAction1(self):
        '''
        show or hide column from side bar
        '''
        check_arr = []
        for i in self.hold_checkbox:
            if self.hold_checkbox[i].checkState(0) == QtCore.Qt.Checked:
                check_arr.append(i)
            else:
                pass
       
        return check_arr 
        
    def mySelectTable(self):
        '''
        get the selected rpws in a table
        returns list or row ids
        '''
        sels = self.tabl.selectedIndexes()
        sels = self.tabl.selectionModel().selectedRows()
        
        park = []
        park1 = []
        for j in sels:
            park.append(j.row()) 
            
            
        for i in set(park):
            selected = self.tabl.item(i, 0).text()
            park1.append(selected)
            
        return park1
    
    def tableSelectAll(self):
        '''
        select or deseletc all rows in a table
        for further action
        '''
        sels = self.mySelectTable()
        
        if(len(sels) > 0):
                self.tabl.selectionModel().clearSelection()
        else:
                self.tabl.selectAll()
       
        
    def moveStudent(self, b, c, a):
        '''
        move student from one class to another
        needs current 
        session (b), 
        list of students (c)
        class to move students to (a)
        '''
        self.form = StudentTable(b, [None], a, [None] )
        p = self.form.classMoveStudent(b, c, a)
        return p
    
    def classActMove(self, b):
        li = self.mySelectTable()
        li2 = self.moveStudent(b, 29, li)
        return li2
    
    def myTableClassUnit(self, state, session):       
        #get list of students
        cn = Dat()
        
        data = cn.studentClassUnitData(session)
        
        al = {}
        for p in data:
            al[p['cid']] = {}
            al[p['cid']]['cname'] = p['clasz']
            al[p['cid']]['name'] = p['classname']
            
        for k in data:
            if k['sex'] == 0:
                al[k['cid']]['0'] = k['id']
            elif k['sex'] == 1:
                al[k['cid']]['1'] = k['id']
         
        #all table headers titles
        cols = ['ID', 'CLASS', 'UNIT', 'MALE', 'FEMALE', 'TOTAL']
        self.tableHeadersSelector(cols)
       
        print_header = {}
        kk = 0
        for a in cols:
            print_header[kk] = a
            kk += 1
            
        if state == 0:
            # initiate table if not exist
            if hasattr(Window, 'table'):
                pass
            else:
                self.table = QtGui.QTableWidget()
            
            
            #header
            header = self.table.horizontalHeader()
            header.setResizeMode(QtGui.QHeaderView.ResizeToContents)
            header.setStretchLastSection(True)
            header.setStyleSheet(self.tableHeaderStyle)
            vheader = self.table.verticalHeader()
            vheader.setStyleSheet(self.tableHeaderStyle)
            # Body
            self.table.setWindowTitle("Class Units")
            self.table.resize(900, 450)
            self.table.setFont(self.tableFont)
            self.table.setSortingEnabled(2)
            self.table.resizeColumnsToContents()
            self.table.setRowCount(len(al))
            self.table.setColumnCount(len(cols))
            self.table.setHorizontalHeaderLabels(cols)
            self.table.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
            self.table.customContextMenuRequested.connect(self.handleHeaderMenu)
            self.table.hideColumn(0)
            self.table.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
            self.table.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
            self.table.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
            
            i = 0
            l = 0
            print_body = {}
            ma_arr = []
            fe_arr = []
            total_arr = []
            for q in al:
                #row id
                self.table.setItem(i, 0, QtGui.QTableWidgetItem(str(q)))
                self.table.setItem(i, 1, QtGui.QTableWidgetItem(str(al[q]['cname']).upper()))
                self.table.setItem(i, 2, QtGui.QTableWidgetItem(str(al[q]['name']).upper()))
                if  (str(0) in al[q]) and (int(al[q][str(0)]) > 0):
                    ma = str(al[q][str(0)])
                else:
                    ma = str(0)
                    
                if(str(1) in al[q]) and (int(al[q][str(1)]) > 0):
                    fe = str(al[q][str(1)])
                else:
                    fe = str(0)
                ma_arr.append(int(ma))  
                fe_arr.append(int(fe))
                self.table.setItem(i, 3, QtGui.QTableWidgetItem(str(ma)))
                self.table.setItem(i, 4, QtGui.QTableWidgetItem(str(fe)))
                total = int(ma) + int(fe)
                total_arr.append(total)
                self.table.setItem(i, 5, QtGui.QTableWidgetItem(str(total)))
                
                print_body1 = {}
                print_body1[0] = l + 1
                print_body1[1] = str(al[q]['cname']).upper()
                print_body1[2] = str(al[q]['name']).upper()
                print_body1[3] = str(ma)
                print_body1[4] = str(fe)
                print_body1[5] = str(total)
                
                print_body[q] = print_body1
                i += 1
                l += 1
                
            mas = sum(ma_arr)
            fes = sum(fe_arr)
            totals = sum(total_arr)
            
            self.table.setItem(i, 0, QtGui.QTableWidgetItem(str('SN')))
            self.table.setItem(i, 1, QtGui.QTableWidgetItem(''))
            self.table.setItem(i, 2, QtGui.QTableWidgetItem(str('TOTAL')))
            self.table.setItem(i, 3, QtGui.QTableWidgetItem(str(mas)))
            self.table.setItem(i, 4, QtGui.QTableWidgetItem(str(fes)))
            self.table.setItem(i, 5, QtGui.QTableWidgetItem(str(totals)))
            
            print_footer = {}
            print_footer[0] = 'SN.'
            print_footer[1] = str('')
            print_footer[2] = str('TOTAL')
            print_footer[3] = str(mas)
            print_footer[4] = str(fes)
            print_footer[5] = str(totals)
                
            print_format = {}
            print_format[0] = 'class="centers" align="center" style="text-align:center;"'
            print_format[1] = 'align="" style="text-align:left;"'
            print_format[2] = ''
            print_format[3] = 'class="centers" align="center" style="text-align:center;"'
            print_format[4] = 'class="centers" align="center" style="text-align:center;"'
            print_format[5] = 'class="centers" align="center" style="text-align:center;"'
            
            
            self.report_table_holder = [session, print_header, print_body, print_footer, print_format]
            self.tabl.close()
            self.tabl = self.table
            self.stackRightBar.setCurrentIndex(6)
            self.stackLeftBar.setCurrentIndex(0)
            self.checkBoxStack.setCurrentIndex(0)
            self.hbox2.addWidget(self.tabl)
            self.tabl.show()
        #report view
        elif state == 1:
            pass
    
    def myTableClassFee(self, state, session):       
        #get list of students
        cn = Dat()
        data = cn.studentClassFee(session)
        al = {}
        for p in data:
            al[p['cid']] = {}
            al[p['cid']]['cname'] = p['clasz']
            al[p['cid']]['name'] = p['classname']
            al[p['cid']]['fee'] = p['fee']
            al[p['cid']]['amount'] = p['amount']
            
        for k in data:
            if k['sex'] == 0:
                al[k['cid']]['0'] = k['id']
            elif k['sex'] == 1:
                al[k['cid']]['1'] = k['id']
         
        #all table headers titles
        cols = self.classUnitFeeTable
        self.tableHeadersSelector(cols)
            
        if state == 0:
            # initiate table if not exist
            if hasattr(Window, 'table'):
                pass
            else:
                self.table = QtGui.QTableWidget()
            
            
            #header
            header = self.table.horizontalHeader()
            header.setResizeMode(QtGui.QHeaderView.ResizeToContents)
            header.setStretchLastSection(True)
            header.setStyleSheet(self.tableHeaderStyle)
            vheader = self.table.verticalHeader()
            vheader.setStyleSheet(self.tableHeaderStyle)
            # Body
            self.table.setWindowTitle("Class Units")
            self.table.resize(900, 750)
            self.table.setFont(self.tableFont)
            self.table.setSortingEnabled(2)
            self.table.resizeColumnsToContents()
            self.table.setRowCount(len(al))
            self.table.setColumnCount(len(cols))
            self.table.setHorizontalHeaderLabels(cols)
            self.table.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
            self.table.customContextMenuRequested.connect(self.handleHeaderMenu)
            self.table.hideColumn(0)
            self.table.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
            self.table.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
            self.table.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
            
            i = 0
            for q in al:
                #row id
                self.table.setItem(i, 0, QtGui.QTableWidgetItem(str(q)))
                self.table.setItem(i, 1, QtGui.QTableWidgetItem(str(al[q]['cname'])))
                self.table.setItem(i, 2, QtGui.QTableWidgetItem(str(al[q]['name'])))
                if  (str(0) in al[q]) and (int(al[q][str(0)]) > 0):
                    ma = str(al[q][str(0)])
                else:
                    ma = str(0)
                    
                if(str(1) in al[q]) and (int(al[q][str(1)]) > 0):
                    fe = str(al[q][str(1)])
                else:
                    fe = str(0)
                    
                self.table.setItem(i, 3, QtGui.QTableWidgetItem(str(ma)))
                self.table.setItem(i, 4, QtGui.QTableWidgetItem(str(fe)))
                total = int(ma) + int(fe)
                amt = total * int(al[q]['amount'])
                self.table.setItem(i, 5, QtGui.QTableWidgetItem(str(total)))
                
                self.table.setItem(i, 6, QtGui.QTableWidgetItem(str(al[q]['fee'])))
                self.table.setItem(i, 7, QtGui.QTableWidgetItem(str(al[q]['amount'])))
                self.table.setItem(i, 8, QtGui.QTableWidgetItem(str(amt)))
                i += 1
            # set data
    
            #self.table.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
            
            
            self.tabl.close()
            self.tabl = self.table
            self.stackRightBar.setCurrentIndex(6)
            self.stackLeftBar.setCurrentIndex(0)
            self.checkBoxStack.setCurrentIndex(0)
            self.hbox2.addWidget(self.tabl)
            self.tabl.show()
        #report view
        elif state == 1:
            pass
    
    def myTableClassUnitFee(self, state, session, clasz = None, claszunit = None):       
        #get list of students
        #state = 0 CLASS UNIT FEE
        #state = 1
        #state = 2
        #state = 3
        #state = 4
        #state = 5 
        
        cn = Dat()
            # initiate table if not exist
        if hasattr(Window, 'table'):
            pass
        else:
            self.table = QtGui.QTableWidget()
            
        #header
        header = self.table.horizontalHeader()
        header.setResizeMode(QtGui.QHeaderView.ResizeToContents)
        header.setStretchLastSection(True)
        header.setStyleSheet(self.tableHeaderStyle)
        vheader = self.table.verticalHeader()
        vheader.setStyleSheet(self.tableHeaderStyle)
            # Body
        self.table.setWindowTitle("Class Units")
        self.table.resize(900, 750)
        self.table.setFont(self.tableFont)
        self.table.setSortingEnabled(2)
        self.table.resizeColumnsToContents()
        self.table.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self.handleHeaderMenu)
        self.table.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        self.table.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
            
        if state == 0:
            tableTitle = 'CLASS FEES REPORT'
            self.tabletitle.setText(tableTitle)
            data = cn.studentClassUnitFee(session)
            if len(data) > 0:
                data = data
            else:
                data = {}
            
            al = {}
            for p in data:
                al[p['cid']] = {}
                al[p['cid']]['cname'] = p['clasz']
                al[p['cid']]['name'] = p['classname']
                al[p['cid']]['fee'] = p['fee']
                al[p['cid']]['amount'] = p['amount']
                al[p['cid']]['pay'] = p['pay']
                
            for k in data:
                if k['sex'] == 0:
                    al[k['cid']]['0'] = k['id']
                elif k['sex'] == 1:
                    al[k['cid']]['1'] = k['id']
            
            
            cols = self.classUnitFeeTable
            self.tableHeadersSelector(cols)
            print_header = {}
            kk = 1
            for a in self.classUnitFeeTable:
                print_header[kk] = a
                kk += 1
                
            self.table.setRowCount(len(al) + 1)
            self.table.setColumnCount(len(cols))
            self.table.setHorizontalHeaderLabels(cols)
            
            i = 0
            tot_male = []
            tot_female = []
            tot_all = []
            tot_amount = []
            pay_amount = []
            fin_amount = []
            print_body = {}
            
            num = 1
            for q in al:
                print_body1 = {}
                #row id
                self.table.setItem(i, 0, QtGui.QTableWidgetItem(str(q)))
                self.table.setItem(i, 1, QtGui.QTableWidgetItem(str(al[q]['cname']).title()))
                self.table.setItem(i, 2, QtGui.QTableWidgetItem(str(al[q]['name']).title()))
                if  (str(0) in al[q]) and (int(al[q][str(0)]) > 0):
                    ma = str(al[q][str(0)])
                    tot_male.append(int(al[q][str(0)]))
                else:
                    ma = str(0)
                    
                if(str(1) in al[q]) and (int(al[q][str(1)]) > 0):
                    fe = str(al[q][str(1)])
                    tot_female.append(int(al[q][str(1)]))
                else:
                    fe = str(0)
                
                total = int(ma) + int(fe)
                tot_all.append(int(total))
                
                item_male = QtGui.QTableWidgetItem(str(ma))
                item_male.setTextAlignment(QtCore.Qt.AlignCenter)
                
                item_female = QtGui.QTableWidgetItem(str(fe))
                item_female.setTextAlignment(QtCore.Qt.AlignCenter)
                
                item_tot = QtGui.QTableWidgetItem(str(total))
                item_tot.setTextAlignment(QtCore.Qt.AlignCenter)
                
                self.table.setItem(i, 3, item_male)
                self.table.setItem(i, 4, item_female)
                self.table.setItem(i, 5, item_tot)
                
                namt = al[q]['amount']
                namts = "{:,}".format(namt)
                item_namt = QtGui.QTableWidgetItem(str(namts))
                item_namt.setTextAlignment(QtCore.Qt.AlignRight)
                
                amt = total * float(al[q]['amount'])
                tot_amount.append(float(amt))
                amts = "{:,}".format(amt)
                item_amt = QtGui.QTableWidgetItem(str(amts))
                item_amt.setTextAlignment(QtCore.Qt.AlignRight)
                
                if 'pay' in al[q] and al[q]['pay'] > 0 :
                    payz = float(al[q]['pay'])
                else:
                    payz = 0
                pay_amount.append(float(payz))
                pamts = "{:,}".format(payz)
                item_pamt = QtGui.QTableWidgetItem(str(pamts))
                item_pamt.setTextAlignment(QtCore.Qt.AlignRight)
                
                famt = amt - payz
                fin_amount.append(float(famt))
                famts = "{:,}".format(famt)
                item_famt = QtGui.QTableWidgetItem(str(famts))
                item_famt.setTextAlignment(QtCore.Qt.AlignRight)
                
                self.table.setItem(i, 6, QtGui.QTableWidgetItem(str(al[q]['fee'])))
                self.table.setItem(i, 7, item_namt)
                self.table.setItem(i, 8, item_amt)
                self.table.setItem(i, 9, item_pamt)
                self.table.setItem(i, 10,item_famt)
                
                print_body1[1] = str(num)
                print_body1[2] = str(al[q]['cname']).title()
                print_body1[3] = str(al[q]['name']).title()
                print_body1[4] = str(ma)
                print_body1[5] = str(fe)
                print_body1[6] = str(str(total))
                print_body1[7] = str(al[q]['fee'])
                print_body1[8] = str(namts)
                print_body1[9] = str(amts)
                print_body1[10] = str(pamts)
                print_body1[11] = str(amts)
                print_body[q] = print_body1
                i += 1
                num += 1
            # set data
            
            tot_m = sum(tot_male)
            tot_f = sum(tot_female)
            tot_t = sum(tot_all)
            tot_a = sum(tot_amount)
            tot_p = sum(pay_amount)
            tot_fi = sum(fin_amount)
            
            item_malex = QtGui.QTableWidgetItem(str("{:,}".format(tot_m)))
            item_malex.setTextAlignment(QtCore.Qt.AlignCenter)
                
            item_femalex = QtGui.QTableWidgetItem(str("{:,}".format(tot_f)))
            item_femalex.setTextAlignment(QtCore.Qt.AlignCenter)
                
            item_totx = QtGui.QTableWidgetItem(str("{:,}".format(tot_t)))
            item_totx.setTextAlignment(QtCore.Qt.AlignCenter)
            
            item_amtx = QtGui.QTableWidgetItem(str("{:,}".format(tot_a)))
            item_amtx.setTextAlignment(QtCore.Qt.AlignRight)
            
            item_pamtx = QtGui.QTableWidgetItem(str("{:,}".format(tot_p)))
            item_pamtx.setTextAlignment(QtCore.Qt.AlignRight)
            
            item_famtx = QtGui.QTableWidgetItem(str("{:,}".format(tot_fi)))
            item_famtx.setTextAlignment(QtCore.Qt.AlignRight)
            
            self.table.setItem(i, 0, QtGui.QTableWidgetItem(str(q)))
            self.table.setItem(i, 1, QtGui.QTableWidgetItem(str('')))
            self.table.setItem(i, 2, QtGui.QTableWidgetItem(str('TOTAL')))
            self.table.setItem(i, 3, item_malex)
            self.table.setItem(i, 4, item_femalex)
            self.table.setItem(i, 5, item_totx)
            self.table.setItem(i, 6, QtGui.QTableWidgetItem(str('')))
            self.table.setItem(i, 7, QtGui.QTableWidgetItem(str('')))
            self.table.setItem(i, 8, item_amtx)
            self.table.setItem(i, 9, item_pamtx)
            self.table.setItem(i, 10,item_famtx)
            print_footer = {}
            print_footer[1] = 'SN'
            print_footer[2] = 'FULLNAME'
            print_footer[3] = 'TOTAL'
            print_footer[4] = str("{:,}".format(tot_m))
            print_footer[5] = str("{:,}".format(tot_f))
            print_footer[6] = str("{:,}".format(tot_t))
            print_footer[7] = ''
            print_footer[8] = ''
            print_footer[9] = str("{:,}".format(tot_a))
            print_footer[10] = str("{:,}".format(tot_p))
            print_footer[11] = str("{:,}".format(tot_fi))
            
            print_format = {}
            print_format[1] = ''
            print_format[2] = ''
            print_format[3] = ''
            print_format[4] = 'class="centers" align="center" style="text-align:center;"'
            print_format[5] = 'class="centers" align="center" style="text-align:center;"'
            print_format[6] = 'class="centers" align="center" style="text-align:center;"'
            print_format[7] = ''
            print_format[8] = ''
            print_format[9] = 'class="centers" align="right" style="text-align:center;"'
            print_format[10] = 'class="centers" align="right" style="text-align:center;"'
            print_format[11] = 'class="centers" align="right" style="text-align:center;"'
            
            self.report_table_holder = [session, print_header, print_body, print_footer, print_format]

        #report view
        elif state == 1:
            class_title = self.getDataById(clasz)
            class_title_name = class_title['abbrv']
            tableTitle = str(class_title_name)+' FEES'
            self.tabletitle.setText(tableTitle)
            cn = StudentTable(session, [None], [clasz], [None])
            raw_students = cn.classStudent()
            data = cn.classUnitStudentFee(raw_students)
            
            da = data[0]
            da1 = data[1]
            da2 = data[2]
            al = {}
            for r in da:
                al[r[0]] = {}
                al[r[0]]['schno'] = r[1]
                al[r[0]]['name'] = str(r[2]+' '+r[3]+' '+r[4]).title()    
                al[r[0]]['cla'] = str(r[32]+r[31]).upper() 
                
            for r in da1:
                al[r['studentID']]['pay'] = r['amount']
        
            for r in da2:
                al[r['studentID']]['fee'] = r['amount']
                
            #all table headers titles
            cols = ['id', 'SCH. NO.', 'FULLNAME','CLASS', ' FEE', ' PAYMENTS', ' BALANCE']
            print_header = {1:'SN', 2:'SCH. NO.', 3:'FULLNAME', 4:'CLASS', 5:' FEE', 6:' PAYMENTS', 7:' BALANCE'}
            self.tableHeadersSelector(cols)
            self.table.setRowCount(len(al) + 1)
            self.table.setColumnCount(len(cols))
            self.table.setHorizontalHeaderLabels(cols)
            
            i = 0
            k1 = 0
            tot_fee = []
            tot_pay = []
            tot_bal = []
            print_body = {}
            for q in al:
                #row id
                self.table.setItem(i, 0, QtGui.QTableWidgetItem(str(q)))
                self.table.setItem(i, 1, QtGui.QTableWidgetItem(str(al[q]['schno'])))
                self.table.setItem(i, 2, QtGui.QTableWidgetItem(str(al[q]['name'])))
                self.table.setItem(i, 3, QtGui.QTableWidgetItem(str(al[q]['cla'])))
                
                if 'fee' in al[q] and float(al[q]['fee']) > 0:
                    famt = float(al[q]['fee'])
                else:
                    famt = 0
                tot_fee.append(float(famt))
                famts = "{:,}".format(famt)
                
                if 'pay' in al[q] and float(al[q]['pay']) > 0:
                    pamt = float(al[q]['pay'])
                else:
                    pamt = 0
                tot_pay.append(float(pamt))
                pamts = "{:,}".format(pamt)
                
                bamt = famt - pamt
                tot_bal.append(float(bamt))
                bamts = "{:,}".format(bamt)
                
                self.table.setItem(i, 4, QtGui.QTableWidgetItem(str(famts)))
                self.table.setItem(i, 5, QtGui.QTableWidgetItem(str(pamts)))
                self.table.setItem(i, 6, QtGui.QTableWidgetItem(str(bamts)))
                
                print_body1 = {}
                print_body1[1] = k1
                print_body1[2] = str(al[q]['schno'])
                print_body1[3] = str(al[q]['name'])
                print_body1[4] = str(al[q]['cla'])
                print_body1[5] = str(famts)
                print_body1[6] = str(pamts)
                print_body1[7] = str(bamts)
                print_body[q] = print_body1
                i += 1
                k1 += 1
            # set data
            
            tot_f = sum(tot_fee)
            tot_p = sum(tot_pay)
            tot_b = sum(tot_bal)
            
            self.table.setItem(i, 0, QtGui.QTableWidgetItem(str(q)))
            self.table.setItem(i, 1, QtGui.QTableWidgetItem(str('SCH. NO.')))
            self.table.setItem(i, 2, QtGui.QTableWidgetItem(str('FULLNAME')))
            self.table.setItem(i, 3, QtGui.QTableWidgetItem(str('TOTAL')))
            self.table.setItem(i, 4, QtGui.QTableWidgetItem(str("{:,}".format(tot_f))))
            self.table.setItem(i, 5, QtGui.QTableWidgetItem(str("{:,}".format(tot_p))))
            self.table.setItem(i, 6, QtGui.QTableWidgetItem(str("{:,}".format(tot_b))))
            
            print_footer = {}
            print_footer[1] = 'S/N' 
            print_footer[2] = str('SCH. NO.')
            print_footer[3] = str('FULLNAME')
            print_footer[4] = str('TOTAL')
            print_footer[5] = str("{:,}".format(tot_f))
            print_footer[6] = str("{:,}".format(tot_p))
            print_footer[7] = str("{:,}".format(tot_b))
            
            print_format = {}
            print_format[1] = ''
            print_format[2] = ''
            print_format[3] = ''
            print_format[4] = 'text-align:center;'
            print_format[5] = 'text-align:right;'
            print_format[6] = 'text-align:right;'
            print_format[7] = 'text-align:right;'
            
            self.report_table_holder = [session, print_header, print_body, print_footer, print_format]
            
        elif state == 2:
            class_title = self.getDataById(clasz)
            class_title_name = class_title['abbrv']
            tableTitle = str(class_title_name)+' STUDENTS FEES DETAILS'
            self.tabletitle.setText(tableTitle)
            cn = StudentTable(session, [None] , [clasz],  [None])
            raw_students = cn.classStudent()
            data = cn.classUnitStudentFeeDetails(raw_students)
            
            da = data[0]
            da1 = data[1]
            
            al = {}
            fees_al = []
            for r in da:
                al[r[0]] = {}
                al[r[0]]['schno'] = r[1]
                al[r[0]]['name'] = str(r[2]+' '+r[3]+' '+r[3]).title() 
                al[r[0]]['cla'] = str(r[32]+r[31]).upper()
           
            for r in da1:
                al[r['studentID']][r['feeID']] = r['amount']
                fees_al.append(r['feeID'])
        
            fees_unique = list(set(fees_al)) 
            fees_arr = cn.getData(fees_unique)
            #all table headers titles
            cols = ['id', 'SCH. NO.', 'FULLNAME', 'CLASS']
            local_arr = {}
            for a in fees_arr:
                cols.append(str(fees_arr[a]).upper())
                local_arr[a] = [] 
            cols.append('TOTAL')
            
            print_header = {}
            a0 = 1
            for a in cols:
                print_header[a0] = a
                a0 += 1

            self.tableHeadersSelector(cols)
            self.table.setRowCount(len(al) + 1)
            self.table.setColumnCount(len(cols))
            self.table.setHorizontalHeaderLabels(cols)
            
            i = 0
            a0 = 1
            final_amt = []
            print_body = {}
            for q in al:
                print_body1 = {}
                #row id
                self.table.setItem(i, 0, QtGui.QTableWidgetItem(str(q)))
                self.table.setItem(i, 1, QtGui.QTableWidgetItem(str(al[q]['schno'])))
                self.table.setItem(i, 2, QtGui.QTableWidgetItem(str(al[q]['name'])))
                self.table.setItem(i, 3, QtGui.QTableWidgetItem(str(al[q]['cla'])))
                print_body1[1] = str(a0)
                print_body1[2] = str(al[q]['schno'])
                print_body1[3] = str(al[q]['name'])
                print_body1[4] = str(al[q]['cla'])
                
                k = 4
                rowxxx = []
                for a in fees_arr:
                    if a in al[q] and float(al[q][a]) > 0:
                        famt = float(al[q][a])
                    else:
                        famt = 0
                    
                    local_arr[a].append(float(famt))
                    rowxxx.append(float(famt))
                    famts = "{:,}".format(famt)
                    self.table.setItem(i, k, QtGui.QTableWidgetItem(str(famts)))
                    print_body1[k + 1] = str(famts)
                    k += 1
                ramt = sum(rowxxx)
                final_amt.append(float(ramt))
                ramts = "{:,}".format(ramt)
                self.table.setItem(i, k, QtGui.QTableWidgetItem(str(ramts)))
                print_body1[k + 1] = str(ramts)
                i += 1
                
            # set data
            print_footer = {}
            print_formart = {}
            self.table.setItem(i, 0, QtGui.QTableWidgetItem(str(q)))
            self.table.setItem(i, 1, QtGui.QTableWidgetItem(str('')))
            self.table.setItem(i, 2, QtGui.QTableWidgetItem(str('')))
            self.table.setItem(i, 3, QtGui.QTableWidgetItem(str('TOTAL')))
            print_footer[1] = str('S/N')
            print_footer[2] = str('')
            print_footer[3] = str('')
            print_footer[4] = str('TOTAL')
            print_formart[1] = ''
            print_formart[2] = ''
            print_formart[3] = ''
            print_formart[4] = ''
            k1 = 4
            for a in fees_arr:
                tot_f = sum(local_arr[a])
                self.table.setItem(i, k1, QtGui.QTableWidgetItem(str("{:,}".format(tot_f))))
                print_footer[k1 + 1] = str("{:,}".format(tot_f))
                print_formart[k1 + 1] = ''
                k1 += 1
            fin_amt = sum(final_amt)
            fin_amts = "{:,}".format(fin_amt)
            self.table.setItem(i, k1, QtGui.QTableWidgetItem(str(fin_amts)))
            print_footer[k1 + 1] = str(fin_amts)
            print_formart[k1 + 1] = ''
        
            self.report_table_holder = [session, print_header, print_body, print_footer, print_formart]
            
        elif state == 3:
            class_title = self.getDataById(clasz)
            class_title_name = class_title['abbrv']
            tableTitle = str(class_title_name)+' STUDENTS PAYMENT DETAILS'
            self.tabletitle.setText(tableTitle)
            cn = StudentTable(session, [None], [clasz], [None])
            raw_students = cn.classStudent()
            data = cn.classUnitStudentPayDetails(raw_students)
            
            da = data[0]
            da1 = data[1]
            
            al = {}
            fees_al = []
            for r in da:
                al[r[0]] = {}
                al[r[0]]['schno'] = r[1]
                al[r[0]]['name'] = str(r[2]+' '+r[3]+' '+r[4]).title() 
                al[r[0]]['cla'] = str(r[32]+r[31]).upper()
           
            for r in da1:
                al[r['studentID']][r['feeID']] = r['amount']
                fees_al.append(r['feeID'])
        
            fees_unique = list(set(fees_al)) 
            fees_arr = cn.getData(fees_unique)
            #all table headers titles
            cols = ['S/N', 'SCH. NO.', 'FULLNAME', 'CLASS']
            local_arr = {}
            for a in fees_arr:
                cols.append(str(fees_arr[a]).upper())
                local_arr[a] = [] 
            cols.append('TOTAL')
            
            print_header = {}
            a0 = 1
            for a in cols:
                print_header[a0] = a
                a0 += 1
                
            self.tableHeadersSelector(cols)
            self.table.setRowCount(len(al) + 1)
            self.table.setColumnCount(len(cols))
            self.table.setHorizontalHeaderLabels(cols)
            
            i = 0
            final_amt = []
            
            print_body = {}
            for q in al:
                print_body1 = {}
                #row id
                self.table.setItem(i, 0, QtGui.QTableWidgetItem(str(q)))
                self.table.setItem(i, 1, QtGui.QTableWidgetItem(str(al[q]['schno'])))
                self.table.setItem(i, 2, QtGui.QTableWidgetItem(str(al[q]['name'])))
                self.table.setItem(i, 3, QtGui.QTableWidgetItem(str(al[q]['cla'])))
                print_body1[1] = str(a0)
                print_body1[2] = str(al[q]['schno'])
                print_body1[3] = str(al[q]['name'])
                print_body1[4] = str(al[q]['cla'])

                k = 4
                rowxxx = []
                for a in fees_arr:
                    if a in al[q] and float(al[q][a]) > 0:
                        famt = float(al[q][a])
                    else:
                        famt = 0
                    
                    local_arr[a].append(float(famt))
                    rowxxx.append(float(famt))
                    famts = "{:,}".format(famt)
                    self.table.setItem(i, k, QtGui.QTableWidgetItem(str(famts)))
                    print_body[k + 1] = str(famts)
                    k += 1
                ramt = sum(rowxxx)
                final_amt.append(float(ramt))
                ramts = "{:,}".format(ramt)
                self.table.setItem(i, k, QtGui.QTableWidgetItem(str(ramts)))
                print_body1[k + 1] = str(ramts)
                print_body[q] = print_body1
                i += 1
            # set data
            self.table.setItem(i, 0, QtGui.QTableWidgetItem(str('')))
            self.table.setItem(i, 1, QtGui.QTableWidgetItem(str('')))
            self.table.setItem(i, 2, QtGui.QTableWidgetItem(str('TOTAL')))
            self.table.setItem(i, 3, QtGui.QTableWidgetItem(str('TOTAL')))
            print_formart = {}
            print_formart[1] = ''
            print_formart[2] = ''
            print_formart[3] = ''
            print_formart[4] = ''
            k1 = 4
            for a in fees_arr:
                tot_f = sum(local_arr[a])
                self.table.setItem(i, k1, QtGui.QTableWidgetItem(str("{:,}".format(tot_f))))
                print_footer[k1 + 1] = str("{:,}".format(tot_f))
                print_formart[k1 + 1] = 'align ="right"'
                k1 += 1
            fin_amt = sum(final_amt)
            fin_amts = "{:,}".format(fin_amt)
            self.table.setItem(i, k1, QtGui.QTableWidgetItem(str(fin_amts)))
            print_footer[k1 + 1] = str(fin_amts)
            print_formart[k1 + 1] = 'align = "right"'
        
            self.report_table_holder = [session, print_header, print_body, print_footer, print_formart]
            
        elif state == 4:
            '''
            CLASS UNIT, STUDENTS NAMES FEES, PAYMENTS AND BALANCE SUMMARY
            '''
            class_title_unit = self.getDataById(claszunit)
            class_title = self.getDataById(class_title['subID'])
            class_title_name = str(class_title['abbrv']+' '+class_title_unit['abbrv']).upper()
            tableTitle = str(class_title_name)+' FEES  & PAYMENT SUMMARY'
            self.tabletitle.setText(tableTitle)
            
            cn = StudentTable(session, [None], [None], [claszunit])
            raw_students = cn.classUnitStudent()
            data = cn.classUnitStudentFee(raw_students)
            
            da = data[0]
            da1 = data[1]
            da2 = data[2]
            al = {}
            for r in da:
                al[r[0]] = {}
                al[r[0]]['schno'] = r[1]
                al[r[0]]['name'] = str(r[2]+' '+r[3]+' '+r[4]).title()    
           
            for r in da1:
                al[r['studentID']]['pay'] = r['amount']
        
            for r in da2:
                al[r['studentID']]['fee'] = r['amount']
                
            #all table headers titles
            cols = ['id', 'SCH. NO.', 'FULLNAME', ' FEE', ' PAYMENTS', ' BALANCE']
            
            print_header = {}
            a0 = 1
            for a in cols:
                print_header[a0] = a
                a0 += 1
            print_header[1] = 'SN.'
            self.tableHeadersSelector(cols)
            self.table.setRowCount(len(al) + 1)
            self.table.setColumnCount(len(cols))
            self.table.setHorizontalHeaderLabels(cols)
            
            i = 0
            k1 = 0
            tot_fee = []
            tot_pay = []
            tot_bal = []
            print_body = {}
            for q in al:
                #row id
                self.table.setItem(i, 0, QtGui.QTableWidgetItem(str(q)))
                self.table.setItem(i, 1, QtGui.QTableWidgetItem(str(al[q]['schno'])))
                self.table.setItem(i, 2, QtGui.QTableWidgetItem(str(al[q]['name'])))
                
                if 'fee' in al[q] and float(al[q]['fee']) > 0:
                    famt = float(al[q]['fee'])
                else:
                    famt = 0
                tot_fee.append(float(famt))
                famts = "{:,}".format(famt)
                
                if 'pay' in al[q] and float(al[q]['pay']) > 0:
                    pamt = float(al[q]['pay'])
                else:
                    pamt = 0
                tot_pay.append(float(pamt))
                pamts = "{:,}".format(pamt)
                
                bamt = famt - pamt
                tot_bal.append(float(bamt))
                bamts = "{:,}".format(bamt)
                
                self.table.setItem(i, 3, QtGui.QTableWidgetItem(str(famts)))
                self.table.setItem(i, 4, QtGui.QTableWidgetItem(str(pamts)))
                self.table.setItem(i, 5, QtGui.QTableWidgetItem(str(bamts)))
                
                print_body1 = {}
                print_body1[1] = i + 1
                print_body1[2] = str(al[q]['schno'])
                print_body1[3] = str(al[q]['name'])
                print_body1[4] = str(famts)
                print_body1[5] = str(pamts)
                print_body1[6] = str(bamts)
                print_body[q] = print_body1
                
                i += 1
                k1 += 1
            # set data
            
            tot_f = sum(tot_fee)
            tot_p = sum(tot_pay)
            tot_b = sum(tot_bal)
            
            self.table.setItem(i, 0, QtGui.QTableWidgetItem(str('SN.')))
            self.table.setItem(i, 1, QtGui.QTableWidgetItem(str('')))
            self.table.setItem(i, 2, QtGui.QTableWidgetItem(str('Total')))
            self.table.setItem(i, 3, QtGui.QTableWidgetItem(str("{:,}".format(tot_f))))
            self.table.setItem(i, 4, QtGui.QTableWidgetItem(str("{:,}".format(tot_p))))
            self.table.setItem(i, 5, QtGui.QTableWidgetItem(str("{:,}".format(tot_b))))
            
            print_footer = {}
            print_footer[1] = 'SN.' 
            print_footer[2] = str('')
            print_footer[3] = str('TOTAL')
            print_footer[4] = str("{:,}".format(tot_f))
            print_footer[5] = str("{:,}".format(tot_p))
            print_footer[6] = str("{:,}".format(tot_b))
            
            print_format = {}
            print_format[1] = 'style="width:10px;"'
            print_format[2] = 'align="center"'
            print_format[3] = ''
            print_format[4] = 'align="right"'
            print_format[5] = 'align="right"'
            print_format[6] = 'align="right"'
           
            self.report_table_holder = [session, print_header, print_body, print_footer, print_format]
        
        elif state == 5:
            class_title_unit = self.getDataById(claszunit)
            class_title = self.getDataById(class_title_unit['subID'])
            class_title_name = str(class_title['abbrv']+' '+class_title_unit['abbrv']).upper()
            tableTitle = str(class_title_name)+' PAYMENTS SUMMARY'
            self.tabletitle.setText(tableTitle)
            cn = StudentTable(session, [None], [None], [claszunit])
            raw_students = cn.classUnitStudent()
            data = cn.classUnitStudentFeeDetails(raw_students)
            
            da = data[0]
            da1 = data[1]
            
            al = {}
            fees_al = []
            for r in da:
                al[r[0]] = {}
                al[r[0]]['schno'] = r[1]
                al[r[0]]['name'] = str(r[2]+' '+r[3]+' '+r[4]).title()    
           
            for r in da1:
                al[r['studentID']][r['feeID']] = r['amount']
                fees_al.append(r['feeID'])
        
            fees_unique = list(set(fees_al)) 
            fees_arr = cn.getData(fees_unique)
            #all table headers titles
            cols = ['id', 'SCH. NO.', 'FULLNAME']
            local_arr = {}
            for a in fees_arr:
                cols.append(str(fees_arr[a]).upper())
                local_arr[a] = [] 
            cols.append('TOTAL')
            
            print_header = {}
            a0 = 1
            for a in cols:
                print_header[a0] = a
                a0 += 1
            self.tableHeadersSelector(cols)
            self.table.setRowCount(len(al) + 1)
            self.table.setColumnCount(len(cols))
            self.table.setHorizontalHeaderLabels(cols)
            
            i = 0
            final_amt = []
            print_body = {}
            for q in al:
                #row id
                print_body1 = {}
                self.table.setItem(i, 0, QtGui.QTableWidgetItem(str(q)))
                self.table.setItem(i, 1, QtGui.QTableWidgetItem(str(al[q]['schno'])))
                self.table.setItem(i, 2, QtGui.QTableWidgetItem(str(al[q]['name'])))
                print_body1[1] = str(a0)
                print_body1[2] = str(al[q]['schno'])
                print_body1[3] = str(al[q]['name'])
                k = 3
                rowxxx = []
                for a in fees_arr:
                    if a in al[q] and float(al[q][a]) > 0:
                        famt = float(al[q][a])
                    else:
                        famt = 0
                    
                    local_arr[a].append(float(famt))
                    rowxxx.append(float(famt))
                    famts = "{:,}".format(famt)
                    self.table.setItem(i, k, QtGui.QTableWidgetItem(str(famts)))
                    print_body1[k] = str(famts)
                    k += 1
                ramt = sum(rowxxx)
                final_amt.append(float(ramt))
                ramts = "{:,}".format(ramt)
                self.table.setItem(i, k, QtGui.QTableWidgetItem(str(ramts)))
                print_body1[k] = str(ramts)
                print_body[q] = print_body1
                i += 1
            # set data
            self.table.setItem(i, 0, QtGui.QTableWidgetItem(str(q)))
            self.table.setItem(i, 1, QtGui.QTableWidgetItem(str('')))
            self.table.setItem(i, 2, QtGui.QTableWidgetItem(str('TOTAL')))
            print_footer = {}
            print_formart = {}
            print_footer[1] = 'S/N'
            print_footer[2] = ''
            print_footer[3] = 'TOTAL'
            print_formart[1] = ''
            print_formart[2] = ''
            print_formart[3] = ''
            k1 = 3
            for a in fees_arr:
                tot_f = sum(local_arr[a])
                self.table.setItem(i, k1, QtGui.QTableWidgetItem(str("{:,}".format(tot_f))))
                print_footer[k1 + 1] = str("{:,}".format(tot_f))
                print_formart[k1 + 1] = ''
                k1 += 1
            fin_amt = sum(final_amt)
            fin_amts = "{:,}".format(fin_amt)
            self.table.setItem(i, k1, QtGui.QTableWidgetItem(str(fin_amts)))
            print_footer[k1 + 1] = str(fin_amts)
            print_formart[k1 + 1] = ''
        
            self.report_table_holder = [session, print_header, print_body, print_footer, print_formart]
        
        elif state == 6:
            class_title_unit = self.getDataById(claszunit)
            class_title = self.getDataById(class_title_unit['subID'])
            class_title_name = str(class_title['abbrv']+' '+class_title_unit['abbrv']).upper()
            tableTitle = str(class_title_name)+' FEES SUMMARY'
            self.tabletitle.setText(tableTitle)
            cn = StudentTable(session, [None], [None], [claszunit])
            raw_students = cn.classUnitStudent()
            data = cn.classUnitStudentPayDetails(raw_students)
            
            da = data[0]
            da1 = data[1]
            
            al = {}
            fees_al = []
            for r in da:
                al[r[0]] = {}
                al[r[0]]['schno'] = r[1]
                al[r[0]]['name'] = str(r[2]+' '+r[3]+' '+r[4]).title()    
           
            for r in da1:
                al[r['studentID']][r['feeID']] = r['amount']
                fees_al.append(r['feeID'])
        
            fees_unique = list(set(fees_al)) 
            fees_arr = cn.getData(fees_unique)
            #all table headers titles
            cols = ['id', 'SCH. NO.', 'FULLNAME']
            local_arr = {}
            for a in fees_arr:
                cols.append(str(fees_arr[a]).upper())
                local_arr[a] = [] 
            cols.append('TOTAL')
            
            print_header = {}
            a0 = 1
            for a in cols:
                print_header[a0] = a
                a0 += 1
            self.tableHeadersSelector(cols)
            self.table.setRowCount(len(al) + 1)
            self.table.setColumnCount(len(cols))
            self.table.setHorizontalHeaderLabels(cols)
            
            i = 0
            final_amt = []
            print_body = {}
            for q in al:
                #row id
                print_body1 = {}
                self.table.setItem(i, 0, QtGui.QTableWidgetItem(str(q)))
                self.table.setItem(i, 1, QtGui.QTableWidgetItem(str(al[q]['schno'])))
                self.table.setItem(i, 2, QtGui.QTableWidgetItem(str(al[q]['name'])))
                print_body1[1] = i + 1
                print_body1[2] = str(al[q]['schno'])
                print_body1[3] = str(al[q]['name'])
                k = 3
                rowxxx = []
                for a in fees_arr:
                    if a in al[q] and float(al[q][a]) > 0:
                        famt = float(al[q][a])
                    else:
                        famt = 0
                    
                    local_arr[a].append(float(famt))
                    rowxxx.append(float(famt))
                    famts = "{:,}".format(famt)
                    self.table.setItem(i, k, QtGui.QTableWidgetItem(str(famts)))
                    print_body1[k + 1] = str(famts)
                    k += 1
                ramt = sum(rowxxx)
                final_amt.append(float(ramt))
                ramts = "{:,}".format(ramt)
                self.table.setItem(i, k, QtGui.QTableWidgetItem(str(ramts)))
                print_body1[k + 1] = str(ramts)
                print_body[q] = print_body1
                i += 1
            # set data
            self.table.setItem(i, 0, QtGui.QTableWidgetItem(str(q)))
            self.table.setItem(i, 1, QtGui.QTableWidgetItem(str('')))
            self.table.setItem(i, 2, QtGui.QTableWidgetItem(str('TOTAL')))
            print_footer = {}
            print_formart = {}
            print_footer[1] = 'S/N'
            print_footer[2] = ''
            print_footer[3] = 'TOTAL'
            print_formart[1] = ''
            print_formart[2] = ''
            print_formart[3] = ''
            k1 = 3
            for a in fees_arr:
                tot_f = sum(local_arr[a])
                self.table.setItem(i, k1, QtGui.QTableWidgetItem(str("{:,}".format(tot_f))))
                print_footer[k1 + 1] = str("{:,}".format(tot_f))
                print_formart[k1 + 1] = 'align:right'
                k1 += 1
            fin_amt = sum(final_amt)
            fin_amts = "{:,}".format(fin_amt)
            self.table.setItem(i, k1, QtGui.QTableWidgetItem(str(fin_amts)))
            print_footer[k1 + 1] = str("{:,}".format(tot_f))
            print_formart[k1 + 1] = 'align:right'
            self.report_table_holder = [session, print_header, print_body, print_footer, print_formart]
        
        self.table.hideColumn(0)
        self.tabl.close()
        self.tabl = self.table
        self.stackRightBar.setCurrentIndex(5)
        self.stackLeftBar.setCurrentIndex(0)
        self.checkBoxStack.setCurrentIndex(0)
        self.hbox2.addWidget(self.tabl)
        self.tabl.show()
    
    def myTableSearch(self, students):       
        #get list of students
        
        self.students = students
        
        #all table headers titles
        cols = ['id', 'SCH. NO.', 'FULLNAME', 'SEX','CLASS' ]
        self.tableHeadersSelector(cols)
        print_header = {}
        a0 = 1
        for a in cols:
           print_header[a0] = a
           a0 += 1
        state = 0    
        if state == 0:
                
            # initiate table if not exist
            if hasattr(Window, 'table'):
                pass
            else:
                self.table = QtGui.QTableWidget()
            
            
            #header
            header = self.table.horizontalHeader()
            header.setResizeMode(QtGui.QHeaderView.ResizeToContents)
            header.setStretchLastSection(True)
            header.setStyleSheet(self.tableHeaderStyle)
            vheader = self.table.verticalHeader()
            vheader.setStyleSheet(self.tableHeaderStyle)
            # Body
            self.table.setWindowTitle("Student Bio-Data")
            self.table.resize(900, 750)
            self.table.setFont(self.tableFont)
            self.table.setSortingEnabled(2)
            self.table.resizeColumnsToContents()
            self.table.setRowCount(len(students))
            self.table.setColumnCount(len(cols))
            self.table.setHorizontalHeaderLabels(cols)
            self.table.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
            self.table.customContextMenuRequested.connect(self.handleHeaderMenu)
            self.table.hideColumn(0)
            self.table.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
            self.table.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
            self.table.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
            
            i = 0
            print_body = {}
            for j in self.students:
                print_body1 = {}
                q = j
                #row id
                self.table.setItem(i, 0, QtGui.QTableWidgetItem(str(q['id'])))
                #school id
                self.table.setItem(i, 1, QtGui.QTableWidgetItem(str(q['schno'])))
                #fullname
                fullname= str(q['surname'])+' '+str(q['firstname'])+' '+str(q['othername'])
                self.table.setItem(i, 2, QtGui.QTableWidgetItem(str(fullname.title())))
                #gender
                if(q['gender'] == 0):
                    sex = 'Male';
                else:
                    sex = 'Female';
                self.table.setItem(i, 3, QtGui.QTableWidgetItem(str(sex)))
                #classname
                classname= str(q['classname'])+' '+str(q['classunit'])
                self.table.setItem(i, 4, QtGui.QTableWidgetItem(str(classname.title())))
                
                print_body1[1] = i + 1
                print_body1[2] = str(q['schno'])
                print_body1[3] = str(fullname.title())
                print_body1[4] = str(classname.title())
               
                print_body[q['id']] = print_body1
                i += 1
            # set data
                print_footer = {}
                
                print_formart = {}
                print_formart[1] = ''
                print_formart[2] = ''
                print_formart[3] = ''
                
    
                self.report_table_holder = [self.mainTerm, print_header, print_body, print_footer, print_formart]
            #self.table.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
            return self.table
        #report view
        elif state == 1:
            pass 
        
    def myTableOthers(self, data, title, state):       
        #get list of students
        #all table headers titles
        if state == 1:
            cols = ['id', 'ITEM', 'TRANSACTIONS' ,'AMOUNT' ]
        elif state == 2:
            cols = ['id', 'ITEM', 'TRANSACTIONS' ,'AMOUNT' ]
        elif state == 3:
            cols = ['id', 'Name', 'No. of ' ]
        elif state == 4:
            cols = ['id', 'Name', 'No. of ' ]
        elif state == 5:
            cols = ['id', 'Name', 'No. of ' ]
        elif state == 6:
            cols = ['id', 'Item', 'Instock', 'Outstock', 'Borrowed', 'Damaged', 'Stock', 'Unit Price', 'Total Price' ]
            new_data = {}
            for i in data:
                new_data[i['itemID']] = {}
                new_data[i['itemID']]['name'] = i['itemname']
                new_data[i['itemID']]['amount'] = i['datesamount']
                new_data[i['itemID']]['state'] = {}
            for i in data:
                new_data[i['itemID']]['state'][i['state']] = [ float(i['quantity']), i['num']]
       
            data = new_data
        self.tabletitle.setText(title)
        self.tableHeadersSelector(cols)
        print_header = {}
        a0 = 1
        for a in cols:
           print_header[a0] = a
           a0 += 1

        # initiate table if not exist
        if hasattr(Window, 'table'):
            pass
        else:
            self.table = QtGui.QTableWidget()
        
        #header
        header = self.table.horizontalHeader()
        header.setResizeMode(QtGui.QHeaderView.ResizeToContents)
        header.setStretchLastSection(True)
        header.setStyleSheet(self.tableHeaderStyle)
        vheader = self.table.verticalHeader()
        vheader.setStyleSheet(self.tableHeaderStyle)
        # Body
        self.table.setWindowTitle("Expenses Table")
        self.table.resize(900, 750)
        self.table.setFont(self.tableFont)
        self.table.setSortingEnabled(2)
        self.table.resizeColumnsToContents()
        self.table.setRowCount(len(data) + 1 )
        self.table.setColumnCount(len(cols))
        self.table.setHorizontalHeaderLabels(cols)
        self.table.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self.handleHeaderMenu)
        self.table.hideColumn(0)
        self.table.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        self.table.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        
        i = 0
        l = 0 
        print_body = {}
        tot_amount = []
        tot_trans = []
        total_price = []
        if state == 6:
                for j in data:
                    print_body1 = {}
                    q = j
                    #row id
                    try:
                        ins = data[j]['state'][1][0]
                    except:
                        ins = 0
                    try:
                        out = data[j]['state'][2][0]
                    except:
                        out = 0
                    try:
                        bor = data[j]['state'][3][0]
                    except:
                        bor = 0
                    try:
                        ret = data[j]['state'][4][0]
                    except:
                        ret = 0
                    try:
                        dam = data[j]['state'][5][0]
                    except:
                        dam = 0
                   
                    bal = ins - out - dam
                    bor = bor - ret
                    
                    
                    item_ins = QtGui.QTableWidgetItem(str(ins))
                    item_ins.setTextAlignment(QtCore.Qt.AlignCenter)
                    
                    item_out = QtGui.QTableWidgetItem(str(out))
                    item_out.setTextAlignment(QtCore.Qt.AlignCenter)
                    
                    item_dam = QtGui.QTableWidgetItem(str(dam))
                    item_dam.setTextAlignment(QtCore.Qt.AlignCenter)
                    
                    item_bal = QtGui.QTableWidgetItem(str(bal))
                    item_bal.setTextAlignment(QtCore.Qt.AlignCenter)
                    
                    item_bor = QtGui.QTableWidgetItem(str(bor))
                    item_bor.setTextAlignment(QtCore.Qt.AlignCenter)
                    
                    price = data[j]['amount']
                    prices = "{:,}".format(price)
                    item_price = QtGui.QTableWidgetItem(str(prices))
                    item_price.setTextAlignment(QtCore.Qt.AlignRight)
                    
                    tot_price = bal *  price
                    tot_prices = "{:,}".format(tot_price)
                    total_price.append(tot_price)
                    item_prices = QtGui.QTableWidgetItem(str(tot_prices))
                    item_prices.setTextAlignment(QtCore.Qt.AlignRight)
                    
                    self.table.setItem(i, 0, QtGui.QTableWidgetItem(j))
                    self.table.setItem(i, 1, QtGui.QTableWidgetItem(str(data[j]['name']).title()))
                    self.table.setItem(i, 2, item_ins)
                    self.table.setItem(i, 3, item_out)
                    self.table.setItem(i, 4, item_bor)
                    self.table.setItem(i, 5, item_dam)
                    self.table.setItem(i, 6, item_bal)
                    self.table.setItem(i, 7, item_price)
                    self.table.setItem(i, 8, item_prices)
                   
                    print_body1[1] = l + 1
                    print_body1[2] = str(data[j]['name']).title()
                    print_body1[3] = ins
                    print_body1[4] = out
                    print_body1[5] = bor
                    print_body1[6] = dam
                    print_body1[7] = bal
                    print_body1[8] = prices
                    print_body1[9] = tot_prices
                    print_body[j] = print_body1
                    i += 1
                    l += 1
                    
                fin_price = sum(total_price)
                fin_prices = "{:,}".format(fin_price)
                item_fin = QtGui.QTableWidgetItem(str(fin_prices))
                item_fin.setTextAlignment(QtCore.Qt.AlignRight)
                
                print_formart = {}
                print_formart[1] = 'align="center"'
                print_formart[2] = ''
                print_formart[3] = 'align="center"'
                print_formart[4] = 'align="center"'
                print_formart[5] = 'align="center"'
                print_formart[6] = 'align="center"'
                print_formart[7] = 'align="center"'
                print_formart[8] = 'align="right"'
                print_formart[9] = 'align="right"'
                
                self.table.setItem(i, 0, QtGui.QTableWidgetItem('SN.'))
                self.table.setItem(i, 1, QtGui.QTableWidgetItem(''))
                self.table.setItem(i, 2, QtGui.QTableWidgetItem(''))
                self.table.setItem(i, 3, QtGui.QTableWidgetItem(''))
                self.table.setItem(i, 4, QtGui.QTableWidgetItem(''))
                self.table.setItem(i, 5, QtGui.QTableWidgetItem(''))
                self.table.setItem(i, 6, QtGui.QTableWidgetItem(''))
                self.table.setItem(i, 7, QtGui.QTableWidgetItem(''))
                self.table.setItem(i, 8, QtGui.QTableWidgetItem(item_fin))
                
                print_footer = {}
                print_footer[1] = ''
                print_footer[2] = ''
                print_footer[3] = ''
                print_footer[4] = ''
                print_footer[5] = ''
                print_footer[6] = ''
                print_footer[7] = ''
                print_footer[8] = ''
                print_footer[9] = fin_prices
                    
        else:
            for j in data:
                print_body1 = {}
                q = j
                
                trans = "{:,}".format(q['transactions'])
                tot_trans.append(q['transactions'])
                item_trans = QtGui.QTableWidgetItem(str(trans))
                item_trans.setTextAlignment(QtCore.Qt.AlignCenter)
                
                if state == 1 or state == 2:
                    amts = "{:,}".format(q['amount'])
                    tot_amount.append(q['amount'])
                    item_amt = QtGui.QTableWidgetItem(str(amts))
                    item_amt.setTextAlignment(QtCore.Qt.AlignRight)
                #row id
                self.table.setItem(i, 0, QtGui.QTableWidgetItem(str(q['expenseID'])))
                self.table.setItem(i, 1, QtGui.QTableWidgetItem(str(q['expenseName']).title()))
                self.table.setItem(i, 2, item_trans)
                if state == 1 or state == 2:
                    self.table.setItem(i, 3, item_amt)
               
                print_body1[0] = l + 1
                print_body1[1] = str(q['expenseName']).title()
                print_body1[2] = trans
                if state == 1 or state == 2:
                    print_body1[3] = amts
                print_body[q['expenseID']] = print_body1
                i += 1
                l += 1
            # set data
            item_tr = QtGui.QTableWidgetItem(str( "{:,}".format(sum(tot_trans))))
            item_tr.setTextAlignment(QtCore.Qt.AlignCenter)
            item_tot = QtGui.QTableWidgetItem(str( "{:,}".format(sum(tot_amount))))
            item_tot.setTextAlignment(QtCore.Qt.AlignRight)
            self.table.setItem(i, 0, QtGui.QTableWidgetItem(str('SN')))
            self.table.setItem(i, 1, QtGui.QTableWidgetItem('TOTAL'))
            self.table.setItem(i, 2, item_tr)
            if state == 1 or state == 2:
                self.table.setItem(i, 3, item_tot)
        
        
            print_footer = {}
            print_footer[0] = ''
            print_footer[1] = ''
            print_footer[2] = "{:,}".format(sum(tot_trans))
            if state == 1 or state == 2:
                print_footer[3] = "{:,}".format(sum(tot_amount))
            
            print_formart = {}
            print_formart[0] = 'align="center"'
            print_formart[1] = ''
            print_formart[2] = 'align="center"'
            if state == 1 or state == 2:
                print_formart[3] = 'align="right"'
            

        self.report_table_holder = [self.mainTerm, print_header, print_body, print_footer, print_formart]
        #self.table.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.table.hideColumn(0)
        self.tabl.close()
        self.tabl = self.table
        self.stackRightBar.setCurrentIndex(5)
        self.stackLeftBar.setCurrentIndex(0)
        self.checkBoxStack.setCurrentIndex(0)
        self.hbox2.addWidget(self.tabl)
        self.tabl.show()
           
        
    def myTableSubject(self, state, session, clasz, claszunit):       
        #get list of students
        cn = Dat()
            # initiate table if not exist
        if hasattr(Window, 'table'):
            pass
        else:
            self.table = QtGui.QTableWidget()
            
        if state == 1: 
           class_title = self.getDataById(clasz)
           class_title_name = class_title['abbrv']
           tableTitle = str(class_title_name)+' STUDENTS SUBJECTS'
           self.tabletitle.setText(tableTitle)
           cn = StudentTable(session, [None], [clasz], [None])
           raw_students = cn.classStudent()
           students = cn.classStudentSubject(raw_students)
        elif state == 2:
           class_title_unit = self.getDataById(claszunit)
           class_title = self.getDataById(class_title_unit['subID'])
           class_title_name = str(class_title['abbrv']+' '+class_title_unit['abbrv']).upper()
           tableTitle = str(class_title_name)+' STUDENTS SUBJECTS'
           self.tabletitle.setText(tableTitle)
           cn = StudentTable(session, [None], [None], [claszunit])
           raw_students = cn.classUnitStudent()
           students = cn.classStudentSubject(raw_students)
            
        da = students[0]
        da1 = students[1]
            
        al = {}
        for r in da:
            al[r[0]] = {}
            al[r[0]]['schno'] = r[1]
            al[r[0]]['name'] = str(r[2]+' '+r[3]+' '+r[4]).title()    
           
        for r in da1:
            try:
                al[r['studentID']]['clasz'] = str(r['classname']+" "+r['classunit']).upper()
            except:
                al[r['studentID']]['clasz'] = str("--").upper()
            try:
                al[r['studentID']]['subjects'] = str(r['subjects']).upper()
            except:
                al[r['studentID']]['subjects'] = str("--").upper()
        
            #all table headers titles
        cols = ['id', 'SCH. NO.',  'FULLNAME', 'CLASS', 'SUBJECTS']
        
        print_header = {}
        a0 = 1
        for a in cols:
            print_header[a0] = a
            a0 += 1
        self.tableHeadersSelector(cols)
        self.table.setRowCount(len(al) + 1)
        self.table.setColumnCount(len(cols))
        self.table.setHorizontalHeaderLabels(cols)
            
        i = 0
       
        print_body = {}
        for q in al:
                #row id
            print_body1 = {}
            self.table.setItem(i, 0, QtGui.QTableWidgetItem(str(q)))
            self.table.setItem(i, 1, QtGui.QTableWidgetItem(str(al[q]['schno'])))
            self.table.setItem(i, 2, QtGui.QTableWidgetItem(str(al[q]['name'])))
            if 'clasz' in al[q]:
                self.table.setItem(i, 3, QtGui.QTableWidgetItem(str(al[q]['clasz'])))
            else:
                self.table.setItem(i, 3, QtGui.QTableWidgetItem(str('--')))
                
            if 'subjects' in al[q]:
                self.table.setItem(i, 4, QtGui.QTableWidgetItem(str(al[q]['subjects'])))
            else:
                self.table.setItem(i, 4, QtGui.QTableWidgetItem(str('--')))
            
            print_body1[1] = i + 1
            print_body1[2] = str(al[q]['schno'])
            print_body1[3] = str(al[q]['name'])
            if 'clasz' in al[q]:
                print_body1[4] = str(al[q]['clasz'])
            else:
                print_body1[4] = str('--')
            if 'subjects' in al[q]:
                print_body1[5] = str(al[q]['subjects'])
            else:
                print_body1[5] = str('--')
            print_body[q] = print_body1        
            i += 1
            # set data
            
        print_footer = {}
        print_formart = {}
        print_footer[1] = 'S/N'
        print_footer[2] = ''
        print_footer[3] = ''
        print_footer[4] = ''
        print_footer[5] = ''
        print_formart[1] = ''
        print_formart[2] = ''
        print_formart[3] = ''
        print_formart[4] = ''
        print_formart[5] = ''
          
        self.report_table_holder = [session, print_header, print_body, print_footer, print_formart]
        
        self.table.hideColumn(0)
        self.tabl.close()
        self.tabl = self.table
        self.stackRightBar.setCurrentIndex(5)
        self.stackLeftBar.setCurrentIndex(0)
        self.checkBoxStack.setCurrentIndex(0)
        self.hbox2.addWidget(self.tabl)
        self.tabl.show()
    
    def myTable1(self, state, students = {}):       
        #get list of students
        
        #students = list(set(a))
        if students:
            self.students = students
        else:
            students ={}
   
        #all table headers titles
        cols = self.bioTable
        self.tableHeadersSelector(cols)
        print_header = {}
        a0 = 1
        for a in cols:
           print_header[a0] = a
           a0 += 1
            
        if state == 0:
                
            # initiate table if not exist
            if hasattr(Window, 'table'):
                pass
            else:
                self.table = QtGui.QTableWidget()
            
            
            #header
            header = self.table.horizontalHeader()
            header.setResizeMode(QtGui.QHeaderView.ResizeToContents)
            header.setStretchLastSection(True)
            header.setStyleSheet(self.tableHeaderStyle)
            vheader = self.table.verticalHeader()
            vheader.setStyleSheet(self.tableHeaderStyle)
            # Body
            self.table.setWindowTitle("Student Bio-Data")
            self.table.resize(900, 750)
            self.table.setFont(self.tableFont)
            self.table.setSortingEnabled(2)
            self.table.resizeColumnsToContents()
            self.table.setRowCount(len(students))
            self.table.setColumnCount(len(cols))
            self.table.setHorizontalHeaderLabels(cols)
            self.table.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
            self.table.customContextMenuRequested.connect(self.handleHeaderMenu)
            self.table.hideColumn(0)
            self.table.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
            self.table.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
            self.table.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
            
            i = 0
            print_body = {}
            #print(students)
            for j in students:
                print_body1 = {}
                q = j
                #row id
                self.table.setItem(i, 0, QtGui.QTableWidgetItem(str(q['id'])))
                #school id
                self.table.setItem(i, 1, QtGui.QTableWidgetItem(str(q['schno'])))
                #fullname
                fullname= str(q['surname'])+' '+str(q['firstname'])+' '+str(q['othername'])
                self.table.setItem(i, 2, QtGui.QTableWidgetItem(str(fullname.title())))
                #classname
                classname= str(q['classname'])+' '+str(q['classunitname'])
                self.table.setItem(i, 3, QtGui.QTableWidgetItem(str(classname.upper())))
                #gender
                if(q['gender'] == 0):
                    sex = 'Male';
                else:
                    sex = 'Female';
                self.table.setItem(i, 4, QtGui.QTableWidgetItem(str(sex)))
                #date of birth
                self.table.setItem(i, 5, QtGui.QTableWidgetItem(str(q['dob']).capitalize()))
                #nationality
                self.table.setItem(i, 6, QtGui.QTableWidgetItem(str(q['nation']).capitalize()))
                #State/LGA
                self.table.setItem(i, 7, QtGui.QTableWidgetItem(str(q['soo']).capitalize()+'/'+str(q['lga']).capitalize()))
                #Address
                self.table.setItem(i, 8, QtGui.QTableWidgetItem(str(q['addr'])))
                print_body1[1] = i + 1
                print_body1[2] = str(q['id'])
                print_body1[3] = str(fullname.title())
                print_body1[4] = str(classname.upper())
                print_body1[5] = str(sex)
                print_body1[6] = str(q['dob']).capitalize()
                print_body1[7] = str(q['nation']).capitalize()
                print_body1[8] = str(q['soo']).capitalize()+'/'+str(q['lga']).capitalize()
                print_body1[9] = str(q['addr'])
                print_body[q['id']] = print_body1
                i += 1
            # set data
                print_footer = {}
                
                print_formart = {}
                print_formart[1] = ''
                print_formart[2] = ''
                print_formart[3] = ''
                print_formart[4] = ''
                print_formart[5] = ''
                print_formart[6] = ''
                print_formart[7] = ''
                print_formart[8] = ''
                print_formart[9] = ''
    
                self.report_table_holder = [self.mainTerm, print_header, print_body, print_footer, print_formart]
            #self.table.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
            return self.table
        #report view
        elif state == 1:
            pass
    
    def myTable2(self, state, a = []):
        #get list of students
        students = list(set(a))
        #all table headers titles
        cols = self.conTable
        print_header = {}
        a0 = 1
        for a in cols:
           print_header[a0] = a
           a0 += 1
        self.tableHeadersSelector(cols)
        
        # initiate table if not exist
        if hasattr(Window, 'table'):
            self.table = QtGui.QTableWidget()
        else:
            self.table = QtGui.QTableWidget()

        #header
        header = self.table.horizontalHeader()
        header.setResizeMode(QtGui.QHeaderView.ResizeToContents)
        header.setStretchLastSection(True)
        header.setStyleSheet(self.tableHeaderStyle)
        vheader = self.table.verticalHeader()
        vheader.setStyleSheet(self.tableHeaderStyle)
        #table body structure
        self.table.setWindowTitle("Contact Information")
        self.table.resize(900, 250)
        self.table.setFont(self.tableFont)
        self.table.setSortingEnabled(2)
        self.table.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        self.table.setRowCount(len(students))
        self.table.setColumnCount(len(cols))
        self.table.setHorizontalHeaderLabels(cols)
        self.table.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self.handleHeaderMenu)
        
        #table content from db
        i = 0
        print_body = {}
        for j in students:
            print_body1 = {}
            q = list(j)
            self.table.setItem(i, 0, QtGui.QTableWidgetItem(str(q[0])))
            self.table.setItem(i, 1, QtGui.QTableWidgetItem(str(q[1])))
            fullname= q[2]+' '+q[3]+' '+q[4]
            self.table.setItem(i, 2, QtGui.QTableWidgetItem(str(fullname.title())))
            classname= q[32]+' '+q[31]
            self.table.setItem(i, 3, QtGui.QTableWidgetItem(str(classname.upper())))
            fg1 = str(q[12]).title() + '\n('+str(q[14]).capitalize()+') \n'+str(q[22])+' \n'+str(q[20])
            fg2 = str(q[13]).title() + '\n('+str(q[15]).capitalize()+') \n'+str(q[23])+' \n'+str(q[21])
            self.table.setItem(i, 4, QtGui.QTableWidgetItem(str(fg1)))
            self.table.setItem(i, 5, QtGui.QTableWidgetItem(str(q[16])+' '+str(q[17])))
            self.table.setItem(i, 6, QtGui.QTableWidgetItem(str(fg2)))
            self.table.setItem(i, 7, QtGui.QTableWidgetItem(str(q[18])+' '+str(q[19]))) 
            
            print_body1[1] = i + 1
            print_body1[2] = str(q[1])
            print_body1[3] = str(fullname.title())
            print_body1[4] = str(classname.upper())
            print_body1[5] = str(fg1)
            print_body1[6] = str(q[16])+' '+str(q[17])
            print_body1[7] = str(fg2)
            print_body1[8] = str(q[18])+' '+str(q[19])
            print_body[q[0]] = print_body1
            i += 1
            print_footer = {}
                
            print_formart = {}
            print_formart[1] = ''
            print_formart[2] = ''
            print_formart[3] = ''
            print_formart[4] = ''
            print_formart[5] = ''
            print_formart[6] = ''
            print_formart[7] = ''
            print_formart[8] = ''  
            
            self.report_table_holder = [self.mainTerm, print_header, print_body, print_footer, print_formart]
            
        #end of table content from DB   
        #table body structure    
        self.table.setColumnWidth(1, 50)
        self.table.setColumnWidth(3, 70)
        self.table.setColumnWidth(4, 300)
        self.table.setColumnWidth(6, 300)
        self.table.setWordWrap(True)
        self.table.resizeRowsToContents()
        self.table.hideColumn(0)
        self.table.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        return self.table
    
    def myTable3(self, a = [], b = [], c = [], d = {}, e ={}):
        students = list(set(a))
        subjects = list(set(b))
        subjects.sort()
        assessments = list(set(c))
        assessments.sort()
        self.d = d

        cn = Db()
        #subjects
        #get the subjects names
        #store in a dictionary
        self.store_sub_name = {}
        for subz in subjects:
            sub_name = None
            sub_name = cn.selectn('datas','', 1, {'id':subz})
            if sub_name:
                self.store_sub_name.update({int(subz):sub_name['abbrv']})
            
        #assessments 
        #get assessments name
        #store in a dictionary
        self.store_ca_name = {}
        for caz in assessments:
            ca_name = None
            ca_names = cn.selectn('datas', '', 1, {'id':caz})
            ca_name = cn.selectn('datas', '', 1, {'id':ca_names['name']})
            if ca_name:
                self.store_ca_name.update({int(caz):ca_name['abbrv']})
            
        #assements max score
        #get assements maximum scores
        #store them in a dictionary
        self.store_ca_max ={}
        for cazn in assessments:
            ca_name = None
            ca_name = cn.selectn('datas', '', 1, {'id':cazn})
         
            try:
                if ca_name:
                    self.store_ca_max.update({int(cazn):float(ca_name['abbrv'])})
                else:
                    self.store_ca_max.update({int(cazn):0})
            except:
                self.store_ca_max.update({int(cazn):0})
       
        #build header columns
        cols = ['id','Sch.No.', 'Fullname', 'Class']
        colsx = {1:'id', 2:'Sch.No.', 3:'Fullname', 4:'Class'}
        
        
        fnum = 4
        for f in e:
                colsx[self.store_sub_name[f].upper()] = {}
                for f1 in list(set(e[f])):
                    try:
                        fin_d = self.store_sub_name[f].upper()+'\n'+self.store_ca_name[f1].upper()+' ('+str(self.store_ca_max[f1]).upper()+')'
                        cols.append(fin_d)
                        colsx[self.store_sub_name[f].upper()][fnum] = self.store_ca_name[f1].upper()+'('+str(self.store_ca_max[f1]).upper()+')' 
                        fnum += 1
                    except:
                        pass
        
        
        print_header = {}
        a0 = 1
        for a in cols:
           print_header[a0] = a
           
        self.tableHeadersSelector(colsx, 1)
        self.checkBoxStack.setCurrentIndex(2)
        self.table = QtGui.QTableWidget()
    
        # initiate table
        header = self.table.horizontalHeader()
        header.setStyleSheet(self.tableHeaderStyle)
        vheader = self.table.verticalHeader()
        vheader.setStyleSheet(self.tableHeaderStyle)
        
        self.table.setWindowTitle("Academic Entries")
        self.table.resize(900, 250)
        self.table.setFont(self.tableFont)
        self.table.setSortingEnabled(2)
        self.table.setRowCount(len(students))
        self.table.setColumnCount(len(cols))
        self.table.setHorizontalHeaderLabels(cols)
        self.table.resizeColumnsToContents()
        self.table.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self.handleHeaderMenu)
        
        header_arr = {}
        self.set_subject = {}
        self.set_ca = {}
        
        jx = 4
        for f in e:
            for f1 in e[f]:
                self.set_subject[jx] = str(f)
                jx += 1
               
        jy = 4
        for f in e:
            for f1 in e[f]:
                self.set_ca[jy] = str(f1)
                jy += 1
               
        #assessment header bar        
        self.table.setItem(1, 0, QtGui.QTableWidgetItem(str(000)))
        self.table.setItem(1, 1, QtGui.QTableWidgetItem(str(000)))
        self.table.setItem(1, 2, QtGui.QTableWidgetItem(str('aaa')))
        self.table.setItem(1, 3, QtGui.QTableWidgetItem(str('clz')))
        #starting from the fourth column populate subjectsassessments
        jy = 4
        for f in e:
            ff = 0
            for f1 in e[f]:
                header_arr[f] = {}
                header_arr[f][ff] = str(f1)
                ff += 1
                self.table.setItem(1, jy, QtGui.QTableWidgetItem(str(f1)))
                jy += 1
        
        i = 0
        for j in students:
            q = list(j)
            self.table.setItem(i, 0, QtGui.QTableWidgetItem(str(q[0])))
            self.table.setItem(i, 1, QtGui.QTableWidgetItem(str(q[1])))
            fullname= q[2]+' '+q[3]
            self.table.setItem(i, 2, QtGui.QTableWidgetItem(str(fullname.title())))
            classname= str(q[32])+' '+str(q[31])
            self.table.setItem(i, 3, QtGui.QTableWidgetItem(str(classname.upper())))
            j = 4
            for f in e:
                for f1 in e[f]:
                    try:
                        num = 'AB'+str(q[0])+'CD'+str(f)+'EF'+str(f1)
                        fac = self.store_ca_max[f1]
                        nu1 = self.d[str(num)]
                        nu = float(fac) * float(nu1)
                    except KeyError:
                        nu = ''
                        
                    self.table.setItem(i, j, QtGui.QTableWidgetItem(str(nu)))
                    j += 1
            i += 1
        
        self.table.setColumnWidth(1, 50)
        self.table.setColumnWidth(2, 200)
        self.table.setWordWrap(True)
        self.table.resizeRowsToContents()
        self.table.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        # set data
        self.table.hideColumn(0)
        
        self.table.itemChanged.connect(lambda state, x = 2: self.getCellValue(state, x))
        #self.table.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        return self.table
    
    
    def myTable4(self, a = [], b = [], c = [], d = {}):
        students = list(set(a))
        affects = list(set(b))
        affects.sort()
        assessments = list(set(c))
        assessments.sort()
        self.d = d

        cn = Db()
        #affective
        #get the affective names
        #store in a dictionary
        self.store_affect_name = {}
        for subz in affects:
            sub_name = None
            sub_name = cn.selectn('datas','', 1, {'id':subz})
            if sub_name:
                self.store_affect_name.update({subz:sub_name['abbrv']})
            
        #affective types 
        #get affective type name
        #store in a dictionary
        self.store_affect_sub_name = {}
        for caz in assessments:
            ca_name = None
            ca_name = cn.selectn('datas', '', 1, {'id':caz})
            if ca_name:
                self.store_affect_sub_name.update({caz:ca_name['abbrv']})
            
        #set max affective max score 10
        self.store_affect_max = 10
      
    
        #build header columns
        cols = ['id','Sch.No.', 'Fullname', 'Class']
        colsx = ['id','Sch.No.', 'Fullname', 'Class']
        for f in affects:
                for f1 in assessments:
                    fin_d = self.store_affect_name[f].upper()+'\n'+self.store_affect_sub_name[f1].upper()+' (10)'
                    fin_dx = self.store_affect_name[f].upper()+':'+self.store_affect_sub_name[f1].upper()+'(10)'
                    cols.append(fin_d)
                    colsx.append(fin_dx)
                    
        
        self.tableHeadersSelector(colsx)
        self.checkBoxStack.setCurrentIndex(3)
        self.table = QtGui.QTableWidget()
    
        # initiate table
        header = self.table.horizontalHeader()
        header.setStyleSheet(self.tableHeaderStyle)
        vheader = self.table.verticalHeader()
        vheader.setStyleSheet(self.tableHeaderStyle)
        
        self.table.setWindowTitle("Affective Entries")
        self.table.resize(900, 250)
        self.table.setFont(self.tableFont)
        self.table.setSortingEnabled(2)
        self.table.setRowCount(len(students))
        self.table.setColumnCount(len(cols))
        self.table.setHorizontalHeaderLabels(cols)
        self.table.resizeColumnsToContents()
        self.table.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self.handleHeaderMenu)
        
        self.affect = affects
        self.affect_list = [0, 1, 2, 3]
        for f in assessments:
            self.affect_list.append(f)
                
            
        i = 0
        for j in students:
            q = list(j)
            self.table.setItem(i, 0, QtGui.QTableWidgetItem(str(q[0])))
            self.table.setItem(i, 1, QtGui.QTableWidgetItem(str(q[1])))
            fullname= q[2]+' '+q[3]
            self.table.setItem(i, 2, QtGui.QTableWidgetItem(str(fullname.title())))
            classname= str(q[32])+' '+str(q[31])
            self.table.setItem(i, 3, QtGui.QTableWidgetItem(str(classname.upper())))
            j = 4
            for f in assessments:
                try:
                    num = 'ABC'+str(q[0])+'DEF'+str(f)
                    fac = self.store_affect_max
                    nu1 = self.d[str(num)]
                    nu = float(fac) * float(nu1)
                except KeyError:
                    nu = ''
                        
                self.table.setItem(i, j, QtGui.QTableWidgetItem(str(nu)))
                j += 1
                    
            i += 1
        
        self.table.setColumnWidth(1, 50)
        self.table.setColumnWidth(2, 200)
        self.table.setWordWrap(True)
        self.table.resizeRowsToContents()
        self.table.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        
        # set data
        self.table.hideColumn(0)
        self.table.hideRow(0)
        self.table.hideRow(1)
        self.table.itemChanged.connect(lambda state, x = 3: self.getCellValue(state, x))
        #self.table.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        return self.table
    
      
    def myTable5(self, a = [], b = [], c = [], d = {}):
        students = list(set(a))
        psycho = list(set(b))
        psycho.sort()
        psycho_sub = list(set(c))
        psycho_sub.sort()
        self.d = d

        cn = Db()
        #affective
        #get the affective names
        #store in a dictionary
        self.store_psycho_name = {}
        for subz in psycho:
            sub_name = None
            sub_name = cn.selectn('datas','', 1, {'id':subz})
            if sub_name:
                self.store_psycho_name.update({subz:sub_name['abbrv']})
            
        #affective types 
        #get affective type name
        #store in a dictionary
        self.store_psycho_sub_name = {}
        for caz in psycho_sub:
            ca_name = None
            ca_name = cn.selectn('datas', '', 1, {'id':caz})
            if ca_name:
                self.store_psycho_sub_name.update({caz:ca_name['abbrv']})
            
        #set max affective max score 10
        self.store_psycho_max = 10
      
        #build header columns
        cols = ['id','Sch.No.', 'Fullname', 'Class']
        colsx = ['id','Sch.No.', 'Fullname', 'Class']
        for f in psycho:
                for f1 in psycho_sub:
                    fin_d = self.store_psycho_name[f].upper()+'\n'+self.store_psycho_sub_name[f1].upper()+' (10)'
                    fin_dx = self.store_psycho_name[f].upper()+':'+self.store_psycho_sub_name[f1].upper()+'(10)'
                    cols.append(fin_d)
                    colsx.append(fin_dx)
                    
        
        self.tableHeadersSelector(colsx)
        self.checkBoxStack.setCurrentIndex(4)
        self.table = QtGui.QTableWidget()
        
        # initiate table
        header = self.table.horizontalHeader()
        header.setStyleSheet(self.tableHeaderStyle)
        vheader = self.table.verticalHeader()
        vheader.setStyleSheet(self.tableHeaderStyle)
        
        self.table.setWindowTitle("Psychomoto Entries")
        self.table.resize(900, 250)
        self.table.setFont(self.tableFont)
        self.table.setSortingEnabled(2)
        self.table.setRowCount(len(students))
        self.table.setColumnCount(len(cols))
        self.table.setHorizontalHeaderLabels(cols)
        self.table.resizeColumnsToContents()
        self.table.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self.handleHeaderMenu)
        
        self.psycho = psycho
        self.psy_list = [0, 1, 2, 3]
        
        for f in psycho_sub:
            self.psy_list.append(f)
                
        
        i = 0
        for j in students:
            q = list(j)
            self.table.setItem(i, 0, QtGui.QTableWidgetItem(str(q[0])))
            self.table.setItem(i, 1, QtGui.QTableWidgetItem(str(q[1])))
            fullname= q[2]+' '+q[3]
            self.table.setItem(i, 2, QtGui.QTableWidgetItem(str(fullname.title())))
            classname= str(q[32])+' '+str(q[31])
            self.table.setItem(i, 3, QtGui.QTableWidgetItem(str(classname.upper())))
            j = 4
            for f in psycho_sub:
                try:
                    num = 'ABC'+str(q[0])+'DEF'+str(f)
                    fac = self.store_psycho_max
                    nu1 = self.d[str(num)]
                    nu = float(fac) * float(nu1)
                except KeyError:
                    nu = ''
                        
                self.table.setItem(i, j, QtGui.QTableWidgetItem(str(nu)))
                j += 1
            i += 1
        
        self.table.setColumnWidth(1, 50)
        self.table.setColumnWidth(2, 200)
        self.table.setWordWrap(True)
        self.table.resizeRowsToContents()
        self.table.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)   
        # set data
        self.table.hideColumn(0)
        self.table.hideRow(0)
        self.table.hideRow(1)
        
        self.table.itemChanged.connect(lambda state, x = 4: self.getCellValue(state, x))
        #self.table.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        return self.table
    
    def getCellValue(self, item, num):
        '''
        get the row and column of the selected cell
        from mytable 2, mytable 3, mytable 4
        '''
        rw = item.row()
        cl = item.column()
        vl = item.text()
        
        conf = False
        try:
            if(int(rw) > -1 and int(cl) > -1):
                conf = True
            else:
                pass
        except:
            pass
        '''
        if row and column number are available
        '''
        
        if (conf and conf == True):
            if num == 2:
                #get subject id
                _subjectID = self.set_subject[cl]
                _caID = self.set_ca[cl]
                _studentID = self.table.item(rw, 0).text()
                value = vl
                maxval = self.store_ca_max[int(_caID)]

            elif num == 3:
                #get affective
                _affectID = self.affect
                #get affective sub caqtegory
                _affect_subID = self.affect_list[cl]
                #get student id
                _studentID = self.table.item(rw, 0).text()
                #use the row id and column id to get value
                value = self.table.item(rw, cl).text()
                #get max value whic is contant 10
                maxval = self.store_affect_max
            elif num == 4:
                #get affective
                _psychoID = self.psycho
                #get affective sub caqtegory
                _psycho_subID = self.psy_list[cl]
                #get student id
                _studentID = self.table.item(rw, 0).text()
                #use the row id and column id to get value
                value = self.table.item(rw, cl).text()
                #get max value whic is contant 10
                maxval = self.store_psycho_max
            
            try:
                if(float(value) <= float(maxval)):
                #if the value entered is less than or equal to the maximum val for the columns
                #then proceed
                    if(isinstance(float(value), numbers.Real)):
                        #if its a real number or foalt continue
                        mscore = maxval
                        _value = float(value) / float(mscore)
                        cn = Db()
                        if num == 2:
                            students = cn.studentScore(self.majorSession, _studentID, _subjectID, _caID, _value)
                        elif num == 3:
                            students = cn.studentAffect(self.majorSession, _studentID, _affectID, _affect_subID, _value)
                        elif num == 4:
                            students = cn.studentPsy(self.majorSession, _studentID, _psychoID, _psycho_subID, _value)
                        
                        if(students == 1):   
                             self.table.item(rw, cl).setBackground(QtGui.QColor(255, 255, 255))
                        else:
                             self.table.item(rw, cl).setBackground(QtGui.QColor(100,100,150))
                    else:
                        self.table.item(rw, cl).setBackground(QtGui.QColor(100,100,150))
                
                else:
                #if the value entered is greater then the maximum val for the columns
                #show error by coloring cell background
                    self.table.item(rw, cl).setBackground(QtGui.QColor(100,100,150))
            except ValueError:
                self.table.item(rw, cl).setBackground(QtGui.QColor(100,100,150))
        else:
            pass
      
    def handleHeaderMenu(self, pos):
        print('column(%d)' % self.table.horizontalHeader().logicalIndexAt(pos))
        menu = QtGui.QMenu()
        menu.addAction('Add')
        menu.addAction('Delete')
        menu.exec_(QtGui.QCursor.pos())    
        
    def pullClass(self, a):
        self.a = a
        cn = Db()
        students = cn.selectn('datas', '' , '', {'subID':self.a, 'active':0})
        arr = {}
        
        for j in students:
            arr[j['id']] = j['name']
        return arr
    
    def pullSession(self):
        cn = Db()
        students = cn.selectn('session', '' , '', '')
       
        arr = {}
        for j in students:
            arr[j['id']] = j['name']
        return arr
    
    def pullTerm(self, a):
        self.a = a
        cn = Db()
        students = cn.selectn('terms', '' , '', {'sessionID':self.a})
        arr = {}
        for j in students:
            arr[j['id']] = j['name']
        return arr
    
    def lunchForm(self):
        self.form = SettingsManager()
        self.form.show()
    
    def lunchSettings(self, x):
        self.form = SettingsManager(x, self)
        self.form.show()
    
    def reloadSession(self):
        self.r = self.titleToolbar()
        self.r.hide()
        
    def lunchSessionForm(self):
        form = SessionsManager(self)
        form.show()
        
    def lunchGradeForm(self):
        self.form = GradeForm()
        self.form.show()
         
    def lunchClassTable(self, clasz, unit, term, grp):
        ar = []
        if unit and unit == 'xx':
            ar.append(clasz)
            self.form = StudentTable(term, [None], ar, [None],  grp)
            p = self.form.classStudent()
            q = self.form.className(ar)
        else:
            ar.append(unit)
            self.form = StudentTable(term, [None], [None], ar, grp)
            p = self.form.classUnitStudent()
            q = self.form.className(ar)
        
        self.tabl.close()
        self.stackRightBar.setCurrentIndex(0)
        self.stackLeftBar.setCurrentIndex(0)
        self.tabl = self.myTable1(0, p)
        self.tabletitle.setText(q)
        self.hbox2.addWidget(self.tabl)
        self.tabl.show()
    
        
    def getClassStudents(self, a, b, c):
        ar = []
        ar.append(b)
        if(int(c) == 0):
            self.form = StudentTable(a, [None], ar, [None] )
            p = self.form.classStudent()
        if(int(c) == 1):
            self.form = StudentTable(a, [None], [None],  ar)
            p = self.form.classUnitStudent()
            
        return p
    
    def getStore(self, a):
        g = Db()
        term = g.selectn('terms', '', 1, {'id':a})
        session = g.selectn('session', '', 1, {'id':term['sessionID']})
        h = Dat()
        r = h.storesData(session['id'], term['start_date'] , term['end_date'])
    
        self.myTableOthers(r,'' 'store')
    
        
    def getSessionData(self, state, terms, start = None, end = None):
        g = Db()
        if terms and terms > 0:
            term = g.selectn('terms', '', 1, {'id':terms})
            session = g.selectn('session', '', 1, {'id':term['sessionID']})
            session = term['sessionID']
            if start or end:
                start = start
                end = end
            else:
                start = term['start_date']
                end = term['end_date']
            
        h = Dat()
        fromx = datetime.utcfromtimestamp(float(start)).strftime('%d %m %Y')
        tox = datetime.utcfromtimestamp(float(end)).strftime('%d %m %Y')
        
        if state == 1:
            title = 'Expenses '+fromx+' '+tox
            r = h.expensesData(session, start , end)
        elif state == 2:
            title = 'Accounts '+fromx+' '+tox
            r = h.accountsData(session, start , end)
        elif state == 3:
            title = 'Mails '+fromx+' '+tox
            r = h.mailsData(session, start , end)
        elif state == 4:
            title = 'Conducts '+fromx+' '+tox
            r = h.conductsData(session, start , end)
        elif state == 5:
            title = 'Misconducts '+fromx+' '+tox
            r = h.misconductsData(session, start , end)
        elif state == 6:
            title = 'Stock '+fromx+' '+tox
            r = h.storesData(session, start , end)
            
            
        self.myTableOthers(r, title, state)
    
    def getClassAllStudents(self, a, c):
        if(int(c) == 0):
            self.form = StudentTable(a, [None], [None], [None] )
            p = self.form.classAllStudent()
        if(int(c) == 1):
            self.form = StudentTable(a, [None], [None],  [None])
            p = self.form.classAllExStudent()
        if(int(c) == 2):
            self.form = StudentTable(a, [None], [None],  [None])
            p = self.form.classAllCrStudent()
            
        return p
        
    def studentLunchForm(self):
        self.toolbarMain.hide()
        self.toolbarStudent.show()
        self.form = StudentForm()
        self.form.show()
        
    def callTerm(self):
        # select a file
        g = Db()
        return  g.select('terms', '', 1, {'active':1})
    
    def getTerm(self):
        # select a file
        dit = {}
        g = Db()
        g1= g.select('session', '', '', '')
        
        for g2 in g1:
            g3 = g.select('terms', '', '', {'sessionID':g2[0]})
            for g4 in g3:
                text = str(g2[1])+" Session "+str(g4[1])+" Term "
                dit.update({g4[0] : text}) 
            
        return dit
    
    def getDataById(self, a):
        # select a file
        g = Db()
        g1= g.selectn('datas', '', 1, {'id':a})
     
        return g1
    
    def getClass(self):
        # select a file
        dit = {}
        g = Db()
        g1= g.select('datas', '', '', {'pubID':1})
    
        for g2 in g1:
            dit.update({g2[0] : g2[2]}) 
        return dit
    
    def getClassUnit(self, a):
        # select a file
        dit = {}
        g = Db()
        g1= g.select('datas', '', '', {'subID':a})
        
        for g2 in g1:
            dit.update({g2[0] : g2[2]}) 
            
        return dit
            
    
    def getSubject(self):
        # select a file
        g = Db()
        return  g.select('terms', '', 1, {'active':1})
    
    def getCa(self):
        # select a file
        g = Db()
        return  g.select('terms', '', 1, {'active':1})
    
    
    def getStudentAssessments(self, session, student=[], subject=[], ca=[]):
        _session = session
        _student = student
        _subject = subject
        _ca = ca
        g = Db()
        data = g.selectStudentsCa(_session, _student, _subject, _ca)
        return data


    def getStudentAffective(self, session, student=[], subject=[], ca=[]):
        _session = session
        _student = student
        _subject = subject
        _ca = ca
        g = Db()
        data = g.selectStudentsAffective(_session, _student, _subject, _ca)
        return data
    
    def getStudentPsychomoto(self, session, student=[], subject=[], ca=[]):
        _session = session
        _student = student
        _subject = subject
        _ca = ca
        g = Db()
        data = g.selectStudentsPsychomoto(_session, _student, _subject, _ca)
        return data
    
    def callSession(self, a):
        # select a file
        self.a = a
        g = Db()
        return  g.select('session', '', 1, {'id':self.a})
    
    def pullStudents(self, a):
        
        cn = Db()
        students = cn.select('students', '' , 500, {'active':0})
        return students
    
    def pullSearch(self):
        search = self.search_box.text()
        session = self.mainTermSession
        students = {}
        if len(search) > 2:
            cn = Db()
            students = cn.selectSearch(session, search)
            self.tabletitle.setText('SEARCHING: '+str(search))
            
        
        if students and len(students) >  0:
            self.tabl.close()    
            self.tabl = self.myTableSearch(students)
            self.stackRightBar.setCurrentIndex(0)
            self.stackLeftBar.setCurrentIndex(0)
            self.hbox2.addWidget(self.tabl)
            self.tabl.show()
        #return students
    def pullSearchTable(self):
        search = self.search_table.text()
        tab = self.table
        
        tc = tab.rowCount()
        for i in range(tc):
            tab.showRow(i)
            
        
        if len(search) > 2:
            t = tab.findItems(search,  QtCore.Qt.MatchContains)
            stores = {}
            store = []
            for tr in t:
                stores[tr.row()] = tr
                store.append(tr.row())
                tab.showRow(tr.row())
             
            for i in range(tc):
                if i in store:
                    pass
                else:
                  tab.hideRow(i)  
           
    
    def lunchStudentAddForm(self):
        self.form = StudentForm()
        self.form.show()
        
    def lunchStudentEditForm(self):
        sid = self.mySelectTable()
        y = 0
        
        for s in sid:
            
            form = StudentEditForm(s, y)
            form.show()
            y = y + 10
            
    def lunchStudentProfile(self):
        sid = self.mySelectTable()
        y = 0
        for s in sid:
            self.forms = StudentProfile(s, y)
            self.forms.show()
            y = y + 10
            
    def lunchChangeClass(self):
        students = self.mySelectTable()
        session = self.activeTerm()
        post = ChangeClassDialog(session, students)
        post.show()
        if post.exec_() == QtGui.QDialog.Accepted:
               rtt = post.getValue()
        return rtt
    
    def lunchRemoveClass(self):
        students = self.mySelectTable()
        session = self.activeTerm()
        post = RemoveClassDialog(session, students)
        post.show()
        if post.exec_() == QtGui.QDialog.Accepted:
               rtt = post.getValue()
    
        return rtt
    
    def lunchSubjectClass(self):
        students = self.mySelectTable()
        session = self.activeTerm()
        post = SubjectClassDialog(session, students)
        post.show()
        if post.exec_() == QtGui.QDialog.Accepted:
               rtt = post.getValue()
    
        return rtt
    
    def lunchPrintTable(self):
        self.pageDisplay()
        
    def lunchFeeDialog(self):
        sid = self.mainTermSession
        post = TermFeeDialog(sid)
        post.show()
        
    def lunchExpenseDialog(self):
        sid = self.mainSession
        post = ExpensesDialog(sid)
        post.show()
        
    def lunchStoreDialog(self):
        sid = self.mainSession
        post = StoreDialog(sid)
        post.show()
        
    def lunchPayDialog(self):
        std = self.mySelectTable()
        student = std[0]
        sid = self.mainTermSession
        post = TermPayDialog(student, sid)
        post.show()  
    
    def academicDataPlus(self):
        _session = self.mainTermSession
        student_id = self.mySelectTable()
        if len(student_id) > 0:
            form = StudentTable(_session, [None], [None], [None] )
            studentsIDs = form.selectedStudents(student_id)
            self.academicData(_session, student_id, studentsIDs)
        
    def affectiveDataPlus(self):
        _session = self.mainTermSession
        student_id = self.mySelectTable()
        if len(student_id) > 0:
            form = StudentTable(_session, [None], [None], [None] )
            studentsIDs = form.selectedStudents(student_id)
            self.affectiveData(_session, student_id, studentsIDs)
        
    def psychoDataPlus(self):
        _session = self.mainTermSession
        student_id = self.mySelectTable()
        if len(student_id) > 0:
            form = StudentTable(_session, [None], [None], [None] )
            studentsIDs = form.selectedStudents(student_id)
            self.psychoData(_session, student_id, studentsIDs)
        
    def academicData(self, _session, student_id, studentsIDs):
        self.post = SubjectCaDialog(_session)
        self.post.show()
        rtt = []
        if self.post.exec_() == QtGui.QDialog.Accepted:
            rtt = self.post.getValue()
                    
        if(rtt[1] == 0):
            subs = list()
            cas = list()
            for x in rtt[0]:
                subs.append(x)
                for y in rtt[0][x]:
                    cas.append(y)
            subs = list(set(subs))
            cas =list(set(cas))
            rtt1 = self.getStudentAssessments(_session, student_id, subs, cas)
            
            _arr = {}
            for g in rtt1:
                #try:
                if int(g['subjectID']) > 0 and int(g['caID']) > 0 and g['subjectID'] in rtt[0] and isinstance(rtt[0][int(g['subjectID'])], list) and int(g['caID']) in rtt[0][int(g['subjectID'])]:
                        st = 'AB'+str(g['studentID'])+'CD'+str(g['subjectID'])+'EF'+str(g['caID'])
                        _arr.update({st:g['score']})
                #except:
                #    pass
            self.tabl.close()    
            self.tabl = self.myTable3(studentsIDs, subs, cas, _arr, rtt[0])
            self.stackRightBar.setCurrentIndex(0)
            self.stackLeftBar.setCurrentIndex(0)
            self.hbox2.addWidget(self.tabl)
            self.tabl.show()
                
        elif(rtt[1] == 1):
            self.tabl.close()
            self.pageDisplay()
            #if hasattr(self, 'web'):
                #self.web.close() 
                
            #self.web = QWebView()
            #self.web.load(QtCore.QUrl("http://localhost:5000/"+str(_session)+"/"+_B+"/"+_C+"/"+_D+""))
            #self.web.page().setForwardUnsupportedContent(True)
            #self.hbox2.removeWidget(self.tabl)
            #self.hbox2.removeWidget(self.web)
            #self.hbox2.addWidget(self.web)
            #self.web.show()  
            
    def affectiveData(self, _session, student_id, studentsIDs):
        self.post = AffectiveCaDialog()
        self.post.show()
        if self.post.exec_() == QtGui.QDialog.Accepted:
            rtt = self.post.getValue()
            rtt1= self.getStudentAffective(_session, student_id, rtt[0], rtt[1])
        _arr = {}
        if rtt1:
            for g in rtt1:
                st = 'ABC'+str(g['studentID'])+'DEF'+str(g['caID'])
                _arr.update({st:g['score']})
        else:
           rtt[0] = {} 
           rtt[1] = {}
               
            
        self.tabl.close()    
        self.tabl = self.myTable4(studentsIDs,  rtt[0], rtt[1], _arr )
        self.stackRightBar.setCurrentIndex(0)
        self.stackLeftBar.setCurrentIndex(0)
        self.hbox2.addWidget(self.tabl)
        self.tabl.show()
            
    def psychoData(self, _session, student_id, studentsIDs):
            #pyschomotor
            self.post = PsychomotoCaDialog()
            self.post.show()
            if self.post.exec_() == QtGui.QDialog.Accepted:
                rtt = self.post.getValue()
                rtt1= self.getStudentPsychomoto(_session, student_id, rtt[0], rtt[1])
            _arr = {}
            for g in rtt1:
                st = 'ABC'+str(g['studentID'])+'DEF'+str(g['caID'])
                _arr.update({st:g['score']})
                        
            self.tabl.close()    
            self.tabl = self.myTable5(studentsIDs,  rtt[0], rtt[1], _arr )
            self.stackRightBar.setCurrentIndex(0)
            self.stackLeftBar.setCurrentIndex(0)
            self.hbox2.addWidget(self.tabl)
            self.tabl.show()
    
    

if __name__ == "__main__":
    #import sys
    app = QtGui.QApplication(sys.argv)
    app.setStyle("cleanlooks")
    GUI = Window()
    GUI.main()
    sys.exit(app.exec_())    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
        




#if __name__ == "__main__":
#    import sys
#    app = QtGui.QApplication(sys.argv)
##    MainWindow = QtGui.QMainWindow()
#    ui = Ui_MainWindow()
#    ui.setupUi(MainWindow)
#    MainWindow.show()
#    sys.exit(app.exec_())
