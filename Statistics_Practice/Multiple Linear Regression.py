import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt

df = pd.read_excel('3.xls',skiprows=3,usecols="B:D",sheet_name = 0,dtype="float64")


df.columns = ['y', 'x2', 'x3']

X=np.linspace(2000, 2016, 17)
plt.plot(X,df['y'])
plt.plot(X,df['x2'])
plt.plot(X,df['x3'])
plt.show()

x = sm.add_constant(df[['x2', 'x3']]) # 生成自变量
y = df['y']    # 生成因变量
model = sm.OLS(y, x) #生成模型
result = model.fit() #模型拟合
print(result.summary())
