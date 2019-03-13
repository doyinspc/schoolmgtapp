# -*- coding: utf-8 -*-
"""
Created on Sat Jul  7 15:54:19 2018

@author: CHARLES
"""
from PyQt4.QtCore import SIGNAL, Qt, QDateTime
from PyQt4.QtGui import QWidget, QTreeWidget, QMessageBox,  QTreeWidgetItem, QComboBox, QFrame, QDateEdit, QRadioButton, QCheckBox, QHBoxLayout, QGroupBox, QGridLayout, QDialog, QApplication, QPushButton, QLineEdit, QFormLayout, QLabel, QVBoxLayout
from dialogreport import ReportDialog, EditReportDialog
from connect import Db
from connectstudents import Con
from studenttable import StudentTable

class TermPayDialog(QDialog):
    
    holdc = {}
    def __init__(self, student, term, parent=None):
        super(TermPayDialog, self).__init__(parent)
        #term data
        self.term = term
        terms = self.pullOnes('terms', self.term)
        session = self.pullOnes('session', terms['sessionID'])
        self.termname = str(session['name'])+' '+terms['name']+' Term Report'
        self.pagetitle = self.termname 
        
        #student data
        self.student = student
        st = self.pullStudent(self.student)
        fullname = str(st['surname']+' '+st['firstname']+' '+st['othername']).title()
        schno = st['schno']
        db_class = 'student_class'+str(self.term)
        student_clasz = self.pullOne(db_class, {'studentID':self.student})

        clasz = self.pullOne('datas', {'id':student_clasz['classID']})
        self.clasz = clasz['subID'];
        armz = self.pullOne('datas', {'id':clasz['subID']})
        classname = armz['abbrv']+' '+clasz['abbrv']
        #pull all CA
        
        fullNameText = QLabel(fullname)
        schnoText = QLabel(schno)
        classText = QLabel(classname)
        
        topLay = QGridLayout()
        topLay.addWidget(fullNameText, 0,0)
        topLay.addWidget(schnoText, 1,0)
        topLay.addWidget(classText, 2,0)
        
        groupBox = QGroupBox('Current Payment')
        groupBox.setLayout(topLay)
        
        payAmountText = QLabel('Amount')
        self.payBalanceText = QLabel('Balance')
        self.payBalanceAmount = QLabel('0.0')
        self.payAmount = QLineEdit()
        self.payAmount.setObjectName("pay")
        self.payAmount.setPlaceholderText("000.00")
        payText = QLabel('Select Account')
        self.payMethod = QComboBox()
        accounts = self.pullAccount()
        self.holdaccount = {}
        i = 0
        for h in accounts:
            tex = str(h['name']).upper()
            self.payMethod.addItem(tex)
            self.holdaccount[i] = h['id']
            
        payDateText = QLabel('Balance')
        self.payDate = QDateEdit()
        self.payDate.setDateTime(QDateTime.currentDateTime())
        self.payDate.setCalendarPopup(True)
        tellerText = QLabel('Teller/Receipt No.')
        self.teller = QLineEdit()
        self.teller.setObjectName("teller")
        self.teller.textChanged.connect(self.pullTeller)
        self.teller.setPlaceholderText("0000000")
        
        self.hw = QGridLayout()
        self.hw.addWidget(payAmountText, 0, 0)
        self.hw.addWidget(self.payAmount, 0, 1)
        self.hw.addWidget(tellerText, 0, 2)
        self.hw.addWidget(self.teller, 0, 3)
        self.hw.addWidget(payText, 1, 0)
        self.hw.addWidget(self.payMethod, 1, 1)
        self.hw.addWidget(payDateText, 1, 2)
        self.hw.addWidget(self.payDate, 1, 3)
        
        head_col1 = QLabel('ITEM')
        head_col2 = QLabel('AMOUNT')
        head_col3 = QLabel('FULL PAY')
        head_col4 = QLabel('PART PAY')
        head_col5 = QLabel('BALANCE')
        
        layout1 = QGridLayout()
        layout1.addWidget(head_col1, 0, 0)
        layout1.addWidget(head_col2, 0, 1)
        layout1.addWidget(head_col3, 0, 2)
        layout1.addWidget(head_col4, 0, 3)
        layout1.addWidget(head_col5, 0, 4)
        
        arr = self.pullFees()
        feex = arr[1]
        payx = arr[2]
        
        normal_pay = []
        full_pay = []
        part_pay = []
        bal_pay = []
        ko = 1
        
        self.holdval =[]
        self.holdfee ={}
        self.holdtextfee ={}
        self.holdtextfeeperm ={}
        self.holdpaid ={}
        self.holdcpaid ={}
        self.holdtextpaid ={}
        self.holdpayments ={}
        self.holdtextbal ={}
        self.holdbal ={}
        
        for val in arr[0]:
            paid = False
            s_normal_pay = []
            s_full_pay = []
            s_part_pay = []
            self.holdval.append(val)
            mz = self.pullOne('datas', {'id':val})
            self.num = val
            self.d = QLabel('Text')
            self.d.setText(str(mz['name']).upper())
            self.d1 = QLabel()
            if val in feex:
                fk = feex[int(val)].values()
                normal_pay.append(float(fk[0]))
                s_normal_pay.append(float(fk[0]))
                self.d1.setText(str("{:,}".format(float(fk[0]))).upper())
            else:
                self.d1.setText(str('-.-').upper())
            
            
            nHbo1 = QVBoxLayout()
            if val in feex:
                fk = feex[int(val)].values()
                fky = feex[int(val)].keys()
                self.c = QCheckBox('cb'+str(val))
                self.c.setEnabled(False)
                self.c.setText(str("{:,}".format(float(fk[0]))).upper())
                self.c.setObjectName("chk"+str(val))
                self.holdfee[int(val)] = self.c
                self.holdtextfee[int(val)] = fk[0]
                self.holdtextfeeperm[int(val)] = fk[0]
                self.c.toggled.connect(lambda state, x = fky[0], fee = int(val), money=fk[0]: self.chkFunc(x, fee,  money, self.c))
                if (val in payx) and len(payx[int(val)]) == 1:
                    pk = payx[int(val)].values()
                    self.c.setChecked(True)
                    if float(pk[0]) == float(fk[0]):
                        full_pay.append(float(fk[0]))
                        s_full_pay.append(float(fk[0]))
                        paid = True
                else:
                    self.c.setChecked(False)  
                nHbo1.addWidget(self.c)
            else:
                nHbo1.addWidget(QLabel('-.-'))
                #nHbo1.hide()
                
            nHbo2 = QHBoxLayout() 
            fk = feex[int(val)].values()
            fky = feex[int(val)].keys()
            c2 = QCheckBox()
            c2.setEnabled(False)
            c2.setMaximumWidth(15)
            c2.setObjectName("chk2"+str(val))
            p = QLineEdit()
            p.setDisabled(True)
            p.setMaximumWidth(50)
            p.setFixedWidth(51)
            p.setObjectName("pay"+str(val))
            p.setPlaceholderText("00.0")
            self.holdpaid[int(val)] = p
            self.holdcpaid[int(val)] = c2
            self.holdtextpaid[int(val)] = list()
            c2.toggled.connect(lambda state, x = fky[0], fee = int(val): self.chkFunc1(x, fee, p))
            if paid == False: 
                nHbo2.addWidget(c2)
                nHbo2.addWidget(p)
                if val in payx and len(payx[val]) > 0:
                    for j in payx[int(val)]:
                        self.c1 = QCheckBox('cb1'+str(j))
                        self.c1.setEnabled(False)
                        self.c1.setText(str(payx[int(val)][j]).upper())
                        self.c1.setObjectName("chk"+str(j))
                        self.c1.toggled.connect(lambda state, x=j: self.chkFunc1(x))
                        self.c1.setChecked(True)
                        part_pay.append(float(fk[0]))
                        s_part_pay.append(float(fk[0]))
                        self.holdpayments[j] = self.c1
                        self.holdtextpaid[val].append(float(fk[0]))
                        nHbo2.addWidget(self.c1)
                else:
                    pass
            else:
                p.hide()
                c2.hide()
                nHbo2.addWidget(c2)
                nHbo2.addWidget(p)
                
            s_tot = sum(s_normal_pay) - (sum(s_full_pay) + sum(s_part_pay))
            bal_pay.append(float(s_tot))
            d2 = QLabel('')
            self.holdbal[int(val)] = d2
            d2.setText(str("{:,}".format(s_tot)).upper())
            self.holdtextbal[int(val)] = s_tot
            
            layout1.addWidget(self.d, ko, 0)
            layout1.addWidget(self.d1, ko, 1)
            layout1.addLayout(nHbo1, ko, 2)
            layout1.addLayout(nHbo2, ko, 3)
            layout1.addWidget(d2, ko, 4)
            ko += 1
        
        normal_payx = sum(normal_pay)
        full_payx = sum(full_pay)
        part_payx = sum(part_pay)
        bal_payx = sum(bal_pay)
        
        self.head_col1 = QLabel('ITEM')
        self.head_col2 = QLabel(str("{:,}".format(normal_payx)).upper())
        self.head_col3 = QLabel(str("{:,}".format(full_payx)).upper())
        self.head_col4 = QLabel(str("{:,}".format(part_payx)).upper())
        self.head_col5 = QLabel(str("{:,}".format(bal_payx)).upper())
        
        layout1.addWidget(self.head_col1, ko, 0)
        layout1.addWidget(self.head_col2, ko, 1)
        layout1.addWidget(self.head_col3, ko, 2)
        layout1.addWidget(self.head_col4, ko, 3)
        layout1.addWidget(self.head_col5, ko, 4)
        
        self.hw1 = QGridLayout()
        self.hw1.addWidget(self.payBalanceText, 0, 0)
        self.hw1.addWidget(self.payBalanceAmount, 1, 0 )
              
        second1 = QGridLayout()
        second1.addLayout(self.hw, 0, 0)
        second1.addLayout(layout1, 1, 0)
        second1.addLayout(self.hw1, 2, 0)
                          
        groupBox1 = QGroupBox('Current Payment')
        groupBox1.setLayout(second1)
        
        self.pb = QPushButton()
        self.pb.setObjectName("Add")
        self.pb.setText("Add Fees")
        
        self.pb1 = QPushButton()
        self.pb1.setObjectName("Cancel")
        self.pb1.setText("Cancel")
        
        self.pb2 = QPushButton()
        self.pb2.setObjectName("Add")
        self.pb2.setText("Print Receipts")
        
        hbo = QHBoxLayout()
        hbo.addWidget(self.pb1)
        hbo.addStretch()
        hbo.addWidget(self.pb)
        hbo.addStretch()
        hbo.addWidget(self.pb2)
        groupBox2 = QGroupBox('')
        groupBox2.setLayout(hbo)
        
        grid = QGridLayout()
        grid.addWidget(groupBox, 0, 0)
        grid.addWidget(groupBox1, 1, 0)
        grid.addWidget(groupBox2, 2, 0)
        
        self.setLayout(grid)
        self.connect(self.pb, SIGNAL("clicked()"), lambda: self.button_click())
        self.connect(self.pb1, SIGNAL("clicked()"), lambda: self.button_close(self))
       
        self.setWindowTitle(self.pagetitle)

    
    
    def reCalFull(self):
        fees_arr = self.holdfee
        fee_store = list()
        for a in fees_arr:
            if fees_arr[a].isChecked() == True:
                h = self.holdtextfee[a]
                fee_store.append(float(h))
            else:
                pass
        
        fee_sum = sum(fee_store)
        self.head_col3.setText('{:,}'.format(fee_sum))
        
    def reCalPart(self):
        fees_arr = self.holdtextpaid
        fee_store = list()
        for a in fees_arr:
            if self.holdtextpaid[a]:
                h = sum(self.holdtextpaid[a])
                fee_store.append(float(h))
        
        fee_sum = sum(fee_store)
        self.head_col4.setText('{:,}'.format(fee_sum))
        
    def reCalBal(self):
        bal_arr = self.holdbal
        bal_store = list()
        for a in bal_arr:
            h = self.holdtextbal[a]
            bal_store.append(float(h))
            
        bal_sum = sum(bal_store)
        self.head_col5.setText('{:,}'.format(bal_sum))
        
    def reCalSingleBal(self):
        bal_arr = self.holdval
        fees_arr = self.holdfee
        for a in bal_arr:
            if fees_arr[a].isChecked() == True:
                b = self.holdtextfee[a]
                self.holdbal[a].setText('{:,}'.format(0))
                self.holdtextbal[a] = 0
            elif fees_arr[a].isChecked() == False:
                b = self.holdtextfee[a]
                self.holdbal[a].setText('{:,}'.format(float(b)))
                self.holdtextbal[a] = float(b)
        
        self.reCalBal()
                
    def chkFunc(self, a, c, d, b):
        # checkbox select to make fuul payment
        self.a = a
        db_fee = 'student_fee'+str(self.term);
        db_pay = 'student_pay'+str(self.term);
        amount = self.payAmount.text()
        teller = self.teller.text()
        # get all paments made for that fee
        # get the check box 
        g = Db()
        fee = g.selectn(db_fee, '', 1, {'id':a})
        loc = self.holdfee[int(fee['feeID'])]
        poc = self.holdpaid[int(fee['feeID'])]
        pocc = self.holdcpaid[int(fee['feeID'])]
        
        try:
            ## fee was checked full pay
            ## confirm if money posted and its greater than or equals
            # confimr if teller number was provided
            ## if those conditions are met payment of fees is possible
            
            if (float(amount) >= float(d)) and len(str(teller)) > 0:
                # confirm if the checkbox was checked
                if loc.isChecked() == True:
                    
                    #if it was checked prepare to insert payment data
                    pay ={}
                    pay['studentID'] = self.student
                    pay['accountID'] = self.payAmount.text()
                    pay['amount'] = d
                    pay['teller'] = teller
                    pay['feeID'] = fee['feeID']
                    pay['datepaid'] = self.payDate.date().toPyDate()
                    # however confirm if full payment had bee made b4
                    dat = g.select(db_pay, '', '' , {'studentID':self.student, 'feeID':fee['feeID']})
                    if dat and len(dat) > 0 and float(dat[0]['amount']) > 0 and float(dat[0]['amount']) == float(d):
                        # full payment made
                        # dont post
                        # keep part pay disabled
                        poc.hide()
                        pocc.hide()
                        # inform user
                        msg = QMessageBox()
                        msg.setIcon(QMessageBox.Information)
                        msg.setWindowTitle("Info")
                        msg.setText("This fee has already been paid for. You cannot repay for it")
                        msg.setStandardButtons(QMessageBox.Cancel)
                        msg.exec_()
                    else:
                        # post payment
                        h = g.insert(db_pay, pay)
                        if int(h) > 0:
                            # deduct from balance
                            
                            # keep part pay disabled]
                            poc.hide()
                            pocc.hide()
                            # recalculate 
                            self.reCalFull()
                            self.reCalSingleBal()
                        else:
                            poc.show()

                else:
                    # money was not posted
                    if len(str(self.teller.text())) > 0:
                        pay ={}
                        pay['studentID'] = self.student
                        pay['teller'] = self.teller.text()
                        pay['feeID'] = fee['feeID']
                        h = g.delete(db_pay, pay)
                        poc.show()
                        pocc.show()
                        self.reCalFull()
                        self.reCalSingleBal()

                    else:
                        msg = QMessageBox()
                        msg.setIcon(QMessageBox.Information)
                        msg.setWindowTitle("Info")
                        msg.setText("Please provide the teller/receipt details before removing amount.")
                        msg.setStandardButtons(QMessageBox.Cancel)
                        msg.exec_()
                    #add to money
            ## if those conditions are not met
            # payment of fees is not possible
            # however user might want to revoke a payment
            # meaning checkbox was unchecked 
            else:
                if loc.isChecked() == False:
                    # prepare to remove payment
                    pay ={}
                    pay['studentID'] = self.student
                    pay['teller'] = self.teller.text()
                    pay['feeID'] = fee['feeID']
                    # remove payment
                    h = g.delete(db_pay, pay)
                    # confirm if removal was succesful
                    if h == 1:
                        # if successful
                        poc.show()
                        pocc.show()
                        # refund balance
                        
                        # recalculate
                        self.reCalFull()
                        self.reCalSingleBal()
                    else:
                        # not sussefull
                        # details not complete
                        #restore it to check 
                        #loc.setChecked(True)
                        poc.hide()
                        pocc.hide()
                        # inform user
                        msg = QMessageBox()
                        msg.setIcon(QMessageBox.Information)
                        msg.setWindowTitle("Safety Measure:")
                        msg.setText("You will need to enter the correct teller/receipt details for this payment before removing it")
                        msg.setStandardButtons(QMessageBox.Cancel)
                        msg.exec_()
                    
                # user trying to make payment with no funds
                else:
                    # uncheck user
                    loc.setChecked(False)
                    poc.show()
                    pocc.show()
                    #give info
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Information)
                    msg.setWindowTitle(" Payment Error")
                    msg.setText("Please provide teller/receipt details or Insufficient funds to make full payments ")
                    msg.setStandardButtons(QMessageBox.Cancel)
                    msg.exec_()
        except:
                if loc.isChecked() == False:
                # money was not posted
                    if len(str(self.teller.text())) > 0:
                        pay ={}
                        pay['studentID'] = self.student
                        pay['teller'] = self.teller.text()
                        pay['feeID'] = fee['feeID']
                        h = g.delete(db_pay, pay)
                        poc.show()
                        pocc.show()
                        self.reCalFull()
                        self.reCalSingleBal()
                    else:
                        pass
                    
                else:
                    loc.setChecked(False)
                    poc.show()
                    pocc.show()
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Information)
                    msg.setWindowTitle(" Payment Error:")
                    msg.setText("Please insert amount and Teller/Receipt details ")
                    msg.setStandardButtons(QMessageBox.Cancel)
                    msg.exec_()
        
    def chkFunc1(self, a, b, c):
        # checkbox select to make fuul payment
        self.a = a
        db_fee = 'student_fee'+str(self.term);
        db_pay = 'student_pay'+str(self.term);
       
        amount = self.payAmount.text()
        teller = self.teller.text()
        # get all paments made for that fee
        # get the check box 
        g = Db()
        fee = g.selectn(db_fee, '', 1, {'id':a})
        loc = self.holdfee[b]
        payfull = self.holdtextfee[b]
        pocc = self.holdpaid[b]
        poc = self.holdcpaid[b]
        
        d = pocc.text()
       
        try:
            ## fee was checked full pay
            ## confirm if money posted and its greater than or equals
            # confimr if teller number was provided
            ## if those conditions are met payment of fees is possible
            if (float(amount) >= float(d)) and len(str(teller)) > 0:
                # confirm if the checkbox was checked
                if poc.isChecked() == True:              
                    #if it was checked prepare to insert payment data
                    pay ={}
                    pay['studentID'] = self.student
                    pay['accountID'] = self.payAmount.text()
                    pay['teller'] = teller
                    pay['feeID'] = fee['feeID']
                    pay['datepaid'] = self.payDate.date().toPyDate()
                    # however confirm if full payment had bee made b4
                    dat = g.selectn(db_pay, '', '' , {'studentID':self.student, 'feeID':fee['feeID']})
                   
                    if dat and len(dat) > 0:
                        mon = list()
                        for dd in dat:
                            mon.append(float(dd['amount']))
                        # full payment made
                        # dont post
                        # keep part pay disabled
                        total_money_paid = sum(mon)
                        #no payments required
                        if float(total_money_paid)  >= float(payfull):
                            pass
                        #payment required
                        elif float(total_money_paid)  < float(payfull):
                            if float(amount) >= float(d):
                                pay['amount'] = d
                                #post
                                h = g.insert(db_pay, pay)
                                if int(h) > 0:
                                    # deduct from balance
                                    
                                    # keep part pay disabled]
                                    loc.hide()
                                    pocc.setDisabled(True)
                                    # recalculate 
                                    self.reCalFull()
                                    self.reCalPart()
                                    self.reCalSingleBal()
                                else:
                                    poc.show() 
                            else:
                                msg = QMessageBox()
                                msg.setIcon(QMessageBox.Information)
                                msg.setWindowTitle("Info")
                                msg.setText("Insufficient funds.")
                                msg.setStandardButtons(QMessageBox.Cancel)
                                msg.exec_()
                           
                        loc.hide()
                        pocc.setDisabled(True)
                        # inform user
                       
                    else:
                        # post payment
                        if float(amount) >= float(d):
                            pay['amount'] = d
                            
                                #post
                            h = g.insert(db_pay, pay)
                          
                            if int(h) > 0:
                                    # deduct from balance
                                    
                                    # keep part pay disabled]
                                    loc.hide()
                                    pocc.setDisabled(True)
                                    # recalculate 
                                    self.reCalFull()
                                    self.reCalSingleBal()
                            else:
                                    poc.show() 

                    # money was not posted
                    if len(str(self.teller.text())) > 0:
                        pay ={}
                        pay['studentID'] = self.student
                        pay['teller'] = self.teller.text()
                        pay['feeID'] = fee['feeID']
                        h = g.delete(db_pay, pay)
                        poc.show()
                        pocc.show()
                        self.reCalFull()
                        self.reCalSingleBal()

                    else:
                        msg = QMessageBox()
                        msg.setIcon(QMessageBox.Information)
                        msg.setWindowTitle("Info")
                        msg.setText("Please provide the teller/receipt details before removing amount.")
                        msg.setStandardButtons(QMessageBox.Cancel)
                        msg.exec_()
                    #add to money
            ## if those conditions are not met
            # payment of fees is not possible
            # however user might want to revoke a payment
            # meaning checkbox was unchecked 
            else:
                if loc.isChecked() == False:
                    # prepare to remove payment
                    pay ={}
                    pay['studentID'] = self.student
                    pay['teller'] = self.teller.text()
                    pay['feeID'] = fee['feeID']
                    # remove payment
                    h = g.delete(db_pay, pay)
                    # confirm if removal was succesful
                    if h == 1:
                        # if successful
                        poc.show()
                        pocc.show()
                        # refund balance
                        
                        # recalculate
                        self.reCalFull()
                        self.reCalSingleBal()
                    else:
                        # not sussefull
                        # details not complete
                        #restore it to check 
                        #loc.setChecked(True)
                        poc.hide()
                        pocc.hide()
                        # inform user
                        msg = QMessageBox()
                        msg.setIcon(QMessageBox.Information)
                        msg.setWindowTitle("Safety Measure:")
                        msg.setText("You will need to enter the correct teller/receipt details for this payment before removing it")
                        msg.setStandardButtons(QMessageBox.Cancel)
                        msg.exec_()
                    
                # user trying to make payment with no funds
                else:
                    # uncheck user
                    loc.setChecked(False)
                    poc.show()
                    pocc.show()
                    #give info
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Information)
                    msg.setWindowTitle(" Payment Error")
                    msg.setText("Please provide teller/receipt details or Insufficient funds to make full payments ")
                    msg.setStandardButtons(QMessageBox.Cancel)
                    msg.exec_()
        except:
                
                if loc.isChecked() == False:
                # money was not posted
                    if len(str(self.teller.text())) > 0:
                        pay ={}
                        pay['studentID'] = self.student
                        pay['teller'] = self.teller.text()
                        pay['feeID'] = fee['feeID']
                        h = g.delete(db_pay, pay)
                        poc.show()
                        pocc.show()
                        self.reCalFull()
                        self.reCalSingleBal()
                    else:
                        pass
                    
                else:
                    loc.setChecked(False)
                    poc.show()
                    pocc.show()
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Information)
                    msg.setWindowTitle(" Payment Error:")
                    msg.setText("Please insert amount and Teller/Receipt details ")
                    msg.setStandardButtons(QMessageBox.Cancel)
                    msg.exec_()
            
    
    def getClass(self, x):
        # shost is a QString object
        class_arr = []
        for i in self.cla_arr:
            if self.cla_arr[i].checkState(0) == Qt.Checked:
                        class_arr.append(i)
                        
        c = self.getClassStudent(class_arr)
        self.feesPop.setText('Total: '+ str(c[0]))
        self.cla = class_arr
        self.students = c[1]

    
    def pullStudent(self, student):
        cn = Db()
        arr = cn.selectn('students', '' , 1, {'id': student})
        return arr
    
    def pullTeller(self):
        cn = Con()
        teller = self.teller.text()
        if len(str(teller)) > 0:
            h1 = self.holdfee
            for x in h1:
                h1[x].setEnabled(True)
                
            h2 = self.holdpaid
            h3 = self.holdcpaid
            for x in h2:
                h2[x].setEnabled(True)
                h3[x].setEnabled(True)
        else:
            h1 = self.holdfee
            for x in h1:
                h1[x].setEnabled(False)
                
            h2 = self.holdpaid
            h3 = self.holdcpaid
            for x in h2:
                h2[x].setEnabled(False)
                h3[x].setEnabled(False)
                
        arr = cn.getTeller(self.term, self.student, teller)
        arr1 = cn.getNonTeller(self.term, self.student, teller)
        
        amount = self.payAmount.text()
        
        if amount and (float(amount) > 0):
            if arr1 and float(arr1['amount']) > 0:
                self.payBalanceAmount.setText('This teller :'+str(teller)+' is already in use ')
            else:
                if arr and float(arr['amount']) > 0:
                    amt = arr['amount']
                    amt_a = "{:,}".format(float(amt))
                    bl = float(amount) - float(amt)
                    bl_a = "{:,}".format(float(bl))
                    self.payBalanceAmount.setText('The sum of'+ str(amt_a) +' has been deducted from this teller')
                    self.payBalanceText.setText('Balance on '+ str(teller) +' : '+str(bl_a)+'')
                else:
                    bl = float(amount)
                    bl_a = "{:,}".format(float(bl))
                    self.payBalanceAmount.setText('No transaction on teller :'+str(teller)) 
                    self.payBalanceText.setText('Balance on '+ str(teller) +' : '+str(bl_a)+'')
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle("Error")
            msg.setText("Error! Please enter an amount before you proceed...")
            msg.setStandardButtons(QMessageBox.Cancel)
            msg.exec_()
    
    def pullFees(self):
        term = self.term
        student = self.student
        fee_id_array = []
        cn = Db()
        db_fee = 'student_fee'+str(term)
        db_pay = 'student_pay'+str(term) 
        
        fee = cn.selectn(db_fee, '' , '', {'studentID': student})
        pay = cn.selectn(db_pay, '' , '', {'studentID': student})
        #get all fees
        arr = {}
        arr1 = {}
        for r in fee:
            fee_id_array.append(int(r['feeID']))
            arr[int(r['feeID'])] = {}
        
        for r in pay:
            fee_id_array.append(int(r['feeID']))
            arr1[int(r['feeID'])] = {}
            
        for r in fee:
            get_mon = cn.selectn('datas', '', 1, {'pubID': 'fee', 'subID':self.term, 'name':self.clasz, 'abbrv': r['feeID']})
            if arr[int(r['feeID'])] and isinstance(arr[int(r['feeID'])], dict):
               arr[int(r['feeID'])][int(r['id'])] = get_mon['description']
            else:
               arr[int(r['feeID'])] = {}
               arr[int(r['feeID'])][int(r['id'])] = get_mon['description']
        
        for r in pay:
            if arr1[int(r['feeID'])] and isinstance(arr1[int(r['feeID'])], dict):
               arr1[int(r['feeID'])][int(r['id'])] = r['amount']
            else:
               arr1[int(r['feeID'])] = {}
               arr1[int(r['feeID'])][int(r['id'])] = r['amount']
          
        fee_ids = list(set(fee_id_array))
        fin = [fee_ids, arr, arr1]
        return fin
    
    def pullOne(self, a,  b):
        cn = Db()
        arr = cn.selectn(a, '' , 1, b)
        return arr
    
    def pullOnes(self, a, b):
        cn = Db()
        arr = cn.selectn(a, '' , 1, {'id': b})
        return arr
    
    def pullAccount(self):
        cn = Db()
        arr = cn.selectn('datas', '' , '', {"pubID":20, "active": 0})
        return arr
    
    def pullRep(self):
        cn = Db()
        ca = "rep"
        arr = cn.selectn('datas', '' , '', {"subID": self.sid, "pubID": ca})
        return arr
    
    def button_close(self, b):
        b.close()
         
    def button_click(self):
        tex = ' Please wait processing, do not cancel or close..';
        self.feesPop.setText(tex)
        _term = self.term
        _class = self.cla
        _students = self.students
        _amount = self.feesAmount.text()
        _fee = self.hol[self.feesCombo.currentIndex()]
         
        for j in _class:
            data = {}
            data['pubID'] = 'fee'
            data['subID'] = _term
            data['abbrv'] = _fee
            data['name'] =  j
        
            cn = Db()
            feeStudent = self.feeStudents(_term, _students, _fee, _amount)
            check = cn.selectn('datas', '', 1, data)
            if(check and check['id'] == 0):
                pass
            else:
                data['description'] =  _amount
                cn.insert('datas', data)
    
        ins = feeStudent
        tex = ' TOTAL of '+ str(ins) +' inserted';
        self.feesPop.setText(tex)
        
    def feeStudents(self, session, students, fee, amount):
        db = 'student_fee'+str(session)
        cn = Db()
        fd = []
        ed = []
        
        for s in students:
            data = {}
            data['studentID'] = s[0]
            data['feeID'] = fee
            
            chk = cn.selectn(db, '', 1, data)
            if(chk and int(chk['id']) > 0):
                #confirm if money available
                pass
            else:
                #if money not set , set
                e = cn.insert(db, data)
                ed.append(e)
                
        return len(ed)
        
    def lunchEditForm(self, row):
        term = self.term
        self.close()
        self.post = EditReportDialog(term, row)
        self.post.show()
        
    def lunchDeleteForm(self, row):
        cn = Db()
        arr = cn.update('datas', {"active": 1})
        self.close()
        self.__init__(self.term, self.termname)
        
    
    
