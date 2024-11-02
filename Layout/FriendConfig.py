from BasicDefine import *
from Custom.mySwitchButton import *
from DataManager import *


class FriendConfigDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("好友通过配置")
        self.setFixedSize(400, 400)
        self.initUI()
        self.load_config()

    def initUI(self):
        layout = QVBoxLayout(self)

        # 初始化用户界面控件等...
        auto_approve_layout = QHBoxLayout()
        self.auto_approve_label = QLabel("是否自动通过")
        self.auto_approve_switch = MySwitchControl()
        auto_approve_layout.addWidget(self.auto_approve_label)
        auto_approve_layout.addWidget(self.auto_approve_switch)
        layout.addLayout(auto_approve_layout)

        auto_reject_layout = QHBoxLayout()
        self.auto_reject_label = QLabel("是否自动拒绝")
        self.auto_reject_switch = MySwitchControl()
        auto_reject_layout.addWidget(self.auto_reject_label)
        auto_reject_layout.addWidget(self.auto_reject_switch)
        layout.addLayout(auto_reject_layout)

        reject_keyword_layout = QHBoxLayout()
        self.reject_keyword_label = QLabel("拒绝理由关键字")
        self.reject_keyword_edit = QTextEdit()
        self.reject_keyword_edit.setPlaceholderText("请输入拒绝理由关键字，每行一个")
        reject_keyword_layout.addWidget(self.reject_keyword_label)
        reject_keyword_layout.addWidget(self.reject_keyword_edit)
        layout.addLayout(reject_keyword_layout)

        auto_reply_layout = QHBoxLayout()
        self.auto_reply_label = QLabel("通过后是否自动发送消息")
        self.auto_reply_switch = MySwitchControl()
        auto_reply_layout.addWidget(self.auto_reply_label)
        auto_reply_layout.addWidget(self.auto_reply_switch)
        layout.addLayout(auto_reply_layout)

        self.reply_text = QTextEdit()
        self.reply_text.setPlaceholderText("请输入发送的消息内容")
        layout.addWidget(QLabel("发送的消息内容:"))
        layout.addWidget(self.reply_text)

        image_layout = QHBoxLayout()
        self.image_button = QPushButton("添加图片")
        self.image_button.setIcon(QIcon("icons/add.png"))
        self.image_button.clicked.connect(self.add_image)
        self.selected_image = QLabel("未选择图片")
        image_layout.addWidget(self.image_button)
        image_layout.addWidget(self.selected_image)
        layout.addLayout(image_layout)

        button_layout = QHBoxLayout()
        self.save_button = QPushButton("保存")
        self.save_button.setIcon(QIcon("icons/save.png"))
        self.save_button.clicked.connect(self.save_config)
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

    def save_config(self):
        old_config = {}
        with open(CONFIG_FILE, 'r') as file:
            old_config = json.load(file)
        config = self.get_config()
        config.update(old_config)
        try:
            with open(CONFIG_FILE, 'w') as file:
                json.dump(config, file, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving configuration: {e}")
        self.accept()

    def load_config(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r') as file:
                    config = json.load(file)
                self.auto_approve_switch.setToggle(config.get("auto_approve", False))
                self.auto_reject_switch.setToggle(config.get("auto_reject", False))
                reject_keywords = config.get("reject_keywords", [])
                self.reject_keyword_edit.setPlainText("\n".join(reject_keywords))
                self.auto_reply_switch.setToggle(config.get("auto_reply", False))
                self.reply_text.setPlainText(config.get("reply_text", ""))
                self.selected_image.setText(config.get("reply_image", "未选择图片"))
            except Exception as e:
                print(f"Error loading configuration: {e}")