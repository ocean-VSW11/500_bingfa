# aes_utils.py

from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import json
import base64

def decrypt_aes(encrypted_data, key, iv):
    """
    对加密的数据进行AES解密

    参数:
    encrypted_data (str): 要解密的Base64编码的密文
    key (bytes): AES密钥
    iv (bytes): 初始向量
    返回:
    dict: 解密后的数据
    """
    ciphertext = base64.b64decode(encrypted_data)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_data = unpad(cipher.decrypt(ciphertext), AES.block_size)
    # return json.loads(decrypted_data.decode())
    return json.dumps(json.loads(decrypted_data.decode()), ensure_ascii=False ,indent=4)

# # # 测试数据 # # # #
data = "yopdHlciCiH98SPWBv4S0j+fJW45HMPvpU4G1GdOUU53eB5dqStysArZnO3DuXQ4gflFuc5HXHuZbYCC6udb9C2VllKbS8iM22QEyjBG4Xn8o80YheIyAzUACMu6yp/0hbj093ZuQzUY+ILx/kKvkXor7Bx6ka4dw2D/VhWpxK/KMj+1FVXM5/N7tecDYshN3EeyjSJx8Mf0ByIAYiyG8xvz+Qn6atK9NcUu9jZ+66csYUyovsRXomSr/nfJFczLlWE+80mkfTCC1TQiOCNJOWf7iCRSDaNTvSsnDTCfr/Evq3slVMBFAqGtg+E/fBK3LenPx2d+raV+xyd7lUoZHiWkQkNhiuayK41fjb69q7v21s1+0gDXfHvY2ADtRFB9pRcKyvZASyAm3hiHEZ1ik1LfHh3U2Y5xLnQ9roY8VVA+agtfNbjpEXTqNuOg9bnS90UcrGeR5Ux2scDTm4zdG7tqzOLjP/NXWIh6cKe44eiZFMyI0WuLr7HdKDSOrVT6n7syw6qNEPCbQUNaUW7q0b9+xSpzwY7ZaUJSwPpnYG/+nnyrEK1jOp6ofa3/CyDCGfdM7Q37F2ju1znz5ZgirLVlaVFQVvXtSSUsODKCh/rkJm6ZjnI5JroRNuFasEE/ueJ9yYZYnw4T6yi2V04VgYZhqXeV7UQCeLw0GoXhQYgcmHAb8aeUFyA2Dnr4iYyCKNTK4gDbZCcGm8b9G7fwYC8QzdWhsMrkf9DES6wcOQn0vT+9eYA1nrqPDX9vDxDfT9+fxzPV7RZlDrnLzZiRHSILILN6u+beXfUug87iD2aj4QvMRlXD4LorlIoMCdlzCvF7b+E/kLxPI6l1WuBGY3x6QdzqUggrs9HRjVvslytGiqRwBfZaatDzxASqsdFtmrYHGE1dtXlVKK9EZ1kanzK0jqhbDeRpxWzRu/HW0vQGgZEu2g0dn9g0QZ5BoCOTgzgIeMcwEcFgkT+gHWGmCkb/17m48RcAsSbYhTYv0Qo8BQGyrX1S/BgqlvdZcJnk/mtpJpM5G6vQwxOjoeGTRf3uDomnogF0Waln9YvHZugRYDvJSfJmOfQG3qr6m0L9MMAHDrlbVniODFbwAPbhyGN3LNu50M5UNuDrHQkW7bKZOG94UuSoyf1q2hxAv/rENRfUUp3hyk+uQd/jzq9Hx5hV4MYA2k+CT9Kovd8XXf+6FCgyXC4v4os69PoQ3R4InQZDqglMPQpCi5/23Yp6nGztjQbYtybXsbS0ruJ3wISVHXcpbVO2r112PhMJihA+or8vtS9f/tF5ZguMs959oCEIlRsoz0OwTUEr8Xqsgu1wv1Eq/hscMc0jDPMKV21pTQoNN6uS9QVK1Cf4snAcmnwJhJPb908O2W/7va6lky36DDfL9lllgOD7HvCo0KdCKVv2dSgCe0yVTKaKc/Tbe4AoKt9tA8jg/yPzlh1Lb1s="


key = b'gjx2023123456789'
iv = b'1234567887654321'
data = decrypt_aes(data,key,iv)
print(data)