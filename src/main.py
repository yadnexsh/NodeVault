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
import json


image_file = r"H:\Gamut\Projects\NodeVault\media\image.png"
file_path =  r"H:\Gamut\Projects\NodeVault\env\studio_shared_folder"
json_file = os.path.join(file_path , "gizmo_file.json")
FIXED_POLICY = QSizePolicy.Policy.Fixed


class NodeVault_GUI(QWidget):  # CHANGED: renamed from two separate classes
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

        self.init_library_ui()
        self.init_submit_ui()

        # -------------- ASSEMBLE MAIN WINDOW --------------
        self.main_layout.addWidget(self.primary_tabs)

    def init_library_ui(self):

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

        self.all_filter = QWidget()
        self.temp_filter = QWidget()

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
        for each in range(1, MAX_ROWS + 1):
            row_options.append(str(each))
        self.row_cbx.addItems(row_options)

        col_options = []
        for each in range(1, MAX_COLS + 1):
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
        
        
        

    def init_submit_ui(self):  

        # -------------- SUBMIT TAB LAYOUT --------------
        self.submit_layout = QHBoxLayout(self.submit_tab)
        self.main_left_box = QVBoxLayout()
        self.main_right_box = QVBoxLayout()

        self.btn_submit = QPushButton("Submit")
        r_hbox_1 = QHBoxLayout()
        self.group_boxes_layout = QGridLayout()
        self.submit_lbl = QLabel("Submit to Dataset")
        self.filetype_lbl = QLabel("File Type")

        self.main_lbl = QLabel("Main File")
        self.description_lbl = QLabel("Description")

        # ------------- File Type Box -----------
        self.filetype_box = QGroupBox("FileType")
        self.filetype_box_layout = QGridLayout(self.filetype_box)

        self.gizmo_btn = QPushButton("Gizmo")
        self.script_btn = QPushButton("Script")
        self.template_btn = QPushButton("Template")

        self.filetype_box_layout.addWidget(self.gizmo_btn, 0, 0)
        self.filetype_box_layout.addWidget(self.script_btn, 0, 1)
        self.filetype_box_layout.addWidget(self.template_btn, 0, 2)

        file_group = QGroupBox("Main File")
        file_layout = QVBoxLayout(file_group)

        self.file_label = QLabel()
        self.file_label.setText("No Image")
        file_layout.addWidget(self.file_label)

        desc_group = QGroupBox("Description")
        desc_layout = QVBoxLayout(desc_group)

        self.desc_edit = QLineEdit()
        self.desc_edit.setPlaceholderText("Enter description…")
        desc_layout.addWidget(self.desc_edit)

        r_hbox_1.addWidget(desc_group)
        
        
        # -------- Information Box ---------------
        self.information_box = QGroupBox("Information")
        self.information_box_layout = QHBoxLayout(self.information_box)

        left_form = QFormLayout()
        right_form = QFormLayout()

        self.filename_le = QLineEdit()
        self.author_le = QLineEdit()
        self.version_le = QLineEdit()
        self.tagline_le = QLineEdit()
        
        left_form.addRow("Filename:", self.filename_le)
        left_form.addRow("Author:", self.author_le)

        right_form.addRow("Version:", self.version_le)
        right_form.addRow("Tagline:", self.tagline_le)

        self.information_box_layout.addLayout(left_form)
        self.information_box_layout.addLayout(right_form)

        # --- Category Options ---
        self.category_box = QGroupBox("Category")
        self.category_layout = QGridLayout(self.category_box)

        self.btn_templates = QPushButton("Templates")
        self.btn_gizmos = QPushButton("Gizmos")
        self.btn_tricks = QPushButton("Tricks")
        self.btn_misc = QPushButton("Misc")

        self.category_layout.addWidget(self.btn_templates, 0, 0)
        self.category_layout.addWidget(self.btn_gizmos, 0, 1)
        self.category_layout.addWidget(self.btn_tricks, 0, 2)
        self.category_layout.addWidget(self.btn_misc, 1, 0)

        # --- Sub-Category Options ---
        self.sub_category_box = QGroupBox("Sub Category")
        self.sub_category_layout = QGridLayout(self.sub_category_box)

        self.btn_deep = QPushButton("Deep")
        self.btn_draw = QPushButton("Draw")
        self.btn_time = QPushButton("Time")
        self.btn_image = QPushButton("Image")
        self.btn_channel = QPushButton("Channel")
        self.btn_filter = QPushButton("Filter")

        self.sub_category_layout.addWidget(self.btn_deep, 0, 0)
        self.sub_category_layout.addWidget(self.btn_draw, 0, 1)
        self.sub_category_layout.addWidget(self.btn_time, 0, 2)
        self.sub_category_layout.addWidget(self.btn_image, 1, 0)
        self.sub_category_layout.addWidget(self.btn_channel, 0, 0)
        self.sub_category_layout.addWidget(self.btn_filter, 0, 1)

        # --- Language Options ---
        self.language_box = QGroupBox("Language")
        self.language_box_layout = QGridLayout(self.language_box)

        self.btn_python = QPushButton("Python")
        self.btn_c = QPushButton("C++")

        self.language_box_layout.addWidget(self.btn_python, 0, 0)
        self.language_box_layout.addWidget(self.btn_c, 0, 1)

        # --- Render Options ---
        self.render_box = QGroupBox("Render")
        self.render_box_layout = QGridLayout(self.render_box)

        self.btn_cpu = QPushButton("CPU")
        self.btn_gpu = QPushButton("GPU")

        self.render_box_layout.addWidget(self.btn_cpu, 0, 0)
        self.render_box_layout.addWidget(self.btn_gpu, 0, 1)

        # -------- External Links Box ---------------
        self.external_box = QGroupBox("External_links")
        self.external_box_layout = QHBoxLayout(self.external_box)

        left_form = QFormLayout()
        right_form = QFormLayout()
        
        self.link_1 = QLineEdit()
        self.link_2 = QLineEdit()
        self.link_3 = QLineEdit()
        self.link_4 = QLineEdit()
        
        left_form.addRow("Repo:", self.link_1)
        left_form.addRow("Issues:", self.link_2)

        right_form.addRow("Website:", self.link_3)
        right_form.addRow("Extra:", self.link_4)

        self.external_box_layout.addLayout(left_form)
        self.external_box_layout.addLayout(right_form)



        self.group_boxes_layout.addWidget(self.category_box, 0, 0)
        self.group_boxes_layout.addWidget(self.sub_category_box, 1, 0)
        self.group_boxes_layout.addWidget(self.language_box, 0, 1)
        self.group_boxes_layout.addWidget(self.render_box, 1, 1)

        self.main_left_box.addWidget(self.filetype_box)
        self.main_left_box.addWidget(self.information_box)
        self.main_left_box.addLayout(self.group_boxes_layout)

        self.main_right_box.addLayout(r_hbox_1)
        self.main_right_box.addWidget(self.external_box)
        self.main_right_box.addWidget(self.btn_submit)

        self.submit_layout.addLayout(self.main_left_box)
        self.submit_layout.addLayout(self.main_right_box)


# -------------------------------------------------------------
    
        self.btn_submit.clicked.connect(self.on_submit)
    
    def get_information(self):
        filename = self.filename_le.text()
        author = self.author_le.text()
        version = self.version_le.text()
        tagline = self.tagline_le.text()
        return filename, author, version, tagline
    
    def get_externals(self):
        link_1 = self.link_1.text()
        link_2 = self.link_2.text()
        link_3 = self.link_3.text()
        link_4 = self.link_4.text()
        return link_1, link_2, link_3, link_4

    def on_submit(self):
        filename, author, version, tagline = self.get_information()
        link_1, link_2, link_3, link_4 = self.get_externals()
        data = {
            "filename": filename,
            "author":   author,
            "version":  version,
            "tagline":  tagline,
            "Link 1" : link_1,
            "Link 2" : link_2,
            "Link 3" : link_3,
            "Link 4" : link_4,
            
        }
        
        with open(json_file, "w") as file:
            json.dump(data, file, indent=4)
            
            
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = NodeVault_GUI()
    window.show()
    sys.exit(app.exec())