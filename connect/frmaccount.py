
"""
Created on Sat Jul  7 15:54:19 2018

@author: CHARLES
"""
from PyQt4.QtCore import SIGNAL, QDate, Qt, QEvent
from PyQt4.QtGui import QStyledItemDelegate,  QStyle, QStyleOptionButton, QTreeWidget, QTreeWidgetItem, QWidget, QIcon, QDateEdit, QRadioButton, QCheckBox, QHBoxLayout, QGroupBox, QGridLayout, QDialog, QApplication, QPushButton, QLineEdit, QFormLayout, QLabel, QVBoxLayout
from connect import Db
from validate import Valid, Buttons, Settingz
import time
from datetime import datetime

class SettingsManager(QDialog):
    def __init__(self, num, n, parent=None):
       super(SettingsManager, self).__init__(parent) 
       
       #main
       self.par = n
       title = Settingz().positions(num)
       self.titleID = title['id']
       self.titleIDx = str(title['id'])+'x'
       self.titlePage = title['page']
       self.titleName = title['name']
       self.titleSub = title['subID']
       self.titleIcon = title['icon']
       self.pagetitle = self.titlePage
       self.sessionMain = 0
       #stylesheet
       stylesheet = Valid().background() + Valid().font()
       treeStyleSheet =  Valid().treez()
       
       self.groupBox1 = QGroupBox(self.titleName)
       self.groupBox2 = QGroupBox('Add')
    
       #items
       self.tree = QTreeWidget()
       self.tree.setHeaderLabel("Choose "+self.titleName)
       self.tree.headerItem().setText(0, 'Name')
       self.tree.headerItem().setText(1, 'Abbrv.')
       self.tree.setStyleSheet(treeStyleSheet)
       self.makeTree()
       self.tree.setMinimumHeight(250)
       self.tree.clicked.connect(lambda:self.getSelection())
       self.tree.itemClicked.connect(lambda state:self.getChecked(state))
       #buttons
       #add
       nImg = Buttons().addButton()
       self.pb = QPushButton()
       self.pb.setFlat(True)
       self.pb.setIcon(QIcon(nImg))
       self.pb.setMaximumHeight(30)
       self.pb.setMaximumWidth(30)
        
       nImg1 = Buttons().closeButton()
       self.pb1 = QPushButton()
       self.pb1.setFlat(True)
       self.pb1.setIcon(QIcon(nImg1))
       self.pb1.setMaximumHeight(30)
       self.pb1.setMaximumWidth(30)
       
       nImg2 = Buttons().editButton()
       self.pb2 = QPushButton()
       self.pb2.setFlat(True)
       self.pb2.setIcon(QIcon(nImg2))
       self.pb2.setMaximumHeight(30)
       self.pb2.setMaximumWidth(30)
       
       nImg3 = Buttons().deleteButton()
       self.pb3 = QPushButton()
       self.pb3.setFlat(True)
       self.pb3.setIcon(QIcon(nImg3))
       self.pb3.setMaximumHeight(30)
       self.pb3.setMaximumWidth(30)
       
       nImg4 = Buttons().saveButton()
       self.pb4 = QPushButton()
       self.pb4.setFlat(True)
       self.pb4.setIcon(QIcon(nImg4))
       self.pb4.setMaximumHeight(30)
       self.pb4.setMaximumWidth(30)
       
       nImg5 = Buttons().resetButton()
       self.pb5 = QPushButton()
       self.pb5.setFlat(True)
       self.pb5.setIcon(QIcon(nImg5))
       self.pb5.setMaximumHeight(30)
       self.pb5.setMaximumWidth(30)
       
       nImg6 = Buttons().closeButton()
       self.pb6 = QPushButton()
       self.pb6.setFlat(True)
       self.pb6.setIcon(QIcon(nImg6))
       self.pb6.setMaximumHeight(30)
       self.pb6.setMaximumWidth(30)
       
       nImg7 = Buttons().addButton()
       self.pb7 = QPushButton()
       self.pb7.setFlat(True)
       self.pb7.setIcon(QIcon(nImg7))
       self.pb7.setMaximumHeight(30)
       self.pb7.setMaximumWidth(30)
        
       hbo = QHBoxLayout()
       hbo.addStretch()
       hbo.addWidget(self.pb1)
       hbo.addWidget(self.pb3)
       hbo.addWidget(self.pb2)
       hbo.addWidget(self.pb7)
       
       vbo = QVBoxLayout()
       vbo.addWidget(self.tree)
       vbo.addLayout(hbo)
       
       self.l1 = QLabel("Name")
       self.le1 = QLineEdit()
       self.le1.setObjectName("name")
       vals1 = Valid().fullText()
       self.le1.setValidator(vals1)
       self.le1.setPlaceholderText("Lowercase max 25 letters")
        
       self.l2 = QLabel("Abbrv")
       self.le2 = QLineEdit()
       self.le2.setObjectName("abbrv")
       vals2 = Valid().limitText()
       self.le2.setValidator(vals2)
       self.le2.setPlaceholderText("Lowercase max 5 letters")
       
       FormLayout = QFormLayout()
       FormLayout.addRow(self.l1, self.le1)
       FormLayout.addRow(self.l2, self.le2)
       
       Hlayout1 = QHBoxLayout()
       Hlayout1.addStretch()
       Hlayout1.addWidget(self.pb6)
       Hlayout1.addWidget(self.pb5)
       Hlayout1.addWidget(self.pb4)
       Hlayout1.addWidget(self.pb)
       
       Vlayout1 = QVBoxLayout()
       Vlayout1.addLayout(FormLayout)
       Vlayout1.addLayout(Hlayout1)
       
       self.groupBox1.setLayout(vbo)
       self.groupBox2.setLayout(Vlayout1)
       self.groupBox2.hide()
       
       self.connect(self.pb, SIGNAL("clicked()"), lambda: self.button_add()) #add
       self.connect(self.pb1, SIGNAL("clicked()"), lambda: self.button_close()) #close
       self.connect(self.pb2, SIGNAL("clicked()"), lambda: self.button_edit()) #edit
       self.connect(self.pb3, SIGNAL("clicked()"), lambda: self.button_delete()) #delete
       self.connect(self.pb4, SIGNAL("clicked()"), lambda: self.button_save()) #save
       self.connect(self.pb5, SIGNAL("clicked()"), lambda: self.button_reset()) #reset
       
       self.pb4.hide()
       self.pb7.hide()
       
       grid = QGridLayout()
       grid.addWidget(self.groupBox1, 0, 0)
       grid.addWidget(self.groupBox2, 1, 0)
        
       self.setLayout(grid)
       self.setStyleSheet(stylesheet)
       self.setWindowIcon(QIcon(self.titleIcon))
       self.setWindowTitle(self.pagetitle)
         
    def makeTree(self):
       self.tree.clear()
       arr = Valid().pullData('datas', '', {'pubID': self.titleID})
       self.hold_data = {}
       self.hold_mdata = {}
       self.hold_data_add = {}
       self.hold_data_add_item = {}
      
       if self.titleSub and self.titleSub > 0:
           if arr and len(arr) > 0:
               for val in arr:
                 ch = Valid().pullData('datas', '', {'subID':val['id']})
                 child = QTreeWidgetItem(self.tree)
                 child.setFlags(child.flags() | Qt.ItemIsUserCheckable)
                 child.setText(0, str(val['name']).upper())
                 child.setText(1, str(val['abbrv']).upper())
                 self.hold_data[val['id']] = child
                 self.hold_mdata[val['id']] = child
                 if (val['active'] == 0):
                     child.setCheckState(0, Qt.Checked)
                 else:
                     child.setCheckState(0, Qt.Unchecked)
              
                  
                 for va in ch:
                     child1 = QTreeWidgetItem(child)
                     child1.setFlags(child1.flags() | Qt.ItemIsUserCheckable)
                     child1.setText(0, str(va['name']).upper())
                     child1.setText(1, str(va['abbrv']).upper())
                     self.hold_data[va['id']] = child1
                     if (va['active'] == 0):
                         child1.setCheckState(0, Qt.Checked)
                     else:
                         child1.setCheckState(0, Qt.Unchecked)
                         
                 child1 = QTreeWidgetItem(child)
                 child1.setFlags(child1.flags() | Qt.ItemIsUserCheckable)
                 child1.setText(0, 'Add New Item')
                 self.hold_data_add_item[val['id']] = child1
       else:
           if arr and len(arr) > 0:
               for val in arr:
                 child = QTreeWidgetItem(self.tree)
                 child.setFlags(child.flags() | Qt.ItemIsUserCheckable)
                 child.setText(0, str(val['name']).upper())
                 child.setText(1, str(val['abbrv']).upper())
                 self.hold_data[val['id']] = child
                 if (val['active'] == 0):
                     child.setCheckState(0, Qt.Checked)
                 else:
                     child.setCheckState(0, Qt.Unchecked)
                 
       child = QTreeWidgetItem(self.tree)
       child.setFlags(child.flags() | Qt.ItemIsUserCheckable)
       child.setText(0, 'Add New')
       self.hold_data_add['addnew'] = child
    
    def getChecked(self, a):
        g = Db()
        for i in self.hold_data:
            if self.hold_data[i].checkState(0) == Qt.Checked:
                g.update('datas', {'active':0}, {'id':i})
            else:
                g.update('datas', {'active':1}, {'id':i}) 
        
        if self.titleID == 1:
        #if class was changed only reload class menu on main window
            self.par.menuStudent()
            self.par.dropdownStudent()
                
    def getSelected(self):
        r = None
        k = None
        for i in self.hold_data:
            if self.hold_data[i].isSelected():
                    r = i
        for j in self.hold_mdata:
            if self.hold_mdata[j].isSelected():
                    k = j
                    
        if r and r > 0:
             if r == k:
                 self.sessionMain = r
             else:
                 self.sessionMain = 0
             self.groupBox2.show()
             return r
        else:
            self.groupBox2.hide()
        
    
    def getSelection(self):
        
        self.le1.clear()
        self.le2.clear()
        
        if self.hold_data_add['addnew'].isSelected():
            self.sessionMain = 0;
            self.groupBox2.setTitle('Add New')
            self.groupBox2.show()
        else:
            r = None
            for i in self.hold_data_add_item:
                if self.hold_data_add_item[i].isSelected():
                    r = i
            if r:
                self.sessionMain = r;
                g = Db()
                v = g.selectn('datas', '', 1, {'id':r})
                vname = str(v['name']).upper()
                self.groupBox2.setTitle('ADD '+str(vname)+' ITEM')
                self.groupBox2.show()
            else:
                self.groupBox2.setTitle('Add')
                self.groupBox2.hide()
        
                
    def setActive(self):
        g = Db()
        for i in self.hold_data:
            if self.hold_data[i].checkState(0) == Qt.Checked:
               g.update('datas', {'active':0}, {'id':i})
            else:
               g.update('datas', {'active':1}, {'id':i})
                  
    def button_add(self):
        s1 = self.le1.text()
        s2 = self.le2.text()
        g = Db()
        try:
            if(len(s1) > 0) and (len(s2) > 0):
                if self.sessionMain == 0:
                    y = { 'name':s1.lower(), 'abbrv':s2.lower(), 'pubID':self.titleID, 'active':0}
                else:
                    y = { 'name':s1.lower(), 'abbrv':s2.lower(),'subID':self.sessionMain,  'pubID':self.titleIDx, 'active':0}
                g.insert('datas', y)
             
                self.makeTree()
                self.button_reset()
                if self.titleID == 1:
                    #if class was changed only relod class menu on main window
                    self.par.menuStudent()
                    self.par.dropdownStudent()
            else:
                pass
        except:
            pass
        
    def button_save(self):
        row = self.editrow
        
        s1 = self.le1.text()
        s2 = self.le2.text()
        g = Db()
        try:
            if(len(s1) > 0) and (len(s2) > 0) and row and  row > 0:
                y = { 'name':s1.lower(), 'abbrv':s2.lower(), 'active':0}
                z = {'id':row}
                g.update('datas', y, z)
                self.makeTree()
                self.button_reset()
                if self.titleID == 1:
                    #if class was changed only relod class menu on main window
                    self.par.menuStudent()
                    self.par.dropdownStudent()
            else:
                pass
        except:
            pass
        
    def button_delete(self):
        row = self.getSelected()
        g = Db()
        try:
            if row and  row > 0:
                y = {'abbrv':'', 'active':2}
                z = {'id':row}
                g.update('datas', y, z)
                self.makeTree()
            else:
                pass
        except:
            pass
        
    def button_reset(self):
        self.le1.clear()
        self.le2.clear()
        self.groupBox2.setTitle('Add')
        self.groupBox2.hide()
        self.pb.show()
        self.pb4.hide()
        self.sessionMain = 0
        
    def button_edit(self):
        row = self.getSelected()
        self.sessionMain = 0
        if row:
            self.groupBox2.setTitle('Edit')
            self.editrow = row
            g = Db()
            data = g.selectn('datas', '', 1, {'id':row})
            if self.titleID == data['pubID']:
                self.sessionMain = 1
            else:
                self.sessionMain = 0
            
            try:
                self.le1.setText(data['name'])
            except:
                self.le1.setText('')
            try:
                self.le2.setText(data['abbrv'])
            except:
                self.le2.setText('')
            self.pb.hide()
            self.pb4.show()
        
    def button_close(self):
        self.close()
                 
class SessionsManager(QDialog):
    def __init__(self, n,  parent=None):
       super(SessionsManager, self).__init__(parent)
       self.par = n
       #main
       title = Settingz().positions(30)
       self.titleID = title['id']
       self.titlePage = title['page']
       self.titleName = title['name']
       self.titleSub = title['subID']
       self.titleIcon = title['icon']
       self.pagetitle = self.titlePage
       #stylesheet
       stylesheet = Valid().background() + Valid().font()
       treeStyleSheet =  Valid().treez()
       
       self.groupBox1 = QGroupBox(self.titleName)
       self.groupBox2 = QGroupBox('Add')
    
       #items
       self.tree = QTreeWidget()
       self.tree.setHeaderLabel("Choose "+self.titleName)
        #tree.setItemDelegate(Delegate())
       self.tree.setItemDelegate(Delegates())
       self.tree.headerItem().setText(0, 'Name')
       self.tree.setStyleSheet(treeStyleSheet)
       self.makeTree()
       self.tree.setMinimumHeight(250)
       self.tree.clicked.connect(lambda:self.getSelection())
       self.tree.itemClicked.connect(lambda state:self.getChecked(state))
       #buttons
       #add
       nImg = Buttons().addButton()
       self.pb = QPushButton()
       self.pb.setFlat(True)
       self.pb.setIcon(QIcon(nImg))
       self.pb.setMaximumHeight(30)
       self.pb.setMaximumWidth(30)
        
       nImg1 = Buttons().closeButton()
       self.pb1 = QPushButton()
       self.pb1.setFlat(True)
       self.pb1.setIcon(QIcon(nImg1))
       self.pb1.setMaximumHeight(30)
       self.pb1.setMaximumWidth(30)
       
       nImg2 = Buttons().editButton()
       self.pb2 = QPushButton()
       self.pb2.setFlat(True)
       self.pb2.setIcon(QIcon(nImg2))
       self.pb2.setMaximumHeight(30)
       self.pb2.setMaximumWidth(30)
       
       nImg3 = Buttons().deleteButton()
       self.pb3 = QPushButton()
       self.pb3.setFlat(True)
       self.pb3.setIcon(QIcon(nImg3))
       self.pb3.setMaximumHeight(30)
       self.pb3.setMaximumWidth(30)
       
       nImg4 = Buttons().saveButton()
       self.pb4 = QPushButton()
       self.pb4.setFlat(True)
       self.pb4.setIcon(QIcon(nImg4))
       self.pb4.setMaximumHeight(30)
       self.pb4.setMaximumWidth(30)
       
       nImg5 = Buttons().resetButton()
       self.pb5 = QPushButton()
       self.pb5.setFlat(True)
       self.pb5.setIcon(QIcon(nImg5))
       self.pb5.setMaximumHeight(30)
       self.pb5.setMaximumWidth(30)
       
       nImg6 = Buttons().closeButton()
       self.pb6 = QPushButton()
       self.pb6.setFlat(True)
       self.pb6.setIcon(QIcon(nImg6))
       self.pb6.setMaximumHeight(30)
       self.pb6.setMaximumWidth(30)
       
       nImg7 = Buttons().addButton()
       self.pb7 = QPushButton()
       self.pb7.setFlat(True)
       self.pb7.setIcon(QIcon(nImg7))
       self.pb7.setMaximumHeight(30)
       self.pb7.setMaximumWidth(30)
        
       hbo = QHBoxLayout()
       hbo.addStretch()
       hbo.addWidget(self.pb1)
       hbo.addWidget(self.pb3)
       hbo.addWidget(self.pb2)
       hbo.addWidget(self.pb7)
       
       vbo = QVBoxLayout()
       vbo.addWidget(self.tree)
       vbo.addLayout(hbo)
       
       self.l1 = QLabel("Name")
       self.le1 = QLineEdit()
       self.le1.setObjectName("name")
       vals1 = Valid().fullNum()
       self.le1.setValidator(vals1)
       self.le1.setPlaceholderText("Lowercase max 25 letters")
        
       
       self.fromLbl = QLabel("Starts")
       self.toLbl = QLabel("Ends")
       self.fromData = QDateEdit()
       self.toData = QDateEdit()
       currentDate = QDate()
       self.fromData.setDate(currentDate.currentDate())
       self.fromData.setCalendarPopup(True)
       self.toData.setDate(currentDate.currentDate())
       self.toData.setCalendarPopup(True)
       
       FormLayout = QFormLayout()
       FormLayout.addRow(self.l1, self.le1)
       FormLayout.addRow(self.fromLbl, self.fromData)
       FormLayout.addRow(self.toLbl, self.toData)
       
       Hlayout1 = QHBoxLayout()
       Hlayout1.addStretch()
       Hlayout1.addWidget(self.pb6)
       Hlayout1.addWidget(self.pb5)
       Hlayout1.addWidget(self.pb4)
       Hlayout1.addWidget(self.pb)
       
       Vlayout1 = QVBoxLayout()
       Vlayout1.addLayout(FormLayout)
       Vlayout1.addLayout(Hlayout1)
       
       self.groupBox1.setLayout(vbo)
       self.groupBox2.setLayout(Vlayout1)
       self.groupBox2.hide()
       
       self.connect(self.pb, SIGNAL("clicked()"), lambda: self.button_add()) #add
       self.connect(self.pb1, SIGNAL("clicked()"), lambda: self.button_close()) #close
       self.connect(self.pb2, SIGNAL("clicked()"), lambda: self.button_edit()) #edit
       self.connect(self.pb3, SIGNAL("clicked()"), lambda: self.button_delete()) #delete
       self.connect(self.pb4, SIGNAL("clicked()"), lambda: self.button_save()) #save
       self.connect(self.pb5, SIGNAL("clicked()"), lambda: self.button_reset()) #reset
       
       self.pb4.hide()
       self.pb7.hide()
       
       grid = QGridLayout()
       grid.addWidget(self.groupBox1, 0, 0)
       grid.addWidget(self.groupBox2, 1, 0)
        
       self.setLayout(grid)
       self.setStyleSheet(stylesheet)
       self.setWindowIcon(QIcon(self.titleIcon))
       self.setWindowTitle(self.pagetitle)
         
    def makeTree(self):
       self.tree.clear()
       arr = Db().selectn('session','', 5)
       self.hold_data = {}
       self.hold_mdata = {}
       self.hold_data_add = {}
       self.hold_data_add_item = {}
       current = time.time()
      
       if self.titleSub and self.titleSub > 0:
           if arr and len(arr) > 0:
               for val in arr:
                 ch = Valid().pullData('terms', '', {'sessionID':val['id']})
                 child = QTreeWidgetItem(self.tree)
                 child.setIcon(0, QIcon('icons.cfolder.png'))
                 try:
                     ts = int(float(val['start_date']))
                 except:
                     ts = int(current)
                 ts = datetime.utcfromtimestamp(ts).strftime('%d-%m-%Y')

                 try:
                     ts1 = int(float(val['end_date']))
                 except:
                     ts1 = int(current)
                 ts1 = datetime.utcfromtimestamp(ts1).strftime('%d-%m-%Y')

                 child.setText(0, str(val['name']).upper()+" - "+ts+" "+ts1)
                 self.hold_mdata[val['id']] = child
                 
              
                  
                 for va in ch:
                     child1 = QTreeWidgetItem(child)
                     child1.setFlags(child1.flags() | Qt.ItemIsUserCheckable)
                     
                     try:
                         ts2 = int(float(va['start_date']))
                     except:
                         ts2 = int(current)
                     ts2 = datetime.utcfromtimestamp(ts2).strftime('%d-%m-%Y')
                     try:
                         ts3 = int(float(va['end_date']))
                     except:
                         ts3 = int(current)
                     ts3 = datetime.utcfromtimestamp(ts3).strftime('%d-%m-%Y')
            
                     child1.setText(0, str(va['name']).upper()+" "+ts2+" "+ts3)
                     self.hold_data[va['id']] = child1
                     if (va['active'] == 1):
                         child1.setCheckState(0, Qt.Checked)
                     else:
                         child1.setCheckState(0, Qt.Unchecked)
                         
                 child1 = QTreeWidgetItem(child)
                 child1.setFlags(child1.flags() | Qt.ItemIsUserCheckable)
                 child1.setText(0, 'Add New Term')
                 self.hold_data_add_item[val['id']] = child1
       else:
           if arr and len(arr) > 0:
               for val in arr:
                 child = QTreeWidgetItem(self.tree)
                 child.setFlags(child.flags() | Qt.ItemIsUserCheckable)
                 child.setText(0, str(val['name']).upper())
                 child.setText(1, str(val['abbrv']).upper())
                 self.hold_data[val['id']] = child
                 if (val['active'] == 0):
                     child.setCheckState(0, Qt.Checked)
                 else:
                     child.setCheckState(0, Qt.Unchecked)
                 
       child = QTreeWidgetItem(self.tree)
       child.setFlags(child.flags() | Qt.ItemIsUserCheckable)
       child.setText(0, 'Add New Session')
       self.hold_data_add['addnew'] = child
    
    def getChecked(self, a):
        arr_hold = []
        g = Db()
        for i in self.hold_data:
            if self.hold_data[i].checkState(0) == Qt.Checked:
                arr_hold.append(i)
                self.hold_data[i].setCheckState(0, Qt.Checked)
                g.update('terms', {'active':0}, {'active':1})
                g.update('terms', {'active':1}, {'id':i})
                tt = g.selectn('terms', '', 1, {'id':i})
                g.update('session', {'active':0}, {'active':1})
                g.update('session', {'active':1}, {'id':tt['sessionID']})
                g.selectn('session', '', 1, {'id':tt['sessionID']})
            else:
               self.hold_data[i].setCheckState(0, Qt.Unchecked) 
                
        self.reloadTerm()
    
     
    def reloadTerm(self):
        session = self.par.activeTerm()
        activeTerm = str(session[1])+' SESSION '+str(session[3])+' TERM'
        self.par.majorSession = session[2];
        self.par.lbl.setText(activeTerm)
                
    def getSelected(self):
        r = False
        self.sessionMain = False
        for i in self.hold_mdata:
            if self.hold_mdata[i].isSelected():
               r = i
               
        if r and r > 0:
            self.groupBox2.show()
            self.sessionMain = True
            return r
        else:
            for i in self.hold_data:
                if self.hold_data[i].isSelected():
                    r = i
            if r and r > 0:
                self.sessionMain = False
                self.groupBox2.show()
                return r
            else:
                self.groupBox2.hide()
            
    def getSession(self):
        self.sessionID = None
        for i in self.hold_data_session:
            if self.hold_data_session[i].isSelected():
               r = i
        if r and r > 0:
          self.sessionID = r   
    
    def getSelection(self):
        self.le1.clear()
        currentDate = QDate()
        self.fromData.setDate(currentDate.currentDate())
        self.toData.setDate(currentDate.currentDate())
        self.sessionMain = False
        
        if self.hold_data_add['addnew'].isSelected():
            self.groupBox2.setTitle('Add New')
            self.groupBox2.show()
            self.sessionMain = True
            self.sessionID = False
        else:
            self.sessionMain = False
            r = None
            for i in self.hold_data_add_item:
                if self.hold_data_add_item[i].isSelected():
                    r = i
            if r:
                g = Db()
                v = g.selectn('session', '', 1, {'id':r})
                vname = str(v['name']).upper()+' Session'
                self.groupBox2.setTitle('ADD '+str(vname)+' Term')
                self.sessionID = r
                self.groupBox2.show()
            else:
                self.groupBox2.setTitle('Add')
                self.sessionID = False
                self.groupBox2.hide()
        
                
    def setActive(self):
        g = Db()
        for i in self.hold_data:
            if self.hold_data[i].checkState(0) == Qt.Checked:
               g.update('datas', {'active':0}, {'id':i})
            else:
               g.update('datas', {'active':1}, {'id':i})
                  
    def button_add(self):
        s1 = self.le1.text()
        _datef = self.fromData.date().toPyDate()
        _datef = time.mktime(_datef.timetuple())
        _datee = self.toData.date().toPyDate()
        _datee = time.mktime(_datee.timetuple())
        g = Db()
        
        if self.sessionID and self.sessionID > 0:
            try:
                if(len(s1) > 0):
                    y = { 'name':s1.lower(), 'start_date':_datef,'sessionID':self.sessionID,  'end_date':_datee, 'active':0}
                    z = g.insert('terms', y)
                    if z and z > 0:
                        g.createClass(z)
                        g.createSubject(z)
                        g.createFee(z)
                        g.createPay(z)
                        g.createResult(z)  
                        g.createAffective(z)
                        g.createPsychomoto(z)
                    self.makeTree()
                    self.button_reset()
                    self.par.menuSession()
                    self.par.dropdownSession()
                else:
                    pass
            except:
                pass
        else:
            try:
                if(len(s1) > 0):
                    y = { 'name':s1.lower(), 'start_date':_datef, 'end_date':_datee, 'active':0}
                    z = g.insert('session', y)
                    if z and z > 0:
                        g.createExpenses(z)
                        g.createStores(z)
                        g.createAwards(z)
                        g.createConducts(z)
                        g.createMails(z)
                        g.createMedicals(z)
                    self.makeTree()
                    self.button_reset()
                    self.par.menuSession()
                    self.par.dropdownSession()
                else:
                    pass
            except:
                pass
        
    def button_save(self):
        row = self.editrow
        s1 = self.le1.text()
        _datef = self.fromData.date().toPyDate()
        _datef = time.mktime(_datef.timetuple())
        _datee = self.toData.date().toPyDate()
        _datee = time.mktime(_datee.timetuple())
        
        g = Db()
        
        if(len(s1) > 0)  and row and  row > 0:
            if self.sessionID and self.sessionID > 0:
                try:
                    if(len(s1) > 0):
                        y = { 'name':s1.lower(), 'start_date':_datef,'sessionID':self.sessionID,  'end_date':_datee, 'active':0}
                        k = {'id':row}
                        g.update('terms', y, k)
                        z = row
                        if z and z > 0:
                            g.createClass(z)
                            g.createSubject(z)
                            g.createFee(z)
                            g.createPay(z)
                            g.createResult(z)  
                            g.createAffective(z)
                            g.createPsychomoto(z)
                        self.makeTree()
                        self.button_reset()
                        self.par.menuSession()
                        self.par.dropdownSession()
                    else:
                        pass
                except:
                    pass
            else:
                try:
                    if(len(s1) > 0):
                        y = { 'name':s1.lower(), 'start_date':_datef, 'end_date':_datee, 'active':0}
                        k = {'id':row}
                        g.update('session', y, k)
                        z = row
                        if z and z > 0:
                            g.createExpenses(z)
                            g.createStores(z)
                            g.createAwards(z)
                            g.createConducts(z)
                            g.createMails(z)
                            g.createMedicals(z)
                        self.makeTree()
                        self.button_reset()
                        self.par.menuSession()
                        self.par.dropdownSession()
                    else:
                        pass
                except:
                    pass
        
    def button_delete(self):
        row = self.getSelected()
        g = Db()
        try:
            if row and  row > 0:
                y = {'abbrv':'', 'active':2}
                z = {'id':row}
                g.update('datas', y, z)
                self.makeTree()
            else:
                pass
        except:
            pass
        
    def button_reset(self):
        self.le1.clear()
        currentDate = QDate()
        self.fromData.setDate(currentDate.currentDate())
        self.toData.setDate(currentDate.currentDate())
        self.groupBox2.setTitle('Add')
        self.groupBox2.hide()
        self.pb.show()
        self.pb4.hide()
        
    def button_edit(self):
        row = self.getSelected()
        currentDate = QDate()
        if row:
            self.editrow = row
            g = Db()
            if self.sessionMain:
                data = g.selectn('session', '', 1, {'id':row})
                data_name = str(data['name'])
                self.groupBox2.setTitle('Edit')
                self.sessionID = False
            else:
                data = g.selectn('terms', '', 1, {'id':row})
                data_sess = g.selectn('session', '', 1, {'id':data['sessionID']})
                data_name = str(data['name'])
                self.sessionID = data['sessionID']
                self.groupBox2.setTitle('Edit '+str(data_sess['name']))
            try:
                self.le1.setText(data_name)
            except:
                self.le1.setText('')
            try:
                self.fromData.setDate(data['start_date'])
            except:
                self.fromData.setDate(currentDate.currentDate())
            try:
                self.toData.setDate(data['end_date'])
            except:
                self.toData.setDate(currentDate.currentDate())
            self.pb.hide()
            self.pb4.show()
        
    def button_close(self):
        self.close()
        
        
class Delegates(QStyledItemDelegate):
    def paint(self, painter, option, index):
        if not index.parent().isValid():
            QStyledItemDelegate.paint(self, painter, option, index)
        else:
            widget = option.widget
            style = widget.style() if widget else QApplication.style()
            opt = QStyleOptionButton()
            opt.rect = option.rect
            opt.text = index.data()
            opt.state |= QStyle.State_On if index.data(Qt.CheckStateRole) else QStyle.State_Off
            style.drawControl(QStyle.CE_RadioButton, opt, painter, widget)

    def editorEvent(self, event, model, option, index):
        value = QStyledItemDelegate.editorEvent(self, event, model, option, index)
        if value:
            if event.type() == QEvent.MouseButtonRelease:
                if index.data(Qt.CheckStateRole) == Qt.Checked:
                    parent = index.parent()
                    for i in range(model.rowCount(parent)):
                        if i != index.row():
                            ix = parent.child(i, 0)
                            model.setData(ix, Qt.Unchecked, Qt.CheckStateRole)

        return value