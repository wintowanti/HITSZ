# -*-encoding=UTF-8-*-
from util_y import *
from path_y import *
def output_dict(class_dict):
    for key in class_dict:
        fs = open("./data/"+key+".csv","w")
        for item in class_dict[key]:
            fs.write(",".join(item)+"\n")

#给频繁名字增加字典
def output_name(name_dict):
    tmp = 0
    fs = open(new_name_dict,"w")
    for key in name_dict:
        if name_dict[key] > 4:
            print key," ",name_dict[key]
            fs.write(key + " "+str(name_dict[key] + 10)+" nr\n")
            tmp += 1

    print "总共的新增人数: ",tmp
    
if __name__ == "__main__":
    lines = open_file(source_input,"\t")
    class_dict,name_dict= get_class_name(lines)
    #output_dict(class_dict)
    tsum  = 0
    for key in class_dict:
        print key," ",len(class_dict[key])
        tsum += len(class_dict[key])
    print tsum
    output_name(name_dict)
    print len(name_dict)
    print jieba
    
