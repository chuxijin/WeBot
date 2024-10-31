import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTabWidget,
    QPushButton, QTableWidget, QTableWidgetItem, QCheckBox, QLabel,
    QTextEdit, QLineEdit, QGroupBox, QFileDialog, QGridLayout, QHeaderView, QMessageBox, QDialog, QPushButton
)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QIcon, QDragEnterEvent, QDropEvent, QPixmap, QFont
import json
import os

from mySwitchButton import MySwitchControl


class AccountManagementTab(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)

        # Table for account details
        self.account_table = QTableWidget()
        self.account_table.setColumnCount(3)
        self.account_table.setHorizontalHeaderLabels(["账号", "微信名", "端口号"])
        self.account_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.account_table.setSelectionMode(QTableWidget.MultiSelection)
        self.account_table.horizontalHeader().setStretchLastSection(True)
        self.account_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.account_table.setStyleSheet("""
            QTableWidget {
                background-color: #F0F0F0;
                alternate-background-color: #E8E8E8;
                gridline-color: #CCCCCC;
                selection-background-color: #87CEFA;
            }
            QHeaderView::section {
                background-color: #B0C4DE;
                color: white;
                padding: 4px;
                font-size: 14px;
            }
        """)
        layout.addWidget(self.account_table)

        # Buttons layout
        button_layout = QHBoxLayout()
        self.add_button = QPushButton("添加账号")
        self.add_button.setIcon(QIcon("icons/add.png"))
        self.remove_button = QPushButton("删除账号")
        self.remove_button.setIcon(QIcon("icons/delete.png"))
        self.login_button = QPushButton("登录选中账号")
        self.login_button.setIcon(QIcon("icons/login.png"))
        self.select_all_checkbox = QCheckBox("全选")

        # Connect buttons to slots
        self.add_button.clicked.connect(self.add_account)
        self.remove_button.clicked.connect(self.remove_account)
        self.login_button.clicked.connect(self.login_selected_accounts)
        self.select_all_checkbox.stateChanged.connect(self.select_all_accounts)

        # Style buttons
        button_style = """
            QPushButton {
                background-color: #4682B4;
                color: white;
                border: none;
                padding: 8px 16px;
                font-size: 14px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #5A9BD4;
            }
            QPushButton:pressed {
                background-color: #3A78C2;
            }
            QCheckBox {
                font-size: 14px;
            }
        """
        self.add_button.setStyleSheet(button_style)
        self.remove_button.setStyleSheet(button_style)
        self.login_button.setStyleSheet(button_style)
        self.select_all_checkbox.setStyleSheet("font-size: 14px;")

        # Add buttons to layout
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.remove_button)
        button_layout.addWidget(self.login_button)
        button_layout.addWidget(self.select_all_checkbox)
        button_layout.addStretch()

        layout.addLayout(button_layout)

    # Slot functions
    def add_account(self):
        pass  # Implement account addition logic

    def remove_account(self):
        pass  # Implement account removal logic

    def login_selected_accounts(self):
        pass  # Implement login logic for selected accounts

    def select_all_accounts(self, state):
        if state == Qt.Checked:
            self.account_table.selectAll()
        else:
            self.account_table.clearSelection()


class MessageManagementTab(QWidget):
    def __init__(self):
        super().__init__()
        # Define configuration file paths
        self.auto_reply_config_path = "configs/auto_reply_config.json"
        self.external_auto_reply_config_path = "configs/external_auto_reply_config.json"
        self.initUI()
        self.load_auto_reply_config()
        self.load_auto_reply_config()

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



class FriendConfigDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("好友通过配置")
        self.setFixedSize(400, 400)  # 调整窗口高度以适应新增内容
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)

        # 自动通过开关
        auto_approve_layout = QHBoxLayout()
        self.auto_approve_label = QLabel("是否自动通过")
        self.auto_approve_switch = MySwitchControl()
        self.auto_approve_switch.setToggle(True)
        auto_approve_layout.addWidget(self.auto_approve_label)
        auto_approve_layout.addWidget(self.auto_approve_switch)
        layout.addLayout(auto_approve_layout)

        # 自动拒绝开关
        auto_reject_layout = QHBoxLayout()
        self.auto_reject_label = QLabel("是否自动拒绝")
        self.auto_reject_switch = MySwitchControl()
        self.auto_reject_switch.setToggle(False)
        auto_reject_layout.addWidget(self.auto_reject_label)
        auto_reject_layout.addWidget(self.auto_reject_switch)
        layout.addLayout(auto_reject_layout)

        # 拒绝的关键字设置
        reject_keyword_layout = QHBoxLayout()
        self.reject_keyword_label = QLabel("拒绝理由关键字")
        self.reject_keyword_edit = QTextEdit()
        self.reject_keyword_edit.setPlaceholderText("请输入拒绝理由关键字，每行一个")
        reject_keyword_layout.addWidget(self.reject_keyword_label)
        reject_keyword_layout.addWidget(self.reject_keyword_edit)
        layout.addLayout(reject_keyword_layout)

        # 自动发送消息开关
        auto_reply_layout = QHBoxLayout()
        self.auto_reply_label = QLabel("通过后是否自动发送消息")
        self.auto_reply_switch = MySwitchControl()
        self.auto_reply_switch.setToggle(True)
        auto_reply_layout.addWidget(self.auto_reply_label)
        auto_reply_layout.addWidget(self.auto_reply_switch)
        layout.addLayout(auto_reply_layout)

        # 发送的消息内容（文本）
        self.reply_text = QTextEdit()
        self.reply_text.setPlaceholderText("请输入发送的消息内容")
        layout.addWidget(QLabel("发送的消息内容:"))
        layout.addWidget(self.reply_text)

        # 发送的消息内容（图片）
        image_layout = QHBoxLayout()
        self.image_button = QPushButton("添加图片")
        self.image_button.setIcon(QIcon("icons/add.png"))
        self.image_button.clicked.connect(self.add_image)
        self.selected_image = QLabel("未选择图片")
        image_layout.addWidget(self.image_button)
        image_layout.addWidget(self.selected_image)
        layout.addLayout(image_layout)

        # 保存和取消按钮
        button_layout = QHBoxLayout()
        self.save_button = QPushButton("保存")
        self.save_button.setIcon(QIcon("icons/save.png"))
        self.save_button.clicked.connect(self.accept)
        self.cancel_button = QPushButton("取消")
        self.cancel_button.setIcon(QIcon("icons/cancel.png"))
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addStretch()
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)

    def add_image(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择图片", "", "Image Files (*.png *.jpg *.bmp)"
        )
        if file_path:
            self.selected_image.setText(file_path)

    def get_config(self):
        reject_keywords = self.reject_keyword_edit.toPlainText().strip().split('\n')
        reject_keywords = [kw.strip() for kw in reject_keywords if kw.strip()]

        return {
            "auto_approve": self.auto_approve_switch.isToggled(),
            "auto_reject": self.auto_reject_switch.isToggled(),
            "reject_keywords": reject_keywords,
            "auto_reply": self.auto_reply_switch.isToggled(),
            "reply_text": self.reply_text.toPlainText(),
            "reply_image": self.selected_image.text() if self.selected_image.text() != "未选择图片" else ""
        }


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
        #self.today_approved_label.setText(f"今日已通过: {self.today_approved}")
       # self.pending_label.setText(f"待通过: {self.pending_requests}")


class GroupMessageConfigDialog(QDialog):
    def __init__(self, parent=None, module_name=""):
        super().__init__(parent)
        self.setWindowTitle(f"{module_name} 消息设置")
        self.setFixedSize(400, 300)
        self.module_name = module_name
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)

        # 消息内容
        self.message_text = QTextEdit()
        self.message_text.setPlaceholderText("请输入发送的消息内容")
        layout.addWidget(QLabel("发送的消息内容:"))
        layout.addWidget(self.message_text)

        # 保存和取消按钮
        button_layout = QHBoxLayout()
        self.save_button = QPushButton("保存")
        self.save_button.clicked.connect(self.accept)
        self.cancel_button = QPushButton("取消")
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addStretch()
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)

    def get_message(self):
        return self.message_text.toPlainText()


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


class MomentsContentConfigDialog(QDialog):
    def __init__(self, parent=None, module_name=""):
        super().__init__(parent)
        self.setWindowTitle(f"{module_name} 朋友圈内容设置")
        self.setFixedSize(400, 350)
        self.module_name = module_name
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)

        # 图片上传
        self.image_button = QPushButton("添加图片")
        self.image_button.clicked.connect(self.add_image)
        self.selected_image = QLabel("未选择图片")
        image_layout = QHBoxLayout()
        image_layout.addWidget(self.image_button)
        image_layout.addWidget(self.selected_image)
        layout.addLayout(image_layout)

        # 文字内容
        self.moments_text = QTextEdit()
        self.moments_text.setPlaceholderText("请输入朋友圈文字内容")
        layout.addWidget(QLabel("朋友圈文字内容:"))
        layout.addWidget(self.moments_text)

        # 保存和取消按钮
        button_layout = QHBoxLayout()
        self.save_button = QPushButton("保存")
        self.save_button.clicked.connect(self.accept)
        self.cancel_button = QPushButton("取消")
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addStretch()
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)

    def add_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "选择图片", "", "Image Files (*.png *.jpg *.bmp)")
        if file_path:
            self.selected_image.setText(file_path)

    def get_content(self):
        return {
            "image": self.selected_image.text(),
            "text": self.moments_text.toPlainText()
        }


class MomentsManagementTab(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.module_contents = {}  # 存储各模块的朋友圈内容

    def initUI(self):
        layout = QHBoxLayout(self)

        # 左侧模块按钮区域
        modules_layout = QVBoxLayout()
        self.modules = ["模块A", "模块B", "模块C"]  # 预留模块名称
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

        # 右侧朋友圈管理内容
        moments_management_layout = QVBoxLayout()

        # Account info
        account_layout = QHBoxLayout()
        account_label = QLabel("当前账号:")
        account_label.setFont(QFont("Arial", 12))
        self.current_account_label = QLabel("未选择账号")
        self.current_account_label.setStyleSheet("color: #FF4500; font-weight: bold;")
        account_layout.addWidget(account_label)
        account_layout.addWidget(self.current_account_label)
        account_layout.addStretch()
        moments_management_layout.addLayout(account_layout)

        # Moments content group
        moments_group = QGroupBox("朋友圈内容")
        moments_group.setStyleSheet("""
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
        moments_layout = QVBoxLayout(moments_group)

        # Image upload with drag and drop
        self.image_label = QLabel("拖拽图片到这里")
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet("""
            QLabel {
                border: 2px dashed #A9A9A9;
                background-color: #F8F8FF;
                color: #696969;
                font-size: 14px;
            }
        """)
        self.image_label.setFixedHeight(200)
        self.image_label.setAcceptDrops(True)
        self.image_label.setPixmap(QPixmap())
        self.image_label.dragEnterEvent = self.dragEnterEvent
        self.image_label.dropEvent = self.dropEvent
        moments_layout.addWidget(self.image_label)

        # Text input
        self.moments_text = QTextEdit()
        self.moments_text.setPlaceholderText("请输入朋友圈文字内容")
        self.moments_text.setStyleSheet("""
            QTextEdit {
                background-color: #FAFAD2;
                color: #000000;
                font-size: 14px;
            }
        """)
        moments_layout.addWidget(self.moments_text)

        moments_group.setLayout(moments_layout)
        moments_management_layout.addWidget(moments_group)

        # Send button
        send_layout = QHBoxLayout()
        self.send_moments_button = QPushButton("一键发送朋友圈")
        self.send_moments_button.setIcon(QIcon("icons/send.png"))
        self.send_moments_button.setStyleSheet("""
            QPushButton {
                background-color: #8A2BE2;
                color: white;
                border: none;
                padding: 10px 20px;
                font-size: 14px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #9400D3;
            }
            QPushButton:pressed {
                background-color: #9932CC;
            }
        """)
        self.send_moments_button.clicked.connect(self.send_moments)
        send_layout.addWidget(self.send_moments_button)
        send_layout.addStretch()
        moments_management_layout.addLayout(send_layout)

        layout.addLayout(moments_management_layout)

    def select_module(self, module):
        # 根据选择的模块加载对应的朋友圈内容
        content = self.module_contents.get(module, {})
        self.moments_text.setPlainText(content.get("text", ""))
        image_path = content.get("image", "")
        if image_path:
            pixmap = QPixmap(image_path)
            self.image_label.setPixmap(pixmap.scaled(
                self.image_label.width(), self.image_label.height(),
                Qt.KeepAspectRatio, Qt.SmoothTransformation
            ))
        else:
            self.image_label.setText("拖拽图片到这里")

    def configure_module(self, module):
        dialog = MomentsContentConfigDialog(self, module)
        if dialog.exec_() == QDialog.Accepted:
            content = dialog.get_content()
            self.module_contents[module] = content
            QMessageBox.information(self, "保存成功", f"{module} 的朋友圈内容已保存。")

    def send_moments(self):
        selected_modules = [m for m, btn in self.module_buttons.items() if btn.isChecked()]
        for module in selected_modules:
            content = self.module_contents.get(module, {})
            message = content.get("text", "")
            image_path = content.get("image", "")
            if message or image_path:
                # TODO: Implement sending moments to accounts based on module
                print(f"发送朋友圈 - 模块: {module}, 内容: {message}, 图片: {image_path}")
            else:
                QMessageBox.warning(self, "警告", f"模块 {module} 没有配置朋友圈内容。")


class WeChatBotManager(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("WeChat 多用户机器人管理")
        self.resize(1300, 900)
        self.setStyleSheet("""
            QWidget {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background-color: #FFFFFF;
            }
            QTabWidget::pane {
                border: 1px solid #CCCCCC;
                background: #FFFFFF;
            }
            QTabBar::tab {
                background: #F5F5F5;
                color: #000000;
                padding: 10px;
                font-size: 14px;
                border: 1px solid #CCCCCC;
                border-bottom: none;
                border-radius: 4px 4px 0 0;
            }
            QTabBar::tab:selected {
                background: #FFFFFF;
                border-bottom: 1px solid #FFFFFF;
            }
            QTabBar::tab:hover {
                background: #E0E0E0;
            }
        """)

        layout = QVBoxLayout(self)

        # Tab Widget
        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)

        # Add tabs
        self.account_tab = AccountManagementTab()
        self.message_tab = MessageManagementTab()
        self.friend_tab = FriendManagementTab()
        self.group_tab = GroupManagementTab()
        self.moments_tab = MomentsManagementTab()

        self.tabs.addTab(self.account_tab, QIcon("icons/account.png"), "账号管理")
        self.tabs.addTab(self.message_tab, QIcon("icons/message.png"), "消息管理")
        self.tabs.addTab(self.friend_tab, QIcon("icons/friend.png"), "好友管理")
        self.tabs.addTab(self.group_tab, QIcon("icons/group.png"), "群管理")
        self.tabs.addTab(self.moments_tab, QIcon("icons/moments.png"), "朋友圈管理")

        # Connect account management selection to update other tabs
        self.account_tab.account_table.itemSelectionChanged.connect(self.update_other_tabs)

    def update_other_tabs(self):
        selected_accounts = self.get_selected_accounts()
        # 根据选中的账号更新其他标签的数据
        # 这里只是示例，实际实现需要根据具体数据源进行更新
        # 示例：在朋友圈管理标签中显示第一个选中的账号
        if selected_accounts:
            self.moments_tab.set_current_account(selected_accounts[0])
        else:
            self.moments_tab.set_current_account("未选择账号")

    def get_selected_accounts(self):
        selected_rows = self.account_tab.account_table.selectionModel().selectedRows()
        accounts = []
        for row in selected_rows:
            account_item = self.account_tab.account_table.item(row.row(), 0)
            if account_item:
                accounts.append(account_item.text())
        return accounts
def main():
    app = QApplication(sys.argv)
    window = WeChatBotManager()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
