import requests
import logging
import hashlib
import time
import json

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

def test_api(url, data, headers, num_requests=1):
    logging.info("Starting API test...")

    for i in range(num_requests):
        print(f"Sending request {i + 1}...")
        try:
            # 发送GET请求
            response = requests.get(url, data, headers=headers)

            status_code = response.status_code
            response_text = json.dumps(json.loads(response.text), ensure_ascii=False ,indent=4)
            # 记录状态码和响应内容
            logging.info(f"Status Code: {status_code}, Response Body: {response.text}")

            # 处理非200状态码的情况
            if status_code != 200:
                print(f"Error: Received status code {status_code} for request {i + 1}")
                return f"Status Code: {status_code}, Response Body: {response.text}"

            # 打印成功的响应
            print(f"Success: Status Code: {status_code}, Response Body: {response_text}")
            return f"Status Code: {status_code}, Response Body: {response.text}"

        except requests.exceptions.RequestException as e:
            # 捕获并打印请求异常
            print(f"Request {i + 1} failed: {e}")
            logging.error(f"Request {i + 1} failed: {e}")  # 记录异常


# 示例：调用函数进行接口测试
url = "http://222.85.202.67:688/api/crm/web/companyInfo/getOrganizationTree"
headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzUxMiJ9.eyJ1c2VyX2lkIjo0MzQyOTksImNvbXBhbnlOYW1lIjpudWxsLCJ1c2VyX2tleSI6IjUwOGRmYmZmLWZlZTAtNGFiZS04ODE5LTU5ZjBlZjllY2I3OSIsInVzZXJuYW1lIjoid3dfdGVzdCJ9.NwaTGo2H9mfvPgr3CWuvjV75NkNoYjWbeFAZUrcf1kr3h0aiWwRyBsKd6Dw4ZAm2oJ6g_JGrSocNA2Ctzn62HQ",  # 替换为实际的 token
    "AppId": "GJX0000000001001",
    "version": "1.0"
}
appid = "GJX0000000001001"
key = "gjx2023123456789"
# 获取当前时间戳
timestamp = str(int(time.time()))

# 生成签名
sign = generate_signature(appid, key, timestamp)

json_payload = {
    "timestamp": 1729237963034,
    "sign": "43fa6df1853e8e372527e2ab44104128"
}

json_payload["timestamp"] = timestamp
json_payload["sign"] = sign

# 调用函数进行接口测试
test_api(url, json_payload, headers, 1)
