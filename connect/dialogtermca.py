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
from PyQt4.QtGui import QWidget,QComboBox, QFrame, QDateEdit, QRadioButton, QCheckBox, QHBoxLayout, QGroupBox, QGridLayout, QDialog, QApplication, QPushButton, QLineEdit, QFormLayout, QLabel, QVBoxLayout
from dialogreport import ReportDialog, EditReportDialog
from connect import Db

class TermCaDialog(QDialog):
    
    holdc = {}
    def __init__(self, sid, termname, parent=None):
        super(TermCaDialog, self).__init__(parent)
        self.sid = sid
        self.term = sid
        self.termname = termname
        terms = self.pullOnes(self.sid)
        self.session = terms['sessionID']
        self.pagetitle = str(termname)+' '+terms['name']+' Term Assessments'
        ko = 0
        layout1 = QGridLayout()
        
        #pull all CA
        arr = self.pullCas()
        hold ={}
        if arr and len(arr) > 0:
            for val in arr:
                num = val['id']
                dt = self.pullOne(val['name'])
                self.c = QCheckBox('cb'+str(num))
                self.c.setText(str(dt['name']).upper()+' ('+val['abbrv']+')')
                self.c.setObjectName("chk"+str(num))
                if (val['active'] == 0):
                    self.c.setChecked(True)
                else:
                   self.c.setChecked(False)
                
                self.c.toggled.connect(lambda state, x=val, y=self.c: self.chkFunc(x, y))
                
                self.b = QPushButton()
                self.b.setObjectName("btn"+str(val))
                self.b.setText('Edit')
                
                hold["btn"+str(val)] = self.b
                
                layout1.addWidget(self.c, ko, 0)
                layout1.addWidget(self.b, ko, 1)
                
                ko += 1
            
      
            for j in arr:
                self.h = j
                b = "btn"+str(j)
                
                self.connect(hold[b], SIGNAL("clicked()"), lambda gh=j: self.lunchEditForm(gh, self))
                
        groupBox1 = QGroupBox('All Assessments')
        groupBox1.setLayout(layout1)
        
        self.pb = QPushButton()
        self.pb.setObjectName("Add")
        self.pb.setText("Add Assessment")
        
        self.pb2 = QPushButton()
        self.pb2.setObjectName("report")
        self.pb2.setText("Reports Settings")
        
        self.pb1 = QPushButton()
        self.pb1.setObjectName("Cancel")
        self.pb1.setText("Cancel")
        
        hbo = QHBoxLayout()
        hbo.addWidget(self.pb1)
        hbo.addStretch()
        hbo.addWidget(self.pb2)
        hbo.addStretch()
        hbo.addWidget(self.pb)
        groupBox2 = QGroupBox('')
        groupBox2.setLayout(hbo)
        
        hbo1 = QHBoxLayout()
    
        templates = self.pullTemp()
        self.lTemplate = QLabel('Select Template')
        self.cTemplate = QComboBox()
        self.cTemplate.addItem('None')
        for i in templates:
            self.cTemplate.addItem(i['abbrv'])
            
        hbo1.addWidget(self.lTemplate)
        hbo1.addWidget(self.cTemplate)
        hbo1.addWidget(self.pb2)
       
        groupBox4 = QGroupBox('')
        groupBox4.setLayout(hbo1)
        
        #pull all CA
        layout2 = QGridLayout()
        arrr = self.pullRep()
        hold ={}
        if arrr and len(arrr) > 0:
            for val in arrr:
                num = val['id']
                lit = val['description']
                lit =lit.split(':::')
                c = QLabel(lit[0].upper())
                
                b = QPushButton()
                b.setObjectName("btn"+str(num))
                b.setText('Edit')
                self.connect(b, SIGNAL("clicked()"), lambda gh=num: self.lunchEditForm(gh))
            
                
                d = QPushButton()
                d.setObjectName("btn1"+str(num))
                d.setText('Delete')
                self.connect(d, SIGNAL("clicked()"), lambda gh=num: self.lunchDeleteForm(gh))
            
                
                hold["btn"+str(val)] = b
                layout2.addWidget(c, ko, 0)
                layout2.addWidget(b, ko, 1)
                layout2.addWidget(d, ko, 2)
                ko += 1
            
        
        groupBox3 = QGroupBox('Academic Report Settings')
        groupBox3.setLayout(layout2)
        
        grid = QGridLayout()
        grid.addWidget(groupBox1, 0, 0)
        grid.addWidget(groupBox2, 1, 0)
        grid.addWidget(groupBox4, 2, 0)
        grid.addWidget(groupBox3, 3, 0)
        
        self.setLayout(grid)
        self.connect(self.pb, SIGNAL("clicked()"), lambda: self.button_click(self))
        self.connect(self.pb1, SIGNAL("clicked()"), lambda: self.button_close(self))
        self.connect(self.pb2, SIGNAL("clicked()"), lambda: self.button_report(self))
       
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
        arr = cn.selectn('datas', '' , '', {'pubID': 7})
        return arr
    
    def pullOne(self, b):
        cn = Db()
        arr = cn.selectn('datas', '' , 1, {'id': b})
        return arr
    
    def pullOnes(self, b):
        cn = Db()
        arr = cn.selectn('terms', '' , 1, {'id': b})
        return arr
    
    def pullCas(self):
        cn = Db()
        ca = "ca"
        arr = cn.selectn('datas', '' , '', {"subID": self.sid, "pubID": ca})
        return arr
    
    def pullRep(self):
        cn = Db()
        ca = "rep"
        arr = cn.selectn('datas', '' , '', {"subID": self.sid, "pubID": ca})
        return arr
    
    def pullTemp(self):
        cn = Db()
        ca = "temp"
        arr = cn.selectn('datas', '' , '', {"subID": self.sid, "pubID": ca})
        return arr
    
    def button_close(self, b):
        b.close()
        from frmsessionterm import TermForm
        self.post = TermForm(self.session)
        self.post.show()
        
    def button_report(self, b):
        b.close()
        self.post = ReportDialog(self.sid)
        self.post.show()
         
    def button_click(self, b):
        b.close()
        self.post = AddDialog(self.term, self.termname, self.pagetitle)
        self.post.show()
        
    def lunchEditForm(self, row):
        term = self.term
        self.close()
        self.post = EditReportDialog(term, row)
        self.post.show()
        
    def lunchDeleteForm(self, row):
        cn = Db()
        arr = cn.update('datas', {"active": 1}, {"id": row})
        self.close()
        self.__init__(self.term, self.termname)
        
    
    
class AddDialog(QDialog):
    
    holdc = {}
    def __init__(self, term, termname, pagetitle, parent=None):
        super(AddDialog, self).__init__(parent)
        self.sid = term
        displayInfo = self.pullSubjects()
        self.pagetitle = pagetitle
        self.termname = termname
        
        self.l1 = QLabel("Assessment Types")
        self.le = QComboBox()
        for dd in displayInfo:
            self.le.addItem(str(dd['name']).upper(), dd['id'])
       
        self.le.setObjectName("name")
        
        self.l2 = QLabel("Max Score")
        self.le2 = QLineEdit()
        self.le2.setObjectName("maxscore")
        
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
        
        groupBox = QGroupBox('Add Assessment')
        groupBox.setLayout(layout)
        
        grid = QGridLayout()
        grid.addWidget(groupBox, 0, 0)
        self.setLayout(grid)
        self.connect(self.pb, SIGNAL("clicked()"), lambda: self.button_click(self))
        self.connect(self.pb1, SIGNAL("clicked()"), lambda: self.button_close(self))
        
        self.setWindowTitle(self.pagetitle)
        
    
    def pullSubjects(self):
        cn = Db()
        arr = cn.selectn('datas', '' , '', {'pubID': 7})
        return arr
    
    def pullOne(self, b):
        cn = Db()
        arr = cn.selectn('datas', '' , 1, {'id': b})
        return arr
    
    def button_close(self, a):
        a.close()
        self.lunchForm()
        
    def lunchForm(self):
        self.close()
        form = TermCaDialog(self.sid, self.termname)
        form.show()
         
    def button_click(self, b):
        # shost is a QString object
        b.close()
        sid = self.sid
        s2 = self.le2.text()
        s1 = self.le.itemData(self.le.currentIndex())
        g = Db()
        try:
            if(int(s2) > 0):
                y = { 'name':s1, 'subID':sid, 'pubID':'ca', 'abbrv':s2, 'active':0}
                h = g.insert('datas', y)
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
    
class EditDialog(QDialog):
    pagetitle = "Edit Term's Assessment"
    holdc = {}
    def __init__(self, sid, mid, parent=None):
        super(EditDialog, self).__init__(parent)
        self.sid = sid
        self.mid = mid
        
        displayInfo = self.pullSubjects()
        
        
        dis = self.pullOne(self.mid)
        
        self.l1 = QLabel("Assessment Types")
        self.le = QComboBox()
        for dd in displayInfo:
            self.le.addItem(str(dd['name']).upper(), dd['id'])
       
        self.le.setObjectName("name")
        #self.le.setCurrentIndex(2)
        
        self.l2 = QLabel("Max Score")
        self.le2 = QLineEdit()
        self.le2.setObjectName("maxscore")
        if dis:
            self.le2.setText(dis['abbrv'])
        else:
            pass
        
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
        
        groupBox = QGroupBox('Add Assessment')
        groupBox.setLayout(layout)
        
        grid = QGridLayout()
        grid.addWidget(groupBox, 0, 0)
        self.setLayout(grid)
        self.connect(self.pb, SIGNAL("clicked()"), lambda: self.button_click(self))
        self.connect(self.pb1, SIGNAL("clicked()"), lambda: self.button_close(self))
        
        self.setWindowTitle(self.pagetitle)
        
    
    def pullSubjects(self):
        cn = Db()
        arr = cn.selectn('datas', '' , '', {'pubID': 7})
        return arr
    
    def pullOne(self, b):
        cn = Db()
        arr = cn.selectn('datas', '' , 1, {'id': b})
        return arr
    
    def button_close(self, a):
        a.close()
        self.lunchForm()
        
    def lunchForm(self):
        sid = self.sid
        form = TermCaDialog(sid)
        form.show()
         
    def button_click(self, b):
        # shost is a QString object
        b.close()
        sid = self.sid
        mid = self.mid
        s2 = self.le2.text()
        s1 = self.le.itemData(self.le.currentIndex())
        g = Db()
        try:
            if(int(s2) > 0):
                y = { 'name':s1,  'abbrv':s2}
                z = {'id':mid}
                g.update('datas', y, z)
    
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