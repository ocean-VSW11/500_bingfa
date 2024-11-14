import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
import time
import logging
from AES_encode import encrypt_aes  # 导入自定义的AES加密模块

# 配置日志
logging.basicConfig(
    filename='api_requests.log',  # 日志文件名
    level=logging.INFO,  # 日志级别为INFO
    format='%(asctime)s - %(levelname)s - %(message)s',  # 日志格式
    datefmt='%Y-%m-%d %H:%M:%S'  # 时间格式
)

# 前置条件：生成签名
def generate_signature(appid, key, timestamp):
    """
    根据 appid, key 和时间戳生成 MD5 签名
    """
    sign_str = f"{appid}{key}{timestamp}"
    sign = hashlib.md5(sign_str.encode()).hexdigest()
    return sign

# 前置条件：获取请求头
def get_headers(token, appid, version):
    """
    获取请求头，包含 Authorization, AppId, version 等信息
    """
    return {
        "Authorization": token,
        "AppId": appid,
        "version": version,
    }

# 发送单个请求
def send_request(url, data, headers):
    """
    发送get请求并返回状态码或错误信息，记录异常。

    参数:
    url (str): 请求的URL
    data (dict): 发送的JSON数据
    headers (dict): 请求头
    """
    try:
        response = requests.get(url, json=data, headers=headers, verify=False)
        status_code = response.status_code
        # 如果请求成功，记录状态码
        logging.info(f"Status Code: {status_code}, Response Body:{response.text}")
        return f"Status Code: {status_code},Response Body:{response.text}"
    except requests.exceptions.RequestException as e:
        # 如果请求失败，记录异常信息
        logging.error(f"Request failed: {e}")
        return f"Request failed: {e}"

# 并发发送请求
def send_requests_concurrently(url, data, num_requests, headers):
    """
    并发地发送指定数量的请求，并将状态码或异常记录到日志文件中。

    参数:
    url (str): 请求的URL
    data (dict): 发送的JSON数据
    num_requests (int): 并发请求的数量
    headers (dict): 请求头
    """
    with ThreadPoolExecutor(max_workers=num_requests) as executor:
        futures = [executor.submit(send_request, url, data, headers) for _ in range(num_requests)]

        for future in as_completed(futures):
            result = future.result()
            print(result)  # 如果需要，也可以打印到控制台


###############################################

# 前置条件：设置签名和头信息
url = "http://192.168.6.160:8080/system/user/100?"  # 替换为实际的 API 端点
appid = "GJX0000000001001"
key = "gjx2023123456789"
version = "1.0"
token = "eyJhbGciOiJIUzUxMiJ9.eyJ1c2VyX2lkIjoxLCJjb21wYW55TmFtZSI6bnVsbCwidXNlcl9rZXkiOiJmMjg0YjgzYS1jOTNjLTRiYzUtYWNhMC0wMjlkYzMxNGI4ODciLCJ1c2VybmFtZSI6ImFkbWluIn0.c0Gd5LNcGB5ae2oze41LlVGhsPTE3_tzvVuEvin68Tsf7ZWgUfvirVXRHiKbXCiu59WCsR8PTj_1W_opYwVfJQ"  # 替换为实际的 token

# 获取当前时间戳
timestamp = str(int(time.time()))

# 生成签名
sign = generate_signature(appid, key, timestamp)

# 设置请求头
headers = get_headers(token, appid, version)

# AES密钥和IV
aes_key = b'gjx2023123456789'  # 替换为实际密钥
iv = b'1234567887654321'  # 替换为实际IV

data = {
    "frontData": {
        "organizationType": "dept",
        "organizationName": "部门9",
        "companyCreditCode": "",
        "companyAddress": "",
        "contactPeople": "王炜_员工测试号",
        "contactTel": "15286025490",
        "companyIndustry": "",
        "legalPersonName": "",
        "busLicenseUrl": "",
        "organizationDesc": "简介",
        "employeeId": 1837094862331228200,
        "pid": "1837119812639305730"
    }
}

# 调用加密函数
encrypted_data = encrypt_aes(data, aes_key, iv)

# 示例数据
json_payload = {
  "timestamp": 1731319975428,
  "sign": "d88dc2eaf2862e1a217f2351d28b9006",
  "data": encrypted_data
}

# 在数据中加入签名和时间戳
json_payload["timestamp"] = timestamp
json_payload["sign"] = sign

# 调用函数并发发送10次请求
send_requests_concurrently(url, json_payload, 1, headers)
