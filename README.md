# 小说爬虫模板

## 项目介绍
本项目是一个小说数据爬虫程序，通过访问指定的API接口，获取小说数据并存储到MySQL数据库中。

## 功能特点
- 从API接口获取小说数据
- 解析并保存数据到MySQL数据库
- 支持分页抓取，断点续传
- 日志记录抓取过程中的信息和错误

## 依赖环境
- Python 3.x
- requests
- SQLAlchemy
- mysql-connector-python
- logging

## 安装步骤

1. 克隆或下载项目到本地
    ```sh
    git clone https://github.com/yourusername/novel-crawler.git
    cd novel-crawler
    ```

2. 安装所需的Python包
    ```sh
    pip install -r requirements.txt
    ```

3. 配置数据库连接
    修改 `main.py` 文件中的数据库连接字符串，确保与本地数据库配置一致：
    ```python
    engine = create_engine("mysql+mysqlconnector://<username>:<password>@<host>/<database>?charset=utf8mb4")
    ```

## 使用方法

1. 初始化数据库
    可以运行 test.ipynb 创建表，可以参考 `Novel` 类的定义：
    ```python
    class Novel(Base):
        __tablename__ = 'novels_collect'

        id = Column(String(255), primary_key=True)
        title = Column(String(255))
        authors = Column(String(255))
        brief = Column(Text)
        categories = Column(String(255))
        tags = Column(String(255))
        wordCount = Column(Integer)
        pornRate = Column(Float)
        collectCount = Column(Integer)
        latestUpdate = Column(String(255))
        updateTime = Column(DateTime)
        createTime = Column(DateTime)
    ```

2. 运行爬虫程序
    ```sh
    python main.py
    ```

## 文件说明

- `main.py`: 主爬虫程序，包括数据抓取和存储的逻辑
- `Novel.py`: 定义小说模型（SQLAlchemy ORM）
- `requirements.txt`: 项目依赖包列表

## 配置说明

### 日志配置
在 `main.py` 中配置日志记录，默认为 `INFO` 级别：
```python
logging.basicConfig(level=logging.INFO)
```

### 请求头配置
在 `main.py` 中配置HTTP请求头：
```python
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
```
