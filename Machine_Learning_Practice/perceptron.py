##徐潇涵 201800820149  18数据科学班

import numpy as np
import pandas as pd
from numpy import *

def preprocessdata(infile,outfile):
    fin=open(infile,"r")
    fout=open(outfile,"w")
    for s in fin:
        if(s.find('?')>-1):
            continue
        else:
            fout.write(s)
    fin.close()
    fout.close()
preprocessdata("C:/Users/xuxh/Desktop/adult.data.csv","outputfile")

# def dealdata(adult_data):
#     adult_raw = pd.read_csv(adult_data, header=None)
#     adult_raw.rename(columns={0: 'age', 1: 'workclass', 2: 'fnlwgt', 3: 'education', 4: 'education_number',
#                               5: 'marriage', 6: 'occupation', 7: 'relationship', 8: 'race', 9: 'sex',
#                               10: 'capital_gain', 11: 'apital_loss', 12: 'hours_per_week', 13: 'native_country',
#                               14: 'income'}, inplace=True)
#     target_columns = ['workclass', 'education', 'marriage', 'occupation', 'relationship', 'race', 'sex',
#                       'native_country',
#                       'income']
#     continous_colums = ['age', 'fnlwgt', 'education_number', 'capital_gain', 'apital_loss', 'hours_per_week']
# dealdata("outputfile")

#连续型变量处理['age', 'fnlwgt', 'education_number', 'capital_gain', 'apital_loss', 'hours_per_week']
f = open("outputfile")
line1 = []
for line in f.readlines():
    try:
        sample = []
        line = line.strip().split(',')
        sample.append(int(line[0]))
        sample.append(int(line[2]))
        sample.append(int(line[10]))
        sample.append(int(line[11]))
        sample.append(int(line[12]))
        line1.append(sample)
    except:
        continue
f.close()
s = np.array(line1)
min1 = np.amin(s, 0)
max1 = np.amax(s, 0)
delata = (max1 - min1) / 5

sex = [0]
age = fnlwgt = capital_gain = captial_loss= hours_per_week = [0, 0, 0, 0, 0]
#离散型变量处理['workclass', 'education', 'marriage', 'occupation', 'relationship', 'race', 'sex','native_country','income']
workclass = [' Private', ' Self-emp-not-inc', ' Self-emp-inc', ' Federal-gov', ' Local-gov', ' State-gov', ' Without-pay',' Never-worked']
education = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16']
marital_status = [' Married-civ-spouse', ' Divorced', ' Never-married', ' Separated', ' Widowed', ' Married-spouse-absent',' Married-AF-spouse']
occupation = [' Tech-support', ' Craft-repair', ' Other-service', ' Sales', ' Exec-managerial', ' Prof-specialty',' Handlers-cleaners', ' Machine-op-inspct', ' Adm-clerical', ' Farming-fishing', ' Transport-moving',' Priv-house-serv', ' Protective-serv', ' Armed-Forces']
relationship = [' Wife', ' Own-child', ' Husband', ' Not-in-family', ' Other-relative', ' Unmarried']
race = [' White', ' Asian-Pac-Islander', ' Amer-Indian-Eskimo', ' Other', ' Black']
native_country = [' United-States', ' Cambodia', ' England', ' Puerto-Rico', ' Canada', ' Germany',
           ' Outlying-US(Guam-USVI-etc)', ' India', ' Japan', ' Greece', ' South', ' China', ' Cuba', ' Iran',
           ' Honduras', ' Philippines', ' Italy', ' Polancaptial_lossd', ' Jamaica', ' Vietnam', ' Mexico', ' Portugal', ' Ireland',
           ' France', ' Dominican-Republic', ' Laos', ' Ecuador', ' Taiwan', ' Haiti', ' Columbia', ' Hungary',
           ' Guatemala', ' Nicaragua', ' Scotland', ' Thailand', ' Yugoslavia', ' El-Salvador', ' Trinadad&Tobago',
           ' Peru', ' Hong', ' Holand-Netherlands']
total = age + workclass + fnlwgt + education + marital_status + occupation + relationship + race + sex + capital_gain + captial_loss + hours_per_week + native_country + [0]
result = [0] * 124
data = []
f = open("outputfile")
for line in f.readlines():
    result = [0] * 124
    try:
        line = line.strip().split(',')
        for i in range(5):
            if int(line[0]) >= min1[0] + i * delata[0] and int(line[0]) <= min1[0] + (i + 1) * delata[0]:
                result[i] = 1
            if int(line[2]) >= min1[1] + i * delata[1] and int(line[2]) <= min1[1] + (i + 1) * delata[1]:
                result[13 + i] = 1
            if int(line[10]) >= min1[2] + i * delata[2] and int(line[10]) <= min1[2] + (i + 1) * delata[2]:
                result[67 + i] = 1
            if int(line[11]) >= min1[3] + i * delata[3] and int(line[11]) <= min1[3] + (i + 1) * delata[3]:
                result[72 + i] = 1
            if int(line[12]) >= min1[4] + i * delata[4] and int(line[12]) <= min1[4] + (i + 1) * delata[4]:
                result[77 + i] = 1
        if line[9] == ' Male':##性别记为男0女1
            result[66] = 0
        else:
            result[66] = 1
        if line[14] == ' <=50K':##将<=50k的记为-1
            result[123] = -1
        else:
            result[123] = 1##将>=50k的记为1
        result[total.index(line[1])] = 1
        result[total.index(line[4])] = 1
        result[total.index(line[5])] = 1
        result[total.index(line[6])] = 1
        result[total.index(line[7])] = 1
        result[total.index(line[8])] = 1
        result[total.index(line[13])] = 1
        data.append(result)
        print(data)
    except:
        continue

f.close()
# 将data中的数据储存到一个文档里
f = open('outputfiles1.txt', 'w')
for target in data:
    for target1 in target:
        f.write(str(target1))
        f.write(' ')
    f.write('\n')
f.close()

#保证alpha的取值
def clipAlpha(ai, H, L):
    if ai > H:
        ai = H
    elif ai < L:
        ai = L
    return ai
#随机选择第二个alpha
def selectJrand(i, n):
    j = i
    while i == j:
        j = int(random.uniform(0,n))
    return j

def Simp_smo(dataMatIn, classLabels, C, toler,max_passes):#为数据集，标签，常数c，容错率，最大的循环次数
    b=0##初始化
    passes=0
    dataMat=mat(dataMatIn)
    class_Labels=mat(classLabels).transpose()
    m,n=shape(dataMat)#m为数据的个数，n为数据的属性的个数
    alphas=mat(zeros((m,1)))
    while (passes < max_passes):
        num_changed_alphas = 0
        for i in range(m):
            ##计算误差
            fXi = int(multiply(alphas ,class_Labels).T * (dataMat * dataMat[i, :].T)) + b # 预测值
            Ei = fXi - int(classLabels[i] ) # 误差值
            if ((class_Labels[i] * Ei) < -toler and alphas[i] < C) or ((class_Labels[i] * Ei) > toler and alphas[i] > 0):
                #选择另一个alphaj，并计算预测值与真实值的差
                j = selectJrand(i, m)  # 调用辅助函数selectJrand
                fXj = float(multiply(alphas,class_Labels).T * (dataMat * dataMat[j, :].T)) + b
                Ej = fXj - class_Labels[j] # 计算误差（同第一个alpha值的误差计算方法）
                alphaoldi = alphas[i].copy()  # 复制alpha，作为alphaold
                alphaoldj= alphas[j].copy()
                if (class_Labels[i] != class_Labels[j]):  # 两个类别不一样
                    L = max(0, alphas[j] - alphas[i])#约束条件
                    H = min(C, C + alphas[j] - alphas[i])
                else:
                    L = max(0, alphas[j] + alphas[i] - C)
                    H = min(C, alphas[j] + alphas[i])
                if L == H:
                    continue
                eta = 2.0 * dataMat[i, :] * dataMat[j, :].T - dataMat[i, :] * dataMat[i, :].T - dataMat[j, :] * dataMat[j, :].T
                if eta>=0:
                    continue
                alphas[j] -= class_Labels[j] * (Ei - Ej) / eta # 未用边界条件修剪过的
                alphas[j] = clipAlpha(alphas[j], H, L)#用边界条件修剪(调用自定义函数clipAlpha)
                if (abs(alphas[j] - alphaoldj) < 0.001):
                    continue
                alphas[i] += class_Labels[j] * class_Labels[i] * (alphaoldj - alphas[j])
                b1 = b - Ei - class_Labels[i] * (alphas[i] - alphaoldi) * dataMat[i, :] * dataMat[i, :].T - \
                     class_Labels[j] * (alphas[j] - alphaoldj) * dataMat[i, :] * dataMat[j, :].T
                b2 = b - Ej - class_Labels[i] * (alphas[i] - alphaoldi) * dataMat[i, :] * dataMat[j, :].T - \
                     class_Labels[j] * (alphas[j] - alphaoldj) * dataMat[j, :] * dataMat[j, :].T
                ##阈值b的计算
                if 0 < alphas[i] and alphas[i]< C:
                    b = b1
                elif 0 < alphas[j] and alphas[j]< C:
                    b = b2
                else:
                    b = (b1 + b2) / 2
                num_changed_alphas += 1
        if num_changed_alphas == 0:
            passes += 1
        else:
            passes = 0
    return b,alphas

#通过训练集的训练，得到w值
def calculate_w(alphas, data, classLabels):#分别为 Lagrange multiplier，数据，标签
    X = mat(data)
    class_Labels= mat(classLabels)
    m,n = shape(X)
    w = zeros((n, 1))
    for i in range(m):
        w += multiply(alphas[i] * class_Labels[i], X[i, :].T)
    return w

def loadDataSet(filename):
    dataMat = []; labelMat = []
    fr = open(filename)
    for line in fr.readlines():
        lineArr = line.strip().split(' ')
        dataMat1=[]
        for i in range(123):
            dataMat1.append(int(lineArr[i]))
        dataMat.append(dataMat1)
        labelMat.append(int(lineArr[123]))
    return dataMat,labelMat

##选取1600个样本作为training set
f = open("outputfiles1.txt","r")
fw = open("1600","w")
raw_list = f.readlines()
random.shuffle(raw_list)
for i in range(1600):
    fw.writelines(raw_list[i])
fw.close()
f.close()

#选取200个样本作为test set
f = open("outputfiles1.txt","r")
fw = open("200","w")
raw_list = f.readlines()
random.shuffle(raw_list)
for i in range(200):
    fw.writelines(raw_list[i])
fw.close()
f.close()

C=0.05
max_passes=1
dataArr,labelArr = loadDataSet('1600')
b,alphas = Simp_smo(dataArr,labelArr,C,0.00001,max_passes)
f = open("outputfiles1.txt","r")
fw = open("200","w")
raw_list = f.readlines()
random.shuffle(raw_list)
for i in range(200):
    fw.writelines(raw_list[i])
fw.close()
f.close()
#print(alphas)
w=calculate_w(alphas,dataArr,labelArr)
wtw=np.dot(w.T,w)
cost=wtw/2+C*sum(C-alphas)
f=open('200','r')
k=0
for line in f.readlines():
    line=line.strip().split(' ')
    line1=[]
    line2=[]
    for i in range(123):
        line1.append(int(line[i]))
    line2.append(int(line[123]))
    if (np.dot(w.T,line1)+b)*line2<0:
        k=k+1
f.close()
print('C={},max_passes={},ww^T={},cost={},number of mis-labeled s={}'.format(C,max_passes,wtw,cost,k))
