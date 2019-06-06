# -*- coding: utf-8 -*-
"""
Created on Fri Mar 29 15:27:15 2019

@author: CHARLES
"""
from PyQt4.QtCore import SIGNAL, Qt, QEvent
from PyQt4.QtGui import QFontDialog, QColorDialog, QTreeWidget, QTreeWidgetItem, QStyle, QStyleOptionButton, QStyledItemDelegate, QStandardItemModel,  QStandardItem, QWidget,QComboBox, QListView, QListWidget, QFrame, QDateEdit, QRadioButton, QCheckBox, QHBoxLayout, QGroupBox, QGridLayout, QDialog, QApplication, QPushButton, QLineEdit, QFormLayout, QLabel, QVBoxLayout
from connect import Db

class DataDialog(QDialog):
    
    holdc = {}
    def __init__(self, parent=None):
        super(DataDialog, self).__init__(parent)
        self.pagetitle = 'School Data' 
    
        Form1 = QFormLayout()
       
        #title
        self.schoolName = QLabel("School Name")
        self.schoolNameData = QLineEdit()
        self.schoolNameData.setObjectName("name")
        self.schoolNameData.setPlaceHolderText("e.g. HERITAGE SCHOOL")
        
        self.schoolAlias = QLabel("School Alias")
        self.schoolAliasData = QLineEdit()
        self.schoolAliasData.setObjectName("alias")
        self.schoolAliasData.setPlaceHolderText("e.g. HERITAGE, HTS, HS ")
        
        self.schoolMotto = QLabel("Motto")
        self.schoolMottoData = QLineEdit()
        self.schoolMottoData.setObjectName("motto")
        self.schoolMottoData.setPlaceHolderText("e.g. Training a Nation ")
        
        self.schoolAddress = QLabel("Address")
        self.schoolAddressData = QLineEdit()
        self.schoolAddressData.setObjectName("address")
        self.schoolAddressData.setPlaceHolderText("e.g. 12. Lincon Street ")
        
        self.schoolCity = QLabel("City")
        self.schoolCityData = QLineEdit()
        self.schoolCityData.setObjectName("city")
        self.schoolCityData.setPlaceHolderText(" ")
        
        self.schoolState = QLabel("State/Region")
        self.schoolStateData = QLineEdit()
        self.schoolStateData.setObjectName("state")
        self.schoolStateData.setPlaceHolderText("California")
        
        self.schoolCountry = QLabel("Country")
        self.schoolCountryData = QLineEdit()
        self.schoolCountryData.setObjectName("country")
        self.schoolCountryData.setPlaceHolderText("USA")
        
        self.schoolEmail1 = QLabel("Email")
        self.schoolEmail1Data = QLineEdit()
        self.schoolEmail1Data.setObjectName("email")
        self.schoolEmail1Data.setPlaceHolderText("e.g. school@mail.com")
        
        self.schoolEmail2 = QLabel("Alternate Email")
        self.schoolEmail2Data = QLineEdit()
        self.schoolEmail2Data.setObjectName("aemail")
        self.schoolEmail2Data.setPlaceHolderText("e.g. school@mail.com")
        
        self.schoolPhone1 = QLabel("Phone Number")
        self.schoolPhone1Data = QLineEdit()
        self.schoolPhone1Data.setObjectName("phone")
        self.schoolPhone1Data.setPlaceHolderText("e.g.")
        
        self.schoolPhone2 = QLabel("Alternate Phone Number")
        self.schoolPhone2Data = QLineEdit()
        self.schoolPhone2Data.setObjectName("aphone")
        self.schoolPhone2Data.setPlaceHolderText("e.g.")
        
        self.schoolZip = QLabel("Zip Code")
        self.schoolZipData = QLineEdit()
        self.schoolZipData.setObjectName("zip")
        self.schoolZipData.setPlaceHolderText("XXXXXX")
        
        self.schoolPmb = QLabel("Mail Box/Bag")
        self.schoolPmbData = QLineEdit()
        self.schoolPmbData.setObjectName("pmb")
        self.schoolPmb2Data.setPlaceHolderText("e.g. P.O.Box 2020")
        
        self.connect(self.pbf, SIGNAL("clicked()"), lambda: self.font_picker())
        
        Form1.addRow(self.schoolName, self.schoolNameData)
        Form1.addRow(self.schoolAlias, self.schoolAliasData)
        Form1.addRow(self.schoolMotto, self.schoolMottoData)
        Form1.addRow(self.schoolAddress, self.schoolAddressData)
        Form1.addRow(self.schoolCity, self.schoolCityData)
        Form1.addRow(self.schoolState, self.schoolStateData)
        Form1.addRow(self.schoolCountry, self.schoolCountryData)
        Form1.addRow(self.schoolEmail1, self.schoolEmail1Data)
        Form1.addRow(self.schoolEmail2, self.schoolEmail2Data)
        Form1.addRow(self.schoolPhone1, self.schoolPhone1Data)
        Form1.addRow(self.schoolPhone2, self.schoolPhone2Data)
        Form1.addRow(self.schoolZip, self.schoolZipData)
        Form1.addRow(self.schoolPmb, self.schoolPmbData)
        
        Gbo = QGridLayout()
        Gbo.addLayout(Form1, 0, 0)
        
        groupBox1 = QGroupBox('Academic Report Setup')
        groupBox1.setLayout(Gbo)
        
        self.pb = QPushButton()
        self.pb.setObjectName("Add")
        self.pb.setText("Save")
        
        self.pb1 = QPushButton()
        self.pb1.setObjectName("Cancel")
        self.pb1.setText("Cancel")
        
        hbo = QHBoxLayout()
        hbo.addWidget(self.pb)
        hbo.addStretch()
        hbo.addWidget(self.pb1)
        
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
    
    def button_close(self, b):
        from dialogtermca import TermCaDialog
        self.close()
        post = TermCaDialog(self.term, self.termname )
        post.show()
        
    
         
    
        
        
       
                
        
