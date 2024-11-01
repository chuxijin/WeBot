from BasicDefine import *


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
