# ttask-pyqt
<!--
Критерии: корректная работа (правильность реализации задания), архитектура, грамотные комментарии.
Приблизительное время: 2-6 ч.
Язык: Python 2.7 или 3.x, библиотека PyQt
Результат: исходный код.


Формулировка:
- Разработать программу, которая открывает окно с пустой сценой на PyQT и по двойному нажатию на сцену добавляет прямоугольники разного цвета в то место, где было произведено двойное нажатие. 
- Прямоугольники можно перетаскивать по сцене. 
- Между прямоугольниками можно создавать/удалять связь (визуально - линия).


Реализация:
- Размер прямоугольников константен (отношение сторон 2:1).
- Цвет создаваемого прямоугольника выбирается случайным образом в момент его создания.
- Выбор способа создания/удаления связи между прямоугольниками осуществляется разработчиком.
- Прямоугольники не могут перекрывать друг друга при создании и перетаскивании.
- Прямоугольники не могут выходить за границы окна/сцены при создании и перетаскивании.
- При взаимодействии с прямоугольником учитываются все возможные коллизии.
- Для упрощения, прямоугольник не создается, если область на сцене, по которой произведен двойной клик, слишком мала для размещения в ней прямоугольника.
- При перетаскивании прямоугольника связанные с ним фигуры остаются на месте, созданные связи сохраняются и обновляются.
- Прямоугольник создаётся с центром в точке клика, перетаскивается за любое место.
- Обойтись только библиотекой PyQT со стадартными инструментами для рисования и виджетов (Widget, Brush, Rectangle и т. п.)
- * Будет плюсом, если при перетаскивании на занятое место прямоугольник будет вставать вплотную к препятствию (упираться в коллизию  на последнем доступном месте), а не возвращаться на прежнюю позицию мыши.

-->

**Criteria:** Correct functionality (correct implementation of the task), architecture, proper comments.
**Approximate time:** 2-6 hours.
**Language:** Python 2.7 or 3.x, PyQt library.
**Result:** Source code.

**Definition of done:**
- [x] The program opens a window with an empty scene on PyQt 
- [x] adds rectangles of different colors at the location of a double-click on the scene.
- [x] Rectangles can be dragged across the scene.
- [ ] Connections (visually represented by lines) can be created/deleted between rectangles.
- [x] Utilize standard PyQt tools like Widget, Brush, Rectangle for implementation.

**TODO:**
- [x] The size of the rectangles is constant (aspect ratio 2:1).
- [x] The color of a newly created rectangle is chosen randomly at the time of its creation.
- [ ] The method for creating/deleting connections between rectangles is chosen by the developer.
  - [x] double left click - create a rectangle
  - [ ] left click on an object - init/finish a connection line
  - [ ] right click on a connection line - remove the line
- [ ] Rectangles cannot overlap each other during creation and dragging.
- [x] Rectangles cannot go outside the window/scene boundaries during creation and dragging.
- [ ] All possible collisions must be considered when interacting with rectangles.
- [ ] For simplicity, a rectangle is not created if the area of the scene where the double-click was made is too small to place the rectangle.
- [ ] When dragging a rectangle, the connected figures remain in place, created connections are preserved and updated.
- [x] A rectangle is created centered at the click point and can be dragged from any point.
- [x] Use only the PyQt library with standard drawing and widget tools (Widget, Brush, Rectangle, etc.)
- [ ] * It would be a plus if, when dragging to an occupied space, the rectangle will snap next to the obstacle (stop at the last available position) instead of returning to the previous mouse position.

