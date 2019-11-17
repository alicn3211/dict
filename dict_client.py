#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 22:36:03 2019

@author: ali
"""

import socket
import sys
import getpass

def main():
    if len(sys.argv) <3:
        print('argv is error')
        return
    
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
    s=socket.socket()
    try:
        s.connect((HOST,PORT))
    except Exception as e:
        print(e)
        return
    while True:
        print("""
              ====================welcome=====================
              1.sign up    2.login    3.quit
              ================================================
        
              """)
        try:
            cmd = int(input('input:'))
        except Exception as e:
            print('error',e)
            continue
        
        if cmd not in [1,2,3]:
            print('input type err')
            sys.stdin.flush()
            continue
        elif cmd ==1:
            r = do_register(s)
            if r == 0:
                print('done')
                
            elif r == 1:
                print('user yicunzai')
            else:
                print('sign up field')
        elif cmd ==2:
            name = do_login(s)
            print(name)
            if name:
                print('denglu chenggong')
                login(s,name)
                    
                    
            else:
                print('shuru bu zhengque')
        elif cmd == 3:
            print('thanks')
            break

def do_login(s):
    
    name = input('User:')
    passwd = getpass.getpass()
    msg = 'L {} {}'.format(name,passwd)
    s.send(msg.encode())
    data = s.recv(128).decode()
    print(data)
    if data == 'OK':
        return name
    
    else:
        return       
            
def do_register(s):
    while True:  
        name = input('User:')
        passwd = getpass.getpass()
        passwd1 = getpass.getpass('again:')
        if (' ' in name) or (' ' in passwd):
            print('user&password bu yunxu you kongge ')
            continue
        if passwd !=passwd1:
            print('liang ci mima bu yizhi')
            continue
        msg = 'R {} {}'.format(name,passwd)
        s.send(msg.encode())
        data = s.recv(128).decode()
        if data =='OK':
            return 0
        elif data == 'EXISTS':
            return 1
        else:
            return 2
    
            
            
def login(s,name):
    while True:
        print('''
            ================chaxun================
            1.chaci      2.lishijilu    3.tuichu
            ======================================                               
            ''')       
        try:
            cmd = int(input('input xuanxiang:'))
        except Exception as e:
            print('err',e)
            continue
        if cmd not in [1,2,3]:
            print('plz input right')
            sys.stdin.flush()
            continue
        elif cmd ==1:
            do_query(s,name)
        elif cmd == 2:
            do_hist(s,name)
        elif cmd ==3:
            return
        
def do_query(s,name):
    while True:
        word = input('shuru danci:')
        if word == '##':
            break
        msg = 'Q {} {}'.format(name,word)
        s.send(msg.encode())
        data= s.recv(128).decode()
        if data == "OK":
            data = s.recv(2048).decode()
            print(data)
        else:
            print('no word')

def do_hist(s,name):
    msg = "H {}".format(name)
    s.send(msg.encode())
    data = s.recv(128).decode()
    #print(data)
    if data =="OK":
        while True:
            data = s.recv(1024).decode()
            print(data)
            if data == "##":
                break
    else:
        print('no history')
    
        
        
        
if __name__ == "__main__":
    main()