# -*- coding: utf-8 -*-
"""
Created on Sat Jan 26 05:26:19 2019

@author: CHARLES
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Nov 17 05:44:29 2018

@author: CHARLES
"""

from PyQt4.QtCore import SIGNAL, QDate, Qt, QSize, QSizeF
from PyQt4.QtGui import  QPrintPreviewDialog, QTextDocument, QPrinter, QLayout, QScrollArea, QMenuBar, QAction, QStackedWidget, QFont, QWidget, QSplitter, QFileDialog, QPixmap, QTabWidget, QComboBox, QRadioButton, QDateEdit, QTextEdit, QCheckBox, QHBoxLayout, QGroupBox, QGridLayout, QDialog, QApplication, QPushButton, QLineEdit, QFormLayout, QLabel, QVBoxLayout, QSizePolicy
from connect import Db
from datetime import datetime
from jinja2 import Template


class TableProfile(QDialog):
    
    def __init__(self, sid,  header, body, footer, formarts, columns, parent=None):
        super(TableProfile, self).__init__(parent)
        #page setup
        self.setGeometry(100, 100, 700, 700)
        self.textStyle = "background-color: white; color:black; border: 3px ridge #ccc"
        self.minW = 670
        self.maxW = 700
        self.sid =sid
        self.header = header
        self.body = body
        self.footer = footer
        self.formarts = formarts
        self.columns = [x + 1 for x in columns]
        
        print(columns)
        self.title = ''
        cn = Db()
        self.myterms = cn.getTermClass(self.sid)
        menu = self.menuUi()
        
        self.h1_box = QVBoxLayout()
        
        bioText = QTextEdit(self)
        bioText.setMinimumWidth(self.minW)
        bioText.setMinimumHeight(self.maxW)
        bioText.setMaximumHeight(self.maxW)
        btext = self.buildBio()
        bioText.insertHtml(btext)
        bioText.setStyleSheet(self.textStyle)
        self.h1_box.addWidget(bioText)
        self.h1_box.setSizeConstraint(QLayout.SetFixedSize)
        self.doc1 = bioText
        
        
        scrollArea = QScrollArea(self)
        scrollArea.setWidgetResizable(True)
        scrollArea.setFixedHeight(700)
        scrollArea.setFixedWidth(700)
        
        bioProfileWidget = QWidget()
        bioProfileWidget.setLayout(self.h1_box)
        #Main layout
        Hbox = QVBoxLayout()
        Hbox.addWidget(menu)
        Hbox.addStretch()
        Hbox.addWidget(bioProfileWidget)
        Hbox.setContentsMargins(0, 0, 0, 0)
       
        #Create central widget, add layout and set
        central_widget = QWidget(scrollArea)
        scrollArea.setWidget(central_widget)
        central_widget.setContentsMargins(0, 0, 0, 0)
        central_widget.setGeometry(0, 0, 650, 700)
        central_widget.setStyleSheet("background-color: #ccc; color:#000")
        central_widget.setLayout(Hbox)
       
        self.setWindowTitle('Title')
        self.show()    
        
    def getFile(self, a):
        fname = QFileDialog.getOpenFileName(self, 'Open', 'c:\\', "Image File (*.jpg *.png)")
        if a == 1:
            self.pic1.setPixmap(QPixmap(fname))
        elif a == 2:
            self.pic2.setPixmap(QPixmap(fname))
        elif a == 2:
            self.pic3.setPixmap(QPixmap(fname))
            
    def getFilez(self):
         fname = QFileDialog.getOpenFileName(self, 'Open', 'c:\\', "Image File (*.jpg *.png)")
         self.pic1.setPixmap(QPixmap(fname))
   
    def lunchPrintForm(self):
        self.lunchPrintPreview()
        #form.exec_()
        
    def handlePaintRequest(self, printer):
        document = self.doc1
        if document != None:
            document.print_(printer)
            
    def lunchPrintPreview(self):
        dialog = QPrintPreviewDialog()
        dialog.setContentsMargins(-5,-5,-5,-5)
        print(dir(dialog))
        dialog.paintRequested.connect(self.handlePaintRequest)
        dialog.exec_()
    
    def lunchPrintPdf(self, printer):
        document = self.doc1
        #document = QTextDocument(document)
        printer = QPrinter()
        printer.setResolution(96)
        printer.setPageMargins(5, 5, 5, 5, QPrinter.Millimeter)
        printer.setPageSize(QPrinter.Letter)
        printer.setOutputFormat(QPrinter.PdfFormat)
        printer.setOutputFileName('jjjjjjjjj.pdf')
        document.setPageSize(QSizeF(printer.pageRect().size()))
        print(document.pageSize(), printer.resolution(), printer.pageRect())
        document.print_(printer)
       
    
            
    def lunchReport(self, a, b, c = None):
        _item = a
        if _item == 1:
            self.profileStack.setCurrentIndex(0)
            self.bioText = QTextEdit()
            self.bioText.setMinimumWidth(self.minW)
            self.bioText.setMinimumHeight(self.maxW)
            self.bioText.setMaximumHeight(self.maxW)
            btext = self.buildBio()
            self.bioText.insertHtml(btext)
            self.bioText.setStyleSheet(self.textStyle)
        
    def menuUi(self):
        extractQuit = QAction(self) 
        extractQuit.setStatusTip('File')
          
        mainMenu = QMenuBar()
        
        fileMenu = mainMenu.addMenu('&File')
        exitMenu = QAction('&Exit', self)
        exitMenu.setShortcut('CTRL+Q')
        exitMenu.setStatusTip('Close Dialog')
        #exitMenu.triggered.connect(self.lunchUnitForm)
        fileMenu.addAction(exitMenu)
    
        printMenu = mainMenu.addMenu('&Print')
        printPrevMenu = QAction('&Print Preview', self)
        printPrevMenu.setShortcut('CTRL+P')
        printPrevMenu.setStatusTip('Print Preview')
        printPrevMenu.triggered.connect(self.lunchPrintForm)
        printMenu.addAction(printPrevMenu)
    
        printPDF = QAction('&Print PDF', self)
        printPDF.setShortcut('CTRL+D')
        printPDF.setStatusTip('PDF')
        printPDF.triggered.connect(self.lunchPrintPdf)
        printMenu.addAction(printPDF)

        printEXCEL = QAction('&Print EXCEL', self)
        printEXCEL.setShortcut('CTRL+E')
        printEXCEL.setStatusTip('EXCEL')
        printEXCEL.triggered.connect(self.lunchPrintForm)
        printMenu.addAction(printEXCEL)
        
        printCSV = QAction('&Print CSV', self)
        printCSV.setShortcut('CTRL+C')
        printCSV.setStatusTip('PDF')
        printCSV.triggered.connect(self.lunchPrintForm)
        printMenu.addAction(printCSV)
        return mainMenu
        
    
    
    def buildBio(self):       
        table = '''<html><head>
        <link rel ='stylesheet' type="text/css" href='static/stylesheets/invoice-print.css'/>
       
        </head>
        <style>
        body{
            font: "Century Gothic";
        }
        @font-face
        {
               
        }
        h1{
                font-family: "Poiret One";
                font-size:30px;
        }
        h2{
                font-family: "Sarala";
                font-size:20px;
        }
        h3{
                font-family: "Sarala";
                font-size:20px;
               
        }
        tbody, th, td{
        padding:2px;
         
        }
        td{ align:center}
        .tch{
                align: left !important;
                background-color:teal; 
                color:white;
                text-transform: uppercase;
                font-family: "Century Gothic";
        }
        .tch1{
                color:black;
                text-transform: uppercase;
                font-family: "Century Gothic";
                font-weight:bold;
                width: 300px;
        }
        .item-tab{
                display:inline-block;
        }
        td img{
        max-width: 100px;
        height:150px;
        }
        td .centers
        {
         align:center !important;
        }
        .xtable{ display:block;}
        .xrow{ display:block;}
        .xcell{ display:inline-block;}
        
        .xtable{ display:table;}
        .xrow{ display:table-row;}
        .xcell{ display:table-cell;}
        .xcell-10{ width:100px !important;}
        </style>
        <body>
        <table width="100%" cellspacing="0" cellpadding="2px"  style="border-width:1px; border-color: teal; padding:2px; color:black; font-family: Century Gothic">
            <thead>
                <tr style='background-color:teal; color:white'>
                {% for r in header %}
                    {% if r in cols %}
                        <th>{{header[r]}}</th>
                    {% endif %}
                {% endfor %}
                </tr>
            </thead>
            <tbody>
                {% for bod in body %}
                    <tr>
                        {% for bo in body[bod] %}
                            {% if bo in cols %}
                                <td {{formarts[bo]}}>{{body[bod][bo]}}</td>
                            {% endif %}    
                        {% endfor %}
                    </tr>
                {% endfor %}
            </tbody>
            <tfoot>
                <tr  style='background-color:teal; color:white'>
                {% for r in footer %}
                    {% if r in cols %}
                        <th>{{footer[r]}}</th>
                    {% endif %}
                {% endfor %}
                </tr>
            </tfoot>
        </table>
            
        </body>
        </html>'''
               
       
        h = Template(table).render(header= self.header, body= self.body, footer = self.footer, formarts = self.formarts, cols = self.columns)
        return h
    
    
    