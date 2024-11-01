from BasicDefine import *
from Layout.GroupMessageConfig import *


class GroupManagementTab(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.module_messages = {}  # 存储各模块的消息内容

    def initUI(self):
        layout = QHBoxLayout(self)

        # 左侧模块按钮区域
        modules_layout = QVBoxLayout()
        self.modules = ["模块1", "模块2", "模块3"]  # 预留模块名称
        self.module_buttons = {}
        for module in self.modules:
            btn_layout = QHBoxLayout()
            btn = QPushButton(module)
            btn.setIcon(QIcon("icons/module.png"))
            btn.clicked.connect(lambda checked, m=module: self.select_module(m))
            settings_btn = QPushButton("...")
            settings_btn.setFixedSize(20, 20)
            settings_btn.setIcon(QIcon("icons/settings.png"))
            settings_btn.clicked.connect(lambda checked, m=module: self.configure_module(m))
            btn_layout.addWidget(btn)
            btn_layout.addWidget(settings_btn)
            btn_layout.addStretch()
            modules_layout.addLayout(btn_layout)
            self.module_buttons[module] = btn

        modules_layout.addStretch()
        layout.addLayout(modules_layout)

        # 右侧群管理内容
        group_management_layout = QVBoxLayout()

        # Filter layout
        filter_layout = QHBoxLayout()
        filter_label = QLabel("筛选关键字:")
        filter_label.setFont(QFont("Arial", 12))
        self.filter_input = QLineEdit()
        self.filter_input.setPlaceholderText("输入关键字筛选群名（多个关键字用逗号分隔）")
        self.filter_input.textChanged.connect(self.filter_groups)
        filter_layout.addWidget(filter_label)
        filter_layout.addWidget(self.filter_input)
        filter_layout.addStretch()
        group_management_layout.addLayout(filter_layout)

        # Group list group
        group_list_group = QGroupBox("群管理")
        group_list_group.setStyleSheet("""
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
        group_list_layout = QVBoxLayout(group_list_group)

        self.group_list_table = QTableWidget()
        self.group_list_table.setColumnCount(4)
        self.group_list_table.setHorizontalHeaderLabels(["账号", "群名", "关键字", "操作"])
        self.group_list_table.horizontalHeader().setStretchLastSection(True)
        self.group_list_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.group_list_table.setStyleSheet("""
            QTableWidget {
                background-color: #F5FFFA;
                alternate-background-color: #E0FFFF;
                gridline-color: #AFEEEE;
                selection-background-color: #20B2AA;
            }
            QHeaderView::section {
                background-color: #2E8B57;
                color: white;
                padding: 4px;
                font-size: 14px;
            }
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
                background-color: #CD3700;
            }
        """)
        group_list_layout.addWidget(self.group_list_table)

        group_management_layout.addWidget(group_list_group)

        # Input message
        message_group = QGroupBox("发送消息")
        message_group.setStyleSheet("""
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
        message_layout = QVBoxLayout(message_group)
        self.group_message_input = QTextEdit()
        self.group_message_input.setPlaceholderText("请输入要发送的消息")
        self.group_message_input.setStyleSheet("""
            QTextEdit {
                background-color: #FFFACD;
                color: #000000;
                font-size: 14px;
            }
        """)
        message_layout.addWidget(self.group_message_input)
        message_group.setLayout(message_layout)
        group_management_layout.addWidget(message_group)

        # Send button
        send_layout = QHBoxLayout()
        self.send_to_groups_button = QPushButton("一键发送到所有群")
        self.send_to_groups_button.setIcon(QIcon("icons/send.png"))
        self.send_to_groups_button.setStyleSheet("""
            QPushButton {
                background-color: #FF1493;
                color: white;
                border: none;
                padding: 10px 20px;
                font-size: 14px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #FF69B4;
            }
            QPushButton:pressed {
                background-color: #FF6EB4;
            }
        """)
        self.send_to_groups_button.clicked.connect(self.send_message_to_groups)
        send_layout.addWidget(self.send_to_groups_button)
        send_layout.addStretch()
        group_management_layout.addLayout(send_layout)

        layout.addLayout(group_management_layout)

    def select_module(self, module):
        # 根据选择的模块加载对应的消息内容
        message = self.module_messages.get(module, "")
        self.group_message_input.setPlainText(message)

    def configure_module(self, module):
        dialog = GroupMessageConfigDialog(self, module)
        if dialog.exec_() == QDialog.Accepted:
            message = dialog.get_message()
            self.module_messages[module] = message
            QMessageBox.information(self, "保存成功", f"{module} 的消息内容已保存。")

    def send_message_to_groups(self):
        selected_modules = [m for m, btn in self.module_buttons.items() if btn.isChecked()]
        for module in selected_modules:
            message = self.module_messages.get(module, "")
            if message:
                # TODO: Implement sending message to groups based on module
                print(f"发送消息到所有群 - 模块: {module}, 内容: {message}")
            else:
                QMessageBox.warning(self, "警告", f"模块 {module} 没有配置消息内容。")

    def filter_groups(self, text):
        keywords = [kw.strip().lower() for kw in text.split(',') if kw.strip()]
        for row in range(self.group_list_table.rowCount()):
            group_name_item = self.group_list_table.item(row, 1)
            if group_name_item:
                group_name = group_name_item.text().lower()
                if any(kw in group_name for kw in keywords):
                    self.group_list_table.setRowHidden(row, False)
                else:
                    self.group_list_table.setRowHidden(row, True)
