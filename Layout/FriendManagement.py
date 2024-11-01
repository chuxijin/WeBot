from BasicDefine import *
from Layout.FriendConfig import *


class FriendManagementTab(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.load_config()

        # 定时器设定
        self.reply_timer = QTimer(self)
        self.reply_timer.timeout.connect(lambda: asyncio.ensure_future(self.auto_reply_to_friends()))
        self.reply_timer.start(self.config['reply_interval_seconds'] * 1000)

        self.fetch_timer = QTimer(self)
        self.fetch_timer.timeout.connect(lambda: asyncio.ensure_future(self.fetch_new_requests()))
        self.fetch_timer.start(self.config['fetch_interval_seconds'] * 1000)

        self.auto_approve = True
        self.auto_reply = True
        self.reply_text = ""
        self.reply_image = ""
        self.today_approved = 0
        self.pending_requests = 0

    def load_config(self):
        config_path = os.path.join('config', 'config.json')
        with open(config_path, 'r') as f:
            self.config = json.load(f)

    async def fetch_new_requests(self):
        print("Checking for new friend requests...")
        return
        # TODO: Implement the logic to fetch new requests
        # This example adds a dummy request - replace it with your actual fetch logic
        new_requests = [("account1", "friend_account1", "remark1"), ("account2", "friend_account2", "remark2")]
        for account, friend_account, remark in new_requests:
            self.add_friend_request(account, friend_account, remark)

    async def auto_reply_to_friends(self):
        return
        for row in range(self.friend_requests.rowCount()):
            remark_item = self.friend_requests.item(row, 3)
            account_item = self.friend_requests.item(row, 1)
            if remark_item and "已回复" not in remark_item.text() and self.config['keyword_responses']:
                message = remark_item.text()
                response = next((resp for keyword, resp in self.config['keyword_responses'].items() if keyword in message), None)

                if response:
                    account = account_item.text() if account_item else "unknown"
                    await self.send_auto_reply(account, response)
                    remark_item.setText(f"{remark_item.text()} (已回复)")

    async def send_auto_reply(self, account, message):
        print(f"Sending auto-reply message to {account}: {message}")
        api_endpoint = "http://example.com/api/sendmessage"  # Replace with actual API
        data = {
            "account": account,
            "message": message
            # Additional API parameters if needed
        }
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(api_endpoint, json=data) as response:
                    if response.status == 200:
                        print("Message sent successfully!")
                    else:
                        print(f"Failed to send message. Status code: {response.status}")
            except aiohttp.ClientError as e:
                print(f"An error occurred: {e}")

    def add_friend_request(self, account, friend_account, remark=""):
        row_position = self.friend_requests.rowCount()
        self.friend_requests.insertRow(row_position)

        # Checkbox
        checkbox = QCheckBox()
        checkbox.setStyleSheet("margin-left: 20px;")
        self.friend_requests.setCellWidget(row_position, 0, checkbox)

        # 账号
        self.friend_requests.setItem(row_position, 1, QTableWidgetItem(account))
        # 好友账号
        self.friend_requests.setItem(row_position, 2, QTableWidgetItem(friend_account))
        # 备注
        self.friend_requests.setItem(row_position, 3, QTableWidgetItem(remark))
        # 操作按钮
        agree_button = QPushButton("同意")
        refuse_button = QPushButton("拒绝")
        agree_button.clicked.connect(lambda: self.agree_friend(row_position))
        refuse_button.clicked.connect(lambda: self.refuse_friend(row_position))
        op_layout = QHBoxLayout()
        op_layout.addWidget(agree_button)
        op_layout.addWidget(refuse_button)
        op_layout.setContentsMargins(0, 0, 0, 0)
        op_widget = QWidget()
        op_widget.setLayout(op_layout)
        self.friend_requests.setCellWidget(row_position, 4, op_widget)

        self.pending_requests += 1
        self.update_statistics()
