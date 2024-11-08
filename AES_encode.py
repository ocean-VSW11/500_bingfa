#AES_encode.py

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import json
import base64

def encrypt_aes(data, key, iv):
    """
    对数据进行AES加密

    参数:
    data (dict): 要加密的数据
    key (bytes): AES密钥
    iv (bytes): 初始向量
    返回:
    str: Base64编码的密文
    """
    json_data = json.dumps(data).encode()
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(json_data, AES.block_size))
    return base64.b64encode(ciphertext).decode()

# # # # 测试数据 # # # #
# data = {
#     "organizationDesc": "简介"
# }
# key = b'gjx2023123456789'
# iv = b'1234567887654321'
# data = encrypt_aes(data,key,iv)
# print(data)
