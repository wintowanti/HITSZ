# -*-encoding=UTF-8 -*-
import re
import datetime

def read_lines(filename):
    '''
        return a list include each line value
    '''
    fs = open(filename,"r");
    ans = fs.read();
    fs.close();
    ans = ans.split("\n")[0::]
    return ans[0:len(ans)-1:]
    
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

if __name__ == "__main__":

    print("开始")
    st1 = "2014-06-27T01:10:40"

    d1 = get_time(st1)
    st2 = "2014-06-2"
    d2 = get_time(st2)
    print dir(d1)
    print d1.__sub__.__doc__
    print (d1 - d2).days
    print type(d1 - d2)

