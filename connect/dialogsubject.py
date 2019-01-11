# -*- coding: utf-8 -*-
"""
Created on Sat Aug 11 10:49:12 2018

@author: CHARLES
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Jul  7 15:54:19 2018

@author: CHARLES
"""
from PyQt4.QtCore import SIGNAL
from PyQt4.QtGui import QWidget, QFrame, QDateEdit, QRadioButton, QCheckBox, QHBoxLayout, QGroupBox, QGridLayout, QDialog, QApplication, QPushButton, QLineEdit, QFormLayout, QLabel, QVBoxLayout
from connect import Db

class SubjectCaDialog(QDialog):
    pagetitle = 'Subject-Assessment'
    holdc = {}
    def __init__(self, term, parent=None):
        super(SubjectCaDialog, self).__init__(parent)
        #self.resize(200, 600)
        ko = 0
        self.subjects = self.pullSubjects()
        self.term = term
        self.cas = self.pullCas(self.term)
        frame1 = QGroupBox('Subjects')
        frame2 = QGroupBox('Assessments')
        
        hc1_box = QVBoxLayout()
        hc2_box = QVBoxLayout()
        self.li = []
        self.liID = []
        for subject in self.subjects:
            num = subject['id']
            self.liID.append(num)
            self.c = QCheckBox('cb'+str(num))
            self.c.setText(str(subject['name']).upper())
            self.c.setObjectName("chk"+str(num))
            self.c.setChecked(False)
            self.c.toggled.connect(lambda state, x=num, y=self.c: self.chkFunc(x, y))
            hc1_box.addWidget(self.c)
            self.li.append(self.c)
            
            ko += 1
           
        
        self.li1 = []
        self.lip = {}
        self.li1ID = []
        g = Db()
        hc2_box = QVBoxLayout()
        for ca in self.cas:
            num = ca['id']
            dt = g.selectn('datas', '', 1, {'id': ca['name']})
            self.li1ID.append(num)
            self.c1 = QCheckBox('cbx'+str(num))
            self.c1.setText(str(dt['name']).upper())
            self.c1.setObjectName("chkx"+str(num))
            self.c1.setChecked(False)
            self.c1.toggled.connect(lambda state, x=num, y=self.c1: self.chkFunc(x, y))
            hc2_box.addWidget(self.c1)
            self.li1.append(self.c1)
            self.lip[num] = self.c1
            ko += 1 
            
        frame1.setLayout(hc1_box)
        #frame1.setFrameShape(QFrame.StyledPanel)
        frame2.setLayout(hc2_box)
        #frame2.setFrameShape(QFrame.StyledPanel)
        
        h_box = QHBoxLayout()
        h_box.addWidget(frame1)
        h_box.addWidget(frame2)
        
        
        self.pb = QPushButton()
        self.pb.setObjectName("MakeEntries")
        self.pb.setText("Edit View")
        
        self.pb1 = QPushButton()
        self.pb1.setObjectName("View Report")
        self.pb1.setText("Report View")
        
        self.pb2 = QPushButton()
        self.pb2.setObjectName("Cancel")
        self.pb2.setText("Cancel")
        
        but_box = QHBoxLayout()
        but_box.addWidget(self.pb2)
        but_box.addWidget(self.pb1)
        but_box.addWidget(self.pb)
        
        main_box = QVBoxLayout()
        main_box.addLayout(h_box)
        main_box.addLayout(but_box)
        
        
        self.setLayout(main_box)
        self.connect(self.pb, SIGNAL("clicked()"), lambda: self.button_click(0))
        self.connect(self.pb1, SIGNAL("clicked()"), lambda: self.button_click(1))
        self.connect(self.pb2, SIGNAL("clicked()"), lambda: self.button_close())
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
        
    
    def pullSubjects(self):
        cn = Db()
        arr = cn.selectn('datas', '' , '', {'pubID': 3})
        return arr
    
    def pullCas(self, term):
        cn = Db()
        arr = cn.selectn('datas', '' , '', {'subID':term , 'pubID':'ca'})
        return arr
    
    def button_close(self):
        self.reject()
        
    def button_click(self, a):
        self.prime = a
        self.accept()
        
    def getValue(self):
        
        k1 = []
        k2 = []
        for s in range(0, len(self.li)):
            if self.li[s].isChecked():
                k1.append(self.liID[s])
            else:
                k2.append(self.liID[s])
                 
          
        
    
        k11 = []
        k21 = []
        for s in self.lip:
            if self.lip[s].isChecked():
                k11.append(s)
            else:
                k21.append(s)
                 
        return [k1, k11, self.prime] 
    
