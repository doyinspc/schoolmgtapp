# -*- coding: utf-8 -*-
"""
Created on Fri Jul 13 15:22:52 2018

@author: CHARLES
"""
from PyQt4.QtCore import SIGNAL, QDate
from PyQt4.QtGui import QWidget, QDateEdit, QRadioButton, QCheckBox, QHBoxLayout, QGroupBox, QGridLayout, QDialog, QApplication, QPushButton, QLineEdit, QFormLayout, QLabel, QVBoxLayout
from connect import Db
import datetime
from dialogtermca import TermCaDialog
from dialogtermfee import TermFeeDialog

class TermForm(QDialog):
    
    def __init__(self, sid, parent=None):
        super(TermForm, self).__init__(parent)
        self.sid = sid
        ko = 0
        layout1 = QGridLayout()
        try: 
            details = self.pullDetails(self.sid)
            self.session = details[1]
            pagetitle = str(details[1]) +' Sessions'
            self.title = str(details[1]) 
        except:
            details = []
            pagetitle = 'None'
        
        self.pagetitle = pagetitle
        arr = self.pullClass(self.sid)
        arrkeys = arr.keys()
        arrkeys.sort()
        hold ={}
        for val in arrkeys:
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
            self.b.setText('CA')
            self.b1 = QPushButton()
            self.b1.setObjectName("btn1"+str(val))
            self.b1.setText('Edit')
            self.b2 = QPushButton()
            self.b2.setObjectName("btn2"+str(val))
            self.b2.setText('Fee')
            hold["btn"+str(val)] = self.b
            hold["btn1"+str(val)] = self.b1
            hold["btn2"+str(val)] = self.b2
            layout1.addWidget(self.c, ko, 0)
            layout1.addWidget(self.d, ko, 1)
            layout1.addWidget(self.b, ko, 2)
            layout1.addWidget(self.b1, ko, 3)
            layout1.addWidget(self.b2, ko, 4)
            ko += 1
            
      
        for j in arr:
            self.h = j
            b = "btn"+str(j)
            b1 = "btn1"+str(j)
            b2 = "btn2"+str(j)
            self.connect(hold[b], SIGNAL("clicked()"), lambda gh=j: self.lunchCa(gh, self))
            self.connect(hold[b1], SIGNAL("clicked()"), lambda gh=j: self.lunchEditForm(gh, self))
            self.connect(hold[b2], SIGNAL("clicked()"), lambda gh=j: self.lunchFeeForm(gh, self))
            
        groupBox1 = QGroupBox('All Terms')
        groupBox1.setLayout(layout1)
        
        self.pb = QPushButton()
        self.pb.setObjectName("Add")
        self.pb.setText("Add Term")
        
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
        self.connect(self.pb, SIGNAL("clicked()"), lambda  a=self.sid: self.lunchAddForm(self, a))
        self.connect(self.pb1, SIGNAL("clicked()"), lambda: self.button_close(self))
        self.setWindowTitle(pagetitle)

        
    def chkFunc(self, a, b):
        # shost is a QString object
        self.a = a
        self.b = b
        g = Db()
        g.update('terms', { 'active':0}, { 'active':1})
        
        if b.isChecked() == True:
            y = { 'active':1}
        else:
            y = { 'active':0}
         
        
        z = {'id': self.a}
        j = g.update('terms', y, z)
        g.update('session', { 'active':0}, { 'active':1})
        k = g.select('terms', '', 1, z)
        g.update('session', { 'active':1} ,{'id':k[2]})
       
        return j 
        
    def pullClass(self, a):
        self.a = a
        cn = Db()
        cn.createData()
        datas = cn.select('terms', '' , '', {'sessionID':self.a})
        arr = {}
        
        try:
            for j in datas:
                arr[j[0]] =[j[1], j[3], j[4], j[5]]
        except:
            pass
        return arr
    
    def pullDetails(self, a):
        self.a = a
        cn = Db()
        datas = cn.select('session', '' , 1, {'id':self.a})
        return datas
    
    def lunchEditForm(self, a, b):
        b.close()
        self.a = a
        self.form = EditForm(self.a, self.pagetitle, self.sid)
        self.form.show()
        
    def lunchFeeForm(self, a, b):
        b.close()
        self.a = a
        self.form = TermFeeDialog(self.a, self.pagetitle, self.sid)
        self.form.show()
        
    def lunchAddForm(self, b,  a):
        b.close()
        self.a = a 
        self.form = AddForm(self.a, self.pagetitle, self.sid)
        self.form.show()
        
    def lunchForm(self):
        self.form = super.SessionForm()
        self.form.show()
        
    def lunchCa(self, a, b):
        b.close()
        self.post = TermCaDialog(a, self.title)
        self.post.show()
    
    def button_close(self, a):
        a.close()
        from frmsession import SessionForm
        self.form = SessionForm()
        self.form.show()
        
    
class AddForm(QDialog):    
    def __init__(self, sid, pagetitle, session,  parent=None):
        super(AddForm, self).__init__(parent)
        self.sid = sid
        self.session = session
        try: 
            details = self.pullDetails(self.sid)
            pagetitle = pagetitle
        except:
            details = []
            pagetitle = 'None'
        
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
        
        
        groupBox = QGroupBox('Add New Term')
        groupBox.setLayout(layout)
        
        
        grid = QGridLayout()
        grid.addWidget(groupBox, 0, 0)
        self.setLayout(grid)
        self.connect(self.pb, SIGNAL("clicked()"), lambda: self.button_click(self.sid, self))
        self.connect(self.pb1, SIGNAL("clicked()"), lambda: self.button_close())
        self.setWindowTitle(pagetitle)
        
    def button_click(self, a, b):
        # shost is a QString object
        b.close()
        self.a = a
        s1 = self.le.text()
        s2 = self.le2.date().toPyDate()
        s3 = self.le3.date().toPyDate()
        g = Db()
        try:
            if(len(s1) > 0):
                y = { 'name':s1, 'sessionID':self.a,  'start_date':s2, 'end_date':s3, 'active':0}
                z = g.insert('terms', y)
                
                if z and z > 0:
                    g.createClass(z)
                    g.createFee(z)
                    g.createResult(z)  
                    g.createAffective(z)
                    g.createPsychomoto(z)
            else:
                pass
        except:
            pass
        
        try:
            self.lunchForm(self.session)
        except:
            pass
        try:
            self.close()
        except:
            pass
        
    def pullDetails(self, a):
        self.a = a
        cn = Db()
        datas = cn.select('session', '' , 1, {'id':self.a})
        return datas    
        
    def lunchForm(self, a):
        self.a = a
        self.form = TermForm(self.a)
        self.form.show()
        
            
    def button_close(self):
        self.close()
        self.lunchForm(self.session)
        

class EditForm(QDialog): 
    
    def __init__(self, sid, pagetitle, session, parent=None):
        super(EditForm, self).__init__(parent)
        self.sid = sid
        data = self.callData(self.sid)
        self.session = session
        self.pagetitle = pagetitle
         
        try: 
            details = self.pullDetails(term)
            pagetitle = pagetitle
        except:
            details = []
            pagetitle = 'None'
        
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
        self.connect(self.pb, SIGNAL("clicked()"), lambda x = data[0] : self.button_click(x, self))
        self.connect(self.pb1, SIGNAL("clicked()"),self.button_close)
        self.setWindowTitle(pagetitle)
        
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
            g.update('terms', y, z)
            if self.a and self.a > 0:
                    g.createClass(self.a)
                    g.createFee(self.a)
                    g.createResult(self.a) 
                    g.createAffective(self.a)
                    g.createPsychomoto(self.a)
        
        self.form = TermForm(self.session)
        self.form.show()
        self.close()
        #self.lunchForm()
        
    def lunchForm(self, a):
        self.a = a
        self.form = TermForm(self.session)
        self.form.show()
        
    def button_close(self):
        self.lunchForm(self.session)
        
    def pullDetails(self, a):
        self.a = a
        cn = Db()
        datas = cn.select('session', '' , 1, {'id':self.a})
        
        return datas

    def callData(self, a):
        # select a file
        self.a = a
        g = Db()
        return  g.select('terms', '', 1, {'id':self.a})