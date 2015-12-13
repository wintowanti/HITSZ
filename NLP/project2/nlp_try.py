# -*- coding: utf-8 -*-
import jieba
import jieba.posseg as pseg
from numpy import *
import copy
from svmutil import *

def get_feature_dict(line, pos1, pos2, index, feature_dict, window):
    vec = pseg.cut(line)
    words = []; tags = []
    for w,tag in vec:
        words.append(w)
        tags.append(tag)
    for pos in [pos1, pos2]:
        for i in range(-window, 0)+range(1, window+1):
            if pos+i < 0 or pos+i >= len(words):
                continue
            word_keys = feature_dict[i]['word'].keys()
            tag_keys = feature_dict[i]['tag'].keys()
            w = words[pos+i]; tag = tags[pos+i]
            if w in word_keys:
                feature_dict[i]['word'][w].append(index)
            else:
                feature_dict[i]['word'][w] = [index]
            if tag in tag_keys:
                feature_dict[i]['tag'][tag].append(index)
            else:
                feature_dict[i]['tag'][tag] = [index]
    return feature_dict



def build_matrix(feature_dict, multi_class, labels, window):
    train_data = []

    n = len(labels)
    for row in range(n):
        vec = []
        for pos in range(-window, 0)+range(1, window+1):
            data = feature_dict[pos]
            for k in ['word', 'tag']:
                keys = data[k].keys()
                for w in keys:
                    if len(data[k][w]) < 3:
                        continue
                    if row in data[k][w]:
                        vec.append(1)
                    else:
                        vec.append(0)
        train_data.append(vec)
    print len(train_data[0])
    return train_data



'''
feature_dict 的格式为{-2:{'word':{w1:[index1,index2..],w2:{}..},'tag':{}}, -1:{}...}
'''
def read_file(lines, names, window):
    multi_class = []; labels = []
    words = {}; tags = {}
    feature_dict = {}
    for i in range(-window, 0)+range(1, window+1):
        #统计名字旁第i个词的词和词性
        feature_dict[i] = {'word':{}, 'tag':{}}
    for i, line in enumerate(lines):
        vec = line.split('\t')
        name1 = vec[1].decode('utf-8')
        name2 = vec[2].decode('utf-8')
        keys = names[i].keys()
        if name1 in keys and name2 in keys:
            pos1 = names[i][name1]
            pos2 = names[i][name2]
            get_feature_dict(vec[3], pos1, pos2, i, feature_dict, window)
        multi_class.append(vec[0])
        labels.append(vec[4][:-1])
    train_data = build_matrix(feature_dict, multi_class, labels, window)
    return train_data, multi_class, labels
    

def get_surname(file_name):
    f = open(file_name)
    lines = f.readlines()
    surname = []
    for w in lines:
        surname.append(w.strip())
    return surname

#name = {name:pos}
def analyse(line, surname):
    words = []
    tags = []
    names = {}
    vec = pseg.cut(line)
    for w,tag in vec:
        words.append(w)
        tags.append(tag)
    jump = False
    n = len(tags)
    for i in range(n):
        if jump:
            jump = False
            continue
        if tags[i] == 'nr':
            if len(words[i]) > 1:
                names[words[i]] = i
            else:
                ss = words[i].encode('utf-8')
                if ss in surname and i < n-1:
                    name = words[i] + words[i+1]
                    names[name] = i
                    jump = True
                else:
                    ss1 = words[i-1][-1:].encode('utf-8')
                    ss2 = words[i-1][-2:-1].encode('utf-8')
                    if ss1 in surname:
                        name = words[i-1][-2:] + words[i]
                        names[name] = i-1
                    elif ss2 in surname:
                        name = words[i-1][-2:] + words[i]
                        names[name] = i-1
        elif len(tags[i]) > 1:
            if tags[i][:2] == 'nr':
                ss = words[i][0].encode('utf-8')
                if ss in surname:
                    names[words[i]] = i
    return names
                



def get_name(lines):
    jieba.load_userdict('F:joey_name.txt')
    jieba.load_userdict('F:bigname.txt')
    jieba.load_userdict('F:famous_name.txt')
    jieba.load_userdict('F:renmin.txt')
    surname_file = 'F:surname_.txt'
    surname = get_surname(surname_file)
    names = []
    for line in lines:
        vec = line.split('\t')
        name = analyse(vec[3], surname)
        names.append(name)
    return names


def split_data(train_data, multi_class, test_num):
    train_matrix = []; train_class = []
    test_matrix = []; test_class = []
    random_vec = []
    n = len(train_data)
    for i in range(test_num):
        k = random.randint(0, n)
        while k in random_vec:
            k = random.randint(0, n)
        random_vec.append(k)
    for i in range(n):
        if i in random_vec:
            test_matrix.append(train_data[i])
            test_class.append(multi_class[i])
        else:
            train_matrix.append(train_data[i])
            train_class.append(multi_class[i])
    return train_matrix, train_class, test_matrix, test_class, random_vec

'''
在class_set中位置靠前的类标记为1，靠后的标记为-1
'''
def one_vs_one_data(train_matrix, train_class, class1, class2):
    n = len(train_matrix)
    x = []; y = []
    for i in range(n):
        if multi_class[i] == class1:
            x.append(train_matrix[i])
            y.append(1)
        elif multi_class[i] == class2:
            x.append(train_matrix[i])
            y.append(-1)
    return x, y


def balance_data(x, y):
    pos_data = []; neg_data = []
    pos_label = []; neg_label = []
    for i in range(len(y)):
        if y[i] == 1:
            pos_data.append(x[i])
            pos_label.append(y[i])
        else:
            neg_data.append(x[i])
            neg_label.append(y[i])
    n1 = len(pos_data)
    n2 = len(neg_data)
    if n1 > n2:
        for i in range(n1-n2):
            k = random.randint(0, n2)
            x.append(neg_data[k])
            y.append(neg_label[k])
    else:
        for i in range(n2-n1):
            k = random.randint(0, n1)
            x.append(pos_data[k])
            y.append(pos_label[k])
    return x, y



def get_svm_classer(train_matrix, train_class, class_set, lines):
    d = len(class_set)
    classer_vec = []
    for i in range(d):
        for j in range(i+1, d):
            class1 = class_set[i]; class2 = class_set[j]
            x, y = one_vs_one_data(train_matrix, train_class, class1, class2)
            x, y = balance_data(x, y)
            m = svm_train(y, x, ' -t 2 -c 4 -g 0.1')
            classer_vec.append(m)

            
    return classer_vec

def get_label(predict_vec):
    pre_set = list(set(predict_vec))
    max_num = -1; label = ''
    for val in pre_set:
        num = predict_vec.count(val)
        if num > max_num:
            max_num = num
            label = val
    print max_num, label.decode('utf-8')
    return label


def count_err(classer_vec, test_matrix, test_class, class_set, lines):
    n = len(test_class); d = len(class_set)
    err = 0
    for i in range(n):
        data = []
        data.append(train_matrix[i])
        label = test_class[i]
        num = 0
        predict_vec = []
        for j in range(d):
            for k in range(j+1, d):
                class1 = class_set[j]; class2 = class_set[k]
                y = [1]; m = classer_vec[num]
                p_label, p_acc, p_val = svm_predict(y, data, m)
                if p_label[0] == 1:
                    predict_vec.append(class_set[j])
                else:
                    predict_vec.append(class_set[k])
                print class_set[j].decode('utf-8'), class_set[k].decode('utf-8'), p_label[0], label.decode('utf-8')
                num = num+1
        predict_label = get_label(predict_vec)
        #print vec[3].decode('utf-8')
        print predict_label.decode('utf-8')
        print label.decode('utf-8')
        if predict_label != label:
            err = err+1
    print err/float(n)
    return err/float(n)
        


if __name__ == "__main__":
    file_name = "F:project2_TrainingSet7000"
    f = open(file_name)
    lines = f.readlines()
    names = get_name(lines)
    window = 2
    test_num = 100
    train_data, multi_class, labels = read_file(lines, names, window)
    train_matrix, train_class, test_matrix, test_class, index_vec = \
                  split_data(train_data, multi_class, test_num)
    #通过svm训练d(d-1)/2个二元分类器，d为关系类的个数
    class_set = list(set(multi_class))
    classer_vec = get_svm_classer(train_data, multi_class, class_set, lines)
    err_rate = count_err(classer_vec, train_data, multi_class, class_set, lines)
            














    
