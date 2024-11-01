from BasicDefine import *
from Layout.FriendConfig import *

class FriendManagementTab(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.auto_approve = True
        self.auto_reply = True
        self.reply_text = ""
        self.reply_image = ""
        self.today_approved = 0
        self.pending_requests = 0

    def initUI(self):
        layout = QVBoxLayout(self)

        # Friend requests group
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

        # 添加全选复选框到表头
        header = self.friend_requests.horizontalHeader()
        self.select_all_checkbox = QCheckBox()
        self.select_all_checkbox.stateChanged.connect(self.select_all_friends)
        header_widget = QWidget()
        header_layout = QHBoxLayout(header_widget)
        header_layout.addWidget(self.select_all_checkbox)
        header_layout.setAlignment(Qt.AlignCenter)
        header_layout.setContentsMargins(0, 0, 0, 0)
        self.friend_requests.setCellWidget(0, 0,
                                           self.select_all_checkbox)  # Placeholder, will adjust after setting row count

        requests_layout.addWidget(self.friend_requests)

        layout.addWidget(requests_group)

        # Statistics
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

        # 初始化统计
        self.update_statistics()

    def select_all_friends(self, state):
        for row in range(self.friend_requests.rowCount()):
            checkbox = self.friend_requests.cellWidget(row, 0)
            if isinstance(checkbox, QCheckBox):
                checkbox.setChecked(state == Qt.Checked)

    def approve_all_friends(self):
        for row in range(self.friend_requests.rowCount()):
            checkbox = self.friend_requests.cellWidget(row, 0)
            if isinstance(checkbox, QCheckBox) and checkbox.isChecked():
                self.agree_friend(row)
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

    def agree_friend(self, row):
        account_item = self.friend_requests.item(row, 1)
        friend_account_item = self.friend_requests.item(row, 2)
        if account_item and friend_account_item:
            account = account_item.text()
            friend_account = friend_account_item.text()
            # TODO: 实现通过好友请求的逻辑，例如调用微信API
            # 更新备注为“微信名 + 当前日期”
            current_date = QDate.currentDate().toString("yyyy-MM-dd")
            new_remark = f"{friend_account} {current_date}"
            self.friend_requests.setItem(row, 3, QTableWidgetItem(new_remark))
            # 发送固定消息
            if self.auto_reply:
                self.send_auto_reply(account, friend_account)
            self.today_approved += 1
            self.pending_requests -= 1
            self.update_statistics()

    def refuse_friend(self, row):
        account_item = self.friend_requests.item(row, 1)
        friend_account_item = self.friend_requests.item(row, 2)
        if account_item and friend_account_item:
            account = account_item.text()
            friend_account = friend_account_item.text()
            # TODO: 实现拒绝好友请求的逻辑，例如调用微信API
            # 可以在备注中标记为已拒绝
            self.friend_requests.setItem(row, 3, QTableWidgetItem("已拒绝"))
            self.pending_requests -= 1
            self.update_statistics()

    def send_auto_reply(self, account, friend_account):
        # TODO: 实现发送自动回复消息的逻辑
        # 可以发送文本消息和图片消息
        print(f"发送自动回复消息给 {friend_account} from {account}: {self.reply_text}")
        if self.reply_image:
            print(f"发送图片: {self.reply_image}")

    def update_statistics(self):
        total = self.friend_requests.rowCount()
        self.total_label.setText(f"好友申请总计: {total}")
        # self.today_approved_label.setText(f"今日已通过: {self.today_approved}")
    # self.pending_label.setText(f"待通过: {self.pending_requests}")
