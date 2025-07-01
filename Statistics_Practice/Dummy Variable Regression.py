import statsmodels.api as sm
import pandas as pd

data3 = pd.read_excel('data.xlsx', sheet_name='Sheet3')
fit3 = sm.formula.ols(formula='生活消费 ~ 工资收入 + 其他收入 + C(农村or城镇)', data=data3).fit()
print(fit3.summary())




