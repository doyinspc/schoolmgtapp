# -*- coding: utf-8 -*-
"""
Created on Sat Jul  7 14:37:47 2018

@author: CHARLES
"""
from PyQt4 import QtCore, QtGui
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *

def window():
     app = QtGui.QApplication(sys.argv)
     win = QtGui.QWidget()
     l1= QtGui.QLabel("Name")
     nm= QtGui.QLineEdit()
    
     l2= QtGui.QLabel("Abbrv")
     add1= QtGui.QLineEdit()
     add2= QtGui.QLineEdit()
     fbox= QtGui.QFormLayout()
     fbox.addRow(l1,nm)
     vbox= QtGui.QVBoxLayout()
    
     vbox.addWidget(add1)
     vbox.addWidget(add2)
    
     fbox.addRow(l2,vbox)
     hbox= QtGui.QHBoxLayout()
     r1= QtGui.QRadioButton("Male")
     r2= QtGui.QRadioButton("Female")
     hbox.addWidget(r1)
     hbox.addWidget(r2)
     hbox.addStretch()
     fbox.addRow( QtGui.QLabel("sex"),hbox)
     fbox.addRow(QtGui.QPushButton("Submit"),QtGui.QPushButton("Cancel"))
    
     win.setLayout(fbox)
    
     win.setWindowTitle("PyQt")
     win.show()
     sys.exit(app.exec_())
     
     
     
if __name__ == '__main__':
 window()
