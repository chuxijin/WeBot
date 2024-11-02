from BasicDefine import *
from Layout.FriendConfig import *


class FriendManagementTab(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.load_config()

        # Timers for automated tasks.
        self.reply_timer = QTimer(self)
        self.reply_timer.timeout.connect(lambda: asyncio.ensure_future(self.auto_reply_to_friends()))
        self.reply_timer.start(self.config['reply_interval_seconds'] * 1000)

        self.fetch_timer = QTimer(self)
        self.fetch_timer.timeout.connect(lambda: asyncio.ensure_future(self.fetch_new_requests()))
        self.fetch_timer.start(self.config['fetch_interval_seconds'] * 1000)

        self.auto_approve_timer = QTimer(self)
        self.auto_approve_timer.timeout.connect(lambda: asyncio.ensure_future(self.auto_approve_friends()))
        self.auto_approve_timer.start(self.config.get('friend_approval_interval_seconds', 10) * 1000)

        self.auto_approve = True
        self.auto_reply = True
        self.reply_text = self.config.get('approval_message', "")
        self.reply_image = self.config.get('approval_image', "")

    def initUI(self):
        layout = QVBoxLayout(self)

        # Friend requests group box
        requests_group = QGroupBox("好友申请")
        requests_group.setStyleSheet("""
               QGroupBox {
                   font-size: 16px;
                   font-weight: bold;
                   margin-top: 10px;
               }
               QGroupBox::title {
                   subcontrol-origin: margin;
                   left: 10px;
                   padding: 0 3px 0 3px;
               }
           """)
        requests_layout = QVBoxLayout(requests_group)
        self.friend_requests = QTableWidget()
        self.friend_requests.setColumnCount(5)
        self.friend_requests.setHorizontalHeaderLabels(["选择", "账号", "好友账号", "备注", "操作"])
        self.friend_requests.horizontalHeader().setStretchLastSection(True)
        self.friend_requests.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.friend_requests.setStyleSheet("""
               QTableWidget {
                   background-color: #FFF0F5;
                   alternate-background-color: #FFE4E1;
                   gridline-color: #FFB6C1;
                   selection-background-color: #FF69B4;
               }
               QHeaderView::section {
                   background-color: #C71585;
                   color: white;
                   padding: 4px;
                   font-size: 14px;
               }
               QPushButton {
                   background-color: #20B2AA;
                   color: white;
                   border: none;
                   padding: 6px 12px;
                   font-size: 12px;
                   border-radius: 4px;
               }
               QPushButton:hover {
                   background-color: #3CB371;
               }
               QPushButton:pressed {
                   background-color: #2E8B57;
               }
           """)

        requests_layout.addWidget(self.friend_requests)
        layout.addWidget(requests_group)

        # Statistics layout
        stats_layout = QHBoxLayout()
        self.total_label = QLabel("好友申请总计: 0")
        self.today_approved_label = QLabel("今日已通过: 0")
        self.pending_label = QLabel("待通过: 0")
        stats_layout.addWidget(self.total_label)
        stats_layout.addWidget(self.today_approved_label)
        stats_layout.addWidget(self.pending_label)
        stats_layout.addStretch()
        layout.addLayout(stats_layout)

        # Buttons layout
        button_layout = QHBoxLayout()
        self.approve_all_button = QPushButton("一键通过")
        self.approve_all_button.setIcon(QIcon("icons/approve.png"))
        self.approve_all_button.setStyleSheet("""
               QPushButton {
                   background-color: #1E90FF;
                   color: white;
                   border: none;
                   padding: 10px 20px;
                   font-size: 14px;
                   border-radius: 4px;
               }
               QPushButton:hover {
                   background-color: #1C86EE;
               }
               QPushButton:pressed {
                   background-color: #1874CD;
               }
           """)
        self.approve_all_button.clicked.connect(self.approve_all_friends)

        self.config_button = QPushButton("好友通过配置")
        self.config_button.setIcon(QIcon("icons/config.png"))
        self.config_button.setStyleSheet("""
               QPushButton {
                   background-color: #FF69B4;
                   color: white;
                   border: none;
                   padding: 10px 20px;
                   font-size: 14px;
                   border-radius: 4px;
               }
               QPushButton:hover {
                   background-color: #FF6EB4;
               }
               QPushButton:pressed {
                   background-color: #FF1493;
               }
           """)
        self.config_button.clicked.connect(self.open_config_dialog)

        button_layout.addWidget(self.approve_all_button)
        button_layout.addWidget(self.config_button)
        button_layout.addStretch()

        layout.addLayout(button_layout)

        # Initialize statistics
        self.update_statistics()

    def update_statistics(self):
        total = self.friend_requests.rowCount()
        self.total_label.setText(f"好友申请总计: {total}")

    def load_config(self):
        with open(CONFIG_FILE, 'r') as f:
            self.config = json.load(f)

    async def fetch_new_requests(self):
        print("Checking for new friend requests...")
        # Simulated fetch logic - replace with your actual fetch request logic
        new_requests = [("account1", "friend_account1", "remark1"), ("account2", "friend_account2", "remark2")]
        for account, friend_account, remark in new_requests:
            self.add_friend_request(account, friend_account, remark)

    async def auto_approve_friends(self):
        for row in range(self.friend_requests.rowCount()):
            checkbox = self.friend_requests.cellWidget(row, 0)
            if isinstance(checkbox, QCheckBox) and checkbox.isChecked():
                await self.agree_friend(row)

    async def agree_friend(self, row):
        account_item = self.friend_requests.item(row, 1)
        friend_account_item = self.friend_requests.item(row, 2)
        if account_item and friend_account_item:
            print(f"Approving friend request from {friend_account_item.text()} for account {account_item.text()}")
            if self.reply_text or self.reply_image:
                await self.send_auto_reply(friend_account_item.text(), self.reply_text, self.reply_image)
            self.friend_requests.removeRow(row)

    async def send_auto_reply(self, account, message, image_path):
        print(f"Sending auto-reply message to {account}: {message}, with image: {image_path}")
        api_endpoint = "http://example.com/api/sendmessage"  # Replace with actual API
        data = {
            "account": account,
            "message": message,
            "image_path": image_path
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
        checkbox = QCheckBox()
        checkbox.setStyleSheet("margin-left: 20px;")
        self.friend_requests.setCellWidget(row_position, 0, checkbox)
        self.friend_requests.setItem(row_position, 1, QTableWidgetItem(account))
        self.friend_requests.setItem(row_position, 2, QTableWidgetItem(friend_account))
        self.friend_requests.setItem(row_position, 3, QTableWidgetItem(remark))
        agree_button = QPushButton("同意")
        refuse_button = QPushButton("拒绝")
        agree_button.clicked.connect(lambda: asyncio.ensure_future(self.agree_friend(row_position)))
        refuse_button.clicked.connect(lambda: self.refuse_friend(row_position))
        op_layout = QHBoxLayout()
        op_layout.addWidget(agree_button)
        op_layout.addWidget(refuse_button)
        op_layout.setContentsMargins(0, 0, 0, 0)
        op_widget = QWidget()
        op_widget.setLayout(op_layout)
        self.friend_requests.setCellWidget(row_position, 4, op_widget)

    def approve_all_friends(self):
        for row in range(self.friend_requests.rowCount()):
            checkbox = self.friend_requests.cellWidget(row, 0)
            if isinstance(checkbox, QCheckBox) and checkbox.isChecked():
                asyncio.ensure_future(self.agree_friend(row))
        QMessageBox.information(self, "完成", "已自动通过选中的好友申请。")
        self.update_statistics()

    def open_config_dialog(self):
        dialog = FriendConfigDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            config = dialog.get_config()
            self.auto_approve = config["auto_approve"]
            self.auto_reply = config["auto_reply"]
            self.reply_text = config["reply_text"]
            self.reply_image = config["reply_image"]
            QMessageBox.information(self, "配置已保存", "好友通过配置已更新。")

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
