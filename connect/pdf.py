# -*- coding: utf-8 -*-
"""
Created on Wed Aug 29 06:53:54 2018

@author: CHARLES
"""

from reportlab.pdfgen import canvas


def hello(c):
        c.drawString(100,100,"Hello World")
    
def coords(canvas):
     from reportlab.lib.units import inch
     from reportlab.lib.colors import pink, black, red, blue, green
     c = canvas
     c.setStrokeColor(pink)
     c.grid([inch, 2*inch, 3*inch, 4*inch], [0.5*inch, inch, 1.5*inch, 2*inch, 2.5*inch])
     c.setStrokeColor(black)
     c.setFont("Times-Roman", 20)
     c.drawString(0,0, "(0,0) the Origin")
     c.drawString(2.5*inch, inch, "(2.5,1) in inches")
     c.drawString(4*inch, 2.5*inch, "(4, 2.5)")
     c.setFillColor(red)
 
 
c = canvas.Canvas("hello.pdf")
hello(c)
coords(c)
c.showPage()
#c.save()
