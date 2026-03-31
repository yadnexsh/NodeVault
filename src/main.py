from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QSizePolicy,
    QLabel,
    QComboBox,
    QTabWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout
)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
import sys
import os

image_file = r"C:\Users\Radha\Desktop\test.png"
FIXED_POLICY = QSizePolicy.Policy.Fixed

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Node Vault")
        self.initUI()

    def initUI(self):
        self.main_layout = QVBoxLayout(self)

        self.tabs = QTabWidget()
        self.library_tab = QWidget()

        library_tab_outer = QVBoxLayout(self.library_tab)

        # ----- THUMB GRID ----
        self.library_tab_layout = QGridLayout()
        rows = 4
        columns = 3
        for row in range(rows):
            for col in range(columns):
                thumb = QLabel()
                thumb.setPixmap(QPixmap(image_file))
                self.library_tab_layout.addWidget(thumb, row, col)
        library_tab_outer.addLayout(self.library_tab_layout)

        # ----- ROW COL OPTION ----
        # controls_outer_layout = QHBoxLayout()
        self.controls_layout = QHBoxLayout()

        self.row_lbl = QLabel("Rows")
        self.col_lbl = QLabel("Columns")
        self.row_cbx = QComboBox()
        self.row_cbx.addItem("- ")
        self.col_cbx = QComboBox()
        self.col_cbx.addItem("5")
        # self.row_lbl.setAlignment()
        # test_lbl = QLabel("Test")
        # controls_outer_layout.addWidget(test_lbl)
        # self.controls_lbl = QLabel("Grid Controls")
        
        self.row_lbl.setSizePolicy(FIXED_POLICY, FIXED_POLICY)
        self.row_cbx.setSizePolicy(FIXED_POLICY, FIXED_POLICY)
        self.col_lbl.setSizePolicy(FIXED_POLICY, FIXED_POLICY)
        self.col_cbx.setSizePolicy(FIXED_POLICY, FIXED_POLICY)
        
        # self.controls_layout.addWidget(self.controls_lbl)
        # self.controls_layout.addStretch(1)
        self.controls_layout.setContentsMargins(100,0,1,0)
        self.controls_layout.addWidget(self.row_lbl)
        self.controls_layout.addWidget(self.row_cbx)
        self.controls_layout.addWidget(self.col_lbl)
        
        self.controls_layout.addWidget(self.col_cbx)
        
        # controls_outer_layout.addLayout(self.controls_layout)
        library_tab_outer.addLayout(self.controls_layout)

        # ----- TABS ----
        self.submit_tab = QWidget()
        self.tabs.addTab(self.library_tab, "Library")
        self.tabs.addTab(self.submit_tab, "Submit")

        self.main_layout.addWidget(self.tabs)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())