# -*- coding: utf-8 -*-
"""
Created on Tue Dec  4 11:59:44 2018

@author: CHARLES
"""
from PyQt4.QtCore import SIGNAL, QSizeF
from PyQt4.QtGui import  QTextCursor,  QPrinter, QFont, QTextDocument, QPrintDialog, QWidget, QFrame, QDateEdit, QPrintPreviewDialog, QCheckBox, QHBoxLayout, QGroupBox, QGridLayout, QDialog, QApplication, QPushButton, QLineEdit, QFormLayout, QLabel, QVBoxLayout


class PrintTable(QDialog):
   
    def __init__(self, table, parent=None):
        super(PrintTable,  self).__init__(parent)
        self.table = table
        #self.handlePreview()
        #self.handlePrintPdf()
        
    def handlePrintPdf(self):
        printer = QPrinter()
        pdffile ='test.pdf'
        printer.setResolution(96)
        printer.setPageSize(QPrinter.Letter)
        printer.setOutputFormat(QPrinter.PdfFormat)
        printer.setOutputFileName(pdffile)
        printer.setPageMargins(5, 5, 5, 10, QPrinter.Millimeter)
        document = self.makeTableDocument()
        
        document.setPageSize(QSizeF(printer.pageRect().size()))
        document.print_(printer)
        
        
    def handlePrint(self):
        dialog = QPrintDialog()
        if dialog.exec_() == QDialog.Accepted:
            self.handlePaintRequest(dialog.printer())

    def handlePreview(self):
        dialog = QPrintPreviewDialog()
        dialog.setStyleSheet("table {border:1px; border-color:teal}")
        dialog.setWindowTitle('Adedoyin Adetunji')
        #dialog.showMaximized()
        #dialog.setMaximumSize(True)
        #dialog.setResolution(96)
        #dialog.setPageSize(QPrinter.Letter)
        #dialog.setPageMargins(5, 5, 5, 10, QPrinter.Millimeter)
        dialog.paintRequested.connect(self.handlePaintRequest)
        dialog.exec_()
    
    def handlePaintRequest(self, printer):
        document = self.makeTableDocument()
        document.print_(printer)

    def makeTableDocument(self):
        printer = QPrinter()
        document = QTextDocument()
        document.setDefaultStyleSheet("table {border:1px; border-color:teal}")
        document.setDefaultStyleSheet("h1, h2, h3 {color:teal}")
        document.setDocumentMargin(0.0)
        document.setPageSize(QSizeF(printer.pageRect().size()))
        header = '''
                <html>
                    <body>
                        <div style="line-height:2.5">
                            <h1>Desmond International College</h1>
                            <h2>Km4, Happiness Street, Kafanchan</h2>
                            <h2>Kaduna, Nigeria</h2>
                        </div>
                        <div>
                            <h2 style='display:block; text-align:center; word-spacing:10vw; text-transform: uppercase; margin-top:25px; margin-bottom:15px'><u>STUDENT DATA TABLE</u></h2>    
                        </div>
                    </body>
                </html>
                '''
        #print(dir(document))
        
        cursor = QTextCursor(document)
        rows = self.table.rowCount()
        columns = self.table.columnCount()
        cursor.insertHtml(header)
        table = cursor.insertTable(rows + 1, columns)
        formats = table.format()
        formats.setHeaderRowCount(1)
        table.setFormat(formats)
        formats = cursor.blockCharFormat()
        formats.setFontWeight(QFont.Bold)
        for column in range(columns):
            cursor.setCharFormat(formats)
            cursor.insertText(self.table.horizontalHeaderItem(column).text())
            cursor.movePosition(QTextCursor.NextCell)
        for row in range(rows):
            for column in range(columns):
                cursor.insertText(self.table.item(row, column).text())
                cursor.movePosition(QTextCursor.NextCell)
        
        
        return document
    
    def makeHeader(self):
        header = '''
                <html>
                    <body>
                        <div style="line-height:2.5">
                            <h1>Desmond International College</h1>
                            <h2>Km4, Happiness Street, Kafanchan</h2>
                            <h2>Kaduna, Nigeria</h2>
                        </div>
                        <div>
                            <h2 style='display:block; text-align:center; word-spacing:10vw; text-transform: uppercase; margin-top:25px; margin-bottom:15px'><u>STUDENT DATA TABLE</u></h2>    
                        </div>
                    </body>
                </html>
                '''
        return header
    
    def makeTable(self, cols, rows, data):
    
        table = '<div>'
        table +='<table width="100%" style="Background-color:darkblue;color:white">'
        table +='<thead>'
        table +='<tr>'
        for a in cols:
          table +='<td>'
          table += str(a)
          table +='</td>'   
        table +='</tr>'
        table +='</thead>'
        table +='<tbody>'
        table +='</tbody>'
        
        table +='</table>'
        table +='</div>'
              
           
        return table