### 徐潇涵 201800820149
### 按目标函数求解最小值进行编写，求最大值时输入矩阵应手动变换

from numpy import *
import prettytable as pt

class mytwophase:
    def __init__(self,r,b,c,N,z):
        self.r = r # 第一阶段目标函数系数
        self.b = b # 第二阶段目标函数系数
        self.c = c # 约束方程解
        self.N = N # 加入松弛变量后的约束条件矩阵
        self.z = z # （r）最终解

    def estimate(self,b):
        b1 = where(b > 0, 1,where(b < 0,-1, 0))
        if 1 in b1:
                return True

    def definition1(self,r,c):
        x = len(r)
        y = len(c)
        k1 = [k for k in range(x) if r[k] == 0]
        k2 = [k for k in range(x) if r[k] != 0]
        a = []
        a1 = []  # 原有变量
        a2 = []  # 手动松弛变量
        m=0
        n=0
        for i in range(x):
            if i in k1:
                m = m + 1
                a.append("x%s" % m)
            elif i in k2:
                n = n + 1
                a.append("R%s" % n)
        a1=a[0:len(r)-len(c)]
        a2=a[len(r)-len(c):len(r)+1]  # 松弛变量
        return x,y,k1,k2,a1,a2,a

    def definition2(self,b,c):
        x = len(b)
        y = len(c)
        a1 = []  # 非基变量
        for i in range(1, 1 + x - y):
            a1.append("x%s" % i)
        a2 = []  # 基变量
        for i in range(1, 1 + y):
            a2.append("s%s" % i)
        a = ["基"] + a1 + a2
        return x,y,a1,a2,a

    def Iteration1(self,r,c,N,z,a,a1,a2):
        x = len(r)
        y = len(c)
        k1 = [k for k in range(x) if r[k] == 0]
        k2 = [k for k in range(x) if r[k] != 0]
        jud=zeros(y)
        en=[]
        ou=[]
        while self.estimate(r):
            ent=int(argmax(r)) # 进基变量下标，对应列
            en.append(ent)
            # 判断解与进基列比例大小
            for i in range(y):     # 分母为负不考虑
                if N[i,ent]!=0:
                    jud[i] = c[i] / N[i, ent]
                else:
                    jud[i]=100
            for j in jud:      # 分母为零不考虑
                if j < 0 :
                    jud[where(jud == j)] = 100
            out=int(argmin(jud)) #离基变量下标，对应行
            ou.append(out)

            ai=a2[out]
            a2[out]=a1[ent]
            a1[ent]=ai

            c[out]=c[out]/N[out,ent] # 解要先于矩阵进行更新
            N[out,:]=N[out,:]/N[out,ent]  # 枢纽行更新
            m=[i for i in range(0,y)]
            del m[out]
            for i in m:
                c[i]=c[i]-N[i,ent]*c[out]
                N[i,:]=N[i,:]-N[i,ent]*N[out,:]
            z = z - r[ent] * c[out]
            r=r-r[ent]*N[out,:]

            for i in range(y) :
                for j in range(x) :
                    N[i,j]=round(N[i,j],4)
            for i in range(x):
                r[i]=round(r[i],4)
            for i in range(y):
                c[i]=round(c[i],4)
            z=round(z,4)
            # ri=["z"]+list(r)

        return N,c,r,z,a,a1,a2,en,ou

    def Iteration2(self, b, c, N, z, a, a1, a2):
        x = len(b)
        y = len(c)
        jud = zeros(y)
        en = []
        ou = []
        while self.estimate(b):
            ent = int(argmax(b))  # 进基变量下标，对应列
            en.append(ent)
            # 判断解与进基列比例大小
            for i in range(y):  # 分母为负不考虑
                if N[i, ent] != 0:
                    jud[i] = c[i] / N[i, ent]
                else:
                    jud[i] = 100
            for j in jud:  # 分母为零不考虑
                if j < 0:
                    jud[where(jud == j)] = 100
            out = int(argmin(jud))  # 离基变量下标，对应行
            ou.append(out)
            # ai = a2[out]
            a2[out] = a1[ent]
            # a1[ent] = ai

            c[out] = c[out] / N[out, ent]  # 解要先于矩阵进行更新
            N[out, :] = N[out, :] / N[out, ent]  # 枢纽行更新
            m = [i for i in range(0, y)]
            del m[out]
            for i in m:
                c[i] = c[i] - N[i, ent] * c[out]
                N[i, :] = N[i, :] - N[i, ent] * N[out, :]
            z = z - b[ent] * c[out]
            b = b - b[ent] * N[out, :]

            for i in range(y):
                for j in range(x):
                    N[i, j] = round(N[i, j], 4)
            for i in range(x):
                r[i] = round(r[i], 4)
            for i in range(y):
                c[i] = round(c[i], 4)
            z = round(z, 4)
        return N, c, b, z, a, a1, a2, en, ou

    def main(self,r,b,c,N,z):
        x, y, k1,k2,a1, a2,a = self.definition1(r, c)
        print("-------------------------")
        print("第一阶段初始表格为")
        ai = ["基"] + a
        ri = ["z"] + list(r)
        tb = pt.PrettyTable()
        tb.field_names = ai
        tb.add_row(ri)
        for i in range(y):
            col = [a2[i]] + list(N[i, :])
            tb.add_row(col)
        ci = [z] + list(c)
        tb.add_column('解', ci)
        print(tb)
        count=0
        for x in r:
            if x != 0:
                r=r+N[count,:]
                z=z+c[count]
                count += 1
        N,c,r,z,a,a1,a2,en,ou=self.Iteration1(r,c,N,z,a,a1,a2)

        print("-------------------------")
        print("第一阶段最优表格为")
        ai=["基"]+a
        ri = ["z"] + list(r)
        tb = pt.PrettyTable()
        tb.field_names = ai
        tb.add_row(ri)
        for i in range(y):
            col=[a2[i]]+list(N[i,:])
            tb.add_row(col)
        ci=[z]+list(c)
        tb.add_column('解',ci)
        print(tb)
        print("第一阶段最优解为", z)
        print("基本可行解分别为", [ai[i+1] for i in en])
        print("对应最优值分别为",[c[i] for i in ou])

        N2=full((len(c),len(k1)),0.)
        m=0
        for i in k1:
            N2[:,m]=N[:,i]
            m=m+1
        count=0
        for x in r:
            if x != 0:
                z = z - b[count] * c[count]
                b=b-b[count]*N2[count,:]
                count+=1
        a1=[]
        for i in k1:
            a1.append(a[i])

        print("-------------------------")
        print("第二阶段初始单纯形表格为")
        ai=["基"]+a1
        bi = ["z"] + list(b)
        tb = pt.PrettyTable()
        tb.field_names = ai
        tb.add_row(bi)
        for i in range(y):
            col=[a2[i]]+list(N2[i,:])
            tb.add_row(col)
        ci=[z]+list(c)
        tb.add_column('解',ci)
        print(tb)

        N2,c,b,z,a,a1,a2,en,ou = self.Iteration2(b,c,N2,z,a,a1,a2)
        print("-------------------------")
        print("第二阶段最优表格为")
        ai=["基"]+a1
        bi = ["z"] + list(b)
        tb = pt.PrettyTable()
        tb.field_names = ai
        tb.add_row(bi)
        for i in range(y):
            col=[a2[i]]+list(N2[i,:])
            tb.add_row(col)
        ci=[z]+list(c)
        tb.add_column('解',ci)
        print(tb)
        print("第二阶段最优解为", z)
        print("基本可行解分别为", [ai[i+1] for i in en])
        print("对应最优值分别为",[c[i] for i in ou])

if __name__ == "__main__":
    r = array([0.,0.,0.,-1.,-1.,0.])
    b = array([-4.,-1.,0.,0.])
    c = array([3., 6., 4.])
    N = array([[3., 1., 0., 1., 0., 0.], [4., 3., -1., 0., 1., 0.], [1., 2., 0., 0., 0., 1.]])
    z = 0
    twophase = mytwophase(r,b,c,N,z)
    twophase.main(r,b,c,N,z)
