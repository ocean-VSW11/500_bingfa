import requests
from urllib3.poolmanager import PoolManager
import ssl
from requests.adapters import HTTPAdapter
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging


# 自定义适配器，强制使用TLSv1.2
class TLSAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        context = ssl.create_default_context()
        context.set_ciphers('TLSv1.2')  # 强制使用TLSv1.2
        kwargs['ssl_context'] = context
        return super(TLSAdapter, self).init_poolmanager(*args, **kwargs)


# 配置日志
logging.basicConfig(
    filename='api_requests.log',  # 日志文件名
    level=logging.INFO,  # 日志级别为INFO
    format='%(asctime)s - %(levelname)s - %(message)s',  # 日志格式
    datefmt='%Y-%m-%d %H:%M:%S'  # 时间格式
)


def send_request(session, url, data):
    """
    发送POST请求并返回状态码或错误信息，记录异常。

    参数:
    session (requests.Session): 配置了TLS的会话
    url (str): 请求的URL
    data (dict): 发送的JSON数据
    """
    try:
        # 使用会话发送请求
        response = session.post(url, json=data)
        status_code = response.status_code
        # 如果请求成功，记录状态码
        logging.info(f"Status Code: {status_code}")
        return f"Status Code: {status_code}"
    except requests.exceptions.RequestException as e:
        # 如果请求失败，记录异常信息
        logging.error(f"Request failed: {e}")
        return f"Request failed: {e}"


def send_requests_concurrently(url, data, num_requests=500):
    """
    并发地发送指定数量的请求，并将状态码或异常记录到日志文件中。

    参数:
    url (str): 请求的URL
    data (dict): 发送的JSON数据
    num_requests (int): 并发请求的数量，默认500
    """
    session = requests.Session()
    session.mount('https://', TLSAdapter())

    with ThreadPoolExecutor(max_workers=num_requests) as executor:
        futures = [executor.submit(send_request, session, url, data) for _ in range(num_requests)]

        for future in as_completed(futures):
            result = future.result()
            print(result)  # 如果需要，也可以打印到控制台


# 示例数据
url = "https://222.85.202.67:689"
json_payload = {
    "username": "test_user",
    "password": "secure_password",
    "token": "abcd1234"
}

# 调用函数并发发送500次请求
send_requests_concurrently(url, json_payload, 10)
