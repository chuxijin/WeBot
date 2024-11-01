from BasicDefine import *
from Custom.mySwitchButton import *

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
