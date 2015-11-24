# -*- encoding=UTF-8 -*-
from util_y import *
from path_y import *
from basic_y import *
from load_y import *
from sklearn import svm
from sklearn import cross_validation
from sklearn import tree
from sklearn import ensemble

globe_date = load_date(path_date)
globe_enrollment = load_enrollment(path_train_enrollment)
# 小数据
globe_log = load_log(path_train_log_process)
globe_truth = load_truth(path_train_truth)

globe_uc = []
globe_u = []
globe_c = []
#end 后28数  bool 模型
day_28 = {}

for i in range(4):
    globe_uc.append({})
    globe_u.append({})
    globe_c.append({})
    
def add_to(globe,nid,se):
    if nid not in globe: globe[nid] = Source_Event()
    globe[nid].add(se)


for item in globe_log:
    eid = item.eid
    cid = globe_enrollment[eid].cid
    uid = globe_enrollment[eid].uid
    start_time = globe_date[cid].start_time
    end_time = globe_date[cid].end_time
    now_time = item.time
    # first add 28
    if eid not in day_28:
        day_28[eid] = []
        for i in range(28):
            day_28[eid].append(0.0)
    last_days = (end_time - now_time).days
    if(last_days >=0 and last_days < 28): day_28[eid][last_days] += 1.0
    se = item.source + item.event
    # 总体
    add_to(globe_uc[0],eid,se)
    add_to(globe_u[0],uid,se)
    add_to(globe_c[0],cid,se)
    if (now_time - start_time).days <= 7 :
        #第一周
        add_to(globe_uc[1],eid,se)
        add_to(globe_u[1],uid,se)
        add_to(globe_c[1],cid,se)
        pass
    elif (end_time - now_time).days <= 7:
        #倒数第一周
        add_to(globe_uc[3],eid,se)
        add_to(globe_u[3],uid,se)
        add_to(globe_c[3],cid,se)
    elif (end_time - now_time).days >7 and (end_time - now_time).days <=14:
        #倒数第二周
        add_to(globe_uc[2],eid,se)
        add_to(globe_u[2],uid,se)
        add_to(globe_c[2],cid,se)

eid = 1
cid = globe_enrollment[eid].cid
uid = globe_enrollment[eid].uid
globe_uc[0][eid].debug()
globe_c[0][cid].debug()
globe_u[0][uid].debug()
globe_uc[0][eid].div (globe_c[0][cid]).debug()

X = []
Y = []
#每一门课 人的集合 对应的list
globe_c_u= { }
#每一人 课的集合 对应的list
globe_u_c= { }

#每一门课 drop out人数  float
globe_c_drop = {}
#每一人课 drop out人数  float
globe_u_drop = {}

for key in globe_enrollment:
    item = globe_enrollment[key]
    eid = item.eid
    uid = item.uid
    cid = item.cid
    if cid not in globe_c_u: globe_c_u[cid] = []
    globe_c_u[cid].append(uid)

    if uid not in globe_u_c: globe_u_c[uid] = []
    globe_u_c[uid].append(cid)

    if cid not in globe_c_drop: globe_c_drop[cid] = 0.0
    if globe_truth[eid].answer == 0: globe_c_drop[cid] += 1.0

    if uid not in globe_u_drop: globe_u_drop[uid] = 0.0
    if globe_truth[eid].answer == 0: globe_u_drop[uid] += 1.0

for key in globe_enrollment:
    item = globe_enrollment[key]
    eid = item.eid
    uid = item.uid
    cid = item.cid
    x1 = []
    y1 = int(globe_truth[eid].answer)
    if key % 10000 == 0: print key
    # 108 维度(108)
    for index in range(4):
        if eid not in globe_uc[index]: globe_uc[index][eid] = Source_Event()
        if uid not in globe_u[index]: globe_u[index][uid] = Source_Event()
        if cid not in globe_c[index]: globe_c[index][cid] = Source_Event()
        divu = globe_uc[index][eid].div(globe_u[index][uid])
        divc = globe_uc[index][eid].div(globe_c[index][cid])
        x1.extend(globe_uc[index][eid].count)
        x1.extend(divu.count)
        x1.extend(divc.count)
    # 28 维 28 day(28)
    x1.extend(day_28[eid])
    # 此课程选课人数 (1)
    x1.append(len(globe_c_u[cid]))
    # 此人选课总数 (1)
    x1.append(len(globe_u_c[uid]))
    # 此课的放弃率
    x1.append(globe_c_drop[cid] * 1.0 / len(globe_c_u[cid]))
    # 此人的放弃率
    x1.append(globe_u_drop[uid] * 1.0 / len(globe_u_c[uid]))

    X.append(x1)
    Y.append(y1)

print "good"
sv = svm.LinearSVC()
tr = tree.DecisionTreeClassifier()
rf = ensemble.RandomForestClassifier()
gbc = ensemble.GradientBoostingClassifier()

y1 = cross_validation.cross_val_score(sv,X,Y,cv=8)
print "svm linearSVC: ",y1

y1 = cross_validation.cross_val_score(tr,X,Y,cv=8)
print "svm tree-descsion: ",y1

y1 = cross_validation.cross_val_score(rf,X,Y,cv=8)
print "randomforest :",y1

y1 = cross_validation.cross_val_score(gbc,X,Y,cv=8)
print "GradientBoostingClassifier :",y1



