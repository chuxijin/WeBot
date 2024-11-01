from BasicDefine import *
from Layout.MomentsContentConfig import *


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
