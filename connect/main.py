# -*- coding: utf-8 -*-
"""
Created on Mon Jul  2 04:09:36 2018

@author: CHARLES
"""

import connect as con


g = con.Db()
j = g.createData()
#h = g.select('students')
#g.delete('students', {'id':5})
#print(g.select('students'))
#g.createStudent()
#g.insert('students', {'firstname':'dmarkaa', 'surname':'james', 'othername':'fato', 'address' : 'gggggggdmark', 'gender':0 })
#y = { 'firstname':'fabol', 'surname':'fiam', 'othername':'zed', 'gender':1 }
#y = ['surname', 'Firstaname', 'othername']
#z = {'id':3}
#z = {'surname': 'Charles'}
#h = g.list_to_str(y)
#g.insert('students', y)
h = g.select('datas')
print(j)