import requests
import time

# 固定测试参数
code = "000001"
orgId = "gssz0000001"
date = "2000-01-01~2025-07-31"

url = "http://www.cninfo.com.cn/new/hisAnnouncement/query"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    'Referer': 'http://www.cninfo.com.cn/',
    'Origin': 'http://www.cninfo.com.cn',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'X-Requested-With': 'XMLHttpRequest',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
}

# 构造请求体
data = {
    'pageNum': '1',
    'pageSize': '30',
    'column': 'szse',
    'tabName': 'fulltext',
    'plate': '',
    'stock': f'{code},{orgId}',
    'searchkey': '',
    'secid': '',
    'category': 'category_ndbg_szsh',  # 年报
    'trade': '',
    'seDate': date,
    'sortName': '',
    'sortType': '',
    'isHLtitle': 'true'
}

# 发送请求
response = requests.post(url=url, headers=headers, data=data)
response.encoding = response.apparent_encoding
json_data = response.json()

# 提取公告
announcements = json_data.get("announcements", [])

# 打印前几条结果
if announcements:
    print(f"getting {len(announcements)} reports (page 1)")
    for i, item in enumerate(announcements[:5]):
        title = item["announcementTitle"]
        pdf_url = "http://static.cninfo.com.cn/" + item["adjunctUrl"]
        print(f"\n[{i+1}] {title}\n📄 {pdf_url}")
else:
    print("No reports at all. plz check your orgId / code / time .")
