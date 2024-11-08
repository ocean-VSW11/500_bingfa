import requests
import time
import logging

# 配置日志记录
logging.basicConfig(
    filename='测试_log.log',  # 日志文件名
    level=logging.INFO,  # 日志级别
    format='%(asctime)s - %(levelname)s - %(message)s',  # 日志格式
    datefmt='%Y-%m-%d %H:%M:%S'  # 时间格式
)


def test_api_with_json_and_logging(url, json_data, num_requests=500):
    """
    测试API接口，执行500次POST请求，并发送JSON数据，同时记录日志。

    参数:
    url (str): 接口的URL地址
    json_data (dict): 发送的JSON数据
    num_requests (int): 要执行的请求次数，默认为500次
    """
    for i in range(num_requests):
        try:
            # 发送POST请求并携带JSON数据
            response = requests.post(url, json=json_data)
            # content_type = response.headers.get('Content-Type', '') #简化log
            #
            # # 判断响应内容是否为HTML
            # if 'text/html' in content_type:
            #     # 如果响应是HTML，可能意味着重定向或错误页面
            #     response_summary = 'HTML response detected (possible redirect)'
            # else:
            #     # 否则，取前100个字符作为响应摘要
            #     response_summary = response.text[:100] + '...'      #简化log

            # 打印请求的结果信息（状态码和响应内容）
            print(f"Request {i + 1}/{num_requests}: Status Code = {response.status_code}, Response = {response.text}")

            # 将请求结果写入日志文件
            logging.info(
                f"Request {i + 1}/{num_requests}: Status Code = {response.status_code}, Response = {response.text}")

            # 处理非200状态码的情况，并写入警告日志
            if response.status_code != 200:
                logging.warning(f"Error: Received status code {response.status_code} for request {i + 1}")

        except requests.exceptions.RequestException as e:
            # 捕获并打印请求异常，同时记录到日志
            print(f"Request {i + 1} failed: {e}")
            logging.error(f"Request {i + 1} failed: {e}")



# 示例：调用函数进行接口测试，发送JSON数据，并记录日志
json_payload = {
    "username": "test_user",
    "password": "secure_password",
    "token": "abcd1234"
}

# 调用函数，发送JSON格式数据并记录日志
while True:
    test_api_with_json_and_logging("https://www.ww.com/api", json_payload)  # 调用目标函数
    time.sleep(10)  # 等待10秒