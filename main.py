import json
import time
from Novel import Novel
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import requests
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
# 创建数据库连接
engine = create_engine("mysql+mysqlconnector://root:123456@127.0.0.1/crawler?charset=utf8mb4")
Session = sessionmaker(bind=engine)
session = Session()


headers = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,ja;q=0.6,und;q=0.5',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Cookie': '_ga=GA1.1.506110502.1713323082; _ga_4BC3P9JVX3=GS1.1.1713335374.2.0.1713335374.60.0.591288986',
    'Referer': 'https://www.uaa003.com/novel',
    'Sec-Ch-Ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
    'Sec-Ch-Ua-Mobile': '?1',
    'Sec-Ch-Ua-Platform': '"Android"',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'Token': '',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Mobile Safari/537.36'
}
# 爬取小说数据并插入数据库
url = 'https://www.uaa003.com/api/novel/app/novel/search'
params = {
    'category': '',
    'excludeTags': '',
    'orderType': 2,
    'searchType': 1,
    'page': 1,
    'size': 40
}

# 获取第一页数据，以确定总页数
response = requests.get(url, params=params, headers=headers)
content = response.content.decode('utf-8')

# 将解压缩后的数据转换为字符串
print(f'status code: {response.status_code}, response: {content}')
data = json.loads(content)['model']
total_pages = data['totalPage']

count = 0
last_processed_page = 0  # 上次处理的页数，用于断点继续
def exist(novel_id):
    return session.query(Novel).filter_by(id=novel_id).first() is not None
# 将失败
# 遍历所有页面并请求数据
def fetch_data(url, params, total_pages, session):
    global count, last_processed_page

    # 遍历所有页面并请求数据
    for page in range(last_processed_page + 1, total_pages + 1):
        params['page'] = page
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()['model']['data']
            for novel_data in data:
                novel = Novel(
                    id=novel_data['id'],
                    title=novel_data['title'],
                    authors=novel_data['authors'],
                    brief=novel_data['brief'],
                    categories=novel_data['categories'],
                    tags=novel_data['tags'],
                    wordCount=novel_data['wordCount'],
                    pornRate=novel_data['pornRate'],
                    collectCount=novel_data['collectCount'],
                    latestUpdate=novel_data['latestUpdate'],
                    updateTime=novel_data['updateTime'],
                    createTime=novel_data['createTime']
                )
                if exist(novel.id):
                    continue
                session.add(novel)
                count += 1
            session.commit()
            last_processed_page = page  # 更新上次处理的页数
            if page % 10 == 0:
                logging.info(f'Fetching data from page {page}...')
        else:
            logging.error(f'Failed to fetch data from page {page}, status code: {response.status_code}, response: {response.text}')
            # 重试机制，这里可以根据实际情况设置重试逻辑
            # time.sleep(1)  # 增加重试间隔时间

        time.sleep(1)  # 控制请求频率

    logging.info(f'Finished fetching data, total count: {count}')

# 使用示例
fetch_data(url, params, total_pages, session)

# 关闭会话
session.close()
