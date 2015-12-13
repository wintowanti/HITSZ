# -*-encoding=UTF-8-*-
from path_y import *
import jieba
from sklearn import svm
print "加载 util_y 成功"


#打开文件  返回list list 包含list 用split_char分割
def open_file(filepath,split_char):
    fs = open(filepath,"r")
    lines = fs.readlines()
    ans = []
    for line in lines:
        line = line.replace("\n","")
        line = line.replace("\r","")
        ans.append(line.split(split_char))
    return ans

# 根据每一个类别 分割 
#返回一个class_dict 用类别作为Id 每一个dict[id] 是一个list
#返回一个name_dict 用名字作为Id 每一个dict[id] 表示次数
def get_class_name(lines):
    class_dict = {}
    name_dict = { }
    for line in lines:
        if line[0] not in class_dict: class_dict[line[0]] = []
        class_dict[line[0]].append(line)
        if line[1] not in name_dict: name_dict[line[1]] = 0
        name_dict[line[1]] += 1
        if line[2] not in name_dict: name_dict[line[2]] = 0
        name_dict[line[2]] += 1
    return class_dict,name_dict

#载入新词字典
def add_dict():
    print "加载新词典成功"
    jieba.load_userdict(new_name_dict) 
    jieba.load_userdict(famous_name_dict) 
    jieba.load_userdict(joey_name_dict) 

add_dict()
#根据两个类别建立分类器
#返回分类器，和term
if __name__ == "__main__":
    add_dict()
    str1 = "金秀贤真太丑"
    li = jieba.cut(str1)
    print ",".join(li)
    

