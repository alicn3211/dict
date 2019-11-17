#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 21:10:05 2019

@author: ali
"""

import pymysql
import re

f = open('all.txt')
db = pymysql.connect('localhost','root','19871228','dict')
cursor = db.cursor()

for line in f:
    l = re.split(r'\s+',line)
    word = l[0]
    interpret = ' '.join(l[1])
    
    sql = "insert into words (word,interpret) values('%s','%s')"%(word,interpret)
    
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()
f.close()