# ***************************************************************************************************
# ***************************************************************************************************
#
# 标明：所有的库都包含在这个文件里面，然后在别的文件里面使用只需要import BasicDefine 就可以了！
# 更新需要在顶部import然后再把具体库名放在__all__这个列表里面！
#
# ***************************************************************************************************
# ***************************************************************************************************

import sys
import os
import json
import time
import requests
import asyncio
import aiohttp
import hashlib
from PIL import Image
import mimetypes
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTabWidget,
    QPushButton, QTableWidget, QTableWidgetItem, QCheckBox, QLabel,
    QTextEdit, QLineEdit, QGroupBox, QFileDialog, QGridLayout,
    QHeaderView, QMessageBox, QDialog, QScrollArea, QMenuBar, QMenu,
    QListWidget, QAction, QTreeWidget, QTreeWidgetItem
)
from PyQt5.QtCore import (
    Qt, QDate, pyqtSignal, QTimer, QPropertyAnimation, pyqtProperty, QSize
)
from PyQt5.QtGui import (
    QIcon, QDragEnterEvent, QDropEvent, QPixmap, QFont, QColor,
    QPaintEvent, QPainter, QMouseEvent, QResizeEvent
)


__all__ = \
    [
        # 系统库
        'sys', 'json', 'os', 'time', 'requests', 'asyncio', 'aiohttp', 'hashlib', 'Image', 'mimetypes',
        # Qt库
        'QApplication', 'QWidget', 'QVBoxLayout', 'QHBoxLayout', 'QTableWidget', 'QPushButton', 'QTabWidget', 'QDialog',
        'QTableWidgetItem', 'QCheckBox', 'QLabel', 'QTextEdit', 'QLineEdit', 'QGroupBox', 'QFileDialog', 'QGridLayout',
        'QHeaderView', 'QMessageBox', 'Qt', 'QDate', 'QIcon', 'QDragEnterEvent', 'QDropEvent', 'QPixmap', 'QFont',
        'pyqtSignal', 'QColor', 'QTimer', 'QPaintEvent', 'QPainter', 'QMouseEvent', 'QResizeEvent',
        'QPropertyAnimation', 'pyqtProperty', 'QSize', 'QScrollArea', 'QMenuBar', 'QMenu', 'QListWidget', 'QAction',
        'QTreeWidget', 'QTreeWidgetItem'
    ]

