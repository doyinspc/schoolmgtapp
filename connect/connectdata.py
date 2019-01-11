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
            
    def studentClassUnitFee(self, session):
        '''
        get number of student in class
        '''
        db = 'student_class'+str(session)

        sql = "SELECT SUM(P.id) as id, P.sex as sex, P.cid, P.classname, P.classID, P.clasz, datas.abbrv as fee, sum(datas.description) as amount FROM (SELECT COUNT (id) as id, sex, cid, (SELECT name FROM datas WHERE id = cid LIMIT 1) as classname, (SELECT subID FROM datas WHERE id = cid LIMIT 1) as classID, (SELECT name FROM datas WHERE id = (SELECT subID FROM datas WHERE id = cid LIMIT 1)) as clasz FROM (SELECT students.id as id, students.gender as sex, "+ db +".classID as cid FROM "+ db +" LEFT JOIN students ON "+ db +".studentID = students.id) GROUP BY sex, cid) as P LEFT JOIN `datas` ON  `P`.`classID` = `datas`.`name` WHERE `datas`.`pubID` = 'fee' and `datas`.`subID` = "+str(session)+" GROUP BY P.classID, P.sex "
        try:
            conn = sqlite3.connect(self.dbs)
            conn.row_factory = lambda C, R: {c[0]: R[i] for i, c in enumerate(C.description)}
            c = conn.cursor()
            c.execute(sql)
            return c.fetchall()
            conn.close()
        except sqlite3.Error as e:
            print(e)
    
   