
# -*- coding: utf-8 -*-
"""
Created on Sat Jul  7 15:54:19 2018

@author: CHARLES
"""
from PyQt4.QtCore import SIGNAL, Qt, QEvent
from PyQt4.QtGui import QFontDialog, QColorDialog, QTreeWidget, QTreeWidgetItem, QStyle, QStyleOptionButton, QStyledItemDelegate, QStandardItemModel,  QStandardItem, QWidget,QComboBox, QListView, QListWidget, QFrame, QDateEdit, QRadioButton, QCheckBox, QHBoxLayout, QGroupBox, QGridLayout, QDialog, QApplication, QPushButton, QLineEdit, QFormLayout, QLabel, QVBoxLayout
from connect import Db

class FeeDialog(QDialog):
    
    holdc = {}
    def __init__(self, term, parent=None):
        super(FeeDialog, self).__init__(parent)
        
        self.term = term
        self.sid = term
        terms = self.pullOnes('terms', self.term)
        session = self.pullOnes('session', terms['sessionID'])
        self.termname = str(session['name'])+' '+terms['name']+' Term Report'
        self.pagetitle = self.termname 
        ko = 0
        
        
        Form1 = QFormLayout()
        Form2 = QFormLayout()
        
        #title
        self.title = QLabel("Set Fees")
        self.titleData = QComboBox()
        self.titleData.setObjectName("name")
        #self.titleData.setPlaceHolderText("e.g. 2019 FIRST TERM RESULT")
        
        tree = QTreeWidget()
        tree.setItemDelegate(Delegate())
        tree.setHeaderLabel("Which grading system will you be using?")
        
        tree1 = QTreeWidget()
        tree1.setHeaderLabel("Choose Assessments and Classes")
        
        tree2 = QTreeWidget()
        tree2.setHeaderLabel("Report Card Settings")
        
        self.ass_arr = {}
        parent = QTreeWidgetItem(tree1)
        parent.setText(0, "Select Assessments")
        parent.setFlags(parent.flags() | Qt.ItemIsTristate | Qt.ItemIsUserCheckable)
        arr = self.pullCas()
        if arr and len(arr) > 0:
            for val in arr:
                dt = self.pullOne(val['name'])
                child = QTreeWidgetItem(parent)
                child.setFlags(child.flags() | Qt.ItemIsUserCheckable)
                child.setText(0, str(dt['name']).upper())
                self.ass_arr[val['name']] = child
                if (val['active'] == 0):
                    child.setCheckState(0, Qt.Unchecked)
                else:
                    child.setCheckState(0, Qt.Unchecked)
                ko += 1
        
        self.cla_arr ={}
        parent1 = QTreeWidgetItem(tree1)
        parent1.setText(0, "Select Class")
        parent1.setFlags(parent1.flags() | Qt.ItemIsTristate | Qt.ItemIsUserCheckable)
        arr = self.pullClass()
        if arr and len(arr) > 0:
            for val in arr:
                child = QTreeWidgetItem(parent1)
                child.setFlags(child.flags() | Qt.ItemIsUserCheckable)
                child.setText(0, str(val['name']).upper())
                self.cla_arr[val['id']] = child
                if (val['active'] == 0):
                    child.setCheckState(0, Qt.Unchecked)
                else:
                    child.setCheckState(0, Qt.Unchecked)
                ko += 1

        self.gra_arr = {}
        parent2 = QTreeWidgetItem(tree)
        parent2.setText(0, "Select Grade")
        arr = self.pullGrade()
        if arr and len(arr) > 0:
            for val in arr:
                child = QTreeWidgetItem(parent2)
                child.setFlags(child.flags() | Qt.ItemIsUserCheckable)
                child.setText(0, str(val['name']).upper())
                self.gra_arr[val['id']] = child
                if (val['active'] == 0):
                    child.setCheckState(0, Qt.Unchecked)
                else:
                    child.setCheckState(0, Qt.Unchecked)
                ko += 1
                
        self.set_arr= {}
        parent3 = QTreeWidgetItem(tree2)
        parent3.setText(0, "Include ...")
        parent3.setFlags(parent3.flags() | Qt.ItemIsTristate | Qt.ItemIsUserCheckable)
        arr ={
                1:'School Number',
                2:'Class Position',
                3:'Class Unit Position',
                4:'Total (100%)',
                5:'Total',
                6:'Grading',
                7:'Subject Average',
                8:'Ranking',
                9:'Ranking and Student Population',
                10:'Student Passport',
                11:'School Logo',
                12:'School Address',
                13:'Students Address',
                14:'Attendance',
                15:'Fees Owed',
                16:'Test/Assesments'
            }
        if arr and len(arr) > 0:
            for val in arr:
                child = QTreeWidgetItem(parent3)
                child.setFlags(child.flags() | Qt.ItemIsUserCheckable)
                child.setText(0, str(arr[val]).upper())
                self.set_arr[val] = child
                child.setCheckState(0, Qt.Unchecked)
            
            child1 = QTreeWidgetItem(parent3)
            child1.setFlags(child1.flags() | Qt.ItemIsUserCheckable)
            child1.setText(0, 'AFFECTIVE DOMAIN REPORT')
            self.set_arr['aff'] = child1
            child1.setCheckState(0, Qt.Unchecked)
            
            child2 = QTreeWidgetItem(child1)
            child2.setFlags(child2.flags() | Qt.ItemIsTristate | Qt.ItemIsUserCheckable)
            child2.setText(0, 'TABLE')
            self.set_arr['afftable'] = child2
            child2.setCheckState(0, Qt.Unchecked)
            
            child3 = QTreeWidgetItem(child1)
            child3.setFlags(child3.flags() | Qt.ItemIsUserCheckable)
            child3.setText(0, 'GRAPH')
            self.set_arr['affgraph'] = child3
            child3.setCheckState(0, Qt.Unchecked)
            
            child4 = QTreeWidgetItem(parent3)
            child4.setFlags(child4.flags() | Qt.ItemIsTristate | Qt.ItemIsUserCheckable)
            child4.setText(0, 'PYSCHOMOTOR DOMAIN REPORT')
            self.set_arr['psy'] = child4
            child4.setCheckState(0, Qt.Unchecked)
            
            child5 = QTreeWidgetItem(child4)
            child5.setFlags(child5.flags() | Qt.ItemIsUserCheckable)
            child5.setText(0, 'TABLE')
            self.set_arr['psytable'] = child5
            child5.setCheckState(0, Qt.Unchecked)
            
            child6 = QTreeWidgetItem(child4)
            child6.setFlags(child6.flags() | Qt.ItemIsUserCheckable)
            child6.setText(0, 'GRAPH')
            self.set_arr['psygraph'] = child6
            child6.setCheckState(0, Qt.Unchecked)

        tree.expandAll()
        tree1.expandAll()
        tree2.expandAll()
        #tree.show()
     
        self.l5 = QLabel("Theme Color")
        self.pbc = QPushButton()
        self.pbc.setObjectName("Pickcolor")
        self.pbc.setText("Click to change")
        
        self.le5 = QLineEdit()
        self.le5.setObjectName("Showcolor")
        self.le5.setText("#000000")
        self.pbc.setStyleSheet("background-color: black; color: white")
        self.connect(self.pbc, SIGNAL("clicked()"), lambda: self.color_picker())
        
        self.l6 = QLabel("Pick Theme Font")
        self.pbf = QPushButton()
        self.pbf.setObjectName("Pickfont")
        self.pbf.setText("Click to Change")
        
        self.le6 = QLineEdit()
        self.le6.setObjectName("Showcolor")
        self.le6.setText("#000000")
        self.pbf.setStyleSheet("background-color: black; color: white")
        self.connect(self.pbf, SIGNAL("clicked()"), lambda: self.font_picker())
        
        self.lv_box = QHBoxLayout()
        self.lv_box.addWidget(self.pbc)
        self.lv_box.addWidget(self.le5)
        
        self.lv_box1 = QHBoxLayout()
        self.lv_box1.addWidget(self.pbf)
        self.lv_box1.addWidget(self.le6)
        
        Form1.addRow(self.title, self.titleData)
        Form2.addRow(self.l5, self.lv_box)
        Form2.addRow(self.l6, self.lv_box1)
        
        Gbo = QGridLayout()
        Gbo.addLayout(Form1, 0, 0, 1, 2)
        Gbo.addWidget(tree, 1, 0)
        Gbo.addWidget(tree1, 1, 1)
        Gbo.addWidget(tree2, 2, 0)
        Gbo.addLayout(Form2, 2, 1)
        
        groupBox1 = QGroupBox('Academic Report Setup')
        groupBox1.setLayout(Gbo)
        
        self.pb = QPushButton()
        self.pb.setObjectName("Add")
        self.pb.setText("Save")
        
        
        self.pb1 = QPushButton()
        self.pb1.setObjectName("Cancel")
        self.pb1.setText("Cancel")
        
        self.pb2 = QPushButton()
        self.pb2.setObjectName("Save")
        self.pb2.setText("Save and Keep Template")
        
        self.lTemplate = QLineEdit() 
        self.lTemplate.setPlaceholderText('Template Name')
        
        self.rTemplate = QLabel() 
        self.rTemplate.setText('')
        
        hbo = QHBoxLayout()
        hbo.addWidget(self.pb1)
        hbo.addStretch()
        hbo.addWidget(self.lTemplate)
        hbo.addWidget(self.pb2)
        hbo.addWidget(self.rTemplate)
        hbo.addStretch()
        hbo.addWidget(self.pb)
        
        groupBox2 = QGroupBox('')
        groupBox2.setLayout(hbo)
            
        grid = QGridLayout()
        grid.addWidget(groupBox1, 0, 0)
        grid.addWidget(groupBox2, 1, 0)
        
        self.setLayout(grid)
        self.connect(self.pb, SIGNAL("clicked()"), lambda: self.button_click(self))
        self.connect(self.pb2, SIGNAL("clicked()"), lambda: self.button_template(self))
        self.connect(self.pb1, SIGNAL("clicked()"), lambda: self.button_close(self))
       
        self.setWindowTitle(self.pagetitle)

        
    def color_picker(self):
        self.cp = QColorDialog.getColor()
        self.le5.setText(self.cp.name())
        self.pbc.setStyleSheet("background-color:"+self.cp.name() +"")
        return self.cp.name()
    
    def font_picker(self):
        item, ok = QFontDialog.getFont()
        if ok is True:
            self.le6.setText(item.toString())
        else:
            self.le6.setText('teal')
        self.pbf.setStyleSheet("font-family:"+self.cp.name() +"")
    
    def chkFunc(self, a, b):
        # shost is a QString object
        self.a = a
        self.b = b
        g = Db()
        if b.isChecked() == True:
            y = { 'active':0}
        else:
            y = { 'active':1}
         
        z = {'id': self.a}
        j = g.update('datas', y, z)
       
        return j 
        
    
    def pullClass(self):
        cn = Db()
        arr = cn.selectn('datas', '' , '', {'pubID': 1})
        return arr
    
    def pullGrade(self):
        cn = Db()
        arr = cn.selectn('datas', '' , '', {'pubID': 5})
        return arr
    
    def pullOne(self, b):
        cn = Db()
        arr = cn.selectn('datas', '' , 1, {'id': b})
        return arr
    
    def pullOnes(self,a, b):
        cn = Db()
        arr = cn.selectn(a, '' , 1, {'id': b})
        return arr
    
    def pullCas(self):
        cn = Db()
        ca = "ca"
        arr = cn.selectn('datas', '' , '', {"subID": self.sid, "pubID": ca})
        return arr
    
    def pullReports(self):
        cn = Db()
        ca = "ca"
        arr = cn.selectn('datas', '' , '', {"subID": self.sid, "pubID": ca})
        return arr
    
    def button_close(self, b):
        from dialogtermca import TermCaDialog
        self.close()
        post = TermCaDialog(self.term, self.termname )
        post.show()
        
    def button_template(self, b):
        template  = self.lTemplate.text()
        template =template.lower()
        if(len(template) >  0):
            g = Db()
            Ch =  g.selectn('datas', '', 1, {'abbrv':template, 'pubID': 'temp'})
            if Ch and Ch['id'] > 0:
                self.rTemplate.setText('Failed: Name already exist.')
            else:
                set_arr = []
                ass_arr = []
                gra_arr = []
                cla_arr = []
                
                for i in self.set_arr:
                    if self.set_arr[i].checkState(0) == Qt.Checked:
                        set_arr.append(i)
                
                for i in self.ass_arr:
                    if self.ass_arr[i].checkState(0) == Qt.Checked:
                        ass_arr.append(i) 
                        
                for i in self.gra_arr:
                    if self.gra_arr[i].checkState(0) == Qt.Checked:
                        gra_arr.append(i)
                        
                for i in self.cla_arr:
                    if self.cla_arr[i].checkState(0) == Qt.Checked:
                        cla_arr.append(i)
                        
                title = self.titleData.text()
                themeColor = self.le5.text()
                themeFont = self.le6.text()
                cla_store = self.cla_arr
                cla_store = ','.join(str(x) for x in cla_store)
                
                set_arr = '::'.join(str(x) for x in set_arr)
                gra_arr = '::'.join(str(x) for x in gra_arr)
                ass_arr = '::'.join(str(x) for x in ass_arr)
                
                
                save1 = title.upper()+':::'+ themeColor+':::'+ themeFont+':::'+ass_arr+':::'+ gra_arr+':::'+set_arr 
    
            
            
            try:
                if(len(title) > 0):
                    y = { 'name':cla_store, 'subID':self.term, 'pubID':'temp', 'abbrv':template, 'description': save1, 'active':0}
                    h = g.insert('datas', y)
                    self.button_click()
                else:
                    pass
            except:
                pass
        else:
            self.rTemplate.setText('Please give the template a name')

            
         
    def button_click(self, b):
        
        set_arr = []
        ass_arr = []
        gra_arr = []
        cla_arr = []
        
        for i in self.set_arr:
            if self.set_arr[i].checkState(0) == Qt.Checked:
                set_arr.append(i)
        
        for i in self.ass_arr:
            if self.ass_arr[i].checkState(0) == Qt.Checked:
                ass_arr.append(i) 
                
        for i in self.gra_arr:
            if self.gra_arr[i].checkState(0) == Qt.Checked:
                gra_arr.append(i)
                
        for i in self.cla_arr:
            if self.cla_arr[i].checkState(0) == Qt.Checked:
                cla_arr.append(i)
                
        title = self.titleData.text()
        themeColor = self.le5.text()
        themeFont = self.le6.text()
        cla_store = self.cla_arr
        cla_store = ','.join(str(x) for x in cla_store)
        
        set_arr = '::'.join(str(x) for x in set_arr)
        gra_arr = '::'.join(str(x) for x in gra_arr)
        ass_arr = '::'.join(str(x) for x in ass_arr)
        
        
        save1 = title.upper()+':::'+ themeColor+':::'+ themeFont+':::'+ass_arr+':::'+ gra_arr+':::'+set_arr 

        
        g = Db()
        try:
            if(len(title) > 0):
                y = { 'name':cla_store, 'subID':self.term, 'pubID':'rep', 'abbrv':'rep', 'description': save1, 'active':0}
                h = g.insert('datas', y)
            else:
                pass
        except:
            pass
        
        self.button_close(self)
        
        
       
                
        
class Delegate(QStyledItemDelegate):
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
            style.drawControl(QStyle.CE_CheckBox, opt, painter, widget)

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
    


class EditReportDialog(QDialog):
    
    holdc = {}
    def __init__(self, term, row,  parent=None):
        super(EditReportDialog, self).__init__(parent)
        
        self.term = term
        self.sid = term
        self.row = row
        terms = self.pullOnes('terms', self.term)
        datas = self.pullOnes('datas', self.row)
        session = self.pullOnes('session', terms['sessionID'])
        self.termname = str(session['name'])+' '+terms['name']+' Term Report'
        self.pagetitle = self.termname 
        ko = 0
        
        #prepare data
        d = datas['description']
        d = d.split(':::')
        _title = d[0]
        _theme = d[1]
        _font = d[2]
        _ass = d[3]
        _gra = d[4]
        _set = d[5]
        
        _ass_list =_ass.split('::') 
        _gra_list =_gra.split('::')
        _set_list =_set.split('::')
        
        _cla_list =_set.split('::')
        layout1 = QGridLayout()
        Form1 = QFormLayout()
        Form2 = QFormLayout()
        
        #title
        self.title = QLabel("Report Title")
        self.titleData = QLineEdit()
        self.titleData.setObjectName("name")
        self.titleData.setText(_title)
        
        tree = QTreeWidget()
        tree.setItemDelegate(Delegate())
        tree.setHeaderLabel("Which grading system will you be using?")
        
        tree1 = QTreeWidget()
        tree1.setHeaderLabel("Choose Assessments and classes")
        
        tree2 = QTreeWidget()
        tree2.setHeaderLabel("Report Card Settings")
        
        self.ass_arr = {}
        parent = QTreeWidgetItem(tree1)
        parent.setText(0, "Select Assessments")
        parent.setFlags(parent.flags() | Qt.ItemIsTristate | Qt.ItemIsUserCheckable)
        arr = self.pullCas()
        if arr and len(arr) > 0:
            for val in arr:
                dt = self.pullOne(val['name'])
                child = QTreeWidgetItem(parent)
                child.setFlags(child.flags() | Qt.ItemIsUserCheckable)
                child.setText(0, str(dt['name']).upper())
                self.ass_arr[val['id']] = child
                if str(val['id']) in _ass_list:
                    child.setCheckState(0, Qt.Checked)
                else:
                    child.setCheckState(0, Qt.Unchecked)
                ko += 1
        
        self.cla_arr ={}
        parent1 = QTreeWidgetItem(tree1)
        parent1.setText(0, "Select Class")
        parent1.setFlags(parent1.flags() | Qt.ItemIsTristate | Qt.ItemIsUserCheckable)
        arr = self.pullClass()
        if arr and len(arr) > 0:
            for val in arr:
                child = QTreeWidgetItem(parent1)
                child.setFlags(child.flags() | Qt.ItemIsUserCheckable)
                child.setText(0, str(val['name']).upper())
                self.cla_arr[val['id']] = child
                va = str(val['id'])
                if ( va in _cla_list):
                    child.setCheckState(0, Qt.Checked)
                else:
                    child.setCheckState(0, Qt.Unchecked)
                ko += 1

        self.gra_arr = {}
        parent2 = QTreeWidgetItem(tree)
        parent2.setText(0, "Select Grade")
        arr = self.pullGrade()
        if arr and len(arr) > 0:
            for val in arr:
                child = QTreeWidgetItem(parent2)
                child.setFlags(child.flags() | Qt.ItemIsUserCheckable)
                child.setText(0, str(val['name']).upper())
                self.gra_arr[val['id']] = child
                if str(val['id']) in _gra_list:
                    child.setCheckState(0, Qt.Checked)
                else:
                    child.setCheckState(0, Qt.Unchecked)
                ko += 1
                
        self.set_arr= {}
        parent3 = QTreeWidgetItem(tree2)
        parent3.setText(0, "Include ...")
        parent3.setFlags(parent3.flags() | Qt.ItemIsTristate | Qt.ItemIsUserCheckable)
        arr ={
                1:'School Number',
                2:'Class Position',
                3:'Class Unit Position',
                4:'Total (100%)',
                5:'Total',
                6:'Grading',
                7:'Subject Average',
                8:'Ranking',
                9:'Ranking and Student Population',
                10:'Student Passport',
                11:'School Logo',
                12:'School Address',
                13:'Students Address',
                14:'Attendance',
                15:'Fees Owed',
                16:'Test/Assesments'
            }
        if arr and len(arr) > 0:
            for val in arr:
                
                child = QTreeWidgetItem(parent3)
                child.setFlags(child.flags() | Qt.ItemIsUserCheckable)
                child.setText(0, str(arr[val]).upper())
                self.set_arr[val] = child
            
                if str(val) in _set_list:
                  
                    child.setCheckState(0, Qt.Checked)
                else:
                    child.setCheckState(0, Qt.Unchecked)
            
            child1 = QTreeWidgetItem(parent3)
            child1.setFlags(child1.flags() | Qt.ItemIsUserCheckable)
            child1.setText(0, 'AFFECTIVE DOMAIN REPORT')
            self.set_arr['aff'] = child1
            if 'aff' in _set_list:
                child1.setCheckState(0, Qt.Checked)
            else:
                child1.setCheckState(0, Qt.Unchecked)
            
            child2 = QTreeWidgetItem(child1)
            child2.setFlags(child2.flags() | Qt.ItemIsTristate | Qt.ItemIsUserCheckable)
            child2.setText(0, 'TABLE')
            self.set_arr['afftable'] = child2
            if 'afftable' in _set_list:
                child2.setCheckState(0, Qt.Checked)
            else:
                child2.setCheckState(0, Qt.Unchecked)
            
            child3 = QTreeWidgetItem(child1)
            child3.setFlags(child3.flags() | Qt.ItemIsUserCheckable)
            child3.setText(0, 'GRAPH')
            self.set_arr['affgraph'] = child3
            if 'affgraph' in _set_list:
                child3.setCheckState(0, Qt.Checked)
            else:
                child3.setCheckState(0, Qt.Unchecked)
            
            child4 = QTreeWidgetItem(parent3)
            child4.setFlags(child4.flags() | Qt.ItemIsTristate | Qt.ItemIsUserCheckable)
            child4.setText(0, 'PYSCHOMOTOR DOMAIN REPORT')
            self.set_arr['psy'] = child4
            if 'psy' in _set_list:
                child4.setCheckState(0, Qt.Checked)
            else:
                child4.setCheckState(0, Qt.Unchecked)
            
            child5 = QTreeWidgetItem(child4)
            child5.setFlags(child5.flags() | Qt.ItemIsUserCheckable)
            child5.setText(0, 'TABLE')
            self.set_arr['psytable'] = child5
            if 'psytable' in _set_list:
                child5.setCheckState(0, Qt.Checked)
            else:
                child5.setCheckState(0, Qt.Unchecked)
            
            child6 = QTreeWidgetItem(child4)
            child6.setFlags(child6.flags() | Qt.ItemIsUserCheckable)
            child6.setText(0, 'GRAPH')
            self.set_arr['psygraph'] = child6
            if 'psygraph' in _set_list:
                child6.setCheckState(0, Qt.Checked)
            else:
                child6.setCheckState(0, Qt.Unchecked)

        tree.expandAll()
        tree1.expandAll()
        tree2.expandAll()
        #tree.show()
     
        self.l5 = QLabel("Theme Color")
        self.pbc = QPushButton()
        self.pbc.setObjectName("Pickcolor")
        self.pbc.setText("Click to change")
        
        self.le5 = QLineEdit()
        self.le5.setObjectName("Showcolor")
        self.le5.setText(_theme)
        self.pbc.setStyleSheet("background-color: "+ _theme +"; color: white")
        self.connect(self.pbc, SIGNAL("clicked()"), lambda: self.color_picker())
        
        self.l6 = QLabel("Pick Theme Font")
        self.pbf = QPushButton()
        self.pbf.setObjectName("Pickfont")
        self.pbf.setText(_font)
        
        self.le6 = QLineEdit()
        self.le6.setObjectName("Showcolor")
        self.le6.setText("#000000")
        self.pbf.setStyleSheet("color: black")
        self.connect(self.pbf, SIGNAL("clicked()"), lambda: self.font_picker())
        
        self.lv_box = QHBoxLayout()
        self.lv_box.addWidget(self.pbc)
        self.lv_box.addWidget(self.le5)
        
        self.lv_box1 = QHBoxLayout()
        self.lv_box1.addWidget(self.pbf)
        self.lv_box1.addWidget(self.le6)
        
        Form1.addRow(self.title, self.titleData)
        Form2.addRow(self.l5, self.lv_box)
        Form2.addRow(self.l6, self.lv_box1)
        
        Gbo = QGridLayout()
        Gbo.addLayout(Form1, 0, 0, 1, 2)
        Gbo.addWidget(tree, 1, 0)
        Gbo.addWidget(tree1, 1, 1)
        Gbo.addWidget(tree2, 2, 0)
        Gbo.addLayout(Form2, 2, 1)
        
        groupBox1 = QGroupBox('Academic Report Setup')
        groupBox1.setLayout(Gbo)
        
        self.pb = QPushButton()
        self.pb.setObjectName("Add")
        self.pb.setText("Add Assessment")
        
        
        self.pb1 = QPushButton()
        self.pb1.setObjectName("Cancel")
        self.pb1.setText("Cancel")
        
        hbo = QHBoxLayout()
        hbo.addWidget(self.pb1)
        hbo.addStretch()
        hbo.addWidget(self.pb)
        
        groupBox2 = QGroupBox('')
        groupBox2.setLayout(hbo)
            
        grid = QGridLayout()
        grid.addWidget(groupBox1, 0, 0)
        grid.addWidget(groupBox2, 1, 0)
        
        self.setLayout(grid)
        self.connect(self.pb, SIGNAL("clicked()"), lambda: self.button_click(self))
        self.connect(self.pb1, SIGNAL("clicked()"), lambda: self.button_close(self))
       
        self.setWindowTitle(self.pagetitle)

        
    def color_picker(self):
        self.cp = QColorDialog.getColor()
        self.le5.setText(self.cp.name())
        self.pbc.setStyleSheet("background-color:"+self.cp.name() +"")
        return self.cp.name()
    
    def font_picker(self):
        item, ok = QFontDialog.getFont()
        if ok is True:
            self.le6.setText(item.toString())
        else:
            self.le6.setText('teal')
        self.pbf.setStyleSheet("font-family:"+self.cp.name() +"")
    
    def chkFunc(self, a, b):
        # shost is a QString object
        self.a = a
        self.b = b
        g = Db()
        if b.isChecked() == True:
            y = { 'active':0}
        else:
            y = { 'active':1}
         
        z = {'id': self.a}
        j = g.update('datas', y, z)
       
        return j 
        
    
    def pullClass(self):
        cn = Db()
        arr = cn.selectn('datas', '' , '', {'pubID': 1})
        return arr
    
    def pullGrade(self):
        cn = Db()
        arr = cn.selectn('datas', '' , '', {'pubID': 5})
        return arr
    
    def pullOne(self, b):
        cn = Db()
        arr = cn.selectn('datas', '' , 1, {'id': b})
        return arr
    
    def pullOnes(self,a, b):
        cn = Db()
        arr = cn.selectn(a, '' , 1, {'id': b})
        return arr
    
    def pullCas(self):
        cn = Db()
        ca = "ca"
        arr = cn.selectn('datas', '' , '', {"subID": self.sid, "pubID": ca})
        return arr
    
    def pullReports(self):
        cn = Db()
        ca = "ca"
        arr = cn.selectn('datas', '' , '', {"subID": self.sid, "pubID": ca})
        return arr
    
    def button_close(self, b):
        from dialogtermca import TermCaDialog
        self.close()
        post = TermCaDialog(self.term, self.termname )
        post.show()
         
    def button_click(self, b):
        
        set_arr = []
        ass_arr = []
        gra_arr = []
        cla_arr = []
        
        for i in self.set_arr:
            if self.set_arr[i].checkState(0) == Qt.Checked:
                set_arr.append(i)
        
        for i in self.ass_arr:
            if self.ass_arr[i].checkState(0) == Qt.Checked:
                ass_arr.append(i) 
                
        for i in self.gra_arr:
            if self.gra_arr[i].checkState(0) == Qt.Checked:
                gra_arr.append(i)
                
        for i in self.cla_arr:
            if self.cla_arr[i].checkState(0) == Qt.Checked:
                cla_arr.append(i)
                
        title = self.titleData.text()
        themeColor = self.le5.text()
        themeFont = self.le6.text()
        cla_store = self.cla_arr
        cla_store = ','.join(str(x) for x in cla_store)
        
        set_arr = '::'.join(str(x) for x in set_arr)
        gra_arr = '::'.join(str(x) for x in gra_arr)
        ass_arr = '::'.join(str(x) for x in ass_arr)
        
        
        save1 = title.upper()+':::'+ themeColor+':::'+ themeFont+':::'+ass_arr+':::'+ gra_arr+':::'+set_arr 

        
        g = Db()
        try:
            if(len(title) > 0):
                y = { 'name':cla_store, 'subID':self.term,  'description': save1}
                h = g.update('datas', y, {'id':self.row})
            else:
                pass
        except:
            pass
        
        self.button_close(self)
   