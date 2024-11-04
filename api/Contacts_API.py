# 通讯录API
from api.public_api import *
from BasicDefine import *


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


# 设置备注
def set_other_name(old_name, new_name):
    """
    参数名	    必选	类型	    说明
    type	    是	int	    接口编号
    userName	是	string	用户wxid
    remark	    是	string	备注信息
    """
    if not new_name:
        # 获取当前日期
        current_date = datetime.now()

        # 格式化日期为指定格式并转换为字符串
        new_name = old_name + current_date.strftime('%y%m%d')
    request_data = {
        "type": 10013,
        "userName": old_name,
        "remark": new_name
    }
    parsed_data = public_request(request_data)


# 获取用户信息 *特别重要* 获取到api实际返回，可以将上面的接口改写成传user_name！
def get_user_info(userName):
    """
    参数名	            必选	类型	            说明
    type	            是	int	            接口编号
    userName	        是	string, list	用户wxid或wxid列表
    chatroomUserName	否	string	        群聊wxid，如果指定了此参数，将会通过群聊获取目标用户信息
    """
    request_data = {
        "type": 10015,
        "userName": userName
    }
    parsed_data = public_request(request_data)
    status = parsed_data.get('status', None)
    desc = parsed_data.get('desc', None)
    data = parsed_data.get('data', [])
    return data


# 获取所有好友列表
def get_all_list():
    """
    type	        是	int	    接口编号
    dbName	        否	string	数据库名称，优先级低于dbHandle
    dbHandle	    否	int	    数据库句柄，优先级高于dbName
    sql	            是	string	sql
    """
    """
    获取所有好友列表，以及所有群里的好友列表
    {
     "type": 10058,
     "dbName": "MicroMsg.db",
     "sql": "SELECT chl.smallHeadImgUrl, c.UserName, c.Remark, c.nickName FROM Contact c LEFT JOIN ContactHeadImgUrl chl ON c.UserName = chl.usrName;"
    }
    
    只获取通讯录好友列表
    {
    "type": 10058,
    "dbName": "MicroMsg.db",
    "sql": "SELECT UserName,Remark,NickName,PYInitial,RemarkPYInitial,t2.smallHeadImgUrl FROM Contact t1 LEFT JOIN ContactHeadImgUrl t2 ON t1.UserName = t2.usrName WHERE t1.VerifyFlag = 0 AND (t1.Type = 3 OR t1.Type > 50) and t1.Type != 2050 AND t1.UserName NOT IN ('qmessage', 'tmessage') ORDER BY t1.Remark DESC;"
    }
    
    只获取群
    {
    "type": 10058,
    "dbName": "MicroMsg.db",
    "sql": "SELECT UserName,Remark, NickName,PYInitial,RemarkPYInitial FROM Contact t1 WHERE t1.Type in(2,2050);"
    }
    
    判断群聊是否是企业群
    {
    "type": 10058,
    "dbName": "MicroMsg.db",
    "sql": "SELECT UserName,Remark, NickName,PYInitial,RemarkPYInitial FROM Contact t1 WHERE t1.Type = 2050 and t1.UserName='xxxx@chatroom';"
    }
    
    获取企业群中的昵称
    {
    "type": 10058,
    "dbName": "OpenIMContact.db",
    "sql": "SELECT Remark, NickName FROM OpenIMContact t1 where UserName = 'xxxxx@openim'"
    }
    """
    request_data = {
        "type": 10058,
        "dbName": "MicroMsg.db",
        "sql": "SELECT chl.smallHeadImgUrl, c.UserName, c.Remark, c.nickName FROM Contact c LEFT JOIN ContactHeadImgUrl chl ON c.UserName = chl.usrName;"
    }
    parsed_data = public_request(request_data)
    status = parsed_data.get('status', None)
    desc = parsed_data.get('desc', None)
    data = parsed_data.get('data', [])
    return data