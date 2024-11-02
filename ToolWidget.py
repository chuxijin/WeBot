from Layout.AccountManagement import *
from Layout.FriendConfig import *
from Layout.FriendManagement import *
from Layout.GroupManagement import *
from Layout.GroupMessageConfig import *
from Layout.MessageManagement import *
from Layout.MomentsManagement import *
from Layout.MomentsContentConfig import *
from Layout.SendMsgManagement import *


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
        self.send_tab = SendMsgManagementTab()

        self.tabs.addTab(self.account_tab, QIcon("icons/account.png"), "账号管理")
        self.tabs.addTab(self.message_tab, QIcon("icons/message.png"), "消息管理")
        self.tabs.addTab(self.friend_tab, QIcon("icons/friend.png"), "好友管理")
        self.tabs.addTab(self.group_tab, QIcon("icons/group.png"), "群管理")
        self.tabs.addTab(self.moments_tab, QIcon("icons/moments.png"), "朋友圈管理")
        self.tabs.addTab(self.send_tab, QIcon("icons/send.png"), "发送消息管理")

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
