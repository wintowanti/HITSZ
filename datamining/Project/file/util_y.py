# -*-encoding=UTF-8 -*-
import re
import datetime

'''def read_lines(filepath):
        return a list include each line value
    fs = open(filepath,"r");
    strs = fs.read();
    fs.close();
    strs = strs.split("\n")
    strs = strs[0:len(strs)-1:]
    ans = []
    for item in strs:
        ans.append(item.split(","))
    return ans
'''
def read_lines(filepath):
    ans = []
    with open(filepath,"r") as infile:
        for line in infile:
            line = line.replace("\n","");
            line = line.replace("\r","");
            ans.append(line.split(","))
    return ans
    
# 字符串得到标准时间
# 1 y m d
# 2 y m d H M S
def get_time(timestr):
    tmp = re.findall(r"[\d]+",timestr)
    time_int = []
    for item in tmp:
        time_int.append(int(item))
    if len(time_int) == 3:
        return datetime.datetime(time_int[0],time_int[1],time_int[2])
    elif len(time_int) == 6:
        return datetime.datetime(time_int[0],time_int[1],time_int[2],time_int[3],time_int[4],time_int[5])
    else:
        #如果不符合上述情况， 返回最小时间
        return datetime.datetime.min
def now_time():
    import time
    tmp = time.strftime('%Y-%m-%d : %H:%M:%S',time.localtime(time.time()))
    return " time: " + tmp
# 输出函数
def print_y_x(filepath,z,y,x):
    outputf = open(filepath,"w+")
    for index in range(len(y)):
        outputf.write(str(z[index]))
        outputf.write(","+str(y[index]))
        for item in x[index]:
            outputf.write("," + str(item))
        outputf.write("\n")
    outputf.close()
    

def spilt_line():
    print "\n----------------------------------------------------------\n"
if __name__ == "__main__":

    print("开始")
    now_time()
    from path_y import *
    print now_time()
    print now_time()
    #read_lines(path_train_log)
    print now_time()
    print_y_x("./for_hjn/test.csv",[4,3,2],[1,2,3],[[1,2,3],[4,5,6],[7,8,9]])
    print("结束")

