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
    QTreeView,
    QGroupBox, QLineEdit, QFormLayout
)
from PySide6.QtGui import QPixmap, QStandardItemModel, QStandardItem
from PySide6.QtCore import Qt
import sys
import os

image_file = r"H:\Gamut\Projects\NodeVault\media\image.png"
FIXED_POLICY = QSizePolicy.Policy.Fixed


class SubmitTab_GUI(QWidget):
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
        # self.primary_tabs.setTabBar(self.submit_tab)


        # -------------- LIBRARY TAB LAYOUT --------------
        self.library_layout = QHBoxLayout(self.library_tab)
        
        # -------------- LIBRARY TAB LAYOUT --------------
        self.submit_layout = QHBoxLayout(self.submit_tab)
        left_vbox = QVBoxLayout()
        right_vbox = QVBoxLayout()
        l_vbox_1 = QVBoxLayout()
        l_hbox_1 = QHBoxLayout()
        r_hbox_1 = QHBoxLayout()
        l_grid = QGridLayout()
        l_btns_grid =  QGridLayout()
        self.submit_lbl = QLabel("Submit to Dataset")
        self.filetype_lbl = QLabel("File Type")
        self.gizmo_btn = QPushButton("Gizmo")
        self.script_btn = QPushButton("Gizmo")
        self.template_btn = QPushButton("Gizmo")
        self.main_lbl = QLabel("Main File")
        self.description_lbl = QLabel("Description")
        
        
        file_group = QGroupBox("Main File")
        file_layout = QVBoxLayout(file_group)

        self.file_label = QLabel()
        # self.file_label.setFixedSize(90, 90)
        # self.file_label.setAlignment(Qt.AlignCenter)
        self.file_label.setText("No Image")
        file_layout.addWidget(self.file_label)

        desc_group = QGroupBox("Description")
        desc_layout = QVBoxLayout(desc_group)

        self.desc_edit = QLineEdit()
        self.desc_edit.setPlaceholderText("Enter description…")
        desc_layout.addWidget(self.desc_edit)

        # Row 0
        l_grid.addWidget(QLabel("Name:"),0, 0)
        l_grid.addWidget(QLineEdit(),0, 1)
        l_grid.addWidget(QLabel("Email:"),0, 2)
        l_grid.addWidget(QLineEdit(),0, 3)

        # Row 1
        l_grid.addWidget(QLabel("Phone:"),1, 0)
        l_grid.addWidget(QLineEdit(),1, 1)
        l_grid.addWidget(QLabel("City:"),1, 2)
        l_grid.addWidget(QLineEdit(),1, 3)
        r_hbox_1.addWidget(file_group)
        r_hbox_1.addWidget(desc_group)

        category_box = QGroupBox("Category")
        category_layout = QGridLayout(category_box)

        self.btn_templates = QPushButton("Templates")
        self.btn_gizmos = QPushButton("Gizmos")
        self.btn_tricks = QPushButton("Tricks")
        self.btn_misc = QPushButton("Misc")

        category_layout.addWidget(self.btn_templates,0, 0)
        category_layout.addWidget(self.btn_gizmos,0, 1)
        category_layout.addWidget(self.btn_tricks,0, 2)
        category_layout.addWidget(self.btn_misc,1, 0)
        
        sub_category_box = QGroupBox("Sub Cat")
        sub_category_layout = QGridLayout(sub_category_box)
        
        self.x = QPushButton("Templates")
        self.y = QPushButton("Gizmos")
        self.z = QPushButton("Tricks")
        self.c = QPushButton("Misc")

        
        
        l_btns_grid.addWidget(category_box, 0, 0)
        
        l_vbox_1.addWidget(self.submit_lbl)
        l_vbox_1.addWidget(self.filetype_lbl)
        l_hbox_1.addWidget(self.gizmo_btn)
        l_hbox_1.addWidget(self.script_btn)
        l_hbox_1.addWidget(self.template_btn)
        
        left_vbox.addLayout(l_vbox_1)
        
        
        left_vbox.addLayout(l_hbox_1)
        left_vbox.addLayout(l_btns_grid)
        
        left_vbox.addLayout(l_grid)
        
        right_vbox.addLayout(r_hbox_1)
        self.submit_layout.addLayout(left_vbox)
        self.submit_layout.addLayout(right_vbox)
        
        
        self.main_layout.addWidget(self.primary_tabs)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = SubmitTab_GUI()
    window.show()
    sys.exit(app.exec())