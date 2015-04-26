#coding=utf-8
# 对偶形式感知机
import os
import random


def initial():
    training_set = [[(3, 3), 1], [(4, 3), 1], [(1, 1), -1]]  # 原始数据集
    w = [0 for i in training_set[0][0]]  # 参数向量初始化
    alpha = [0 for i in training_set]  # 中间向量初始化
    b = 0  # bias
    n_step = 1  # 梯度下降步长
    n_sentry = 1000  # 迭代次数哨兵
    v_sentry = lambda x, y: x == 0 and not y  # cost_func 值哨兵
    error_dots = []  # 误分类点集合
    gram_set = Gram(training_set)  # Gram 矩阵，因为我使用的cost_func哨兵不太一样。所以这个东西没用上。
    return training_set, w, alpha, b, n_step, n_sentry, v_sentry, error_dots, gram_set


def _inner(va, vb):
    res = 0
    for idx in range(len(va)):
        res = res + va[idx] * vb[idx]
    return res


def Gram(training_set):
    gram_set = [[0 for i in training_set ] for i in training_set]
    for r_idx, row in enumerate(gram_set):
        for c_idx, col in enumerate(row):
            gram_set[r_idx][c_idx] = _inner(training_set[r_idx][0], training_set[c_idx][0])
    return gram_set


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


def next_step(w, alpha, b, n_step, training_set):

    error_dot_idxs = []
    for i, item in enumerate(training_set):
        inner_product = 0
        for idx in xrange(len(item[0])):
            inner_product = inner_product + item[0][idx]*w[idx]
        if (inner_product + b) * item[1] <= 0:
            error_dot_idxs.append(i)
    error_dot_idx = random.choice(error_dot_idxs)
    alpha[error_dot_idx] = alpha[error_dot_idx] + n_step
    b = b + n_step * training_set[error_dot_idx][1]
    for idx in range(len(w)):
        w[idx] = 0
        for i in range(len(alpha)):
            w[idx] = w[idx] + alpha[i] * training_set[i][0][idx] * training_set[i][1]
    print "One Step: w %s, b %s, alpha: %s" % (w, b, alpha)
    return w, alpha, b


def run():
    Flag = False
    training_set, w, alpha, b, n_step, n_sentry, v_sentry, error_dots, gram_set = initial()
    for idx in xrange(n_sentry):
        cost, error_dots = cost_func(w, b, training_set)
        print "Cost : %s" % cost
        if v_sentry(cost, error_dots):
            Flag = True
            break
        else:
            w, alpha, b = next_step(w, alpha, b, n_step, training_set)

    if Flag:
        print "Result w:%s  b:%s  alpha: %s" % (w, b, alpha)
    else:
        print "The training_set is not linear separable. "

if __name__ == "__main__":
    run()
