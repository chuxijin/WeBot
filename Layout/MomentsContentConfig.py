from BasicDefine import *


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
