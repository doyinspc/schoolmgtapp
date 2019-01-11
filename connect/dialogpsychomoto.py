# -*- coding: utf-8 -*-
"""
Created on Wed Aug 29 01:00:55 2018

@author: CHARLES
"""

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
import sip

class PsychomotoCaDialog(QDialog):
    pagetitle = 'Skill-Assessment'
    holdc = {}
    hold  = []
    def __init__(self, parent=None):
        super(PsychomotoCaDialog, self).__init__(parent)
        
        ko = 0
        self.subjects = self.pullSubjects()
        
        self.frame1 = QGroupBox('Skills')
        self.frame2 = QGroupBox('Categories')
        
        hc1_box = QVBoxLayout()
        hc2_box = QVBoxLayout()
        self.li = []
        self.liID = []
        for subject in self.subjects:
            num = subject['id']
            self.liID.append(num)
            self.c = QRadioButton('cb'+str(num))
            self.c.setText(str(subject['name']).upper())
            self.c.setObjectName("chk"+str(num))
            self.c.setChecked(False)
            self.c.toggled.connect(lambda state, x=num, y=self.c: self.catItems(x, y))
            hc1_box.addWidget(self.c)
            self.li.append(self.c)
            
            ko += 1
           
        
        self.li1 = []
        self.li1ID = []
        self.hc2_box = QVBoxLayout()
            
        self.frame1.setLayout(hc1_box)
        #frame1.setFrameShape(QFrame.StyledPanel)
        self.frame2.setLayout(self.hc2_box)
        #frame2.setFrameShape(QFrame.StyledPanel)
        
        h_box = QHBoxLayout()
        h_box.addWidget(self.frame1)
        h_box.addWidget(self.frame2)
        
        
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
        self.connect(self.pb, SIGNAL("clicked()"), lambda: self.button_click())
        self.connect(self.pb, SIGNAL("clicked()"), lambda: self.button_click())
        self.connect(self.pb2, SIGNAL("clicked()"), lambda: self.button_close())
        self.setWindowTitle(self.pagetitle)

    
    def catItems(self, a, b):
        _a = a
        self.cas = self.pullCas(_a)
        print(self.hold)
        self.li1 = []
        self.li1ID = []
        for rp in self.hold:
            self.hc2_box.removeWidget(rp)
            sip.delete(rp)
        
        self.hold = []
        ko = 0
        for ca in self.cas:
            num = ca['id']
            self.li1ID.append(num)
            self.c1 = QCheckBox('cbx'+str(num))
            self.c1.setText(str(ca['name']).upper())
            self.c1.setObjectName("chkx"+str(num))
            self.c1.setChecked(True)
            self.hc2_box.addWidget(self.c1)
            self.hold.append(self.c1)
            self.li1.append(self.c1)
            ko += 1
            
        
        #self.hc2_box.show()
        
    
    def pullSubjects(self):
        cn = Db()
        arr = cn.selectn('datas', '' , '', {'pubID': 9})
        return arr
    
    def pullCas(self, a):
        _a = a
        cn = Db()
        arr = cn.selectn('datas', '' , '', {'subID': _a})
        return arr
    
    def button_close(self):
        self.reject()
        
    def button_click(self):
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
        for s in range(0, len(self.li1)):
            if self.li1[s].isChecked():
                k11.append(self.li1ID[s])
            else:
                k21.append(self.li1ID[s])
                 
        return [k1, k11] 
    
