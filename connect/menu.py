# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
from PyQt4 import QtCore, QtGui
from connect import Db
from frm import Form


class Menu(QtGui.QMainWindow):
    
    
    def __init__(self, ):
        super(Menu, self).__init__() 
        itz = self.pullClass(1)
        extractQuit = QtGui.QAction(self) 
        extractQuit.setStatusTip('File')
        #extractQuit.triggered.connect(self.pullClass)
          
        self.statusBar()
        
        mainMenu = self.menuBar()
        
        fileMenu = mainMenu.addMenu('&File')
        exitMenu = QtGui.QAction('&Exit', self)
        exitMenu.setShortcut('CTRL+Q')
        exitMenu.setStatusTip('Close Application')
        exitMenu.triggered.connect(self.lunchForm)
        fileMenu.addAction(exitMenu)
        
        #Session menu
        sessionMenu = mainMenu.addMenu('&Session')
       
        
        for k in itz:
           act = '&'+str(itz[k])
           at = sessionMenu.addMenu(act)
           QtCore.QObject.connect(at, QtCore.SIGNAL("clicked()"), lambda: self.lunchForm)

        
        #student menu
        studentMenu = mainMenu.addMenu('&Student')
        ## student menu static items
        studentAllMenu = QtGui.QAction('&All Students', self)
        studentAllMenu.setShortcut('CTRL+P+A')
        studentAllMenu.setStatusTip('All Students')
        studentAllMenu.triggered.connect(self.lunchForm)
        
        studentExMenu = QtGui.QAction('&Ex. Students', self)
        studentExMenu.setShortcut('CTRL+E')
        studentExMenu.setStatusTip('All Students')
        studentExMenu.triggered.connect(self.lunchForm)
        
        studentCrMenu = QtGui.QAction('&Current Students', self)
        studentCrMenu.setShortcut('CTRL+C')
        studentCrMenu.setStatusTip('Current Students')
        studentCrMenu.triggered.connect(self.lunchForm)
        
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
           stud.triggered.connect(self.lunchForm)
           studentMenu.addAction(stud)
           
        studentMenu.addSeparator()
           
        for k in itz:
           act = '&'+str(itz[k])
           stud = studentMenu.addMenu(act)

           arr = self.pullClass(k)
           for j in arr:
               act1 = '&'+str(arr[j])
               st = QtGui.QAction(act1, self)
               st.triggered.connect(self.lunchForm)
               stud.addAction(st)

           
        staffMenu = mainMenu.addMenu('&Staff')
        staffMenu.addAction(extractQuit)
        

        #settings menu
        settingMenu = mainMenu.addMenu('&Settings')
        ## student menu static items
        classMenu = QtGui.QAction('&Class Manager', self)
        classMenu.setStatusTip('Manage Class settings')
        classMenu.triggered.connect(self.lunchForm)
        
        gradeMenu = QtGui.QAction('&Grades Manager', self)
        gradeMenu.setStatusTip('All Students')
        gradeMenu.triggered.connect(self.lunchForm)
        
        feeMenu = QtGui.QAction('&Fee Manager', self)
        feeMenu.setStatusTip('Current Students')
        feeMenu.triggered.connect(self.lunchForm)
        
        settingMenu.addAction(classMenu)
        settingMenu.addAction(gradeMenu)
        settingMenu.addAction(feeMenu)
        
        
    def pullClass(self, a):
        self.a = a
        cn = Db()
        students = cn.select('datas', '' , '', {'subID':self.a})
        arr = {}
        
        for j in students:
            arr[j[0]] = j[2]
        return arr
     
    def lunchForm(self):
        self.form = Form()
        self.form.show()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
        




