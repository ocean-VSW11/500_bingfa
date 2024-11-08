import requests
import time


def test_api_with_form_data(url, form_data, num_requests=500,):
    """
    测试API接口，执行500次POST请求，并发送表单键值对数据。

    参数:
    url (str): 接口的URL地址
    form_data (dict): 发送的表单数据（键值对）
    num_requests (int): 要执行的请求次数，默认为500次
    delay (int): 每次请求之间的延迟时间，默认为15秒
    """
    for i in range(num_requests):
        try:
            # 发送POST请求并携带表单数据
            response = requests.post(url, data=form_data)

            # 打印请求的结果信息（状态码和响应内容）
            print(f"Request {i + 1}/{num_requests}: Status Code = {response.status_code}, Response = {response.text}")

            # 处理非200状态码的情况
            if response.status_code != 200:
                print(f"Error: Received status code {response.status_code} for request {i + 1}")

        except requests.exceptions.RequestException as e:
            # 捕获并打印请求异常
            print(f"Request {i + 1} failed: {e}")


# 示例：调用函数进行接口测试，发送表单数据
form_payload = {
    "key1": "value1",
    "key2": "value2",
    "key3": "1234"
}

# 调用函数，发送表单格式的键值对数据
# while True:
#     test_api_with_form_data("https://your-api-endpoint.com/api", form_payload)
#     time.sleep(10)  # 等待10秒
