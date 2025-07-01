import networkx as nx
import matplotlib.pyplot as plt
from itertools import islice
import numpy as np
import time
# np.random.seed(100) #保持每次随机数相同
start_time=time.time()
G = nx.Graph()

edges=[]
with open('4data.txt','r') as f:
    for line in f.readlines():
        edge = tuple(line.split())
        edges.append(edge)


# print(edges)
print('边总数为',len(edges))
G.add_edges_from(edges,weight=1)

def Stoer_W(G):
    cut_value = -1
    originNodes = set(G)
    originN = len(G)
    n = len(G)
    A = set()
    shousuo = []  # 每一轮都收缩最后两个点 记下来每次收缩的两个点
    globalMinCutN = -10

    while n>1:
        nodes=set(G)
        # nx.draw(G,with_labels=True)
        # plt.show()
        for item in nodes:
            G.nodes[item]['visit'] = 0
        wage = {}
        t = np.random.choice(G) #随机选一个起点
        G.nodes[t]['visit']=1
        A.add(t)
        for i in range(1,n): #i表示添加点的次数
            p=-1
            # print('i=',i,'t=',t,'wage=',wage,'n=',n)
            # print('当前t相接的',G[t].items())
            # print('A集合',A)

            for v, e in G[t].items():# v是和t相接的点，e是tv之间的权重字典
                # print('v=',v,'e=',e,'visit',G.nodes[v]['visit'])
                if G.nodes[v]['visit'] != 1:
                    # print('当前t=',t,'相接的没访问过的',v)
                    wage[v] = wage.get(v,0)+e["weight"]
                    if p == -1 or wage[v]>wage.get(p,0):
                        p=v #找到当前wage最大的点v
                #如果和t相接的点全都访问过了，那就寻找当前最大的wage[v]
            if p==-1:
                newWage={}
                for item in nodes:
                    if G.nodes[item]['visit']!=1 and wage.get(item,0)>0:
                        newWage[item] =wage[item]
                        # print('当前未找过的点是',item)
                # print('newWage',newWage)
                maxV=max(newWage,key=newWage.get)
                p=maxV

            # print('i=',i,'p=',p,type(p))
            G.nodes[p]['visit']=1   #点p是当前找到的最大wage点加到A里
            A.add(p)
            if i==n-1:  #表示添加了n-2次点 这次添加的是最后一个点T就是p 倒数第二个点S是t
                for w, e in G[p].items():
                    if w != t:
                        if w not in G[t]:
                            G.add_edge(t, w, weight=e["weight"])
                        else:
                            G[t][w]["weight"] += e["weight"]
                G.remove_node(p)
                shousuo.append((t,p))
                n=n-1

                if cut_value==-1:
                    cut_value=wage[p]
                    globalMinCutN=originN-1-n
                else:
                    if cut_value>wage[p]:
                        cut_value=min(cut_value,wage[p])
                        globalMinCutN = originN - 1 - n

            t=p
    return cut_value,originNodes,originN,shousuo,globalMinCutN,G

cut_value,originNodes,originN,shousuo,globalMinCutN,G_changed=Stoer_W(G)

Terminal=shousuo[globalMinCutN][1] #全局最小割的T点

F=nx.Graph()
if globalMinCutN==0:
    F.add_node(Terminal)
else:
    F.add_edges_from(shousuo[0:globalMinCutN])

# print(shousuo)

reachable=set(nx.single_source_shortest_path_length(F, Terminal))
partition = (list(reachable), list(originNodes - reachable))
print('全局最小割为',partition)
end_time=time.time()
time_used=end_time-start_time
print('算法用时',time_used,'秒')
nx.draw(G_changed,with_labels=True)
plt.show()


print('全局最小割值为',cut_value)
print('全局最小割出现在第',globalMinCutN+1,'次合并点时','即此时的(s,t)=',shousuo[globalMinCutN],'这个st最小割就是全局最小割')
print('所有两两合并的点的列表,前者为S，后者为T：',shousuo)
