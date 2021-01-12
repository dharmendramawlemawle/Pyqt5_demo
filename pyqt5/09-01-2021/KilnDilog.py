from PyQt5.QtWidgets import *
from PyQt5 import QtCore


# ===================== Class KilnDilog ======================
class KilnDilog(QDialog):
    def __init__(self):
        super().__init__()
        self.setupUi()
        self.dialogbuttonBox()
        self.inputsolidLayout()
        self.outputsolidLayout()
        self.inputgasLayout()
        self.outputgasLaout()

    def dialogbuttonBox(self):
        # ================ Dialog box Buttons ================
        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setGeometry(QtCore.QRect(20, 410, 611, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

    def inputsolidLayout(self):
        # ================ Input Solid Layout ================
        self.input_solid_layout = QVBoxLayout()
        self.input_solid_layout.setObjectName("input_solid_layout")

        self.Input_solid_label = QLabel(self.layoutWidget)
        self.Input_solid_label.setAlignment(QtCore.Qt.AlignCenter)
        self.Input_solid_label.setObjectName("Input_solid_label")
        self.input_solid_layout.addWidget(self.Input_solid_label)

        self.horizontalLayout_1 = QHBoxLayout()
        self.horizontalLayout_1.setObjectName("horizontalLayout_1")

        self.input_solid_box_1 = QLineEdit(self.layoutWidget)
        self.input_solid_box_1.setObjectName("input_solid_box_1")
        self.horizontalLayout_1.addWidget(self.input_solid_box_1)

        self.input_solid_box_2 = QLineEdit(self.layoutWidget)
        self.input_solid_box_2.setObjectName("input_solid_box_2")
        self.horizontalLayout_1.addWidget(self.input_solid_box_2)

        self.input_solid_layout.addLayout(self.horizontalLayout_1)
        self.Input_solid_label.setText("Input Solid")
        self.maingridLayout.addLayout(self.input_solid_layout, 0, 0, 1, 1)

    def outputsolidLayout(self):
        # ================ Output Solid Layout ================
        self.output_solid_layout = QVBoxLayout()
        self.output_solid_layout.setObjectName("output_solid_layout")

        self.output_solid_label = QLabel(self.layoutWidget)
        self.output_solid_label.setAlignment(QtCore.Qt.AlignCenter)
        self.output_solid_label.setObjectName("output_solid_label")

        self.output_solid_layout.addWidget(self.output_solid_label)

        self.output_solid_box = QLineEdit(self.layoutWidget)
        self.output_solid_box.setObjectName("output_solid_box")

        self.output_solid_layout.addWidget(self.output_solid_box)
        self.output_solid_label.setText("Output Solid")
        self.maingridLayout.addLayout(self.output_solid_layout, 1, 0, 1, 1)

    def inputgasLayout(self):
        # ================ Input Gas layout  ================
        self.input_gas_layout = QVBoxLayout()
        self.input_gas_layout.setObjectName("input_gas_layout")

        self.input_gas_label = QLabel(self.layoutWidget)
        self.input_gas_label.setAlignment(QtCore.Qt.AlignCenter)
        self.input_gas_label.setObjectName("input_gas_label")

        self.input_gas_layout.addWidget(self.input_gas_label)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")

        self.input_gas_box_1 = QLineEdit(self.layoutWidget)
        self.input_gas_box_1.setObjectName("input_gas_box_1")

        self.horizontalLayout_2.addWidget(self.input_gas_box_1)

        self.input_gas_box_2 = QLineEdit(self.layoutWidget)
        self.input_gas_box_2.setObjectName("input_gas_box_2")

        self.horizontalLayout_2.addWidget(self.input_gas_box_2)
        self.input_gas_layout.addLayout(self.horizontalLayout_2)
        self.input_gas_label.setText("Input Gas")
        self.maingridLayout.addLayout(self.input_gas_layout, 0, 2, 1, 1)

    def outputgasLaout(self):
        # ================ Output Gas Layout ================
        self.output_gas_layout = QVBoxLayout()
        self.output_gas_layout.setObjectName("output_gas_layout")

        self.output_gas_label = QLabel(self.layoutWidget)
        self.output_gas_label.setAlignment(QtCore.Qt.AlignCenter)
        self.output_gas_label.setObjectName("output_gas_label")

        self.output_gas_layout.addWidget(self.output_gas_label)
        self.output_gas_box = QLineEdit(self.layoutWidget)
        self.output_gas_box.setObjectName("output_gas_box")
        self.output_gas_layout.addWidget(self.output_gas_box)
        self.output_gas_label.setText("Output Gas")
        self.maingridLayout.addLayout(self.output_gas_layout, 1, 2, 1, 1)

    def setupUi(self):
        # ================ Dialog Window ================
        self.setWindowTitle("Kiln")
        self.resize(640, 455)

        # ================ Tab Widget ================
        self.tabWidget = QTabWidget(self)
        self.tabWidget.setGeometry(QtCore.QRect(20, 10, 601, 381))
        self.tabWidget.setObjectName("tabWidget")
        self.input_tab = QWidget()
        self.input_tab.setObjectName("input_tab")
        self.tabWidget.addTab(self.input_tab, "")
        self.reaction_tab = QWidget()
        self.reaction_tab.setObjectName("reaction_tab")
        self.tabWidget.addTab(self.reaction_tab, "")

        # ================ Tab input Layout ================
        self.layoutWidget = QWidget(self.input_tab)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 10, 270, 131))
        self.layoutWidget.setObjectName("layoutWidget")

        # ================ Main Grid Layout ================
        self.maingridLayout = QGridLayout(self.layoutWidget)
        self.maingridLayout.setContentsMargins(0, 0, 0, 0)
        self.maingridLayout.setObjectName("maingridLayout")

        # ================ Vertical Spacer ================
        spacerItem = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.maingridLayout.addItem(spacerItem, 0, 1, 2, 1)

        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(self)

        self.tabWidget.setTabText(self.tabWidget.indexOf(self.input_tab), "Input")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.reaction_tab), "Reaction")
