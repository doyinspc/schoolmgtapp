# -*- coding: utf-8 -*-
"""
Created on Sun Jun 24 08:58:36 2018

@author: CHARLES
"""

class Tables:
    
    def session(self):
        return  "CREATE TABLE IF NOT EXISTS session (id integer PRIMARY KEY AUTOINCREMENT, name text UNIQUE, start_date int, end_date int, active boolean NULL) " 
    
    def terms(self):
        return  "CREATE TABLE IF NOT EXISTS terms (id integer PRIMARY KEY AUTOINCREMENT, name text,  sessionID int,   start_date int, end_date int, active boolean)" 
        
    def students(self):
       return  "CREATE TABLE IF NOT EXISTS students (id integer PRIMARY KEY AUTOINCREMENT, schno text, surname text, firstname text, othername text NULL, addr text NULL, gender boolean NOT NULL, pix int, pix1 TEXT, pix2 TEXT, pix3 TEXT, soo text NULL, lga text NULL, nation text NULL, dob text NULL, admit text NULL, g1 text NULL, g2 text NULL, g1rel text NULL, g2rel text NULL, g1p1 text null, g1p2 text NULL, g2p1 text NULL, g2p2 text NULL, g1email text NULL, g2email text NULL, g1addr text NULL, g2addr text NULL, reason text NULL, active boolean NOT NULL ) "
     
    def datas(self):
       return  "CREATE TABLE IF NOT EXISTS datas (id integer PRIMARY KEY AUTOINCREMENT, subID int NULL, name text, abbrv text, active boolean NULL) "
   
    def studentClasz(self, term):
        self.term = term
        if self.term > 0:
            table = 'student_class' +str( self.term)
            return  "CREATE TABLE IF NOT EXISTS "+ table  +" (id integer PRIMARY KEY AUTOINCREMENT, studentID int, classID int, active boolean NULL) "
        else:
            pass
        
    def studentSubjects(self, term):
        self.term = term
        if self.term > 0:
            table = 'student_subject' +str( self.term)
            return  "CREATE TABLE IF NOT EXISTS "+ table  +" (id integer PRIMARY KEY AUTOINCREMENT, studentID int, subjectID int, active boolean NULL) "
        else:
            pass
        
    def studentResult(self, term):
        self.term = term
        if self.term > 0:
            table = 'student_result' + str(self.term)
            return  "CREATE TABLE IF NOT EXISTS "+ table  +" (id integer PRIMARY KEY AUTOINCREMENT, studentID int, subjectID int, caID int, score real, active boolean NULL) "
        else:
            pass
        
    def studentAffective(self, term):
        self.term = term
        if self.term > 0:
            table = 'student_affective' + str(self.term)
            return  "CREATE TABLE IF NOT EXISTS "+ table  +" (id integer PRIMARY KEY AUTOINCREMENT, studentID int, caID int, score real, active boolean NULL) "
        else:
            pass
        
    def studentPsychomoto(self, term):
        self.term = term
        if self.term > 0:
            table = 'student_psy' + str(self.term)
            return  "CREATE TABLE IF NOT EXISTS "+ table  +" (id integer PRIMARY KEY AUTOINCREMENT, studentID int, caID int, score real, active boolean NULL) "
        else:
            pass
        
    def studentFee(self, term):
        self.term = term
        if self.term > 0:
            table = 'student_fee' + str(self.term)
            return  "CREATE TABLE IF NOT EXISTS "+ table  +" (id integer PRIMARY KEY AUTOINCREMENT, studentID int, feeID int, amount real, active int NULL) "
        else:
            pass
       
    
    def studentPay(self, term):
        self.term = term
        if self.term > 0:
            table = 'student_pay' + str(self.term)
            return  "CREATE TABLE IF NOT EXISTS "+ table  +" (id integer PRIMARY KEY AUTOINCREMENT, studentID int, accountID int, feeID int, teller text,  amount real, datepaid text, active boolean NULL) "
        else:
            pass
#db = Tables()
#h = dir(db.session)  
#print(h[4])
    def schoolExpenses(self, session):
        self.term = session
        if self.term > 0:
            table = 'school_expenses' + str(self.term)
            return  "CREATE TABLE IF NOT EXISTS "+ table  +" (id integer PRIMARY KEY AUTOINCREMENT, expenseID int, accountID int, teller text, description text, user int,  amount real, datepaid text, active boolean NULL) "
        else:
            pass
    
    def schoolStores(self, session):
        self.term = session
        if self.term > 0:
            table = 'school_stores' + str(self.term)
            return  "CREATE TABLE IF NOT EXISTS "+ table  +" (id integer PRIMARY KEY AUTOINCREMENT, itemID int, quantity real, period int, person text,  state int,  teller text, description text, user int,  amount real, datepaid text, active boolean NULL) "
        else:
            pass
        
    def schoolFacilities(self, session):
        self.term = session
        if self.term > 0:
            table = 'school_facilities' + str(self.term)
            return  "CREATE TABLE IF NOT EXISTS "+ table  +" (id integer PRIMARY KEY AUTOINCREMENT, facilityID int, accountID int, teller text,  amount real, datepaid text, active boolean NULL) "
        else:
            pass
        
    def schoolAwards(self, session):
        self.term = session
        if self.term > 0:
            table = 'school_awards' + str(self.term)
            return  "CREATE TABLE IF NOT EXISTS "+ table  +" (id integer PRIMARY KEY AUTOINCREMENT, studentID int, action text, reaction text,  staffname real, datepaid text, active boolean NULL) "
        else:
            pass
        
    def schoolConducts(self, session):
        self.term = session
        if self.term > 0:
            table = 'school_conducts' + str(self.term)
            return  "CREATE TABLE IF NOT EXISTS "+ table  +" (id integer PRIMARY KEY AUTOINCREMENT, studentID int, action text, reaction text,  staffname real, datepaid text, state boolean, active boolean NULL) "
        else:
            pass
        
    def schoolMails(self, session):
        self.term = session
        if self.term > 0:
            table = 'school_mails' + str(self.term)
            return  "CREATE TABLE IF NOT EXISTS "+ table  +" (id integer PRIMARY KEY AUTOINCREMENT, studentID int, message text, subject text, datepaid text, active boolean NULL) "
        else:
            pass
        
    def schoolMedicals(self, session):
        self.term = session
        if self.term > 0:
            table = 'school_medicals' + str(self.term)
            return  "CREATE TABLE IF NOT EXISTS "+ table  +" (id integer PRIMARY KEY AUTOINCREMENT, studentID int, ailment text, treatment text, datepaid text, active boolean NULL) "
        else:
            pass