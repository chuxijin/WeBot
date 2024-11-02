from BasicDefine import *


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
        self.radius = self.height() / 2
        self.margin = 2
        self.thumb_position = self.margin
        self.animation = QPropertyAnimation(self, b"thumbPosition")
        self.animation.setDuration(200)

    def isToggled(self):
        return self.checked

    def setToggle(self, checked):
        if self.checked != checked:
            self.checked = checked
            self.toggle_animation()

    def toggle_animation(self):
        start_position = self.thumb_position
        end_position = self.width() - self.height() + self.margin if self.checked else self.margin
        self.animation.stop()
        self.animation.setStartValue(start_position)
        self.animation.setEndValue(end_position)
        self.animation.start()

    def getThumbPosition(self):
        return self.thumb_position

    def setThumbPosition(self, pos):
        self.thumb_position = pos
        self.update()

    thumbPosition = pyqtProperty(int, fget=getThumbPosition, fset=setThumbPosition)

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

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Background
        bg_color = self.checked_color if self.checked else self.background_color
        painter.setBrush(bg_color)
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(self.rect(), self.radius, self.radius)

        # Thumb
        thumb_rect = self.height() - 2 * self.margin
        painter.setBrush(self.thumb_color)
        painter.drawEllipse(self.thumb_position, self.margin, thumb_rect, thumb_rect)

    def mousePressEvent(self, event):
        if self.isEnabled() and event.button() == Qt.LeftButton:
            self.checked = not self.checked
            self.toggle_animation()
            self.toggled.emit(self.checked)
            event.accept()
        else:
            event.ignore()
