from Layout.GroupMessageConfig import *


class GroupManagementTab(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.module_messages = {}  # 存储各模块的消息内容
        self.modules = ["模块1", "模块2", "模块3"]  # 预留模块名称
        self.updateModuleButtons()

    def initUI(self):
        layout = QHBoxLayout(self)

        # 滚动区域
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area_widget = QWidget(scroll_area)

        # 模块布局设置
        self.modules_layout = QVBoxLayout(scroll_area_widget)
        self.modules_layout.setSpacing(10)  # 设置模块之间的固定间距

        # 添加模块按钮
        add_module_button = QPushButton("+")
        add_module_button.setFixedSize(30, 30)
        add_module_button.setStyleSheet("""
            QPushButton {
                background-color: #FF0000;  # Bright red color
                color: white;
                font-weight: bold;
                border-radius: 15px;
            }
            QPushButton:hover {
                background-color: #FF3333;  # Lighter red on hover
            }
            QPushButton:pressed {
                background-color: #CC0000;  # Darker red when pressed
            }
        """)
        add_module_button.clicked.connect(self.add_module)
        self.modules_layout.addWidget(add_module_button, alignment=Qt.AlignCenter)

        scroll_area.setWidget(scroll_area_widget)
        scroll_area.setFixedWidth(120)  # 设置固定宽度
        layout.addWidget(scroll_area)

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

    def updateModuleButtons(self):
        # 清除现有的模块布局项
        while self.modules_layout.count() > 1:  # 保留添加模块的按钮
            item = self.modules_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        # 重新添加模块按钮
        for module in self.modules:
            btn = QPushButton(module, self)
            btn.setFixedSize(80, 80)
            btn.setIcon(QIcon("icons/module.png"))
            btn.setIconSize(QSize(40, 40))
            btn.setStyleSheet("""
                QPushButton {
                    border: 1px solid #DDDDDD;
                    border-radius: 10px;
                    background-color: #F0F0F0;
                    margin: 10px 0;  # Add fixed vertical spacing between buttons
                }
                QPushButton:hover {
                    background-color: #E0E0E0;
                }
                QPushButton:pressed {
                    background-color: #D0D0D0;
                }
            """)
            btn.clicked.connect(lambda checked, m=module: self.configure_module(m))

            # 创建关闭按钮，并放置在模块按钮的右上角
            close_btn = QPushButton("x", btn)
            close_btn.setFixedSize(16, 16)
            close_btn.setStyleSheet("""
                QPushButton {
                    background-color: #FF0000;  # Bright red color
                    color: white;
                    border: none;
                    font-size: 12px;
                    border-radius: 8px;
                }
                QPushButton:hover {
                    background-color: #FF3333;  # Lighter red on hover
                }
                QPushButton:pressed {
                    background-color: #CC0000;  # Darker red when pressed
                }
            """)
            close_btn.move(btn.width() - close_btn.width(), 0)
            close_btn.clicked.connect(lambda checked, m=module: self.remove_module(m))

            self.modules_layout.insertWidget(self.modules_layout.count() - 1, btn, alignment=Qt.AlignTop)

    def configure_module(self, module):
        # 弹出配置对话框
        dialog = GroupMessageConfigDialog(self, module)
        if dialog.exec_() == QDialog.Accepted:
            message = dialog.get_message()
            self.module_messages[module] = message
            QMessageBox.information(self, "保存成功", f"{module} 的消息内容已保存。")

    def add_module(self):
        # 添加新模块逻辑
        new_module_name = f"新模块{len(self.modules) + 1}"
        self.modules.append(new_module_name)
        self.updateModuleButtons()
        # QMessageBox.information(self, "模块添加", f"{new_module_name} 已添加。")

    def remove_module(self, module):
        # 移除模块逻辑
        if module in self.modules:
            self.modules.remove(module)
            self.updateModuleButtons()

    def send_message_to_groups(self):
        selected_modules = [m for m in self.modules]
        for module in selected_modules:
            message = self.module_messages.get(module, "")
            if message:
                # TODO: 实现将消息发送到组的逻辑
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