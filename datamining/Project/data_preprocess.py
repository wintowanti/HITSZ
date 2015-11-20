# -*-coding=UTF-8 -*-
from yy_util import *

class Course(object):
    def __init__(self,cid,hashstring,start_time,end_time):
        self.cid = cid
        self.hashstring = hashstring
        self.start_time = start_time
        self.end_time = end_time
    def debug(self):
        print "---------------------------------"
        print "cid : ",self.cid
        print "hashstring : ",self.hashstring
        print "start_time : ",self.start_time
        print "end_time : ",self.end_time
        print "---------------------------------"
    def get_line(self):
        tmp = []
        tmp.append(self.cid)
        tmp.append(self.hashstring)
        tmp.append(self.start_time)
        tmp.append(self.end_time)
        return ",".join(tmp) + '\n'

class Course_Object(object):

    def __init__(self,cid,mid,category,children,start_time):
        self.cid = cid
        self.mid = mid
        self.category = category
        self.children = children
        self.start_time = start_time

    def debug(self):
        print "---------------------------------"
        print "cid : ",self.cid
        print "mid : ",self.mid
        print "category : ",self.category
        print "children : ",self.children
        print "start_time : ",self.start_time
        print "---------------------------------"

globe_Cdict = {"size":0};
globe_Mdict = {"size":0};
globe_Sdict = {"size":0};

def get_ID(Dict,hashstring):
    if hashstring in Dict:
        return Dict[hashstring]
    else:
        Dict[hashstring] = Dict["size"] + 1
        Dict["size"] = Dict["size"] + 1
        return Dict[hashstring]

if __name__ == "__main__":
    print "开始"
    path_date = "./data/date.csv"
    lines_date = read_lines(path_date)
    print lines_date
    tmp = []
    for index,line in enumerate(lines_date[1::]):
        mylist = line.split(",")
        c1 = Course(str(index + 1),mylist[0],mylist[1],mylist[2])
        tmp.append(c1);
    fs_data = open("data_process.csv","w")
    fs_data.write("Cid,Hashstring,start_time,end_time"+ "\n")
    for item in tmp:
        item.debug()
    for item in tmp:
        get_ID(globe_Cdict,item.hashstring)
        fs_data.write(item.get_line())
        print "bug",item.get_line()
    fs_data.close();
    print "len",len(tmp);

    print globe_Cdict

    path_object = "./data/object.csv"
    lines_object = read_lines(path_object)
    tmp = [];
    for index,line in enumerate(lines_object[1:10:]):
        mylist = line.split(",");
        print mylist
        print len(mylist)
        children_list = []
        for item in mylist[3].split(' '):
            if(item != ''):
                children_list.append(get_ID(globe_Mdict,item))
        cb1 = Course_Object(get_ID(globe_Cdict,mylist[0]),get_ID(globe_Mdict,mylist[1]),mylist[2],children_list,mylist[4])
        tmp.append(cb1)
    #for item in tmp:
    #    item.debug()
        
    print "结素"
