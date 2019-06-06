# -*- coding: utf-8 -*-
"""
Created on Fri Mar 29 15:27:15 2019

@author: CHARLES
"""
from PyQt4.QtCore import SIGNAL, Qt, QEvent
from PyQt4.QtGui import QFileDialog,QPixmap, QImage, QFontDialog, QColorDialog, QTreeWidget, QTreeWidgetItem, QStyle, QStyleOptionButton, QStyledItemDelegate, QStandardItemModel,  QStandardItem, QWidget, QComboBox, QListView, QListWidget, QFrame, QDateEdit, QRadioButton, QCheckBox, QHBoxLayout, QGroupBox, QGridLayout, QDialog, QApplication, QPushButton, QLineEdit, QFormLayout, QLabel, QVBoxLayout
from connect import Db
from validate import Valid, Buttons, Settingz
from PIL import Image
from PIL.ImageQt import ImageQt
import os
import zipfile
import pandas as pd
import time
import ast
from datetime import datetime

class DataDialog(QDialog):

    def __init__(self, parent=None):
        super(DataDialog, self).__init__(parent)
        self.pagetitle = 'School Data' 
        stylesheet = Valid().background() + Valid().font()
        self.setStyleSheet(stylesheet)
        Form1 = QFormLayout()
        Form2 = QGridLayout()
        
        data = Valid().pullData('datas', '', {'pubID':'datas'})
        data_arr = {}
        for d in data:
            data_arr[d['name']] = d['description']
    
        namex = None
        alias = None
        motto = None
        address = None
        city = ''
        state = ''
        country = ''
        pmb = ''
        zipx = ''
        email1 = ''
        email2 = ''
        phone1 = ''
        phone2 = ''
        color1 = ''
        color2 = ''
        
        try:
            if(data_arr and data_arr['namex']): namex = data_arr['namex']
            print(namex)
        except:
            pass
        try:
            if(data_arr and data_arr['alias']): alias = data_arr['alias']
        except:
            pass
        try:
            if(data_arr and data_arr['motto']): motto = data_arr['motto']
        except:
            pass
        try:
            if(data_arr and data_arr['address']): address = data_arr['address']
        except:
            pass
        try:
            if(data_arr and data_arr['city']): city = data_arr['city']
        except:
            pass
        try:
            if(data_arr and data_arr['state']): state = data_arr['state']
        except:
            pass
        try:
            if(data_arr and data_arr['country']): country = data_arr['country']
        except:
            pass
        try:
            if(data_arr and data_arr['pmb']): pmb = data_arr['pmb']
        except:
            pass
        try:
            if(data_arr and data_arr['zip']): zipx = data_arr['zip']
        except:
            pass
        try:
            if(data_arr and data_arr['email1']): email1 = data_arr['email1']
        except:
            pass
        try:
            if(data_arr and data_arr['email2']): email2 = data_arr['email2']
        except:
            pass
        try:
            if(data_arr and data_arr['phone1']): phone1 = data_arr['phone1']
        except:
            pass
        try:
            if(data_arr and data_arr['phone2']): phone2 = data_arr['phone2']
        except:
            pass
        try:
            if(data_arr and data_arr['color1']): color1 = data_arr['color1']
        except:
            pass
        try:
            if(data_arr and data_arr['color2']): color2 = data_arr['color2']
        except:
            pass
     
        
        #title
        self.schoolName = QLabel("School Name")
        self.schoolNameData = QLineEdit()
        self.schoolNameData.setObjectName("name")
        self.schoolNameData.setPlaceholderText("e.g. HERITAGE SCHOOL")
        if namex: self.schoolNameData.setText(namex)
        
        self.schoolAlias = QLabel("School Alias")
        self.schoolAliasData = QLineEdit()
        self.schoolAliasData.setObjectName("alias")
        self.schoolAliasData.setPlaceholderText("e.g. HERITAGE, HTS, HS ")
        if alias: self.schoolAliasData.setText(alias)
        
        self.schoolMotto = QLabel("Motto")
        self.schoolMottoData = QLineEdit()
        self.schoolMottoData.setObjectName("motto")
        self.schoolMottoData.setPlaceholderText("e.g. Training a Nation ")
        if motto: self.schoolMottoData.setText(motto)
        
        self.schoolAddress = QLabel("Address")
        self.schoolAddressData = QLineEdit()
        self.schoolAddressData.setObjectName("address")
        self.schoolAddressData.setPlaceholderText("e.g. 12. Lincon Street ")
        if address: self.schoolAddressData.setText(address)
        
        self.schoolCity = QLabel("City")
        self.schoolCityData = QLineEdit()
        self.schoolCityData.setObjectName("city")
        self.schoolCityData.setPlaceholderText("Abuja")
        if city: self.schoolCityData.setText(city)
        
        self.schoolState = QLabel("State/Region")
        self.schoolStateData = QLineEdit()
        self.schoolStateData.setObjectName("state")
        self.schoolStateData.setPlaceholderText("California")
        if state: self.schoolStateData.setText(state)
        
        self.schoolCountry = QLabel("Country")
        self.schoolCountryData = QLineEdit()
        self.schoolCountryData.setObjectName("country")
        self.schoolCountryData.setPlaceholderText("USA")
        if country: self.schoolCountryData.setText(country)
        
        self.schoolEmail1 = QLabel("Email")
        self.schoolEmail1Data = QLineEdit()
        self.schoolEmail1Data.setObjectName("email")
        self.schoolEmail1Data.setPlaceholderText("e.g. school@mail.com")
        if email1: self.schoolEmail1Data.setText(email1)
        
        self.schoolEmail2 = QLabel("Alternate Email")
        self.schoolEmail2Data = QLineEdit()
        self.schoolEmail2Data.setObjectName("aemail")
        self.schoolEmail2Data.setPlaceholderText("e.g. school@mail.com")
        if email2: self.schoolEmail2Data.setText(email2)
        
        self.schoolPhone1 = QLabel("Phone Number")
        self.schoolPhone1Data = QLineEdit()
        self.schoolPhone1Data.setObjectName("phone")
        self.schoolPhone1Data.setPlaceholderText("")
        if phone1: self.schoolPhone1Data.setText(phone1)
        
        self.schoolPhone2 = QLabel("Alternate Phone Number")
        self.schoolPhone2Data = QLineEdit()
        self.schoolPhone2Data.setObjectName("aphone")
        self.schoolPhone2Data.setPlaceholderText("")
        if phone2: self.schoolPhone2Data.setText(phone2)
        
        self.schoolZip = QLabel("Zip Code")
        self.schoolZipData = QLineEdit()
        self.schoolZipData.setObjectName("zip")
        self.schoolZipData.setPlaceholderText("XXXXXX")
        if zipx: self.schoolZipData.setText(zipx)
        
        self.schoolPmb = QLabel("Mail Box/Bag")
        self.schoolPmbData = QLineEdit()
        self.schoolPmbData.setObjectName("pmb")
        self.schoolPmbData.setPlaceholderText("e.g. P.O.Box 2020")
        if pmb: self.schoolPmbData.setText(pmb)
        
        self.colorLbl = QLabel("Pick School's primary and secondary colors. White and Black colors would be ignored")
        self.colorPrimary = QPushButton('Select')
        self.colorSecondary = QPushButton('Select')
        self.colorPrimaryLbl = QLineEdit()
        self.colorSecondaryLbl = QLineEdit()
        self.colorPrimaryLbls = QLabel('Primary Color')
        self.colorSecondaryLbls = QLabel('Secondary Color')
        if color1: self.colorPrimaryLbl.setText(color1)
        if color2: self.colorSecondaryLbl.setText(color2)
        if color1: self.colorPrimaryLbl.setStyleSheet("background-color:"+ color1 +"")
        if color2: self.colorSecondaryLbl.setStyleSheet("background-color:"+ color2 +"")
        
        self.connect(self.colorPrimary, SIGNAL("clicked()"), lambda x= 0: self.color_picker(x))
        self.connect(self.colorSecondary, SIGNAL("clicked()"), lambda x = 1: self.color_picker(x))
        
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
        Form2.addWidget(self.colorPrimaryLbls, 0, 0)
        Form2.addWidget(self.colorPrimaryLbl, 0, 1)
        Form2.addWidget(self.colorPrimary, 0, 2)
        Form2.addWidget(self.colorSecondaryLbls, 1, 0)
        Form2.addWidget(self.colorSecondaryLbl, 1, 1)
        Form2.addWidget(self.colorSecondary, 1, 2)
        
        groupBox1 = QGroupBox('School Data')
        groupBox1.setLayout(Form1)
        
        Gbo = QGridLayout()
        Gbo.addWidget(self.colorLbl, 0, 0)
        Gbo.addLayout(Form2, 1, 0)
        
        groupBox2 = QGroupBox('School Colors')
        groupBox2.setLayout(Gbo)
        
        self.pb = QPushButton()
        self.pb.setObjectName("Add")
        self.pb.setText("Save")
        
        self.pb1 = QPushButton()
        self.pb1.setObjectName("Cancel")
        self.pb1.setText("Close")
        
        hbo = QHBoxLayout()
        hbo.addWidget(self.pb1)
        hbo.addStretch()
        hbo.addWidget(self.pb)
        
        groupBox3 = QGroupBox('')
        groupBox3.setLayout(hbo)
            
        grid = QGridLayout()
        grid.addWidget(groupBox1, 0, 0)
        grid.addWidget(groupBox2, 1, 0)
        grid.addWidget(groupBox3, 2, 0)
        
        self.setLayout(grid)
        self.connect(self.pb, SIGNAL("clicked()"), lambda: self.button_click())
        self.connect(self.pb1, SIGNAL("clicked()"), lambda: self.button_close(self))
       
        self.setWindowTitle(self.pagetitle)

    
    def color_picker(self, a):
        self.cp = QColorDialog.getColor()
        if a == 0:
            self.colorPrimaryLbl.setText(self.cp.name())
            self.colorPrimaryLbl.setStyleSheet("background-color:"+self.cp.name() +"")
        elif a == 1:
            self.colorSecondaryLbl.setText(self.cp.name())
            self.colorSecondaryLbl.setStyleSheet("background-color:"+self.cp.name() +"")
      
    
    def button_close(self, a):
        a.close()
    
        
    def button_click(self):
        arr = {}
        arr['namex'] = self.schoolNameData.text()
        arr['alias'] = self.schoolAliasData.text()
        arr['motto'] = self.schoolMottoData.text()
        arr['address'] = self.schoolAddressData.text()
        arr['city'] = self.schoolCityData.text()
        arr['country'] = self.schoolCountryData.text()
        arr['state'] = self.schoolStateData.text()
        arr['email1'] = self.schoolEmail1Data.text()
        arr['email2'] = self.schoolEmail2Data.text()
        arr['phone1'] = self.schoolPhone1Data.text()
        arr['phone2'] = self.schoolPhone2Data.text()
        arr['zip'] = self.schoolZipData.text()
        arr['pmb'] = self.schoolPmbData.text()
        arr['color1'] = self.colorPrimaryLbl.text()
        arr['color2'] = self.colorSecondaryLbl.text()
        
        #print(arr)
        db = 'datas'
        g = Db()
        
        for a in arr:
            s = g.selectn(db , '', 1, {'pubID':'datas', 'name':a})
            if s and s['id'] > 0:
                if arr[a] and len(arr[a]) > 0:
                    g.update(db, {'description': arr[a]}, {'id':s['id']})
                else:
                    g.delete(db, {'id':s['id']})
            else:
                if arr[a] and len(arr[a]) > 0:
                    print(arr[a])
                    g.insert(db, {'pubID': 'datas', 'name':a, 'description': arr[a]})
        
    
        self.button_close(self)

class LogoDialog(QDialog):

    def __init__(self, parent=None):
        super(LogoDialog, self).__init__(parent)
        self.pagetitle = 'School Data' 
        stylesheet = Valid().background() + Valid().font()
        self.setStyleSheet(stylesheet)
        
        data = Db().selectn('datas', '', 1, {'pubID':'datas', 'name':'logo'})
        d = ''
        if data:
            d = data['description']
        else:
            d = ''
        
        self.pic1 = QLabel()
        self.pic1.setAlignment(Qt.AlignCenter)
        if os.path.isfile('./pic_main/logo.png'):
            image1 = Image.open('pic_main/logo.png')
        else:
            image1 = Image.open('img/stdpic.png')
        
        self.mainLink = ''
        imageQ1 = ImageQt(image1)
        imagep1 = QPixmap(QPixmap.fromImage(QImage(imageQ1).scaled(250, 300, Qt.IgnoreAspectRatio)))
        self.pic1.resize(250, 300)
        self.pic1.setPixmap(imagep1)
        self.pic1.setMaximumHeight(250)
        #self.pic1.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.picBtn1 = QPushButton('Select Image')
        self.picBtn1.clicked.connect(lambda:self.getFilez())
        self.colorLbl = QLabel('Please use only only images in png format prferablly with transperent background')
        self.colorLbl1 = QLabel('Image should be a perfect square')
        
        Gbo = QGridLayout()
        Gbo.addWidget(self.colorLbl, 0, 0)
        Gbo.addWidget(self.colorLbl1, 1, 0)
        Gbo.addWidget(self.pic1, 2, 0)
        Gbo.addWidget(self.picBtn1, 3, 0)
        
        groupBox1 = QGroupBox('Upload School Logo')
        groupBox1.setLayout(Gbo)
        
        self.pb = QPushButton()
        self.pb.setObjectName("Add")
        self.pb.setText("Save")
        
        self.pb1 = QPushButton()
        self.pb1.setObjectName("Cancel")
        self.pb1.setText("Close")
        
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
        self.connect(self.pb, SIGNAL("clicked()"), lambda: self.button_click())
        self.connect(self.pb1, SIGNAL("clicked()"), lambda: self.button_close(self))
        self.setWindowTitle(self.pagetitle)

    
    def getFilez(self):
         fname = QFileDialog.getOpenFileName(self, 'Select Image', 'c:\\', '*.png')
         image1 = Image.open(fname)
         imageQ1 = ImageQt(image1)
         imagep1 = QPixmap(QPixmap.fromImage(QImage(imageQ1).scaled(300, 300, Qt.IgnoreAspectRatio)))
         self.pic1.resize(300, 300)
         self.pic1.setPixmap(imagep1)
         self.mainLink = image1
        
    
    def setCurrentPix(self):
        file1 = "pic_main/"
        img = ''
        img = str(file1)+'logo.png'
             
        image1 = Image.open(img)
        imageQ1 = ImageQt(image1)
        imagep1 = QPixmap(QPixmap.fromImage(QImage(imageQ1).scaled(250, 250, Qt.IgnoreAspectRatio)))
        self.pic1.resize(250, 250)
        self.pic1.setPixmap(imagep1)
      
    
    def button_close(self, a):
        a.close()
      
    def button_click(self):
        fname = self.mainLink
        im1 = fname
        file1 = 'pic_thumb/'
        file2 = 'pic_main/'
        lnk = "logo.png"
      
        im1.thumbnail((128, 128))
        im1.save(file1 + lnk, "PNG" )
        
        im1.thumbnail((300, 300))
        im1.save(file2 + lnk, "PNG")
    
        g = Db()
        sel = g.selectn('datas', '', 1, {'pubID':'datas', 'name':'logo'})
        if sel and sel['id'] > 0:
            pass
        else:
            g.insert('datas', {'pubID':'datas', 'name':'logo', 'description': lnk})
            
        self.setCurrentPix()  
        self.button_close(self)
    
                
class OfflineDialog(QDialog):
       
    def __init__(self, parent=None):
        super(OfflineDialog, self).__init__(parent)
        
        self.pagetitle = 'Offline Back Up' 
        stylesheet = Valid().background() + Valid().font()

        
        self.hold_data = {}
        self.tree = QTreeWidget()
        self.tree.setHeaderLabel("Choose Sessions to Back-up")
        self.tree.headerItem().setText(0, 'Name')
        #self.tree.setStyleSheet(treeStyleSheet)
        arr = Db().selectn('session','', 5)
        if arr and len(arr) > 0:
               for val in arr:
                 child = QTreeWidgetItem(self.tree)
                 child.setFlags(child.flags() | Qt.ItemIsUserCheckable)
                 child.setText(0, str(val['name']).upper())
                 self.hold_data[val['id']] = child
                 child.setCheckState(0, Qt.Checked)
                
        
        
        self.pb = QPushButton()
        self.pb.setObjectName("Add")
        self.pb.setText("Save")
        
        self.pb1 = QPushButton()
        self.pb1.setObjectName("Cancel")
        self.pb1.setText("Close")
        
        hbo = QHBoxLayout()
        hbo.addWidget(self.pb1)
        hbo.addStretch()
        hbo.addWidget(self.pb)
        
        groupBox2 = QGroupBox('')
        groupBox2.setLayout(hbo)
            
        grid = QGridLayout()
        grid.addWidget(self.tree, 0, 0)
        grid.addWidget(groupBox2, 1, 0)
        
        self.setLayout(grid)
        self.connect(self.pb, SIGNAL("clicked()"), lambda: self.button_click())
        self.connect(self.pb1, SIGNAL("clicked()"), lambda: self.button_close(self))
        
        self.setStyleSheet(stylesheet)
        #self.setWindowIcon(QIcon(self.titleIcon))
        self.setWindowTitle(self.pagetitle)

    def button_close(self, a):
        a.close()

        
    def getSelected(self):
        k = []
        for i in self.hold_data:
            if self.hold_data[i].checkState(0) == Qt.Checked:
                    k.append(i)
        return  k          
        
        
    def button_click(self):
        session = self.getSelected()
        arr = []
        g = Db()
        for a in session:
            arr.append('school_awards'+str(a))
            arr.append('school_expenses'+str(a))
            arr.append('school_mails'+str(a))
            arr.append('school_medicals'+str(a))
            arr.append('school_stores'+str(a))
            terms = g.selectn('terms', '', '', {'sessionID': a})
            
            for b in terms:
                arr.append('student_affective'+str(b['id']))
                arr.append('student_class'+str(b['id']))
                arr.append('student_fee'+str(b['id']))
                arr.append('student_pay'+str(b['id']))
                arr.append('student_psy'+str(b['id']))
                arr.append('student_result'+str(b['id']))
                arr.append('student_subject'+str(b['id']))
         
        arr.append('session') 
        arr.append('terms')
        arr.append('students')
        arr.append('datas')
        
        try:
            f = open('_temp/data.txt', "w")
            save_date = time.time()
            f.write('SAVED_DATE='+str(save_date)+'\n SAVED_TABLES='+str(arr)+'\n SAVED_IDS='+str(session))
            f.close()
        except:
            pass
        
        for c in arr:
            try:
                df = g.selectPandas(c)
                df.to_csv('_temp/'+c+'.csv', index=False)
            except:
                pass
           
        fileName = QFileDialog.getSaveFileName(self, 'Save File as', '', '*.zip')
        achi_zip = zipfile.ZipFile(fileName+'.zip', 'w')
        
        for root, dirs, files in os.walk('_temp/'):
            for afile in files:
                achi_zip.write(os.path.join(root, afile), afile, compress_type = zipfile.ZIP_DEFLATED)
        
        achi_zip.close()
        
        #self.clearFolder()
        
    def clearFolder(self):
        folder = '_temp'
        for f in os.listdir(folder):
            f_path = os.path.join(folder, f)
            try:
                if os.path.isfile(f_path):
                    os.unlink(f_path)
            except:
                pass
        
        
        
class OfflinerDialog(QDialog):
       
    def __init__(self, parent = None):
        super(OfflinerDialog, self).__init__(parent)
        
        self.pagetitle = 'Offline Restore' 
        stylesheet = Valid().background() + Valid().font()
        fileName = QFileDialog.getOpenFileName(self, 'Save File as', '', '*.zip')
        achi_zip = zipfile.ZipFile(fileName)
        achi_zip.extractall('_temp')
        achi_zip.close()
        
        re = open('_temp/data.txt', 'r')
        arr_string = {}
        contents = re.readlines()
        for con in contents:    
            r = con.split('=')
            arr_string[r[0].strip()] = r[1]
            
        #print(arr_string)
        list_dt = arr_string['SAVED_DATE']
        damt = datetime.utcfromtimestamp(float(list_dt)).strftime('%d-%m-%Y, %H:%M:%S')
        #dt = 
        self.sessions = ast.literal_eval(arr_string['SAVED_IDS'])
        self.list_data = ast.literal_eval(arr_string['SAVED_TABLES'])
        self.hold_data = {}
        self.tree = QTreeWidget()
        self.tree.setHeaderLabel("Choose Sessions to restore")
        self.tree.headerItem().setText(0, 'Choose Sessions')
        #self.tree.setStyleSheet(treeStyleSheet)
        for t in self.sessions:
            arr = Db().selectn('session', '', 1, {'id':t})
         
            if arr and arr['id'] > 0:
                     child = QTreeWidgetItem(self.tree)
                     child.setFlags(child.flags() | Qt.ItemIsUserCheckable)
                     child.setText(0, str(arr['name']).upper())
                     self.hold_data[arr['id']] = child
                     child.setCheckState(0, Qt.Checked)
        
        self.pb = QPushButton()
        self.pb.setObjectName("Add")
        self.pb.setText("Restore")
        
        self.pb1 = QPushButton()
        self.pb1.setObjectName("Cancel")
        self.pb1.setText("Close")
        
        hbo = QHBoxLayout()
        hbo.addWidget(self.pb1)
        hbo.addStretch()
        hbo.addWidget(self.pb)
        
        groupBox2 = QGroupBox('')
        groupBox2.setLayout(hbo)
        
        self.lbl = QLabel('Saved on the '+damt)
        
        grid = QGridLayout()
        grid.addWidget(self.lbl, 0, 0)
        grid.addWidget(self.tree, 1, 0)
        grid.addWidget(groupBox2, 2, 0)
        
        self.setLayout(grid)
        self.connect(self.pb, SIGNAL("clicked()"), lambda: self.button_click())
        self.connect(self.pb1, SIGNAL("clicked()"), lambda: self.button_close(self))
        
        self.setStyleSheet(stylesheet)
        #self.setWindowIcon(QIcon(self.titleIcon))
        self.setWindowTitle(self.pagetitle)

    def button_close(self, a):
        a.close()

        
    def getSelected(self):
        k = []
        for i in self.hold_data:
            if self.hold_data[i].checkState(0) == Qt.Checked:
                    k.append(i)
        return  k          
        
        
    def button_click(self):
        g = Db()
        
        g.createDatas()
        g.createStudent()
        g.createSession()
        g.createTerm()
        
        for z in self.sessions:
             g.createExpenses(z)
             g.createStores(z)
             g.createAwards(z)
             g.createConducts(z)
             g.createMails(z)
             g.createMedicals(z)
             arr = g.selectn('terms', '', '', {'id':z})
        
             for t1  in arr:
                 t = t1['id']
                 g.createClass(t)
                 g.createSubject(t)
                 g.createFee(t)
                 g.createPay(t)
                 g.createResult(t)  
                 g.createAffective(t)
                 g.createPsychomoto(t)
        
        for c in self.list_data:
            try:
                g.replacePandas(c)
            except:
                pass
        
        off = OfflineDialog() 
        off.clearFolder()
               
 