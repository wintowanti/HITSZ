# -*-encoding=UTF-8 -*-
from feature_y import *
from drawroc import *
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.svm import LinearSVC
from sklearn.ensemble import RandomForestClassifier
import numpy  as ny

def main():
    pass
if __name__ =="__main__":
    gbc = RandomForestClassifier()
    X,Y = get_feature()
    X = ny.array(X)
    Y = ny.array(Y)
    print draw(X,Y,gbc)
    print Y
    print X
    print "开始"
    print "结束"

