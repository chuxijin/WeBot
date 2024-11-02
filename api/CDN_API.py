# CDN api
from api.public_api import *


def upload_file(file_path: str):
    """
    参数名	        必选	类型	        说明
    type	        是	int	        接口编号
    filePath	    是	string	    文件绝对路径
    aeskey	        是	string	    文件的md5
    fileType	    是	int	        文件类型，可参考枚举值，更多类型可从消息XML获取
    bAsync	        否	bool	    如果将该参数设置为true，则任务不再阻塞，接口响应内容会通过消息处理器返回，消息推送类型为0<br/>如果提供了asyncUserData参数，会随调用结果一起推送
    asyncUserData	否	str	        xxxx
    """
    request_data = {
        "type": 7,
        "filePath": file_path,
        "aeskey": get_file_md5(file_path),
        "fileType": determine_file_type(file_path)
    }
    data = public_request(request_data)

    status = data.get("status", "未定义")
    description = data.get("desc", "")
    nested_data = data.get("data", {})

    aeskey = nested_data.get("aeskey", "")
    encrypt_file_md5 = nested_data.get("encryptfilemd5", "")
    file_crc = nested_data.get("filecrc", "")
    file_id = nested_data.get("fileid", "")
    file_key = nested_data.get("filekey", "")
    # 可继续解析更多数据...


def download_file(fileid='', aeskey='', fileType=5, savePath='', bAsync=True, asyncUserData='', chatType=0):
    """
    参数名	        必选	类型	        说明
    type	        是	int	        接口编号
    fileid	        是	string	    fileid
    aeskey	        是	string	    aeskey
    fileType	    是	int	        文件类型，可参考枚举值，更多类型可从消息XML获取
    savePath	    是	string	    文件保存路径
    bAsync	        否	bool	    如果将该参数设置为true，则任务不再阻塞，接口响应内容会通过消息处理器返回，消息推送类型为0<br/>如果提供了asyncUserData参数，会随调用结果一起推送
    asyncUserData	否	str	        xxxx
    chatType	    否	int	        消息类型，默认为0 <br/>0:私聊消息 1:群聊消息
    此接口支持企业微信联系人发送的消息，使用的参数需要从url中提取，f表示fileid，p表示fileType。
    企业联系人发送的cdn消息，可以使用GET方式请求url（注意要将&替换为&），然后使用aes-ecb解密，并使用PKCS7进行unpadding。
    （不能保证企业微信发的消息测试用例覆盖完整，如方案无法正常执行请提供原始的xml/入群链接等方式帮助技术排查研究）
    """
    request_data = {
        "type": 88,
        "fileid": fileid,
        "aeskey": aeskey,
        "fileType": fileType,
        "savePath": savePath
    }
    data = public_request(request_data)
    status = data.get("status", "未定义")
    desc = data.get("desc", "")
