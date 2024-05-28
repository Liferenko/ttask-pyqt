import random
import datetime
import pdb

from PyQt5.QtWidgets import QApplication, QWidget, QGraphicsRectItem
from PyQt5.QtGui import QPainter, QColor, QBrush, QMouseEvent
from PyQt5.QtCore import Qt, QRect, QPoint
from PyQt5.QtGui import QMouseEvent

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

class RectangleItem(QGraphicsRectItem):
    def __init__(self):
        super().__init__()
        self.setRect(0, 0, 200, 100)
        self.setBrush(QBrush(QColor(random.choice(colors))))
        self.mouse_pressed = False
        self.offset = QPoint()
        self.connections = []

    # def paint(self, painter):
    #
    #     painter.setBrush(QBrush(QColor(random.choice(colors))))
    #     painter.drawRect(self.rect)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and self.contains(event.pos()):
            self.mouse_pressed = True
            self.offset = event.pos() - self.rect.topLeft()

    def handle_collision(self, event: QMouseEvent) -> None:
        new_pos = event.pos() - self.offset
        updated_rect = QRect(new_pos, self.rect.size())

        # TODO handle obj-to-obj collisions
        for rect in Scene().rect_items:
            if rect != self:
                if updated_rect.intersects(rect.rect):
                    print(f"#{datetime.datetime.now()} - UNACCEPTABLEEEEEE!!!")
                    new_pos.setX(max(new_pos.x(), rect.rect.left() - self.rect.width()))
                    new_pos.setX(min(new_pos.x(), rect.rect.right()))

                    new_pos.setY(max(new_pos.y(), rect.rect.top() - self.rect.height()))
                    new_pos.setY(min(new_pos.y(), rect.rect.bottom()))

                    print(f'new position - #{new_pos}')
        # Collisions with Scene boundaries
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

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if self.mouse_pressed:
            self.handle_collision(event)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.LeftButton:
            self.mouse_pressed = False


class Scene(QWidget):
    def __init__(self):
        super().__init__()
        # TODO Create rectangles by click
        self.rect_items = []
        self.setFixedSize(800, 500)
        self.setMouseTracking(True)
        self.show()

    # def paintEvent(self, event: QMouseEvent) -> None:
    #     painter = QPainter(self)
    #     painter.setRenderHint(QPainter.Antialiasing)
    #     for rect_item in self.rect_items:
    #         rect_item.paint(painter)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        for rect_item in self.rect_items:
            if rect_item.contains(event.pos()):
                rect_item.mousePressEvent(event)

    def mouseDoubleClickEvent(self, event: QMouseEvent) -> None:
        new_rect_item = RectangleItem()
        new_rect_item.setPos(event.screenPos())

        print(self.rect_items)
        #self.addItem(rect_item)
        self.rect_items.append(new_rect_item)

        # return super().mouseDoubleClickEvent(event)
        print("Sup doubleclick")


    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        for rect_item in self.rect_items:
            rect_item.mouseMoveEvent(event)
        self.update()

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        for rect_item in self.rect_items:
            rect_item.mouseReleaseEvent(event)


if __name__ == "__main__":
    app = QApplication([])

    # TODO REMOVE BEFORE FLIGHT!!!!!!
    # rect_array = [
    #     QRect(50, 50, 100, 100),
    #     QRect(200, 200, 150, 150),
    # ]

    window = Scene()
    app.exec_()
