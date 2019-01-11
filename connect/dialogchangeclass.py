
from PyQt4.QtCore import SIGNAL
from PyQt4.QtGui import  QComboBox, QWidget, QFrame, QDateEdit, QRadioButton, QCheckBox, QHBoxLayout, QGroupBox, QGridLayout, QDialog, QApplication, QPushButton, QLineEdit, QFormLayout, QLabel, QVBoxLayout
from connect import Db
from studenttable import StudentTable
import sip

class ChangeClassDialog(QDialog):
    pagetitle = 'Change Class'
    holdc = {}
    hold  = []
    def __init__(self, session, students, parent=None):
        super(ChangeClassDialog, self).__init__(parent)
        
        ko = 0
        self.students = self.pullStudents(students)
        self.session = session[2]
        self.claszs = self.pullClass(1)
        
        
        self.d_displayData = QComboBox()
        for k in self.claszs:
            act = str(self.claszs[k])+' '
            for k in self.claszs:
               arr = self.pullClass(k)
               for dd in arr:
                   self.d_displayData.addItem(str(act + arr[dd]).upper(), dd)
        
        self.frame1 = QGroupBox('Students')
        self.frame2 = QGroupBox('New Class')
        
        hc1_box = QVBoxLayout()
        
        self.li = []
        self.liID = []
        for student in self.students:
            num = student['id']
            self.liID.append(num)
            self.c = QCheckBox('cb'+str(num))
            self.c.setText(str(student['surname']+' '+student['firstname']+' '+student['othername']).title())
            self.c.setObjectName("chk"+str(num))
            self.c.setChecked(True)
            self.c.toggled.connect(lambda state, x=num, y=self.c: self.catItems(x, y))
            hc1_box.addWidget(self.c)
            self.li.append(self.c)
            
            ko += 1
           
        
        self.li1 = []
        self.li1ID = []
        
        exp = QLabel('Select Class')
        ses_name = str(session[1])+' '+str(session[3])
        ses = QLabel(ses_name)
        
        
        v_box = QHBoxLayout()
        v_box.addWidget(exp)
        v_box.addStretch()
        v_box.addWidget(self.d_displayData)
        
        hv_box= QVBoxLayout()
        hv_box.addWidget(ses)
        hv_box.addStretch()
        hv_box.addLayout(v_box)
            
        self.frame1.setLayout(hc1_box)
        #frame1.setFrameShape(QFrame.StyledPanel)
        self.frame2.setLayout(hv_box)
        #frame2.setFrameShape(QFrame.StyledPanel)
        
        h_box = QVBoxLayout()
        h_box.addWidget(self.frame2)
        h_box.addWidget(self.frame1)
                 
        self.pb = QPushButton()
        self.pb.setObjectName("setclass")
        self.pb.setText("Set Class")        
        
        self.pb2 = QPushButton()
        self.pb2.setObjectName("Cancel")
        self.pb2.setText("Cancel")
        
        but_box = QHBoxLayout()
        but_box.addWidget(self.pb2)
        but_box.addWidget(self.pb)
        
        main_box = QVBoxLayout()
        main_box.addLayout(h_box)
        main_box.addLayout(but_box)
        
        self.setLayout(main_box)
        self.connect(self.pb, SIGNAL("clicked()"), lambda: self.button_click())
        self.connect(self.pb2, SIGNAL("clicked()"), lambda: self.button_close())
        self.setWindowTitle(self.pagetitle)

    
    def catItems(self, a, b):
        _a = a
        self.cas = self.pullCas(_a)
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
        
    
    def pullClasz(self):
        cn = Db()
        arr = cn.selectn('datas', '' , '', {'pubID': 11})
        return arr
    
    def pullClass(self, a):
        self.a = a
        cn = Db()
        students = cn.select('datas', '' , '', {'subID':self.a, 'active':0})
        arr = {}
        
        for j in students:
            arr[j[0]] = j[2]
        return arr
    
    def pullStudents(self, a):
        cn = Db()
        arr = cn.selectStudents(a)
        return arr
    
    def pullCas(self, a):
        _a = a
        cn = Db()
        arr = cn.selectn('datas', '' , '', {'subID': _a})
        return arr
    
    def button_close(self):
        self.reject()
        
    def button_click(self):
        students = self.getValue()
        moveclass = self.d_displayData.itemData(self.d_displayData.currentIndex())
        session = self.session
        data =  StudentTable()
        data.classMoveStudent(session, moveclass, students[0])
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
    
    def pullSession(self, a):
        # select a file
        self.a = a
        g = Db()
        return  g.select('session', '', 1, {'id':self.a})

        
class RemoveClassDialog(QDialog):
    pagetitle = 'Change Class'
    holdc = {}
    hold  = []
    def __init__(self, session, students, parent=None):
        super(RemoveClassDialog, self).__init__(parent)
        
        
        ko = 0
        self.students = self.pullStudents(students)
        self.session = session[2]
        self.frame1 = QGroupBox('Remove From Class')
        
        hc1_box = QVBoxLayout()
        ses_name = str(session[1])+' '+str(session[3]+' Term')
        ses = QLabel(ses_name)
        hc1_box.addWidget(ses)
        
        self.li = []
        self.liID = []
        for student in self.students:
            num = student['id']
            self.liID.append(num)
            self.c = QCheckBox('cb'+str(num))
            self.c.setText(str(student['surname']+' '+student['firstname']+' '+student['othername']).title())
            self.c.setObjectName("chk"+str(num))
            self.c.setChecked(True)
            self.c.toggled.connect(lambda state, x=num, y=self.c: self.catItems(x, y))
            hc1_box.addWidget(self.c)
            self.li.append(self.c)
            
            ko += 1
           
        
        self.li1 = []
        self.li1ID = []

        self.frame1.setLayout(hc1_box)
        #frame1.setFrameShape(QFrame.StyledPanel)
        
        self.pb = QPushButton()
        self.pb.setObjectName("setclass")
        self.pb.setText("Set Class")        
        
        self.pb2 = QPushButton()
        self.pb2.setObjectName("Cancel")
        self.pb2.setText("Cancel")
        
        but_box = QHBoxLayout()
        but_box.addWidget(self.pb2)
        but_box.addWidget(self.pb)
        
        main_box = QVBoxLayout()
        main_box.addWidget(self.frame1)
        main_box.addLayout(but_box)
        
        self.setLayout(main_box)
        self.connect(self.pb, SIGNAL("clicked()"), lambda: self.button_click())
        self.connect(self.pb2, SIGNAL("clicked()"), lambda: self.button_close())
        self.setWindowTitle(self.pagetitle)

    
    def catItems(self, a, b):
        _a = a
        self.cas = self.pullCas(_a)
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
        
    
    def pullClasz(self):
        cn = Db()
        arr = cn.selectn('datas', '' , '', {'pubID': 11})
        return arr
    
    def pullClass(self, a):
        self.a = a
        cn = Db()
        students = cn.select('datas', '' , '', {'subID':self.a, 'active':0})
        arr = {}
        
        for j in students:
            arr[j[0]] = j[2]
        return arr
    
    def pullStudents(self, a):
        cn = Db()
        arr = cn.selectStudents(a)
        return arr
    
    def pullCas(self, a):
        _a = a
        cn = Db()
        arr = cn.selectn('datas', '' , '', {'subID': _a})
        return arr
    
    def button_close(self):
        self.reject()
        
    def button_click(self):
        students = self.getValue()
        session = self.session
        data =  StudentTable()
        data.classRemoveStudent(session, students[0])
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
    
    def pullSession(self, a):
        # select a file
        self.a = a
        g = Db()
        return  g.select('session', '', 1, {'id':self.a})

       