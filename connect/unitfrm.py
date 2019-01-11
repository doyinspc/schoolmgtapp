# -*- coding: utf-8 -*-
"""
Created on Sun Jul  8 11:46:41 2018

@author: CHARLES
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Jul  7 15:54:19 2018

@author: CHARLES
"""

import sys
from PyQt4.QtCore import SIGNAL
from PyQt4.QtGui import QWidget, QCheckBox, QHBoxLayout, QGroupBox, QGridLayout, QDialog, QApplication, QPushButton, QLineEdit, QFormLayout, QLabel, QVBoxLayout
from connect import Db

class UnitForm(QDialog):
    
    
    def __init__(self, sid, parent=None):
        super(UnitForm, self).__init__(parent)
       
        self.sid = sid
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
        
        ko = 0
        layout1 = QGridLayout()
        
        details = self.pullDetails(self.sid)
        detailsname = str(details[2])
        arr = self.pullClass(self.sid)
        for i in arr:
            self.c = QCheckBox()
            self.c.setText(arr[i])
            self.c.setObjectName("chk"+str(i))
            self.b = QPushButton()
            self.b.setObjectName("btn"+str(i))
            self.b.setText('Add')
            self.b1 = QPushButton()
            self.b1.setObjectName("btn1"+str(i))
            self.b1.setText('Edit')
            self.connect(self.b, SIGNAL("clicked()"), lambda x = i:self.button_click(x))
            self.connect(self.b1, SIGNAL("clicked()"), lambda y = i:self.button_click(y))


            layout1.addWidget(self.c, ko, 0)
            layout1.addWidget(self.b, ko, 1)
            layout1.addWidget(self.b1, ko, 2)
            ko += 1
        
        groupBox = QGroupBox('Add Class')
        groupBox.setLayout(layout)
        
        groupBox1 = QGroupBox('All Classes')
        groupBox1.setLayout(layout1)
        
        
        grid = QGridLayout()
        grid.addWidget(groupBox, 0, 0)
        grid.addWidget(groupBox1, 1, 0)
        self.setLayout(grid)
        self.connect(self.pb, SIGNAL("clicked()"), lambda: self.button_click(self.sid))
        self.connect(self.pb1, SIGNAL("clicked()"), self.close)
        self.setWindowTitle(detailsname)

    def button_click(self, a):
        # shost is a QString object
        s1 = self.le.text()
        s2 = self.le2.text()
        self.a = a
        g = Db()
        if(len(s1) > 0):
            y = { 'name':s1, 'subID': self.a, 'abbrv':s2}
            g.insert('datas', y)
        self.repaint()

    def button_click1(self, a):
        # shost is a QString object
        s1 = self.le.text()
        s2 = self.le2.text()
        self.a = a
        g = Db()
        if(len(s1) > 0):
            y = { 'name':s1, 'subID': self.a, 'abbrv':s2}
            return  g.insert('datas', y)
        
    def pullClass(self, a):
        self.a = a
        cn = Db()
        students = cn.select('datas', '' , '', {'subID':self.a})
        arr = {}
        
        for j in students:
            arr[j[0]] = j[2]
        return arr
    
    def pullDetails(self, a):
        self.a = a
        cn = Db()
        return cn.select('datas', '' , 1, {'id':self.a})
       # arr = {}
        
        
        #print(students)
        #for j in students:
           # arr[j[0]] = j[2]
        #return arr
    
   
        


