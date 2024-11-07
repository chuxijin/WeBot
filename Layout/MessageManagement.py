from BasicDefine import *
from Handle_Server import *


class MessageManagementTab(QWidget):
    def __init__(self):
        super().__init__()
        # Define configuration file paths
        self.auto_reply_config_path = "configs/auto_reply_config.json"
        self.external_auto_reply_config_path = "configs/external_auto_reply_config.json"
        self.initUI()
        self.load_auto_reply_config()
        self.load_auto_reply_config()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_pending_messages)
        self.timer.start(5000)

    def initUI(self):
            layout = QVBoxLayout(self)

            # Auto-reply group
            auto_reply_group = QGroupBox("关键字自动回复")
            auto_reply_group.setStyleSheet("""
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
            auto_reply_layout = QVBoxLayout(auto_reply_group)

            self.auto_reply_list = QTableWidget()
            self.auto_reply_list.setColumnCount(4)
            self.auto_reply_list.setHorizontalHeaderLabels(["账号", "关键字", "回复内容", "操作"])
            self.auto_reply_list.horizontalHeader().setStretchLastSection(True)
            self.auto_reply_list.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            self.auto_reply_list.setStyleSheet("""
                QTableWidget {
                    background-color: #F0F8FF;
                    alternate-background-color: #E6F2FF;
                    gridline-color: #ADD8E6;
                    selection-background-color: #87CEFA;
                }
                QHeaderView::section {
                    background-color: #4682B4;
                    color: white;
                    padding: 4px;
                    font-size: 14px;
                }
                QPushButton {
                    background-color: #4682B4;
                    color: white;
                    border: none;
                    padding: 6px 12px;
                    font-size: 12px;
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background-color: #5A9BD4;
                }
                QPushButton:pressed {
                    background-color: #3A78C2;
                }
            """)
            auto_reply_layout.addWidget(self.auto_reply_list)

            # Buttons for auto-reply
            auto_reply_buttons = QHBoxLayout()
            self.add_reply_button = QPushButton("添加规则")
            self.add_reply_button.setIcon(QIcon("icons/add.png"))
            self.remove_reply_button = QPushButton("删除规则")
            self.remove_reply_button.setIcon(QIcon("icons/delete.png"))
            self.save_reply_button = QPushButton("保存配置")
            self.save_reply_button.setIcon(QIcon("icons/save.png"))

            # self.add_reply_button.clicked.connect(self.add_auto_reply)
            # self.remove_reply_button.clicked.connect(self.remove_auto_reply)
            # self.save_reply_button.clicked.connect(self.save_auto_reply)

            # Style buttons
            button_style = """
                QPushButton {
                    background-color: #32CD32;
                    color: white;
                    border: none;
                    padding: 8px 16px;
                    font-size: 14px;
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background-color: #3CB371;
                }
                QPushButton:pressed {
                    background-color: #2E8B57;
                }
            """
            self.add_reply_button.setStyleSheet(button_style)
            self.remove_reply_button.setStyleSheet(button_style)
            self.save_reply_button.setStyleSheet(button_style)

            auto_reply_buttons.addWidget(self.add_reply_button)
            auto_reply_buttons.addWidget(self.remove_reply_button)
            auto_reply_buttons.addWidget(self.save_reply_button)
            auto_reply_buttons.addStretch()

            auto_reply_layout.addLayout(auto_reply_buttons)

            layout.addWidget(auto_reply_group)

            # External Auto-reply Type
            external_reply_group = QGroupBox("外部接口关键字自动回复")
            external_reply_group.setStyleSheet("""
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
            external_reply_layout = QVBoxLayout(external_reply_group)

            self.external_reply_list = QTableWidget()
            self.external_reply_list.setColumnCount(5)
            self.external_reply_list.setHorizontalHeaderLabels(["账号", "关键字", "模式", "调用接口", "操作"])
            self.external_reply_list.horizontalHeader().setStretchLastSection(True)
            self.external_reply_list.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            self.external_reply_list.setStyleSheet("""
                QTableWidget {
                    background-color: #E6E6FA;
                    alternate-background-color: #D8BFD8;
                    gridline-color: #DDA0DD;
                    selection-background-color: #BA55D3;
                }
                QHeaderView::section {
                    background-color: #800080;
                    color: white;
                    padding: 4px;
                    font-size: 14px;
                }
                QPushButton {
                    background-color: #800080;
                    color: white;
                    border: none;
                    padding: 6px 12px;
                    font-size: 12px;
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background-color: #9932CC;
                }
                QPushButton:pressed {
                    background-color: #8A2BE2;
                }
            """)
            external_reply_layout.addWidget(self.external_reply_list)

            # Buttons for external auto-reply
            external_reply_buttons = QHBoxLayout()
            self.add_external_reply_button = QPushButton("添加外部规则")
            self.add_external_reply_button.setIcon(QIcon("icons/add.png"))
            self.remove_external_reply_button = QPushButton("删除外部规则")
            self.remove_external_reply_button.setIcon(QIcon("icons/delete.png"))
            self.save_external_reply_button = QPushButton("保存外部配置")
            self.save_external_reply_button.setIcon(QIcon("icons/save.png"))

            # self.add_external_reply_button.clicked.connect(self.add_external_auto_reply)
            # self.remove_external_reply_button.clicked.connect(self.remove_external_auto_reply)
            # self.save_external_reply_button.clicked.connect(self.save_external_auto_reply)

            # Style buttons
            external_button_style = """
                QPushButton {
                    background-color: #6A5ACD;
                    color: white;
                    border: none;
                    padding: 8px 16px;
                    font-size: 14px;
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background-color: #7B68EE;
                }
                QPushButton:pressed {
                    background-color: #483D8B;
                }
            """
            self.add_external_reply_button.setStyleSheet(external_button_style)
            self.remove_external_reply_button.setStyleSheet(external_button_style)
            self.save_external_reply_button.setStyleSheet(external_button_style)

            external_reply_buttons.addWidget(self.add_external_reply_button)
            external_reply_buttons.addWidget(self.remove_external_reply_button)
            external_reply_buttons.addWidget(self.save_external_reply_button)
            external_reply_buttons.addStretch()

            external_reply_layout.addLayout(external_reply_buttons)

            external_reply_group.setLayout(external_reply_layout)
            layout.addWidget(external_reply_group)

            # Log group
            log_group = QGroupBox("日志记录")
            log_group.setStyleSheet("""
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
            log_layout = QVBoxLayout(log_group)

            self.log_text = QTextEdit()
            self.log_text.setReadOnly(True)
            self.log_text.setStyleSheet("""
                QTextEdit {
                    background-color: #FFFACD;
                    color: #000000;
                    font-size: 14px;
                }
            """)
            log_layout.addWidget(self.log_text)

            log_group.setLayout(log_layout)
            layout.addWidget(log_group)

            # Pending messages group
            pending_group = QGroupBox("待处理消息")
            pending_group.setStyleSheet("""
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
            pending_layout = QVBoxLayout(pending_group)

            self.pending_messages = QTableWidget()
            self.pending_messages.setColumnCount(4)
            self.pending_messages.setHorizontalHeaderLabels(["账号", "发送者", "消息内容", "操作"])
            self.pending_messages.horizontalHeader().setStretchLastSection(True)
            self.pending_messages.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            self.pending_messages.setStyleSheet("""
                QTableWidget {
                    background-color: #F0FFF0;
                    alternate-background-color: #E0FFE0;
                    gridline-color: #90EE90;
                    selection-background-color: #7CFC00;
                }
                QHeaderView::section {
                    background-color: #228B22;
                    color: white;
                    padding: 4px;
                    font-size: 14px;
                }
                QPushButton {
                    background-color: #FFA500;
                    color: white;
                    border: none;
                    padding: 4px 8px;
                    font-size: 12px;
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background-color: #FF8C00;
                }
                QPushButton:pressed {
                    background-color: #FF7F50;
                }
            """)

            pending_layout.addWidget(self.pending_messages)

            # Buttons for pending messages
            pending_buttons = QHBoxLayout()
            self.process_message_button = QPushButton("处理选中消息")
            self.process_message_button.setIcon(QIcon("icons/process.png"))
            self.refresh_pending_button = QPushButton("刷新待处理消息")
            self.refresh_pending_button.setIcon(QIcon("icons/refresh.png"))

            self.process_message_button.clicked.connect(self.process_selected_messages)
            self.refresh_pending_button.clicked.connect(self.refresh_pending_messages)

            # Style buttons
            pending_button_style = """
                QPushButton {
                    background-color: #FF8C00;
                    color: white;
                    border: none;
                    padding: 8px 16px;
                    font-size: 14px;
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background-color: #FFA500;
                }
                QPushButton:pressed {
                    background-color: #FF6EB4;
                }
            """
            self.process_message_button.setStyleSheet(pending_button_style)
            self.refresh_pending_button.setStyleSheet(pending_button_style)

            pending_buttons.addWidget(self.process_message_button)
            pending_buttons.addWidget(self.refresh_pending_button)
            pending_buttons.addStretch()

            pending_layout.addLayout(pending_buttons)

            pending_group.setLayout(pending_layout)
            layout.addWidget(pending_group)

    def update_pending_messages(self):
        """Timer triggered method to update pending messages"""
        new_messages = fetch_messages()
        if new_messages:
            for msg_content in new_messages:
                self.add_pending_message_row(msg_content)

    def add_pending_message_row(self, msg):
        """Add a new row in the pending messages table"""
        row_position = self.pending_messages.rowCount()
        self.pending_messages.insertRow(row_position)
        self.pending_messages.setItem(row_position, 0, QTableWidgetItem("账号示例"))
        self.pending_messages.setItem(row_position, 1, QTableWidgetItem(msg['from']))
        self.pending_messages.setItem(row_position, 2, QTableWidgetItem(msg['content']))
        # Add an operation button
        operation_btn = QPushButton("处理")
        operation_btn.clicked.connect(lambda: self.handle_pending_message(row_position))
        self.pending_messages.setCellWidget(row_position, 3, operation_btn)

    def load_auto_reply_config(self):
        """加载普通自动回复配置到表格"""
        if not os.path.exists(self.auto_reply_config_path):
            # Ensure the directory exists
            os.makedirs(os.path.dirname(self.auto_reply_config_path), exist_ok=True)
            # Create an empty config file
            with open(self.auto_reply_config_path, 'w', encoding='utf-8') as f:
                json.dump([], f, ensure_ascii=False, indent=4)

        with open(self.auto_reply_config_path, 'r', encoding='utf-8') as f:
            try:
                config = json.load(f)
            except json.JSONDecodeError:
                QMessageBox.warning(self, "加载配置失败", "普通自动回复配置文件格式错误。")
                config = []

        self.auto_reply_list.setRowCount(0)
        for rule in config:
            self.add_auto_reply_row(rule)

    def add_auto_reply_row(self, rule=None):
        """向自动回复表格添加一行"""
        row_position = self.auto_reply_list.rowCount()
        self.auto_reply_list.insertRow(row_position)

        account_item = QTableWidgetItem(rule.get("account", "") if rule else "")
        keyword_item = QTableWidgetItem(rule.get("keyword", "") if rule else "")
        reply_content_item = QTableWidgetItem(rule.get("reply_content", "") if rule else "")

        self.auto_reply_list.setItem(row_position, 0, account_item)
        self.auto_reply_list.setItem(row_position, 1, keyword_item)
        self.auto_reply_list.setItem(row_position, 2, reply_content_item)

        # 操作按钮
        operation_btn = QPushButton("删除")
        operation_btn.setStyleSheet("""
            QPushButton {
                background-color: #FF6347;
                color: white;
                border: none;
                padding: 6px 12px;
                font-size: 12px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #FF4500;
            }
            QPushButton:pressed {
                background-color: #CD5C5C;
            }
        """)
        operation_btn.clicked.connect(lambda: self.delete_external_auto_reply_row(row_position))
        self.external_reply_list.setCellWidget(row_position, 4, operation_btn)

    def add_external_auto_reply(self):
        """添加外部接口自动回复规则"""
        self.add_external_auto_reply_row()

    def delete_external_auto_reply_row(self, row):
        """删除指定行的外部接口自动回复规则"""
        self.external_reply_list.removeRow(row)
        # 重新连接操作按钮以防行号变化
        self.refresh_external_auto_reply_operations()

    def refresh_external_auto_reply_operations(self):
        """刷新外部接口自动回复表格中操作按钮的行号"""
        for row in range(self.external_reply_list.rowCount()):
            btn = self.external_reply_list.cellWidget(row, 4)
            if btn:
                # Disconnect previous connections
                try:
                    btn.clicked.disconnect()
                except:
                    pass
                # Connect with the correct row
                btn.clicked.connect(lambda checked, r=row: self.delete_external_auto_reply_row(r))

    def save_external_auto_reply(self):
        """保存外部接口自动回复配置到JSON文件"""
        config = []
        for row in range(self.external_reply_list.rowCount()):
            account_item = self.external_reply_list.item(row, 0)
            keyword_item = self.external_reply_list.item(row, 1)
            mode_widget = self.external_reply_list.cellWidget(row, 2)
            interface_url_item = self.external_reply_list.item(row, 3)

            account = account_item.text().strip() if account_item else ""
            keyword = keyword_item.text().strip() if keyword_item else ""
            mode = mode_widget.currentText() if mode_widget else ""
            interface_url = interface_url_item.text().strip() if interface_url_item else ""

            if account and keyword and mode and interface_url:
                config.append({
                    "account": account,
                    "keyword": keyword,
                    "mode": mode,
                    "interface_url": interface_url
                })
            else:
                QMessageBox.warning(self, "保存失败", f"第{row + 1}行存在空字段，请填写完整。")
                return

        with open(self.external_auto_reply_config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=4)
        QMessageBox.information(self, "保存成功", "外部接口自动回复配置已成功保存。")

    def process_selected_messages(self):
        """处理选中的待处理消息"""
        # 实现具体逻辑，例如审核消息、删除消息等
        selected_rows = set()
        for item in self.pending_messages.selectedItems():
            selected_rows.add(item.row())
        if not selected_rows:
            QMessageBox.information(self, "提示", "请先选择要处理的消息。")
            return

        for row in sorted(selected_rows, reverse=True):
            # 这里可以添加具体的处理逻辑
            self.pending_messages.removeRow(row)

        QMessageBox.information(self, "处理完成", "选中的消息已被处理。")

    def refresh_pending_messages(self):
        """刷新待处理消息列表"""
        # 实现具体的刷新逻辑，例如从数据库或API获取最新的待处理消息
        # 这里提供一个示例，添加一条假消息
        row_position = self.pending_messages.rowCount()
        self.pending_messages.insertRow(row_position)
        self.pending_messages.setItem(row_position, 0, QTableWidgetItem("账号示例"))
        self.pending_messages.setItem(row_position, 1, QTableWidgetItem("发送者示例"))
        self.pending_messages.setItem(row_position, 2, QTableWidgetItem("消息内容示例"))

        # 操作按钮（例如审核通过或拒绝）
        operation_btn = QPushButton("处理")
        operation_btn.setStyleSheet("""
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
        operation_btn.clicked.connect(lambda: self.handle_pending_message(row_position))
        self.pending_messages.setCellWidget(row_position, 3, operation_btn)

    def handle_pending_message(self, row):
        """处理单条待处理消息"""
        # 实现具体的处理逻辑
        # 例如，弹出审核窗口，决定通过或拒绝
        # 这里只是简单地删除该行
        self.pending_messages.removeRow(row)
        QMessageBox.information(self, "处理完成", "该消息已被处理。")
