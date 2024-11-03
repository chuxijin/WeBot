# 发送消息API + 表情包API
from api.public_api import *


def send_txt_msg(userName, msgContent, atUserList=None):
    """
    参数名	            必选	类型	        说明
    type	            是	int	        接口编号
    userName	        是	string	    接收人wxid
    msgContent	        是	string	    文本内容
    atUserList	        否	list	    被艾特wxid列表
    insertToDatabase	否	bool	    是否将消息回写到数据库中，默认为true，<br/>如果您发现某些电脑出现阻塞可设置为false<br/>该参数在1.0.4.f2及以上版本出现
    bAsync	            否	bool	    如果将该参数设置为true，则任务不再阻塞，接口响应内容会通过消息处理器返回，消息推送类型为0<br/>如果提供了asyncUserData参数，会随调用结果一起推送
    asyncUserData	    否	str	    xxxx
    """
    request_data = {
        "type": 10009,
        "userName": userName,
        "msgContent": msgContent,
        "atUserList": atUserList,
        "insertToDatabase": False
    }
    data = public_request(request_data)
    print(data)
