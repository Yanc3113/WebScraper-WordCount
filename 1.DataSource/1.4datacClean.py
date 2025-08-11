# import pandas as pd


# # pd.set_option('max_columns', 100)
# # pd.set_option('max_colwidth', 100)
# df=pd.read_csv('ndbg_data.csv',dtype={'code':'str'},encoding='utf-8')
# # 删除摘要和已取消的
# df = df.drop(df[df['announcementTitle'].str.contains('摘要',regex=False)==True].index)
# df = df.drop(df[df['announcementTitle'].str.contains('取消',regex=False)==True].index)
# df = df.drop(df[df['announcementTitle'].str.contains('公告',regex=False)==True].index)
# df = df.drop(df[df['announcementTitle'].str.contains('英文',regex=False)==True].index)
# df = df.drop(df[df['announcementTitle'].str.contains(r'[a-zA-Z]',regex=True)==True].index)#英文标题
# df = df.drop(df[df['code'].str.contains('code',regex=False)==True].index)#删除上一步骤多写进去的标题
# #提取年份
# df['year']=df['announcementTitle'].str.extract(r'(\d{4}年)', expand=False)
# #保留最新一次更新的年报
# df=df.drop_duplicates(['code','year'],keep='first')
# print('正在保存,请稍等')
# df.to_excel('all_url_data.xlsx',index=False)
# print(df)

import pandas as pd

# 读取 CSV 文件
df = pd.read_csv('ndbg_data.csv', dtype={'code': 'str'}, encoding='utf-8')

# 删除摘要、取消、公告、英文等无效年报
df = df.drop(df[df['announcementTitle'].str.contains('摘要', regex=False)].index)
df = df.drop(df[df['announcementTitle'].str.contains('取消', regex=False)].index)
df = df.drop(df[df['announcementTitle'].str.contains('公告', regex=False)].index)
df = df.drop(df[df['announcementTitle'].str.contains('英文', regex=False)].index)
df = df.drop(df[df['announcementTitle'].str.contains(r'[a-zA-Z]', regex=True)].index)
df = df.drop(df[df['code'].str.contains('code', regex=False)].index)  # 删除误写入的表头

# 提取年份（如 2024年 → 2024）
df['year'] = df['announcementTitle'].str.extract(r'(\d{4})年', expand=False)

# 按公司和年份去重，保留最新一次更新
df = df.drop_duplicates(['code', 'year'], keep='first')

# 输出为 CSV
print('saving all_url_data.csv, please wait...')
df.to_csv('all_url_data.csv', index=False, encoding='utf-8-sig')  # 避免中文乱码
print(df)
print(df["code"].nunique())