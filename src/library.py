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
    QGridLayout,
    QTreeView
)
from PySide6.QtGui import QPixmap, QStandardItemModel, QStandardItem
from PySide6.QtCore import Qt
import sys
import os

image_file = r"H:\Gamut\Projects\NodeVault\media\image.png"
FIXED_POLICY = QSizePolicy.Policy.Fixed


class LibraryTab_GUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Node Vault")
        self.initUI()

    def initUI(self):

        # -------------- MAIN LAYOUT --------------
        self.main_layout = QVBoxLayout(self)

        # -------------- PRIMARY TABS (Library / Submit) --------------
        self.primary_tabs = QTabWidget()

        self.library_tab = QWidget()
        self.submit_tab = QWidget()

        self.primary_tabs.addTab(self.library_tab, "Library")
        self.primary_tabs.addTab(self.submit_tab, "Submit")

        # -------------- LIBRARY TAB LAYOUT --------------
        self.library_layout = QHBoxLayout(self.library_tab)

        # -------------- CATEGORY PANEL (Tree View) --------------
        self.category_panel = QTreeView()
        self.category_panel.setFixedWidth(300)

        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(["Category"])

        template_item = QStandardItem("Templates")
        gizmos_item = QStandardItem("Gizmos")
        deep_item = QStandardItem("Deep")
        image_item = QStandardItem("Image")
        draw_item = QStandardItem("Draw")
        time_item = QStandardItem("Time")
        channel_item = QStandardItem("Channel")
        filter_item = QStandardItem("Filter")
        tricks_item = QStandardItem("Tricks")
        misc_item = QStandardItem("Misc")

        model.appendRow(template_item)

        model.appendRow(gizmos_item)
        gizmos_item.appendRow(deep_item)
        gizmos_item.appendRow(image_item)
        gizmos_item.appendRow(draw_item)
        gizmos_item.appendRow(time_item)
        gizmos_item.appendRow(channel_item)
        gizmos_item.appendRow(filter_item)

        model.appendRow(tricks_item)
        model.appendRow(misc_item)

        self.category_panel.setModel(model)
        
        

        # -------------- ACTIVE FILTER BAR --------------
        self.filter_bar = QTabWidget()

        self.all_filter    = QWidget()
        self.temp_filter   = QWidget()

        self.filter_bar.addTab(self.all_filter, "All")
        self.filter_bar.addTab(self.temp_filter, "Temp")

        # -------------- GIZMO GRID (inside All filter) --------------
        self.files_grid_layout = QGridLayout()

        rows = 4
        columns = 3

        for row in range(rows):
            for col in range(columns):
                thumb = QLabel()
                thumb.setPixmap(QPixmap(image_file))
                self.files_grid_layout.addWidget(thumb, row, col)

        self.all_filter.setLayout(self.files_grid_layout)

        # -------------- DISPLAY CONTROLS (Rows / Columns) --------------
        self.display_controls_layout = QHBoxLayout()

        self.row_lbl = QLabel("Rows")
        self.col_lbl = QLabel("Columns")
        self.row_cbx = QComboBox()
        self.col_cbx = QComboBox()

        MAX_ROWS = 5
        MAX_COLS = 5
        
        row_options = []
        for each in range(1 , MAX_ROWS + 1):
            row_options.append(str(each))
        self.row_cbx.addItems(row_options)
        
        col_options = []
        for each in range(1 , MAX_COLS + 1):
            col_options.append(str(each))
        self.col_cbx.addItems(col_options)

        self.row_lbl.setSizePolicy(FIXED_POLICY, FIXED_POLICY)
        self.row_cbx.setSizePolicy(FIXED_POLICY, FIXED_POLICY)
        self.col_lbl.setSizePolicy(FIXED_POLICY, FIXED_POLICY)
        self.col_cbx.setSizePolicy(FIXED_POLICY, FIXED_POLICY)

        self.display_controls_layout.addStretch()
        self.display_controls_layout.addWidget(self.row_lbl)
        self.display_controls_layout.addWidget(self.row_cbx)
        self.display_controls_layout.addWidget(self.col_lbl)
        self.display_controls_layout.addWidget(self.col_cbx)

        # -------------- CONTENT AREA LAYOUT (filter bar + controls) --------------
        self.right_panel_layout = QVBoxLayout()
        self.right_panel_layout.addWidget(self.filter_bar)
        self.right_panel_layout.addLayout(self.display_controls_layout)

        # -------------- ASSEMBLE LIBRARY TAB --------------
        self.library_layout.addWidget(self.category_panel)
        self.library_layout.addLayout(self.right_panel_layout)

        # -------------- ASSEMBLE MAIN WINDOW --------------
        self.main_layout.addWidget(self.primary_tabs)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = LibraryTab_GUI()
    window.show()
    sys.exit(app.exec())