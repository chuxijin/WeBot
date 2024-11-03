# 个人信息API
from api.public_api import *


def get_user_info():
    request_data = {
        "type": 28
    }
    parsed_data = public_request(request_data)

    status = parsed_data.get('status', None)
    desc = parsed_data.get('desc', None)
    data = parsed_data.get('data', {})

    alias = data.get('alias', None)
    big_head_img_url = data.get('bigHeadImgUrl', None)
    nick_name = data.get('nickName', None)
    signature = data.get('signature', None)
    user_name = data.get('userName', None)

    # 打印解析结果
    print(f"Status: {status}")
    print(f"Description: {desc}")
    print(f"Alias: {alias}")
    print(f"Big Head Image URL: {big_head_img_url}")
    print(f"Nick Name: {nick_name}")
    print(f"Signature: {signature}")
    print(f"User Name: {user_name}")


def get_user_name():
    request_data = {
        "type": 28
    }
    parsed_data = public_request(request_data)
    data = parsed_data.get('data', {})
    return data.get('userName', None)
