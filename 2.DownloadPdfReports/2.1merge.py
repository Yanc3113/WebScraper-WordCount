import pandas as pd

# pd.set_option('max_columns', 100)
# pd.set_option('max_colwidth', 100)

# df1=pd.read_excel('./aim_data.xlsx',dtype={'code':str})  # 读取目标数据
# df2=pd.read_excel('./all_url_data.xlsx',dtype={'code':str}) # 读取所有数据

# df3=pd.merge(df1,df2,on=['code','year'],how='left') 

# df4=df3.loc[:,['code','firm','year','pdf_url']] 
# df4.to_excel('./merged_data.xlsx',index=False) # 保存数据

# print(df4)

import pandas as pd

# 读取目标公司列表（目标是匹配年报链接）
df1 = pd.read_csv('./aim_data.csv', dtype={'code': str})

# 读取所有公司年报链接数据（已清洗）
df2 = pd.read_csv('./all_url_data.csv', dtype={'code': str})

# 合并：按 code 和 year 进行左连接
df3 = pd.merge(df1, df2, on=['code', 'year'], how='left')

# 提取关心的字段
df4 = df3.loc[:, ['code', 'firm', 'year', 'pdf_url']]

# 保存为 CSV，utf-8-sig 保证 Excel 兼容
df4.to_csv('./merged_data.csv', index=False, encoding='utf-8-sig')

# 打印结果并显示公司数量
print(df4)
print(f"共匹配到 PDF 的公司记录数：{df4['pdf_url'].notna().sum()} 条")
print(f"涉及公司数量：{df4['code'].nunique()} 家")
