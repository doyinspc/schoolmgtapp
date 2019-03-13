# -*- coding: utf-8 -*-
"""
Created on Sat Jul  7 15:54:19 2018

@author: CHARLES
"""
from PyQt4.QtCore import SIGNAL, Qt, QDate
from PyQt4.QtGui import  QCursor, QPlainTextEdit, QFont, QMenu, QWidget, QHeaderView, QTableWidgetItem, QAbstractItemView, QTableWidget, QTreeWidget, QTreeWidgetItem, QComboBox, QFrame, QDateEdit, QRadioButton, QCheckBox, QHBoxLayout, QGroupBox, QGridLayout, QDialog, QApplication, QPushButton, QLineEdit, QFormLayout, QLabel, QVBoxLayout
from dialogreport import ReportDialog, EditReportDialog
from connect import Db
from studenttable import StudentTable
from datetime import datetime
import time

class ExpensesDialog(QDialog):
    
    holdc = {}
    def __init__(self, session, parent=None):
        super(ExpensesDialog, self).__init__(parent)
        self.session = session
        session = self.pullOnes('session', session)
        self.sessionname = str(session['name'])+' Session'
        self.pagetitle = self.sessionname 
        self.tableFont = QFont('Century Gothic', 8)
        #self.tableFont.setFamily('Century Gothic')
        self.tableHeaderStyle = "::section {""background-color: teal; color:white}"
        #pull all CA
        self.editID = 0
        self.hold_account = {}
        self.hold_expenses = {}
        self.hold_expensesGroup = {}
        
        from_label = QLabel('From:')
        to_label = QLabel('To:')
        self.fromData = QDateEdit()
        self.toData = QDateEdit()
        currentDate = QDate()
        self.fromData.setDate(currentDate.currentDate())
        self.fromData.setCalendarPopup(True)
        self.toData.setDate(currentDate.currentDate())
        self.toData.setCalendarPopup(True)
        self.pull_btn = QPushButton()
        self.pull_btn.setText("Load")
        h_pull_box = QHBoxLayout()
        h_pull_box.addWidget(from_label)
        h_pull_box.addWidget(self.fromData)
        h_pull_box.addWidget(to_label)
        h_pull_box.addWidget(self.toData)
        h_pull_box.addWidget(self.pull_btn)
        
        expensesGroup = self.pullGroupExpenses()
        account = self.pullAccount()
        
        self.expenseGroupText = QLabel('Category')
        self.expenseGroupData = QComboBox()
        self.expenseGroupData.currentIndexChanged.connect(self.reloadExpenses)
        self.expenseText = QLabel('Expenses')
        self.expenseData = QComboBox()
        self.amountText = QLabel('Amount')
        self.amountData = QLineEdit()
        self.amountData.setPlaceholderText('0000.00')
        self.tellerText = QLabel('Teller/Reciept No.')
        self.tellerData = QLineEdit()
        self.tellerData.setPlaceholderText('xxxxxxxxx')
        self.accountText = QLabel('Account')
        self.accountData = QComboBox()
        self.dateText = QLabel('Date')
        self.dateData = QDateEdit()
        self.dateData.setDate(currentDate.currentDate())
        self.dateData.setCalendarPopup(True)
        self.descriptionText = QLabel('Brief Description')
        self.descriptionData = QPlainTextEdit()
        self.descriptionData.move(200, 100)
        hboz = QHBoxLayout()
        self.gender = QLabel('State')
        self.r1 = QRadioButton('Expenses')
        self.r1.setChecked(True)
        self.r2 = QRadioButton('Refund')
        hboz.addWidget(self.r1)
        hboz.addWidget(self.r2)
        
        i = 0
        for a in expensesGroup:
            self.hold_expensesGroup[i] = a['id']
            tex = str(a['name']).upper()
            self.expenseGroupData.addItem(tex)
            i += 1
            
        i = 0 
        exp_key = self.hold_expensesGroup[self.expenseGroupData.currentIndex()]
        expenses = self.pullExpenses(exp_key)
        for a in expenses:
            self.hold_expenses[i] = a['id']
            tex = str(a['name']).upper()
            self.expenseData.addItem(tex)
            i += 1
            
        i = 0    
        for a in account:
            self.hold_account[i] = a['id']
            tex = str(a['name']).upper()
            self.accountData.addItem(tex)
            i += 1     
            
        self.FormLayout = QFormLayout()
        self.FormLayout.addRow(self.expenseGroupText,self.expenseGroupData)
        self.FormLayout.addRow(self.expenseText,self.expenseData)
        self.FormLayout.addRow(self.accountText,self.accountData)
        self.FormLayout.addRow(self.tellerText,self.tellerData)
        self.FormLayout.addRow(self.amountText,self.amountData)
        self.FormLayout.addRow(self.gender, hboz)
        self.FormLayout.addRow(self.dateText,self.dateData)
        self.FormLayout.addRow(self.descriptionText,self.descriptionData)
        
        groupBox1 = QGroupBox('Add Expenses')
        groupBox1.setLayout(self.FormLayout)
        
        self.pb = QPushButton()
        self.pb.setObjectName("Add")
        self.pb.setText("Add Expenses")
        
        self.pb1 = QPushButton()
        self.pb1.setObjectName("Edit")
        self.pb1.setText("Edit Row")
        self.pb1.setEnabled(False)
        
        self.pb2 = QPushButton()
        self.pb2.setObjectName("Close")
        self.pb2.setText("Close")
        
        self.pb3 = QPushButton()
        self.pb3.setObjectName("Delete")
        self.pb3.setText("Delete Row")
        self.pb3.setEnabled(False)
        
        self.pb4 = QPushButton()
        self.pb4.setObjectName("Reset")
        self.pb4.setText("Reset")
        self.pb4.hide()
        
        self.pb5 = QPushButton()
        self.pb5.setObjectName("Change")
        self.pb5.setText("Change Expenses")
        self.pb5.hide()
        
        self.pb6 = QPushButton()
        self.pb6.setObjectName("Clear")
        self.pb6.setText("Clear Selection")
        self.pb6.setEnabled(False)
        
        hbo = QHBoxLayout()
        hbo.addWidget(self.pb)
        hbo.addWidget(self.pb5)
        hbo.addWidget(self.pb4)
        hbo.addWidget(self.pb2)
        groupBox2 = QGroupBox('Expenses Data')
        groupBox2.setLayout(hbo)
        
        self.cols =  ['SN', 'EXPENSES', 'ACCOUNT', 'AMOUNT', 'DATE']
        al = self.pullExpensesData()
        if len(al) > 0:
            al = al
        else:
            al = {}
        
       
        
        self.table = QTableWidget()
        header = self.table.horizontalHeader()
        header.setResizeMode(QHeaderView.ResizeToContents)
        header.setStretchLastSection(True)
        header.setStyleSheet(self.tableHeaderStyle)
        vheader = self.table.verticalHeader()
        vheader.setStyleSheet(self.tableHeaderStyle)
            # Body
        self.table.setWindowTitle("Expenses")
        self.table.resize(300,250)
        self.table.setFont(self.tableFont)
        self.table.setSortingEnabled(2)
        #self.table.resizeColumnsToContents()
        self.table.setRowCount(len(al))
        self.table.setColumnCount(len(self.cols))
        self.table.setHorizontalHeaderLabels(self.cols)
        self.table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self.handleHeaderMenu)
        self.table.hideColumn(0)
        self.table.setSelectionMode(QAbstractItemView.MultiSelection)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        
        i = 0
        for q in al:
            #row id
            self.table.setItem(i, 0, QTableWidgetItem(str(q['id'])))
            self.table.setItem(i, 1, QTableWidgetItem(str(q['expensename']).upper()))
            self.table.setItem(i, 2, QTableWidgetItem(str(q['accountname']).upper()))
            zamt = str("{:,}".format(float(q['amount'])))
            self.table.setItem(i, 3, QTableWidgetItem(zamt))
            damz = float(q['datepaid'])
            damt = datetime.utcfromtimestamp(damz).strftime('%d-%m-%Y')
            self.table.setItem(i, 4, QTableWidgetItem(str(damt)))
            i += 1
        self.table.itemSelectionChanged.connect(self.confirmSelection)
        self.table.resizeRowsToContents()
        v_pull_box = QVBoxLayout()
        self.h1_pull_box = QVBoxLayout()
        self.h1_pull_box.addWidget(self.table)
        v_pull_box.addLayout(h_pull_box)
        v_pull_box.addLayout(self.h1_pull_box)
        h2_pull_box = QHBoxLayout()
        h2_pull_box.addWidget(self.pb1)
        h2_pull_box.addWidget(self.pb3)
        h2_pull_box.addWidget(self.pb6)
        v_pull_box.addLayout(h2_pull_box)
        
        groupBox3 = QGroupBox()
        groupBox3.setLayout(hbo)
        groupBox2.setLayout(v_pull_box)
        
        grid = QGridLayout()
        grid.addWidget(groupBox1, 0, 0)
        grid.addWidget(groupBox2, 0, 1, 2, 1)
        grid.addWidget(groupBox3, 1, 0)
        
        self.setLayout(grid)
        self.connect(self.pb, SIGNAL("clicked()"), lambda: self.button_click())
        self.connect(self.pb1, SIGNAL("clicked()"), lambda: self.button_editshow())
        self.connect(self.pb2, SIGNAL("clicked()"), lambda: self.button_close(self))
        self.connect(self.pb3, SIGNAL("clicked()"), lambda: self.button_delete())
        self.connect(self.pb4, SIGNAL("clicked()"), lambda: self.button_reset())
        self.connect(self.pb5, SIGNAL("clicked()"), lambda: self.button_edit())
        self.connect(self.pb6, SIGNAL("clicked()"), lambda: self.button_clear())
        self.connect(self.pull_btn, SIGNAL("clicked()"), lambda x =1: self.reloadTable(x))
       
        self.setWindowTitle(self.pagetitle)
    
    def handleHeaderMenu(self, pos):
        print('column(%d)' % self.table.horizontalHeader().logicalIndexAt(pos))
        menu = QMenu()
        menu.addAction('Add')
        menu.addAction('Delete')
        menu.exec_(QCursor.pos()) 
        
    def pullGroupExpenses(self):
        cn = Db()
        arr = cn.selectn('datas', '' , '', {"pubID":15, "active": 0})
        return arr
    
    def pullExpenses(self, a):
        cn = Db()
        arr = cn.selectn('datas', '' , '', {"subID":a})
        return arr
    
    def pullAccount(self):
        cn = Db()
        arr = cn.selectn('datas', '' , '', {"pubID":20, "active": 0})
        return arr
    
    def pullExpensesData(self):
        st_date = self.fromData.date().toPyDate()
        en_date = self.toData.date().toPyDate()
        st_date = time.mktime(st_date.timetuple())
        en_date = time.mktime(en_date.timetuple())
        
        db = 'school_expenses'+str(self.session)
        cn = Db()
        arr = cn.selectExpenseDate(db, st_date, en_date)
        return arr
    
    def mySelectTable(self):
        '''
        get the selected rpws in a table
        returns list or row ids
        '''
        sels = self.table.selectedIndexes()
        sels = self.table.selectionModel().selectedRows()
        
        park = []
        park1 = []
        for j in sels:
            park.append(j.row()) 
            
            
        for i in set(park):
            selected = self.table.item(i, 0).text()
            park1.append(selected)
            
        return park1
        
    def editRow(self, a):
        _session = self.session
        g = Db()
        db = 'school_expenses'+str(_session)
        data = g.selectn(db, '', 1, {'id':a})
        if len(data) > 0:
            self.editID = int(data['id'])
            if float(data['amount']) < 0:
                amt = float(data['amount']) * -1
                self.amountData.setText(str(amt))
                self.r1.setChecked(True)
            else:
                amt = float(data['amount'])
                self.amountData.setText(str(amt))
                self.r2.setChecked(True)
                
            self.descriptionData.clear()
            self.descriptionData.insertPlainText(str(data['description']))
            self.tellerData.setText(str(data['teller']))
            acID = self.hold_account.keys()[self.hold_account.values().index(data['accountID'])]
            self.accountData.setCurrentIndex(acID)
            exID = self.hold_expenses.keys()[self.hold_expenses.values().index(data['expenseID'])]
            self.expenseData.setCurrentIndex(exID)
        
    def reloadExpenses(self):
        cat = self.hold_expensesGroup[self.expenseGroupData.currentIndex()]
        expenses = self.pullExpenses(cat)
        self.expenseData.clear()
        self.hold_expenses = {}
        i = 0
        for a in expenses:
            self.hold_expenses[i] = a['id']
            tex = str(a['name']).upper()
            self.expenseData.addItem(tex)
            i += 1
        
    
    def reloadTable(self, a):
        data = self.pullExpensesData()
        self.table.close()
        self.table = QTableWidget()
        header = self.table.horizontalHeader()
        header.setResizeMode(QHeaderView.ResizeToContents)
        header.setStretchLastSection(True)
        header.setStyleSheet(self.tableHeaderStyle)
        vheader = self.table.verticalHeader()
        vheader.setStyleSheet(self.tableHeaderStyle)
            # Body
        self.table.setWindowTitle("Expenses")
        self.table.resize(300, 250)
        self.table.setFont(self.tableFont)
        self.table.setSortingEnabled(2)
        self.table.resizeColumnsToContents()
        self.table.setRowCount(len(data))
        self.table.setColumnCount(len(self.cols))
        self.table.setHorizontalHeaderLabels(self.cols)
        self.table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self.handleHeaderMenu)
        self.table.hideColumn(0)
        self.table.setSelectionMode(QAbstractItemView.MultiSelection)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        i = 0
        for q in data:
            #row id
            self.table.setItem(i, 0, QTableWidgetItem(str(q['id'])))
            self.table.setItem(i, 1, QTableWidgetItem(str(q['expensename']).upper()))
            self.table.setItem(i, 2, QTableWidgetItem(str(q['accountname']).upper()))
            zamt = str("{:,}".format(float(q['amount'])))
            self.table.setItem(i, 3, QTableWidgetItem(zamt))
            damz = float(q['datepaid'])
            damt = datetime.utcfromtimestamp(damz).strftime('%d-%m-%Y')
            self.table.setItem(i, 4, QTableWidgetItem(str(damt)))
            i += 1
        self.table.itemSelectionChanged.connect(self.confirmSelection)
        self.table.resizeRowsToContents()
        self.h1_pull_box.addWidget(self.table)
        self.table.show()
    
    def pullOnes(self, a, b):
        cn = Db()
        arr = cn.selectn(a, '' , 1, {'id': b})
        return arr
     
    def confirmSelection(self):
        item =self.mySelectTable()
        if len(item) == 1:
            self.pb1.setEnabled(True)
            self.pb3.setEnabled(True)
            self.pb6.setEnabled(True)
        elif len(item) > 1:
            self.pb1.setEnabled(False)
            self.pb3.setEnabled(True)
            self.pb6.setEnabled(True)
        else:
            self.pb1.setEnabled(False)
            self.pb3.setEnabled(False)
            self.pb6.setEnabled(False)
            
    def button_close(self, b):
        b.close()
        
    def button_editshow(self):
        item =self.mySelectTable()
        self.editRow(item[0])
        self.pb.hide()
        self.pb4.show()
        self.pb5.show()
        
    def button_delete(self):
        item =self.mySelectTable()
        _session = self.session
        g = Db()
        db = 'school_expenses'+str(_session)
        for j in item:
            g.delete(db, {'id':j})
        
        self.reloadTable(1)
        
    def button_edit(self):
        _session = self.session
        _amount = self.amountData.text()
        _teller = self.tellerData.text()
        _date = self.dateData.date().toPyDate()
        _date = time.mktime(_date.timetuple())
        _description = self.descriptionData.toPlainText()
        _account = self.hold_account[self.accountData.currentIndex()]
        _expense = self.hold_expenses[self.expenseData.currentIndex()]
        if self.r1.isChecked():
           _amount = float(_amount)  
        else:
           _amount = float(_amount) * -1
        
        arr = {}
        if _amount and not(_amount == 0)  and int(_expense) > 0 and int(_account) > 0:
            arr['amount'] = _amount
            arr['datepaid'] = _date
            arr['description'] = _description
            arr['accountID'] = _account
            arr['expenseID'] = _expense
            arr['teller'] = _teller
            
            ups = {}
            ups['id'] = self.editID 
            if int(self.editID) > 0:
                db = 'school_expenses'+str(_session)
                g = Db()
                g.update(db, arr, ups)
                if int(self.editID) > 0:
                    self.button_reset()
                    
    def button_reset(self):
        self.reloadTable(1)
        self.amountData.setText('')
        self.descriptionData.clear()
        self.tellerData.setText('')
        self.pb4.hide()
        self.pb5.hide()
        self.pb.show()
        self.editID = 0
        self.button_clear()
        self.confirmSelection()
        
    def button_clear(self):
        self.table.selectionModel().clearSelection()
        
        
    def button_click(self):
        _session = self.session
        _amount = self.amountData.text()
        _teller = self.tellerData.text()
        _date = self.dateData.date().toPyDate()
        _date = time.mktime(_date.timetuple())
        _description = self.descriptionData.toPlainText()
        _account = self.hold_account[self.accountData.currentIndex()]
        _expense = self.hold_expenses[self.expenseData.currentIndex()]
        if self.r1.isChecked():
           _amount = float(_amount)  
        else:
           _amount = float(_amount) * -1
        
         
        arr = {}
        if _amount and not(_amount == 0)  and int(_expense) > 0 and int(_account) > 0:
            arr['amount'] = _amount
            arr['datepaid'] = _date
            arr['description'] = _description
            arr['accountID'] = _account
            arr['expenseID'] = _expense
            arr['teller'] = _teller
            
            db = 'school_expenses'+str(_session)
            g = Db()
            ins = g.insert(db, arr)
            if int(ins) > 0:
                self.button_reset()
                
            
        
    
