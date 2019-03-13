# -*- coding: utf-8 -*-
"""
Created on Sat Jul  7 15:54:19 2018

@author: CHARLES
"""
from PyQt4.QtCore import SIGNAL, QDate
from PyQt4.QtGui import QWidget, QDateEdit, QRadioButton, QCheckBox, QHBoxLayout, QGroupBox, QGridLayout, QDialog, QApplication, QPushButton, QLineEdit, QFormLayout, QLabel, QVBoxLayout
from connect import Db
from frmsessionterm import TermForm
import datetime

class SessionForm(QDialog):
    pagetitle = 'Session Manager'
    def __init__(self, parent=None):
        super(SessionForm, self).__init__(parent)
        
        ko = 0
        layout1 = QGridLayout()
        arr = self.pullClass()
        hold ={}
        for val in arr:
            self.num = val
            self.c = QRadioButton('cb'+str(val))
            self.c.setText(str(arr[val][0]))
            self.c.setObjectName("chk"+str(val))
            if (arr[val][3] == 1):
                self.c.setChecked(True)
            else:
               self.c.setChecked(False)
            
            self.c.toggled.connect(lambda state, x=val, y=self.c: self.chkFunc(x, y))
            self.d = QLabel()
            sd = datetime.datetime.strptime(arr[val][1], '%Y-%m-%d').date()
            ed = datetime.datetime.strptime(arr[val][2], '%Y-%m-%d').date()
            sd = "{:%d, %b %Y}".format(sd)
            ed = "{:%d, %b %Y}".format(ed)
            self.d.setText(sd + ' - '+ ed)
            
            self.b = QPushButton()
            self.b.setObjectName("btn"+str(val))
            self.b.setText('Terms')
            self.b1 = QPushButton()
            self.b1.setObjectName("btn1"+str(val))
            self.b1.setText('Edit')
            hold["btn"+str(val)] = self.b
            hold["btnx"+str(val)] = self.b1
            layout1.addWidget(self.c, ko, 0)
            layout1.addWidget(self.d, ko, 1)
            layout1.addWidget(self.b, ko, 2)
            layout1.addWidget(self.b1, ko, 3)
            ko += 1
            
      
        for j in arr:
            self.h = j
            b = "btn"+str(j)
            b1 = "btnx"+str(j)
            self.connect(hold[b], SIGNAL("clicked()"), lambda gh=j: self.lunchUnitForm(gh, self))
            self.connect(hold[b1], SIGNAL("clicked()"), lambda gh=j: self.lunchEditForm(gh, self))
            
        groupBox1 = QGroupBox('All Sessions')
        groupBox1.setLayout(layout1)
        
        self.pb = QPushButton()
        self.pb.setObjectName("Add")
        self.pb.setText("Add Session")
        
        self.pb1 = QPushButton()
        self.pb1.setObjectName("Cancel")
        self.pb1.setText("Cancel")
        
        hbo = QHBoxLayout()
        hbo.addWidget(self.pb1)
        hbo.addStretch()
        hbo.addWidget(self.pb)
        groupBox2 = QGroupBox('')
        groupBox2.setLayout(hbo)
        
        grid = QGridLayout()
        grid.addWidget(groupBox1, 0, 0)
        grid.addWidget(groupBox2, 1, 0)
        
        self.setLayout(grid)
        self.connect(self.pb, SIGNAL("clicked()"), lambda: self.lunchAddForm(self))
        self.connect(self.pb1, SIGNAL("clicked()"), lambda: self.button_close())
        self.setWindowTitle(self.pagetitle)

        
    def chkFunc(self, a, b):
        # shost is a QString object
        self.a = a
        self.b = b
        g = Db()
        g.update('session', { 'active':0}, { 'active':1})
        
        if b.isChecked() == True:
            y = { 'active':1}
        else:
            y = { 'active':0}
         
        
        z = {'id': self.a}
        j = g.update('session', y, z)
       
        return j 
        
    def pullClass(self):
        cn = Db()
        students = cn.select('session', '' , '')
        arr = {}
        
        try:
            for j in students:
                arr[j[0]] =[j[1], j[2], j[3], j[4]]
        except:
            pass
        return arr
    
    def lunchUnitForm(self, a, b):
        b.close()
        self.a = a
        form = TermForm(self.a)
        form.show()
        if form.exec_() == QDialog.Accepted:
               rtt = form.getValue()
    
    def lunchEditForm(self, a, b):
        b.close()
        self.a = a
        self.form = EditForm(self.a)
        self.form.show()
        
    def lunchAddForm(self, a):
        a.close()
        self.form = AddForm()
        self.form.show()
        
    def lunchForm(self):
        self.__init__()
        self.reloadSession()
    
    def button_close(self):
        self.close()
        #self.lunchForm()
        
    
class AddForm(QDialog):    
    def __init__(self, parent=None):
        super(AddForm, self).__init__(parent)
        
        self.l1 = QLabel("Name")
        self.le = QLineEdit()
        self.le.setObjectName("name")
        self.le.setText("")
        
        self.l2 = QLabel("Start Date")
        self.le2 = QDateEdit()
        self.le2.setObjectName("startdate")
        self.le2.setCalendarPopup(True)
        
        self.l3 = QLabel("End Date")
        self.le3 = QDateEdit()
        self.le3.setObjectName("enddate")
        self.le3.setCalendarPopup(True)

        self.pb = QPushButton()
        self.pb.setObjectName("Submit")
        self.pb.setText("Submit")
        
        self.pb1 = QPushButton()
        self.pb1.setObjectName("Cancel")
        self.pb1.setText("Cancel")
        
        layout = QFormLayout()
        layout.addRow(self.l1, self.le)
        layout.addRow(self.l2, self.le2)
        layout.addRow(self.l3, self.le3)
        layout.addRow(self.pb1, self.pb)
        
        
        groupBox = QGroupBox('Add Session')
        groupBox.setLayout(layout)
        
        
        grid = QGridLayout()
        grid.addWidget(groupBox, 0, 0)
        self.setLayout(grid)
        self.connect(self.pb, SIGNAL("clicked()"), lambda: self.button_click(self))
        self.connect(self.pb1, SIGNAL("clicked()"), lambda: self.button_close(self))
        self.setWindowTitle("Session Manager")
        
    def button_click(self, a):
        # shost is a QString object
        a.close()
        s1 = self.le.text()
        s2 = self.le2.date().toPyDate()
        s3 = self.le3.date().toPyDate()
        g = Db()
        try:
            if(len(s1) > 0):
                y = { 'name':s1, 'start_date':s2, 'end_date':s3, 'active':0}
                z = g.insert('session', y)
                if z and z > 0:
                    g.createExpenses(z)
                    g.createStores(z)
                    g.createAwards(z)
                    g.createConducts(z)
                    g.createMails(z)
                    g.createMedicals(z)
            else:
                pass
        except:
            pass
        
        try:
            self.button_close()
        except:
            pass
        try:
            self.close()
        except:
            pass
        
        
        
    def lunchForm(self):
        self.form = SessionForm()
        self.form.show()
    
    def button_close(self,a):
        a.close()
        #self.lunchForm()
        

class EditForm(QDialog): 
    
    def __init__(self, sid, parent=None):
        super(EditForm, self).__init__(parent)
        self.sid = sid
        data = self.callData(self.sid)
        
        self.l1 = QLabel("Name")
        self.le = QLineEdit()
        self.le.setObjectName("name")
        self.le.setText(str(data[1]))
        
        self.l2 = QLabel("Start Date")
        self.le2 = QDateEdit()
        self.le2.setObjectName("startdate")
        #self.le2.setDate(data[2])
        
        self.l3 = QLabel("End Date")
        self.le3 = QDateEdit()
        self.le3.setObjectName("enddate")
        #self.le3.setDate(data[3])

        self.pb = QPushButton()
        self.pb.setObjectName("Submit")
        self.pb.setText("Submit")
        
        self.pb1 = QPushButton()
        self.pb1.setObjectName("Cancel")
        self.pb1.setText("Cancel")
        
        layout = QFormLayout()
        layout.addRow(self.l1, self.le)
        layout.addRow(self.l2, self.le2)
        layout.addRow(self.l3, self.le3)
        layout.addRow(self.pb1, self.pb)
        
        groupBox = QGroupBox('Edit Session')
        groupBox.setLayout(layout)
        
        grid = QGridLayout()
        grid.addWidget(groupBox, 0, 0)
        self.setLayout(grid)
        self.connect(self.pb, SIGNAL("clicked()"), lambda: self.button_click(data[0], self))
        self.connect(self.pb1, SIGNAL("clicked()"),lambda: self.button_close(self))
        self.setWindowTitle("Session Manager")
        
    def button_click(self, a, b):
        # shost is a QString object
        b.close()
        s1 = self.le.text()
        s2 = self.le2.date().toPyDate()
        s3 = self.le3.date().toPyDate()
        self.a = a
        g = Db()
        if(len(s1) > 0):
            y = { 'name':s1, 'start_date':s2, 'end_date':s3}
            z = {'id':self.a}
            g.update('session', y, z)
            if z and z > 0:
                g.createExpenses(self.a)
                g.createStores(self.a)
                g.createAwards(self.a)
                g.createConducts(self.a)
                g.createMails(self.a)
                g.createMedicals(self.a)
        
        self.form = SessionForm()
        self.form.show()
        self.close()
        #self.lunchForm()
        
    def lunchForm(self):
        self.form = SessionForm()
        self.form.show()
        
    def button_close(self, a):
        a.close()
        self.lunchForm()

    def callData(self, a):
        # select a file
        self.a = a
        g = Db()
        return  g.select('session', '', 1, {'id':self.a})