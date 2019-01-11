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
       return  "CREATE TABLE IF NOT EXISTS students (id integer PRIMARY KEY AUTOINCREMENT, schno text, surname text, firstname text, othername text NULL, addr text NULL, gender boolean NOT NULL, soo text NULL, lga text NULL, nation text NULL, dob text NULL, admit text NULL, g1 text NULL, g2 text NULL, g1rel text NULL, g2rel text NULL, g1p1 text null, g1p2 text NULL, g2p1 text NULL, g2p2 text NULL, g1email text NULL, g2email text NULL, g1addr text NULL, g2addr text NULL, reason text NULL, active boolean NOT NULL ) "
     
    def datas(self):
       return  "CREATE TABLE IF NOT EXISTS datas (id integer PRIMARY KEY AUTOINCREMENT, subID int NULL, name text, abbrv text, active boolean NULL) "
   
    def studentClasz(self, term):
        self.term = term
        if self.term > 0:
            table = 'student_class' +str( self.term)
            return  "CREATE TABLE IF NOT EXISTS "+ table  +" (id integer PRIMARY KEY AUTOINCREMENT, studentID int, classID int, active boolean NULL) "
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
            return  "CREATE TABLE IF NOT EXISTS "+ table  +" (id integer PRIMARY KEY AUTOINCREMENT, studentID int, feeID int, active boolean NULL) "
        else:
            pass
       
    
    def studentPay(self, term):
        self.term = term
        if self.term > 0:
            table = 'student_pay' + str(self.term)
            return  "CREATE TABLE IF NOT EXISTS "+ table  +" (id integer PRIMARY KEY AUTOINCREMENT, studentID int, classID int, active boolean NULL) "
        else:
            pass
#db = Tables()
#h = dir(db.session)  
#print(h[4])