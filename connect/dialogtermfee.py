# -*- coding: utf-8 -*-
"""
Created on Sat Jul  7 15:54:19 2018

@author: CHARLES
"""
from PyQt4.QtCore import SIGNAL, Qt
from PyQt4.QtGui import QWidget, QTreeWidget, QTreeWidgetItem, QComboBox, QFrame, QDateEdit, QRadioButton, QCheckBox, QHBoxLayout, QGroupBox, QGridLayout, QDialog, QApplication, QPushButton, QLineEdit, QFormLayout, QLabel, QVBoxLayout
from dialogreport import ReportDialog, EditReportDialog
from connect import Db
from studenttable import StudentTable

class TermFeeDialog(QDialog):
    
    holdc = {}
    def __init__(self, term, parent=None):
        super(TermFeeDialog, self).__init__(parent)
        self.term = term
        terms = self.pullOnes('terms', self.term)
        session = self.pullOnes('session', terms['sessionID'])
        self.termname = str(session['name'])+' '+terms['name']+' Term Report'
        self.pagetitle = self.termname 
        
        
        #pull all CA
        ko = 0
        feesText = QLabel('Select Fee')
        feesAmountText = QLabel('Amount')
        self.feesPop = QLabel('Total:')
        self.feesAmount = QLineEdit()
        self.feesAmount.setObjectName("schno")
        self.feesAmount.setPlaceholderText("000.00")
        self.feesCombo = QComboBox()
        self.arr = self.pullFees()
        self.hol = {}
        ko = 0
        if self.arr and len(self.arr) > 0:
            for val in self.arr:
                self.feesCombo.addItem(val['name'].upper())
                self.hol[ko] = val['id']
                ko += 1
          
        self.tree1 = QTreeWidget()
        self.tree1.setHeaderLabel("Choose Class")
        self.cla_arr ={}
        parent1 = QTreeWidgetItem(self.tree1)
        parent1.setText(0, "Select Class")
        parent1.setFlags(parent1.flags() | Qt.ItemIsTristate | Qt.ItemIsUserCheckable)
        arr1 = self.pullClass()
        if arr1 and len(arr1) > 0:
            for val in arr1:
                child = QTreeWidgetItem(parent1)
                child.setFlags(child.flags() | Qt.ItemIsUserCheckable)
                child.setText(0, str(val['name']).upper())
                
                self.cla_arr[val['id']] = child
                if (val['active'] == 0):
                    child.setCheckState(0, Qt.Unchecked)
                else:
                    child.setCheckState(0, Qt.Unchecked)
                ko += 1
        
        self.tree1.itemClicked.connect(lambda x = 7: self.getClass(x))
        
        self.hw = QFormLayout()
        self.hw.addRow(feesText, self.feesCombo)
        
        self.hw1 = QFormLayout()
        self.hw1.addRow(feesAmountText, self.feesAmount)
        
        layout1 = QGridLayout()
        layout1.addLayout(self.hw, 0, 0)
        layout1.addWidget(self.tree1, 1, 0)
        layout1.addLayout(self.hw1, 2, 0)
        
        layout2 = QGridLayout()
        layout2.addWidget(self.feesPop, 0, 0)
        
        groupBox1 = QGroupBox('Fees Settings')
        groupBox1.setLayout(layout1)
        
        self.pb = QPushButton()
        self.pb.setObjectName("Add")
        self.pb.setText("Add Fees")
        
        self.pb1 = QPushButton()
        self.pb1.setObjectName("Cancel")
        self.pb1.setText("Cancel")
        
        hbo = QHBoxLayout()
        hbo.addWidget(self.pb1)
        hbo.addStretch()
        hbo.addWidget(self.pb)
        groupBox2 = QGroupBox('')
        groupBox2.setLayout(hbo)
        
        groupBox3 = QGroupBox('')
        groupBox3.setLayout(layout2)
        
        grid = QGridLayout()
        grid.addWidget(groupBox1, 0, 0)
        grid.addWidget(groupBox3, 1, 0)
        grid.addWidget(groupBox2, 2, 0)
        
        self.setLayout(grid)
        self.connect(self.pb, SIGNAL("clicked()"), lambda: self.button_click())
        self.connect(self.pb1, SIGNAL("clicked()"), lambda: self.button_close(self))
       
        self.setWindowTitle(self.pagetitle)

    
    def getClass(self, x):
        # shost is a QString object
        class_arr = []
        for i in self.cla_arr:
            if self.cla_arr[i].checkState(0) == Qt.Checked:
                        class_arr.append(i)
                        
        c = self.getClassStudent(class_arr)
        self.feesPop.setText('Total: '+ str(c[0]))
        self.cla = class_arr
        self.students = c[1]

    
    def getClassStudent(self, x = []):
        post = StudentTable(self.term, [None], x, [None])
        d = post.classStudentMul()
        return d
    
    def pullSubjects(self):
        cn = Db()
        arr = cn.selectn('datas', '' , '', {'pubID': 7})
        return arr
    
    def pullOne(self, b):
        cn = Db()
        arr = cn.selectn('datas', '' , 1, {'id': b})
        return arr
    
    def pullOnes(self, a, b):
        cn = Db()
        arr = cn.selectn(a, '' , 1, {'id': b})
        return arr
    
    def pullFees(self):
        cn = Db()
        arr = cn.selectn('datas', '' , '', {"pubID":17, "active": 0})
        return arr
    
    def pullClass(self):
        cn = Db()
        arr = cn.selectn('datas', '' , '', {"pubID":1, "active": 0})
        return arr
    
    def pullRep(self):
        cn = Db()
        ca = "rep"
        arr = cn.selectn('datas', '' , '', {"subID": self.sid, "pubID": ca})
        return arr
    
    def button_close(self, b):
        b.close()
        
    def button_report(self, b):
        b.close()
        self.post = ReportDialog(self.sid)
        self.post.show()
         
    def button_click(self):
        tex = ' Please wait processing, do not cancel or close..';
        self.feesPop.setText(tex)
        _term = self.term
        _class = self.cla
        _students = self.students
        _amount = self.feesAmount.text()
        _fee = self.hol[self.feesCombo.currentIndex()]
        print(_fee)
         
        for j in _class:
            data = {}
            data['pubID'] = 'fee'
            data['subID'] = _term
            data['abbrv'] = _fee
            data['name'] =  j
        
            cn = Db()
            feeStudent = self.feeStudents(_term, _students, _fee, _amount)
            check = cn.selectn('datas', '', 1, data)
            if(check and check['id'] == 0):
                pass
            else:
                data['description'] =  _amount
                cn.insert('datas', data)
    
        ins = feeStudent
        tex = ' TOTAL of '+ str(ins) +' inserted';
        self.feesPop.setText(tex)
        
    def feeStudents(self, session, students, fee, amount):
        db = 'student_fee'+str(session)
        cn = Db()
        fd = []
        ed = []
        
        for s in students:
            data = {}
            data['studentID'] = s[0]
            data['feeID'] = fee
            
            chk = cn.selectn(db, '', 1, data)
            if(chk and int(chk['id']) > 0):
                #confirm if money available
                pass
            else:
                #if money not set , set
                e = cn.insert(db, data)
                ed.append(e)
                
        return len(ed)
        
    def lunchEditForm(self, row):
        term = self.term
        self.close()
        self.post = EditReportDialog(term, row)
        self.post.show()
        
    def lunchDeleteForm(self, row):
        cn = Db()
        arr = cn.update('datas', {"active": 1})
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