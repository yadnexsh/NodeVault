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
    QGroupBox, 
    QLineEdit, 
    QFormLayout,
    QTextEdit, 
    QFileDialog,
    QSpacerItem,
    QButtonGroup,
    QMessageBox
)
from PySide6.QtGui import QPixmap, QStandardItemModel, QStandardItem, QIcon
from PySide6.QtCore import Qt, Slot, QSize
import sys
import os
import json
import datetime
import uuid
import shutil

ROOT_FOLDER = r"H:\Gamut\Projects\node_vault"


MEDIA_FOLDER = os.path.join(ROOT_FOLDER, "media")
ICON_FOLDER = os.path.join(MEDIA_FOLDER, "icons")

OUTPUT_FOLDER = os.path.join(ROOT_FOLDER, "output")
GIZMO_FOLDER = os.path.join(OUTPUT_FOLDER,"Gizmos")
TEMPLATE_FOLDER = os.path.join(OUTPUT_FOLDER,"Template")
SCRIPT_FOLDER = os.path.join(OUTPUT_FOLDER,"Scripts")

USERNAME = os.getlogin()

THUMBNAIL_FILE = os.path.join(MEDIA_FOLDER, "heavily_compressed.png")
IMAGE_ICON_PATH = os.path.join(ICON_FOLDER, "image_icon.png")
VIDEO_ICON_PATH = os.path.join(ICON_FOLDER, "video_icon.png")

FIXED_POLICY = QSizePolicy.Policy.Fixed
FILETYPE_FOLDERS = ["Gizmos"]


class NodeVault_GUI(QWidget):
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Node Vault")
        self.resize(1300, 600)
        
        try:
            for each in FILETYPE_FOLDERS:
                if not each in os.listdir(OUTPUT_FOLDER):
                    each_folder = os.path.join(OUTPUT_FOLDER,f"{each}")
                    os.makedirs(each_folder)
                    print(f"Created {each} folder.")
                else:
                    print(f"{each} folder already exists.")
        except Exception as e:
            print(f"{e}")
            
        self.initUI()
        self.main_file = []
        self.attached_images = []
        self.attached_video = []
        self.extra_docs = []
        
    def initUI(self):

        # -------------- MAIN LAYOUT --------------
        self.main_layout = QVBoxLayout(self)

        # -------------- PRIMARY TABS (Library / Submit) --------------
        self.primary_tabs = QTabWidget()

        self.library_tab = QWidget()
        self.submit_tab = QWidget()

        self.primary_tabs.addTab(self.library_tab, "Library")
        self.primary_tabs.addTab(self.submit_tab, "Submit")

        self.init_library_ui()


        # -------------- ASSEMBLE MAIN WINDOW --------------
        self.main_layout.addWidget(self.primary_tabs)

    def init_library_ui(self):

        # -------------- LIBRARY TAB LAYOUT --------------
        self.library_master_layout = QHBoxLayout(self.library_tab)

        # -------------- CATEGORY PANEL (Tree View) --------------
        self.category_panel = QTreeView()
        self.category_panel.setFixedWidth(300)
        self.category_panel.setEditTriggers(QTreeView.NoEditTriggers) 

        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(["Category"])

        # self.template_item = QStandardItem("Templates")
        self.gizmos_item = QStandardItem("Gizmos")
        self.deep_item = QStandardItem("Deep")
        self.image_item = QStandardItem("Image")
        self.draw_item = QStandardItem("Draw")
        self.time_item = QStandardItem("Time")
        self.channel_item = QStandardItem("Channel")
        self.filter_item = QStandardItem("Filter")
        # self.tricks_item = QStandardItem("Tricks")
        # self.misc_item = QStandardItem("Misc")

        # model.appendRow(self.template_item)

        model.appendRow(self.gizmos_item)
        self.gizmos_item.appendRow(self.deep_item)
        self.gizmos_item.appendRow(self.image_item)
        self.gizmos_item.appendRow(self.draw_item)
        self.gizmos_item.appendRow(self.time_item)
        self.gizmos_item.appendRow(self.channel_item)
        self.gizmos_item.appendRow(self.filter_item)

        # model.appendRow(self.tricks_item)
        # model.appendRow(self.misc_item)

        self.category_panel.setModel(model)
        self.category_panel.expandAll()
        
        self.category_panel.clicked.connect(self.on_category_panel_clicked)
        # -------------- ACTIVE FILTER BAR --------------
        self.tabs = QTabWidget()

        self.all_tab = QWidget()
        self.temp_tab = QWidget()

        self.tabs.addTab(self.all_tab, "All")
        self.tabs.addTab(self.temp_tab, "Temp")

        # -------------- GIZMO GRID (inside All filter) --------------
        self.files_grid_layout = QGridLayout()
        self.all_tab.setLayout(self.files_grid_layout)


        # -------------- CONTENT AREA LAYOUT  --------------
        self.right_panel_layout = QVBoxLayout()
        self.right_panel_layout.addWidget(self.tabs)

        # -------------- ASSEMBLE LIBRARY TAB --------------
        self.library_master_layout.addWidget(self.category_panel)
        self.library_master_layout.addLayout(self.right_panel_layout)
        
        
        
    def on_category_panel_clicked(self, index):
        
        folder_name = os.listdir(GIZMO_FOLDER)
        MAX_COLS = 4
        counter = 0
        clicked_test = index.data()
        
        while self.files_grid_layout.count():
            item = self.files_grid_layout.takeAt(0)
            item.widget().deleteLater()
        
        for each in folder_name:
            filename = f"{each}.json"
            each_folder = os.path.join(GIZMO_FOLDER, each)
            each_json = os.path.join(each_folder, filename)
            
            with open(each_json, "r") as file:
                data = json.load(file)
                filename = data["filename"]
                sub_category = data["sub_category"]
            
            if clicked_test == sub_category:
                row = counter // MAX_COLS
                col = counter % MAX_COLS
                each = QPushButton(filename)
                self.files_grid_layout.addWidget(each, row, col)
                counter += 1
                

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NodeVault_GUI()
    window.show()
    sys.exit(app.exec())