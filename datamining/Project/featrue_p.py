# -*- encoding=UTF-8 -*-
from util_y import *
from path_y import *
from basic_y import *
from load_y import *
from sklearn import svm
from sklearn import cross_validation
from sklearn import tree
from sklearn import ensemble

global_date = load_date(path_date)
global_enrollment = load_enrollment(path_train_enrollment)
global_log = load_log(path_train_log_process)
global_truth = load_truth(path_train_truth)
global_object_vector = load_object_vector()

global_uc = []
global_u = [] 
global_c = []
#end 后28数  
day_28 = {}
last_operate_day = {}

for i in range(4):
    global_uc.append({})
    global_u.append({})
    global_c.append({})
    
def add_to(globe,nid,se):
    if nid not in globe: globe[nid] = Source_Event()
    globe[nid].add(se)


for item in global_log:
    eid = item.eid
    cid = global_enrollment[eid].cid
    uid = global_enrollment[eid].uid
    start_time = global_date[cid].start_time
    end_time = global_date[cid].end_time
    now_time = item.time
    # first add 28
    if eid not in day_28:
        day_28[eid] = []
        for i in range(28):
            day_28[eid].append(0.0)
    last_days = (end_time - now_time).days
    # 最后一次操作
    if eid not in last_operate_day : last_operate_day[eid] = 100
    if last_days < last_operate_day[eid]:
        last_operate_day[eid] = last_days

    # 最后28天的是否有 操作
    if(last_days >=0 and last_days < 28): day_28[eid][last_days] = 1.0
    se = item.source + item.event
    # 总体
    add_to(global_uc[0],eid,se)
    #add_to(global_u[0],uid,se)
    #add_to(global_c[0],cid,se)
    if (now_time - start_time).days <= 7 :
        #第一周
        add_to(global_uc[1],eid,se)
        #add_to(global_u[1],uid,se)
        #add_to(global_c[1],cid,se)
        pass
    elif (end_time - now_time).days <= 7:
        #倒数第一周
        add_to(global_uc[3],eid,se)
        #add_to(global_u[3],uid,se)
        #add_to(global_c[3],cid,se)
    elif (end_time - now_time).days >7 and (end_time - now_time).days <=14:
        #倒数第二周
        add_to(global_uc[2],eid,se)
        #add_to(global_u[2],uid,se)
        #add_to(global_c[2],cid,se)

X = []
Y = []
#每一门课 人的集合 对应的list
global_c_u= { }
#每一人 课的集合 对应的list
global_u_c= { }

#每一门课 drop out人数  float
global_c_drop = {}
#每一人课 drop out人数  float
global_u_drop = {}
last_operate_day = {}

for key in global_enrollment:
    item = global_enrollment[key]
    eid = item.eid
    uid = item.uid
    cid = item.cid
    if cid not in global_c_u: global_c_u[cid] = []
    global_c_u[cid].append(uid)
    last_operate_day = {}

    if uid not in global_u_c: global_u_c[uid] = []
    global_u_c[uid].append(cid)

    if cid not in global_c_drop: global_c_drop[cid] = 0.0
    if global_truth[eid].answer == 0: global_c_drop[cid] += 1.0
    if uid not in global_u_drop: global_u_drop[uid] = 0.0 
    last_operate_day = {}
    if global_truth[eid].answer == 0: global_u_drop[uid] += 1.0

for key in global_enrollment:
    item = global_enrollment[key]
    eid = item.eid
    uid = item.uid
    cid = item.cid
    x1 = []
    y1 = int(global_truth[eid].answer)
    if key % 10000 == 0: print key
    # 72 维度()
    for index in range(4):
        if eid not in global_uc[index]: global_uc[index][eid] = Source_Event()
        #if uid not in global_u[index]: global_u[index][uid] = Source_Event()
        #if cid not in global_c[index]: global_c[index][cid] = Source_Event()
        #divu = global_uc[index][eid].div(global_u[index][uid])
        #divc = global_uc[index][eid].div(global_c[index][cid])
        # 9个操作的每一个总数
        x1.extend(global_uc[index][eid].count)
        tsum = 0.0
        for item in global_uc[index][eid].count:
            tsum += item
        tmp = Source_Event()
        for i in range( len(tmp.count) ): 
            tmp.count[i] = tsum

        # 9个操作每一个的占总的比例
        tnext = global_uc[index][eid].div(tmp)
        x1.extend(tnext.count)
        #x1.extend(divu.count)
        #x1.extend(divc.count)
    # 28 维 28 day(28)
    x1.extend(day_28[eid])
    # 此课程选课人数 (1)
    x1.append(len(global_c_u[cid]))
    # 此人选课总数 (1)
    x1.append(len(global_u_c[uid]))
    # 最后一次操作距离截止日的天数(1)
    if eid not in last_operate_day: last_operate_day[eid] = 100
    x1.append(last_operate_day[eid])
    # 此课的放弃率
    #x1.append(global_c_drop[cid] * 1.0 / len(global_c_u[cid]))
    # 此人的放弃率
    #x1.append(global_u_drop[uid] * 1.0 / len(global_u_c[uid]))
    #加载课程向量
    x1.extend(global_object_vector[cid])

    X.append(x1)
    Y.append(y1)

print "good"
sv = svm.LinearSVC()
tr = tree.DecisionTreeClassifier()
rf = ensemble.RandomForestClassifier()
gbc = ensemble.GradientBoostingClassifier()

y1 = cross_validation.cross_val_score(sv,X,Y,cv=4)
print "svm linearSVC: ",y1," average: ",sum(y1)/len(y1)

y1 = cross_validation.cross_val_score(tr,X,Y,cv=4)
print "tree-descsion: ",y1," average: ",sum(y1)/len(y1)

y1 = cross_validation.cross_val_score(rf,X,Y,cv=4)
print "randomforest :",y1," average: ",sum(y1)/len(y1)

y1 = cross_validation.cross_val_score(gbc,X,Y,cv=4)
print "GradientBoostingClassifier :",y1," average: ",sum(y1)/len(y1)



