# -*-encoding=UTF-8 -*-
from util_y import *
from basic_y import *
from path_y import *

# 加载 Date 返回一个dict 以cid 做索引
def load_date(filepath):
    spilt_line()
    print "开始加载date " + now_time()
    print "路径为 : " + filepath
    date_strs = read_lines(filepath)
    dict_date = {}
    for item in date_strs[1::]:
        d1 = Date(item[0],item[1],item[2])
        dict_date[d1.cid] = d1
    print "dict length : ", len(dict_date)
    print "完成加载date " + now_time()
    spilt_line()
    return dict_date;
    
# 加载 object 返回一个dict 以cid 做索引
def load_object(filepath):
    spilt_line()
    print "开始加载object " + now_time()
    print "路径为 : " + filepath
    object_strs = read_lines(filepath)
    dict_object = {}
    for item in object_strs[1::]:
        o1 = Object(item[0],item[1],item[2],item[3],item[4])
        if o1.cid not in dict_object:   dict_object[o1.cid] = []
        dict_object[o1.cid].append(o1);
    print "dict length : ", len(dict_object)
    print "完成加载object " + now_time()
    spilt_line()
    return dict_object;


# 加载 Log 返回一个list 包含每一条log
def load_log(filepath):
    spilt_line()
    print "开始加载log " + now_time()
    print "路径为 : " + filepath
    print "file load finish"
    list_log = []
    for item in read_lines(filepath):
       list_log.append(Log(item[0],item[1],item[2],item[3]))
    print "dict length : ", len(list_log)
    print "完成加载log " + now_time()
    spilt_line()
    return list_log;

# 加载 enrollment 返回一个dict 以eid 为索引
def load_enrollment(filepath):
    spilt_line()
    print "开始加载enrollment " + now_time()
    print "路径为 : " + filepath
    dict_enrollment = { }
    for item in read_lines(filepath)[1::]:
        e1 = Enrollment(item[0],item[1],item[2])
        dict_enrollment[e1.eid] = e1
    print "dict length : ", len(dict_enrollment)
    print "完成加载log " + now_time()
    spilt_line()
    return dict_enrollment;

# 加载 truth 返回一个dict 以eid 为索引
def load_truth(filepath):
    print "开始加载truth " + now_time()
    print "路径为 : " + filepath
    dict_truth = {}
    for item in read_lines(filepath)[::]:
        t1 = Truth(item[0],item[1])
        dict_truth[t1.eid] = t1
    print "dict length : ", len(dict_truth)
    print "完成加载truth " + now_time()
    spilt_line()
    print dict_truth[1]
    return dict_truth
    
def load_object_vector():
    print "开始加载object vector " + now_time()

    dict_object = load_object(path_object)
    ss = set()
    ss_list = []
    vector = {}
    for key in dict_object:
        for item in dict_object[key]:
            ss.add(item.category)
    for key in ss:
        ss_list.append(key)
    ss_list.sort()
    for key in dict_object:
        tmp = []
        for i in range(len(ss_list)):
            tmp.append(1.0)
        for index,item in enumerate(ss_list):
            for tt in dict_object[key]:
                if tt.category == item:
                    tmp[index] += 1.0
        vector[key] = []
        vector[key].append(sum(tmp))
        vector[key].extend(tmp)
        tsum = sum(tmp)
        for index in range(len(tmp)):
            tmp[index] /= tsum
        vector[key].extend(tmp)
    print "完成加载object vector " + now_time()
    return vector

if __name__ == "__main__":
    #load_date(path_date)
    #load_enrollment(path_train_enrollment)
    #tmp = load_truth(path_train_truth)
    #print tmp[1]
    #print len(tmp)
    #my_list = load_log(path_train_log_process)
    load_object_vector()
            
            
        
