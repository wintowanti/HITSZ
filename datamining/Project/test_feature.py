from util_y import *
from path_y import *
from basic_y import *
from load_y import *

def get_feature():
    global_date = load_date(path_date)
    global_enrollment = load_enrollment(path_test_enrollment)
    global_log = load_log(path_train_log_process)
    global_truth = load_truth(path_train_truth)
    global_object_vector = load_object_vector()


