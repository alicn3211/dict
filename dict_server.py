#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 22:19:36 2019

@author: ali

"""
import socket
import os
import time
import signal
import pymysql
import sys

DICT_TXT = './all.txt'
HOST = '0.0.0.0'
PORT = 8345
ADDR = (HOST,PORT)

def main():
    #db = pymysql.connect('loaclhost','root','19871228','dict')
    db = pymysql.connect(host="localhost",user='root',
                     password='19871228',database='dict')
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    s.bind(ADDR)
    s.listen(5)

    signal.signal(signal.SIGCHLD,signal.SIG_IGN)
    
    while True:
        try:
             c,addr = s.accept()
             print('connect from ',addr)
        except KeyboardInterrupt:
            s.close()
            sys.exit('quit')
        except Exception as e:
            print(e)
            continue
        
        pid = os.fork()
        if pid ==0:
            s.close()
            do_child(c,db)
        else:
            c.close()
            continue
def do_child(c,db):
    
    
    while True:
        data = c.recv(128).decode()
        print(c.getpeername(),':',data)
        if data[0] == 'R':
            do_register(c,db,data)
        elif data[0] == "L":
            do_login(c,db,data)
        elif data[0] == "Q":
            do_query(c,db,data)
        elif data[0] == "H":
            do_hist(c,db,data)
        
    
    
    
    
    
    
def do_login(c,db,data):
    print('denglu caozuo')
    l = data.split(' ')
    name = l[1]
    passwd = l[2]
    cursor = db.cursor()
    print(name,passwd)
    
    sql = "select * from user where name = '%s' and passwd='%s'"%(name,passwd)
    cursor.execute(sql)
    r = cursor.fetchone()
    if r == None:
        c.send(b'FALL')
    else:
        print('%s denglu chenggong'%name)
        c.send(b'OK')
    
def do_register(c,db,data):
    print('sign up done')
    l = data.split(' ')
    name = l[1]
    passwd = l[2]
    cursor = db.cursor()
    sql = "select * from user where name='%s'"%name
    cursor.execute(sql)
    r = cursor.fetchone()
    if r !=None:
        c.send(b'EXISTS')
        return
    sql = "insert into user (name,passwd) values('%s','%s')"%(name,passwd)
    try:
        cursor.execute(sql)
        db.commit()
        c.send(b'OK')
    except:
        db.rollback()
        c.send(b'FALL')
    else:
        print("%s done"%name)
    
def do_query(c,db,data):
    print("chaxun caozuo")
    l = data.split(' ')
    name =l[1]
    word = l[2]
    cursor = db.cursor()
    #print(word)
    def insert_history():
        tm = time.ctime()
        
        sql = "insert into hist (name,word,time) values('%s','%s','%s')"%(name,word,tm)
        try:
            cursor.execute(sql)
            db.commit()
            #print('charu chenggongs')
        except:
            db.rollback()
            print('err')
    try:
        f= open(DICT_TXT)
    except:
        c.send(b'FALL')
        return
    for line in f:
        tmp = line.split(' ')[0]
        #print(tmp)
        if tmp > word:
            c.send(b'FALL')
            return
            f.close()
        elif tmp ==word:
            c.send(b'OK')
            time.sleep(0.1)
            c.send(line.encode())
            f.close()
            insert_history()
            return
    c.send(b'FALL')
    f.close()
            
            
            
            
            
def do_hist(c,db,data):
    print("lishi jilu")
    l = data.split(' ')
    name = l[1]
    cursor = db.cursor()
    
    sql = "select * from hist where name='%s'"%name
    cursor.execute(sql)
    r= cursor.fetchall()
    #print(r)
    #print(type(r))
    if not r:
        c.send(b'FALL')
    else:
        c.send(b'OK')
    for i in r:
        time.sleep(0.1)
        msg = "%s   %s  %s"%(i[1],i[2],i[3])
        c.send(msg.encode())
    time.sleep(0.1)
    c.send(b'##')

    
if __name__ == "__main__":
    main()










