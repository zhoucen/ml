#coding=utf-8
import os
import math
import collections


def initial():
    train_set = [((2, 3), 0), ((5, 4), 0), ((9, 6), 1), ((4, 7), 0), ((8, 1), 1), ((7, 2), 1)]  # 原始数据集
    k = 2  # 最靠近的k个近邻有投票权
    dist = Euclidean_dist  # 距离计算函数
    dot = (8, 2)  # 需要预测的点
    return train_set, k, dist, dot


def Euclidean_dist(dotA, dotB):
    distance = 0
    for idx, item in enumerate(dotA):
        distance = distance + math.pow(dotB[idx] - dotA[idx], 2)
    return math.sqrt(distance)


def KNN(train_set, k, dist, dot):
    dist_list = []
    for t_dot in train_set:
        dist_list.append([t_dot[0],t_dot[1],dist(dot, t_dot[0])])
    top_k = sorted(dist_list, cmp=lambda x,y:cmp(x[2], y[2]))[:k]
    category = collections.Counter([ k[1] for k in top_k]).most_common(1)[0][0]
    print "%s is %s" % (dot, category)


def main():
    train_set, k, dist, dot = initial()
    KNN(train_set, k, dist, dot)


if __name__ == '__main__':
    main()