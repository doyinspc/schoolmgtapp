# -*- coding: utf-8 -*-
"""
Created on Sun Mar  3 03:09:08 2019

@author: CHARLES
"""
from PyQt4 import QtCore, QtGui
from connect import Db
class Valid():
    
    def limitText(self):
        reg = "[a-z0-9]{5}"
        regEx = QtCore.QRegExp(reg)
        validator = QtGui.QRegExpValidator(regEx)
        return validator
    
    def fullNum(self):
        reg = "[0-9]{8}"
        regEx = QtCore.QRegExp(reg)
        validator = QtGui.QRegExpValidator(regEx)
        return validator
    
    def fullText(self):
        reg = "[a-z/s/w]{25}"
        regEx = QtCore.QRegExp(reg)
        validator = QtGui.QRegExpValidator(regEx)
        return validator
    
    def background(self):
        style = "background-color: #171941;"
        return style
    
    def treez(self):
        style = ""
        return style
    
    def font(self):
        style = "color: #adb5bd; opacity: 1;"
        return style
    
    def addBackground(self):
        style = "background-color: #171941;"
        return style
    
    def addFont(self):
        style = "color: #adb5bd; opacity: 1;"
        return style
    def editBackground(self):
        style = "background-color: #171941;"
        return style
    
    def editFont(self):
        style = "color: #adb5bd; opacity: 1;"
        return style
    
    def pullData(self, db, num = '', sel=None):
         g = Db()
         v = g.selectn(db, '', num, sel)
         return v

class Settingz():
    def positions(self, a):
        arr = { 
                1:{'id':20 ,'page':'Accounts Settings', 'name':'Accounts', 'subID': None, 'icon':'icon/pic.png' },
                2:{'id':3 ,'page':'Subjects Settings', 'name':'Subjects', 'subID': None, 'icon':'icon/pic.png' },
                3:{'id':1 ,'page':'Class Settings', 'name':'Classes', 'subID': 1, 'icon':'icon/pic.png' },
                4:{'id':15 ,'page':'Expenses Setting', 'name':'Expenses', 'subID': 1, 'icon':'icon/pic.png' },
                5:{'id':23 ,'page':'Stock Settings', 'name':'Stocks', 'subID': 1, 'icon':'icon/pic.png' },
                6:{'id':17 ,'page':'Fees Settings', 'name':'Fees', 'subID': None, 'icon':'icon/pic.png' },
                7:{'id':11 ,'page':'Affective/Attitude Settings', 'name':'Affectives', 'subID': 1, 'icon':'icon/pic.png' },
                8:{'id':9 ,'page':'Psycomotor/Skills Settings', 'name':'Psycomotors', 'subID': 1, 'icon':'icon/pic.png' },
                9:{'id':7 ,'page':'Assessment Types', 'name':'Assessment', 'subID': None, 'icon':'icon/pic.png' },  
                10:{'id':27 ,'page':'Deparments Settings', 'name':'Departments', 'subID': 1, 'icon':'icon/pic.png' },
                11:{'id':28 ,'page':'Pension Managers', 'name':'Pension', 'subID': None, 'icon':'icon/pic.png' },
                12:{'id':29 ,'page':'Health Managers', 'name':'Health', 'subID': None, 'icon':'icon/pic.png' },
                30:{'id':30 ,'page':'Sessions Settings', 'name':'Settings', 'subID': 1, 'icon':'icon/pic.png' }
              }
        
        #1 account
        #2 subjects
        #3 class
        #4 expenses
        #5 stock
        #6 fees
        #7 affective
        #8 psycomotor
        #9 assessment
        
        return arr[a]
class Arrayz():
    def arrayz(self, a):
        arr = {}
        if a == 1:
            #relationship
            arr[0] = 'Father'
            arr[1] = 'Mother'
            arr[2] = 'Brother'
            arr[3] = 'Sister'
            arr[4] = 'Child'
            arr[5] = 'Aunt'
            arr[6] = 'Uncle'
            arr[7] = 'Grand Parent'
            arr[8] = 'Guardian'
            arr[9] = 'Others'
                
        elif a == 2:
            #access
            arr[0] = 'DENIED'
            arr[1] = 'GRANT'
        elif a == 3:
            #level
            arr[0] = '0'
            arr[1] = '1'
            arr[2] = '2'
            arr[3] = '3'
            arr[4] = '4'
            arr[5] = '5'
            arr[6] = '6'
            arr[7] = '7'
            arr[8] = '8'
            arr[9] = '9'
        elif a == 4:
            #reason staff
            arr[0] = 'IN-SERVICE'
            arr[1] = 'RESIGNATION'
            arr[2] = 'DISMISSAL'
            arr[3] = 'SUMMARY DISMISSAL'
            arr[4] = 'TERMINATION'
            arr[5] = 'REDUNDANCY'
            
        elif a == 5:
            #gender
            arr[0] = 'MALE'
            arr[1] = 'FEMALE'
            
        elif a == 6:
            #marital
            arr[0] = 'SINGLE'
            arr[1] = 'MARRIED'
            arr[2] = 'WIDOWED'
            
        elif a == 7:
            #religion
            arr[0] = 'CHRISTIANITY'
            arr[1] = 'ISLAM'
            arr[2] = 'TRADITIONAL'
            arr[3] = 'OTHERS'
            
        return arr
class Headers():
    def headers(self, a):
        arr = {}
        if a == 1:
            arr[1] = ['matric', 'MATRIC. NUMBER', '', '', '']
            arr[2] = ['name', 'FULLNAME', '', 'title', '']
            arr[3] = ['classunit', 'CLASS', '', '', '']
            arr[4] = ['fee', 'FEES', 'align="center"', '', '']
        if a == 2:
            arr[1] = ['matric', 'MATRIC. NUMBER', '', '', '']
            arr[2] = ['name', 'FULLNAME', '', 'title', '']
            arr[3] = ['classunit', 'CLASS', '', '', '']
            arr[4] = ['pay', 'PAYMENTS', 'align="center"', '', '']
        if a == 3:
            arr[1] = ['matric', 'MATRIC. NUMBER', '', '', '']
            arr[2] = ['name', 'FULLNAME', '', 'title', '']
            arr[3] = ['classunit', 'CLASS', '', '', '']
            arr[4] = ['fee', 'FEES', 'align="center"', '', '']
            arr[5] = ['pay', 'PAYMENTS', 'align="center"', '', '']
            arr[6] = ['bal', 'BALANCE', 'align="center"', '', '']
        if a == 4:
            arr[1] = ['matric', 'MATRIC. NUMBER', '', '', '']
            arr[2] = ['name', 'FULLNAME', '', 'title', '']
            arr[3] = ['classunit', 'CLASS', '', '', '']
            arr[4] = ['subjects', 'SUBJECTS', 'align="left"', '', '']
        if a == 5:
            arr[1] = ['matric', 'MATRIC. NUMBER', '', '', '']
            arr[2] = ['name', 'FULLNAME', '', 'title', '']
            arr[3] = ['classunit', 'CLASS', '', '', '']
            arr[4] = ['fee', 'FEES', 'align="center"', '', '']
        if a == 6:
            arr[1] = ['matric', 'MATRIC. NUMBER', '', '', '']
            arr[2] = ['name', 'FULLNAME', '', 'title', '']
            arr[3] = ['classunit', 'CLASS', '', '', '']
            arr[4] = ['fee', 'FEES', 'align="center"', '', '']
        
        return arr
    
    def students(self):
        selections = {}
        selections[1] = 'Biodata'
        selections[2] = 'Next of Kins'
        selections[3] = 'Next of Kins'
        selections[4] = 'Academic'
        selections[5] = 'Professional'
        selections[6] = 'Work Experience/History'
        selections[7] = 'Workshop/Seminar'
        selections[8] = 'Misconduct'
        selections[9] = 'Commendation/Awards'
        selections[10] = 'Duties/Rsponsibilities'
        return selections
    
    def staffs(self):
        selections = {}
        selections[1] = 'Biodata'
        selections[2] = 'Next of Kins'
        selections[3] = 'Next of Kins'
        selections[4] = 'Academic'
        selections[5] = 'Professional'
        selections[6] = 'Work Experience/History'
        selections[7] = 'Workshop/Seminar'
        selections[8] = 'Misconduct'
        selections[9] = 'Commendation/Awards'
        selections[10] = 'Duties/Rsponsibilities'
        return selections
    
    def analize(self):
        selections = {}
        selections['sum'] = 'Total'
        selections['count'] = 'Count'
        selections['mean'] = 'AVG,'
        selections['min'] = 'MIM'
        selections['max'] = 'MAX'
        selections['std'] = 'STD. DEV.'
        selections['25%'] = '25%'
        selections['50%'] = '50%'
        selections['75%'] = '75%' 
        return selections
                
class Buttons():
    def addButton(self):
        return 'icons/cadd.png'
    def editButton(self):
        return 'icons/cedit.png'
    def deleteButton(self):
        return 'icons/cdelete.png'
    def closeButton(self):
        return 'icons/cclose.png'
    def saveButton(self):
        return 'icons/csave.png'
    def resetButton(self):
        return 'icons/creset.png'
    def printButton(self):
        return 'icons/print.png'