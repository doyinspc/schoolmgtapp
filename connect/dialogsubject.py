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
from PyQt4.QtCore import SIGNAL, Qt
from PyQt4.QtGui import QWidget, QTreeWidgetItem, QTreeWidget, QFrame, QDateEdit, QRadioButton, QCheckBox, QHBoxLayout, QGroupBox, QGridLayout, QDialog, QApplication, QPushButton, QLineEdit, QFormLayout, QLabel, QVBoxLayout
from connect import Db

class SubjectCaDialog(QDialog):
    pagetitle = 'Subject-Assessment'
    holdc = {}
    def __init__(self, term, parent=None):
        super(SubjectCaDialog, self).__init__(parent)
        self.setMinimumHeight(280)
        ko = 0
        self.subjects = self.pullSubjects()
        self.term = term
        self.cas = self.pullCas(self.term)
        g = Db()
        hc1_box = QVBoxLayout()
        self.subject_hold = {}
        self.ca_hold = {}
        self.tree1 = QTreeWidget()
        self.tree1.setMinimumHeight(280)
        self.tree1.setHeaderLabel("Select Subject and CA to Display")
        self.hold_checkbox = []
        parent1 = QTreeWidgetItem(self.tree1)
        parent1.setText(0, "Select")
        parent1.setFlags(parent1.flags() | Qt.ItemIsTristate | Qt.ItemIsUserCheckable)
        for subject in self.subjects:
            num = subject['id']
            child = QTreeWidgetItem(parent1)
            child.setFlags(child.flags() | Qt.ItemIsTristate | Qt.ItemIsUserCheckable) 
            child.setText(0, str(subject['name']).upper())                        
            child.setCheckState(0, Qt.Checked)
            for ca in self.cas:
                dt = g.selectn('datas', '', 1, {'id': ca['name']})
                child2 = QTreeWidgetItem(child)
                child2.setFlags(child2.flags() | Qt.ItemIsTristate | Qt.ItemIsUserCheckable)
                child2.setText(0, str(dt['name']).upper())
                child2.setCheckState(0, Qt.Checked)
                self.hold_checkbox.append(child2)
                self.subject_hold[child2] = num 
                self.ca_hold[child2] = ca['id']
                ko += 1

            hc1_box.addWidget(self.tree1)
            
            
            ko += 1
        
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
        main_box.addLayout(hc1_box)
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
        _subject = {}
        for s in self.hold_checkbox:
            if s.checkState(0) == Qt.Checked:
                sub = int(self.subject_hold[s])
                ca = int(self.ca_hold[s])
                if sub in _subject and isinstance(_subject[sub], list):
                    _subject[sub].append(ca)
                else:
                    _subject[sub] = []
                    _subject[sub].append(ca)     
            else:
               pass
                 
        return [_subject, self.prime] 
    
