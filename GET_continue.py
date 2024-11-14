import requests
import logging
import hashlib
import time
import json
from concurrent.futures import ThreadPoolExecutor, as_completed

# 配置日志
logging.basicConfig(
    filename='api_requests.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


# 前置条件：生成签名
def generate_signature(appid, key, timestamp):
    """
    根据 appid, key 和时间戳生成 MD5 签名
    """
    sign_str = f"{appid}{key}{timestamp}"
    sign = hashlib.md5(sign_str.encode()).hexdigest()
    return sign


# 发送单个请求
def send_request(url, data, headers):
    try:
        response = requests.get(url, params=data, headers=headers)
        status_code = response.status_code
        response_text = json.dumps(json.loads(response.text), ensure_ascii=False, indent=4)

        # 记录状态码和响应内容
        logging.info(f"Status Code: {status_code}, Response Body: {response_text}")

        if status_code != 200:
            print(f"Error: Received status code {status_code}")
        else:
            print(f"Success: Status Code: {status_code}")

        return status_code, response_text

    except requests.exceptions.RequestException as e:
        logging.error(f"Request failed: {e}")
        print(f"Request failed: {e}")


# 并发发送多个请求
def test_api(url, data, headers, num_requests):
    logging.info("Starting API test with concurrency...")

    with ThreadPoolExecutor(max_workers=num_requests) as executor:
        futures = [executor.submit(send_request, url, data, headers) for _ in range(num_requests)]

        for i, future in enumerate(as_completed(futures)):
            try:
                result = future.result()
                print(f"Request {i + 1} completed with result: {result}")
            except Exception as e:
                print(f"Request {i + 1} failed with exception: {e}")


# 示例：调用函数进行接口测试
url = "http://222.85.202.67:688/api/crm/web/companyInfo/getOrganizationTree"
headers = {
    "Authorization": "eyJhbGciOiJIUzUxMiJ9.eyJ1c2VyX2lkIjo0MzQyOTksImNvbXBhbnlOYW1lIjpudWxsLCJ1c2VyX2tleSI6ImZlNWJiZWQ2LThlM2ItNGZmZC1iZWMwLWUzYTQyYWI1MDZhNCIsInVzZXJuYW1lIjoid3dfdGVzdCJ9.CKJ7atYf5z-wc-JKPtkhkbvw2UVR1NntpHLkGfZ0tuU1DB17dylz-m511U0PoKJs9Ebjdez-GYfFBR18i-5dBw",
    # 替换为实际的 token
    "AppId": "GJX0000000001001",
    "version": "1.0"
}
appid = "GJX0000000001001"
key = "gjx2023123456789"
timestamp = str(int(time.time()))

# 生成签名
sign = generate_signature(appid, key, timestamp)
json_payload = {
    "timestamp": timestamp,
    "sign": sign
}

# 调用函数进行接口测试，发起100个并发请求###
test_api(url, json_payload, headers, 1)
