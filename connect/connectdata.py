# -*- coding: utf-8 -*-
"""
Created on Fri Dec 28 03:28:08 2018

@author: CHARLES
"""
import sqlite3

class Dat(object):
    dbs = 'test.db';
    def studentClassUnitData(self, session):
        '''
        get number of student in class
        '''
        db = 'student_class'+str(session)

        sql = "SELECT COUNT (id) as id, sex, cid, (SELECT name FROM datas WHERE id = cid LIMIT 1) as classname, (SELECT name FROM datas WHERE id = (SELECT subID FROM datas WHERE id = cid LIMIT 1)) as clasz FROM (SELECT students.id as id, students.gender as sex, "+ db +".classID as cid FROM "+ db +" LEFT JOIN students ON "+ db +".studentID = students.id) GROUP BY sex, cid "

        try:
            conn = sqlite3.connect(self.dbs)
            conn.row_factory = lambda C, R: {c[0]: R[i] for i, c in enumerate(C.description)}
            c = conn.cursor()
            c.execute(sql)
            return c.fetchall()
            conn.close()
        except sqlite3.Error as e:
            print(e)
            
    def studentClassFee(self, session):
        '''
        get number of student in class
        '''
        db = 'student_class'+str(session)
        
        sql = "SELECT UNIQUE(P.id) as id, P.sex as sex, P.cid, P.classname, P.classID, P.clasz, datas.abbrv as fee, sum(datas.description) as amount FROM (SELECT COUNT (id) as id, sex, cid, (SELECT name FROM datas WHERE id = cid LIMIT 1) as classname, (SELECT subID FROM datas WHERE id = cid LIMIT 1) as classID, (SELECT name FROM datas WHERE id = (SELECT subID FROM datas WHERE id = cid LIMIT 1)) as clasz FROM (SELECT students.id as id, students.gender as sex, "+ db +".classID as cid FROM "+ db +" LEFT JOIN students ON "+ db +".studentID = students.id) GROUP BY sex, cid) as P LEFT JOIN `datas` ON  `P`.`classID` = `datas`.`name` WHERE `datas`.`pubID` = 'fee' and `datas`.`subID` = "+str(session)+" GROUP BY P.classID, P.sex "
        
        try:
            conn = sqlite3.connect(self.dbs)
            conn.row_factory = lambda C, R: {c[0]: R[i] for i, c in enumerate(C.description)}
            c = conn.cursor()
            c.execute(sql)
            return c.fetchall()
            conn.close()
        except sqlite3.Error as e:
            print(e)
    
    def studentClassUnitFee(self, session):
        '''
        get number of student in class
        '''
        db = 'student_class'+str(session)
        db_pay = 'student_pay'+str(session)
              
        sql = "SELECT P.name as name, P.id as id, P.sex as sex, P.cid, P.classname, P.classID, P.clasz, COUNT(datas.abbrv) as fee, SUM(datas.description) as amount, SUM(pay) as pay FROM datas LEFT JOIN (SELECT CONCAT(surname,'',firstname) as name, COUNT (id) as id, sex, cid, (SELECT name FROM datas WHERE id = cid LIMIT 1) as classname, (SELECT subID FROM datas WHERE id = cid LIMIT 1) as classID, (SELECT name FROM datas WHERE id = (SELECT subID FROM datas WHERE id = cid LIMIT 1)) as clasz, sum(pay) as pay FROM (SELECT students.id as id, students.gender as sex, "+ db +".classID as cid, (SELECT SUM(amount) as pay FROM "+ db_pay +" WHERE studentID ="+ db +".studentID) as pay  FROM "+ db +" LEFT JOIN students ON "+ db +".studentID = students.id) GROUP BY cid, sex) AS P ON  `P`.`classID` = `datas`.`name` WHERE `datas`.`pubID` = 'fee' and `datas`.`subID` = "+str(session)+" GROUP BY P.cid, sex  "
        
        try:
            conn = sqlite3.connect(self.dbs)
            conn.row_factory = lambda C, R: {c[0]: R[i] for i, c in enumerate(C.description)}
            c = conn.cursor()
            c.execute(sql)
            return c.fetchall()
            conn.close()
        except sqlite3.Error as e:
            print(e)
       
    def classUnitPay(self, session, students, state):
        '''
        get number of student in class
        '''
        db_pay = 'student_pay'+str(session)
        db_fee = 'student_fee'+str(session)
        students_list = ', '.join(str(e) for e in students)
        whr = 'WHERE studentID in ('+students_list+')'
         
        if state == 0: 
            sql = "SELECT studentID, sum(amount) as amount FROM "+db_pay+" "+whr+" GROUP BY studentID"
        elif state == 1:
            sql = "SELECT studentID, feeID, amount FROM "+db_pay+" "+whr+" "
        elif state == 2:
            sql = "SELECT studentID, sum(amount) as amount FROM "+db_fee+" "+whr+" GROUP BY studentID"
        elif state == 3:
            sql = "SELECT studentID, feeID, sum(amount) as amount FROM "+db_fee+" "+whr+"GROUP BY studentID, feeID "
            
        try:
            conn = sqlite3.connect(self.dbs)
            conn.row_factory = lambda C, R: {c[0]: R[i] for i, c in enumerate(C.description)}
            c = conn.cursor()
            c.execute(sql)
            return c.fetchall()
            conn.close()
        except sqlite3.Error as e:
            print(e)
    
    def classUnitSubject(self, session, students):
        '''
        get number of student in class
        '''
        db_subject = 'student_subject'+str(session)
        db_class = 'student_class'+str(session)
        students_list = ', '.join(str(e) for e in students)
        whr = 'WHERE `'+db_subject+'`.studentID in ('+students_list+')'
          
        sql = "SELECT `"+ db_subject +"`.`studentID`, classID, (SELECT abbrv FROM datas WHERE id = (SELECT subID FROM datas WHERE id = `"+ db_class +"`.`classID` LIMIT 1)) as classname,  (SELECT abbrv FROM datas WHERE id = `"+ db_class +"`.`classID`) as classunit, GROUP_CONCAT((SELECT `name` FROM `datas` WHERE `id` =`"+db_subject+"`. `subjectID` limit 1)) as subjects FROM `"+db_subject+"` LEFT JOIN `"+db_class+"` ON `"+db_subject+"`.`studentID` = `"+db_class+"`.`studentID` "+whr+" GROUP BY `"+db_subject+"`.`studentID`"
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
    
    def expensesData(self, session, start, end):
        '''
        get number of student in class
        '''
        db = 'school_expenses'+str(session)
          
        if start == end:
            sql = "SELECT expenseID, COUNT(id) as transactions,  (SELECT `name` FROM `datas` WHERE id = expenseID LIMIT 1 ) as expenseName,   sum(amount) as amount FROM `"+ db +"` WHERE  datepaid >= '"+str(int(start))+"' GROUP BY expenseID"
        else:
            sql = "SELECT expenseID, COUNT(id) as transactions, (SELECT `name` FROM `datas` WHERE id = expenseID LIMIT 1 ) as expenseName,   sum(amount) as amount FROM `"+ db +"` WHERE  CAST(datepaid AS REAL) >= "+str(int(start))+" AND CAST(datepaid AS REAL) <= "+str(int(end))+" GROUP BY expenseID"
           
        try:
            conn = sqlite3.connect(self.dbs)
            conn.row_factory = lambda C, R: {c[0]: R[i] for i, c in enumerate(C.description)}
            c = conn.cursor()
            c.execute(sql)
            return c.fetchall()
            conn.close()
        except sqlite3.Error as e:
            print(e)
            
    def storesData(self, session, start, end):
        '''
        get number of student in class
        '''
        db = 'school_stores'+str(session)
          
        if start == end:
            sql = "SELECT itemID, state, COUNT(id) as num, (SELECT `name` FROM `datas` WHERE id = itemID LIMIT 1 ) as itemname, sum(quantity) as quantity, (SELECT amount FROM `"+ db +"` WHERE itemID = itemID ORDER BY id ASC LIMIT 1) AS datesamount FROM `"+ db +"` WHERE  datepaid >= '"+str(int(start))+"' GROUP BY itemID, state"
        else:
            sql = "SELECT itemID, state, COUNT(id) as num, (SELECT `name` FROM `datas` WHERE id = itemID LIMIT 1 ) as itemname, sum(quantity) as quantity, (SELECT amount FROM `"+ db +"` WHERE itemID = itemID ORDER BY id ASC LIMIT 1) AS datesamount FROM `"+ db +"` WHERE  CAST(datepaid AS REAL) >= "+str(int(start))+" AND CAST(datepaid AS REAL) <= "+str(int(end))+" GROUP BY itemID, state"
           
        try:
            conn = sqlite3.connect(self.dbs)
            conn.row_factory = lambda C, R: {c[0]: R[i] for i, c in enumerate(C.description)}
            c = conn.cursor()
            c.execute(sql)
            return c.fetchall()
            conn.close()
        except sqlite3.Error as e:
            print(e)
            
    def accountsData(self, session, start, end):
        '''
        get number of student in class
        '''
        db = 'school_expenses'+str(session)
          
        if start == end:
            sql = "SELECT accountID as expenseID, COUNT(id) as transactions,  (SELECT `name` FROM `datas` WHERE id = accountID LIMIT 1 ) as expenseName,   sum(amount) as amount FROM `"+ db +"` WHERE  datepaid >= '"+str(int(start))+"' GROUP BY accountID"
        else:
            sql = "SELECT accountID as expenseID, COUNT(id) as transactions, (SELECT `name` FROM `datas` WHERE id = accountID LIMIT 1 ) as expenseName,   sum(amount) as amount FROM `"+ db +"` WHERE  CAST(datepaid AS REAL) >= "+str(int(start))+" AND CAST(datepaid AS REAL) <= "+str(int(end))+" GROUP BY accountID"
           
        try:
            conn = sqlite3.connect(self.dbs)
            conn.row_factory = lambda C, R: {c[0]: R[i] for i, c in enumerate(C.description)}
            c = conn.cursor()
            c.execute(sql)
            return c.fetchall()
            conn.close()
        except sqlite3.Error as e:
            print(e)
            
    def mailsData(self, session, start, end):
        '''
        get number of student in class
        '''
        db = 'school_mails'+str(session)
          
        if start == end:
            sql = "SELECT studentID as expenseID, COUNT(id) as transactions, (SELECT (surname || \" \" || firstname) as name  FROM `students` WHERE id = studentID LIMIT 1 ) as expenseName FROM `"+ db +"` WHERE  datepaid >= '"+str(int(start))+"' GROUP BY studentID"
        else:
            sql = "SELECT studentID as expenseID, COUNT(id) as transactions, (SELECT (surname || \" \" || firstname) as name FROM `students` WHERE id = studentID LIMIT 1 ) as expenseName FROM `"+ db +"` WHERE  CAST(datepaid AS REAL) >= "+str(int(start))+" AND CAST(datepaid AS REAL) <= "+str(int(end))+" GROUP BY studentID"
           
        try:
            conn = sqlite3.connect(self.dbs)
            conn.row_factory = lambda C, R: {c[0]: R[i] for i, c in enumerate(C.description)}
            c = conn.cursor()
            c.execute(sql)
            return c.fetchall()
            conn.close()
        except sqlite3.Error as e:
            print(e)
    
    def conductsData(self, session, start, end):
        '''
        get number of student in class
        '''
        db = 'school_conducts'+str(session)
          
        if start == end:
            sql = "SELECT studentID as expenseID, COUNT(id) as transactions, (SELECT (surname || \" \" || firstname) as name  FROM `students` WHERE id = studentID LIMIT 1 ) as expenseName FROM `"+ db +"` WHERE  datepaid >= '"+str(int(start))+"' GROUP BY studentID"
        else:
            sql = "SELECT studentID as expenseID, COUNT(id) as transactions, (SELECT (surname || \" \" || firstname) as name FROM `students` WHERE id = studentID LIMIT 1 ) as expenseName FROM `"+ db +"` WHERE  CAST(datepaid AS REAL) >= "+str(int(start))+" AND CAST(datepaid AS REAL) <= "+str(int(end))+" GROUP BY studentID"
           
        try:
            conn = sqlite3.connect(self.dbs)
            conn.row_factory = lambda C, R: {c[0]: R[i] for i, c in enumerate(C.description)}
            c = conn.cursor()
            c.execute(sql)
            return c.fetchall()
            conn.close()
        except sqlite3.Error as e:
            print(e)
            
    def misconductsData(self, session, start, end):
        '''
        get number of student in class
        '''
        db = 'school_conducts'+str(session)
          
        if start == end:
            sql = "SELECT studentID as expenseID, COUNT(id) as transactions, (SELECT (surname || \" \" || firstname) as name  FROM `students` WHERE id = studentID LIMIT 1 ) as expenseName FROM `"+ db +"` WHERE  datepaid >= '"+str(int(start))+"' GROUP BY studentID"
        else:
            sql = "SELECT studentID as expenseID, COUNT(id) as transactions, (SELECT (surname || \" \" || firstname) as name FROM `students` WHERE id = studentID LIMIT 1 ) as expenseName FROM `"+ db +"` WHERE  CAST(datepaid AS REAL) >= "+str(int(start))+" AND CAST(datepaid AS REAL) <= "+str(int(end))+" GROUP BY studentID"
           
        try:
            conn = sqlite3.connect(self.dbs)
            conn.row_factory = lambda C, R: {c[0]: R[i] for i, c in enumerate(C.description)}
            c = conn.cursor()
            c.execute(sql)
            return c.fetchall()
            conn.close()
        except sqlite3.Error as e:
            print(e)
    
    def getSubData(self, rows,  state, session, start, end):
        '''
        get number of student in class
        '''
        
        sql = ''
        if state == 1:
            db = 'school_expenses'+str(session)
            lists = ', '.join(str(e) for e in rows)
            whr = 'expenseID in ('+lists+')'
            whr1 = "CAST(datepaid AS REAL) >= "+str(int(start))+" AND CAST(datepaid AS REAL) <= "+str(int(end))+" "
            whrs = " WHERE "+whr +" AND "+whr1
            sql = "SELECT id, datepaid, teller, expenseID, accountID, description, amount, (SELECT `name` FROM `datas` WHERE id = expenseID LIMIT 1) as expensename, (SELECT `name` FROM `datas` WHERE id = accountID LIMIT 1) as accountname FROM `"+ db +"` "+whrs
        
        elif state == 2:
            db = 'school_expenses'+str(session)
            lists = ', '.join(str(e) for e in rows)
            whr = 'accountID in ('+lists+')'
            whr1 = "CAST(datepaid AS REAL) >= "+str(int(start))+" AND CAST(datepaid AS REAL) <= "+str(int(end))+" "
            whrs = " WHERE "+whr +" AND "+whr1
            sql = "SELECT id, datepaid, teller, expenseID, accountID, description, amount, (SELECT `name` FROM `datas` WHERE id = expenseID LIMIT 1) as expensename, (SELECT `name` FROM `datas` WHERE id = accountID LIMIT 1) as accountname FROM `"+ db +"` "+whrs
            
        elif state == 3:
            db = 'school_mails'+str(session)
            lists = ', '.join(str(e) for e in rows)
            whr = 'studentID in ('+lists+')'
            whr1 = "CAST(datepaid AS REAL) >= "+str(int(start))+" AND CAST(datepaid AS REAL) <= "+str(int(end))+" "
            whrs = " WHERE "+whr +" AND "+whr1
            sql = "SELECT id, subject, message, datepaid,  (SELECT (surname || \" \" || firstname) as name FROM students WHERE id = studentID LIMIT 1) as name FROM `"+ db +"` "+whrs
            
        elif state == 4:
            db = 'school_conducts'+str(session)
            lists = ', '.join(str(e) for e in rows)
            whr = 'studentID in ('+lists+')'
            whr1 = "CAST(datepaid AS REAL) >= "+str(int(start))+" AND CAST(datepaid AS REAL) <= "+str(int(end))+" "
            whrs = " WHERE "+whr +" AND "+whr1
            sql = "SELECT id, action, reaction, datepaid,  staffname as staff,  (SELECT (surname || \" \" || firstname) as name FROM students WHERE id = studentID LIMIT 1) as name FROM `"+ db +"` "+whrs+" AND state = 0"
                
        elif state == 5:
            db = 'school_conducts'+str(session)
            lists = ', '.join(str(e) for e in rows)
            whr = 'studentID in ('+lists+')'
            whr1 = "CAST(datepaid AS REAL) >= "+str(int(start))+" AND CAST(datepaid AS REAL) <= "+str(int(end))+" "
            whrs = " WHERE "+whr +" AND "+whr1
            sql = "SELECT id, action, reaction, datepaid,  staffname as staff,  (SELECT (surname || \" \" || firstname) as name FROM students WHERE id = studentID LIMIT 1) as name FROM `"+ db +"` "+whrs+" AND state = 1"
        
        elif state == 6:
            db = 'school_stores'+str(session)
            lists = ', '.join(str(e) for e in rows)
            whr = 'itemID in ('+lists+')'
            whr1 = "CAST(datepaid AS REAL) >= "+str(int(start))+" AND CAST(datepaid AS REAL) <= "+str(int(end))+" "
            whrs = " WHERE "+whr +" AND "+whr1
            sql = "SELECT id, quantity, amount, person, datepaid, itemID, state, (SELECT `name` FROM `datas` WHERE id = itemID LIMIT 1) as name  FROM `"+ db +"` "+whrs
           
        elif state == 7:
            db_class = 'student_class'+str(session)
            db_fee = 'student_fee'+str(session)
            db_pay = 'student_pay'+str(session)
            db = 'students'
            lists = ', '.join(str(e) for e in rows)
            whr = 'classID in ('+lists+')'
            ar = '(SELECT abbrv FROM datas WHERE id = (SELECT subID FROM datas WHERE datas.id = classID LIMIT 1 ) LIMIT 1 ) as ar'
            ca = '(SELECT abbrv FROM datas WHERE datas.id = classID LIMIT 1 ) as ca'
            fe = '(SELECT SUM(amount) as fee FROM `'+ db_fee +'` WHERE studentID = `'+ db_class +'`.`studentID` GROUP BY studentID ) as fee'
            pa = '(SELECT SUM(amount) as pay FROM `'+ db_pay +'` WHERE studentID = `'+ db_class +'`.`studentID` GROUP BY studentID ) as pay'
            whrs = " WHERE "+whr 
            sql = "SELECT students.id, schno, gender, (surname || \" \" || firstname || \" \" || othername) as name,"+ ar +", "+ ca +", "+ fe +", "+ pa +"  FROM `"+ db_class +"` LEFT JOIN `students` ON  `"+ db_class +"`.`studentID` = `students`.`id` "+whrs+" GROUP BY studentID ORDER BY surname, firstname"
        elif state == 8:
            db_class = 'student_class'+str(session)
            db = 'students'
            lists = ', '.join(str(e) for e in rows)
            whr = 'classID in ('+lists+')'
            ar = '(SELECT abbrv FROM datas WHERE id = (SELECT subID FROM datas WHERE datas.id = classID LIMIT 1 ) LIMIT 1 ) as ar'
            ca = '(SELECT abbrv FROM datas WHERE datas.id = classID LIMIT 1 ) as ca'
            whrs = " WHERE "+whr 
            sql = "SELECT *, students.id as sid, (surname || \" \" || firstname || \" \" || othername) as name,"+ ar +", "+ ca +"  FROM `"+ db_class +"` LEFT JOIN `students` ON  `"+ db_class +"`.`studentID` = `students`.`id` "+whrs+" GROUP BY studentID ORDER BY surname, firstname"
            
        try:
            conn = sqlite3.connect(self.dbs)
            conn.row_factory = lambda C, R: {c[0]: R[i] for i, c in enumerate(C.description)}
            c = conn.cursor()
            c.execute(sql)
            return c.fetchall()
            conn.close()
        except sqlite3.Error as e:
            print(e)
    