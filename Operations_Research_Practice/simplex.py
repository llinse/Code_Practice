### 徐潇涵 201800820149
### 按目标函数求解最大值进行编写，求最小值时输入矩阵应手动变换

from numpy import *
import prettytable as pt

class mysimplex:
    def __init__(self,b,c,N):
        self.b = b # 目标函数系数
        self.c = c # 约束方程解
        self.N = N # 加入松弛变量后的约束条件矩阵

    def estimate(self,b):
        b1 = where(b < 0, 1,where(b > 0,-1, 0))
        if 1 in b1:
                return True

    def definition(self,b,c):
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

    def Iteration(self,b,c,N):
        x,y,a1,a2,a=self.definition(b,c)
        jud=zeros(y)
        z=0
        en=[]
        ou=[]
        while self.estimate(b):
            ent=int(argmin(b)) # 进基变量下标，对应列
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
            z = z - b[ent] * c[out]
            b=b-b[ent]*N[out,:]

            for i in range(y) :
                for j in range(x) :
                    N[i,j]=round(N[i,j],4)
            for i in range(x):
                b[i]=round(b[i],4)
            for i in range(y):
                c[i]=round(c[i],4)
            z=round(z,4)
            bi=["z"]+list(b)

            tb = pt.PrettyTable()
            tb.field_names = a
            tb.add_row(bi)
            for i in range(y):
                col=[a2[i]]+list(N[i,:])
                tb.add_row(col)
            ci=[z]+list(c)
            tb.add_column('解',ci)
            print(tb)

        print("最优解为", z)
        print("对应的决策变量分别为", [a[i+1] for i in en])
        print("决策变量最优值分别为",[c[i] for i in ou])
        return N,c,b,z

if __name__ == "__main__":
    b = array([-5.,-4.,0.,0.,0.,0.])
    c = array([24., 6., 1., 2.])
    N = array([[6., 4., 1., 0., 0., 0.], [1., 2., 0., 1., 0., 0.], [-1., 1., 0., 0., 1., 0.] ,[ 0., 1., 0., 0., 0., 1.]])
    simplex = mysimplex(b,c,N)
    simplex.Iteration(b,c,N)
