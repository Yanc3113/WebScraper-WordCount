import pandas as pd
import requests
import os

# ===== 配置参数 =====
root = './ReportPDF'               # 存放 PDF 的目录
data_path = './all_url_data.csv'   # 数据路径
start_row = 1                      # 从第几行开始（从0起算）
end_row = 100                      # 到第几行结束（包含）
# =====================

# 读取数据
df = pd.read_csv(data_path, dtype={'code': str})

# 选取范围
df_range = df.iloc[start_row:end_row + 1]  # 注意包含 end_row

# 创建错误日志列表
errors = []

# 遍历选定范围的数据行
for idx, row in df_range.iterrows():
    try:
        code = row['code']
        firm = row.get('secName', '未知公司')
        year = str(row['year'])
        pdf_url = row['pdf_url']

        # 构造路径
        dir_name = f"{code}-{firm}"
        pdf_name = f"{year}年度报告"
        dir_path = os.path.join(root, dir_name)
        pdf_path = os.path.join(dir_path, pdf_name + '.pdf')

        os.makedirs(dir_path, exist_ok=True)

        # 下载 PDF
        response = requests.get(pdf_url, timeout=15)
        response.raise_for_status()
        with open(pdf_path, 'wb') as f:
            f.write(response.content)

        print(f'✅ 已下载：{pdf_path}')

    except Exception as e:
        print(f'❌ 下载失败：{code}-{firm}-{year}')
        errors.append({
            'code': code,
            'firm': firm,
            'year': year,
            'pdf_url': pdf_url,
            'error': str(e)
        })

# 保存错误信息
if errors:
    error_df = pd.DataFrame(errors)
    error_df.to_csv('error_log.csv', index=False, encoding='utf-8-sig')
    print(f'\n⚠️ 共 {len(errors)} 个文件下载失败，错误日志已保存至 error_log.csv')
else:
    print('\n✅ 全部下载成功，没有出错。')
