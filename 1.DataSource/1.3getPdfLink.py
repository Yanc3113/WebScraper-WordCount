import requests
import time
import csv
import random
import pandas as pd
import openpyxl
import math
import os


csv_path = "firm_message.csv"  
output_csv = "ndbg_data.csv"
error_xlsx = "error.xlsx"
date_range = '2000-01-01~2025-07-31'
# start, end = 2, 100  # change it by yourself (iy means the range of the "firm_message.csv" )
start, end = 101, 400  # change it by yourself (iy means the range of the "firm_message.csv" )



url = 'http://www.cninfo.com.cn/new/hisAnnouncement/query'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    'Referer': 'http://www.cninfo.com.cn/',
    'Origin': 'http://www.cninfo.com.cn',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'X-Requested-With': 'XMLHttpRequest',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
}

# === Step 0: 加载数据 ===
df = pd.read_csv(csv_path, dtype={'code': str})
print(f"Successfully loading {len(df)} companies")

# === Step 1: 获取页数 ===
def get_pages(code, orgId):
    data = {
        'pageNum': '1',
        'pageSize': '30',
        'column': 'szse',
        'tabName': 'fulltext',
        'stock': f'{code},{orgId}',
        'category': 'category_ndbg_szsh',
        'seDate': date_range,
        'isHLtitle': 'true'
    }
    resp = requests.post(url, headers=headers, data=data)
    resp.encoding = resp.apparent_encoding
    total = resp.json().get('totalAnnouncement', 0)
    return math.ceil(total / 30)


if not os.path.exists(error_xlsx):
    openpyxl.Workbook().save(error_xlsx)
wb = openpyxl.load_workbook(error_xlsx)
ws = wb.active

if not os.path.exists(output_csv):
    with open(output_csv, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['code', 'secName', 'orgId', 'announcementId', 'announcementTitle', 'pdf_url'])

with open(output_csv, 'a', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    for i in range(start-2, end-1):
        row = df.iloc[i]
        code, orgId, zwjc = row['code'], row['orgId'], row['zwjc']
        try:
            pages = get_pages(code, orgId)
            for page in range(1, pages + 1):
                print(f"📘 {zwjc}（{code}）第 {page}/{pages} 页")
                data = {
                    'pageNum': str(page),
                    'pageSize': '30',
                    'column': 'szse',
                    'tabName': 'fulltext',
                    'stock': f'{code},{orgId}',
                    'category': 'category_ndbg_szsh',
                    'seDate': date_range,
                    'isHLtitle': 'true'
                }
                r = requests.post(url, headers=headers, data=data)
                announcements = r.json().get("announcements", [])
                for ann in announcements:
                    title = ann['announcementTitle']
                    if any(keyword in title for keyword in ['摘要', '说明', '公告', '英文']):
                        continue
                    pdf_url = 'http://static.cninfo.com.cn/' + ann['adjunctUrl']
                    writer.writerow([code, ann['secName'], orgId, ann['announcementId'], title, pdf_url])
                time.sleep(random.uniform(0.1, 0.5))
        except Exception as e:
            print(f"Error：{code} - {e}")
            ws.append([f'{code} Error：{str(e)}'])
            wb.save(error_xlsx)

print("All done!!!")
