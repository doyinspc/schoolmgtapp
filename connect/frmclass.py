# -*- coding: utf-8 -*-
"""
Created on Sat Jul  7 15:54:19 2018

@author: CHARLES
"""
from PyQt4.QtCore import SIGNAL
from PyQt4.QtGui import QWidget, QCheckBox, QHBoxLayout, QGroupBox, QGridLayout, QDialog, QApplication, QPushButton, QLineEdit, QFormLayout, QLabel, QVBoxLayout
from connect import Db
from unitfrm import UnitForm

class Form(QDialog):
    
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        
        ko = 0
        layout1 = QGridLayout()
        arr = self.pullClass(1)
        hold ={}
        for val in arr:
            self.num = val
            self.c = QCheckBox('cb'+str(val))
            self.c.setText(arr[val][0])
            self.c.setObjectName("chk"+str(val))
            if (arr[val][1] == 1):
                self.c.setChecked(False)
            else:
               self.c.setChecked(True)
            
            self.c.stateChanged.connect(lambda state, x=val, y=self.c: self.chkFunc(x, y))
            self.b = QPushButton()
            self.b.setObjectName("btn"+str(val))
            self.b.setText('Subunit')
            self.b1 = QPushButton()
            self.b1.setObjectName("btn1"+str(val))
            self.b1.setText('Edit')
            hold["btn"+str(val)] = self.b
            hold["btnx"+str(val)] = self.b1
            layout1.addWidget(self.c, ko, 0)
            layout1.addWidget(self.b, ko, 1)
            layout1.addWidget(self.b1, ko, 2)
            ko += 1
            
      
        for j in arr:
            self.h = j
            b = "btn"+str(j)
            b1 = "btnx"+str(j)
            self.connect(hold[b], SIGNAL("clicked()"), lambda gh=j: self.lunchUnitForm(gh))
            self.connect(hold[b1], SIGNAL("clicked()"), lambda gh=j: self.lunchEditForm(gh))
            
        groupBox1 = QGroupBox('All Classes')
        groupBox1.setLayout(layout1)
        
        self.pb = QPushButton()
        self.pb.setObjectName("Add")
        self.pb.setText("Add Class")
        
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
        adF = AddForm()
        self.connect(self.pb, SIGNAL("clicked()"), lambda: adF.show())
        self.connect(self.pb1, SIGNAL("clicked()"), self.close)
        self.setWindowTitle("Class Manager")

    def button_click(self, a):
        # shost is a QString object
        s1 = self.le.text()
        s2 = self.le2.text()
        self.a = a
        g = Db()
        if(len(s1) > 0):
            y = { 'name':s1, 'subID': self.a, 'abbrv':s2}
            return  g.insert('datas', y)
        
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
        
    def chkFunc(self, a, b):
        # shost is a QString object
        self.a = a
        self.b = b
        
         
        if b.isChecked() == True:
            y = { 'active':0}
        else:
            y = { 'active':1}
         
        g = Db()
        z = {'id': self.a}
        j = g.update('datas', y, z)
       
        return j 
        
    def pullClass(self, a):
        self.a = a
        cn = Db()
        students = cn.select('datas', '' , '', {'subID':self.a})
        arr = {}
        
        for j in students:
            arr[j[0]] =[j[2], j[4], j[0]]
        return arr
    
    def lunchUnitForm(self, a):
        self.a = a
        self.form = UnitForm(self.a)
        self.form.show()
        #form.exec_()
    
    def lunchEditForm(self, a):
        self.a = a
        self.form = EditForm(self.a)
        self.form.show()
        #form.exec_()
        
    
class AddForm(QDialog):    
    def __init__(self, parent=None):
        super(AddForm, self).__init__(parent)
        
        self.l1 = QLabel("Name")
        self.le = QLineEdit()
        self.le.setObjectName("host")
        self.le.setText("")
        
        self.l2 = QLabel("Abbrv.")
        self.le2 = QLineEdit()
        self.le2.setObjectName("Abbrv.")
        self.le2.setText("")

        self.pb = QPushButton()
        self.pb.setObjectName("Submit")
        self.pb.setText("Submit")
        
        self.pb1 = QPushButton()
        self.pb1.setObjectName("Cancel")
        self.pb1.setText("Cancel")
        
        layout = QFormLayout()
        layout.addRow(self.l1, self.le)
        layout.addRow(self.l2, self.le2)
        layout.addRow(self.pb1, self.pb)
        
        
        groupBox = QGroupBox('Add Class')
        groupBox.setLayout(layout)
        
        
        grid = QGridLayout()
        grid.addWidget(groupBox, 0, 0)
        self.setLayout(grid)
        self.connect(self.pb, SIGNAL("clicked()"), lambda: self.button_click(1))
        
        self.repaint()
            
        self.connect(self.pb1, SIGNAL("clicked()"), self.close)
        self.setWindowTitle("Class Manager")
        
    def button_click(self, a):
        # shost is a QString object
        s1 = self.le.text()
        s2 = self.le2.text()
        self.a = a
        g = Db()
        if(len(s1) > 0):
            y = { 'name':s1, 'subID': self.a, 'abbrv':s2}
            return  g.insert('datas', y)
        

class EditForm(QDialog): 
    
    def __init__(self, sid, parent=None):
        super(EditForm, self).__init__(parent)
        self.sid = sid
        data = self.callData(self.sid)
        
        self.l1 = QLabel("Name")
        self.le = QLineEdit()
        self.le.setObjectName("host")
        self.le.setText(data[2])
        
        self.l2 = QLabel("Abbrv.")
        self.le2 = QLineEdit()
        self.le2.setObjectName("Abbrv.")
        self.le2.setText(data[3])

        self.pb = QPushButton()
        self.pb.setObjectName("Submit")
        self.pb.setText("Submit")
        
        self.pb1 = QPushButton()
        self.pb1.setObjectName("Cancel")
        self.pb1.setText("Cancel")
        
        layout = QFormLayout()
        layout.addRow(self.l1, self.le)
        layout.addRow(self.l2, self.le2)
        layout.addRow(self.pb1, self.pb)
        
        
        groupBox = QGroupBox('Edit Class')
        groupBox.setLayout(layout)
        
        
        grid = QGridLayout()
        grid.addWidget(groupBox, 0, 0)
        self.setLayout(grid)
        self.connect(self.pb, SIGNAL("clicked()"), lambda: self.button_click(data[0]))
        self.connect(self.pb1, SIGNAL("clicked()"), self.close)
        self.setWindowTitle("Class Manager")
        
    def button_click(self, a):
        # shost is a QString object
        s1 = self.le.text()
        s2 = self.le2.text()
        self.a = a
        g = Db()
        if(len(s1) > 0):
            y = { 'name':s1, 'abbrv':s2}
            z = {'id':self.a}
            return  g.update('datas', y, z)

    def callData(self, a):
        # select a file
        self.a = a
        g = Db()
        return  g.select('datas', '', 1, {'id':self.a})