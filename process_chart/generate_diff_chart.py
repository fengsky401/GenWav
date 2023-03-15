import pandas as pd

# 读取表A和表B
df_a = pd.read_excel('03_14_500Hz_new_data.xlsx')
df_b = pd.read_excel('0818_True_倍频程T60.xlsx')

# 剔除表A中已经出现在表B中的行数据
df_c = df_a[~df_a.isin(df_b)].dropna()

# 将表A中出现而表B中没出现的行数据保存到表C中
df_c.to_excel('table_c.xlsx', index=False)
