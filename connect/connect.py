# -*- coding: utf-8 -*-
"""
Created on Sun Jun 24 04:41:40 2018
@author: CHARLES
"""
import sqlite3
from tables import Tables
import smtplib
import pandas as pd
import os

class Db(object):
    dbs = 'test.db';
    
    def __init__(self):
        pass
    
    def logConnect(self, sql):
        self.sql = sql
       
        try:
            conn = sqlite3.connect(self.dbs)
            c = conn.cursor()
            c.execute(self.sql)
            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            print(e)

    
    def createTable(self, a):
        self.a = a
        t = Tables()
        sql = t.students()
        self.logConnect(sql)
        
    def createClass(self, a):
        self.a = a
        t = Tables()
        sql = t.studentClasz(self.a)
        self.logConnect(sql)
        
    def createSubject(self, a):
        self.a = a
        t = Tables()
        sql = t.studentSubjects(self.a)
        self.logConnect(sql)
        
    def createResult(self, a):
        self.a = a
        t = Tables()
        sql = t.studentResult(self.a)
        self.logConnect(sql)
        
    def createAffective(self, a):
        self.a = a
        t = Tables()
        sql = t.studentAffective(self.a)
        self.logConnect(sql)
        
    def createPsychomoto(self, a):
        self.a = a
        t = Tables()
        sql = t.studentPsychomoto(self.a)
        self.logConnect(sql)
        
    def createFee(self, a):
        self.a = a
        t = Tables()
        sql = t.studentFee(self.a)
        self.logConnect(sql)
    
    def createPay(self, a):
        self.a = a
        t = Tables()
        sql = t.studentPay(self.a)
        self.logConnect(sql)
        
    def createExpenses(self, a):
        self.a = a
        t = Tables()
        sql = t.schoolExpenses(self.a)
        self.logConnect(sql)
        
    def createStores(self, a):
        self.a = a
        t = Tables()
        sql = t.schoolStores(self.a)
        self.logConnect(sql)
        
    def createAwards(self, a):
        self.a = a
        t = Tables()
        sql = t.schoolAwards(self.a)
        self.logConnect(sql)
        
    def createConducts(self, a):
        self.a = a
        t = Tables()
        sql = t.schoolConducts(self.a)
        self.logConnect(sql)
        
    def createMails(self, a):
        self.a = a
        t = Tables()
        sql = t.schoolMails(self.a)
        self.logConnect(sql)
        
    def createMedicals(self, a):
        self.a = a
        t = Tables()
        sql = t.schoolMedicals(self.a)
        self.logConnect(sql)
        
    def createStudent(self):
        t = Tables()
        sql = t.students()
        self.logConnect(sql)
        
    def createSession(self):
        t = Tables()
        sql = t.session()
        self.logConnect(sql)
    
    def createTerm(self):
        t = Tables()
        sql = t.terms()
        self.logConnect(sql)
        
    def createStaffs(self):
        t = Tables()
        sql = t.staffs()
        self.logConnect(sql)
        
    def createDatas(self):
        t = Tables()
        sql = t.datas()
        self.logConnect(sql)
        
    def createData(self):
        t = Tables()
        sql = t.terms()
        #try:
        conn = sqlite3.connect(self.dbs)
        c = conn.cursor()
        c.execute(sql)
        conn.commit()
        conn.close()
        #except:
            #pass
        #self.logConnect(sql)
   
    def getTermClass(self, student):
        #get all terms
        f = self.selectn('terms', '', '')
        store = {}
        #check if in clas
        
        for a in f:
            if a != None and a['id']:
                db = 'student_class'+str(a['id'])
                r = {}
                r = self.selectn(db, ['id', 'classID'], 1, {'studentID':student})
                if (r and len(r) > 0):
                    e = self.selectn('session', '', 1, {'id':a['sessionID']})
                    c = self.selectn('datas', '', 1, {'id':r['classID']})
                    if c:
                        d = self.selectn('datas', ['id', 'abbrv'], 1, {'id':c['subID']})
                        if d:
                            pass
                        else:
                          d['abbrv'] ='--'  
                    else:
                        c['abbrv'] ='--'
                        d['abbrv'] ='--'
                        
                    st = str(d['abbrv'])+str(c['abbrv'])+' '+str(e['name'])+' '+str(a['name'])+' Term'
                    store[a['id']] = []  
                    store[a['id']].append(str(st))
                    store[a['id']].append(str(d['id']))
                    store[a['id']].append(str(a['sessionID']))
                    store[a['id']].append(str(r['classID']))
        return store
    
    def convert(self, r):
        '''
        Prepare the dictionary into two 
        tuple of columnes
        dictionary of values
        
        '''
        self.r = r
        if len(self.r) > 0:
            i = 0
            v = []
            v1 = ''
            v2 = '('
            v3 = '('
            v4 = '('
            v5 = '('
            v6 = ''
            for key in self.r:
                v.append(':'+ str(key))
                if i == 0:
                    v3 += str(key) + ' : '+ str(self.r[key])
                    v4 += '"'+str(self.r[key])+'"'
                    v2 += '"'+ str(key)+'"'
                    v5 += '"'+str(key) + '" = "'+ str(self.r[key])+'"'
                    v6 += '"'+str(key) + '" = "'+ str(self.r[key])+'"'
                    v1 += str(key)
                    i += 1
                else:
                     v3 += ', '+ str(key) + ' : '+ str(self.r[key])
                     v4 += ', "'+ str(self.r[key])+'"'
                     v2 += ', "'+ str(key)+'"'
                     v5 += ' AND "'+ str(key) + '" = "'+ str(self.r[key])+'"'
                     v6 += ' , "'+ str(key) + '" = "'+ str(self.r[key])+'"'
                     v1 += ', '+ str(key) 
                     i += 1
            v2 +=')'
            v3 +=')'
            v4 +=')'
            v5 +=')'
            v6 += ''
            return [v, v1, v2, r, v3, v4, v5, v6]
        else:
            pass
        
    
    def list_to_str(self, a):  
          '''
          convert a list to string
          '''
          self.a = a
          return ", ".join(str(x) for x in self.a)
      
    def list_to_or(self, a, b=[]):
        mainstr = '( '
        i = len(b)
        for n in b:
            i -= 1
            mainstr += a
            mainstr += ' = "'+str(n)+'" '
            if i > 0:
             mainstr += ' OR '
            else:
                pass
        mainstr += ' )'
            
        return mainstr
      
        
    def insert(self, db, a):
        ''' 
        Place interm into specified database content must be in dictionary
        '''
        self.a = a
        self.db = db
        f = self.convert(self.a)
        sql = "INSERT INTO "+ self.db +" "+f[2]+" VALUES "+ f[5] 
        
        num = None
        try:
            conn = sqlite3.connect(self.dbs)
            c = conn.cursor()
            c.execute(sql)
            num = c.lastrowid
            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            print(e)
            
        return num
        
    def update(self, db, a, b):
      
        self.db = db
        self.a = a
        self.b = b
        
        f = self.convert(self.a)
        g = self.convert(self.b) 
        
        sql = "UPDATE "+ self.db +" SET "+f[7]+" WHERE "+g[6]

        self.logConnect(sql)
        
        
    def delete(self, db, whr):
        '''
        select form database tables
        give table name, columns, number of rows,
        '''
        self.db = db
        self.whr = whr
        
        if len(whr) > 0:
            where = self.convert(whr)
            where = str( where[6])
            
            if len(where) > 0:
                wheres = ' WHERE '+ where
            
            sql = "DELETE FROM "+ self.db +" "+ wheres
            self.logConnect(sql)
        else:
            pass;
        
    def select(self, db, col = '', num ='', whr = ''):
        '''
        select form database tables
        give table name, columns, number of rows,
        '''
        self.db = db
        self.col = col
        self.num = num
        self.whr = whr
        where =''
        wheres =''
        
        if col == '':
            column = '*'
        else:
            column = self.list_to_str(self.col)
            
        if not whr == '':
            where = self.convert(whr)
            where = str( where[6])
        else:
            where ='';
            
        if len(where) > 0:
            wheres = ' WHERE '+ where
        
        
        sql = "SELECT "+ column +" FROM "+ self.db +" "+ wheres
       # print(sql)
        
        try:
            conn = sqlite3.connect(self.dbs)
            c = conn.cursor()
            c.execute(sql)
            if (num and int(num) == 1):
                return c.fetchone()
            elif (num and int(num) > 1):
                return c.fetchmany(self.num)
            else:
                return c.fetchall()
                
            conn.close()
        except:
            pass
    
    def selectn(self, db, col = '', num ='', whr = ''):
        '''
        select form database tables
        give table name, columns, number of rows,
        '''
        self.db = db
        self.col = col
        self.num = num
        self.whr = whr
        where =''
        wheres =''
        
        if col == '':
            column = '*'
        else:
            column = self.list_to_str(self.col)
            
        if not whr == '':
            where = self.convert(whr)
            where = str( where[6])
        else:
            where ='';
            
        if len(where) > 0:
            wheres = ' WHERE '+ where
        
        sql = "SELECT "+ column +" FROM "+ self.db +" "+ wheres
        
        
        try:
            conn = sqlite3.connect(self.dbs)
            conn.row_factory = lambda C, R: {c[0]: R[i] for i, c in enumerate(C.description)}
            c = conn.cursor()
            c.execute(sql)
            if (num and int(num) == 1):
                return c.fetchone()
            elif (num and int(num) > 1):
                return c.fetchmany(self.num)
            else:
                return c.fetchall()
                
            conn.close()
        except:
            pass
    
    def selectSearch(self, session,  txt):
        '''
        select form database tables
        give table name, columns, number of rows,
        '''
        #self.db_class = 'students_class'+str(session)
        self.db = 'students'
        self.db_class = 'student_class'+str(session)
        num = ''
        sql = "SELECT `id`, `schno`, `surname`, `firstname`, `othername`, `gender`, (SELECT `classID` FROM `"+ self.db_class +"` WHERE `studentID` =  `students`.`id` LIMIT 1) as cid, (SELECT `abbrv` FROM `datas` WHERE `id` = (SELECT `classID` FROM `"+ self.db_class +"` WHERE `studentID` = `students`.`id` LIMIT 1) LIMIT 1) as classunit, (SELECT `abbrv` FROM `datas` WHERE `id` = (SELECT `subID` FROM `datas` WHERE `id` = (SELECT `classID` FROM `"+ self.db_class +"` WHERE `studentID` = `students`.`id` LIMIT 1) LIMIT 1) LIMIT 1) as classname  FROM `"+ self.db +"` WHERE `surname` LIKE '%"+txt+"%' OR `firstname` LIKE '%"+txt+"%' OR `othername` LIKE '%"+txt+"%' "
       
        
        try:
            conn = sqlite3.connect(self.dbs)
            conn.row_factory = lambda C, R: {c[0]: R[i] for i, c in enumerate(C.description)}
            c = conn.cursor()
            c.execute(sql)
            if (num and int(num) == 1):
                return c.fetchone()
            elif (num and int(num) > 1):
                return c.fetchmany(self.num)
            else:
                return c.fetchall()
                
            conn.close()
        except:
            pass
    
    def selectMultiplen(self, db,  whr):
        '''
        select form database tables
        give table name, columns, number of rows,
        '''
        self.db = db
        self.whr = whr
        where =''
        wheres = self.list_to_or('id', whr)
        

            
        if len(whr) > 0:
            wheres = ' WHERE '+ wheres
            sql = "SELECT * FROM "+ self.db +" "+ wheres
        else:
            wheres = ''
            sql = ''
        
        
        try:
            conn = sqlite3.connect(self.dbs)
            conn.row_factory = lambda C, R: {c[0]: R[i] for i, c in enumerate(C.description)}
            c = conn.cursor()
            c.execute(sql)
            return c.fetchall()
    
            conn.close()
        except:
            pass
        
    def selectStudents(self, students):
        '''
        select form database tables
        give table name, columns, number of rows,
        '''
        students = students
        num = -1
       
        where = self.list_to_or('id', students)
        wheres =''
            
        if len(where) > 0:
            wheres = ' WHERE '+ where
        
        sql = "SELECT id, schno, surname, firstname, othername FROM students "+ wheres
        
        try:
            conn = sqlite3.connect(self.dbs)
            conn.row_factory = lambda C, R: {c[0]: R[i] for i, c in enumerate(C.description)}
            c = conn.cursor()
            c.execute(sql)
            if (num and int(num) == 1):
                return c.fetchone()
            elif (num and int(num) > 1):
                return c.fetchmany(self.num)
            else:
                return c.fetchall()
                
            conn.close()
        except sqlite3.Error as e:
            print(e) 
            
    
        
    def selectStudentClass(self, db, classunit = [], text = None):
        '''
        select form database tables
        give table name, columns, number of rows,
        '''
        
        self.db = db
        self.classunit = classunit
        new1 = ''
        new2 = ''
        new3 = ''
        if len(self.classunit) > 0:
            new = list(set(self.classunit))
            new1 = self.list_to_or('classID', new) 
        else:
            new1 =''
            
        if text and int(text) > -1:
            if len(new1) > 0:
                new3 += ' AND gender = "'+str(int(text) - 1)+'"'
            else:
                new3 += ' gender = "'+str(int(text) - 1)+'"'
            
        if len(new1) > 0:
            new2 = ' WHERE ' + new1 +' '+new3
            
        sql = "SELECT *, `students`.`id` as id, `"+self.db +"`.`id` as cid, (SELECT abbrv FROM datas WHERE id = `"+self.db +"`.`classID` LIMIT 1) as classunitname, (SELECT abbrv FROM datas WHERE id = (SELECT subID FROM datas WHERE id = `"+self.db +"`.`classID` LIMIT 1) LIMIT 1) as classname  FROM  `students`  LEFT JOIN `"+ self.db +"` ON `students`.`id` = `"+self.db+"`.`studentID` "+new2
        #print(sql)
        try:
            conn = sqlite3.connect(self.dbs)
            conn.row_factory = lambda C, R: {c[0]: R[i] for i, c in enumerate(C.description)}
            c = conn.cursor()
            c.execute(sql)
            return c.fetchall()
            conn.close()
        except:
            pass
        
    def selectStudentSelected(self, session, students = []):
        '''
        select form database tables
        give table name, columns, number of rows,
        '''
        self.db = 'student_class'+str(session)
        self.students = students
        print(students)
        #cl = self.select('datas', '', 1, {'id':self.classunit} )
        #print(cl)
        if len(self.students) > 0:
            new = list(set(self.students))
            new1 = self.list_to_or('studentID', new)
            new2 = ' WHERE ' + new1
        else:
            new2 =''
        
        
        sql = "SELECT *, `"+self.db +"`.`id` as cid, (SELECT abbrv FROM datas WHERE id = `"+self.db +"`.`classID` LIMIT 1) as classunitname, (SELECT abbrv FROM datas WHERE id = (SELECT subID FROM datas WHERE id = `"+self.db +"`.`classID` LIMIT 1) LIMIT 1) as classname  FROM  `students`  LEFT JOIN `"+ self.db +"` ON `students`.`id` = `"+self.db+"`.`studentID` "+new2
       
        try:
            conn = sqlite3.connect(self.dbs)
            c = conn.cursor()
            c.execute(sql)
            fil =  c.fetchall()
            conn.close()
            return fil
        except sqlite3.Error as e:
            print(e)
        
    def selectStudentAll(self, session):
        '''
        select form database tables
        give table name, columns, number of rows,
        '''
               
        self.db = 'student_class'+str(session)
                   
        sql = "SELECT *,  `"+self.db +"`.`id` as cid, (SELECT abbrv FROM datas WHERE id = `"+self.db +"`.`classID` LIMIT 1) as classunitname, (SELECT abbrv FROM datas WHERE id = (SELECT subID FROM datas WHERE id = `"+self.db +"`.`classID` LIMIT 1) LIMIT 1) as classname  FROM  `students`  LEFT JOIN `"+ self.db +"` ON `students`.`id` = `"+self.db+"`.`studentID` "
        
        try:
            conn = sqlite3.connect(self.dbs)
            conn.row_factory = lambda C, R: {c[0]: R[i] for i, c in enumerate(C.description)}
            c = conn.cursor()
            c.execute(sql)
            return c.fetchall()
            conn.close()
        except sqlite3.Error as e:
            print(e)
            
    def selectPandas(self, db):
        '''
        select form database tables
        give table name, columns, number of rows,
        '''
                   
        sql = "SELECT * FROM  `"+db+"`"
        
        try:
            conn = sqlite3.connect(self.dbs)
            df = pd.read_sql_query(sql, conn)
            conn.close()
            return df
        except sqlite3.Error as e:
            print(e)
    
    def replacePandas(self, db):
        '''
        select form database tables
        give table name, columns, number of rows,
        '''
        f_path = '_temp/'+db+'.csv'
        try:
            if os.path.isfile(f_path):
                conn = sqlite3.connect(self.dbs)
                df = pd.read_csv(f_path)
                df.to_sql(db, conn , if_exists='replace', index=False)
                conn.close()
                print(f_path)
                return df
            else:
                print('fail')
                pass
        except sqlite3.Error as e:
            print('Error: '+ e)
    
    def selectExpenseDate(self, db, start, end):
        '''
        get expenses by date
        '''
        
        if start == end:
            sql = "SELECT id, amount, expenseID, accountID, datepaid, teller, description, (SELECT name FROM datas WHERE id = expenseID) as expensename, (SELECT name FROM datas WHERE id = accountID) as accountname FROM `"+db+"` WHERE  datepaid >= '"+str(int(start))+"' " 
        else:
            sql = "SELECT id, amount, expenseID, accountID, datepaid, teller, description, (SELECT name FROM datas WHERE id = expenseID) as expensename, (SELECT name FROM datas WHERE id = accountID) as accountname FROM `"+db+"` WHERE  datepaid >= '"+str(int(start))+"' AND datepaid <= '"+str(int(end))+"' "
        
            
        try:
            conn = sqlite3.connect(self.dbs)
            conn.row_factory = lambda C, R: {c[0]: R[i] for i, c in enumerate(C.description)}
            c = conn.cursor()
            c.execute(sql)
            return c.fetchall()
                
            conn.close()
        except sqlite3.Error as e:
            print(e)
       
    def selectStoreDate(self, db, start, end, st = None):
        '''
        get expenses by date
        '''
        wh = ''
        if st:
            wh = ' AND state = '+str(st)
            
        if start == end:
            sql = "SELECT id, amount, itemID, quantity, period, person, state, datepaid, teller, description, (SELECT name FROM datas WHERE id = itemID) as itemname FROM `"+db+"` WHERE  datepaid >= '"+str(int(start))+"' "+wh 
        else:
            sql = "SELECT id, amount, itemID, quantity, period, person, state, datepaid, teller, description, (SELECT name FROM datas WHERE id = itemID) as itemname FROM `"+db+"` WHERE  datepaid >= '"+str(int(start))+"' AND datepaid <= '"+str(int(end))+"' "+wh
        
        try:
            conn = sqlite3.connect(self.dbs)
            conn.row_factory = lambda C, R: {c[0]: R[i] for i, c in enumerate(C.description)}
            c = conn.cursor()
            c.execute(sql)
            return c.fetchall()
                
            conn.close()
        except sqlite3.Error as e:
            print(e)
            
    def selectStoreReturned(self, db, dt):
        '''
        get store
        '''
       
        sql = "SELECT sum(quantity) as qty FROM "+ db +" where state = '5' AND active = "+str(dt)+" GROUP BY itemID  " 
        
        try:
            conn = sqlite3.connect(self.dbs)
            conn.row_factory = lambda C, R: {c[0]: R[i] for i, c in enumerate(C.description)}
            c = conn.cursor()
            c.execute(sql)
            return c.fetchone()
            conn.close()
        except sqlite3.Error as e:
            print(e)
     
    def selectStoreQuantity(self, db, dt):
        '''
        get store
        '''
       
        sql = "SELECT state, itemID, sum(quantity) as qty FROM "+ db +" where `itemID` = "+str(dt)+" GROUP BY state  " 
        
        try:
            conn = sqlite3.connect(self.dbs)
            conn.row_factory = lambda C, R: {c[0]: R[i] for i, c in enumerate(C.description)}
            c = conn.cursor()
            c.execute(sql)
            return c.fetchall()
            conn.close()
        except sqlite3.Error as e:
            print(e)
            
    def selectStudentAllCr(self, session):
        '''
        select form database tables
        give table name, columns, number of rows,
        '''
               
        num = -1
        self.db = 'student_class'+str(session)
                   
        sql = "SELECT *,  `"+self.db +"`.`id` as cid, (SELECT abbrv FROM datas WHERE id = `"+self.db +"`.`classID` LIMIT 1) as classunitname, (SELECT abbrv FROM datas WHERE id = (SELECT subID FROM datas WHERE id = `"+self.db +"`.`classID` LIMIT 1) LIMIT 1) as classname  FROM  `"+ self.db +"`  LEFT JOIN `students` ON `"+self.db+"`.`studentID` = `students`.`id` "
        
        try:
            conn = sqlite3.connect(self.dbs)
            conn.row_factory = lambda C, R: {c[0]: R[i] for i, c in enumerate(C.description)}
            c = conn.cursor()
            c.execute(sql)
            return c.fetchall()
            conn.close()
        except sqlite3.Error as e:
            print(e)
   
    def selectStudentAllEx(self, session):
        '''
        select form database tables
        give table name, columns, number of rows,
        '''
               
     
        self.db = 'student_class'+str(session)
                   
        sql = "SELECT *,  `"+self.db +"`.`id` as cid, (SELECT abbrv FROM datas WHERE id = `"+self.db +"`.`classID` LIMIT 1) as classunitname, (SELECT abbrv FROM datas WHERE id = (SELECT subID FROM datas WHERE id = `"+self.db +"`.`classID` LIMIT 1) LIMIT 1) as classname  FROM `students` LEFT JOIN `"+ self.db +"`  ON `"+self.db+"`.`studentID` = `students`.`id` WHERE `"+self.db +"`.`classID` IS NULL"
      
        try:
            conn = sqlite3.connect(self.dbs)
            conn.row_factory = lambda C, R: {c[0]: R[i] for i, c in enumerate(C.description)}
            c = conn.cursor()
            c.execute(sql)
            return c.fetchall()
            conn.close()
        except sqlite3.Error as e:
            print(e)         
            
    def selectStudentsCa(self, session , student = [], subject = [], ca = []):
        '''
        select form database tables
        give table name, columns, number of rows,
        '''
        self.session = session
        self.student = student
        self.subject = subject
        self.ca = ca
        db = 'student_result'+str(self.session)
        new2 =''
        
        if len(self.student) > 0:
            new = list(set(self.student))
            new1 = self.list_to_or('`students`.`id`', new)
            new2 = new1
        
        if len(self.subject) < 0:
            new = list(set(self.subject))
            new1 = self.list_to_or('`'+db+'`.`subjectID`', new)
            if(len(new) > 0):
                if(len(new2) > 0):
                    new2 += 'AND '+new1
                else:
                    new2 += new1
            else:
                new2 += ' ' + new1
            
        if len(self.ca) > 0:
            new = list(set(self.ca))
            new1 = self.list_to_or('`'+db+'`.`caID`', new)
            if(len(new) > 0):
                if(len(new2) > 0):
                    new2 += 'AND '+new1
                else:
                    new2 += new1
            else:
                new2 += ' ' + new1
                
        new2 = ' WHERE ' + new2
        
        sql = "SELECT `students`.`id` as id, `"+db+"`.`subjectID` as subjectID, `"+db+"`.`caID` as caID, `"+db+"`.`studentID` as studentID, `"+db+"`.`score` as score FROM `students` LEFT JOIN `"+db+"` ON  `"+db+"`.`studentID`=  `students`.`id` "+new2
        
        try:
            conn = sqlite3.connect(self.dbs)
            conn.row_factory = lambda C, R: {c[0]: R[i] for i, c in enumerate(C.description)}
            c = conn.cursor()
            c.execute(sql)
            return c.fetchall()
                
            conn.close()
        except sqlite3.Error as e:
            print(e)

    def selectStudentsCaSum(self, session , student = [], subject = [], ca = []):
        '''
        select form database tables
        give table name, columns, number of rows,
        '''
        self.session = session
        self.student = student
        self.subject = subject
        self.ca = ca
        db = 'student_result'+str(self.session)
        new2 =''
        
        if len(self.student) > 0:
            new = list(set(self.student))
            new1 = self.list_to_or('`students`.`id`', new)
            new2 = new1
        
        if len(self.subject) < 0:
            new = list(set(self.subject))
            new1 = self.list_to_or('`'+db+'`.`subjectID`', new)
            if(len(new) > 0):
                if(len(new2) > 0):
                    new2 += 'AND '+new1
                else:
                    new2 += new1
            else:
                new2 += ' ' + new1
            
        if len(self.ca) > 0:
            new = list(set(self.ca))
            new1 = self.list_to_or('`'+db+'`.`caID`', new)
            if(len(new) > 0):
                if(len(new2) > 0):
                    new2 += 'AND '+new1
                else:
                    new2 += new1
            else:
                new2 += ' ' + new1
                
        new2 = ' WHERE ' + new2
        
        sql = "SELECT `students`.`id` as id, `"+db+"`.`subjectID` as subjectID, GROUP_CONCAT(`"+db+"`.`caID`) as caID, `"+db+"`.`studentID` as studentID, SUM(`"+db+"`.`score`) as score FROM `students` LEFT JOIN `"+db+"` ON  `"+db+"`.`studentID`=  `students`.`id` "+new2+" GROUP BY `students`.`id`, `"+db+"`.`subjectID` "
        
        try:
            conn = sqlite3.connect(self.dbs)
            conn.row_factory = lambda C, R: {c[0]: R[i] for i, c in enumerate(C.description)}
            c = conn.cursor()
            c.execute(sql)
            return c.fetchall()
                
            conn.close()
        except sqlite3.Error as e:
            print(e)
    
    def selectStudentsCaRep(self, session , student = [], subject = [], ca = []):
        '''
        select form database tables
        give table name, columns, number of rows,
        '''
        self.session = session
        self.student = student
        self.subject = subject
        self.ca = ca
        db = 'student_result'+str(self.session)
        new2 =''
        
        if len(self.student) > 0:
            new = list(set(self.student))
            new1 = self.list_to_or('`students`.`id`', new)
            new2 = new1
        
        if len(self.subject) < 0:
            new = list(set(self.subject))
            new1 = self.list_to_or('`'+db+'`.`subjectID`', new)
            if(len(new) > 0):
                new2 += ' AND ' + new1
            else:
                new2 += ' ' + new1
            
        if len(self.ca) > 0:
            new = list(set(self.ca))
            new1 = self.list_to_or('`'+db+'`.`caID`', new)
            if(len(new) > 0):
                if(len(new2) > 0):
                    new2 += 'AND '+new1
                else:
                    new2 += new1
            else:
                new2 += ' ' + new1
                
        new2 = ' WHERE ' + new2
        
        
        sql = "SELECT `students`.`id` as id, `"+db+"`.`subjectID` as subjectID, `"+db+"`.`caID` as caID, `"+db+"`.`studentID` as studentID, `"+db+"`.`score` as score, (SELECT abbrv FROM datas WHERE `name`= `caID` AND `pubID`="+str(self.session)+" ) as mmax FROM `students` LEFT JOIN `"+db+"` ON  `"+db+"`.`studentID`=  `students`.`id` "+new2
    
        try:
            conn = sqlite3.connect(self.dbs)
            conn.row_factory = lambda C, R: {c[0]: R[i] for i, c in enumerate(C.description)}
            c = conn.cursor()
            c.execute(sql)
            return c.fetchall()
                
            conn.close()
        except sqlite3.Error as e:
            print(e)
            
    def selectStudentsAffective(self, session , student = [], subject = [], ca = []):
        '''
        select form database tables
        give table name, columns, number of rows,
        '''
        self.session = session
        self.student = student
        self.subject = subject
        self.ca = ca
        db = 'student_affective'+str(self.session)
        new2 =''
        
        if len(self.student) > 0:
            new = list(set(self.student))
            new1 = self.list_to_or('`students`.`id`', new)
            new2 = new1
        
            
        if len(self.ca) > 0:
            new = list(set(self.ca))
            new1 = self.list_to_or('`'+db+'`.`caID`', new)
            if(len(new) > 0):
                if(len(new2) > 0):
                    new2 += 'AND '+new1
                else:
                    new2 += new1
            else:
                new2 += ' ' + new1
                
        new2 = ' WHERE ' + new2
        
        
        sql = "SELECT `students`.`id` as id, `"+db+"`.`caID` as caID, (SELECT subID FROM datas WHERE id = caID LIMIT 1) AS subjectID, `"+db+"`.`studentID` as studentID, `"+db+"`.`score` as score FROM `students` LEFT JOIN `"+db+"` ON  `"+db+"`.`studentID`=  `students`.`id` "+new2
        
        try:
            conn = sqlite3.connect(self.dbs)
            conn.row_factory = lambda C, R: {c[0]: R[i] for i, c in enumerate(C.description)}
            c = conn.cursor()
            c.execute(sql)
            return c.fetchall()
                
            conn.close()
        except sqlite3.Error as e:
            print(e)      
    def selectStudentsAffectiveSum(self, session , student = [], subject = [], ca = []):
        '''
        select form database tables
        give table name, columns, number of rows,
        '''
        self.session = session
        self.student = student
        self.subject = subject
        self.ca = ca
        db = 'student_affective'+str(self.session)
        new2 =''
        
        if len(self.student) > 0:
            new = list(set(self.student))
            new1 = self.list_to_or('`students`.`id`', new)
            new2 = new1
        
            
        if len(self.ca) > 0:
            new = list(set(self.ca))
            new1 = self.list_to_or('`P`.`caID`', new)
            if(len(new) > 0):
                if(len(new2) > 0):
                    new2 += 'AND '+new1
                else:
                    new2 += new1
            else:
                new2 += ' ' + new1
                
        new2 = ' WHERE ' + new2
        
        inner = '(SELECT score, caID, studentID, (SELECT subID FROM datas WHERE id = caID LIMIT 1) as pID FROM '+db+' ) AS P';
        
        sql = "SELECT `students`.`id` as id, `P`.`pID` as caID, GROUP_CONCAT(`P`.`caID`) as caIDs,GROUP_CONCAT(`P`.`score`) as vals, `P`.`studentID` as studentID, COUNT( `P`.`score`) as num, AVG( `P`.`score`) as score FROM `students` LEFT JOIN "+inner+" ON  `P`.`studentID`=  `students`.`id` "+new2+" GROUP BY P.pID, P.studentID"
        #print(sql)
        try:
            conn = sqlite3.connect(self.dbs)
            conn.row_factory = lambda C, R: {c[0]: R[i] for i, c in enumerate(C.description)}
            c = conn.cursor()
            c.execute(sql)
            return c.fetchall()
                
            conn.close()
        except sqlite3.Error as e:
            print(e)      
    
    def selectStudentsPsychomoto(self, session , student = [], subject = [], ca = []):
        '''
        select form database tables
        give table name, columns, number of rows,
        '''
        self.session = session
        self.student = student
        self.subject = subject
        self.ca = ca
        db = 'student_psy'+str(self.session)
        new2 =''
        
        if len(self.student) > 0:
            new = list(set(self.student))
            new1 = self.list_to_or('`students`.`id`', new)
            new2 = new1
        
            
        if len(self.ca) > 0:
            new = list(set(self.ca))
            new1 = self.list_to_or('`'+db+'`.`caID`', new)
            if(len(new) > 0):
                if(len(new2) > 0):
                    new2 += 'AND '+new1
                else:
                    new2 += new1
            else:
                new2 += ' ' + new1
                
        new2 = ' WHERE ' + new2
        
        
        sql = "SELECT `students`.`id` as id, `"+db+"`.`caID` as caID, (SELECT subID FROM datas WHERE id = caID LIMIT 1) AS subjectID, `"+db+"`.`studentID` as studentID, `"+db+"`.`score` as score FROM `students` LEFT JOIN `"+db+"` ON  `"+db+"`.`studentID`=  `students`.`id` "+new2
        try:
            conn = sqlite3.connect(self.dbs)
            conn.row_factory = lambda C, R: {c[0]: R[i] for i, c in enumerate(C.description)}
            c = conn.cursor()
            c.execute(sql)
            return c.fetchall()
                
            conn.close()
        except sqlite3.Error as e:
            print(e)   
    def selectStudentsPsychomotoSum(self, session , student = [], subject = [], ca = []):
        '''
        select form database tables
        give table name, columns, number of rows,
        '''
        self.session = session
        self.student = student
        self.subject = subject
        self.ca = ca
        db = 'student_psy'+str(self.session)
        new2 =''
        
        if len(self.student) > 0:
            new = list(set(self.student))
            new1 = self.list_to_or('`students`.`id`', new)
            new2 = new1
        
            
        if len(self.ca) > 0:
            new = list(set(self.ca))
            new1 = self.list_to_or('`P`.`caID`', new)
            if(len(new) > 0):
                if(len(new2) > 0):
                    new2 += 'AND '+new1
                else:
                    new2 += new1
            else:
                new2 += ' ' + new1
                
        new2 = ' WHERE ' + new2
        
        inner = '(SELECT score, caID, studentID, (SELECT subID FROM datas WHERE id = caID LIMIT 1) as pID FROM '+db+' ) AS P';
        
        sql = "SELECT `students`.`id` as id, `P`.`pID` as caID, GROUP_CONCAT(`P`.`caID`) as caIDs,GROUP_CONCAT(`P`.`score`) as vals, `P`.`studentID` as studentID, COUNT( `P`.`score`) as num, AVG( `P`.`score`) as score FROM `students` LEFT JOIN "+inner+" ON  `P`.`studentID`=  `students`.`id` "+new2+" GROUP BY P.pID, P.studentID"
        #print(sql)
        try:
            conn = sqlite3.connect(self.dbs)
            conn.row_factory = lambda C, R: {c[0]: R[i] for i, c in enumerate(C.description)}
            c = conn.cursor()
            c.execute(sql)
            return c.fetchall()
                
            conn.close()
        except sqlite3.Error as e:
            print(e)        
    def selectStudentClassxx(self, db, classunit = []):
        '''
        select form database tables
        give table name, columns, number of rows,
        '''
        self.db = db
        self.classunit = classunit
        #cl = self.select('datas', '', 1, {'id':self.classunit} )
        #print(cl)
        if len(self.classunit) > 0:
            new = list(set(self.classunit))
            new1 = self.list_to_or('classID', new)
            new2 = ' WHERE ' + new1
        else:
            new2 =''
        
        
        sql = "SELECT *, `"+self.db +"`.`id` as cid, (SELECT abbrv FROM datas WHERE id = `"+self.db +"`.`classID` LIMIT 1) as classunitname, (SELECT abbrv FROM datas WHERE id = (SELECT subID FROM datas WHERE id = `"+self.db +"`.`classID` LIMIT 1) LIMIT 1) as classname  FROM  `students`  LEFT JOIN `"+ self.db +"` ON `students`.`id` = `"+self.db+"`.`studentID` "+new2
        #print(sql)
        try:
            conn = sqlite3.connect(self.dbs)
            c = conn.cursor()
            c.execute(sql)
            fil =  c.fetchall()
            conn.close()
            return fil
        except:
            pass
        
    def studentScore(self, session , student, subject, ca, value):
        '''
        select form database tables
        give table name, columns, number of rows,
        '''
        _session = session
        _student = student
        _subject = subject
        _ca = ca
        _value = value
        
        db = 'student_result'+str(_session)
        
        try:
            if(float(_value) and float(_value) > 0):
                #confirm if exist
                v = self.selectn(db, '', 1, {'studentID':_student, 'subjectID':_subject, 'caID':_ca })
                
                if(v and int(v['id']) > 0):
                    self.update(db, {'score':_value}, {'id':v['id']})
                    return 1
                else:
                    self.insert(db, {'studentID':_student, 'subjectID':_subject, 'caID':_ca , 'score':_value})
                    return 1
            else:
                 v = self.selectn(db, '', 1, {'studentID':_student, 'subjectID':_subject, 'caID':_ca })
                 if(v and int(v['id']) > 0):
                    self.delete(db,{'id':v['id']})
                    return 1
                 else:
                    return 'x';
        except:
            return 'y'
        
    def studentAffect(self, session , student, subject, ca, value):
        '''
        select form database tables
        give table name, columns, number of rows,
        '''
        _session = session
        _student = student
        _subject = subject
        _ca = ca
        _value = value
        
        db = 'student_affective'+str(_session)
        
        try:
            if(float(_value) and float(_value) > 0):
                #confirm if exist
                v = self.selectn(db, '', 1, {'studentID':_student, 'caID':_ca })
                
                if(v and int(v['id']) > 0):
                    self.update(db, {'score':_value}, {'id':v['id']})
                    return 1
                else:
                    self.insert(db, {'studentID':_student,  'caID':_ca , 'score':_value})
                    return 1
            else:
                 v = self.selectn(db, '', 1, {'studentID':_student,  'caID':_ca })
                 if(v and int(v['id']) > 0):
                    self.delete(db,{'id':v['id']})
                    return 1
                 else:
                    return 'x';
        except:
            return 'y'
        
        
    def studentPsy(self, session , student, subject, ca, value):
        '''
        select form database tables
        give table name, columns, number of rows,
        '''
        _session = session
        _student = student
        _subject = subject
        _ca = ca
        _value = value
        
        db = 'student_psy'+str(_session)
        
        try:
            if(float(_value) and float(_value) > 0):
                #confirm if exist
                v = self.selectn(db, '', 1, {'studentID':_student, 'caID':_ca })
                
                if(v and int(v['id']) > 0):
                    self.update(db, {'score':_value}, {'id':v['id']})
                    return 1
                else:
                    self.insert(db, {'studentID':_student,  'caID':_ca , 'score':_value})
                    return 1
            else:
                 v = self.selectn(db, '', 1, {'studentID':_student,  'caID':_ca })
                 if(v and int(v['id']) > 0):
                    self.delete(db,{'id':v['id']})
                    return 1
                 else:
                    return 'x';
        except:
            return 'y'
     
    
    def sendMail(self, to_addr_list, subject, message):
        smtpserver='smtp.gmail.com:587'
        login = 'doyinspc2@gmail.com'
        password = 'james414'
        from_addr = 'doyinspc2@gmail.com'
        header  = 'From: %s' % from_addr
        header += 'To: %s' % ','.join(to_addr_list)
        header += 'Subject: %s' % subject
        message = header + message
     
        server = smtplib.SMTP(smtpserver)
        server.starttls()
        server.login(login,password)
        try:
            e = server.sendmail(from_addr, to_addr_list, message)
        except e:
            return e
        server.quit()
        return e
        
        
        
        
                
 
        