# -*- coding: utf-8 -*-

import requests
import logging
import hashlib
import time
import json
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

# 设置标准输出编码为UTF-8
sys.stdout.reconfigure(encoding='utf-8')

# 配置日志，编码改为UTF-8
logging.basicConfig(
    filename='api_requests.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    encoding='utf-8'
)

# 生成签名
def generate_signature(appid, key, timestamp):
    """
    根据 appid, key 和时间戳生成 MD5 签名
    """
    sign_str = f"{appid}{key}{timestamp}"
    sign = hashlib.md5(sign_str.encode()).hexdigest()
    return sign

# 发送请求的函数
def send_request(url, params, headers):
    try:
        response = requests.get(url, params=params, headers=headers)
        status_code = response.status_code
        response_text = json.dumps(response.json(), ensure_ascii=False, indent=4)

        logging.info(f"Status Code: {status_code}, Response Body: {response_text}")

        # 返回请求结果
        if status_code == 200:
            print(f"Success: Status Code: {status_code}, Response Body: {response_text}")
        else:
            print(f"Error: Status Code: {status_code}")
        return status_code, response_text

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        logging.error(f"Request failed: {e}")
        return None, None

# 配置请求信息
url = "http://192.168.6.160:8080/system/user/100?"
headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzUxMiJ9.eyJ1c2VyX2lkIjoxLCJjb21wYW55TmFtZSI6bnVsbCwidXNlcl9rZXkiOiJmMjg0YjgzYS1jOTNjLTRiYzUtYWNhMC0wMjlkYzMxNGI4ODciLCJ1c2VybmFtZSI6ImFkbWluIn0.c0Gd5LNcGB5ae2oze41LlVGhsPTE3_tzvVuEvin68Tsf7ZWgUfvirVXRHiKbXCiu59WCsR8PTj_1W_opYwVfJQ",  # 替换为实际的 token
    "AppId": "GJX0000000001001",
    "version": "1.0"
}
appid = "GJX0000000001001"
key = "gjx2023123456789"
timestamp = str(int(time.time() * 1000))  # 使用毫秒级时间戳
sign = generate_signature(appid, key, timestamp)

params = {
    "timestamp": timestamp,
    "sign": sign
}

# 并发发送500个请求
num_requests = 500
with ThreadPoolExecutor(max_workers=500) as executor:
    futures = [executor.submit(send_request, url, params, headers) for _ in range(num_requests)]
    for future in as_completed(futures):
        status_code, response_text = future.result()
