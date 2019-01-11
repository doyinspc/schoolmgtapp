# -*- coding: utf-8 -*-
"""
Created on Fri Jul 13 15:22:52 2018

@author: CHARLES
"""
from PyQt4.QtCore import SIGNAL, QDate
from PyQt4.QtGui import QWidget, QDateEdit, QRadioButton, QCheckBox, QHBoxLayout, QGroupBox, QGridLayout, QDialog, QApplication, QPushButton, QLineEdit, QFormLayout, QLabel, QVBoxLayout
from connect import Db

class CompForm(QDialog):
    
    def __init__(self, sid, parent=None):
        super(CompForm, self).__init__(parent)
        self.sid = sid
        ko = 0
        layout1 = QGridLayout()
        try: 
            details = self.pullDetails(self.sid)
            pagetitle = str(details[1]) +' ' 
        except:
            details = []
            pagetitle = 'None'
        
        arr = self.pullClass(self.sid)
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
            self.d.setText(arr[val][1] + ' - '+ arr[val][2])
            self.b = QPushButton()
            self.b.setObjectName("btn"+str(val))
            self.b.setText('Terms')
            self.b1 = QPushButton()
            self.b1.setObjectName("btn1"+str(val))
            self.b1.setText('Edit')
            hold["btn"+str(val)] = self.b
            layout1.addWidget(self.c, ko, 0)
            layout1.addWidget(self.d, ko, 1)
            layout1.addWidget(self.b, ko, 2)
            ko += 1
            
      
        for j in arr:
            self.h = j
            b = "btn"+str(j)
            self.connect(hold[b], SIGNAL("clicked()"), lambda gh=j: self.lunchEditForm(gh, self))
            
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
        self.connect(self.pb, SIGNAL("clicked()"), lambda: self.lunchAddForm(self.sid, self))
        self.connect(self.pb1, SIGNAL("clicked()"), lambda: self.button_close(self))
        self.setWindowTitle(pagetitle)

        
    def chkFunc(self, a, b):
        # shost is a QString object
        self.a = a
        self.b = b
        g = Db()
        g.update('datas', {'active':1}, {'active':0})
        
        if b.isChecked() == True:
            y = { 'active':0}
        else:
            y = { 'active':1}
         
        
        z = {'id': self.a}
        j = g.update('datas', y, z)
       
        return j 
        
    def pullClass(self, a):
        self.a = a
        cn = Db()
        cn.createData()
        datas = cn.select('datas', '' , '', {'subID':self.a})
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
        datas = cn.select('datas', '' , 1, {'id':self.a})
        
        return datas
    
    def lunchEditForm(self, a, b):
        b.close()
        self.a = a
        self.form = EditForm(self.a)
        self.form.show()
        
    def lunchAddForm(self, a, b):
        b.close()
        self.a = a 
        self.form = AddForm(self.a)
        self.form.show()
        
    def lunchForm(self):
        self.form = super.SubjectForm()
        self.form.show()
    
    def button_close(self, a):
        a.close()
        from frmsubject import SubjectForm
        self.form = SubjectForm()
        self.form.show()
        
    
class AddForm(QDialog):    
    def __init__(self, sid,  parent=None):
        super(AddForm, self).__init__(parent)
        self.sid = sid
        try: 
            details = self.pullDetails(self.sid)
            pagetitle = str(details[1]) +' Session' 
        except:
            details = []
            pagetitle = 'None'
        
        self.l1 = QLabel("Name")
        self.le = QLineEdit()
        self.le.setObjectName("name")
        self.le.setText("")
        
        self.pb = QPushButton()
        self.pb.setObjectName("Submit")
        self.pb.setText("Submit")
        
        self.pb1 = QPushButton()
        self.pb1.setObjectName("Cancel")
        self.pb1.setText("Cancel")
        
        layout = QFormLayout()
        layout.addRow(self.l1, self.le)
        layout.addRow(self.pb1, self.pb)
        
        
        groupBox = QGroupBox('Add New Term')
        groupBox.setLayout(layout)
        
        
        grid = QGridLayout()
        grid.addWidget(groupBox, 0, 0)
        self.setLayout(grid)
        self.connect(self.pb, SIGNAL("clicked()"), lambda: self.button_click(self.sid, self))
        self.connect(self.pb1, SIGNAL("clicked()"), lambda: self.button_close(self.sid, self))
        self.setWindowTitle(pagetitle)
        
    def button_click(self, a, b):
        # shost is a QString object
        b.close()
        self.a = a
        s1 = self.le.text()
        g = Db()
        try:
            if(len(s1) > 0):
                y = { 'name':s1, 'sessionID':self.a,  'start_date':s2, 'end_date':s3, 'active':0}
                z = g.insert('terms', y)
                
                if z and z > 0:
                    g.createClass(z)
                    g.createFee(z)
                    g.createResult(z)   
            else:
                pass
        except:
            pass
        
        try:
            self.lunchForm(self.a)
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
    
    def button_close(self, a, b):
        b.close()
        self.a = a
        self.lunchForm(self.a)
        

class EditForm(QDialog): 
    
    def __init__(self, sid, parent=None):
        super(EditForm, self).__init__(parent)
        self.sid = sid
        data = self.callData(self.sid)
        
        
        try: 
            details = self.pullDetails(data[1])
            pagetitle = str(details[2]) +' Session' 
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
        self.connect(self.pb, SIGNAL("clicked()"), lambda: self.button_click(data[0], self))
        self.connect(self.pb1, SIGNAL("clicked()"),lambda: self.button_close(self))
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
        
        self.form = TermForm(self.a)
        self.form.show()
        self.close()
        #self.lunchForm()
        
    def lunchForm(self, a):
        self.a = a
        self.form = TermForm(self.a)
        self.form.show()
        
    def button_close(self, a, b):
        b.close()
        self.a = a
        self.lunchForm(self.a)
        
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