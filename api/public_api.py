import requests
from typing import List, Optional, Dict, Any


class MessageClient:
    def __init__(self, base_url: str = "http://127.0.0.1:8888/api/"):
        self.base_url = base_url.rstrip('/')

    def send_text_message(
            self,
            type_code: int,
            user_name: str,
            msg_content: str,
            at_user_list: Optional[List[str]] = None,
            insert_to_database: bool = True,
            b_async: bool = False,
            async_user_data: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        发送文本消息。

        :param type_code: 接口编号（例如：10009）
        :param user_name: 接收人wxid
        :param msg_content: 文本内容
        :param at_user_list: 被艾特wxid列表
        :param insert_to_database: 是否将消息回写到数据库中，默认为True
        :param b_async: 是否异步发送
        :param async_user_data: 异步发送的附加数据
        :return: API返回的JSON数据
        """
        url = f"{self.base_url}/"  # 确保URL正确
        payload = {
            "type": type_code,
            "userName": user_name,
            "msgContent": msg_content,
        }

        if at_user_list:
            payload["atUserList"] = at_user_list
        if insert_to_database is not None:
            payload["insertToDatabase"] = insert_to_database
        if b_async is not None:
            payload["bAsync"] = b_async
        if async_user_data:
            payload["asyncUserData"] = async_user_data

        headers = {
            'Content-Type': 'application/json'
        }

        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"请求失败: {e}")
            return {"error_code": -1, "description": str(e), "data": None}

    def send_mention_all_message(
            self,
            type_code: int,
            user_name: str,
            msg_content: str,
            is_admin: bool = False,
            insert_to_database: bool = True,
            b_async: bool = False,
            async_user_data: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        发送@所有人的消息。

        :param type_code: 接口编号（例如：10009）
        :param user_name: 接收人wxid
        :param msg_content: 文本内容，需要包含“@所有人”
        :param is_admin: 是否为管理员，发送@所有人通常需要管理员权限
        :param insert_to_database: 是否将消息回写到数据库中，默认为True
        :param b_async: 是否异步发送
        :param async_user_data: 异步发送的附加数据
        :return: API返回的JSON数据
        """
        if not is_admin:
            print("发送@所有人消息通常需要管理员权限。")
            return {"error_code": 1, "description": "权限不足，无法发送@所有人消息。", "data": None}

        msg_content = "@所有人 " + msg_content
        at_user_list = ["notify@all"]

        return self.send_text_message(
            type_code=type_code,
            user_name=user_name,
            msg_content=msg_content,
            at_user_list=at_user_list,
            insert_to_database=insert_to_database,
            b_async=b_async,
            async_user_data=async_user_data
        )

    def handle_response(self, response: Dict[str, Any]) -> None:
        """
        处理API响应。

        :param response: API返回的JSON数据
        """
        if response.get("error_code") != 0:
            print(f"错误代码: {response.get('error_code')}, 描述: {response.get('description')}")
        else:
            print("消息发送成功！")
            print("返回数据:", response.get("data"))