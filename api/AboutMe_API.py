# 个人信息API
from api.public_api import *


def get_user_info():
    request_data = {
        "type": 28
    }
    parsed_data = public_request(request_data)
    status = parsed_data['status']
    desc = parsed_data['desc']
    data = parsed_data['data']

    alias = data['alias']
    big_head_img_url = data['bigHeadImgUrl']
    nick_name = data['nickName']
    signature = data['signature']
    user_name = data['userName']

    # 打印解析结果
    print(f"Status: {status}")
    print(f"Description: {desc}")
    print(f"Alias: {alias}")
    print(f"Big Head Image URL: {big_head_img_url}")
    print(f"Nick Name: {nick_name}")
    print(f"Signature: {signature}")
    print(f"User Name: {user_name}")
