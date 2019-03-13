from PyQt4.QtCore import SIGNAL, Qt, QEvent
from PyQt4.QtGui import QStyledItemDelegate, QStyleOptionButton, QStyle,  QComboBox, QTreeWidget, QTreeWidgetItem, QWidget, QFrame, QDateEdit, QRadioButton, QCheckBox, QHBoxLayout, QGroupBox, QGridLayout, QDialog, QApplication, QPushButton, QLineEdit, QFormLayout, QLabel, QVBoxLayout
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
        
        tree = QTreeWidget()
        tree.setHeaderLabel("Students?")
        self.std_arr = {}
        parent = QTreeWidgetItem(tree)
        parent.setText(0, "Selected Students")
        parent.setFlags(parent.flags() | Qt.ItemIsTristate | Qt.ItemIsUserCheckable)
        for student in self.students:
                child = QTreeWidgetItem(parent)
                child.setFlags(child.flags() | Qt.ItemIsUserCheckable)
                child.setText(0, str(student['surname']+' '+student['firstname']+' '+student['othername']).title())
                self.std_arr[student['id']] = child
                child.setCheckState(0, Qt.Checked)
                ko += 1
        
        hc1_box.addWidget(tree)
        
        
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
        
        self.pb1 = QPushButton()
        self.pb1.setObjectName("remclass")
        self.pb1.setText("Remove from Class")
        
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
        self.connect(self.pb1, SIGNAL("clicked()"), lambda: self.button_remove())
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
        
    def button_remove(self):
        students = self.getValues()
        session = self.session
        data =  StudentTable()
        data.classRemoveStudent(session, students)
        self.accept()
        
    def button_click(self):
        students = self.getValue()
        moveclass = self.d_displayData.itemData(self.d_displayData.currentIndex())
        session = self.session
        data =  StudentTable()
        data.classMoveStudent(session, moveclass, students)
        self.accept()
        
    def getValue(self):
        k1 = []
        for i in self.std_arr:
            if self.std_arr[i].checkState(0) == Qt.Checked:
                k1.append(i)
                 
        return k1 
    
    def getValues(self):
        
        k1 = []
        for i in self.std_arr:
            if self.std_arr[i].checkState(0) == Qt.Checked:
                k1.append(i)
                 
        return k1 
    
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

   
class SubjectClassDialog(QDialog):
    pagetitle = 'Change Class'
    holdc = {}
    hold  = []
    def __init__(self, session, students, parent=None):
        super(SubjectClassDialog, self).__init__(parent)
        
        ko = 0
        self.students = self.pullStudents(students)
        self.session = session[2]
        self.frame1 = QGroupBox('Set Student Subjects')
        
        hc1_box = QVBoxLayout()
        ses_name = str(session[1])+' '+str(session[3]+' Term')
        ses = QLabel(ses_name)
        
        
        tree = QTreeWidget()
        tree.setHeaderLabel("Students?")
        self.std_arr = {}
        parent = QTreeWidgetItem(tree)
        parent.setText(0, "Selected Students")
        parent.setFlags(parent.flags() | Qt.ItemIsTristate | Qt.ItemIsUserCheckable)
        for student in self.students:
                child = QTreeWidgetItem(parent)
                child.setFlags(child.flags() | Qt.ItemIsUserCheckable)
                child.setText(0, str(student['surname']+' '+student['firstname']+' '+student['othername']).title())
                self.std_arr[student['id']] = child
                child.setCheckState(0, Qt.Checked)
                ko += 1
        
        tree1 = QTreeWidget()
        tree1.setHeaderLabel("Subjects?")
        self.sub_arr = {}
        parent1 = QTreeWidgetItem(tree1)
        parent1.setText(0, "Selected Subjects")
        parent1.setFlags(parent.flags() | Qt.ItemIsTristate | Qt.ItemIsUserCheckable)
        arr = self.pullSubject()
        for v in arr:
                child = QTreeWidgetItem(parent1)
                child.setFlags(child.flags() | Qt.ItemIsUserCheckable)
                child.setText(0, str(v['name']).upper())
                self.sub_arr[v['id']] = child
                child.setCheckState(0, Qt.Unchecked)
                ko += 1
        
        
        hc1_box.addWidget(ses)
        hc1_box.addWidget(tree)
        hc1_box.addWidget(tree1)
           
        
        self.frame1.setLayout(hc1_box)
        
        self.pb = QPushButton()
        self.pb.setObjectName("setsub")
        self.pb.setText("Set Subject") 
        
        self.pb1 = QPushButton()
        self.pb1.setObjectName("remsub")
        self.pb1.setText("Remove Subject")
        
        self.pb2 = QPushButton()
        self.pb2.setObjectName("Cancel")
        self.pb2.setText("Cancel")
        
        but_box = QHBoxLayout()
        but_box.addWidget(self.pb2)
        but_box.addWidget(self.pb1)
        but_box.addWidget(self.pb)
        
        main_box = QVBoxLayout()
        main_box.addWidget(self.frame1)
        main_box.addLayout(but_box)
        
        self.setLayout(main_box)
        self.connect(self.pb, SIGNAL("clicked()"), lambda: self.button_click())
        self.connect(self.pb1, SIGNAL("clicked()"), lambda: self.button_remove())
        self.connect(self.pb2, SIGNAL("clicked()"), lambda: self.button_close())
        self.setWindowTitle(self.pagetitle)
    
    def pullClasz(self):
        cn = Db()
        arr = cn.selectn('datas', '' , '', {'pubID': 11})
        return arr
    
    def pullSubject(self):
        cn = Db()
        arr = cn.selectn('datas', '' , '', {'pubID': 3, 'active':0})
        return arr
    
    def pullStudents(self, a):
        cn = Db()
        arr = cn.selectStudents(a)
        return arr
    
    def button_close(self):
        self.reject()
        
    def button_click(self):
        self.pb2.setText("Please Wait..")
        self.pb1.setEnabled(False)
        self.getValue()
        self.accept()
        
    def button_remove(self):
        self.pb1.setText("Please Wait..")
        self.pb2.setEnabled(False)
        self.getValue()
        self.accept()
        
    def getValue(self):
        k1 = []
        k2 = []
        for i in self.std_arr:
            if self.std_arr[i].checkState(0) == Qt.Checked:
                k1.append(i)
                 
        for i in self.sub_arr:
            if self.sub_arr[i].checkState(0) == Qt.Checked:
                k2.append(i)
        
        self.setSubject(k1, k2)
        
    def setSubject(self, a, b):
        session = self.session
        db = 'student_subject'+str(session)
        g = Db()
        for i in a:
            for j in b:
                f = g.selectn(db, '', 1, {'studentID':i, 'subjectID':j})
                if f and f['id'] > 0:
                    pass
                else:
                    g.insert(db, {'studentID':i, 'subjectID':j})
                
    def removeSubject(self, a, b):
        session = self.session
        db = 'student_subject'+str(session)
        g = Db()
        for i in a:
            for j in b:
                f = g.selectn(db, '', 1, {'studentID':i, 'subjectID':j})
                if f and f['id'] > 0:
                    g.delete(db, {'id':f['id']})   
    
    def pullSession(self, a):
        # select a file
        self.a = a
        g = Db()
        return  g.select('session', '', 1, {'id':self.a})



    