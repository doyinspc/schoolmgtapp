# -*- coding: utf-8 -*-
"""
Created on Fri Jul 13 15:22:52 2018

@author: CHARLES
"""
from PyQt4.QtCore import SIGNAL, QDate
from PyQt4.QtGui import QWidget, QDateEdit, QColorDialog, QRadioButton, QCheckBox, QHBoxLayout, QGroupBox, QGridLayout, QDialog, QApplication, QPushButton, QLineEdit, QFormLayout, QLabel, QVBoxLayout
from connect import Db
import json
class GradingForm(QDialog):
    
    def __init__(self, sid, parent=None):
        super(GradingForm, self).__init__(parent)
        self.sid = sid
        ko = 0
        layout1 = QGridLayout()
        try: 
            details = self.pullDetails(self.sid)
            pagetitle = str(details['name']) +' ' 
        except:
            details = []
            pagetitle = 'None'
        
        arr = self.pullClass(self.sid)
       
        hold ={}
        for val in arr:
            grp = arr[val][2].split(':')
            self.num = val
            self.c = QCheckBox('cb'+str(val))
            self.c.setText(arr[val][0] + ' - '+ arr[val][1])
            self.c.setObjectName("chk"+str(val))
            
            if (arr[val][3] == 0):
                self.c.setChecked(True)
            else:
               self.c.setChecked(False)
            
             
            self.c.toggled.connect(lambda state, x=val, y=self.c: self.chkFunc(x, y))
            self.d = QPushButton()
            self.d.setObjectName("btnx"+str(val))
            self.d.setText(grp[0] + ' to '+ grp[1])
            self.d.setStyleSheet("background-color:"+grp[2] +"; color: white")
            #self.b = QPushButton()
            #self.b.setObjectName("btn"+str(val))
            #self.b.setText('Terms')
            self.b1 = QPushButton()
            self.b1.setObjectName("btn1"+str(val))
            self.b1.setText('Edit')
            hold["btn"+str(val)] = self.b1
            layout1.addWidget(self.c, ko, 0)
            layout1.addWidget(self.d, ko, 1)
            layout1.addWidget(self.b1, ko, 2)
            ko += 1
            
      
        for j in arr:
            self.h = j
            b = "btn"+str(j)
            self.connect(hold[b], SIGNAL("clicked()"), lambda gh=j: self.lunchEditForm(gh, self))
            
        groupBox1 = QGroupBox('Grading')
        groupBox1.setLayout(layout1)
        
        self.pb = QPushButton()
        self.pb.setObjectName("Add")
        self.pb.setText("Add")
        
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
        
        if b.isChecked() == True:
            y = { 'active':1}
        else:
            y = { 'active':0}
         
        
        z = {'id': self.a}
        j = g.update('datas', y, z)
       
        return j 
        
    def pullClass(self, a):
        self.a = a
        cn = Db()
        datas = cn.selectn('datas', '' , '', {'subID':self.a})
        arr = {}
        
        try:
            for j in datas:
                arr[j['id']] =[j['name'], j['abbrv'], j['description'], j['active']]
        except:
            pass
        return arr
    
    def pullDetails(self, a):
        self.a = a
        cn = Db()
        datas = cn.selectn('datas', '' , 1, {'id':self.a})
    
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
        self.form = super.GradeForm()
        self.form.show()
    
    def button_close(self, a):
        a.close()
        from frmgrade import GradeForm
        self.form = GradeForm()
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
        
        self.l2 = QLabel("Abbrv")
        self.le2 = QLineEdit()
        self.le2.setObjectName("abbrv")
        self.le2.setText("")
        
        self.l3 = QLabel("Max Score")
        self.le3 = QLineEdit()
        self.le3.setObjectName("maxz")
        self.le3.setText("")
        
        self.l4 = QLabel("Min Score")
        self.le4 = QLineEdit()
        self.le4.setObjectName("minz")
        self.le4.setText("")
        
        self.l5 = QLabel("Pick Color")
        self.pb2 = QPushButton()
        self.pb2.setObjectName("Pickcolor")
        self.pb2.setText("Click to change")
        
        self.le5 = QLineEdit()
        self.le5.setObjectName("Showcolor")
        self.le5.setText("#000000")
        self.pb2.setStyleSheet("background-color: black; color: white")
        
        self.lv_box = QHBoxLayout()
        self.lv_box.addWidget(self.pb2)
        self.lv_box.addWidget(self.le5)
        
        
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
        layout.addRow(self.l4, self.le4)
        layout.addRow(self.l5, self.lv_box)
        layout.addRow(self.pb1, self.pb)
        
        
        groupBox = QGroupBox('Add New')
        groupBox.setLayout(layout)
        
        self.connect(self.pb2, SIGNAL("clicked()"), lambda: self.color_picker())
        grid = QGridLayout()
        grid.addWidget(groupBox, 0, 0)
        self.setLayout(grid)
        self.connect(self.pb, SIGNAL("clicked()"), lambda: self.button_click(self.sid, self))
        self.connect(self.pb1, SIGNAL("clicked()"), lambda: self.button_close(self.sid, self))
        self.setWindowTitle(pagetitle)
        
    
    def color_picker(self):
        self.cp = QColorDialog.getColor()
        self.le5.setText(self.cp.name())
        self.pb2.setStyleSheet("background-color:"+self.cp.name() +"")
        return self.cp.name()
        
    def button_click(self, a, b):
        # shost is a QString object
        b.close()
        self.a = a
        s1 = self.le.text()
        s2 = self.le2.text()
        s3 = self.le3.text()
        s4 = self.le4.text()
        s5 = self.le5.text()
        fil = str(s3)+":"+str(s4)+":"+str(s5)
        
        g = Db()
        try:
            if(len(s1) > 0 and len(s2) > 0 and len(s3) > 0 and len(s4) > 0):
                y = { 'name':s1, 'abbrv':s2, 'pubID':6, 'subID':self.a,  'description':fil ,'active':0}
                w = g.insert('datas', y) 
                print(w)
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
        self.form = GradingForm(self.a)
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
        
        data1 = str(data['description']).split(":")
        
        try: 
            details = self.pullDetails(data['subID'])
            pagetitle = str(details[2]) +' grading' 
        except:
            details = []
            pagetitle = 'None'
        
        self.l1 = QLabel("Name")
        self.le = QLineEdit()
        self.le.setObjectName("name")
        self.le.setText(data['name'])
        
        self.l2 = QLabel("Abbrv")
        self.le2 = QLineEdit()
        self.le2.setObjectName("abbrv")
        self.le2.setText(data['abbrv'])
        
        self.l3 = QLabel("Max Score")
        self.le3 = QLineEdit()
        self.le3.setObjectName("maxz")
        self.le3.setText(data1[0])
        
        self.l4 = QLabel("Min Score")
        self.le4 = QLineEdit()
        self.le4.setObjectName("minz")
        self.le4.setText(data1[1])
        
        self.l5 = QLabel("Pick Color")
        self.pb2 = QPushButton()
        self.pb2.setObjectName("Pickcolor")
        self.pb2.setText("Click to change")
        
        self.le5 = QLineEdit()
        self.le5.setObjectName("Showcolor")
        self.le5.setText(data1[2])
        self.pb2.setStyleSheet("background-color: "+data1[2]+"; color: white")
        
        self.lv_box = QHBoxLayout()
        self.lv_box.addWidget(self.pb2)
        self.lv_box.addWidget(self.le5)
        
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
        layout.addRow(self.l4, self.le4)
        layout.addRow(self.l5, self.lv_box)
        layout.addRow(self.pb1, self.pb)
        
        groupBox = QGroupBox('Edit Grading')
        groupBox.setLayout(layout)
        
        grid = QGridLayout()
        grid.addWidget(groupBox, 0, 0)
        self.setLayout(grid)
        self.connect(self.pb2, SIGNAL("clicked()"), lambda: self.color_picker())
        self.connect(self.pb, SIGNAL("clicked()"), lambda: self.button_click(self.sid, details[0], self))
        self.connect(self.pb1, SIGNAL("clicked()"),lambda: self.button_close(details[0], self))
        self.setWindowTitle(pagetitle)
        
    def color_picker(self):
        self.cp = QColorDialog.getColor()
        self.le5.setText(self.cp.name())
        self.pb2.setStyleSheet("background-color:"+self.cp.name() +"")
        return self.cp.name()
    
    def button_click(self, a, c, b):
        # shost is a QString object
        b.close()
        s1 = self.le.text()
        s2 = self.le2.text()
        s3 = self.le3.text()
        s4 = self.le4.text()
        s5 = self.le5.text()
        fil = str(s3)+":"+str(s4)+":"+str(s5)
        self.a = a
        self.c = c
        g = Db()
        if(len(s1) > 0 and len(s2) > 0 and len(s3) > 0 and len(s4) > 0):
                
                y = { 'name':s1, 'abbrv':s2, 'description':fil ,'active':0}
                z = {'id':self.a}
                g.update('datas', y, z)
            
        self.form = GradingForm(self.c)
        self.form.show()
        self.close()
        #self.lunchForm()
        
    def lunchForm(self, a):
        self.a = a
        self.form = GradingForm(self.a)
        self.form.show()
        
    def button_close(self, a, b):
        b.close()
        self.a = a
        self.lunchForm(self.a)
        
    def pullDetails(self, a):
        self.a = a
        cn = Db()
        datas = cn.select('datas', '' , 1, {'id':self.a})
        
        return datas 

    def callData(self, a):
        # select a file
        self.a = a
        g = Db()
        return  g.selectn('datas', '', 1, {'id':self.a})