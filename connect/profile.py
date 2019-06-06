# -*- coding: utf-8 -*-
"""
Created on Sat Nov 17 05:44:29 2018

@author: CHARLES
"""
from PyQt4.QtCore import SIGNAL, QDate, Qt, QSize
from PyQt4.QtGui import  QPrintPreviewDialog, QLayout, QScrollArea, QMenuBar, QAction, QStackedWidget, QFont, QWidget, QSplitter, QFileDialog, QPixmap, QTabWidget, QComboBox, QRadioButton, QDateEdit, QTextEdit, QCheckBox, QHBoxLayout, QGroupBox, QGridLayout, QDialog, QApplication, QPushButton, QLineEdit, QFormLayout, QLabel, QVBoxLayout, QSizePolicy
from connect import Db
from connectstudents import Con
from datetime import datetime
from validate import Arrayz, Headers
from studenttable import StudentTable
#import datetime
import jinja2
from dateutil.relativedelta import relativedelta
import math
import numpy as np
from PIL import Image
from PIL.ImageQt import ImageQt
import os
import sys
import pandas as pd

class Profile():
    loader = jinja2.FileSystemLoader('/tmp')
    env = jinja2.Environment(autoescape=True, loader = loader)
    def datetimeformat(a, b):
        return a.strftime(b)
    
    def timestamp_to_time(a):
        try:
            return datetime.utcfromtimestamp(int(float(a))).strftime('%a, %B %d')
        except:
            return None
    
    env.filters['datetimeformat']  = datetimeformat
    env.filters['timestamp_to_time']  = timestamp_to_time
    
    def lunchPrintForm(self, a):
        self.item = a
        self.lunchPrintPreview()
        #form.exec_()
        
    def handlePaintRequest(self, printer):
        document = self.doc1
        if document != None:
            document.print_(printer)
            
    def lunchPrintPreview(self):
        dialog = QPrintPreviewDialog()
        dialog.paintRequested.connect(self.handlePaintRequest)
        dialog.exec_()
        
    def menuUiz(self):
        
        mainMenu = QMenuBar()
        
        fileMenu = mainMenu.addMenu('&File')
        exitMenu = QAction('&Exit', self)
        exitMenu.setShortcut('CTRL+Q')
        exitMenu.setStatusTip('Close Dialog')
        exitMenu.triggered.connect(self.lunchUnitForm)
        fileMenu.addAction(exitMenu)
    
        #settings menu
        ViewMenu = mainMenu.addMenu('&Veiws')
        bioMenu = QAction('Biodata', self)
        bioMenu.setStatusTip('Bio and Contact data')
        bioMenu.triggered.connect(lambda state, x = 1, y = 'k': self.lunchReport(x, y))
        ViewMenu.addAction(bioMenu)
        
#        feeMenu =  ViewMenu.addMenu('Fees')
#        dumpClass4 = {}
#        for k in self.myterms:
#           act = str(self.myterms[k])
#           stud = QAction(act, self)
#           dumpClass4[k] = stud
#           stud.triggered.connect(lambda state, x = 5, y = k: self.lunchReport(x, y))
#           feeMenu.addAction(stud)
        
        
        printMenu = mainMenu.addMenu('&Print')
        exitMenu1 = QAction('&Exit', self)
        exitMenu1.setShortcut('CTRL+Q')
        exitMenu1.setStatusTip('Close Dialog')
        exitMenu1.triggered.connect(lambda state, x = 1:self.lunchPrintForm(x))
        printMenu.addAction(exitMenu1)
        #printMenu.triggered.connect(lambda state, x = 1:self.lunchPrintForm(x))
        

        return mainMenu
        
    def getSex(self, a):
        if a == 0:
            self.gender = 'Male'
        elif a == 1:
            self.gender = 'Female'
        else:
            self.gender = 'None Stated'
    
    def getDate(self, a):
        now = datetime.today()
        
        dob = a
        try:
            dt = datetime.strptime(dob, '%d/%m/%Y').date()
        except:
            dt = datetime.today()
            
        dt1 = now.date()
        try:
          diff = (dt1 - dt).days 
        except:
          diff = 10000   
        age1 = int(diff)/365.25
        agey = round(int(diff)/365.25, 0)
        agem = age1 - agey
        months = round(agem * 12)
        dob = "{:%d, %b %Y}".format(dt)
        age = str(math.floor(agey))+' yrs '+str(math.floor(months))+' months '
        
        return [dob, age]
    
    def student(self, a, title,  b = None):
        g = Db()
        
        self.data = g.selectn('students', '', 1, {'id':a}) 
        self.getSex(self.data['gender'])
        dob = self.getDate(self.data['dob'])
        adm = self.getDate(self.data['admit'])
        self.dob = dob[0]
        self.age = dob[1]
        self.adm = adm[0]
        
        try:
            empno = str(self.data['empno']).upper()
        except:
            empno = ''
        try:
            title = str(self.data['title'])
        except:
            title= ''
        try:
            surname = str(self.data['surname']).title()
        except:
            surname = ''
        try:
            firstname = str(self.data['firstname']).title()
        except:
            firstname = ''
        try:
            middlename = str(self.data['othername']).title()
        except:
            middlename = ''
        
        self.fullname = empno+" "+title +" "+surname+" "+firstname+" "+middlename
           
        try:
            dob = self.getDate(self.data['dob'])
        except:
            dob = None
        try:
            adm = self.getDate(self.data['admit'])
        except:
            adm = None
        try:
            dol = self.getDate(self.data['dol'])[0]
        except:
            dol = None
        
        try:
            if os.path.isfile('pic_main/'+str(self.data['pix'])):
                    image1 = 'pic_main/'+str(self.data['pix'])
            else:
                    image1 = 'img/stdpic.png'
        except:
            image1 = 'img/stdpic.png'
        try:
            if os.path.isfile('pic_main/'+str(self.data['g1pix'])):
                    image2 = 'pic_main/'+str(self.data['g1pix'])
            else:
                    image2 = 'img/stdpic.png'
        except:
            image2 = 'img/stdpic.png'
        
        try:
            if os.path.isfile('pic_main/'+str(self.data['g2pix'])):
                    image3 = 'pic_main/'+str(self.data['g2pix'])
            else:
                    image3 = 'img/stdpic.png'
        except:
            image3 = 'img/stdpic.png'
        
        self.file = {}
        try:
            self.file['gender'] = Arrayz().arrayz(5)[int(self.data['gender'])]
        except:
            self.file['gender'] = 'None'
        try:
            self.file['photo'] = image1
        except:
            self.file['photo']  = ''
            
        try:
            self.file['photo1'] = image2
        except:
            self.file['photo1']  = ''
        try:
            self.file['photo2'] = image3
        except:
            self.file['photo2']  = ''
        try:
            self.file['dob'] = dob[0]
        except:
            self.file['dob']  = ''
        try:
            self.file['dol'] = dol
        except:
            self.file['dol']  = ''
        try:
            self.file['age'] = dob[1]
        except:
            self.file['age']  = ''
        try:
            self.file['adm'] = adm[0]
        except:
            self.file['adn']  = ''
        try:
            self.file['empyrs'] = adm[1]
        except:
            self.file['empyrs']  = ''
        try: 
            department = g.selectn('datas', '', 1, {'id':self.data['department']})
            self.file['dep'] = department['name']
        except:
            self.file['dep']  = None
        try:
            unit = g.selectn('datas', '', 1, {'id':self.data['unit']})
            self.file['unit'] = unit['name']
        except:
            self.file['unit']  = None
        try:
            bank = g.selectn('datas', '', 1, {'id':self.data['bank']})
            self.file['bank'] = bank['name']
        except:
            self.file['bank']  = None
        try:
            pension = g.selectn('datas', '', 1, {'id':self.data['pension']})
            self.file['pen'] = pension['name']
        except:
            self.file['pen']  = None
       
        try:
            self.file['access'] = Arrayz().arrayz(2)[int(self.data['access'])]
        except:
            self.file['access'] = 'None'
        try:
            self.file['reason'] = Arrayz().arrayz(4)[int(self.data['reason'])]
        except:
            self.file['reason'] = 'None'
        try:
            self.file['reasonid'] = int(self.data['reason'])
        except:
            self.file['reasonid'] = 0
        try:
            self.file['religion'] = Arrayz().arrayz(7)[int(self.data['religion'])]
        except:
            self.file['religion'] = 'None'
            
        
        aca  = g.selectn('stafffile', '', '', {'state':1, 'staffID':a})
        pro  = g.selectn('stafffile', '', '', {'state':2, 'staffID':a})
        wrk  = g.selectn('stafffile', '', '', {'state':3, 'staffID':a})
        tra  = g.selectn('stafffile', '', '', {'state':4, 'staffID':a})
        dis  = g.selectn('stafffile', '', '', {'state':5, 'staffID':a})
        com  = g.selectn('stafffile', '', '', {'state':6, 'staffID':a})
        dut  = g.selectn('stafffile', '', '', {'state':7, 'staffID':a})
        
        
        
        
        
        
        ret = self.studentProfile()
        return ret
    
    def staff(self, a, title,  b = None):
        g = Db()
        if b:
            pass
        else:
            b = [1,2,3,4,5,6,7,8,9,10]
            
        self.selections = b
        self.data = g.selectn('staffs', '', 1, {'id':a}) 
        
        try:
            empno = str(self.data['empno']).upper()
        except:
            empno = ''
        try:
            title = str(self.data['title'])
        except:
            title= ''
        try:
            surname = str(self.data['surname']).title()
        except:
            surname = ''
        try:
            firstname = str(self.data['firstname']).title()
        except:
            firstname = ''
        try:
            middlename = str(self.data['othername']).title()
        except:
            middlename = ''
        
        self.fullname = empno+" "+title +" "+surname+" "+firstname+" "+middlename
           
        try:
            dob = self.getDate(self.data['dob'])
        except:
            dob = None
        try:
            adm = self.getDate(self.data['admit'])
        except:
            adm = None
        try:
            dol = self.getDate(self.data['dol'])[0]
        except:
            dol = None
        
        try:
            if os.path.isfile('pic_main/'+str(self.data['pix'])):
                    image1 = 'pic_main/'+str(self.data['pix'])
            else:
                    image1 = 'img/stdpic.png'
        except:
            image1 = 'img/stdpic.png'
        try:
            if os.path.isfile('pic_main/'+str(self.data['g1pix'])):
                    image2 = 'pic_main/'+str(self.data['g1pix'])
            else:
                    image2 = 'img/stdpic.png'
        except:
            image2 = 'img/stdpic.png'
        
        try:
            if os.path.isfile('pic_main/'+str(self.data['g2pix'])):
                    image3 = 'pic_main/'+str(self.data['g2pix'])
            else:
                    image3 = 'img/stdpic.png'
        except:
            image3 = 'img/stdpic.png'
        
        self.file = {}
        try:
            self.file['gender'] = Arrayz().arrayz(5)[int(self.data['gender'])]
        except:
            self.file['gender'] = 'None'
        try:
            self.file['photo'] = image1
        except:
            self.file['photo']  = ''
            
        try:
            self.file['photo1'] = image2
        except:
            self.file['photo1']  = ''
        try:
            self.file['photo2'] = image3
        except:
            self.file['photo2']  = ''
        try:
            self.file['dob'] = dob[0]
        except:
            self.file['dob']  = ''
        try:
            self.file['dol'] = dol
        except:
            self.file['dol']  = ''
        try:
            self.file['age'] = dob[1]
        except:
            self.file['age']  = ''
        try:
            self.file['emp'] = adm[0]
        except:
            self.file['emp']  = ''
        try:
            self.file['empyrs'] = adm[1]
        except:
            self.file['empyrs']  = ''
        try: 
            department = g.selectn('datas', '', 1, {'id':self.data['department']})
            self.file['dep'] = department['name']
        except:
            self.file['dep']  = None
        try:
            unit = g.selectn('datas', '', 1, {'id':self.data['unit']})
            self.file['unit'] = unit['name']
        except:
            self.file['unit']  = None
        try:
            bank = g.selectn('datas', '', 1, {'id':self.data['bank']})
            self.file['bank'] = bank['name']
        except:
            self.file['bank']  = None
        try:
            pension = g.selectn('datas', '', 1, {'id':self.data['pension']})
            self.file['pen'] = pension['name']
        except:
            self.file['pen']  = None
        try:
            health = g.selectn('datas', '', 1, {'id':self.data['health']})
            self.file['health'] = health['name']
        except:
            self.file['health']  = None
        try:
            self.file['access'] = Arrayz().arrayz(2)[int(self.data['access'])]
        except:
            self.file['access'] = 'None'
        try:
            self.file['reason'] = Arrayz().arrayz(4)[int(self.data['reason'])]
        except:
            self.file['reason'] = 'None'
        try:
            self.file['reasonid'] = int(self.data['reason'])
        except:
            self.file['reasonid'] = 0
        try:
            self.file['religion'] = Arrayz().arrayz(7)[int(self.data['religion'])]
        except:
            self.file['religion'] = 'None'
            
        try:
            self.file['marital'] = Arrayz().arrayz(6)[int(self.data['marital'])]
        except:
            self.file['marital'] = 'None'
        
        try:
            self.file['user'] = Arrayz().arrayz(2)[int(self.data['user'])]
        except:
            self.file['user'] = 'None'
        
        aca  = g.selectn('stafffile', '', '', {'state':1, 'staffID':a})
        pro  = g.selectn('stafffile', '', '', {'state':2, 'staffID':a})
        wrk  = g.selectn('stafffile', '', '', {'state':3, 'staffID':a})
        tra  = g.selectn('stafffile', '', '', {'state':4, 'staffID':a})
        dis  = g.selectn('stafffile', '', '', {'state':5, 'staffID':a})
        com  = g.selectn('stafffile', '', '', {'state':6, 'staffID':a})
        dut  = g.selectn('stafffile', '', '', {'state':7, 'staffID':a})
        
        self.filez = {}
        self.filez[1] = aca
        self.filez[2] = pro
        self.filez[3] = wrk
        self.filez[4] = tra
        self.filez[5] = dis
        self.filez[6] = com
        self.filez[7] = dut
        
        ret = self.staffProfile()
        return ret
    
    
    def classPull(self, semester, state, studentsID, allStudents):
        g = Db()
        if state == 1:
            student_ca = g.selectStudentsCa(semester, studentsID)
        elif state == 2:
            student_ca = g.selectStudentsAffective(semester, studentsID)
        elif state == 3:
            student_ca = g.selectStudentsPsychomoto(semester, studentsID)  
            
        arr = {}
        for g in allStudents:
            arr[int(g['id'])] = {}
            arr[int(g['id'])]['matric'] = g['schno']
            arr[int(g['id'])]['name'] = str(str(g['surname'])+' '+str(g['firstname'])+' '+str(g['othername'])).title()
            arr[int(g['id'])]['classunit'] = str(str(g['classname'])+''+str(g['classunitname'])).upper()
            arr[int(g['id'])]['sco'] = {}
                    
        ca_list = []
        sub_list = []
        for s in student_ca:
            sub_list.append(s['subjectID'])
            ca_list.append(s['caID'])
            if s['studentID'] and int(s['studentID']):
                if 'sco' in arr[int(s['studentID'])]:
                    pass
                else:
                  arr[int(s['studentID'])]['sco'] = {}
                
                try:
                    if s['subjectID'] in arr[int(s['studentID'])]['sco']:
                        pass
                    else:
                      arr[int(s['studentID'])]['sco'][s['subjectID']] = {}
                except:
                    pass
             
            try:
                if s['caID'] in arr[int(s['studentID'])]['sco'][s['subjectID']]:
                    pass
                else:
                  arr[int(s['studentID'])]['sco'][s['subjectID']][s['caID']] = s['score']
            except:
                pass
            
             
        assessments = list(set(ca_list))
        subjects = list(set(sub_list))
       
        cn = Db()
        #subjects
        #get the subjects names
        #store in a dictionary
        self.store_sub_name = {}
        for subz in subjects:
            sub_name = None
            sub_name = cn.selectn('datas','', 1, {'id':subz})
            if sub_name:
                self.store_sub_name.update({int(subz):sub_name['abbrv']})
        
        
        cn = Db()
        #assessments 
        #get assessments name
        #store in a dictionary
        self.store_ca_name = {}
        if state == 1:
            for caz in assessments:
                if caz:
                    ca_name = None
                    ca_names = cn.selectn('datas', '', 1, {'id':caz})
                    ca_name = cn.selectn('datas', '', 1, {'id':ca_names['name']})
                    if ca_name and caz:
                        self.store_ca_name.update({int(caz):ca_name['abbrv']})
        else:
            for caz in assessments:
                if caz:
                    ca_name = None
                    ca_name = cn.selectn('datas', '', 1, {'id':caz})
                    if ca_name and caz:
                        self.store_ca_name.update({int(caz):ca_name['abbrv']})                
                        
        #assements max score
        #get assements maximum scores
        #store them in a dictionary
        self.store_ca_max ={}
        if state == 1:
            for cazn in assessments:
                ca_name = None
                ca_name = cn.selectn('datas', '', 1, {'id':cazn})
                try:
                    if ca_name:
                        self.store_ca_max.update({int(cazn):float(ca_name['abbrv'])})
                    else:
                        self.store_ca_max.update({int(cazn):0})
                except:
                    self.store_ca_max.update({int(cazn):0})
        else:
            for cazn in assessments:
                if cazn:
                    try:
                        if ca_name:
                            self.store_ca_max.update({int(cazn):10})
                        else:
                            self.store_ca_max.update({int(cazn):0})
                    except:
                        self.store_ca_max.update({int(cazn):0})
        
        
        for r in arr:
            for s in subjects:
                if s in arr[r]['sco']:
                    for a in assessments:
                        if a in arr[r]['sco'][s]:
                            arr[r]['sco'][s][a] = round(arr[r]['sco'][s][a] * self.store_ca_max[a])
        
        self.body = arr
        self.fullname = ''
        ret = self.classAcademicsProfile()
        
        return ret
    
    def classPullData(self, semester, state, group, studentsID, allStudents):
        student_re = {}
        student_tag = ''
        #Get data
        if group == 1:
            student_re = self.getStudentAssessments(semester, studentsID)
            student_tag = 'subjectID'
        elif group == 2:
            student_re = self.getStudentAffective(semester, studentsID)
            student_tag = 'caID'
        elif group == 3:
            student_re = self.getStudentPsychomoto(semester, studentsID)
            student_tag = 'caID'
        else:
            student_re = {}
            student_tag = ''
         
            
        #set arrays
        arr = {}
        arrr = {}
        sub_list = []
        sub_list2 = []
        #set students pre data
        for g in allStudents:
            arr[int(g['id'])] = {}
            arr[int(g['id'])]['matric'] = g['schno']
            arr[int(g['id'])]['name'] = str(str(g['surname'])+' '+str(g['firstname'])+' '+str(g['othername'])).title()
            arr[int(g['id'])]['classunit'] = str(str(g['classname'])+''+str(g['classunitname'])).upper()
            arr[int(g['id'])]['sco'] = {}
            arrr[int(g['id'])] = {}        
        
        
        for s in student_re:
            sub_list.append(s[student_tag])
            if s['studentID']:
                if 'sco' in arr[int(s['studentID'])]:
                    pass
                else:
                  arr[int(s['studentID'])]['sco'] = {}
                
                try:
                    if s[student_tag] in arr[int(s['studentID'])]['sco']:
                        pass
                    else:
                      arr[int(s['studentID'])]['sco'][s[student_tag]] = s['score']
                except:
                    pass
         
        
        for s in student_re:
            sub_list2.append(s[student_tag])
            try:
                if s[student_tag] in arrr[int(s['studentID'])]:
                    pass
                else:
                  arrr[int(s['studentID'])][s[student_tag]] = s['score']
            except:
                pass
        
        
        subjects = list(set(sub_list))
        cn = Db()
        #subjects
        #get the subjects names
        #store in a dictionary
        self.store_sub_name = {}
        for subz in subjects:
            sub_name = None
            sub_name = cn.selectn('datas','', 1, {'id':subz})
            if sub_name:
                self.store_sub_name.update({int(subz):sub_name['name']})
        
        self.store_ca_name = {}
        self.store_ca_max = {}
        for r in arr:
            for s in subjects:
                if s in arr[r]['sco']:
                    try:
                        arr[r]['sco'][s] = round(arr[r]['sco'][s] * 100)
                    except:
                        pass
                    try:
                        arrr[int(r)][s] = round(arrr[r][s] * 100)
                    except:
                        pass
    
        #self.classAcademics()
        if state == 1:
            self.body = arr
            self.fullname = ''
            ret = self.classAcademicsSumProfile()
        if state == 2:
            self.body = arr
            self.fullname = ''
            self.header = Headers().analize()
            df = pd.DataFrame.from_dict(arrr,  orient='index')
            dt1 = df.transpose()
            dt = dt1.describe()
            df['sum'] = dt1.sum()
            dt = dt.transpose()
            dp = dt.join(df['sum'])
            dt = dp.to_dict('index')
            dt = {int(k): v for k,v in dt.items()}
            details = {arr[k]['name']: v for k, v in dt.items()}
            self.body1 = dt
            #dg = dp.plot.bar(stacked=True)
            #dg = dg[0].get_figure()
            #dg.save_figure('tmp/fig1.png')
            self.graph = 'tmp/fig1.png'
            ret = self.classAcademicsStudentProfile()
        if state == 3:
            self.body = arr
            self.fullname = ''
            self.header = Headers().analize()
            df = pd.DataFrame.from_dict(arrr,  orient='index')
            dt = df.describe()
            dp = dt.transpose()
            dt = dp.to_dict('index')
            dt = {int(k): v for k, v in dt.items()}
            details = {self.store_sub_name[k]: v for k, v in dt.items()}
            gd = pd.DataFrame.from_dict(details,  orient='index')
            #take data attache value
            self.graph = 'tmp/fig1.png'
            self.body1 = dt
            #dg = dp.plot.bar()
            #dg = dg[0].get_figure()
            #dg.save_figure('img/fig1.png')
            self.graph = 'img/fig1.png'
            ret = self.classAcademicsSubjectProfile()
        return ret
                    
    def classItems(self, clas, num, semester, items = None, sub_titles = None, columns = None):
        raw_students = {}
        allFees = {}
        allPays = {}
        allSubjects = {}
        allStudents = {}
        arr = {}
        if num == 0 or num == 1:
            if num == 0:
                cn = StudentTable(semester, [None] , [clas],  [None])
                raw_students = cn.classStudent()
            elif num == 1:
                cn = StudentTable(semester, [None] , [None], [clas])
                raw_students = cn.classUnitStudent()
            
            
            c = {}   
            try:
                semester_title = self.getSemester
            except:
                semester_title = ''
            
            if sub_titles:
               sub_titles = sub_titles
            else:
               sub_titles = ''
               
            if cn:
                if items == 1:
                    title = semester_title+' '+sub_titles+' '+' Fees'
                    dat = cn.classUnitStudentFeeDetails(raw_students)
                    allStudents = dat[0]
                    allFees = dat[1]
                    arr = Headers().headers(items)
                if items == 2:
                    title = semester_title+' '+sub_titles+' '+' Payments'
                    dat = cn.classUnitStudentPayDetails(raw_students)
                    allStudents = dat[0]
                    allPays = dat[1]
                    arr = Headers().headers(items)
                if items == 3:
                    title = semester_title+' '+sub_titles+' '+' Balance'
                    dat = cn.classUnitStudentFee(raw_students)
                    allStudents = dat[0]
                    allPays = dat[1]
                    allFees = dat[2]
                    arr = Headers().headers(items)
                if items == 4:
                    title = semester_title+' '+sub_titles+' '+' Subjects'
                    dat = cn.classStudentSubject(raw_students)
                    allStudents = dat[0]
                    allSubjects = dat[1]
                    arr = Headers().headers(items)
                if items == 5:
                    title = semester_title+' '+sub_titles+' '+'Academic  Details'
                    studentsID = cn.getIDs(raw_students)
                    dat = self.classPull(semester, 1, studentsID, raw_students )
                    return dat
                if items == 6:
                    title = semester_title+' '+sub_titles+' '+'Academic Summary'
                    studentsID = cn.getIDs(raw_students)
                    dat = self.classPullData(semester, 1, 1, studentsID, raw_students )
                    return dat
                if items == 7:
                    title = semester_title+' '+sub_titles+' '+'Students Academic Analysis'
                    studentsID = cn.getIDs(raw_students)
                    dat = self.classPullData(semester, 2, 1, studentsID, raw_students )
                    return dat
                if items == 8:
                    title = semester_title+' '+sub_titles+' '+'Subject Analysis'
                    studentsID = cn.getIDs(raw_students)
                    dat = self.classPullData(semester, 3, 1, studentsID, raw_students )
                    return dat
                if items == 9:
                    title = semester_title+' '+sub_titles+' '+'Affective  Details'
                    studentsID = cn.getIDs(raw_students)
                    dat = self.classPull(semester, 2, studentsID, raw_students )
                    return dat
                if items == 10:
                    title = semester_title+' '+sub_titles+' '+'Affective Summary'
                    studentsID = cn.getIDs(raw_students)
                    dat = self.classPullData(semester, 1, 2, studentsID, raw_students )
                    return dat
                if items == 11:
                    title = semester_title+' '+sub_titles+' '+'Students Attitude Analysis'
                    studentsID = cn.getIDs(raw_students)
                    dat = self.classPullData(semester, 2, 2, studentsID, raw_students )
                    return dat
                if items == 12:
                    title = semester_title+' '+sub_titles+' '+'Attitude Analysis'
                    studentsID = cn.getIDs(raw_students)
                    dat = self.classPullData(semester, 3, 2, studentsID, raw_students )
                    return dat
                if items == 13:
                    title = semester_title+' '+sub_titles+' '+'Psychomoto  Details'
                    studentsID = cn.getIDs(raw_students)
                    dat = self.classPull(semester, 3, studentsID, raw_students )
                    return dat
                if items == 14:
                    title = semester_title+' '+sub_titles+' '+'Psychomoto Summary'
                    studentsID = cn.getIDs(raw_students)
                    dat = self.classPullData(semester, 1, 3, studentsID, raw_students )
                    return dat
                if items == 15:
                    title = semester_title+' '+sub_titles+' '+'Students Skills Analysis'
                    studentsID = cn.getIDs(raw_students)
                    dat = self.classPullData(semester, 2, 3, studentsID, raw_students )
                    return dat
                if items == 16:
                    title = semester_title+' '+sub_titles+' '+'Skills Analysis'
                    studentsID = cn.getIDs(raw_students)
                    dat = self.classPullData(semester, 3, 3, studentsID, raw_students )
                    return dat


                if items <  5:    
                    students = {}
                    for g in allStudents:
                        students[g['id']] = {}
                        students[g['id']]['matric'] = g['schno']
                        students[g['id']]['name'] = str(str(g['surname'])+' '+str(g['firstname'])+' '+str(g['othername'])).title()
                        students[g['id']]['classunit'] = str(str(g['classname'])+''+str(g['classunitname'])).upper()
                        
                    try:
                        if allSubjects:
                            for g in allSubjects:
                                students[int(g['studentID'])]['subjects'] = str(g['subjects']).upper()      
                    except:
                        pass
                            
                    if allPays:
                        for g in allPays:
                            students[int(g['studentID'])]['pay'] = g['amount']
                    
                    try:
                        if allFees:
                            for g in allFees:
                                students[int(g['studentID'])]['fee'] = g['amount']
                    except:
                        pass
                    
                    #print(students)
                    try:
                        if allFees or allPays:
                            for g in students:
                                try:
                                  fees = float(students[g]['fees'])
                                except:
                                  fees = 0.0 
                                try:
                                  pays = float(students[g]['pay'])
                                except:
                                  pays = 0.0 
                                  
                                students[g]['bal'] = fees - pays
                    except:
                        pass
                        
                    c = {}
                    for a in students:
                        if a in c:
                            pass
                        else:
                            c[a] = {}
                        for b in arr:
                            try:
                                c[a][arr[b][0]] = students[a][arr[b][0]]
                            except:
                                c[a][arr[b][0]] =  ''
                           
                    
                    self.body = c
                    if(columns):
                        self.header = {}
                        for j in arr:
                            if j in columns:
                              self.header[j] = arr[j]   
                    else:
                        self.header = arr
                        
                    self.fullname = title
                    
                    ret = self.classItemsProfile()
                    return ret
                    
                
        
    def classItemsProfile(self):
        table = '''<html><head>
        <link rel ='stylesheet' type="text/css" href='static/stylesheets/invoice-print.css'/>
       
        </head>
        <style>
        body{
            font: "Century Gothic";
        }
        @font-face
        {
               
        }
        h1{
                font-family: "Poiret One";
                font-size:30px;
        }
        h2{
                font-family: "Sarala";
                font-size:20px;
        }
        h3{
                font-family: "Sarala";
                font-size:20px;
               
        }
        tbody, th, td{
        padding:2px;
         
        }
        td{ align:center}
        .tch{
                align: left !important;
                background-color:teal; 
                color:white;
                text-transform: uppercase;
                font-family: "Century Gothic";
        }
        .tch1{
                color:black;
                text-transform: uppercase;
                font-family: "Century Gothic";
                font-weight:bold;
                width: 300px;
        }
        .item-tab{
                display:inline-block;
        }
        td img{
        max-width: 100px;
        height:150px;
        }
        td .centers
        {
         align:center !important;
        }
        .xtable{ display:block;}
        .xrow{ display:block;}
        .xcell{ display:inline-block;}
        
        .xtable{ display:table;}
        .xrow{ display:table-row;}
        .xcell{ display:table-cell;}
        .xcell-10{ width:100px !important;}
        </style>
        <body>

        <div width="100%" style="display:block; margin:0px; padding:0px; color:black" align="center">
        <h3>{{title | upper}}</h3>
        </div>
        
        <table width="100%" cellspacing="0" cellpadding="2px"  style="border-width:1px; border-color: teal; padding:2px; color:black; font-family: Century Gothic">
            <thead>
                <tr style='background-color:teal; color:white'>
                {% for r in header%}
                        <th>{{header[r][1]}}</th>
                {% endfor %}
                </tr>
            </thead>
            <tbody>
                {% for bod in body %}
                    <tr>
                    {% for r in header %}
                       <td {{header[r][2]}}>{{body[bod][header[r][0]] }}</td>
                    {% endfor %}
                    </tr>
                {% endfor %}
            </tbody>
            <tfoot>
                <tr  style='background-color:teal; color:white'>
                {% for r in header %}
                    {% if header[r][4] and  len(header[r][4]) > 0 %}
                        <th>{{header[r][1]}}</th>
                    {% else  %}
                        <th>-.-</th>
                    {% endif %}
                {% endfor %}
                </tr>
            </tfoot>
        </table>
        </body>
        </html>'''
        
        h = self.env.from_string(table).render(header = self.header, body = self.body, title = self.fullname)
        return h
     

    def classAcademicsProfile(self):
        table = '''<html><head>
        <link rel ='stylesheet' type="text/css" href='static/stylesheets/invoice-print.css'/>
       
        </head>
        <style>
        body{
            font: "Century Gothic";
        }
        @font-face
        {
               
        }
        h1{
                font-family: "Poiret One";
                font-size:30px;
        }
        h2{
                font-family: "Sarala";
                font-size:20px;
        }
        h3{
                font-family: "Sarala";
                font-size:20px;
               
        }
        tbody, th, td{
        padding:2px;
         
        }
        td{ align:center}
        .tch{
                align: left !important;
                background-color:teal; 
                color:white;
                text-transform: uppercase;
                font-family: "Century Gothic";
        }
        .tch1{
                color:black;
                text-transform: uppercase;
                font-family: "Century Gothic";
                font-weight:bold;
                width: 300px;
        }
        .item-tab{
                display:inline-block;
        }
        td img{
        max-width: 100px;
        height:150px;
        }
        td .centers
        {
         align:center !important;
        }
        .vert{
            vertical-align:middle; 
            display:inline-block;
            transform-origin:top left !important;
            transform: rotate(-90deg) !important;
            -ms-transform: rotate(-90deg);
            -o-transform: rotate(-90deg); 
            -moz-transform: rotate(-90deg);
        }
        .xtable{ display:block;}
        .xrow{ display:block;}
        .xcell{ display:inline-block;}
        
        .xtable{ display:table;}
        .xrow{ display:table-row;}
        .xcell{ display:table-cell;}
        .xcell-10{ width:100px !important;}
        </style>
        <body>

        <div width="100%" style="display:block; margin:0px; padding:0px; color:black" align="center">
        <h3>{{title | upper}}</h3>
        </div>
        
        <table width="100%" cellspacing="0" cellpadding="2px"  style="border-width:1px; border-color: teal; padding:2px; color:black; font-family: Century Gothic">
            <thead>
                <tr style='background-color:teal; color:white'>
                <th rowspan='2'>SN.</th>
                <th rowspan='2'>MATRIC. NO.</th>
                <th rowspan='2' style="width:200px">FULLNAME</th>
                <th rowspan='2'>CLASS</th>
                {% set cnt = 3 %}
                {% for r in subjects%}
                        <th colspan={{ cnt }}>{{subjects[r] | upper}}</th>
                {% endfor %}
                </tr>
                
                <tr style='background-color:teal; color:white'>
                {% for r in subjects %}
                    {% for c in cas %}
                        <th><div style="overflow: hidden"><div class='vert'>{{cas[c] | upper}}</div></div></th>
                    {% endfor %}
                {% endfor %}
                </tr>
            </thead>
            <tbody>
                {% for bod in body %}
                    <tr>
                    <td>SN.</td>
                    <th>{{body[bod]['matric'] | upper}}</th>
                    <th style='wrap:nowarp; min-width:200px !important">{{body[bod]['name'] | title}}</th>
                    <td>{{body[bod]['classunit'] | upper}}</td>
                        {% for r in subjects %}
                            {% for c in cas %}
                                {% if r in body[bod]['sco'] %}
                                    <td>{{body[bod]['sco'][r][c]}}</td>
                                {% else %}
                                    <td>-.-</td>
                                {% endif %}
                            {% endfor %}
                        {% endfor %}
                    </tr>
                {% endfor %}
            </tbody>
            
        </table>
        </body>
        </html>'''
        
        h = self.env.from_string(table).render(subjects = self.store_sub_name, cas = self.store_ca_name, casm = self.store_ca_max, body = self.body, title = self.fullname )
        return h          
    
    def classAcademicsSumProfile(self):
        table = self.htmlTag()
        table += '''
        <div width="100%" style="display:block; margin:0px; padding:0px; color:black" align="center">
        <h3>{{title | upper}}</h3>
        </div>
        <table width="100%" cellspacing="0" cellpadding="2px"  style="border-width:1px; border-color: teal; padding:2px; color:black; font-family: Century Gothic">
            <thead>
                <tr style='background-color:teal; color:white'>
                <th>SN.</th>
                <th >MATRIC. NO.</th>
                <th  style="width:200px">FULLNAME</th>
                <th >CLASS</th>
                {% set cnt = 3 %}
                {% for r in subjects%}
                        <th >{{subjects[r] | upper}}</th>
                {% endfor %}
                </tr>
                
                
            </thead>
            <tbody>
                {% for bod in body %}
                    <tr>
                    <td>SN.</td>
                    <th>{{body[bod]['matric'] | upper}}</th>
                    <th style='wrap:nowarp; min-width:200px !important">{{body[bod]['name'] | title}}</th>
                    <td>{{body[bod]['classunit'] | upper}}</td>
                        {% for r in subjects %}
                                {% if r in body[bod]['sco'] %}
                                    <td>{{body[bod]['sco'][r]}}</td>
                                {% else %}
                                    <td>-.-</td>
                                {% endif %}
                        {% endfor %}
                    </tr>
                {% endfor %}
            </tbody>
            
        </table>
        </body>
        </html>'''
        
        h = self.env.from_string(table).render(subjects = self.store_sub_name, cas = self.store_ca_name, casm = self.store_ca_max, body = self.body, title = self.fullname)
        return h  
    
    def classAcademicsSubjectProfile(self):
        table = self.htmlTag()
        table += '''
        <div width="100%" style="display:block; margin:0px; padding:0px; color:black" align="center">
        <h3>{{title | upper}}</h3>
        </div>
        <table width="100%" cellspacing="0" cellpadding="2px"  style="border-width:1px; border-color: teal; padding:2px; color:black; font-family: Century Gothic">
            <thead>
                <tr style='background-color:teal; color:white'>
                    <th>SN.</th>
                    <th style="wrap:nowarp; min-width:250px !important">ITEMS</th>
                    {% for r in headers %}
                        <th style="wrap:wrap">{{headers[r] | upper}}</th>
                    {% endfor %}
                </tr>
            </thead>
            <tbody>
               {% for j in subjects %}
                    <tr>
                    <td>SN.</td>
                    <td align='left' style="wrap:nowarp; min-width:250px !important">{{ subjects[j] | upper }} </td>
                        {% for a in headers %}
                                {% if a in body1[j] %}
                                    <td align='center'>{{body1[j][a] | round(2) }}</td>
                                {% else %}
                                    <td align='center'>-.-</td>
                                {% endif %}
                        {% endfor %}
                    
                    </tr>
                {% endfor %}
            </tbody>
            
        </table>
        <div width="100%" style="display:block; margin:0px; padding:0px; color:black" align="center">
        <img src="{{graph}}" >
        </div>
        </body>
        </html>'''
        
        h = self.env.from_string(table).render(headers = self.header,  subjects = self.store_sub_name,  casm = self.store_ca_max, body = self.body, body1 = self.body1, title = self.fullname, graph = self.graph)
        return h  
    
    def classAcademicsStudentProfile(self):
        table = self.htmlTag()
        table += '''
        <div width="100%" style="display:block; margin:0px; padding:0px; color:black" align="center">
        <h3>{{title | upper}}</h3>
        </div>
        <table width="100%" cellspacing="0" cellpadding="2px"  style="border-width:1px; border-color: teal; padding:2px; color:black; font-family: Century Gothic">
            <thead>
                <tr style='background-color:teal; color:white'>
                <th>SN.</th>
                <th>MATRIC. NO.</th>
                <th style="width:200px">FULLNAME</th>
                <th>CLASS</th>
                {% for r in headers%}
                        <th >{{headers[r] | upper}}</th>
                {% endfor %}
                </tr>
                
                
            </thead>
            <tbody>
                {% set serial = namespace(a = 1) %}
                {% for bod in body %}
                    <tr>
                    <td align ="center">{{ serial.a }}</td>
                    {% set serial.a = serial.a + 1 %}
                    <th>{{body[bod]['matric'] | upper}}</th>
                    <td style='wrap:nowarp; min-width:200px !important; float:left !important">{{body[bod]['name'] | title}}</td>
                    <td>{{body[bod]['classunit'] | upper}}</td>
                        {% for r in headers %}
                                {% if r in body1[bod] %}
                                    <td align="center">{{body1[bod][r] | round(2)}}</td>
                                {% else %}
                                    <td>-.-</td>
                                {% endif %}
                        {% endfor %}
                    </tr>
                
                {% endfor %}
            </tbody>
        </table>
        <div width="100%" style="display:block; margin:0px; padding:0px; color:black" align="center">
        <img src="{{graph}}" >
        </div>
        </body>
        </html>'''
        
        h = self.env.from_string(table).render(headers = self.header,  subjects = self.store_sub_name,  casm = self.store_ca_max, body = self.body, body1 = self.body1, title = self.fullname, graph = self.graph)
        return h  
    
    def classAcademicsStudentsProfile(self):
        table = self.htmlTag()
        table += '''
        <div width="100%" style="display:block; margin:0px; padding:0px; color:black" align="center">
        <h3>{{title | upper}}</h3>
        </div>
        <table width="100%" cellspacing="0" cellpadding="2px"  style="border-width:1px; border-color: teal; padding:2px; color:black; font-family: Century Gothic">
            <thead>
                <tr style='background-color:teal; color:white'>
                <th>SN.</th>
                <th >MATRIC. NO.</th>
                <th  style="width:200px">FULLNAME</th>
                <th >CLASS</th>
                {% set cnt = 3 %}
                {% for r in subjects%}
                        <th >{{subjects[r] | upper}}</th>
                {% endfor %}
                </tr>
                
                
            </thead>
            <tbody>
            {% set serial = 0 %}
                {% for bod in body %}
                    <tr>
                    <td align ='center'>{{ serial++ }}</td>
                    <th>{{body[bod]['matric'] | upper}}</th>
                    <th style='wrap:nowarp; min-width:200px !important">{{body[bod]['name'] | title}}</th>
                    <td>{{body[bod]['classunit'] | upper}}</td>
                        {% for r in subjects %}
                                {% if r in body[bod]['sco'] %}
                                    <td>{{body[bod]['sco'][r]}}</td>
                                {% else %}
                                    <td>-.-</td>
                                {% endif %}
                        {% endfor %}
                    </tr>
                {% endfor %}
            </tbody>
            
        </table>
        </body>
        </html>'''
        
        h = self.env.from_string(table).render(subjects = self.store_sub_name, cas = self.store_ca_name, casm = self.store_ca_max, body = self.body, title = self.fullname)
        return h          
    def staffProfile(self):
        table = '''<html><head>
        <link rel ='stylesheet' type="text/css" href='static/stylesheets/invoice-print.css'/>
        <link rel ='stylesheet' type="text/css" href='static/stylesheets/theme.css'/>
        </head>
        <style>
        body{
            font: "Century Gothic";
        }
        table
        {
        
        }
        tbody, th, td{
        padding:2px;
         
        }
        td{ align:left}
        .tch{
                align: left !important;
                background-color:teal; 
                color:white;
                text-transform: uppercase;
                font-family: "Century Gothic";
        }
        .tch1{
                color:black;
                font-family: "Century Gothic";
                
                width: 300px;
        }
        .item-tab{
                display:inline-block;
        }
        td img{
        max-width: 100px;
        height:150px;
        }
        </style>
        <body>
            <div width='100%'>
            <div display="block">
                <h2>STAFF PROFILE: <span>{{name}}</span></h2>
            </div>
            {% if 1 in sel %}
                <div width="100%" style="background-color:teal; color:white; text-transform:uppercase; text-align:center">
                    <h3>Bio-Data and Contact Information</h3>
                </div>
                <div style='display:flex'>
                    <div class="item-tab" width='600px' >
                    <table width="100% " cellspacing="0" cellpadding="2px"  style="border-width:1px; border-color: teal; padding:2px" >
                        <tbody>
                            <tr><td rowspan="16" width="33%" style="background-color:None; margin:0px; padding:0px" ><img style="margin:0px; padding:0px"  src="{{fil.photo}}" width="270" height="390" /></td><th class="tch" align='right'>EMPLOYEE NUMBER</th><td class="tch1" width="40%">{{dat.empno}}</td>
                            </tr>
                            <tr><th class="tch" align='right' >SURNAME</th><td class="tch1" width="40%">{{dat.surname | upper}}</td></tr>
                            <tr><th class="tch" align='right' style="align:right">FIRSTNAME</th><td class="tch1" width="40%">{{dat.firstname | upper}}</td></tr>
                            <tr><th class="tch" align='right' >MIDDLENAME</th><td class="tch1" width="40%">{{dat.othername | upper}}</td></tr>
                            <tr><th class="tch" align='right'>SEX / DATE OF BIRTH / AGE</th><td class="tch1" width="40%">{{fil.gender}}/ {{fil.dob }} /{{fil.age}}</td></tr>
                             <tr><th class="tch" align='right'>RELIGION</th><td class="tch1" width="40%">{{fil.religion | upper}}</td></tr>
                            <tr><th class="tch" align='right'>LGA/DISTRICT</th><td class="tch1" width="40%">{{dat.lga | upper}}</td></tr>
                            <tr><th class="tch" align='right' style='wrap:nowrap'>STATE/ NATIONALITY</th><td class="tch1" width="40%">{{dat.soo | upper}} {{dat.nation | upper}}</td></tr>
                            <tr><th class="tch" align='right'>DATE EMPLOYED</th><td class="tch1" width="40%">{{fil.emp}}  ( {{fil.empyrs}})</td></tr>
                             <tr><th class="tch" align='right'>DEPARTMENT & UNIT</th><td class="tch1" width="40%">{{fil.dep}}  ( {{fil.unit}})</td></tr>
                            <tr><th class="tch" align='right'>MARITAL STATUS</th><td class="tch1" width="40%">{{fil.marital}}  ( {{dat.noc}} children)</td></tr>
                            <tr><th class="tch" align='right'>EMPLOYMENT STATUS</th><td class="tch1" width="40%">{{fil.user}} ({{dat.access}} )</td></tr>
                            {% if fil.reasonid > 0 %}
                                <tr><th class="tch" align='right'>REASON FOR LEAVING </th><td class="tch1" width="40%"> <span style="color:red">{{fil.reason}} </span> {{fil.dol}}<p style='margin:0px; display:block '> {{dat.dolinfo}}</p></td></tr>
                            {% endif %}
                            <tr><th class="tch" align='right'>ADDRESS</th><td class="tch1" width="40%" style="word-wrap:break-word;overflow:none">{{dat.addr}}</td></tr>
                            <tr><th class="tch" align='right'>PHONE & EMAIL</th><td class="tch1" width="40%" style="word-wrap:break-word;overflow:none">{{dat.phone1}} {{dat.phone2}} {{dat.email}}</td></tr>
                        </tbody>
                        </tbody>
                    </table>
                </div>
                </div>
                {% endif %}
                {% if 2 in sel %}
                <div width="100%" style="background-color:teal; color:white; text-transform:uppercase; align:center">
                    <h3>Next of Kin</h3>
                </div>
                <div>
                <table width="100% " cellspacing="0" cellpadding="2px"  style="border-width:1px; border-color: teal; padding:2px" >
                    <tbody style='align:left'>
                        <tr><td class="tch1" width="10%"><img src='{{fil.photo1}}' width='100' height='100' style='margin:0px'></td><td class="tch1" width="90%"><ul><li>{{dat.g1 | upper}}({{dat.g1rel | upper}}) </li><li> {{dat.g1p1}} | {{dat.g1p2}} </li><li> {{dat.g1addr | upper}} </li> <li>{{dat.g1email}}</li></ul></td></tr>
                        <tr><td class="tch1" width="10%"><img src='{{fil.photo2}}' width='100' height='100' style='margin:0px'></td><td class="tch1" width="90%"><ul><li>{{dat.g2 | upper}}({{dat.g2rel | upper}}) </li><li> {{dat.g2p1}} | {{dat.g2p2}} </li><li> {{dat.g2addr | upper}} </li> <li>{{dat.g2email}}</li></ul></td></tr>
                    </tbody>
                </table>
                </div>
                {% endif %}
                {% if 3 in sel %}
                <div width="100%" style="background-color:teal; color:white; text-transform:uppercase; align:center">
                    <h3>Finanial Details</h3>
                </div>
                <div>
                <table width="100% " cellspacing="0" cellpadding="2px"  style="border-width:1px; border-color: teal; padding:2px" >
                    <tbody style='align:left'>
                        <tr><td class="tch1" width="20%">Account</td><td class="tch1" width="80%">{{fil.bank | upper}}( {{dat.account | upper}}) {{dat.sort | upper}}</td></tr>
                        <tr><td class="tch1" width="20%">Pension</td><td class="tch1" width="80%">{{fil.pen | upper}}( {{dat.pensioncode | upper}})</td></tr>
                        <tr><td class="tch1" width="20%">Health Insurance</td><td class="tch1" width="80%">{{fil.health | upper}}( {{dat.healthcode | upper}})</td></tr>
                        <tr><td class="tch1" width="20%">Social Insurance</td><td class="tch1" width="80%">{{dat.socialcode | upper}}</td></tr>
                    </tbody>
                </table>
                </div>
                {% endif %}
                {% if 4 in sel %}
                <div width="100%" style="background-color:teal; color:white; text-transform:uppercase; align:center">
                    <h3>Academic History</h3>
                </div>
                <div>
                <table width="100% " cellspacing="0" cellpadding="2px"  style="border-width:1px; border-color: teal; padding:2px" >
                    <tbody style='align:left'>
                    {%for s in ss[1]%}
                        <tr><td class="tch1" width="100%"><div style='margin:0px'><span style='display:flex'><b>{{s.school | upper}}</b></span> <span style="float:right; flex:1">{{s.startdate | timestamp_to_time  }} to {{s.enddate | timestamp_to_time  }}</span></div><p style='margin:0px'>{{s.degree}} {{s.course | upper}} ({{s.grade | upper}})</p></td></tr>
                    {% endfor %}
                    </tbody>
                </table>
                </div>
                {% endif %}
                {% if 5 in sel %}
                <div width="100%" style="background-color:teal; color:white; text-transform:uppercase; align:center">
                    <h3>Professional Qualification</h3>
                </div>
                <div>
                <table width="100% " cellspacing="0" cellpadding="2px"  style="border-width:1px; border-color: teal; padding:2px" >
                    <tbody style='align:left'>
                    {%for s in ss[2]%}
                        <tr><td class="tch1" width="100%"><div style='margin:0px'><span style='display:flex'>{{s.degree}} <b>{{s.school | upper}}</b></span> <span style="float:right; flex:1"> ({{s.startdate | timestamp_to_time  }})</span></div><p style='margin:0px'>{{s.course | upper}}</p></td></tr>
                    {% endfor %}
                    </tbody>
                </table>
                </div>
                {% endif %}
                {% if 6 in sel %}
                <div width="100%" style="background-color:teal; color:white; text-transform:uppercase; align:center">
                    <h3>Work Experience/History</h3>
                </div>
                <div>
                <table width="100% " cellspacing="0" cellpadding="2px"  style="border-width:1px; border-color: teal; padding:2px" >
                    <tbody style='align:left'>
                    {%for s in ss[3]%}
                        <tr><td class="tch1" width="20%"><div style='margin:0px'>{{s.startdate | timestamp_to_time  }} to {{s.enddate | timestamp_to_time  }}</td><td class="tch1" width="100%"><div style='margin:0px'><span style='display:flex'>{{s.degree}} <b>{{s.school | upper}}</b></span></div><p style='margin:0px'><br> {{s.course | upper}}</p><p style='display:block'>{{s.description}}</ </p></td></tr>
                    {% endfor %}
                    </tbody>
                </table>
                </div>
                {% endif %}
                {% if 7 in sel %}
                <div width="100%" style="background-color:teal; color:white; text-transform:uppercase; align:center">
                    <h3>WORKSHOPS/SEMINARS</h3>
                </div>
                <div>
                <table width="100% " cellspacing="0" cellpadding="2px"  style="border-width:1px; border-color: teal; padding:2px" >
                    <tbody style='align:left'>
                    {%for s in ss[4]%}
                        <tr><td class="tch1" width="20%"><div style='margin:0px'>{{s.startdate | timestamp_to_time  }}= {{s.enddate | timestamp_to_time  }}</td><td class="tch1" width="100%"><div style='margin:0px'><span style='display:flex'><b>{{s.school | upper}}</b></span></div><p style='margin:0px;display:block'> {{s.course | upper}} {{s.degree | upper}}</p><p style='display:block'>{{s.description}}</p></td></tr>
                    {% endfor %}
                    </tbody>
                </table>
                </div>
                {% endif %}
                {% if 8 in sel %}
                <div width="100%" style="background-color:teal; color:white; text-transform:uppercase; align:center">
                    <h3>MISCONDUCT</h3>
                </div>
                <div>
                <table width="100% " cellspacing="0" cellpadding="2px"  style="border-width:1px; border-color: teal; padding:2px" >
                    <tbody style='align:left'>
                    {%for s in ss[5]%}
                        <tr><td class="tch1" width="20%"><div style='margin:0px'>{{s.startdate | timestamp_to_time  }}</td><td class="tch1" width="100%"><div style='margin:0px'><span style='display:flex'><b>{{s.school}}</b></span></div><p style='margin:0px;display:block'><i> {{s.course}} </i></p><p style='margin:1px; display:block'><b><i>{{s.degree}}</i></b></p></td></tr>
                    {% endfor %}
                    </tbody>
                </table>
                </div>
                {% endif %}
                {% if 9 in sel %}
                <div width="100%" style="background-color:teal; color:white; text-transform:uppercase; align:center">
                    <h3>COMMENDATIONS/AWARDS</h3>
                </div>
                <div>
                <table width="100% " cellspacing="0" cellpadding="2px"  style="border-width:1px; border-color: teal; padding:2px" >
                    <tbody style='align:left'>
                    {%for s in ss[6]%}
                        <tr><td class="tch1" width="20%"><div style='margin:0px'>{{s.startdate | timestamp_to_time  }}</td><td class="tch1" width="100%"><div style='margin:0px'><span style='display:flex'><b>{{s.school}}</b></span></div><p style='margin:0px;display:block'><i> {{s.course}} </i></p><p style='margin:1px; display:block'><b><i>{{s.degree}}</i></b></p></td></tr>
                    {% endfor %}
                    </tbody>
                </table>
                </div>
                {% endif %}
                {% if 10 in sel %}
               <div width="100%" style="background-color:teal; color:white; text-transform:uppercase; align:center">
                    <h3>DUTIES/RESPONSIBILITIES</h3>
                </div>
                <div>
                <table width="100% " cellspacing="0" cellpadding="2px"  style="border-width:1px; border-color: teal; padding:2px" >
                    <tbody style='align:left'>
                    {%for s in ss[7]%}
                        <tr><td class="tch1" width="20%"><div style='margin:0px'>{{s.startdate | timestamp_to_time  }}= {{s.enddate | timestamp_to_time  }}</td><td class="tch1" width="100%"><div style='margin:0px'><span style='display:flex'><b>{{s.school | upper}}</b></span></div><p style='margin:0px;display:block'> {{s.course | upper}} {{s.degree | upper}}</p><p style='display:block'>{{s.description}}</p></td></tr>
                    {% endfor %}
                    </tbody>
                </table>
                </div>
                {% endif %}
                
                </body></html>'''
               
            
        h = self.env.from_string(table).render(dat = self.data, fil = self.file, ss = self.filez, sel = self.selections, name = self.fullname)
        return h
    
    
    
    def studentProfile(self):
        table = '''<html><head>
        <link rel ='stylesheet' type="text/css" href='static/stylesheets/invoice-print.css'/>
        <link rel ='stylesheet' type="text/css" href='static/stylesheets/theme.css'/>
        </head>
        <style>
        body{
            font: "Century Gothic";
        }
        table
        {
        
        }
        tbody, th, td{
        padding:2px;
         
        }
        td{ align:left}
        .tch{
                align: left !important;
                background-color:teal; 
                color:white;
                text-transform: uppercase;
                font-family: "Century Gothic";
        }
        .tch1{
                color:black;
                text-transform: uppercase;
                font-family: "Century Gothic";
                font-weight:bold;
                width: 300px;
        }
        .item-tab{
                display:inline-block;
        }
        td img{
        max-width: 100px;
        height:150px;
        }
        </style>
        <body>
            <div width='100%'>
                <div width="100%" style="background-color:teal; color:white; text-transform:uppercase; text-align:center">
                    <h3>Bio-Data and Contact Information</h3>
                </div>
                <div style='display:flex'>
                    <div class="item-tab" width='600px' >
                    <table width="500px " cellspacing="0" cellpadding="2px"  style="border-width:1px; border-color: teal; padding:2px" >
                        <tbody>
                            <tr><th class="tch" style="align:right">SCHOOL NUMBER</th><td class="tch1" width="40%">{{dat.schno}}</td>
                            <td rowspan="13" width="40%" style="background-color:green"><img src="img/studentz.png" width="250" height="340" /></td></tr>
                            <tr><th class="tch" style="align:right">SURNAME</th><td class="tch1" width="40%">{{dat.surname | upper}}</td></tr>
                            <tr><th class="tch" style="align:right">FIRSTNAME</th><td class="tch1" width="40%">{{dat.firstname | upper}}</td></tr>
                            <tr><th class="tch" style="align:right">MIDDLENAME</th><td class="tch1" width="40%">{{dat.othername | upper}}</td></tr>
                            <tr><th class="tch" style="align:right">SEX</th><td class="tch1" width="40%">{{gender}}</td></tr>
                            <tr><th class="tch" style="align:right">DATE OF BIRTH</th><td class="tch1" width="40%">{{dob }}</td></tr>
                            <tr><th class="tch" style="align:right">AGE</th><td class="tch1" width="40%">{{age}}</td></tr>
                            <tr><th class="tch" style="align:right">LGA/District</th><td class="tch1" width="40%">{{dat.lga | upper}}</td></tr>
                            <tr><th class="tch" style="align:right">State/Region</th><td class="tch1" width="40%">{{dat.soo | upper}}</td></tr>
                            <tr><th class="tch" style="align:right">Nationality</th><td class="tch1" width="40%">{{dat.nation | upper}}</td></tr>
                            <tr><th class="tch" style="align:right">Date Started</th><td class="tch1" width="40%">{{admit}}  ( {{admit_dur}})</td></tr>
                            <tr><th class="tch" style="align:right">Status</th><td class="tch1" width="40%">{{dat.schno}}<.td></tr>
                            <tr><th class="tch" style="align:right">Address</th><td class="tch1" width="40%" style="word-wrap:break-word;overflow:none">{{dat.addr}}</td></tr>
                        </tbody>
                    </table>
                </div>
                </div>
                <div width="100%" style="background-color:teal; color:white; text-transform:uppercase; align:center">
                    <h3>Guradians/Primary Care Giver</h3>
                </div>
                <div>
                <table width="100% " cellspacing="0" cellpadding="2px"  style="border-width:1px; border-color: teal; padding:2px" >
                <tbody style='align:left'>
                    <tr><td class="tch1" width="100%"><ul><li>{{dat.g1 | upper}}({{dat.g1rel | upper}}) </li><li> {{dat.g1p1}} | {{dat.g1p2}} </li><li> {{dat.g1addr | upper}} </li> <li>{{dat.g1email}}</li></ul></td></tr>
                    <tr><td class="tch1" width="100%"><ul><li>{{dat.g2 | upper}}({{dat.g2rel | upper}}) </li><li> {{dat.g2p1}} | {{dat.g2p2}} </li><li> {{dat.g2addr | upper}} </li> <li>{{dat.g2email}}</li></ul></td></tr>
                </tbody>
                </table>
                
                </div></body></html>'''
               
            
        h = jinja2.Template(table).render(dat = self.data, age=self.age, don =self.dob, adm = self.adm)
        return h
    
    def getStudentAssessments(self, session, student=[]):
        _session = session
        _student = student
        g = Db()
        data = g.selectStudentsCa(_session, _student, [], [])
        return data
    def getStudentAffective(self, session, student=[]):
        _session = session
        _student = student
        g = Db()
        data = g.selectStudentsAffectiveSum(_session, _student, [], [])
        return data
    def getStudentPsychomoto(self, session, student=[]):
        _session = session
        _student = student
        g = Db()
        data = g.selectStudentsPsychomotoSum(_session, _student, [], [])
        return data
    
    
    def htmlTag(self):
        ht ='''
        <html><head>
        <link rel ='stylesheet' type="text/css" href='static/stylesheets/invoice-print.css'/>
       
        </head>
        <style>
        body{
            font: "Century Gothic";
        }
        @font-face
        {
               
        }
        h1{
                font-family: "Poiret One";
                font-size:30px;
        }
        h2{
                font-family: "Sarala";
                font-size:20px;
        }
        h3{
                font-family: "Sarala";
                font-size:20px;
               
        }
        tbody, th, td{
        padding:2px;
         
        }
        td{ align:center}
        .tch{
                align: left !important;
                background-color:teal; 
                color:white;
                text-transform: uppercase;
                font-family: "Century Gothic";
        }
        .tch1{
                color:black;
                text-transform: uppercase;
                font-family: "Century Gothic";
                font-weight:bold;
                width: 300px;
        }
        .item-tab{
                display:inline-block;
        }
        td img{
        max-width: 100px;
        height:150px;
        }
        td .centers
        {
         align:center !important;
        }
        .vert{
            vertical-align:middle; 
            display:inline-block;
            transform-origin:top left !important;
            transform: rotate(-90deg) !important;
            -ms-transform: rotate(-90deg);
            -o-transform: rotate(-90deg); 
            -moz-transform: rotate(-90deg);
        }
        .xtable{ display:block;}
        .xrow{ display:block;}
        .xcell{ display:inline-block;}
        
        .xtable{ display:table;}
        .xrow{ display:table-row;}
        .xcell{ display:table-cell;}
        .xcell-10{ width:100px !important;}
        </style>
        <body>

        '''
        return ht