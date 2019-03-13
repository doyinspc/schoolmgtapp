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