import random
import copy
import time
from math import *
import networkx as nx
import matplotlib.pyplot as plt

def contract(ver, e):
    while len(ver) > 2:
        # G = nx.MultiGraph()
        # G.add_nodes_from(ver)
        # G.add_edges_from(e)
        # nx.draw_networkx(G,node_color='pink')
        # plt.show()

        ind = random.randrange(0, len(e))
        [u,v] = e.pop(ind)  # pick a edge randomly
        ver.remove(v)  # remove v from vertices
        newEdge = []
        for i in range(len(e)):
            if e[i][0] == v:
                e[i][0] = u
            elif e[i][1] == v:
                e[i][1] = u
            if e[i][0] != e[i][1]: newEdge.append(e[i])  # remove self-loops
        e = newEdge
    # G = nx.MultiGraph()
    # G.add_nodes_from(ver)
    # G.add_edges_from(e)
    # nx.draw_networkx(G,node_color='pink')
    # plt.show()
    return (len(e),e)  # return the number of the remained edges and the remained edges


if __name__ == '__main__':
    # f = open('BenchmarkNetwork.txt')
    # f = open('Corruption_Gcc.txt')
    # f = open('PPI_gcc.txt')
    # f = open('RodeEU_gcc.txt')
    # f = open('Crime_Gcc.txt')
    f = open('4data.txt')

    _f = list(f)
    edges = []
    vertices = []
    for i in range(len(_f)):
        s = _f[i].split()
        vertices.append(int(s[0]))
        vertices.append(int(s[1]))
        vertices = list(set(vertices))
        edges.append([int(s[0]), int(s[1])])
    n=len(vertices)
    # n=int((n^2)*log(n))  # 循环次数
    print(n)

    result1 = []
    result2 = []
    start = time.time()
    for i in range(n):
        v = copy.deepcopy(vertices)
        e = copy.deepcopy(edges)
        rl,re = contract(v, e)
        result1.append(rl)
        result2.append(re)
    r=result1.index(min(result1))
    end = time.time()
    print("全局最小割值：",min(result1))
    print("s,t:",result2[r])
    print("运行时间:",end-start)

