# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
from PyQt4 import QtCore, QtGui
from PyQt4.QtWebKit import QWebView
from connect import Db
from connectdata import Dat
from frmclass import Form
from frmstudent import StudentForm
from frmstudentedit import StudentEditForm
from frmstudentprofile import StudentProfile
from frmsession import SessionForm
from frmsubject import SubjectForm
from frmgrade import GradeForm
from frmca import CaForm
from frmaffective import AffectiveForm
from frmpsyco import PsycoForm
from frmexpense import ExpenseForm
from frmfee import FeeForm
from studenttable import StudentTable
from dialogtermfee import TermFeeDialog
from dialogsubject import SubjectCaDialog
from dialogaffective import AffectiveCaDialog
from dialogpsychomoto import PsychomotoCaDialog
from dialogchangeclass import ChangeClassDialog, RemoveClassDialog
from printtable import PrintTable
from collections import defaultdict
from jinja2 import Template
import numbers
import sys
import sip
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
        #table font and header
        self.tableFont = QtGui.QFont()
        self.tableFont.setFamily('Century Gothic')
        self.tableHeaderStyle = "::section {""background-color: teal; color:white}"
        
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

    def menuUi(self):
        itz = self.pullClass(1)
        sess = self.activeTerm()
        
        extractQuit = QtGui.QAction(self) 
        extractQuit.setStatusTip('File')
          
        self.statusBar()
        
        mainMenu = self.menuBar()
        
        #file menu
        fileMenu = mainMenu.addMenu('&File')
        exitMenu = QtGui.QAction('&Exit', self)
        #exitMenu.setShortT('CTRL+Q')
        exitMenu.setStatusTip('Close Application')
        exitMenu.triggered.connect(self.lunchForm)
        fileMenu.addAction(exitMenu)
        
        #session menu
        sessionMenu = mainMenu.addMenu('&Session')
        ## student menu dynamic items
        ses = self.pullSession()
        dumpClass = {}
        for k in ses:
           act = str(ses[k])
           stud = sessionMenu.addMenu(act)
           arr = self.pullTerm(k)
           for j in arr:
               act1 = str(arr[j]).upper()
               studs = stud.addMenu(act1)
    
               st = QtGui.QAction('Class', self)
               st.triggered.connect(lambda state, x = j: self.myTableClassUnit(0, x))
               studs.addAction(st)
               
               fe = QtGui.QAction('Fees', self)
               fe.triggered.connect(lambda state, x = j: self.myTableClassUnitFee(0, x))
               studs.addAction(fe)
               
               ex = QtGui.QAction('Expenses', self)
               ex.triggered.connect(lambda state, x = j: self.lunchClassUnitTable(x))
               studs.addAction(ex)
               
               fc = QtGui.QAction('Facilities', self)
               fc.triggered.connect(lambda state, x = j: self.lunchClassUnitTable(x))
               studs.addAction(fc)
              
        #student menu
        studentMenu = mainMenu.addMenu('&Student')
        ## student menu static items
        studentAddMenu = QtGui.QAction('&Add Student', self)
        studentAddMenu.setShortcut('CTRL+A')
        studentAddMenu.setStatusTip('Add Students')
        studentAddMenu.triggered.connect(self.studentLunchForm)
        
        studentAllMenu = QtGui.QAction('&All Students', self)
        studentAllMenu.setShortcut('CTRL+P+A')
        studentAllMenu.setStatusTip('All Students')
        studentAllMenu.triggered.connect(lambda: self.genTable(0))
        
        studentExMenu = QtGui.QAction('&Ex. Students', self)
        studentExMenu.setShortcut('CTRL+E')
        studentExMenu.setStatusTip('All Students')
        studentExMenu.triggered.connect(lambda:self.genTable(1))
        
        studentCrMenu = QtGui.QAction('&Current Students', self)
        studentCrMenu.setShortcut('CTRL+C')
        studentCrMenu.setStatusTip('Current Students')
        studentCrMenu.triggered.connect(lambda: self.genTable(2))
        
        studentMenu.addAction(studentAddMenu)
        studentMenu.addAction(studentAllMenu)
        studentMenu.addAction(studentExMenu)
        studentMenu.addAction(studentCrMenu)
        studentMenu.addSeparator()
        
        ## student menu dynamic items
        dumpClass = {}
        for k in itz:
           act = '& All '+str(itz[k])
           stud = QtGui.QAction(act, self)
           dumpClass[k] = stud
           stud.triggered.connect(lambda state, x = k, y = sess[2]: self.lunchClassTable(x, y))
           studentMenu.addAction(stud)
           
        studentMenu.addSeparator()
           
        for k in itz:
           act = '&'+str(itz[k])
           stud = studentMenu.addMenu(act)

           arr = self.pullClass(k)
           for j in arr:
               act1 = '&'+str(arr[j])
               st = QtGui.QAction(act1, self)
               st.triggered.connect(lambda state, x = j, y = sess[2] : self.lunchClassUnitTable(x, y))
               stud.addAction(st)

        
        
        #staff menu
        staffMenu = mainMenu.addMenu('&Staff')
        staffMenu.addAction(extractQuit)
        

        #settings menu
        settingMenu = mainMenu.addMenu('Se&ttings')
        ## student menu static items
        sessionMenu = QtGui.QAction('&Session Manager', self)
        sessionMenu.setStatusTip('Manage Academic Session')
        sessionMenu.triggered.connect(self.lunchSessionForm)
        
        classMenu = QtGui.QAction('&Class Manager', self)
        classMenu.setStatusTip('Manage Class settings')
        classMenu.triggered.connect(self.lunchForm)
        
        assessMenu = QtGui.QAction('Assess&ment', self)
        assessMenu.setStatusTip('Manage assessment')
        assessMenu.triggered.connect(self.lunchCaForm)
        
        affectMenu = QtGui.QAction('&Affective/Attitude', self)
        affectMenu.setStatusTip('Manage Affective domain')
        affectMenu.triggered.connect(self.lunchAffectiveForm)
        
        psycoMenu = QtGui.QAction('&Psychomotor/Skills', self)
        psycoMenu.setStatusTip('Manage skills')
        psycoMenu.triggered.connect(self.lunchPsycoForm)
        
        subjectMenu = QtGui.QAction('&Subject Manager', self)
        subjectMenu.setStatusTip('Manage subjects taught')
        subjectMenu.triggered.connect(self.lunchSubjectForm)
        
        gradeMenu = QtGui.QAction('&Grades Manager', self)
        gradeMenu.setStatusTip('Manage grading system')
        gradeMenu.triggered.connect(self.lunchGradeForm)
        
        feeMenu = QtGui.QAction('&Fees Manager', self)
        feeMenu.setStatusTip('Manage fees type')
        feeMenu.triggered.connect(self.lunchFeeForm)
        
        expenseMenu = QtGui.QAction('&Expenses Manager', self)
        expenseMenu.setStatusTip('Expense type')
        expenseMenu.triggered.connect(self.lunchExpenseForm)
        
        settingMenu.addAction(sessionMenu)
        settingMenu.addAction(classMenu)
        settingMenu.addAction(subjectMenu)
        settingMenu.addAction(assessMenu)
        settingMenu.addAction(affectMenu)
        settingMenu.addAction(psycoMenu)
        settingMenu.addAction(gradeMenu)
        settingMenu.addAction(feeMenu)
        settingMenu.addAction(expenseMenu)
    
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
        sessionss = self.getTerm()
        clasz = self.getClass()
        
        
        self.d_session = QtGui.QLabel('Quick Selection')
        self.d_sessionData = QtGui.QComboBox()
        for ss in sessionss:
            self.d_sessionData.addItem(sessionss[ss], ss)
        
       
        self.d_classData = QtGui.QComboBox()
        for cc in clasz:
            self.d_classData.addItem(clasz[cc], str(cc)+',xx')
            claszunit = self.getClassUnit(cc)
            for uu in claszunit:
                self.d_classData.addItem(str(clasz[cc]).upper()+' '+str(claszunit[uu]).upper(), str(uu)+','+str(cc))
       
        displayInfo = {}
        displayInfo.update({1: 'BioData'})
        displayInfo.update({2: 'Contact Information'})
        displayInfo.update({3: 'Photo Gallery'})
        displayInfo.update({4: 'Academic'})
        displayInfo.update({5: 'Affective'})
        displayInfo.update({6: 'Psychomotor'})
        displayInfo.update({7: 'Report Card'})
        displayInfo.update({8: 'Fees and payments'})
        
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
        self.mainStack.addWidget(self.studentStack)
        self.mainStack.addWidget(self.staffStack)
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
            self.mainStack.setCurrentIndex(a)
        else:
            pass
            
    def genTable(self, a):
        _session = self.mainTermSession
        if a == 0:
            studentsIDs = self.getClassAllStudents(_session, 0)
        elif a == 1:
            studentsIDs = self.getClassAllStudents(_session, 1)
        elif a == 2:
            studentsIDs = self.getClassAllStudents(_session, 2)
            
            
        student_id = []
        
        for dx in studentsIDs :
            student_id.append(dx[0])
            
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
            self.tabl.close()  
            self.web = QWebView()
            self.web.load(QtCore.QUrl("http://localhost:5000/"+str(_session)+"/"+str(student_id)+"/"+str(_session)+"/"+str(_session)+""))
            self.web.page().setForwardUnsupportedContent(True)
            self.hbox2.removeWidget(self.tabl)
            self.hbox2.removeWidget(self.web)
            self.hbox2.addWidget(self.web)
            self.web.show()
            
            
        elif(_display == 8): 
            #fees and payments
            pass
            
        elif(_display == 9):
            pass
            
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
        printer = QtGui.QPrinter()
        pdffile ='test.pdf'
        printer.setResolution(200)
        printer.setPageSize(QtGui.QPrinter.Letter)
        printer.setOutputFormat(QtGui.QPrinter.PdfFormat)
        printer.setOutputFileName(pdffile)
        printer.setPageMargins(5, 5, 5, 10, QtGui.QPrinter.Millimeter)
        document = self.document
        #document.setPageSize(QtGui.QSizeF(printer.pageRect().size()))
        document.print_(printer)
    
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
        document = self.document
    
    def lunchPrintExcel(self):
        document = self.document
        
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
        
        #create the Right and left stack for srudents page
        self.stackRightBar = QtGui.QStackedWidget()
        self.stackLeftBar = QtGui.QStackedWidget()
        self.checkBoxStack = QtGui.QStackedWidget()
        
        self.leftReportTable = QtGui.QWidget()  #for tables students
        self.leftReportText = QtGui.QWidget()   #for students reports
        self.rightPrimaryMenu = QtGui.QWidget() #for main students menu
        self.rightPrintMenu = QtGui.QWidget()
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
        self.stackLeftBar.addWidget(self.rightPrimaryMenu)
        self.stackLeftBar.addWidget(self.rightPrintListMenu)
        
        self.hbox4 = QtGui.QHBoxLayout()
        self.hbox4.addWidget(self.tabletitle)
        self.hbox4.addStretch()
        self.hbox4.addWidget(self.tablerefresh)
        
        self.hbox4x = QtGui.QHBoxLayout()   
        self.hbox4x.addWidget(self.reportTitle)
        self.hbox4x.addStretch()
        self.hbox4x.addWidget(self.reportPrint)
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
        self.pbMove.setText("Change Student(s) Class")
        self.pbMove.setStyleSheet(bntstyle)
        self.pbMove.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        
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
        
        self.connect(self.pbAdd, QtCore.SIGNAL("clicked()"), self.lunchStudentAddForm)
        self.connect(self.pbEdit, QtCore.SIGNAL("clicked()"), self.lunchStudentEditForm)
        self.connect(self.pbProfile, QtCore.SIGNAL("clicked()"), self.lunchStudentProfile)
        self.connect(self.pbMove, QtCore.SIGNAL("clicked()"), self.lunchChangeClass)
        self.connect(self.pbRemove, QtCore.SIGNAL("clicked()"), self.lunchRemoveClass)
        self.connect(self.pbPhoto, QtCore.SIGNAL("clicked()"), self.lunchStudentAddForm)
        self.connect(self.pbPrint, QtCore.SIGNAL("clicked()"), self.lunchBack)
        self.connect(self.pbPrintPrev, QtCore.SIGNAL("clicked()"), self.quickReport)
        self.connect(self.pbPrintPdf, QtCore.SIGNAL("clicked()"), self.lunchPrintPreview)
        self.connect(self.pbPrintCsv, QtCore.SIGNAL("clicked()"), self.lunchPrintCsv)
        self.connect(self.pbPrintExcel, QtCore.SIGNAL("clicked()"), self.lunchPrintExcel)
        self.connect(self.pbPay, QtCore.SIGNAL("clicked()"), self.lunchStudentAddForm)
        self.connect(self.pbEmail, QtCore.SIGNAL("clicked()"), self.lunchStudentAddForm)
        self.connect(self.pbAcademic, QtCore.SIGNAL("clicked()"), self.academicDataPlus)
        self.connect(self.pbAffective, QtCore.SIGNAL("clicked()"), self.affectiveDataPlus)
        self.connect(self.pbPsyco, QtCore.SIGNAL("clicked()"), self.psychoDataPlus)
        self.connect(self.pbBack, QtCore.SIGNAL("clicked()"), self.lunchForward)
        
        addImg = QtGui.QPixmap('img/add.png').scaled(picstyle, picstyle1)
        editImg = QtGui.QPixmap('img/edit.png').scaled(picstyle, picstyle1)
        profileImg = QtGui.QPixmap('img/profile.png').scaled(picstyle, picstyle1)
        moveImg = QtGui.QPixmap('img/change.png').scaled(picstyle, picstyle1)
        removeImg = QtGui.QPixmap('img/remove.png').scaled(picstyle, picstyle1)
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
        
        #Left main menu
        self.f_box.addWidget(self.picProfile, 1, 0)
        self.f_box.addWidget(self.pbProfile, 1, 1)
        self.f_box.addWidget(self.picAdd, 0, 0)
        self.f_box.addWidget(self.pbAdd, 0, 1)
        self.f_box.addWidget(self.picEdit, 2, 0)
        self.f_box.addWidget(self.pbEdit, 2, 1)
        self.f_box.addWidget(self.picMove, 3, 0)
        self.f_box.addWidget(self.pbMove, 3, 1)
        self.f_box.addWidget(self.picRemove, 4, 0)
        self.f_box.addWidget(self.pbRemove, 4, 1)
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
        self.f_box.addWidget(self.picPrint, 11, 0)
        self.f_box.addWidget(self.pbPrint, 11, 1)
        
        #Left print menu
        self.f_box1.addWidget(self.picPrevPrint, 1, 0)
        self.f_box1.addWidget(self.pbPrintPrev, 1, 1)
        self.f_box1.addWidget(self.picPdfPrint, 0, 0)
        self.f_box1.addWidget(self.pbPrintPdf, 0, 1)
        self.f_box1.addWidget(self.picCsvPrint, 2, 0)
        self.f_box1.addWidget(self.pbPrintCsv, 2, 1)
        self.f_box1.addWidget(self.picExcelPrint, 3, 0)
        self.f_box1.addWidget(self.pbPrintExcel, 3, 1)
        self.f_box1.addWidget(self.picBack, 3, 0)
        self.f_box1.addWidget(self.pbBack, 3, 1)
        
        self.b_box = QtGui.QHBoxLayout()
        self.b_box.addLayout(self.b1_box)
        self.b_box.addLayout(self.b2_box)
        self.b_box.addLayout(self.b3_box)
        
        frm_search  = QtGui.QFormLayout()
        search_box = QtGui.QLineEdit()
        search_btn = QtGui.QPushButton('Search')
        frm_search.addRow(search_box, search_btn)
        
        #Table titles
        self.bioTable = ['id','Sch.No.', 'FullName', 'Class','Gender', 'Birth Date', 'Nationality', 'State/LGA', 'Address']
        self.conTable  = ['id','Sch.No.', 'Fullname', 'Class', 'First Guardian', 'Phone No.', 'Second Gurdian', 'Phone No.']
        self.acaTable  = ['id','Sch.No.', 'Fullname', 'Class']
        self.affTable  = ['id','Sch.No.', 'Fullname', 'Class']
        self.psyTable  = ['id','Sch.No.', 'Fullname', 'Class']
        self.classUnitTable  = ['id','Class', 'Unit', 'Male', 'Female', 'Total']
        self.classTable  = ['id','Class', 'Male', 'Female', 'Total']
        self.classUnitFeeTable  = ['id','Class', 'Unit', 'Male', 'Female', 'Population', 'Fee', 'Amount', 'Total Amount' ]
        self.classFeeTable  = ['id','Class','Students', 'Fees', 'Paid', 'Balance' ]
        
        self.tableHeadersSelector(1,  self.bioTable, 'a')
        self.tableHeadersSelector(2,  self.conTable, 'b')
        self.tableHeadersSelector(3,  self.conTable, 'c')
        self.tableHeadersSelector(4,  self.affTable, 'd')
        self.tableHeadersSelector(5,  self.psyTable, 'e')
        self.tableHeadersSelector(6,  self.classUnitTable, 'f')
        self.tableHeadersSelector(7,  self.classTable, 'g')
        self.tableHeadersSelector(8,  self.classUnitFeeTable, 'h')
        self.tableHeadersSelector(9,  self.classFeeTable, 'i')
         
        bioWidget = QtGui.QWidget()
        conWidget = QtGui.QWidget()
        acaWidget = QtGui.QWidget()
        affWidget = QtGui.QWidget()
        psyWidget = QtGui.QWidget()
        cutWidget = QtGui.QWidget()
        ctWidget = QtGui.QWidget()
        cuftWidget = QtGui.QWidget()
        cftWidget = QtGui.QWidget()
        
        bioWidget.setLayout(self.hc1_box)
        conWidget.setLayout(self.hc2_box)
        acaWidget.setLayout(self.hc3_box)
        affWidget.setLayout(self.hc4_box)
        psyWidget.setLayout(self.hc5_box)
        cutWidget.setLayout(self.hc6_box)
        ctWidget.setLayout(self.hc7_box)
        cuftWidget.setLayout(self.hc8_box)
        cftWidget.setLayout(self.hc9_box)
        
        self.checkBoxStack.addWidget(bioWidget)
        self.checkBoxStack.addWidget(conWidget)
        self.checkBoxStack.addWidget(acaWidget)
        self.checkBoxStack.addWidget(affWidget)
        self.checkBoxStack.addWidget(psyWidget)
        self.checkBoxStack.addWidget(cutWidget)
        self.checkBoxStack.addWidget(ctWidget)
        self.checkBoxStack.addWidget(cuftWidget)
        self.checkBoxStack.addWidget(cftWidget)
        
        self.checkBoxStack.setCurrentIndex(0)
        
        self.f_box2 = QtGui.QVBoxLayout()
        self.f_box2.addWidget(self.checkBoxStack)
        self.rightPrintMenu.setLayout(self.f_box1) #for print menu
        self.rightListMenu.setLayout(self.f_box2)
         
        sub_box = QtGui.QVBoxLayout()
        sub_box.addWidget(self.rightPrintMenu)
        sub_box.addWidget(scrollArea)
        
        self.rightPrimaryMenu.setLayout(self.f_box)
        self.rightPrintListMenu.setLayout(sub_box)
        
        self.Frame2 = QtGui.QVBoxLayout()
        self.Frame2.addLayout(frm_search)
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
   
    def windowMain(self):
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        font.setFamily('Tahoma')
        
        self.winBox = QtGui.QHBoxLayout(self)
        self.welcomeStack.setStyleSheet("background-image: url(img/win1.jpg); background-position:center;  background-size:contain; background-repeat:no-repeat")
        self.welcomeStack.setLayout(self.winBox)
        self.wBox = QtGui.QWidget()
        self.wBox.setFixedWidth(220)
        self.wBox.setStyleSheet("background-color: white")
        self.wBox.setFont(font)
        #self.wBox.setLayout(self.Frame2)
        self.wBox.setStyleSheet("background-color: white; width:300px; height:200px")
        self.winBox.addWidget(self.wBox)     
        self.wBox.show()
        
    def tableHeadersSelector(self, place,  primecol, add):
        
        if place == 1:
            if hasattr(self, 'hc1_box'):
                self.hc1_box = QtGui.QVBoxLayout()
                places = self.hc1_box
            else:
                self.hc1_box = QtGui.QVBoxLayout()
                places = self.hc1_box
        elif place == 2:
            if hasattr(self, 'hc2_box'):
                self.hc2_box = QtGui.QVBoxLayout()
                places = self.hc2_box
            else:
                self.hc2_box = QtGui.QVBoxLayout()
                places = self.hc2_box
                
        elif place == 3:
            if hasattr(self, 'hc3_box'):
                places = self.hc3_box
            else:
                self.hc3_box = QtGui.QVBoxLayout()
                places = self.hc3_box
        
        elif place == 4:
            if hasattr(self, 'hc4_box'):
                places = self.hc4_box
            else:
                self.hc4_box = QtGui.QVBoxLayout()
                places = self.hc4_box
                
        elif place == 5:
            if hasattr(self, 'hc5_box'):
                places = self.hc5_box
            else:
                self.hc5_box = QtGui.QVBoxLayout()
                places = self.hc5_box
                
        elif place == 6:
            if hasattr(self, 'hc6_box'):
                places = self.hc6_box
            else:
                self.hc6_box = QtGui.QVBoxLayout()
                places = self.hc6_box
                
        elif place == 7:
            if hasattr(self, 'hc7_box'):
                places = self.hc7_box
            else:
                self.hc7_box = QtGui.QVBoxLayout()
                places = self.hc7_box
                
        elif place == 8:
            if hasattr(self, 'hc8_box'):
                places = self.hc8_box
            else:
                self.hc8_box = QtGui.QVBoxLayout()
                places = self.hc8_box
                
        elif place == 9:
            if hasattr(self, 'hc9_box'):
                places = self.hc9_box
            else:
                self.hc9_box = QtGui.QVBoxLayout()
                places = self.hc9_box
                
        
                
        for i in reversed(range(places.count() - 1)):
            #print(places.itemAt(i).widget())
            if places.itemAt(i).widget() != None:
                sz = places.itemAt(i).widget()
                places.removeWidget(sz)
                #places.itemAt(i).widget().deleteLater()
                if sz != None: 
                    sip.delete(sz)
                #print(str(i)+'=rem')

        
                
        for s in primecol:
            if (s != 'id'):
                num = primecol.index(s)
                c = QtGui.QCheckBox('cb'+str(add)+str(num))
                c.setText(str(s).upper())
                c.setObjectName("chk"+str(add)+"="+str(num))
                c.setChecked(True)
                c.toggled.connect(lambda state, x=num: self.tableHeadersSelectorAction(state, x))
                places.addWidget(c)
        return places
    
    def tableHeadersChecked(self, places):
        self.check_array = []
        for i in reversed(range(places.count() - 1)):
            if ((places.itemAt(i).widget() != None) and  (places.itemAt(i).widget().isChecked)):
                fn = places.itemAt(i).widget().objectName()
                fa = fn.split('=')
                self.check_array.append(fa[1])
    
        return self.check_array
    
    def tableHeadersSelectorAction(self, state, x):
        '''
        show or hide column from side bar
        '''
        if state:
            self.table.showColumn(x)
        else:
            self.table.hideColumn(x)
        
        
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
        cols = self.classUnitTable
        self.tableHeadersSelector(6,  cols, 'f')
        if hasattr(self, 'hc6_box'):
            self.tableHeadersChecked(self.hc6_box)
            
        if state == 0:
            if hasattr(Window, 'checkBoxStack'):
                self.checkBoxStack.setCurrentIndex(0)
                
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
                self.table.setItem(i, 5, QtGui.QTableWidgetItem(str(total)))
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
            table = '''<style>
                table{
                
                }
                td, th{
                border:1px solid black;
                padding:1px;
                }
               tbody tr:nth-child(odd){
                background-color: #4C8BF5;
               }
            
            </style>
            <div>
            <table width="100% " cellspacing="0" cellpadding="2px"  style="border-width:1px; border-color:#53868b; padding:2px" >
            <thead>
            <tr style="background-color:#53868b0;color:white">
            {%for a in headers %}<th>{{a}}</th>{% endfor %}  
            </tr>
            </thead>
            <tbody>
            {% for row in rows %}
                <tr>
                {% set name = row[2] | title +" "+row[3] | title+" "+row[4] | title %}
                {% set cname = row[32] | upper +" "+row[31]| upper %}
                {% set clga = row[7] | title +"/"+row[8]| title %}
                    <td>{{"1"}}</td>
                    <td>{{row[1] }}</td>
                    <td>{{name}}</td>
                    <td>{{cname}}</td>
                    {% if row[6] == 0 %}
                    <td>{{"Male"}}</td>
                    {% elif row[6] == 1 %}
                    <td>{{"Female"}}</td>
                    {% endif %}
                    <td>{{row[10]  | title}}</td>
                    <td>{{row[9] | title}}</td>
                    <td>{{clga}}</td>
                    <td>{{row[5]}}</td>
                </tr>
            {% endfor %}                     
            </tbody>
            </table>
            </div>'''
               
            
            h = Template(table).render(headers=cols, rows=self.students, confirm = self.check_array)
            return h
    
    def myTableClassUnitFee(self, state, session):       
        #get list of students
        cn = Dat()
        
        data = cn.studentClassUnitFee(session)
        print(data)
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
        self.tableHeadersSelector(6,  cols, 'f')
        if hasattr(self, 'hc6_box'):
            self.tableHeadersChecked(self.hc6_box)
            
        if state == 0:
            if hasattr(Window, 'checkBoxStack'):
                self.checkBoxStack.setCurrentIndex(0)
                
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
            table = '''<style>
                table{
                
                }
                td, th{
                border:1px solid black;
                padding:1px;
                }
               tbody tr:nth-child(odd){
                background-color: #4C8BF5;
               }
            
            </style>
            <div>
            <table width="100% " cellspacing="0" cellpadding="2px"  style="border-width:1px; border-color:#53868b; padding:2px" >
            <thead>
            <tr style="background-color:#53868b0;color:white">
            {%for a in headers %}<th>{{a}}</th>{% endfor %}  
            </tr>
            </thead>
            <tbody>
            {% for row in rows %}
                <tr>
                {% set name = row[2] | title +" "+row[3] | title+" "+row[4] | title %}
                {% set cname = row[32] | upper +" "+row[31]| upper %}
                {% set clga = row[7] | title +"/"+row[8]| title %}
                    <td>{{"1"}}</td>
                    <td>{{row[1] }}</td>
                    <td>{{name}}</td>
                    <td>{{cname}}</td>
                    {% if row[6] == 0 %}
                    <td>{{"Male"}}</td>
                    {% elif row[6] == 1 %}
                    <td>{{"Female"}}</td>
                    {% endif %}
                    <td>{{row[10]  | title}}</td>
                    <td>{{row[9] | title}}</td>
                    <td>{{clga}}</td>
                    <td>{{row[5]}}</td>
                </tr>
            {% endfor %}                     
            </tbody>
            </table>
            </div>'''
               
            
            h = Template(table).render(headers=cols, rows=self.students, confirm = self.check_array)
            return h
          
    def myTable1(self, state, a = []):       
        #get list of students
        
        students = list(set(a))
        self.students = students
        
        #all table headers titles
        cols = self.bioTable
        self.tableHeadersSelector(1,  cols, 'a')
        if hasattr(self, 'hc1_box'):
            self.tableHeadersChecked(self.hc1_box)
            
        if state == 0:
            if hasattr(Window, 'checkBoxStack'):
                self.checkBoxStack.setCurrentIndex(0)
                
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
            for j in students:
                q = list(j)
                #row id
                self.table.setItem(i, 0, QtGui.QTableWidgetItem(str(q[0])))
                #school id
                self.table.setItem(i, 1, QtGui.QTableWidgetItem(str(q[1])))
                #fullname
                fullname= str(q[2])+' '+str(q[3])+' '+str(q[4])
                self.table.setItem(i, 2, QtGui.QTableWidgetItem(str(fullname.title())))
                #classname
                classname= str(q[32])+' '+str(q[31])
                self.table.setItem(i, 3, QtGui.QTableWidgetItem(str(classname.upper())))
                #gender
                if(q[6] == 0):
                    sex = 'Male';
                else:
                    sex = 'Female';
                self.table.setItem(i, 4, QtGui.QTableWidgetItem(str(sex)))
                #date of birth
                self.table.setItem(i, 5, QtGui.QTableWidgetItem(str(q[10]).capitalize()))
                #nationality
                self.table.setItem(i, 6, QtGui.QTableWidgetItem(str(q[9]).capitalize()))
                #State/LGA
                self.table.setItem(i, 7, QtGui.QTableWidgetItem(str(q[7]).capitalize()+'/'+str(q[8]).capitalize()))
                #Address
                self.table.setItem(i, 8, QtGui.QTableWidgetItem(str(q[5])))
                
                i += 1
            # set data
    
            #self.table.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
            return self.table
        #report view
        elif state == 1:
            table = '''<style>
                table{
                
                }
                td, th{
                border:1px solid black;
                padding:1px;
                }
               tbody tr:nth-child(odd){
                background-color: #4C8BF5;
               }
            
            </style>
            <div>
            <table width="100% " cellspacing="0" cellpadding="2px"  style="border-width:1px; border-color:#53868b; padding:2px" >
            <thead>
            <tr style="background-color:#53868b0;color:white">
            {%for a in headers %}<th>{{a}}</th>{% endfor %}  
            </tr>
            </thead>
            <tbody>
            {% for row in rows %}
                <tr>
                {% set name = row[2] | title +" "+row[3] | title+" "+row[4] | title %}
                {% set cname = row[32] | upper +" "+row[31]| upper %}
                {% set clga = row[7] | title +"/"+row[8]| title %}
                    <td>{{"1"}}</td>
                    <td>{{row[1] }}</td>
                    <td>{{name}}</td>
                    <td>{{cname}}</td>
                    {% if row[6] == 0 %}
                    <td>{{"Male"}}</td>
                    {% elif row[6] == 1 %}
                    <td>{{"Female"}}</td>
                    {% endif %}
                    <td>{{row[10]  | title}}</td>
                    <td>{{row[9] | title}}</td>
                    <td>{{clga}}</td>
                    <td>{{row[5]}}</td>
                </tr>
            {% endfor %}                     
            </tbody>
            </table>
            </div>'''
               
            
            h = Template(table).render(headers=cols, rows=self.students, confirm = self.check_array)
            return h
    
    def myTable2(self, state, a = []):
        #get list of students
        students = list(set(a))
        #all table headers titles
        cols = self.conTable
        self.tableHeadersSelector(2,  cols, 'b')
        
        if hasattr(Window, 'checkBoxStack'):
            self.checkBoxStack.setCurrentIndex(1)
            
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
        for j in students:
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
            i += 1
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
    
    def myTable3(self, a = [], b = [], c = [], d = {}):
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
                self.store_sub_name.update({subz:sub_name['abbrv']})
            
        #assessments 
        #get assessments name
        #store in a dictionary
        self.store_ca_name = {}
        for caz in assessments:
            ca_name = None
            ca_names = cn.selectn('datas', '', 1, {'id':caz})
            ca_name = cn.selectn('datas', '', 1, {'id':ca_names['name']})
            if ca_name:
                self.store_ca_name.update({caz:ca_name['abbrv']})
            
        #assements max score
        #get assements maximum scores
        #store them in a dictionary
        self.store_ca_max ={}
        for cazn in assessments:
            ca_name = None
            ca_name = cn.selectn('datas', '', 1, {'id':cazn})
         
            try:
                if ca_name:
                    self.store_ca_max.update({cazn:float(ca_name['abbrv'])})
                else:
                    self.store_ca_max.update({cazn:0})
            except:
                self.store_ca_max.update({cazn:0})
       
    
        #build header columns
        cols = ['id','Sch.No.', 'Fullname', 'Class']
        colsx = ['id','Sch.No.', 'Fullname', 'Class']
        for f in subjects:
                for f1 in assessments:
                    fin_d = self.store_sub_name[f].upper()+'\n'+self.store_ca_name[f1].upper()+' ('+str(self.store_ca_max[f1]).upper()+')'
                    fin_dx = self.store_sub_name[f].upper()+':'+self.store_ca_name[f1].upper()+'('+str(self.store_ca_max[f1]).upper()+')'
                    cols.append(fin_d)
                    colsx.append(fin_dx)
                    
        
        self.tableHeadersSelector(3,  colsx, 'c')
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
        
        #subject header bar
        self.table.setItem(0, 0, QtGui.QTableWidgetItem(str(000)))
        self.table.setItem(0, 1, QtGui.QTableWidgetItem(str(000)))
        self.table.setItem(0, 2, QtGui.QTableWidgetItem(str('aaa')))
        self.table.setItem(0, 3, QtGui.QTableWidgetItem(str('clz')))
        #starting from the fourth column populate subjects
        jx = 4
        for f in subjects:
            for f1 in assessments:
                self.table.setItem(0, jx, QtGui.QTableWidgetItem(str(f)))
                jx += 1
                
        #assessment header bar        
        self.table.setItem(1, 0, QtGui.QTableWidgetItem(str(000)))
        self.table.setItem(1, 1, QtGui.QTableWidgetItem(str(000)))
        self.table.setItem(1, 2, QtGui.QTableWidgetItem(str('aaa')))
        self.table.setItem(1, 3, QtGui.QTableWidgetItem(str('clz')))
        #starting from the fourth column populate subjectsassessments
        jy = 4
        for f in subjects:
            for f1 in assessments:
                self.table.setItem(1, jy, QtGui.QTableWidgetItem(str(f1)))
                jy += 1
        
        i = 2
        for j in students:
            q = list(j)
            self.table.setItem(i, 0, QtGui.QTableWidgetItem(str(q[0])))
            self.table.setItem(i, 1, QtGui.QTableWidgetItem(str(q[1])))
            fullname= q[2]+' '+q[3]
            self.table.setItem(i, 2, QtGui.QTableWidgetItem(str(fullname.title())))
            classname= str(q[32])+' '+str(q[31])
            self.table.setItem(i, 3, QtGui.QTableWidgetItem(str(classname.upper())))
            j = 4
            for f in subjects:
                for f1 in assessments:
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
        self.table.hideRow(0)
        self.table.hideRow(1)
        
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
                    
        
        self.tableHeadersSelector(4,  colsx, 'd')
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
                    
        
        self.tableHeadersSelector(5,  colsx, 'e')
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
        
        try:
            if(int(rw) and int(rw) > 0 and int(cl) and int(cl) > 0):
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
                _subjectID = self.table.item(0, cl).text()
                #get assessement id
                _caID = self.table.item(1, cl).text()
                #get student id
                _studentID = self.table.item(rw, 0).text()
                #use the row id and column id to get value
                value = self.table.item(rw, cl).text()
                #also get the maximum value expected for the cells in that column
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
        students = cn.select('datas', '' , '', {'subID':self.a, 'active':0})
        arr = {}
        
        for j in students:
            arr[j[0]] = j[2]
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
        self.form = Form()
        self.form.show()
    
    def reloadSession(self):
        self.r = self.titleToolbar()
        self.r.hide()
        
    def lunchSessionForm(self):
        form = SessionForm()
        form.show()
        if form.exec_() == QtGui.QDialog.Accepted:
            session = self.activeTerm()
            activeTerm = str(session[1])+' SESSION '+str(session[3])+' TERM'
            self.majorSession = session[2];
            self.lbl.close()
            self.lbl = QtGui.QLabel()
            self.lbl.setText(activeTerm)
        else:
            session = self.activeTerm()
            activeTerm = str(session[1])+' SESSION '+str(session[3])+' TERM'
            self.majorSession = session[2];
            self.lbl.close()
            self.lbl.setText(activeTerm)
        
        
    def lunchCaForm(self):
        self.form = CaForm()
        self.form.show()
        
    def lunchAffectiveForm(self):
        self.form = AffectiveForm()
        self.form.show()
        
    def lunchPsycoForm(self):
        self.form = PsycoForm()
        self.form.show()
        
    def lunchGradeForm(self):
        self.form = GradeForm()
        self.form.show()
        
    def lunchExpenseForm(self):
        self.form = ExpenseForm()
        self.form.show()
        
    def lunchSubjectForm(self):
        self.form = SubjectForm()
        self.form.show()
        
    def lunchFeeForm(self):
        self.form = FeeForm()
        self.form.show()
        
    def lunchClassTable(self, a, b):
        ar = []
        ar.append(a)
        self.form = StudentTable(b, [None], ar, [None] )
        p = self.form.classStudent()
        q = self.form.className(ar)
        self.tabl.close()
        self.stackRightBar.setCurrentIndex(0)
        self.stackLeftBar.setCurrentIndex(0)
        self.tabl = self.myTable1(0, p)
        self.tabletitle.setText(q)
        self.hbox2.addWidget(self.tabl)
        self.tabl.show()
    
    
    def lunchClassUnitTable(self, a, b):
        ar = []
        ar.append(a)
        self.form = StudentTable(b, [None], [None],  ar)
        p = self.form.classUnitStudent()
        q = self.form.className(ar)
        try:
            self.tabl.close()
            self.stackRightBar.setCurrentIndex(0)
            self.stackLeftBar.setCurrentIndex(0)
            self.tabl = self.myTable1(0, p)
            self.tabletitle.setText(q)
            self.hbox2.addWidget(self.tabl)
            self.tabl.show()
        except:
            pass
        
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
    
    def lunchPrintTable(self):
        self.pageDisplay()
        #post = PrintTable(self.tabl)
        #post.show()
        #if post.exec_() == QtGui.QDialog.Accepted:
               #rtt = post.getValue()
    
        #return rtt
    def lunchFeeDialog(self, sid):
        post = TermFeeDialog(sid)
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
                
            
        if(rtt[2] == 0):
            rtt1 = self.getStudentAssessments(_session, student_id, rtt[0], rtt[1])
            _arr = {}
            for g in rtt1:
                st = 'AB'+str(g['studentID'])+'CD'+str(g['subjectID'])+'EF'+str(g['caID'])
                _arr.update({st:g['score']})
                            
            self.tabl.close()    
            self.tabl = self.myTable3(studentsIDs,  rtt[0], rtt[1], _arr )
            self.stackRightBar.setCurrentIndex(0)
            self.stackLeftBar.setCurrentIndex(0)
            self.hbox2.addWidget(self.tabl)
            self.tabl.show()
                
        elif(rtt[2] == 1):
            seperator = ','
            _B = seperator.join(str(x) for x in student_id) 
            _C = seperator.join(str(x) for x in rtt[0]) 
            _D = seperator.join(str(x) for x in rtt[1])
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
    import sys
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
