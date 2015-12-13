# -*- encoding=UTF-8 -*-
'''
    包含一些基本的类
'''
from util_y import *
#Date类 表示Date.csv 的数据
class Date(object):
    def __init__(self,cid,start_time,end_time):
        self.cid = cid
        self.start_time = get_time(start_time)
        self.end_time = get_time(end_time)

    def debug(self):
        print "----------------Date start--------------------"
        print "cid: ",self.cid
        print "start_time: ",self.start_time
        print "end_time: ",self.end_time
        print "----------------Date end----------------------"
        
# Object
class Object(object):
    def __init__(self,cid,mid,category,children,start_time):
        self.cid = cid
        self.mid = mid
        self.category = category
        self.start_time = get_time(start_time)
        children = children.split(" ");
        self.children = children[0:len(children)-1:]

    def debug(self):
        print "----------------Objct start--------------------"
        print "cid: ",self.cid
        print "mid: ",self.mid
        print "category: ",self.category
        print "children: ",self.children
        print "start_time: ",self.start_time
        print "----------------Object end----------------------"

# enrollment
class Enrollment(object):
    def __init__(self,eid,uid,cid):
        self.eid = int(eid)
        self.uid = uid
        self.cid = cid

    def debug(self):
        print "----------------Enrollment start--------------------"
        print "eid: ",self.eid
        print "uid: ",self.uid
        print "cid: ",self.cid
        print "----------------Enrollment end----------------------"
# log 
class Log(object):
    def __init__(self,eid,time,source,event):
        self.eid = int(eid)
        self.time = get_time(time)
        self.source = source
        self.event = event

    def debug(self):
        print "----------------Log start--------------------"
        print "eid: ",self.eid
        print "time: ",self.time
        print "source: ",self.source
        print "event: ",self.event
        print "----------------Log end----------------------"

#Truth
class Truth(object):
    def __init__(self,eid,answer):
        self.eid = int(eid)
        self.answer = int(answer)
        
    def debug(self):
        print "----------------Truth start--------------------"
        print "eid: ",self.eid
        print "answer: ",self.answer
        print "----------------Truth end----------------------"

#Source_Event
class Source_Event(object):
    def __init__(self):
        self.count = [];
        for i in range(9):
           self.count.append(0.0)

    def add(self,str1):
        if(str1 == "00"): self.count[0] += 1.0
        elif(str1 == "01"): self.count[1] += 1.0
        elif(str1 == "02"): self.count[2] += 1.0
        elif(str1 == "03"): self.count[3] += 1.0
        elif(str1 == "10"): self.count[4] += 1.0
        elif(str1 == "14"): self.count[5] += 1.0
        elif(str1 == "15"): self.count[6] += 1.0
        elif(str1 == "12"): self.count[7] += 1.0
        elif(str1 == "16"): self.count[8] += 1.0

    def div(self,se1):
        ans = Source_Event()
        for i in range(9):
            if(se1.count[i] == 0.0 and self.count[i] == 0.0):  ans.count[i] = 0.0
            elif(se1.count[i] == 0.0 and self.count[i] != 0.0): ans.count[i] = 0.5
            else: 
                ans.count[i] = self.count[i] / se1.count[i]
        return ans

    def debug(self):
        spilt_line()
        for item in self.count:
            print item," ",
        print "\n"
        spilt_line()
last_operate_day = {}

if __name__ == "__main__":
    print "开始"
    se1 = Source_Event();
    se2 = Source_Event();
    se1.add("01")
    se2.add("01")
    se2.add("00")
    se2.add("01")
    se1.debug()
    se2.debug()
    se3 = se1.div(se2);
    se3.debug();
    print "结束"
