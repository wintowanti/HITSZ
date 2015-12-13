# -*-encoding=utf-8 -*-
from util_y import *

#切割每一个句子 返回一个list 包含每一个词组(str)
def cut_words(line):
    ans_list= []
    words = jieba.cut(line)
    for item in words:
        ans_list.append(item)
    return ans_list

#得到term
def get_term(lista,listb):
    terma = { }
    termb = { }

    for line in lista:
        words = cut_words(line[3])
        for item in words:
            if item not in terma:terma[item] = 0
            terma[item] += 1

    for line in listb:
        words = cut_words(line[3])
        for item in words:
            if item not in termb:termb[item] = 0
            termb[item] += 1
    ans_term = []
    for key in terma:
        #大于某一个阈值才选用
        if terma[key]  > 3:
            ans_term.append(key)
    for key in termb:
        #大于某一个阈值才选用
        if termb[key]  > 3:
            ans_term.append(key)
    return ans_term

    
def get_model(skmodel,lista,listb,keya,keyb):
    term = get_term(lista,listb)
    X = []
    Y = []
    for line in lista:
        x = []
        words = cut_words(line[3])
        for item in term:
            if item in words: x.append(1.0)
            else : x.append(0.0)
        X.append(x)
        Y.append(0.0)

    for line in listb:
        x = []
        x = []
        words = cut_words(line[3])
        for item in term:
            if item in words: x.append(1.0)
            else : x.append(0.0)
        X.append(x)
        Y.append(1.0)
        
    print keya," ",keyb,"",len(term)
    skmodel.fit(X,Y)
    return  skmodel,term

#得到某一个模型
def new_model():
    return svm.SVC(kernel='linear',probability=True)

#返回所有的类型list 和一个model_dict(第一个是model 第二个是 term 第三个为第一个类的名称 第四个为第二个类的名称)
def get_all_model(lines):
 #   lines = open_file(source_input,"\t")
    class_dict,name_dict = get_class_name(lines)
    class_list = [] 
    for key in class_dict:
        print key
        class_list.append(key)
    class_list.sort()

    model_dict = {}
    #遍历两个
    for indexa,keya in enumerate(class_list):
        for indexb,keyb in enumerate(class_list):
            if  indexa < indexb:
                tmp = new_model()
                tmp_model,tmp_term = get_model(tmp,class_dict[keya],class_dict[keyb],keya,keyb)
                model_dict[keya + keyb]=[]
                model_dict[keya + keyb].append(tmp_model)
                model_dict[keya + keyb].append(tmp_term)
                model_dict[keya + keyb].append(keya)
                model_dict[keya + keyb].append(keyb)

    return class_dict,model_dict

def test():
    lines = open_file(source_input,"\t")
    train = lines[0:4000:]
    test = lines[4000:7000:]
    class_dict,model_dict = get_all_model(train)

    tsum = 0.0
    for line in test:
        tmp = {}
        words = cut_words(line[3])
        for key in model_dict:
            models =  model_dict[key]
            X = []
            x = []
            for term in models[1]:
                if term in words: x.append(1.0)
                else: x.append(0.0)
            X.append(x)
            ans = models[0].predict_proba(X)
            if models[2] not in tmp: tmp[models[2]] = 0.0
            if models[3] not in tmp: tmp[models[3]] = 0.0
            tmp[models[2]] += ans[0][0]
            tmp[models[3]] += ans[0][1]
        tmax = 0.0
        tkey = ""
        for key in tmp:
            if(tmp[key] > tmax):
                tkey = key
                tmax = tmp[key]
        if(tkey == line[0]): tsum += 1.0
        else:
            print tkey," ",line[0]," ",line[3]
            for key in tmp:
                print key,tmp[key]
    print tsum/len(test)
                
            
def test2():
    class_dict,model_dict = get_all_model()
    lines = open_file(source_test,"\t")
    fs = open("./test.csv","w")
    tsum = 0.0
    for line in lines:
        tmp = {}
        words = cut_words(line[0])
        for key in model_dict:
            models =  model_dict[key]
            X = []
            x = []
            for term in models[1]:
                if term in words: x.append(1.0)
                else: x.append(0.0)
            X.append(x)
            ans = models[0].predict_proba(X)
            if models[2] not in tmp: tmp[models[2]] = 0.0
            if models[3] not in tmp: tmp[models[3]] = 0.0
            tmp[models[2]] += ans[0][0]
            tmp[models[3]] += ans[0][1]
        tmax = 0.0
        tkey = ""
        for key in tmp:
            if(tmp[key] > tmax):
                tkey = key
                tmax = tmp[key]
        fs.write(tkey+","+line[0]+","+str(tmax)+"\n")
def test3():
    lines = open_file(source_test,"\t")
    dic1 ={ }
    for line in lines:
        dic1[line[0]] = 1
    print len(dic1)
def main():
    test3()
if __name__ == "__main__":
    main()
    str1 = "金秀贤真太丑"
    cut_words(str1)
    pass

