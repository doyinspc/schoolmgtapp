# -*- coding: utf-8 -*-
"""
Created on Sat Jul  7 15:54:19 2018

@author: CHARLES
"""
from PyQt4.QtCore import SIGNAL, Qt, QDate
from PyQt4.QtGui import  QCursor, QColor, QPlainTextEdit, QFont, QMenu, QWidget, QHeaderView, QTableWidgetItem, QAbstractItemView, QTableWidget, QTreeWidget, QTreeWidgetItem, QComboBox, QFrame, QDateEdit, QRadioButton, QCheckBox, QHBoxLayout, QGroupBox, QGridLayout, QDialog, QApplication, QPushButton, QLineEdit, QFormLayout, QLabel, QVBoxLayout
from dialogreport import ReportDialog, EditReportDialog
from connect import Db
from studenttable import StudentTable
from datetime import datetime
import time

class StoreDialog(QDialog):
    
    holdc = {}
    def __init__(self, session, parent=None):
        super(StoreDialog, self).__init__(parent)
        self.session = session
        session = self.pullOnes('session', session)
        self.sessionname = str(session['name'])+' Session'
        self.pagetitle = self.sessionname 
        self.tableFont = QFont('Century Gothic', 8)
        self.table = QTableWidget()
        self.cols =  ['SN', 'ITEM', 'QUANTITY', 'UNIT AMOUNT', 'TOTAL AMOUNT', 'DATE']
        self.h1_pull_box = QVBoxLayout()
        
        #self.tableFont.setFamily('Century Gothic')
        self.tableHeaderStyle = "::section {""background-color: teal; color:white}"
        #pull all CA
        self.editID = 0
        self.hold_unit = {}
        self.hold_store = {}
        self.hold_storeGroup = {}
        self.hold_borrowed = {}
        
        
        from_label = QLabel('From:')
        to_label = QLabel('To:')
        self.fromData = QDateEdit()
        self.toData = QDateEdit()
        currentDate = QDate()
        self.fromData.setDate(currentDate.currentDate())
        self.fromData.setCalendarPopup(True)
        self.toData.setDate(currentDate.currentDate())
        self.toData.setCalendarPopup(True)
        menu = QMenu()
        menu.addAction('All', lambda:self.reloadTable(0))
        menu.addAction('In-Stock', lambda:self.reloadTable(1))
        menu.addAction('Out-Stock', lambda:self.reloadTable(2))
        menu.addAction('Damaged', lambda:self.reloadTable(3))
        menu.addAction('Borrowed', lambda:self.reloadTable(4))
        self.pull_btn = QPushButton()
        self.pull_btn.setText("Load")
        self.pull_btn.setMenu(menu)
        h_pull_box = QHBoxLayout()
        h_pull_box.addWidget(from_label)
        h_pull_box.addWidget(self.fromData)
        h_pull_box.addWidget(to_label)
        h_pull_box.addWidget(self.toData)
        h_pull_box.addWidget(self.pull_btn)
        
        storeGroup = self.pullGroupStore()
        unit = self.pullUnit()
        
        self.storeGroupText = QLabel('Category')
        self.storeGroupData = QComboBox()
        self.storeGroupData.currentIndexChanged.connect(self.reloadStore)
        self.storeText = QLabel('Items')
        self.storeData = QComboBox()
       
        self.amountText = QLabel('Total Cost')
        self.amountData = QLineEdit()
        self.amountData.setPlaceholderText('0000.00')
        self.tellerText = QLabel('Reciept No.')
        self.tellerData = QLineEdit()
        self.tellerData.setPlaceholderText('xxxxxxxxx')
        self.quantityText = QLabel('Quantity.')
        self.quantityData = QLineEdit()
        self.quantityData.setPlaceholderText('00.0')
        self.periodText = QLabel('Period (days)')
        self.periodData = QLineEdit()
        self.periodData.setPlaceholderText('00.0')
        self.personText = QLabel('Recieved By:')
        self.personData = QLineEdit()
        self.personData.setPlaceholderText('00.0')
        self.unitText = QLabel('Unit')
        self.unitData = QComboBox()
        self.borrowedText = QLabel('Borrowed')
        self.borrowedData = QComboBox()
        self.dateText = QLabel('Date')
        self.dateData = QDateEdit()
        self.dateData.setDate(currentDate.currentDate())
        self.dateData.setCalendarPopup(True)
        self.descriptionText = QLabel('Description')
        self.descriptionData = QPlainTextEdit()
        self.descriptionData.move(200, 100)
        self.borrowedText.hide()
        self.borrowedData.hide()
        
        mboz = QVBoxLayout()
        hboz = QHBoxLayout()
        self.state = QLabel('')
        self.r1 = QRadioButton('In-stock')
        self.r1.setChecked(True)
        self.r1.toggled.connect(lambda:self.changeStates())
        self.r2 = QRadioButton('Out-stock')
        self.r2.toggled.connect(lambda:self.changeStates())
        self.r3 = QRadioButton('Damaged')
        self.r3.toggled.connect(lambda:self.changeStates())
        self.r4 = QRadioButton('Borrowed')
        self.r4.toggled.connect(lambda:self.changeStates())
        self.r5 = QRadioButton('Returned')
        self.r5.toggled.connect(lambda:self.changeStates())
        hboz.addWidget(self.r1)
        hboz.addWidget(self.r2)
        hboz.addWidget(self.r3)
        hboz.addWidget(self.r4)
        hboz.addWidget(self.r5)
        
        
        i = 0
        for a in storeGroup:
            self.hold_storeGroup[i] = a['id']
            tex = str(a['name']).upper()
            self.storeGroupData.addItem(tex)
            i += 1
            
        i = 0 
        str_key = self.hold_storeGroup[self.storeGroupData.currentIndex()]
        store = self.pullStore(str_key)
        for a in store:
            self.hold_store[i] = a['id']
            tex = str(a['name']).upper()
            self.storeData.addItem(tex)
            i += 1
            
        i = 0    
        for a in unit:
            self.hold_unit[i] = a['id']
            tex = str(a['name']).upper()
            self.unitData.addItem(tex)
            i += 1     
        
        self.reloadBorrowed()
        self.FormLayout = QFormLayout()
        self.FormLayout.addRow(self.storeGroupText,self.storeGroupData)
        self.FormLayout.addRow(self.storeText,self.storeData)
        self.FormLayout.addRow(self.tellerText,self.tellerData)
        self.FormLayout.addRow(self.quantityText,self.quantityData)
        self.FormLayout.addRow(self.amountText,self.amountData)
        self.FormLayout.addRow(self.dateText,self.dateData)
        self.FormLayout.addRow(self.periodText,self.periodData)
        self.FormLayout.addRow(self.borrowedText,self.borrowedData)
        self.FormLayout.addRow(self.personText,self.personData)
        self.FormLayout.addRow(self.descriptionText, self.descriptionData)
        self.periodText.hide()
        self.periodData.hide()
        
        mboz.addLayout(hboz)
        mboz.addLayout(self.FormLayout)
        mboz.addWidget(self.state)
        
        groupBox1 = QGroupBox('Add Store Item')
        groupBox1.setLayout(mboz)
        
        self.pb = QPushButton()
        self.pb.setObjectName("Add")
        self.pb.setText("Add Store Item")
        
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
        self.pb5.setText("Change Store")
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
        groupBox2 = QGroupBox('Store Data')
        groupBox2.setLayout(hbo)
        
        
        al = self.pullStoreData(0)
        if al and len(al) > 0:
            al = al
        else:
            al = {}
        
        self.storeData.currentIndexChanged.connect(lambda:self.reloadBorrowed())
        
        header = self.table.horizontalHeader()
        header.setResizeMode(QHeaderView.ResizeToContents)
        header.setStretchLastSection(True)
        header.setStyleSheet(self.tableHeaderStyle)
        vheader = self.table.verticalHeader()
        vheader.setStyleSheet(self.tableHeaderStyle)
            # Body
        self.table.setWindowTitle("Store")
        self.table.setStyleSheet("color:white")
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
            if q['state'] == 1:
                color = QColor(100,0,0)
            elif q['state'] == 2:
                color = QColor(100,100,0)
            elif q['state'] == 3:
                color = QColor(100,0,100)
            elif q['state'] == 4:
                color = QColor(0,100,100) 
            else:
                color = QColor(0,50,150) 
   
            self.table.setItem(i, 0, QTableWidgetItem(str(q['id'])))
            self.table.item(i, 0).setBackground(color)
            self.table.setItem(i, 1, QTableWidgetItem(str(q['itemname']).upper()))
            self.table.item(i, 1).setBackground(color)
            self.table.setItem(i, 2, QTableWidgetItem(str(q['quantity']).upper()))
            self.table.item(i, 2).setBackground(color)
            try:
                zamt = str("{:,}".format(float(q['amount'])))
            except:
                zamt = ''
            self.table.setItem(i, 3, QTableWidgetItem(zamt))
            self.table.item(i, 3).setBackground(color)
            try:
                if len(q['amount']) > 0 and float(q['amount']) > 0:
                    tot = float(q['amount']) * float(q['quantity'])
                else:
                    tot = 0
            except:
                tot = 0
            self.table.setItem(i, 4, QTableWidgetItem(str(tot).upper()))
            self.table.item(i, 4).setBackground(color)
            damz = float(q['datepaid'])
            damt = datetime.utcfromtimestamp(damz).strftime('%d-%m-%Y')
            self.table.setItem(i, 5, QTableWidgetItem(str(damt)))
            self.table.item(i, 5).setBackground(color)
            i += 1
        self.table.itemSelectionChanged.connect(self.confirmSelection)
        self.table.resizeRowsToContents()
        v_pull_box = QVBoxLayout()
        
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
        #self.connect(self.pull_btn, SIGNAL("clicked()"), lambda x =1: self.reloadTable(x))
       
        self.setWindowTitle(self.pagetitle)
    
    def stateReciept(self):
        self.amountText.show()
        self.amountData.show()
        self.tellerText.show()
        self.tellerData.show()
        self.tellerText.setText('Reciept No.')
        self.periodText.hide()
        self.periodData.hide()
        self.personText.setText('Recieved By:')
        self.personData.setPlaceholderText('Fullname or department')
        self.borrowedText.hide()
        self.borrowedData.hide()
        self.reloadTable(1)
    
    def stateIssue(self):
        self.amountText.hide()
        self.amountData.hide()
        self.tellerText.show()
        self.tellerData.show()
        self.tellerText.setText('Issue No.')
        self.periodText.hide()
        self.periodData.hide()
        self.personText.setText('Issued to:')
        self.personData.setPlaceholderText('Fullname or department issued to')
        self.borrowedText.hide()
        self.borrowedData.hide()
        self.reloadTable(2)
    
    def stateDamage(self):
        self.amountText.hide()
        self.amountData.hide()
        self.tellerText.hide()
        self.tellerData.hide()
        self.periodText.hide()
        self.periodData.hide()
        self.personText.setText('Reported By:')
        self.personData.setPlaceholderText('Fullname or department')
        self.borrowedText.hide()
        self.borrowedData.hide()
        self.reloadTable(3)
        
    def stateBorrowed(self):
        self.amountText.hide()
        self.amountData.hide()
        self.tellerText.hide()
        self.tellerData.hide()
        self.periodText.show()
        self.periodData.show()
        self.personText.setText('Given to:')
        self.personData.setPlaceholderText('Fullname or department borrowed to')
        self.borrowedText.hide()
        self.borrowedData.hide()
        self.reloadTable(4)
        
    def stateReturned(self):
        self.amountText.hide()
        self.amountData.hide()
        self.tellerText.hide()
        self.tellerData.hide()
        self.periodText.hide()
        self.periodData.hide()
        self.personText.setText('Returned By:')
        self.personData.setPlaceholderText('Fullname or department borrowed to')
        self.borrowedText.show()
        self.borrowedData.show()
        self.reloadBorrowed()
        self.reloadTable(5)
        
    def changeStates(self):
        self.getQuantity()
        if self.r1.isChecked():
           self.stateReciept()  
        elif self.r2.isChecked():
           self.stateIssue()
        elif self.r3.isChecked():
           self.stateDamage()
        elif self.r4.isChecked():
           self.stateBorrowed()
        elif self.r5.isChecked():
           self.stateReturned()
    
    def handleHeaderMenu(self, pos):
        print('column(%d)' % self.table.horizontalHeader().logicalIndexAt(pos))
        menu = QMenu()
        menu.addAction('Add')
        menu.addAction('Delete')
        menu.exec_(QCursor.pos()) 
        
    def pullGroupStore(self):
        cn = Db()
        arr = cn.selectn('datas', '' , '', {"pubID":23, "active": 0})
        return arr
    
    def pullStore(self, a):
        cn = Db()
        arr = cn.selectn('datas', '' , '', {"subID":a})
        return arr
    
    def pullUnit(self):
        cn = Db()
        arr = cn.selectn('datas', '' , '', {"pubID":20, "active": 0})
        return arr
    
    def pullStoreData(self, a = None):
        st_date = self.fromData.date().toPyDate()
        en_date = self.toData.date().toPyDate()
        st_date = time.mktime(st_date.timetuple())
        en_date = time.mktime(en_date.timetuple())
        
        db = 'school_stores'+str(self.session)
        cn = Db()
        arr = cn.selectStoreDate(db, st_date, en_date, a )
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
        db = 'school_stores'+str(_session)
        data = g.selectn(db, '', 1, {'id':a})
        if len(data) > 0:
            try:
                amt = float(data['amount'])
                qty = float(data['quantity'])
                if amt > 0 and qty > 0:
                    cost = amt * qty
                else:
                    cost = 0
            except:
                cost = 0
                amt = 0
                qty = 0
                
            if  data['state'] == 1: 
                self.r1.setChecked(True)
            elif  data['state'] == 2: 
                self.r2.setChecked(True)
            elif  data['state'] == 3: 
                self.r3.setChecked(True)
            elif  data['state'] == 4: 
                self.r4.setChecked(True)
            elif  data['state'] == 5: 
                self.r5.setChecked(True)
                
            self.amountData.setText(str(cost))    
            self.descriptionData.clear()
            self.descriptionData.insertPlainText(str(data['description']))
            self.tellerData.setText(str(data['teller']))
            self.periodData.setText(str(data['period']))
            self.personData.setText(str(data['person']))
            self.quantityData.setText(str(qty))
            stID = self.hold_store.keys()[self.hold_store.values().index(data['itemID'])]
            self.storeData.setCurrentIndex(stID)
        
    def reloadBorrowed(self):
        self.getQuantity()
        _store = self.hold_store[self.storeData.currentIndex()]
        _session = self.session
        g = Db()
        db = 'school_stores'+str(_session)
        data = g.selectn(db, '', '', {'itemID': _store, 'state': 4 })
        fig = 0
        self.borrowedData.clear()
        self.hold_borrowed = {}
        i = 0    
        for a in data:
            ret = g.selectStoreReturned(db, a['id'])
            
            if ret:
                retu = ret['qty']
            else:
                retu = 0
            
            fig = float(a['quantity']) - float(retu)   
            damz = float(a['datepaid'])
            if float(fig) > 0:
                self.hold_borrowed[i] = a['id']
                damt = datetime.utcfromtimestamp(damz).strftime('%d-%m-%Y')
                tex = str(damt)+" "+str(a['person']).upper()+" ("+str(fig).upper() +")"
                self.borrowedData.addItem(tex)
                i += 1
        
    def reloadStore(self):
        self.getQuantity()
        cat = self.hold_storeGroup[self.storeGroupData.currentIndex()]
        store = self.pullStore(cat)
        self.storeData.clear()
        self.hold_store = {}
        i = 0
        for a in store:
            self.hold_store[i] = a['id']
            tex = str(a['name']).upper()
            self.storeData.addItem(tex)
            i += 1
            
    def getQuantity(self):
        if self.storeData.currentIndex() > -1:
            s = self.hold_store[self.storeData.currentIndex()]
            _session = self.session
            g = Db()
            db = 'school_stores'+str(_session)
            fi = g.selectStoreQuantity(db, s) 
            remain = 0
            arr = {}
            for a in fi:
                arr[a['state']] = a['qty'] 
                
            if 1 in arr:
                re = arr[1]
            else:
                re = 0
                
            if 2 in arr:
                isu = arr[2]
            else:
                isu = 0
                
            if 3 in arr:
                dam = arr[3]
            else:
                dam = 0
                
            if 4 in arr:
                bor = arr[4]
            else:
                bor = 0
                
            if 5 in arr:
                ret = arr[5]
            else:
                ret = 0
                
            borrowed = float(bor) - float(ret)
            issued = float(isu) + float(borrowed) + float(dam)
            remain = float(re) - float(issued)
            self.quantityText.setText('QTY: '+str( remain))
            if remain == 0 and (self.r2.isChecked() or self.r3.isChecked() or self.r4.isChecked()):
               self.quantityData.setEnabled(False) 
            else:
               self.quantityData.setEnabled(True) 
            return remain
        
            
    
    def reloadTable(self, a):
        self.getQuantity()
        if not a  == 0:
            data = self.pullStoreData(a)
        else:
            data = self.pullStoreData()
            
        self.table.close()
        self.table = QTableWidget()
        header = self.table.horizontalHeader()
        header.setResizeMode(QHeaderView.ResizeToContents)
        header.setStretchLastSection(True)
        header.setStyleSheet(self.tableHeaderStyle)
        vheader = self.table.verticalHeader()
        vheader.setStyleSheet(self.tableHeaderStyle)
            # Body
        self.table.setWindowTitle("Stores")
        self.table.setStyleSheet("color:white")
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
            
            if q['state'] == 1:
                color = QColor(100,0,0)
            elif q['state'] == 2:
                color = QColor(100,100,0)
            elif q['state'] == 3:
                color = QColor(100,0,100)
            elif q['state'] == 4:
                color = QColor(0,100,100) 
            else:
                color = QColor(0,50,150) 
         
            self.table.setItem(i, 0, QTableWidgetItem(str(q['id'])))
            self.table.item(i, 0).setBackground(color)
            self.table.setItem(i, 1, QTableWidgetItem(str(q['itemname']).upper()))
            self.table.item(i, 1).setBackground(color)
            self.table.setItem(i, 2, QTableWidgetItem(str(q['quantity']).upper()))
            self.table.item(i, 2).setBackground(color)
            try:
                zamt = str("{:,}".format(float(q['amount'])))
            except:
                zamt = ''
            self.table.setItem(i, 3, QTableWidgetItem(zamt))
            self.table.item(i, 3).setBackground(color)
            try:
                if len(q['amount']) > 0 and float(q['amount']) > 0:
                    tot = float(q['amount']) * float(q['quantity'])
                else:
                    tot = 0
            except:
                tot = 0
            self.table.setItem(i, 4, QTableWidgetItem(str(tot).upper()))
            self.table.item(i, 4).setBackground(color)
            damz = float(q['datepaid'])
            damt = datetime.utcfromtimestamp(damz).strftime('%d-%m-%Y')
            self.table.setItem(i, 5, QTableWidgetItem(str(damt)))
            self.table.item(i, 5).setBackground(color)
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
        db = 'school_stores'+str(_session)
        for j in item:
            g.delete(db, {'id':j})
        self.reloadTable(1)
        
    def button_edit(self):
        _session = self.session
        _amounts = self.amountData.text()
        _teller = self.tellerData.text()
        _quantity = self.quantityData.text()
        _person = self.personData.text()
        _period = self.periodData.text()
        _date = self.dateData.date().toPyDate()
        _date = time.mktime(_date.timetuple())
        _description = self.descriptionData.toPlainText()
        _store = self.hold_store[self.storeData.currentIndex()]
        _borrowed = self.hold_borrowed[self.borrowedData.currentIndex()]
        
        arr = {}
        #recieved
        if self.r1.isChecked() and _amounts and not(_amounts == 0)  and int(_store) > 0 and int(_quantity) > 0:
            _amount = float(_amounts)/float(_quantity)
            arr['amount'] = _amount
            arr['datepaid'] = _date
            arr['description'] = _description
            arr['itemID'] = _store
            arr['teller'] = _teller
            arr['quantity'] = _quantity
            arr['person'] = _person
            arr['state'] = 1
        #issued    
        elif self.r2.isChecked()   and int(_store) > 0 and int(_quantity) > 0:    
            _amount = float(_amounts)/float(_quantity)
            arr['amount'] = _amount
            arr['datepaid'] = _date
            arr['description'] = _description
            arr['itemID'] = _store
            arr['teller'] = _teller
            arr['quantity'] = _quantity
            arr['person'] = _person
            arr['state'] = 2
        #damaged    
        elif self.r3.isChecked() and int(_store) > 0 and int(_quantity) > 0:
            arr['datepaid'] = _date
            arr['description'] = _description
            arr['itemID'] = _store
            arr['teller'] = _teller
            arr['quantity'] = _quantity
            arr['person'] = _person 
            arr['state'] = 3
        
        elif self.r4.isChecked() and int(_store) > 0 and int(_quantity) > 0:
            arr['datepaid'] = _date
            arr['description'] = _description
            arr['itemID'] = _store
            arr['quantity'] = _quantity
            arr['person'] = _person
            arr['period'] = _period
            arr['state'] = 4
            
        elif self.r5.isChecked() and int(_store) > 0 and int(_quantity) > 0:
            _borrowed = self.hold_borrowed[self.borrowedData.currentIndex()]
            arr['datepaid'] = _date
            arr['description'] = _description
            arr['itemID'] = _store
            arr['quantity'] = _quantity
            arr['person'] = _person
            arr['period'] = _period
            arr['active'] = _borrowed
            arr['state'] = 5
            
            
        ups = {}
        ups['id'] = self.editID 
        if int(self.editID) > 0 and len(arr) > 0:
            db = 'school_stores'+str(_session)
            g = Db()
            g.update(db, arr, ups)
            if int(self.editID) > 0:
                self.button_reset()
                    
    def button_reset(self):
        self.getQuantity()
        self.reloadTable(1)
        self.amountData.setText('')
        self.descriptionData.clear()
        self.tellerData.setText('')
        self.personData.setText('')
        self.periodData.setText('')
        self.quantityData.setText('')
        self.pb4.hide()
        self.pb5.hide()
        self.pb.show()
        self.editID = 0
        self.button_clear()
        self.confirmSelection()
        self.reloadBorrowed()
        
    def button_clear(self):
        self.table.selectionModel().clearSelection()
        
        
    def button_click(self):
        _session = self.session
        _amounts = self.amountData.text()
        _teller = self.tellerData.text()
        _quantity = self.quantityData.text()
        _person = self.personData.text()
        _period = self.periodData.text()
        _date = self.dateData.date().toPyDate()
        _date = time.mktime(_date.timetuple())
        _description = self.descriptionData.toPlainText()
        _store = self.hold_store[self.storeData.currentIndex()]
        
        
        
        arr = {}
        #recieved
        if self.r1.isChecked() and _amounts and not(_amounts == 0)  and int(_store) > 0 and int(_quantity) > 0:
            _amount = float(_amounts)/float(_quantity)
            arr['amount'] = _amount
            arr['datepaid'] = _date
            arr['description'] = _description
            arr['itemID'] = _store
            arr['teller'] = _teller
            arr['quantity'] = _quantity
            arr['person'] = _person
            arr['state'] = 1
        #issued    
        elif self.r2.isChecked() and _amounts and not(_amounts == 0)  and int(_store) > 0 and int(_quantity) > 0:    
            _amount = float(_amounts)/float(_quantity)
            arr['amount'] = _amount
            arr['datepaid'] = _date
            arr['description'] = _description
            arr['itemID'] = _store
            arr['teller'] = _teller
            arr['quantity'] = _quantity
            arr['person'] = _person
            arr['state'] = 2
        #damaged    
        elif self.r3.isChecked() and int(_store) > 0 and int(float(_quantity)) > 0:
            arr['datepaid'] = _date
            arr['description'] = _description
            arr['itemID'] = _store
            arr['teller'] = _teller
            arr['quantity'] = _quantity
            arr['person'] = _person 
            arr['state'] = 3
        
        elif self.r4.isChecked() and int(_store) > 0 and int(float(_quantity)) > 0:
            arr['datepaid'] = _date
            arr['description'] = _description
            arr['itemID'] = _store
            arr['quantity'] = _quantity
            arr['person'] = _person
            arr['period'] = _period
            arr['state'] = 4
        
        elif self.r5.isChecked() and int(_store) > 0 and int(float(_quantity)) > 0 and self.borrowedData.currentIndex() > 0:
            _borrowed = self.hold_borrowed[self.borrowedData.currentIndex()]
            arr['datepaid'] = _date
            arr['description'] = _description
            arr['itemID'] = _store
            arr['quantity'] = _quantity
            arr['person'] = _person
            arr['period'] = _period
            arr['active'] = _borrowed
            arr['state'] = 5
            
        
        if len(arr) > 0:
            db = 'school_stores'+str(_session)
            g = Db()
            ins = g.insert(db, arr)
            if int(ins) > 0:
                self.button_reset()
                
            
        
    
