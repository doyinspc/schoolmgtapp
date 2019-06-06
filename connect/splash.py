# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 15:03:04 2019

@author: CHARLES
"""

"""
Splash screen example

Eli Bendersky (eliben@gmail.com)
License: this code is in the public domain
Last modified: 09.05.2009
"""
from PyQt4 import QtCore, QtGui


class Form(QtGui.QDialog):
    """ Just a simple dialog with a couple of widgets
    """
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        self.browser = QtGui.QTextBrowser()
        self.setWindowTitle('Just a dialog')
        self.lineedit = QtGui.QLineEdit("Write something and press Enter")
        self.lineedit.selectAll()
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.browser)
        layout.addWidget(self.lineedit)
        self.setLayout(layout)
        self.lineedit.setFocus()
        self.connect(self.lineedit, QtCore.SIGNAL("returnPressed()"), self.update_ui)

    def update_ui(self):
        self.browser.append(self.lineedit.text())


#if __name__ == "__main__":
#    import sys, time
#
#    app = QtGui.QApplication(sys.argv)
#
#    # Create and display the splash screen
#    splash_pix = QtGui.QPixmap('icons/search.png')
#    splash = QtGui.QSplashScreen(splash_pix, QtCore.Qt.WindowStaysOnTopHint)
#    splash.setMask(splash_pix.mask())
#    splash.show()
#    app.processEvents()
#
#    # Simulate something that takes time
#    time.sleep(6 )
#
#    form = Form()
#    form.show()
#    splash.finish(form)
#    app.exec_()