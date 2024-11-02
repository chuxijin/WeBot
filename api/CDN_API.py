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
    try:
        # 发送POST请求
        response = requests.post(url, data=json.dumps(request_data), headers=headers)
        # 检查响应状态码
        if response.status_code == 200:
            # 解析JSON响应
            result = response.json()
            # 提取并输出需要的数据
            data = result.get("data", {})
            status = data.get("status", "未定义")
            description = data.get("desc", "")
            nested_data = data.get("data", {})

            aeskey = nested_data.get("aeskey", "")
            encrypt_file_md5 = nested_data.get("encryptfilemd5", "")
            file_crc = nested_data.get("filecrc", "")
            file_id = nested_data.get("fileid", "")
            file_key = nested_data.get("filekey", "")
            # 可继续解析更多数据...

        else:
            print(f"请求失败，状态码: {response.status_code}")

    except requests.RequestException as e:
        print(f"请求时发生错误: {e}")
