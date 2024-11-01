from BasicDefine import *


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
