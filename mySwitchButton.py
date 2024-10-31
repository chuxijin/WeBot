from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QPainter, QColor, QMouseEvent, QPaintEvent, QResizeEvent, QPixmap

class MySwitchControl(QWidget):
    toggled = pyqtSignal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(60, 30)
        self.checked = False
        self.background_color = QColor(52, 60, 71)
        self.checked_color = QColor(51, 255, 51)
        self.disabled_color = QColor(190, 190, 190)
        self.thumb_color = QColor(Qt.white)
        self.radius = 15.0
        self.margin = 2
        self.thumb_position = self.margin
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.animate)
        self.animation_direction = 1  # 1 for right, -1 for left
        self.animation_speed = 2

    def isToggled(self):
        return self.checked

    def setToggle(self, checked):
        if self.checked != checked:
            self.checked = checked
            self.animation_direction = 1 if self.checked else -1
            self.timer.start(10)

    def setBackgroundColor(self, color):
        self.background_color = color
        self.update()

    def setCheckedColor(self, color):
        self.checked_color = color
        self.update()

    def setDisabledColor(self, color):
        self.disabled_color = color
        self.update()

    def setThumbColor(self, color):
        self.thumb_color = color
        self.update()

    def setStateText(self, text):
        self.state_text = text
        self.update()

    def paintEvent(self, event: QPaintEvent):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Background
        if self.isEnabled():
            bg_color = self.checked_color if self.checked else self.background_color
        else:
            bg_color = self.disabled_color

        painter.setBrush(bg_color)
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(self.rect(), self.radius, self.radius)

        # Thumb
        thumb_color = self.thumb_color
        painter.setBrush(thumb_color)
        painter.drawEllipse(self.thumb_position, self.margin, self.height() - 2*self.margin, self.height() - 2*self.margin)

    def mousePressEvent(self, event: QMouseEvent):
        if self.isEnabled() and event.button() == Qt.LeftButton:
            event.accept()
        else:
            event.ignore()

    def mouseReleaseEvent(self, event: QMouseEvent):
        if self.isEnabled() and event.button() == Qt.LeftButton:
            self.checked = not self.checked
            self.toggled.emit(self.checked)
            self.update()
            event.accept()
        else:
            event.ignore()

    def animate(self):
        if self.animation_direction == 1:
            if self.thumb_position < self.width() - self.height():
                self.thumb_position += self.animation_speed
                self.update()
            else:
                self.timer.stop()
        else:
            if self.thumb_position > self.margin:
                self.thumb_position -= self.animation_speed
                self.update()
            else:
                self.timer.stop()

    def resizeEvent(self, event: QResizeEvent):
        self.radius = self.height() / 2
        self.thumb_position = self.margin if not self.checked else self.width() - self.height() + self.margin
        super().resizeEvent(event)

    def sizeHint(self):
        return self.size()
