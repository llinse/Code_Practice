import statsmodels.api as sm
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

data7 = pd.read_excel('data.xlsx', sheet_name='Sheet7')
X = np.log(data7.loc[:,[ '从事农业经营的纯收入X1', '其他来源纯收入X2']])
Y = np.log(data7["人均消费支出Y"])
X = sm.add_constant(X)
fit = sm.OLS(Y,X).fit()
print(fit.summary())

plt.figure(figsize=(12,8))
plt.scatter(X["其他来源纯收入X2"],np.power(fit.predict(X)-Y,2))
fit.predict(X)
plt.title("异方差性检验图",fontsize=16)
plt.show()

