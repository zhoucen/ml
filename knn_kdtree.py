#coding=utf-8
import os
import math
import collections


class KdNode(object):
    """docstring for KdNode"""
    def __init__(self, train_set):
        super(KdNode, self).__init__()
        self.train_set = train_set
        self.dot = None
        self.dimension = None
        self.left_set = None
        self.left_num = None
        self.left = None
        self.right_set = None
        self.right_num = None
        self.right = None
        self._build()

    def _build(self):
        self._decide_dimension()
        self._split()

    def _decide_dimension(self):
        dim_list = []
        for idx in range(len(self.train_set[0][0])):
            var = self._variance([i[0][idx] for i in self.train_set])
            dim_list.append((idx,var))
        self.dimension = sorted(dim_list, cmp=lambda x,y:cmp(x[1], y[1]))[-1][0]

    def _split(self):
        sort_set =  sorted(self.train_set, cmp=lambda x,y:cmp(x[0][self.dimension], y[0][self.dimension]))
        self.dot = sort_set[len(sort_set)/2]
        self.left_set = sort_set[:len(sort_set)/2]
        self.left_num = len(self.left_set)
        if self.left_set:
            self.left = KdNode(self.left_set)
        self.right_set = sort_set[len(sort_set)/2+1:]
        self.right_num = len(self.right_set)
        if self.right_set:
            self.right = KdNode(self.right_set)

    def _variance(self, data):
        mean = sum(data)/len(data)
        variance = sum([(i - mean)**2 for i in data])/len(data)
        return variance

    def is_leaf(self):
        if self.right or self.left:
            return False
        else:
            return True

    def __repr__(self):
        return str(self.dot)


class KdTree(object):
    """docstring for KdTree"""
    def __init__(self, train_set):
        super(KdTree, self).__init__()
        self.root = KdNode(train_set)

    def search(self, dot, k, dist):
        near_list = []
        for i in range(k):
            search_tack = []
            loc = self.root
            nearest_dot = loc
            nearest_distance = dist(dot, loc.dot[0])
            while loc:  # 遍历得到search_stack
                search_tack.append(loc)
                if dist(dot, loc.dot[0]) < nearest_distance:
                    nearest_dot = loc
                    nearest_distance = dist(dot, loc.dot[0])
                else:
                    if dot[loc.dimension] <= loc.dot[0][loc.dimension]:
                        loc = loc.left
                    else:
                        loc = loc.right

            while search_tack:
                item = search_tack.pop()
                if dist(dot, item.dot[0]) < nearest_distance:  # 更新最邻近点
                    nearest_dot = item
                    nearest_distance = dist(dot, item.dot[0])

                if not item.dimension:
                    continue

                if abs(dot[item.dimension] - item.dot[0][item.dimension]) < nearest_distance:
                    if dot[item.dimension] <= nearest_dot.dot[0][nearest_dot.dimension]:
                        if item.left:
                            search_tack.append(item.left)
                    else:
                        if item.right:
                            search_tack.append(item.right)
                else:
                    if item.left:
                        search_tack.append(item.left)
                    if item.right:
                        search_tack.append(item.right)

            near_list.append(nearest_dot)


def initial():
    train_set = [((2, 3), 0), ((5, 4), 0), ((9, 6), 1), ((4, 7), 0), ((8, 1), 1), ((7, 2), 1)]  # 原始数据集
    k = 1  # 最靠近的k个近邻有投票权
    dist = Euclidean_dist  # 距离计算函数
    dot = (8, 1.9)  # 需要预测的点
    kd_tree = KdTree(train_set)  # Kd Tree
    return train_set, k, dist, dot, kd_tree


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
    train_set, k, dist, dot, kd_tree = initial()
    kd_tree.search(dot, k, dist)


if __name__ == '__main__':
    main()