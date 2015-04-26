#coding=utf-8
# 原始形式感知机
import os
import random


def initial():
    training_set = [[(3, 3), 1], [(4, 3), 1], [(1, 1), -1]]  # 原始数据集
    w = [0 for i in training_set[0][0]]  # 参数向量初始化
    b = 0  # bias
    n_step = 1  # 梯度下降步长
    n_sentry = 1000  # 迭代次数哨兵
    v_sentry = lambda x, y: x == 0 and not y  # cost_func 值哨兵
    error_dots = []
    return training_set, w, b, n_step, n_sentry, v_sentry, error_dots


def cost_func(w, b, training_set):
    cost = 0
    error_dots = []
    for item in training_set:
        inner_product = 0
        for idx in xrange(len(item[0])):
            inner_product = inner_product + item[0][idx]*w[idx]
        if (inner_product + b) * item[1] <= 0:
            cost += -(inner_product + b) * item[1]
            error_dots.append(item)
    return cost, error_dots


def next_step(w, b, n_step, error_dots):
    error_dot = random.choice(error_dots)
    for idx in xrange(len(error_dot)):
        w[idx] = w[idx] + n_step * error_dot[0][idx] * error_dot[1]
    b = b + n_step * error_dot[1]
    print "One Step: w %s, b %s" % (w, b)
    return w, b


def run():
    Flag = False
    training_set, w, b, n_step, n_sentry, v_sentry, error_dots = initial()
    for idx in xrange(n_sentry):
        cost, error_dots = cost_func(w, b, training_set)
        print "Cost : %s" % cost
        if v_sentry(cost, error_dots):
            Flag = True
            break
        else:
            w, b = next_step(w, b, n_step, error_dots)

    if Flag:
        print "Result w:%s  b:%s" % (w, b)
    else:
        print "The training_set is not linear separable. "

if __name__ == "__main__":
    run()
