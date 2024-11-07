# 处理消息API
from BasicDefine import *
# Flask常规操作
app = Flask(__name__)
WECHAT_API_URL = 'http://127.0.0.1:8888/api/'
# 消息列表和锁
message_list = []
lock = threading.Lock()


# 接受消息推送的接口，所有的消息都会回调到这个接口中，由于只是演示，就只支持一个微信，如果多开了微信回调到同一个服务的同一个接口，需自行解析处理
@app.route('/wechatSDK', methods=['POST'])
def chat():
    data = request.json
    print(data)
    pushType = data["pushType"]  #
    if pushType != 1:  # 这里演示，只处理同步类型消息，其他类型可以自行处理
        return jsonify({"success": "true"})
    # 消息类型详见： https://github.com/WeChatAPIs/wechatAPI/blob/main/doc/处理消息/消息类型.md
    if data["data"]['type'] == 1:
        # 文本消息
        hadle_text_msg(data)
    # 消息类型详见： https://github.com/WeChatAPIs/wechatAPI/blob/main/doc/处理消息/消息类型.md
    if data["data"]['type'] == 34:
        # 语音消息
        handle_audio_msg(data)
    if data["data"]['type'] == 3:
        # 图片消息
        handle_image_msg(data)
    if data["data"]['type'] == 49:
        # XML消息
        handle_xml_msg(data)
    if data["data"]['type'] == 37:
        # 收到被添加好友消息
        handle_add_friend_msg(data)
    return jsonify({"success": "true"})


# 调用GPT和API产生结果
def hadle_text_msg(data):
    msg_obj = data["data"]
    # 哪个好友发送的消息，还是哪个群发送的消息
    sendChannel = msg_obj["from"]
    # 发送的消息内容是什么
    msgContent = msg_obj["content"]
    with lock:
        message_list.append({'from': sendChannel, 'content': msgContent})
    print(f"新消息存入列表: {msgContent}")


def handle_audio_msg(data):
    xmlContent = data['data']['content']
    # 微信群发言是有前缀的，这里需要去掉
    split = xmlContent.split(":\n")
    xmlContent = len(split) > 1 and split[1] or xmlContent
    content = xmltodict.parse(xmlContent)
    aeskey = content['msg']['voicemsg']['@aeskey']
    fileid = content['msg']['voicemsg']['@voiceurl']
    # 下载音频文件
    requests.post(
        WECHAT_API_URL,
        json={
            "type": 66,
            "fileid": fileid,
            "aeskey": aeskey,
            "fileType": 15,
            "savePath": f"D:\\aa\\{aeskey}.slik"
        })
    # 识别音频文件
    text = requests.post(
        WECHAT_API_URL,
        json={
            "type": 10045,
            "filePath": "D:\\aa\\" + aeskey + ".slik"
        })
    print("语音转文字结果：" + text.json())
    pass


def handle_add_friend_msg(data):
    xmlContent = data['data']['content']
    content = xmltodict.parse(xmlContent)
    username = content['msg']['@encryptusername']
    ticket = content['msg']['@ticket']
    scene = content['msg']['@scene']  #todo  scene参数取值是随便写的已实际的节点为准，这里只是演示下
    # 同意好友请求，这里只是演示，实际应用中，自己处理
    # 等待一会儿处理，模拟人工晚发现有人添加好友
    randomTime = random.randint(10, 30)
    time.sleep(randomTime)
    requests.post(
        WECHAT_API_URL,
        json={
            "type": 10035,
            "encryptUserName": username,
            "ticket": ticket,
            "scene":scene
        })
    pass


def handle_xml_msg(data):
    xmlContent = data['data']['content']
    # 微信群发言是有前缀的，这里需要去掉
    split = xmlContent.split(":\n")
    xmlContent = len(split) > 1 and split[1] or xmlContent
    content = xmltodict.parse(xmlContent)
    type = content['msg']['appmsg']['type']
    if type == str(6):
        # type 6 是文件，可以下载的，其他类型的消息自行处理，这里只处理文件类型
        fileName = content['msg']['appmsg']['title']
        fileId = content['msg']['appmsg']['appattach']['cdnattachurl']
        aeskey = content['msg']['appmsg']['appattach']['aeskey']
        # 下载文件，部分类型的文件可能有多条xml消息回调，注意判别哪些消息是可以处理，哪些是不能处理的
        requests.post(
            WECHAT_API_URL,
            json={
                "type": 66,
                "fileid": fileId,
                "aeskey": aeskey,
                "fileType": 5,
                "savePath": f"D:\\aa\\{fileName}"
            })
    elif type == str(33):
        # type 33 是小程序，可以打开的，其他类型的消息自行处理，这里只处理小程序类型
        appId = content['msg']['appmsg']['weappinfo']['appid']
        username = content['msg']['appmsg']['weappinfo']['username']
        pageUrl = content['msg']['appmsg']['weappinfo']['pagepath']
        # 打开小程序
        requests.post(
            WECHAT_API_URL,
            json={
                'type': 10106,
                'appid': appId,
                'bizUserName': username,
                'pageUrl': pageUrl
            })
    print(content)
    pass


def handle_image_msg(data):
    xmlContent = data['data']['content']
    # 微信群发言是有前缀的，这里需要去掉
    split = xmlContent.split(":\n")
    xmlContent = len(split) > 1 and split[1] or xmlContent
    content = xmltodict.parse(xmlContent)
    aeskey = content['msg']['img']['@aeskey']
    fileid = content['msg']['img']['@cdnthumburl']
    # 下载图片
    requests.post(
        WECHAT_API_URL,
        json={
            "type": 66,
            "fileid": fileid,
            "aeskey": aeskey,
            "fileType": 2,
            "savePath": f"D:\\aa\\{aeskey}.png"
        })
    print(content)
    pass


def addCallBackUrl(callBackUrl):
    """
    设置回调地址，当有人发送消息时，微信会就把信息发送到这个接口中
    :param callBackUrl: 回调地址，当有人发送消息时，微信会就把信息发送到这个接口中
    :return:
    """
    # 获取所有的回调地址
    resdatalist = requests.post(WECHAT_API_URL, json={"type": 1003}).json()["data"]["data"]
    # 删除之前的回调地址
    for item in resdatalist:
        requests.post(WECHAT_API_URL, json={"type": 1002, "cookie": item["cookie"]})
    # 设置新的回调地址
    requests.post(WECHAT_API_URL, json={"type": 1001, "protocol": 2, "url": callBackUrl})


def fetch_messages():
    with lock:
        if message_list:
            # 处理消息
            kk = copy.deepcopy(message_list)
            # 清空列表
            message_list.clear()
            return kk


try:
    # 给微信设置回调地址，当有人给发送消息时，微信会就把信息发送到这个接口中
    addCallBackUrl("http://127.0.0.1:18000/wechatSDK")
    print("连接微信成功")
except Exception as e:
    print("连接微信失败", e)
app.run(host='0.0.0.0', port=18000)