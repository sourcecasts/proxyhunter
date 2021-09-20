# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject
from concurrent.futures import ThreadPoolExecutor
from time import sleep
from urllib import request
import socks
import re
import socket
import time
import threading 

class Processor(QObject):    # Main Processor check proxy...
    
    length = QtCore.pyqtSignal(int, str, str, str, str, str)
    
    def __init__(self, files, value, timeout, delay):    # Main Processor check proxy...
        super().__init__()
        
        self.Flags = False             # Stop threads flag...
        
        self.files = files             # File name...
        self.value = value             # Threads number...
        self.timeout = int(timeout)    # Threads timeout...
        self.delay = int(delay)        # Threads delay...
                
    def headers(self):    # Socket headers send metod...

        headers = ""
        headers += "GET /ip HTTP/1.1\r\n"
        headers += "Host: httpbin.org\r\n"
        headers += "User-Agent: Mozilla/5.0 (Windows NT 6.1; rv:82.0) Gecko/20100101 Firefox/82.0\r\n"
        headers += "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8\r\n"
        headers += "Accept-Language: ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3\r\n"
        headers += "Accept-Encoding: gzip, deflate\r\n"
        headers += "Connection: keep-alive\r\n"
        headers += "Upgrade-Insecure-Requests: 1\r\n"
        headers += "Cache-Control: max-age=0\r\n\r\n"
    
        return headers.encode()


    def stop(self):    # Stop threads metod...
    
        self.Flags = True
     
    
    def scanner_01(self, execaddress):    # Check processor metod...
    
        if not self.Flags:
            try:
                ipaddress = self.separate(execaddress)[0]    # Check ip metod...
                enaddress = self.separate(execaddress)[1]    # Check port metod...

                c = socks.socksocket()
                c.settimeout(int(self.timeout))
                c.set_proxy(socks.SOCKS5, ipaddress, int(enaddress))
                c.connect(("httpbin.org", 80))
                c.sendall(self.headers())
           
                t = time.time()

                response = c.recv(1024).decode("iso-8859-1")   # Check processor socks data response metod...
                sessions = round(time.time() - t, 3)
                sessions = str(sessions)
            
                if re.search("200", response):
                    self.length.emit(1, ipaddress, enaddress, "SOCKS", sessions, "Anonymus")
                            
            except Exception as error:
                self.length.emit(0, ipaddress, enaddress, "---", "0.00", "---")
                print(error)
    
    
    
    def scanner_02(self, execaddress):    # Check processor metod...
        
        if not self.Flags:
            try:
                ipaddress = self.separate(execaddress)[0]    # Check ip metod...
                enaddress = self.separate(execaddress)[1]    # Check port metod...

                c = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
                c.settimeout(int(self.timeout))
                c.connect((ipaddress, int(enaddress)))
                c.sendall(self.headers())
            
                t = time.time()

                response = c.recv(1024).decode("iso-8859-1")   # Check processor socks data response metod...
                sessions = round(time.time() - t, 3)
                sessions = str(sessions)

                if re.search("200", response):
                    self.length.emit(1, ipaddress, enaddress, "HTTP", sessions, "Transparent")
            
                if re.search("302", response):
                    self.length.emit(1, ipaddress, enaddress, "HTTP", sessions, "Anonymus")
       
            except Exception as error:
                print(error)
    
    
    
    
    def separate(self, execaddress):    # Starting processing separate...
    
        separate = execaddress.strip().split(":")
        return separate
    
    
    
    def sleep(self):    # Starting processing sleep...
    
        sleep = time.sleep(int(self.delay))
        return sleep
    
    
            
    def check(self, i, file): # Starting processing...
        for index in file:
            
            self.scanner_01(index.strip())    # Starting processing scanner_01...
            self.scanner_02(index.strip())    # Starting processing scanner_02...
        else:
            self.Flags = True


   
    def running(self):    # Starting processing threads...
    
        with open(self.files, encoding = "iso-8859-1") as file:  
        
            for i in range(self.value):
                thread = threading.Thread(target = self.check, args = (i, file)).start() 
                self.sleep()
                      
            executor = input("")

    # Starting processing threads...

   
  