import random

from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QMenu,
    QGraphicsLineItem,
)
from PyQt5.QtGui import QPainter, QColor, QBrush, QMouseEvent, QPen
from PyQt5.QtCore import Qt, QRect, QPoint


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

instructions = [
    "Double-click to create a rectangle",
    "Right click -> context menu -> create/remove connection line",
    "Cmd+Q to quit",
]


class RectangleItem:
    def __init__(self, rect):
        self.rect = rect
        self.mouse_pressed = False
        self.offset = QPoint()
        self.connections = []
        self.color = random.choice(colors)
        self.connection_lines = []

    def paint(self, painter):
        painter.setBrush(QBrush(QColor(self.color)))
        painter.drawRect(self.rect)

    def handle_collision_with_rectangles(self):
        for rect_item in Scene().rect_items:
            if rect_item.rect != self.rect and rect_item.rect.intersects(self.rect):
                self.color = rect_item.color
                break

    def handle_collision_with_borders(self, event: QMouseEvent | None) -> None:
        new_pos = event.pos() - self.offset
        updated_rect = QRect(new_pos, self.rect.size())
        borders = Scene().rect()

        # Check for collisions with scene borders
        if updated_rect.top() < borders.top():
            new_pos.setY(borders.top())
        if updated_rect.bottom() > borders.bottom():
            new_pos.setY(borders.bottom() - self.rect.height())
        if updated_rect.left() < borders.left():
            new_pos.setX(borders.left())
        if updated_rect.right() > borders.right():
            new_pos.setX(borders.right() - self.rect.width())
        self.rect.moveTo(new_pos)

    def mousePressEvent(self, event: QMouseEvent | None):
        match event.button():
            case Qt.LeftButton:
                self.mouse_pressed = True
                self.offset = event.pos() - self.rect.topLeft()

            case Qt.RightButton:
                print("Right button clicked!")

    def can_object_be_created_here(target_rect) -> bool:
        # Object can't be created if the new object
        # intersects with any other object
        for rect_item in Scene().rect_items:
            if rect_item.rect.intersects(target_rect):
                return False
        return True

    def mouseDoubleClickEvent(self, event):
        rect = QRect(event.pos().x() - 100, event.pos().y() - 50, 200, 100)

        if self.can_object_be_created_here(rect):
            self.rect_items.append(RectangleItem(rect))
            self.update()

    def mouseMoveEvent(self, event: QMouseEvent | None) -> None:
        if self.mouse_pressed:
            self.handle_collision_with_borders(event)
            self.handle_collision_with_rectangles()

    def mouseReleaseEvent(self, event: QMouseEvent | None) -> None:
        if event.button() == Qt.LeftButton:
            self.mouse_pressed = False


class ConnectionLine(QGraphicsLineItem):
    def __init__(self, start_pos, end_pos):
        super().__init__(start_pos.x(), start_pos.y(), end_pos.x(), end_pos.y())
        self.setPen(QPen(Qt.black, 2))

    def mousePressEvent(self, event: QMouseEvent | None) -> None:
        match event.button():
            case Qt.LeftButton:
                self.mouse_pressed = True
                self.offset = event.pos() - self.rect.topLeft()

            case Qt.RightButton:
                print("Right button clicked!")
                # Update end position
                object_under_cursor = Scene().get_object_under_cursor(event.pos())

                if object_under_cursor:
                    self.connection_line_end_pos = object_under_cursor.rect.center()


class Scene(QWidget):
    def __init__(self):
        super().__init__()
        self.rect_items = []
        self.connection_lines = []
        self.setFixedSize(800, 500)
        self.setMouseTracking(True)
        self.show()

    def paintEvent(self, event: QMouseEvent | None) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Draw object
        for rect_item in self.rect_items:
            rect_item.paint(painter)

        # Draw connection lines
        for connection_line in self.connection_lines:
            painter.drawLine(connection_line.line())

        # Draw instructions
        font = painter.font()
        font.setPointSizeF(font.pointSizeF() * 0.8)
        painter.setOpacity(0.7)
        painter.setFont(font)
        painter.drawText(self.width() - 300, 40, instructions[0])
        painter.drawText(self.width() - 300, 55, instructions[1])
        painter.drawText(self.width() - 300, 70, instructions[2])

    def mouseDoubleClickEvent(self, event):
        rect = QRect(event.pos().x() - 100, event.pos().y() - 50, 200, 100)
        self.rect_items.append(RectangleItem(rect))
        self.update()

    def mousePressEvent(self, event: QMouseEvent | None) -> None:
        for rect_item in self.rect_items:
            if rect_item.rect.contains(event.pos()):
                rect_item.mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent | None) -> None:
        for rect_item in self.rect_items:
            rect_item.mouseMoveEvent(event)

        for connection_line in self.connection_lines:
            connection_line.setLine(
                connection_line.line().x1(),
                connection_line.line().y1(),
                event.pos().x(),
                event.pos().y(),
            )

        self.update()

    def mouseReleaseEvent(self, event: QMouseEvent | None) -> None:
        for rect_item in self.rect_items:
            rect_item.mouseReleaseEvent(event)

    def connect_objects(self, object_a, object_b):
        for line in self.connection_lines:
            if line.contains(object_a.rect.center()) and line.contains(
                object_b.rect.center()
            ):
                print("Connection line exists")
                return

        # Create a new connection line
        connection_line = ConnectionLine(object_a.rect.center(), object_b.rect.center())
        self.add_connection_line(connection_line)

    def get_object_under_cursor(self, cursor_pos):
        for rect_item in self.rect_items:
            if rect_item.rect.contains(cursor_pos):
                return rect_item
        return None

    def contextMenuEvent(self, event):
        menu = QMenu(self)

        menu.addAction(
            "Create connection line",
            lambda: self.connect_objects(
                self.get_object_under_cursor(event.pos()),
                self.rect_items[0],  # FIXIT
            ),
        )
        menu.addAction(
            "Remove connection line",
            lambda: self.remove_connection_line(self.connection_lines[0]),
        )

        action = menu.exec_(event.globalPos())
        if action:
            print(f"Selected option: {action.text()}")

    def add_connection_line(self, connection_line):
        self.connection_lines.append(connection_line)
        self.update()

    def remove_connection_line(self, connection_line):
        if connection_line in self.connection_lines:
            self.connection_lines.remove(connection_line)
            self.update()


if __name__ == "__main__":
    app = QApplication([])
    window = Scene()
    app.exec_()
