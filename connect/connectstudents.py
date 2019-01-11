# -*- coding: utf-8 -*-
"""
Created on Fri Dec 28 03:28:08 2018

@author: CHARLES
"""
from connect import Db
from studenttable import StudentTable
import sqlite3
import pandas as pd


class Con(object):
    dbs = 'test.db';
    def academicReport(self, session, student, ca):
        '''
        select form database tables
        give table name, columns, number of rows,
        '''
        db = 'student_result'+str(session)
        ca = ', '.join(str(e) for e in ca)
        if len(ca) > 0:
            cal = ' AND caID in ('+ ca +')'
        else:
            cal = ''
        sql = "SELECT studentID, score, caID, subjectID, (SELECT abbrv FROM datas WHERE id = caID  LIMIT 1) as camax FROM "+ db +" WHERE studentID = "+ student +" "+ cal +" "

        try:
            conn = sqlite3.connect(self.dbs)
            conn.row_factory = lambda C, R: {c[0]: R[i] for i, c in enumerate(C.description)}
            c = conn.cursor()
            c.execute(sql)
            return c.fetchall()
            conn.close()
        except sqlite3.Error as e:
            print(e)
    
    def academicRank(self, session, student, ca):
        '''
        select form database tables
        give table name, columns, number of rows,
        '''
        db = 'student_result'+str(session)
        ca = ', '.join(str(e) for e in ca)
        if len(ca) > 0:
            cal = ' AND caID in ('+ ca +')'
        else:
            cal = ''
        sql = "SELECT studentID, (SELECT studentID, score, caID, subjectID, (SELECT abbrv FROM datas WHERE id = caID  LIMIT 1) as camax FROM "+ db +" WHERE studentID = "+ student +" "+ cal +" )"

        try:
            conn = sqlite3.connect(self.dbs)
            conn.row_factory = lambda C, R: {c[0]: R[i] for i, c in enumerate(C.description)}
            c = conn.cursor()
            c.execute(sql)
            return c.fetchall()
            conn.close()
        except sqlite3.Error as e:
            print(e)
    
    def academicReportData(self, session, student, ca):
        data = self.academicReport(session, student, ca)
        arr2 = {}
        ca_arr = []
        sub_arr = []
        
        for i in data:
            ca_arr.append(i['caID'])
            sub_arr.append(i['subjectID'])
            nm = 'AB'+str(i['subjectID'])+'CD'+str(i['caID'])
            arr2[nm] = float(i['score']) * float(i['camax'])
            
        ca = self.getDataArrange(ca)
        sub = self.getDataArrange(sub_arr)
        
        return [arr2, ca, sub]
    
    def getData(self, a):
        cn = Db()
        data = cn.selectMultiplen('datas', list(set(a)))
        return data
    
    def getDataArrange(self, a):
        data = self.getData(a)
        arr = {}
        for d in data:
            ar = [d['name'], d['abbrv']]
            arr[d['id']] = ar
        
        return arr
    
    def pullGrade(self, a):
        cn = Db()
        data = cn.selectn('datas', '', '', {'subID':a})
        arr = []
        for f in data:
            des = f['description'].split(':')
            arrd = {}
            arrd['max'] = des[0]
            arrd['min'] = des[1]
            arrd['color'] = des[2]
            arrd['name'] = f['name']
            arrd['abbrv'] = f['abbrv']
            arr.append(arrd)
        
        return arr
    
    def subjectAverage(self, session, student, ca, subject):
        #get student class
        db = 'student_class'+str(session);
        cn = Db()
        cl = cn.selectn(db, '', 1, {'studentID':student})
        scla = cl['classID'] 
        scl = StudentTable(session, student, [], scla)
       
        #get all alass mates
        studentsIDs = scl.classStudents()
        student_id = []
        for dx in studentsIDs :
            student_id.append(dx[0]) 
        
        dat = self.allSubjects(session, student_id, subject, ca)
        df = pd.DataFrame.from_dict(dat)
        ret ={}
        for x in subject:
            dy = df.loc[df['subjectID'] == x]
            me = dy['score'].mean()
            co = dy['score'].count()
            dx = dy.set_index('studentID')
            dx = dx.sort_values('score', ascending=False)
            dx = dx.reset_index()
            dx = dx.index[dx['studentID'] == int(student)]
            dx = dx.values.tolist()
            ran = dx[0] + 1
            arr =[round(me,2), co, ran]
            ret[x] = arr
       
        return ret    
        #get all subjects
    def studentAverage(self, session, student, ca, subject):
        #get student class
        db = 'student_class'+str(session);
        cn = Db()
        cl = cn.selectn(db, '', 1, {'studentID':student})
        scla = cl['classID'] 
        clz = cn.selectn('datas', '', 1, {'id':scla})
        scla = clz['subID']
        ar = []
        ar.append(scla)
        scl = StudentTable(session, [None], ar, [None])
        
        #get all alass mates
        studentsIDs = scl.classStudent()
        student_id = []
        for dx in studentsIDs :
            student_id.append(dx[0]) 
        
        dat = self.allStudents(session, student_id, subject, ca)
        dy = pd.DataFrame.from_dict(dat)
        
        me = dy['score'].mean()
        co = dy['score'].count()
        dx = dy.set_index('studentID')
        dx = dx.sort_values('score', ascending=False)
        dx = dx.reset_index()
        dx = dx.index[dx['studentID'] == int(student)]
        dx = dx.values.tolist()
        ran = dx[0] + 1
        arr =[round(me,2), co, ran]
        return arr 
        
    def studentAverageUnit(self, session, student, ca, subject):
        #get student class
        db = 'student_class'+str(session);
        cn = Db()
        cl = cn.selectn(db, '', 1, {'studentID':student})
        scla = cl['classID'] 
        ar = []
        ar.append(scla)
        scl = StudentTable(session, [None], [None], ar)
       
        #get all alass mates
        studentsIDs = scl.classUnitStudent()
        student_id = []
        for dx in studentsIDs :
            student_id.append(dx[0]) 
        
        dat = self.allStudents(session, student_id, subject, ca)
        dy = pd.DataFrame.from_dict(dat)
        
        me = dy['score'].mean()
        co = dy['score'].count()
        dx = dy.set_index('studentID')
        dx = dx.sort_values('score', ascending=False)
        dx = dx.reset_index()
        dx = dx.index[dx['studentID'] == int(student)]
        dx = dx.values.tolist()
        ran = dx[0] + 1
        arr =[round(me,2), co, ran]
        return arr    
            
    def allSubjects(self, session, students, subjects, ca):
        '''
        get all subjects score fro class
        '''
        db = 'student_result'+str(session)
     
        subject_list = ', '.join(str(e) for e in subjects)
        student_list = ', '.join(str(e) for e in students)
        ca_list = ', '.join(str(e) for e in ca)
        whr = ''
        
        if len(subject_list) > 0:
            whr += ' subjectID in ('+subject_list+')'
        if len(student_list) > 0:
            if len(whr) > 0:
                whr += ' AND studentID in ('+student_list+')'
            else:
                whr += ' studentID in ('+student_list+')'
        if len(ca_list) > 0:
            if len(whr) > 0:
                whr += ' AND caID in ('+ca_list+')'
            else:
                whr += ' AND caID in ('+ca_list+')'
                
        if len(whr) > 0:
            where = ' WHERE '+ whr
        else:
            where =''
        
        sql = "SELECT subjectID, studentID, SUM(score) as score FROM (SELECT subjectID, caID, (score * (SELECT abbrv FROM datas WHERE id = caID  )) as score, studentID  FROM "+ db +" "+ where +")  GROUP BY studentID, subjectID "
       
        try:
            conn = sqlite3.connect(self.dbs)
            conn.row_factory = lambda C, R: {c[0]: R[i] for i, c in enumerate(C.description)}
            c = conn.cursor()
            c.execute(sql)
            return c.fetchall()
            conn.close()
        except sqlite3.Error as e:
            print(e)       
            
     
    def allStudents(self, session, students, subjects, ca):
        '''
        get all subjects score fro class
        '''
        db = 'student_result'+str(session)
     
        subject_list = ', '.join(str(e) for e in subjects)
        student_list = ', '.join(str(e) for e in students)
        ca_list = ', '.join(str(e) for e in ca)
        whr = ''
        
        if len(subject_list) > 0:
            whr += ' subjectID in ('+subject_list+')'
        if len(student_list) > 0:
            if len(whr) > 0:
                whr += ' AND studentID in ('+student_list+')'
            else:
                whr += ' studentID in ('+student_list+')'
        if len(ca_list) > 0:
            if len(whr) > 0:
                whr += ' AND caID in ('+ca_list+')'
            else:
                whr += ' AND caID in ('+ca_list+')'
                
        if len(whr) > 0:
            where = ' WHERE '+ whr
        else:
            where =''
        
        sql = "SELECT studentID, AVG(score) as score FROM (SELECT subjectID, studentID, SUM(score) as score FROM (SELECT subjectID, caID, (score * (SELECT abbrv FROM datas WHERE id = caID  )) as score, studentID  FROM "+ db +" "+ where +")  GROUP BY studentID, subjectID) GROUP BY studentID "
        
        try:
            conn = sqlite3.connect(self.dbs)
            conn.row_factory = lambda C, R: {c[0]: R[i] for i, c in enumerate(C.description)}
            c = conn.cursor()
            c.execute(sql)
            return c.fetchall()
            conn.close()
        except sqlite3.Error as e:
            print(e)    