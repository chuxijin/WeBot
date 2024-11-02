from Layout.MomentsContentConfig import *


class MomentsManagementTab(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.module_contents = {}
        self.modules = ["模块A", "模块B", "模块C"]
        self.module_buttons = {}
        self.updateModuleButtons()

    def initUI(self):
        layout = QHBoxLayout(self)

        # Left side module button area
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area_widget = QWidget(scroll_area)

        self.modules_layout = QVBoxLayout(scroll_area_widget)
        self.modules_layout.setSpacing(15)
        self.modules_layout.setContentsMargins(10, 20, 10, 10)

        scroll_area.setWidget(scroll_area_widget)
        scroll_area.setFixedWidth(140)
        layout.addWidget(scroll_area)
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

        # Right-side moments management content
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

    def add_module(self):
        # 添加新模块逻辑
        new_module_name = f"新模块{len(self.modules) + 1}"
        self.modules.append(new_module_name)
        self.updateModuleButtons()

    def updateModuleButtons(self):
        # Clear existing module layout items
        while self.modules_layout.count() > 1:
            item = self.modules_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        # Re-add module buttons
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

    def select_module(self, module):
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
