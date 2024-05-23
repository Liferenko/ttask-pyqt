import sys
import random

from PyQt5.QtWidgets import (
    QApplication,
    QGraphicsScene,
    QGraphicsView,
)

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
            "yellow",
            "orange",
            "purple",
            "pink",
            "brown",
            "black",
            "white",
            "cyan",
            "magenta",
            "teal",
            "lime",
            "olive",
            "peach",
            "lavender",
            "maroon",
            "navy",
            "silver",
        ]

        # Randomly select a color from the list
        rect_item = 0 #TODO
        rect_item.setPos(event.scenePos())

        self.addItem(rect_item)
        self.rectangles.append(rect_item)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    scene = Scene()
    """
    opens a window with an empty scene on PyQt
    """
    view = QGraphicsView(scene)
    view.show()
    sys.exit(app.exec())
