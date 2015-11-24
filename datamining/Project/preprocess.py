# -*-encoding -*-

from path_y import *
from util_y import *

def b_s(str1):
	if str1 == "browser": return "0"
	else: return "1"

def event(str1):
    if str1 == "access": 
        return "0"
    if str1 == "page_close": 
        return "1"
    if str1 == "problem": 
        return "2"
    if str1 == "video": 
        return "3"
    if str1 == "discussion": 
        return "4"
    if str1 == "navigate": 
        return "5"
    if str1 == "wiki": 
        return "6"
    print str1

fs = open(path_train_log_process,"w")
for item in read_lines(path_train_log)[1::]:
    fs.write(item[0]+","+item[1]+","+b_s(item[2])+","+event(item[3])+'\n')
    
