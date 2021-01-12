# ===================== Import Section =========================
import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from KilnDilog import *
from Component import *


# ===================== Class OurMimeData ======================
class OurMimeData(QMimeData):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def getName(self):
        return self.name


# ===================== Class QDragLabel ======================
class QDragLabel(QLabel):
    clicked = pyqtSignal(str)

    def __init__(self, mimeName, parent=None):
        # super().__init__()
        super(QDragLabel, self).__init__(parent)
        self.mimeName = mimeName

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            data = QByteArray()
            mime_data = OurMimeData(self.mimeName)
            mime_data.setData(self.mimeName, data)
            drag = QDrag(self)
            drag.setMimeData(mime_data)
            drag.setHotSpot(self.rect().topLeft())  # where do we drag from
            if QT_VERSION_STR < '5':
                drop_action = drag.start(Qt.MoveAction)  # drag starts
            else:
                drop_action = drag.exec(Qt.MoveAction)  # drag starts


# ===================== Class ToolbarArrow ======================
class ToolbarArrow(QDragLabel):
    def __init__(self, pos):
        if pos == "left":
            super().__init__("left")
            self.arrow_left()
        elif pos == "right":
            super().__init__("right")
            self.arrow_rigth()
        elif pos == "top":
            super().__init__("top")
            self.arrow_top()
        elif pos == "down":
            super().__init__("down")
            self.arrow_down()

    def arrow_left(self):
        picture = QPixmap("images//left.png")
        self.setPixmap(picture.scaled(20, 10))
        self.mimetext = "application/x-arrow"

    def arrow_rigth(self):
        picture = QPixmap("images//right.png")
        self.setPixmap(picture.scaled(20, 10))
        self.mimetext = "application/x-arrow"

    def arrow_top(self):
        picture = QPixmap("images//top.png")
        self.setPixmap(picture.scaled(10, 20))
        self.mimetext = "application/x-arrow"

    def arrow_down(self):
        picture = QPixmap("images//down.png")
        self.setPixmap(picture.scaled(10, 20))
        self.mimetext = "application/x-arrow"


# ===================== Class CustomQGraphicsPixmapItem ======================
class CustomQGraphicsPixmapItem(QGraphicsPixmapItem):
    def __init__(self, q, label):
        super().__init__(q)
        self.setAcceptHoverEvents(True)
        self.label = label
        self.create_popup()
        if q == QPixmap("images/left.png"):
            self.current_graphic = QPixmap(q)
            self.setPixmap(self.current_graphic.scaledToWidth(150))
            self.setAcceptHoverEvents(True)
        elif q == QPixmap("images/right.png"):
            self.current_graphic = QPixmap(q)
            self.setPixmap(self.current_graphic.scaledToWidth(150))
            self.setAcceptHoverEvents(True)
        elif q == QPixmap("images/top.png"):
            self.current_graphic = QPixmap(q)
            self.setPixmap(self.current_graphic.scaledToWidth(150))
            self.setAcceptHoverEvents(True)
        elif q == QPixmap("images/down.png"):
            self.current_graphic = QPixmap(q)
            self.setPixmap(self.current_graphic.scaledToWidth(150))
            self.setAcceptHoverEvents(True)

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            orig_cursor_position = event.lastScenePos()
            updated_cursor_position = event.scenePos()
            orig_position = self.scenePos()
            updated_cursor_x = updated_cursor_position.x() - orig_cursor_position.x() + orig_position.x()
            updated_cursor_y = updated_cursor_position.y() - orig_cursor_position.y() + orig_position.y()
            self.setPos(QPointF(updated_cursor_x, updated_cursor_y))

    def hoverEnterEvent(self, event):
        app.instance().setOverrideCursor(Qt.OpenHandCursor)

    def hoverLeaveEvent(self, event):
        app.instance().restoreOverrideCursor()

    def create_popup(self):
        self.dg = KilnDilog()

    def mouseDoubleClickEvent(self, event):
        self.dg.exec_()


# ===================== Class DrawingPanel ======================
class DrawingPanel(QGraphicsScene):
    def __init__(self):
        super().__init__()
        self.background_brush = QBrush()
        self.background_picture = QPixmap("images/if_we_want_bg_image")
        self.background_brush.setTexture(self.background_picture)
        self.setBackgroundBrush(self.background_brush)
        self.kilns = []

    def dragEnterEvent(self, event):
        event.accept()

    def dragMoveEvent(self, event):
        event.accept()

    def drop_position(self, item):
        cursor_position = QCursor.pos()
        current_view = self.views()[0]
        scene_position = current_view.mapFromGlobal(cursor_position)
        width = item.boundingRect().width()
        height = item.boundingRect().height()
        width_offset = width / .5
        height_offset = height / .5
        drop_x = scene_position.x() - width_offset
        drop_y = scene_position.y() - height_offset
        return drop_x, drop_y

    def visualise_graphic_item(self, name):
        # if len(self.kilns)> = 1:return
        print(name)
        kiln = CustomQGraphicsPixmapItem(QPixmap("images/" + name), name)
        kiln.setFlags(QGraphicsItem.ItemIsMovable)
        self.kilns.append(kiln)
        x, y = self.drop_position(self.kilns[-1])
        self.kilns[-1].setPos(x, y)
        self.kilns[-1].setOffset(10, 20)
        self.addItem(self.kilns[-1])

    def dropEvent(self, event):
        event.accept()
        name = event.mimeData().getName()
        if len(name) == 0: return
        self.visualise_graphic_item(name)

    def removeKilns(self):
        if len(self.kilns) <= 0:
            return None
        else:
            item = self.kilns.pop()
            self.removeItem(item)
            return item

    def addKilns(self, item):
        self.addItem(item)
        self.kilns.append(item)


# ===================== Class App ======================
class App(QMainWindow):
    # ============ Constructor ============
    def __init__(self):
        super().__init__()
        self.title = 'AB SIM!!!'
        self.left = 0
        self.top = 0
        self.width = 740
        self.height = 500
        self.initUI()
        self.items = []

    # ============ Undo Method ============
    def undo(self):
        item = self.drawingBoard.removeKilns()
        if item == None: return
        self.items.append(item)

    # ============ Redo Method ============
    def redo(self):
        if len(self.items) == 0: return
        item = self.items.pop()
        self.drawingBoard.addKilns(item)

    # ============ Test Method ============
    def test(self, toolbar, image):
        button_action = QAction(QIcon(image), "Your button", self)
        toolbar.addAction(button_action)
        toolbar.addSeparator()

    # ============ create_push_button Method ============
    def create_push_button(self, image):
        button = QPushButton()
        button.setIcon(QIcon(image))
        button.setMaximumWidth(20)
        button.setFixedWidth(25)
        return button

    # ============ create_qlabel_with_images Method ============
    def create_qlabel_with_images(self, image):
        label = QLabel()
        pixmap = QPixmap(image)
        pixmap = pixmap.scaled(40, 40, Qt.KeepAspectRatio, Qt.FastTransformation)
        label.setPixmap(pixmap)
        return label

    # ============ create_qlabel_with_images Method ============
    def add_model_images(self, mimeName, image, name2, layout_image, ratio1=100, ratio2=100):
        kiln = QDragLabel(mimeName)
        pixmap = QPixmap(image)
        pixmap = pixmap.scaled(ratio1, ratio2, Qt.KeepAspectRatio, Qt.FastTransformation)
        kiln.setPixmap(pixmap)
        layout_image.addWidget(kiln)
        bold_name1 = QLabel(name2)
        bold_name1.setStyleSheet("font-weight:bold")
        layout_image.addWidget(bold_name1)

    # ============ initUI Method ============
    def initUI(self):

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        mainMenu = self.menuBar()
        self.Component = Component()

        # ========== newAction ===========
        newAction = QAction('&New', self)
        newAction.setShortcut('CTRL+N')
        newAction.setStatusTip('New Document')
        # newAction.triggered.connect(self.newCall)

        # ========== openAction ===========
        openAction = QAction('&Open', self)
        openAction.setShortcut('CTRL+O')
        openAction.setStatusTip('Open Document')
        # openAction.triggered.connect(self.OpenCall)

        # ========== exitAction ===========
        exitAction = QAction('&Exit', self)
        exitAction.setShortcut('CTRL+Q')
        exitAction.setStatusTip('Exit Application')
        # exitAction.triggered.connect(self.ExitCall)

        # ========== compAction ===========
        compAction = QAction('&Component Database', self)
        compAction.setStatusTip('Connect to Component Database')
        compAction.triggered.connect(self.Component.exec_)

        # ========== compAction ===========
        eleAction = QAction('&Element Database', self)
        eleAction.setStatusTip('Connect to Element Database')
        # eleAction.triggered.connect()

        # ========== file menu ===========
        fileMenu = mainMenu.addMenu('File')
        fileMenu.addAction(newAction)
        fileMenu.addAction(openAction)
        fileMenu.addSeparator()
        fileMenu.addAction(exitAction)

        # ========== Edit menu ===========
        editMenu = mainMenu.addMenu('Edit')
        editMenu.addAction(compAction)
        editMenu.addAction(eleAction)

        # ========== View menu ===========
        viewMenu = mainMenu.addMenu('View')

        # ========== Search menu ===========
        searchMenu = mainMenu.addMenu('Graphics')

        # ========== Tools menu ===========
        toolsMenu = mainMenu.addMenu('Model')

        # ========== run menu ===========
        runMenu = mainMenu.addMenu('Run')

        # ========== help menu ===========
        helpMenu = mainMenu.addMenu('Help')

        # toolbar feature
        toolbar = QToolBar("My main toolbar")
        self.addToolBar(toolbar)
        toolbar.setIconSize(QSize(20, 20))
        for i in range(12):
            self.test(toolbar, "images/image" + str(i))
        # create toolbar
        self.toolbar = QToolBar()
        # create toolbar label
        # ======= left arrow tool bar ===========
        self.left = ToolbarArrow("left")
        self.left.setToolTip("Left Arrow")
        # add label to toolbars
        self.toolbar.addWidget(self.left)
        self.toolbar.addSeparator()

        # ======= right arrow tool bar ===========
        self.right = ToolbarArrow("right")
        self.right.setToolTip("Right Arrow")
        # add label to toolbars
        self.toolbar.addWidget(self.right)
        self.toolbar.addSeparator()

        # ======= top arrow tool bar ===========
        self.top = ToolbarArrow("top")
        self.top.setToolTip("Top Arrow")
        # add label to toolbars
        self.toolbar.addWidget(self.top)
        self.toolbar.addSeparator()

        # ======= down arrow tool bar ===========
        self.down = ToolbarArrow("down")
        self.down.setToolTip("Down Arrow")
        # add label to toolbars
        self.toolbar.addWidget(self.down)
        self.toolbar.addSeparator()
        # add toolbars to window
        self.addToolBar(self.toolbar)
        # done done
        layout = QGridLayout()
        layout.setRowStretch(0, 1)
        layout.setRowStretch(1, 9)
        layout1 = QHBoxLayout()

        label = QLabel('Browser')
        buttons = []
        ii = 13
        for i in range(6):
            buttons.append(self.create_push_button("images/image_" + str(ii)))
            ii += 1
        input = QLineEdit()
        input.setPlaceholderText("Model")
        input.setFocus()
        input.setMaximumWidth(400)
        input.setFixedWidth(420)

        layout1.addWidget(label)
        layout1.addWidget(buttons[0])

        layout1.addWidget(buttons[1])
        layout1.addWidget(buttons[2])
        layout1.addWidget(buttons[3])
        layout1.addWidget(buttons[4])
        layout1.addWidget(buttons[5])
        layout1.addWidget(input)

        layout2 = QHBoxLayout()

        layout_fn = QVBoxLayout()
        layout_drag = QVBoxLayout()
        layout_image = QVBoxLayout()

        layout_fn.setSpacing(5)

        name_label = QLabel("Model")
        name_label.setStyleSheet("font-weight:bold")
        layout_fn.addWidget(name_label)
        layout_fn.setAlignment(Qt.AlignRight)
        feature_images = []
        for i in range(3):
            feature_images.append(self.create_qlabel_with_images("images/icon1.png"))

        layout_fn.addWidget(feature_images[0])
        layout_fn.addWidget(QLabel("Hose_Flow_Rate"))
        layout_fn.addWidget(feature_images[1])
        layout_fn.addWidget(QLabel("Input_Rate"))
        i1 = self.create_qlabel_with_images("images/icon2.png")
        layout_fn.addWidget(i1)
        layout_fn.addWidget(QLabel("Leakage_Fraction"))
        layout_fn.addWidget(feature_images[2])
        layout_fn.addWidget(QLabel("Tank_Capacity"))
        layout_fn.addStretch()

        calculate = QPushButton('Calculate')
        calculate.setStyleSheet("background-color : #2366a8;color: white")
        calculate.setMaximumWidth(100)
        calculate.setFixedWidth(120)

        layout_drag.addWidget(calculate)
        textEdit = DrawingPanel()

        # adding a property dynamically
        self.drawingBoard = textEdit
        textEdit = QGraphicsView(textEdit)
        rcontent = textEdit.contentsRect()
        textEdit.setSceneRect(0, 0, rcontent.width(), rcontent.height())

        layout_drag.addWidget(textEdit)
        # undo redo
        buttons[5].clicked.connect(self.redo)
        buttons[4].clicked.connect(self.undo)

        bold_name = QLabel("              Model")
        bold_name.setStyleSheet("font-weight:bold")
        layout_image.addWidget(bold_name)

        self.add_model_images("kiln", "images/kiln.png", "                Kiln", layout_image)
        self.add_model_images("kiln2", "images/kiln2", "                Kiln2", layout_image)

        layout_image.addStretch()

        layout2.addLayout(layout_fn)
        layout2.addLayout(layout_drag)
        layout2.addLayout(layout_image)

        layout.addLayout(layout1, 0, 0)
        layout.addLayout(layout2, 1, 0)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.show()


# =======================if __name__ == '__main__'======================
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    app.exec_()
