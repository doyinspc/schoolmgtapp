# -*- coding: utf-8 -*-
"""
Created on Sat Jul 28 13:30:41 2018

@author: CHARLES
"""
from connect import Db

class StudentTable():
    
    def __init__(self, session=None , studentID=[], classID=[], classUnitID =[]):
        #super(StudentTable, self).__init__()
        self.session = session
        self.studentID = studentID
        self.classID = classID
        self.classUnitID = classUnitID
            
    
    def classStudentMul(self):
        num = 0
        d = {}
        for a1 in self.classID:
            d = self.classStudentO(a1)
            num = int(num) + int(len(d))
            
            
        return [num, d]
    
    def classStudentO(self, a):
        allUnits = self.getClassUnit(a)
        d = self.pullStudentsID(self.session, allUnits)
        return d
    
    def classStudent(self):
        allUnits = self.getClassUnit(self.classID[0])
        d = self.pullStudentsID(self.session, allUnits)
        return d
    
    def classStudents(self):
        allUnits = self.getClassUnit(self.classUnitID)
        d = self.pullStudentsID(self.session, allUnits)
        return d
    
    def classAllStudent(self):
        d = self.pullStudentsAllID(self.session)
        return d
    
    def classAllExStudent(self):
        d = self.pullStudentsAllID(self.session)
        return d
    
    def classAllCrStudent(self):
        d = self.pullStudentsAllCrID(self.session)
        return d
    
    def className(self, a =[]):
        d = self.getClassName(a)
        return d
    
    def classUnitStudent(self):
        d = self.pullStudentsID(self.session, self.classUnitID)
        return d
    
    def classMoveStudent(self, session, moveclass, students):
        session = session
        classtable = 'student_class'+str(session)
        arr = []
        g = Db()
        for student in students:
            f = g.select(classtable, '', 1, {'studentID':student})
            if f and int(f[0]) > 1:
                h = g.update(classtable, {'classID': moveclass}, {'id': f[0]})
                h = f[0]
                
            else:
                h = g.insert(classtable, {'studentID': student, 'classID': moveclass,'active': 0})   
                
            arr.append(h)
        return arr
    
    def classRemoveStudent(self, session, students):
        session = session
        classtable = 'student_class'+str(session)
        arr = []
        g = Db()
        for student in students:
            f = g.select(classtable, '', 1, {'studentID':student})
            if f and int(f[0]) > 1:
                h = g.delete(classtable, {'studentID': student})
                h = f[0]
            else:
                pass   
                
            arr.append(h)
        return arr
    
    def pullStudentsID(self, a, b=[]):
        self.a = a
        self.b = b
        termtable = 'student_class'+str(self.a)
        cn = Db()
        students = cn.selectStudentClass(termtable, self.b)
        return students
    
    def pullStudentsAllID(self, a):
        self.a = a
        cn = Db()
        students = cn.selectStudentAll(self.a)
        return students
    
    def pullStudentsAllCrID(self, a):
        self.a = a
        cn = Db()
        students = cn.selectStudentAllCr(self.a)
        return students
    
    def pullStudentsAllExID(self, a):
        self.a = a
        cn = Db()
        students = cn.selectStudentAllEx(self.a)
        return students
    
    def getClassUnit(self, *a):
        self.a = a[0]
        arr = []
        g = Db()
        si = g.select('datas', '', '', {'subID':self.a})
        for s in si:
            arr.append(s[0])
            
        return arr
    
    def getClassName(self, a={}):
        self.a = a
        nm = ''
        g = Db()
        for re in self.a:
            si = g.selectn('datas', '', 1, {'id':re})
            sii = g.selectn('datas', '', 1, {'id':si['subID']})
            
            nm = nm+sii['abbrv']+' '+si['abbrv']+' '
            
        return nm
    
    def selectedStudents(self, b = []):
        _a = self.session
        _b = b
        print(b)
        cn = Db()
        students = cn.selectStudentSelected(_a, _b)
        return students