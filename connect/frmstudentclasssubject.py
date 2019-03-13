# -*- coding: utf-8 -*-
"""
Created on Thu Feb 21 08:18:56 2019

@author: CHARLES
"""
from PyQt4.QtCore import  Qt, SIGNAL, QDate
from PyQt4.QtGui import  QPlainTextEdit, QTreeWidgetItem, QTreeWidget, QWidget, QTextDocument, QTextCursor, QImage, QFileDialog, QFont, QPixmap, QTabWidget, QComboBox, QRadioButton, QDateEdit, QTextEdit, QCheckBox, QHBoxLayout, QGroupBox, QGridLayout, QDialog, QApplication, QPushButton, QLineEdit, QFormLayout, QLabel, QVBoxLayout, QSizePolicy
from connect import Db
from datetime import datetime
import time


class FormClassSubject(QDialog):
    
     def __init__(self, student, term, parent=None):
        super(FormClassSubject, self).__init__(parent)
        self.student = student
        self.term = term
        
        self.db_class = 'student_class'+str(self.term)
        self.db_subject = 'student_subject'+str(self.term)
        
        student = self.pullData('students', 1, {'id':self.student})
        term = self.pullData('terms', 1, {'id':self.term})
        session = self.pullData('session', 1 , {'id':term['sessionID']})
        subjects = self.pullData('datas', '' , {'pubID':3})
        student_class = self.pullData(self.db_class, 1 , {'studentID':self.student})
        student_subject = self.pullData(self.db_subject, '' , {'studentID':self.student})
        
        subjects_arr = self.convert_arr(student_subject)
        self.session = str(str(session['name'])+" "+str(term['name']+" Term")).title()
        self.fullname = str(str(student['surname'])+" "+str(student['firstname'])).title()
        
        fullnameLbl = QLabel(self.fullname)
        fullnameLbl.setFont(QFont("Candara", 14, QFont.Bold))
        termLbl = QLabel(self.session)
        termLbl.setFont(QFont("Candara", 12, QFont.Bold))
        classLbl = QLabel('Select Class')
        self.classCombo = QComboBox()
        pullClass = self.pullData('datas', '', {'pubID':1})
        self.class_arr = {}
        ko = 0
        for r in pullClass:
            pullClassUnit = self.pullData('datas', '', {'subID':r['id']})
            for f in pullClassUnit:
                self.classCombo.addItem(str(r['abbrv']).upper()+" "+str(f['abbrv']).upper())
                self.class_arr[ko] = f['id']
                ko += 1
                
        tree = QTreeWidget()
        tree.setHeaderLabel("Select Subjects")
        self.sub_arr = {}
        parent = QTreeWidgetItem(tree)
        parent.setText(0, "Subjects")
        parent.setFlags(parent.flags() | Qt.ItemIsTristate | Qt.ItemIsUserCheckable)
        if subjects and len(subjects) > 0:
            for val in subjects:
                child = QTreeWidgetItem(parent)
                child.setFlags(child.flags() | Qt.ItemIsUserCheckable)
                child.setText(0, str(val['name']).upper())
                self.sub_arr[val['id']] = child
                if int(val['id']) in subjects_arr:
                    child.setCheckState(0, Qt.Checked)
                else:
                    child.setCheckState(0, Qt.Unchecked)
                ko += 1
                
        tree1 = QTreeWidget()
        tree1.setHeaderLabel("Remove Subjects")
        self.sub1_arr = {}
        parent1 = QTreeWidgetItem(tree1)
        parent1.setText(0, "Subjects")
        parent1.setFlags(parent1.flags() | Qt.ItemIsTristate | Qt.ItemIsUserCheckable)
        
        if student_subject and len(student_subject) > 0:
            for val in student_subject:
                st_nam = self.pullData('datas', 1, {'id':val['subjectID']})
                child = QTreeWidgetItem(parent1)
                child.setFlags(child.flags() | Qt.ItemIsUserCheckable)
                child.setText(0, str(st_nam['name']).upper())
                self.sub1_arr[st_nam['id']] = child
                child.setCheckState(0, Qt.Checked)
                ko += 1
                
        h_box = QHBoxLayout()
        h_box.addWidget(classLbl)
        h_box.addWidget(self.classCombo)
        
        self.pb = QPushButton()
        self.pb.setObjectName("close")
        self.pb.setText("Close")
        
        self.pb1 = QPushButton()
        self.pb1.setObjectName("Submit")
        self.pb1.setText("Submit")
        
        self.connect(self.pb1, SIGNAL("clicked()"), lambda: self.button_click())
        self.connect(self.pb, SIGNAL("clicked()"), lambda: self.button_close())
        
        h_box1 = QHBoxLayout()
        h_box1.addWidget(self.pb)
        h_box1.addWidget(self.pb1)
        
        self.v_box = QVBoxLayout()
        self.v_box.addWidget(fullnameLbl)
        self.v_box.addWidget(termLbl)
        self.v_box.addLayout(h_box)
        self.v_box.addWidget(tree)
        self.v_box.addWidget(tree1)
        self.v_box.addLayout(h_box1)
        
        if student_class and student_class['classID'] > 0 :
            stID = self.class_arr.keys()[self.class_arr.values().index(student_class['classID'])]
            self.classCombo.setCurrentIndex(stID)
        
        self.setLayout(self.v_box)
        self.setWindowTitle("Class")
        
        
     def pullData(self, db, sid, arr):
         g = Db()
         data = g.selectn(db, '', sid, arr)
         return data
        
     def convert_arr(self, arr):
         ar = []
         for a in arr:
             ar.append(a['subjectID'])
                
         return ar
     
     def button_close(self):
         self.reject()
         
     def button_click(self):
         subject = self.getValue() 
         #clasz = self.classCombo.itemData(self.classCombo.currentIndex())
         clasz = self.class_arr[self.classCombo.currentIndex()]
         ## set class
         g = Db()
         sel = g.selectn(self.db_class, '', 1, {'studentID':self.student})
         
         if sel and sel['id'] > 0:
             if int(sel['classID']) == clasz:
                 pass
             else:
                g.update(self.db_class, {'classID':clasz} , {'id': sel['id']})
         else:
                g.insert(self.db_class, {'studentID':self.student, 'classID':clasz})
          
         if len(subject[0]) > 0:
             for a in subject[0]:
                sel = g.selectn(self.db_subject, '', 1, {'studentID':self.student, 'subjectID':a})
                if sel and int(sel['id']) > 0:
                    pass
                else:
                    g.insert(self.db_subject, {'studentID':self.student, 'subjectID':a})
                
         if len(subject[1]) > 0:
             for a in subject[1]:
                 g.delete(self.db_subject, {'studentID':self.student, 'subjectID':a})
            
         ## set subject
         self.accept()
         
     def getValue(self):
        k1 = []
        for i in self.sub_arr:
            if self.sub_arr[i].checkState(0) == Qt.Checked:
                k1.append(i)        
     
        k2 = []
        for i in self.sub1_arr:
            if self.sub1_arr[i].checkState(0) == Qt.Unchecked:
                k2.append(i)        
        return [k1, k2] 
    
    
class FormStudentMedical(QDialog):
    
     def __init__(self, student, term, edit=None, parent=None):
        super(FormStudentMedical, self).__init__(parent)
        self.student = student
        self.term = term
        
        self.db_class = 'student_class'+str(self.term)
        self.db_subject = 'student_subject'+str(self.term)
        
        student = self.pullData('students', 1, {'id':self.student})
        term = self.pullData('terms', 1, {'id':self.term})
        session = self.pullData('session', 1 , {'id':term['sessionID']})

        self.session = str(str(session['name'])+" "+str(term['name']+" Term")).title()
        self.fullname = str(str(student['surname'])+" "+str(student['firstname'])).title()
        self.sessionID = session['id']
        
        fullnameLbl = QLabel(self.fullname)
        fullnameLbl.setFont(QFont("Candara", 14, QFont.Bold))
        termLbl = QLabel(self.session)
        termLbl.setFont(QFont("Candara", 12, QFont.Bold))
        
        ailmentLbl = QLabel('Ailment/Allergies')
        treatmentLbl = QLabel('Treatment/Medication')
        self.ailmentData = QPlainTextEdit()
        self.treatmentData = QPlainTextEdit()
        
        self.pb = QPushButton()
        self.pb.setObjectName("close")
        self.pb.setText("Close")
        
        self.pb1 = QPushButton()
        self.pb1.setObjectName("Add")
        self.pb1.setText("Add")
        
        self.pb2 = QPushButton()
        self.pb2.setObjectName("Edit")
        self.pb2.setText("Edit")
        
        self.connect(self.pb1, SIGNAL("clicked()"), lambda: self.button_click())
        self.connect(self.pb2, SIGNAL("clicked()"), lambda: self.button_edit())
        self.connect(self.pb, SIGNAL("clicked()"), lambda: self.button_close())
        
        self.dateLbl = QLabel('Choose Date:')
        currentDate = QDate()
        self.dateData = QDateEdit()
        self.dateData.setDate(currentDate.currentDate())
        self.dateData.setCalendarPopup(True)
        
        h_box = QHBoxLayout()
        h_box.addWidget(self.dateLbl)
        h_box.addWidget(self.dateData)
        
        h_box1 = QHBoxLayout()
        h_box1.addWidget(self.pb)
        h_box1.addWidget(self.pb1)
        h_box1.addWidget(self.pb2)
        
        self.v_box = QVBoxLayout()
        self.v_box.addWidget(fullnameLbl)
        self.v_box.addWidget(termLbl)
        self.v_box.addLayout(h_box)
        self.v_box.addWidget(ailmentLbl)
        self.v_box.addWidget(self.ailmentData)
        self.v_box.addWidget(treatmentLbl)
        self.v_box.addWidget(self.treatmentData)
        self.v_box.addLayout(h_box1)
        
        if edit and len(edit) > 0:
            self.edit = edit
            self.editRow(edit)
            self.pb1.hide()
            self.pb2.show()
        else:
            self.edit = None
            self.pb1.show()
            self.pb2.hide()
              
        self.setLayout(self.v_box)
        self.setWindowTitle("Medical Report Form")
        
        
     def pullData(self, db, sid, arr):
         g = Db()
         data = g.selectn(db, '', sid, arr)
         return data
        
     def convert_arr(self, arr):
         ar = []
         for a in arr:
             ar.append(a['subjectID'])
                
         return ar
     
     def editRow(self, a):
         e = a.split('_')
         g = Db()
         self.mainrow = e[1]
         self.mainses = e[0]
         db = 'school_medicals'+str(e[0])
         data = g.selectn(db, '', 1, {'id':e[1]})
         if data and len(data) > 0: 
            self.ailmentData.clear()
            self.ailmentData.insertPlainText(str(data['ailment']))
            self.treatmentData.clear()
            self.treatmentData.insertPlainText(str(data['treatment']))
            
            
     def button_close(self):
         self.reject()
         
     def button_click(self):
         ailment = self.ailmentData.toPlainText()
         treatment = self.treatmentData.toPlainText()
         _date = self.dateData.date().toPyDate()
         _date = time.mktime(_date.timetuple())
    
         db = 'school_medicals'+str(self.sessionID)
         
         if len(ailment) > 0 and  len(treatment) > 0:
             arr ={}
             arr['studentID'] = self.student
             arr['ailment'] = ailment
             arr['treatment'] = treatment
             arr['datepaid'] = _date
             g = Db()
             g.insert(db, arr)
            
         ## set subject
         self.getValue()
         
     def button_edit(self):
         ailment = self.ailmentData.toPlainText()
         treatment = self.treatmentData.toPlainText()
         _date = self.dateData.date().toPyDate()
         _date = time.mktime(_date.timetuple())
    
         db = 'school_medicals'+str(self.mainses)
         
         if len(ailment) > 0 and  len(treatment) > 0:
             arr ={}
             arr['ailment'] = ailment
             arr['treatment'] = treatment
             arr['datepaid'] = _date
             g = Db()
             g.update(db, arr, {'id':self.mainrow})
            
         ## set subject
         self.getValue()

     def getValue(self):
        self.accept()
        
        
class FormStudentConduct(QDialog):
    
     def __init__(self, student, term, edit=None, parent=None):
        super(FormStudentConduct, self).__init__(parent)
        self.student = student
        self.term = term
        
        self.db_class = 'student_class'+str(self.term)
        self.db_subject = 'student_subject'+str(self.term)
        
        student = self.pullData('students', 1, {'id':self.student})
        term = self.pullData('terms', 1, {'id':self.term})
        session = self.pullData('session', 1 , {'id':term['sessionID']})

        self.session = str(str(session['name'])+" "+str(term['name']+" Term")).title()
        self.fullname = str(str(student['surname'])+" "+str(student['firstname'])).title()
        self.sessionID = session['id']
        
        fullnameLbl = QLabel(self.fullname)
        fullnameLbl.setFont(QFont("Candara", 14, QFont.Bold))
        termLbl = QLabel(self.session)
        termLbl.setFont(QFont("Candara", 12, QFont.Bold))
        
        actionLbl = QLabel('Action')
        reactionLbl = QLabel('Award/Prize etc.')
        issuerLbl = QLabel('Issuer')
        self.actionData = QPlainTextEdit()
        self.reactionData = QPlainTextEdit()
        self.staffData = QLineEdit()
        self.staffData.setPlaceholderText('Staff Name or  Deparment or Organisation')
        
        self.pb = QPushButton()
        self.pb.setObjectName("close")
        self.pb.setText("Close")
        
        self.pb1 = QPushButton()
        self.pb1.setObjectName("Add")
        self.pb1.setText("Add")
        
        self.pb2 = QPushButton()
        self.pb2.setObjectName("Edit")
        self.pb2.setText("Edit")
        
        self.connect(self.pb1, SIGNAL("clicked()"), lambda: self.button_click())
        self.connect(self.pb2, SIGNAL("clicked()"), lambda: self.button_edit())
        self.connect(self.pb, SIGNAL("clicked()"), lambda: self.button_close())
        
        self.dateLbl = QLabel('Choose Date:')
        currentDate = QDate()
        self.dateData = QDateEdit()
        self.dateData.setDate(currentDate.currentDate())
        self.dateData.setCalendarPopup(True)
        
        h_box = QHBoxLayout()
        h_box.addWidget(self.dateLbl)
        h_box.addWidget(self.dateData)
        
        h_box2 = QHBoxLayout()
        h_box2.addWidget(issuerLbl)
        h_box2.addWidget(self.staffData)
        
        h_box1 = QHBoxLayout()
        h_box1.addWidget(self.pb)
        h_box1.addWidget(self.pb1)
        h_box1.addWidget(self.pb2)
        
        self.v_box = QVBoxLayout()
        self.v_box.addWidget(fullnameLbl)
        self.v_box.addWidget(termLbl)
        self.v_box.addLayout(h_box)
        self.v_box.addWidget(actionLbl)
        self.v_box.addWidget(self.actionData)
        self.v_box.addWidget(reactionLbl)
        self.v_box.addWidget(self.reactionData)
        self.v_box.addLayout(h_box2)
        self.v_box.addLayout(h_box1)
        
        if edit and len(edit) > 0:
            self.edit = edit
            self.editRow(edit)
            self.pb1.hide()
            self.pb2.show()
        else:
            self.edit = None
            self.pb1.show()
            self.pb2.hide()
              
        self.setLayout(self.v_box)
        self.setWindowTitle("Conduct Report Form")
        
        
     def pullData(self, db, sid, arr):
         g = Db()
         data = g.selectn(db, '', sid, arr)
         return data
        
     def convert_arr(self, arr):
         ar = []
         for a in arr:
             ar.append(a['subjectID'])
                
         return ar
     
     def editrow(self, a):
        e = a.split('_')
        self.mainrow = e[1]
        self.mainses = e[0]
       
        g = Db()
        db = 'school_conducts'+str(self.mainses)
        data = g.selectn(db, '', 1, {'id':self.mainrow})
        if data and len(data) > 0: 
            self.ailmentData.clear()
            self.ailmentData.insertPlainText(str(data['ailment']))
            self.staffData.setText(str(data['staffname']))
            self.treatmentData.clear()
            self.treatmentData.insertPlainText(str(data['treatment']))   
            
     def button_close(self):
         self.reject()
         
     def button_click(self):
         action = self.actionData.toPlainText()
         reaction = self.reactionData.toPlainText()
         staff = self.staffData.text()
         _date = self.dateData.date().toPyDate()
         _date = time.mktime(_date.timetuple())
    
         db = 'school_conducts'+str(self.sessionID)
         
         if len(action) > 0 and  len(reaction) > 0:
             arr ={}
             arr['studentID'] = self.student
             arr['action'] = action
             arr['reaction'] = reaction
             arr['datepaid'] = _date
             arr['staffname'] = staff
             arr['state'] = 0
             g = Db()
             g.insert(db, arr)
            
         ## set subject
         self.getValue()
         
     def button_edit(self):
         action = self.actionData.toPlainText()
         reaction = self.reactionData.toPlainText()
         staff = self.staffData.text()
         _date = self.dateData.date().toPyDate()
         _date = time.mktime(_date.timetuple())
    
         db = 'school_conducts'+str(self.sessionID)
         
         if len(action) > 0 and  len(reaction) > 0:
             arr ={}
             arr['action'] = action
             arr['reaction'] = reaction
             arr['datepaid'] = _date
             arr['staffname'] = staff
             g = Db()
             g.update(db, arr, {'id':self.edit})
            
         ## set subject
         self.getValue()

     def getValue(self):
        self.accept()
        

class FormStudentMisconduct(QDialog):
    
     def __init__(self, student, term, edit=None, parent=None):
        super(FormStudentMisconduct, self).__init__(parent)
        self.student = student
        self.term = term
        
        self.db_class = 'student_class'+str(self.term)
        self.db_subject = 'student_subject'+str(self.term)
        
        student = self.pullData('students', 1, {'id':self.student})
        term = self.pullData('terms', 1, {'id':self.term})
        session = self.pullData('session', 1 , {'id':term['sessionID']})

        self.session = str(str(session['name'])+" "+str(term['name']+" Term")).title()
        self.fullname = str(str(student['surname'])+" "+str(student['firstname'])).title()
        self.sessionID = session['id']
        
        fullnameLbl = QLabel(self.fullname)
        fullnameLbl.setFont(QFont("Candara", 14, QFont.Bold))
        termLbl = QLabel(self.session)
        termLbl.setFont(QFont("Candara", 12, QFont.Bold))
        
        actionLbl = QLabel('Action')
        reactionLbl = QLabel('Corrective/Punitive Measure')
        issuerLbl = QLabel('Issuer')
        self.actionData = QPlainTextEdit()
        self.reactionData = QPlainTextEdit()
        self.staffData = QLineEdit()
        self.staffData.setPlaceholderText('Staff Name or  Deparment or Organisation')
        
        self.pb = QPushButton()
        self.pb.setObjectName("close")
        self.pb.setText("Close")
        
        self.pb1 = QPushButton()
        self.pb1.setObjectName("Add")
        self.pb1.setText("Add")
        
        self.pb2 = QPushButton()
        self.pb2.setObjectName("Edit")
        self.pb2.setText("Edit")
        
        self.connect(self.pb1, SIGNAL("clicked()"), lambda: self.button_click())
        self.connect(self.pb2, SIGNAL("clicked()"), lambda: self.button_edit())
        self.connect(self.pb, SIGNAL("clicked()"), lambda: self.button_close())
        
        self.dateLbl = QLabel('Choose Date:')
        currentDate = QDate()
        self.dateData = QDateEdit()
        self.dateData.setDate(currentDate.currentDate())
        self.dateData.setCalendarPopup(True)
        
        h_box = QHBoxLayout()
        h_box.addWidget(self.dateLbl)
        h_box.addWidget(self.dateData)
        
        h_box2 = QHBoxLayout()
        h_box2.addWidget(issuerLbl)
        h_box2.addWidget(self.staffData)
        
        h_box1 = QHBoxLayout()
        h_box1.addWidget(self.pb)
        h_box1.addWidget(self.pb1)
        h_box1.addWidget(self.pb2)
        
        self.v_box = QVBoxLayout()
        self.v_box.addWidget(fullnameLbl)
        self.v_box.addWidget(termLbl)
        self.v_box.addLayout(h_box)
        self.v_box.addWidget(actionLbl)
        self.v_box.addWidget(self.actionData)
        self.v_box.addWidget(reactionLbl)
        self.v_box.addWidget(self.reactionData)
        self.v_box.addLayout(h_box2)
        self.v_box.addLayout(h_box1)
        
        if edit and len(edit) > 0:
            self.edit = edit
            self.editRow(edit)
            self.pb1.hide()
            self.pb2.show()
        else:
            self.edit = None
            self.pb1.show()
            self.pb2.hide()
              
        self.setLayout(self.v_box)
        self.setWindowTitle("Misconduct Report Form")
        
        
     def pullData(self, db, sid, arr):
         g = Db()
         data = g.selectn(db, '', sid, arr)
         return data
        
     def convert_arr(self, arr):
         ar = []
         for a in arr:
             ar.append(a['subjectID'])
                
         return ar
     
     def editrow(self, a):
        e = a.split('_')
        g = Db()
        self.mainrow = e[1]
        self.mainses = e[0]
        db = 'school_conducts'+str(self.mainses)
        data = g.selectn(db, '', 1, {'id':self.mainrow})
        if data and len(data) > 0: 
            self.ailmentData.clear()
            self.ailmentData.insertPlainText(str(data['action']))
            self.staffData.setText(str(data['staffname']))
            self.treatmentData.clear()
            self.treatmentData.insertPlainText(str(data['reaction']))
            
            
     def button_close(self):
         self.reject()
         
     def button_click(self):
         action = self.actionData.toPlainText()
         reaction = self.reactionData.toPlainText()
         staff = self.staffData.text()
         _date = self.dateData.date().toPyDate()
         _date = time.mktime(_date.timetuple())
    
         db = 'school_conducts'+str(self.sessionID)
         
         if len(action) > 0 and  len(reaction) > 0:
             arr ={}
             arr['studentID'] = self.student
             arr['action'] = action
             arr['reaction'] = reaction
             arr['datepaid'] = _date
             arr['staffname'] = staff
             arr['state'] = 1
             g = Db()
             g.insert(db, arr)
            
         ## set subject
         self.getValue()
         
     def button_edit(self):
         action = self.actionData.toPlainText()
         reaction = self.reactionData.toPlainText()
         staff = self.staffData.text()
         _date = self.dateData.date().toPyDate()
         _date = time.mktime(_date.timetuple())
    
         db = 'school_conducts'+str(self.sessionID)
         
         if len(action) > 0 and  len(reaction) > 0:
             arr ={}
             arr['action'] = action
             arr['reaction'] = reaction
             arr['datepaid'] = _date
             arr['staffname'] = staff
             
             g = Db()
             g.update(db, arr, {'id':self.edit})
            
         ## set subject
         self.getValue()

     def getValue(self):
        self.accept()