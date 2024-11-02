from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem

from BasicDefine import *


class SendMsgManagementTab(QWidget):
    def __init__(self):
        super().__init__()

        # 初始化UI
        self.init_ui()

    def init_ui(self):
        # 设置窗口标题和初始大小
        self.setWindowTitle('微信消息模拟界面')
        self.setGeometry(100, 100, 600, 500)

        # 主布局
        main_layout = QHBoxLayout()

        # 创建账号和好友的树形结构
        self.account_tree = QTreeWidget(self)
        self.account_tree.setHeaderLabel('通讯录')
        self.build_account_tree()
        main_layout.addWidget(self.account_tree, 1)  # 占1/4的宽度

        # 右侧的布局，包含消息列表和发送框
        right_layout = QVBoxLayout()

        # 按钮布局
        button_layout = QHBoxLayout()

        # 添加自定义按钮
        emoticon_button = QPushButton('😀', self)
        emoticon_button.setFixedSize(40, 40)
        emoticon_button.clicked.connect(self.send_emoticon)
        button_layout.addWidget(emoticon_button)

        image_button = QPushButton('图片', self)
        image_button.setFixedSize(40, 40)
        image_button.clicked.connect(self.send_image)
        button_layout.addWidget(image_button)

        file_button = QPushButton('文件', self)
        file_button.setFixedSize(40, 40)
        file_button.clicked.connect(self.send_file)
        button_layout.addWidget(file_button)

        button_layout.addStretch(0)

        # 消息显示区域
        self.message_list = QListWidget(self)
        right_layout.addWidget(self.message_list, 3)  # 这里用伸缩因子来控制比例

        # 添加按钮布局到右侧主布局
        right_layout.addLayout(button_layout)

        # 消息输入框
        self.text_input = QTextEdit(self)
        right_layout.addWidget(self.text_input, 1)

        # 发送按钮布局
        send_layout = QHBoxLayout()
        send_layout.addStretch(0)
        self.send_button = QPushButton('发送', self)
        self.send_button.clicked.connect(self.send_message)
        send_layout.addWidget(self.send_button)
        right_layout.addLayout(send_layout)
        # 设置样式表
        self.send_button.setStyleSheet("""
                    QPushButton {
                        border: none;
                        background-color: #4CAF50;
                        color: white;
                        border-radius: 5px;
                    }
                    QPushButton:pressed {
                        background-color: #45a049;
                    }
                    QPushButton#发送 {
                        background-color: #2196F3;
                    }
                """)
        # 将右侧布局添加到主布局中
        main_layout.addLayout(right_layout, 3)  # 占3/4的宽度

        # 设置主布局
        self.setLayout(main_layout)

    def build_account_tree(self):
        # 示例账号与好友数据
        account_name = "MyAccount"  # 你的账号
        friends = {
            'A': ['Alice'],
            'B': ['Bob', 'Becky'],
            'C': ['Charlie'],
            'Z': ['Zara', 'Zane'],
            '#': ['12345']
        }

        # 创建根节点
        account_item = QTreeWidgetItem([account_name])
        self.account_tree.addTopLevelItem(account_item)

        # 按键排序并构建树结构
        for key in sorted(friends.keys()):
            letter_item = QTreeWidgetItem(account_item, [key])
            for friend in sorted(friends[key]):
                friend_item = QTreeWidgetItem(letter_item, [friend])

    def send_message(self):
        # 获取输入框的文本内容
        message = self.text_input.toPlainText().strip()

        if message:
            # 将消息添加到列表中
            self.message_list.addItem(f"你: {message}")
            # 清空输入框
            self.text_input.clear()

    def send_emoticon(self):
        # 这里添加发送表情包的逻辑
        self.message_list.addItem("系统消息: 发送表情包功能未实现")

    def send_image(self):
        # 打开文件对话框以选择要发送的图片
        file_path, _ = QFileDialog.getOpenFileName(self, '选择图片', '', 'Images (*.png *.xpm *.jpg *.bmp *.gif)')

        if file_path:
            # 模拟发送图片
            self.message_list.addItem(f"你: [图片] {file_path.split('/')[-1]}")

    def send_file(self):
        # 打开文件对话框以选择要发送的文件
        file_path, _ = QFileDialog.getOpenFileName(self, '选择文件', '')

        if file_path:
            # 模拟发送文件
            self.message_list.addItem(f"你: [文件] {file_path.split('/')[-1]}")

