# -*- coding: utf-8 -*-
"""
Created on Sat Jul  7 15:54:19 2018

@author: CHARLES
"""
from PyQt4.QtCore import SIGNAL, QDate
from PyQt4.QtGui import QWidget, QDateEdit, QRadioButton, QCheckBox, QHBoxLayout, QGroupBox, QGridLayout, QDialog, QApplication, QPushButton, QLineEdit, QFormLayout, QLabel, QVBoxLayout
from connect import Db
from frmstoretype import StoreTypeForm

class StoreForm(QDialog):
    pagetitle = 'Store Manager'
    def __init__(self, parent=None):
        super(StoreForm, self).__init__(parent)
        
        ko = 0
        layout1 = QGridLayout()
        arr = self.pullClass()
        
        hold ={}
        for val in arr:
            self.num = arr[val][0]
            self.d = QLabel()
            self.d.setText(str(arr[val][1]).upper())
            self.b = QPushButton()
            self.b.setObjectName("btn"+str(val))
            self.b.setText('Types')
            self.b1 = QPushButton()
            self.b1.setObjectName("btn1"+str(val))
            self.b1.setText('Edit')
            hold["btn"+str(val)] = self.b
            hold["btnx"+str(val)] = self.b1
            #layout1.addWidget(self.c, ko, 0)
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
            
        groupBox1 = QGroupBox('Categories')
        groupBox1.setLayout(layout1)
        
        self.pb = QPushButton()
        self.pb.setObjectName("Add")
        self.pb.setText("Add Category")
        
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
        
        if b.isChecked() == True:
            y = { 'active':0}
        else:
            y = { 'active':1}
         
        z = {'id': self.a}
        j = g.update('datas', y, z)
       
        return j 
        
    def pullClass(self):
        cn = Db()
        dts = cn.selectn('datas', '' , '', {'pubID': 23})
        arr = {}
        
        try:
            for j in dts:
                arr[j['id']] =[j['id'], j['name'], j['abbrv'], j['subID'], j['active']]
        except:
            pass
    
        return arr
    
    def lunchUnitForm(self, a, b):
        b.close()
        self.a = a
        self.form = StoreTypeForm(self.a)
        self.form.show()
    
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
        
        self.l2 = QLabel("Abbrv")
        self.le2 = QLineEdit()
        self.le2.setObjectName("abbrv")
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
        
        
        groupBox = QGroupBox('Add Category')
        groupBox.setLayout(layout)
        
        
        grid = QGridLayout()
        grid.addWidget(groupBox, 0, 0)
        self.setLayout(grid)
        self.connect(self.pb, SIGNAL("clicked()"), lambda: self.button_click(self))
        self.connect(self.pb1, SIGNAL("clicked()"), lambda: self.button_close(self))
        self.setWindowTitle("Stores Manager")
        
    def button_click(self, a):
        # shost is a QString object
        a.close()
        s1 = self.le.text()
        s2 = self.le2.text()
        g = Db()
        try:
            if(len(s1) > 0) and (len(s2) > 0):
                y = { 'name':s1.lower(), 'abbrv':s2.lower(), 'pubID':23, 'active':0}
                g.insert('datas', y)
                
            else:
                pass
        except:
            pass
        
        try:
            self.lunchForm()
        except:
            pass
        try:
            self.close()
        except:
            pass
        
        
        
    def lunchForm(self):
        self.form = StoreForm()
        self.form.show()
    
    def button_close(self,a):
        a.close()
        self.lunchForm()
        

class EditForm(QDialog): 
    
    def __init__(self, sid, parent=None):
        super(EditForm, self).__init__(parent)
        self.sid = sid
        data = self.callData(self.sid)
        
        self.l1 = QLabel("Name")
        self.le = QLineEdit()
        self.le.setObjectName("name")
        self.le.setText(str(data['name']))
        
        self.l2 = QLabel("Abbrv.")
        self.le2 = QLineEdit()
        self.le2.setObjectName("abbrv")
        self.le2.setText(str(data['abbrv']))
        

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
        
        groupBox = QGroupBox('Edit Category')
        groupBox.setLayout(layout)
        
        grid = QGridLayout()
        grid.addWidget(groupBox, 0, 0)
        self.setLayout(grid)
        self.connect(self.pb, SIGNAL("clicked()"), lambda x = data['id']: self.button_click(x, self))
        self.connect(self.pb1, SIGNAL("clicked()"),lambda: self.button_close(self))
        self.setWindowTitle("Stores Manager")
        
    def button_click(self, a, b):
        # shost is a QString object

        b.close()
        s1 = self.le.text()
        s2 = self.le2.text()
        self.a = a
        g = Db()
        if(len(s1) > 0):
            y = { 'name':s1.lower(), 'abbrv':s2.lower()}
            z = {'id':self.a}
            g.update('datas', y, z)
        
        self.form = StoreForm()
        self.form.show()
        self.close()
        #self.lunchForm()
        
    def lunchForm(self):
        self.form = StoreForm()
        self.form.show()
        
    def button_close(self, a):
        a.close()
        self.lunchForm()

    def callData(self, a):
        # select a file
        self.a = a
        g = Db()
        return  g.selectn('datas', '', 1, {'id':self.a})