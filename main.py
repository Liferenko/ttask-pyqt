import sys
import random
import pdb

from PyQt5.QtWidgets import (
    QApplication,
    QGraphicsScene,
    QGraphicsView,
    QGraphicsRectItem,
)
from PyQt5.QtGui import QBrush, QTransform, QColor  # Add this line
from PyQt5.QtCore import QRectF, Qt, QLineF


class RectangleItem(QGraphicsRectItem):
    """
    A QGraphicsRectItem subclass - a rectangle item on the scene.
    """

    def __init__(self, color):
        super().__init__(QRectF(0, 0, 200, 100))
        # TODO remove before flight
        # self.setRect(0, 0, 200, 100)
        self.setBrush(QBrush(QColor(color)))
        # TODO need it? self.setFlag(QGraphicsRectItem.ItemIsMovable)
        self.connections = []
        self.dragging = False

    def itemChange(self, change, value):
        if change == QGraphicsRectItem.ItemPositionChange:
            for connection in self.connections:
                connection.updateLine()
        return super().itemChange(change, value)


class ConnectionItem(QGraphicsRectItem):
    """
    QGraphicsRectItem - a connection item between rectangles.
    """

    def __init__(self, start_item, end_item):
        super().__init__()
        self.start_item = start_item
        self.end_item = end_item
        self.updateLine()

    def updateLine(self):
        start_pos = self.start_item.scenePos() + self.start_item.rect().center()

        end_pos = self.end_item.scenePos() + self.end_item.rect().center()
        line = QLineF(start_pos, end_pos)

        print(line)
        self.setLine(line)


class Scene(QGraphicsScene):
    """
    QGraphicsScene handles the scene events, manages the items
    """

    def __init__(self):
        super().__init__()
        self.setSceneRect(0, 0, 800, 600)
        self.rectangles = []
        self.connections = []

    def mouseDoubleClickEvent(self, event):
        # 20 colors
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

        # Randomly select a color from the list
        rect_item = RectangleItem(random.choice(colors))
        rect_item.setPos(event.scenePos())

        self.addItem(rect_item)
        self.rectangles.append(rect_item)

    def mousePressEvent(self, event):
        for rect_item in self.rectangles:
            if event.button() == Qt.LeftButton and rect_item.contains(event.pos()):
                rect_item.dragging = True
                # rect_item.offset = event.pos() - rect_item.topLeft()

    def mouseMoveEvent(self, event):
        for rect_item in self.rectangles:
            if rect_item.dragging:
                new_pos = event.pos() - rect_item.offset

                if rect_item.contains(new_pos):
                    rect_item.mouseTopLeft(new_pos)
                    self.update()

        # for rect_item in self.rectangles:
        #     rect_item.setSelected(False)
        #     print(rect_item)

        # item = self.itemAt(event.scenePos(), QTransform())

        # if isinstance(item, RectangleItem):
        #     item.setSelected(True)

    # OPTIMIZE
    def mouseReleaseEvent(self, event):
        for rect_item in self.rectangles:
            if event.button() == Qt.LeftButton and rect_item.dragging:
                rect_item.dragging = False
                self.update()

        # if event.button() == Qt.LeftButton:
        #     start_item = self.itemAt(event.scenePos(), QTransform())
        #     if isinstance(start_item, RectangleItem):
        #         end_item = self.itemAt(event.scenePos(), QTransform())
        #         if isinstance(end_item, RectangleItem) and start_item != end_item:
        #             connection_item = ConnectionItem(start_item, end_item)
        #             self.addItem(connection_item)
        #             self.connections.append(connection_item)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    scene = Scene()
    """
    opens a window with an empty scene on PyQt
    """
    view = QGraphicsView(scene)
    view.show()
    sys.exit(app.exec())
