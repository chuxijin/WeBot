# 通讯录API
from api.public_api import *


# 获取通讯录
def get_contacts():
    request_data = {
        "type": 29
    }
    parsed_data = public_request(request_data)
    status = parsed_data.get('status', None)
    desc = parsed_data.get('desc', None)
    data = parsed_data.get('data', [])
    return data


# 通过好友
def pass_friend_request(encryptUserName, ticket, scene=None):
    """
    参数名	        必选	类型	        说明
    type	        是	int	        接口编号
    encryptUserName	是	string	    用户v3数据
    ticket	        是	string	    用户v4数据
    scene	        否	int	        好友来源，可以从消息xml中获取
    """
    request_data = {
        "type": 10035,
        "encryptUserName": encryptUserName,
        "ticket": ticket
    }
    parsed_data = public_request(request_data)
    if parsed_data == {}:
        request_data = {
            "type": 10035,
            "encryptUserName": encryptUserName,
            "ticket": ticket,
            "scene": scene
        }
    parsed_data = public_request(request_data)
