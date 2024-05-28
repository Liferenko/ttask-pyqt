import random
import pdb

from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QColor, QBrush, QMouseEvent
from PyQt5.QtCore import Qt, QRect, QPoint


class RectangleItem:
    def __init__(self, rect):
        self.rect = rect
        self.mouse_pressed = False
        self.offset = QPoint()
        self.connections = []

    def paint(self, painter):
        colors = [
            "red",
            "blue",
            "green",
            "black",
            "yellow",
            "orange",
            "purple",
            "pink",
            "brown",
            "white",
        ]

        painter.setBrush(QBrush(QColor(random.choice(colors))))
        painter.drawRect(self.rect)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and self.rect.contains(event.pos()):
            self.mouse_pressed = True
            self.offset = event.pos() - self.rect.topLeft()

    def handle_collision(self, event: QMouseEvent | None) -> None:
        new_pos = event.pos() - self.offset
        updated_rect = QRect(new_pos, self.rect.size())
        borders = Scene().rect()

        if updated_rect.top() < borders.top():
            new_pos.setY(borders.top())
        if updated_rect.bottom() > borders.bottom():
            new_pos.setY(borders.bottom() - self.rect.height())
        if updated_rect.left() < borders.left():
            new_pos.setX(borders.left())
        if updated_rect.right() > borders.right():
            new_pos.setX(borders.right() - self.rect.width())

        self.rect.moveTo(new_pos)

    def mouseMoveEvent(self, event: QMouseEvent | None) -> None:
        if self.mouse_pressed:
            self.handle_collision(event)

    def mouseReleaseEvent(self, event: QMouseEvent | None) -> None:
        if event.button() == Qt.LeftButton:
            self.mouse_pressed = False


class Scene(QWidget):
    def __init__(self):
        super().__init__()
        # TODO Create rectangles by click
        self.rect_items = [RectangleItem(rect) for rect in rect_array]
        self.setFixedSize(800, 500)
        self.setMouseTracking(True)
        self.show()

    def paintEvent(self, event: QMouseEvent | None) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        for rect_item in self.rect_items:
            rect_item.paint(painter)

    def mousePressEvent(self, event: QMouseEvent | None) -> None:
        for rect_item in self.rect_items:
            if rect_item.rect.contains(event.pos()):
                rect_item.mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent | None) -> None:
        for rect_item in self.rect_items:
            rect_item.mouseMoveEvent(event)
        self.update()

    def mouseReleaseEvent(self, event: QMouseEvent | None) -> None:
        for rect_item in self.rect_items:
            rect_item.mouseReleaseEvent(event)


if __name__ == "__main__":
    app = QApplication([])
    rect_array = [
        QRect(50, 50, 100, 100),
        QRect(200, 200, 150, 150),
    ]

    window = Scene()
    app.exec_()
