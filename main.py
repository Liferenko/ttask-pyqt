import sys
import random
import pdb

from PyQt5.QtWidgets import (
    QApplication,
    QGraphicsScene,
    QGraphicsView,
    QGraphicsRectItem,
)
from PyQt5.QtGui import QBrush, QTransform, QColor
from PyQt5.QtCore import Qt, QLineF

# pdb.set_trace()


class RectangleItem(QGraphicsRectItem):
    def __init__(self):
        super().__init__()
        self.setRect(0, 0, 200, 100)

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

        self.setBrush(QBrush(QColor(random.choice(colors))))
        self.setFlag(QGraphicsRectItem.ItemIsMovable)
        self.connections = []

    def itemChange(self, change, value):
        if change == QGraphicsRectItem.ItemPositionChange:
            for connection in self.connections:
                connection.updateLine()
        return super().itemChange(change, value)


class ConnectionItem(QGraphicsRectItem):
    def __init__(self, start_item, end_item):
        super().__init__()
        self.start_item = start_item
        self.end_item = end_item
        # pdb.set_trace()
        self.updateLine()

    def updateLine(self):
        start_pos = self.start_item.scenePos() + self.start_item.rect().center()
        end_pos = self.end_item.scenePos() + self.end_item.rect().center()

        line = QLineF(start_pos, end_pos)
        print("Imma draw a connection line")
        # self.setLine(line)


class Scene(QGraphicsScene):
    def __init__(self):
        super().__init__()
        self.setSceneRect(0, 0, 800, 600)
        self.rectangles = []
        self.connections = []

    def mouseDoubleClickEvent(self, event):
        # Randomly select a color from the list
        rect_item = RectangleItem()
        rect_item.setPos(event.scenePos())

        self.addItem(rect_item)
        self.rectangles.append(rect_item)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            start_item = self.itemAt(event.scenePos(), QTransform())
            target_item = None

            print(f"start item #{start_item}")

            if isinstance(start_item, RectangleItem):
                connection_item = ConnectionItem(start_item, start_item)
                print(f"target_item item #{connection_item}")
                print(connection_item)

                self.addItem(connection_item)
                self.connections.append(connection_item)

        if event.button() == Qt.RightButton:
            print("Context menu called")
            # TODO:
            # - add "Create connection"
            # - add "Remove connection"
            # - add "Remove object"

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            for rect_item in self.rectangles:
                rect_item.setSelected(False)
            item = self.itemAt(event.scenePos(), QTransform())
            if isinstance(item, RectangleItem):
                item.setSelected(True)

    # OPTIMIZE
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            start_item = self.itemAt(event.scenePos(), QTransform())
            if isinstance(start_item, RectangleItem):
                end_item = self.itemAt(event.scenePos(), QTransform())
                if isinstance(end_item, RectangleItem) and start_item != end_item:
                    connection_item = ConnectionItem(start_item, end_item)
                    self.addItem(connection_item)
                    self.connections.append(connection_item)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    scene = Scene()
    """
    opens a window with an empty scene on PyQt
    """
    view = QGraphicsView(scene)
    view.show()
    sys.exit(app.exec())
