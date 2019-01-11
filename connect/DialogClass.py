# -*- coding: utf-8 -*-
"""
Created on Sat Jul  7 04:19:29 2018

@author: CHARLES
"""

from PyQt4 import QtCore, QtGui

class ClassDialog(QtGui.QDialog):
    
    
    def __init__(self, parent = None):
        super(ClassDialog, self).__init__(parent)
        self.resize(300, 300)
        buttonBox = QtGui.QDialogButtonBox(self)
        buttonBox.setGeometry(QtCore.QRect(300, 40, 81, 221))
        buttonBox.setOrientation(QtCore.Qt.Vertical)
        buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        
        self.setWindowTitle("Dialog")
        QtCore.QObject.connect(buttonBox, QtCore.SIGNAL("accepted()"), ClassDialog.accept)
        
        QtCore.QMetaObject.connectSlotsByName(self)
        
        
    def showEvent(self, event):
        geom = self.frameGeometry()
        geom.moveCenter(QtGui, QCursor.pos())
        self.setGeometry(geom)
        super(ClassDialog, self).showEvent(event)
        
    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key.Escape:
            self.hide()
            event.accept()
        else:
            super(ClassDialog, self).keyPressEvent(event)
            
            

if __name__ == '__main__':
    app = QtGui.QApplication([])
    d = ClassDialog()
    d.show()
    d.raise_()
    
    app.exec_()
    
    