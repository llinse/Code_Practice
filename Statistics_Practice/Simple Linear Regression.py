import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt

df = pd.read_excel('2.xlsx',skiprows=3,usecols="D:E",sheet_name = 2,dtype="float64")

df.columns = ['y', 'x']

x = df['x']
y = df['y']

plt.scatter(x, y)
plt.show()

model = sm.OLS(y, x) #生成模型
result = model.fit() #模型拟合
print(result.summary())
