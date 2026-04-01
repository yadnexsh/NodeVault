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
    QGroupBox, QLineEdit, QFormLayout,
    QTextEdit, QFileDialog
)
from PySide6.QtGui import QPixmap, QStandardItemModel, QStandardItem
from PySide6.QtCore import Qt , Slot
import sys
import os
import json


image_file = r"H:\Gamut\Projects\node_vault\media\image.png"
STUDIO_SHARED_FOLDER =  r"H:\Gamut\Projects\node_vault\env\studio_shared_folder"
json_file = os.path.join(STUDIO_SHARED_FOLDER , "gizmo_file.json")
FIXED_POLICY = QSizePolicy.Policy.Fixed
GIZMO_PATH = r"H:\Gamut\Projects\node_vault\env\studio_shared_folder\files\Gizmos\gizmo_3_name"
USER_NUKE_PATH = r"H:\Gamut\Projects\node_vault\env\user_nuke"

class NodeVault_GUI(QWidget):
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
        self.temp_subscribe_ui()

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

        # -------------- CONTENT AREA LAYOUT  --------------
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

        # ------------- Main File Box -----------
        file_group = QGroupBox("Main File")
        file_layout = QVBoxLayout(file_group)

        self.file_label = QLabel()
        self.file_label.setText("No file selected")
        file_layout.addWidget(self.file_label)

        self.file_browse_btn = QPushButton("Browse")
        self.file_browse_btn.clicked.connect(self.on_file_browse_clicked)
        file_layout.addWidget(self.file_browse_btn)

        # ------------- Description Box -----------
        desc_group = QGroupBox("Description")
        desc_layout = QVBoxLayout(desc_group)

        self.desc_edit = QTextEdit()
        self.desc_edit.setPlaceholderText("Enter description…")
        self.desc_edit.setFixedHeight(80)
        desc_layout.addWidget(self.desc_edit)

        r_hbox_1.addWidget(file_group)
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

        # --- Sub-Category Options  ---
        self.sub_category_box = QGroupBox("Sub Category")
        self.sub_category_layout = QHBoxLayout(self.sub_category_box)

        self.btn_deep    = QPushButton("Deep")
        self.btn_draw    = QPushButton("Draw")
        self.btn_time    = QPushButton("Time")
        self.btn_image   = QPushButton("Image")
        self.btn_channel = QPushButton("Channel")
        self.btn_filter  = QPushButton("Filter")

        self.sub_category_layout.addWidget(self.btn_deep)
        self.sub_category_layout.addWidget(self.btn_draw)
        self.sub_category_layout.addWidget(self.btn_time)
        self.sub_category_layout.addWidget(self.btn_image)
        self.sub_category_layout.addWidget(self.btn_channel)
        self.sub_category_layout.addWidget(self.btn_filter)

        # --- Render + Nuke Version  ---
        self.render_nuke_layout = QHBoxLayout()

        self.render_box = QGroupBox("Render")
        self.render_box_layout = QHBoxLayout(self.render_box)

        self.btn_cpu = QPushButton("CPU")
        self.btn_gpu = QPushButton("GPU")

        self.render_box_layout.addWidget(self.btn_cpu)
        self.render_box_layout.addWidget(self.btn_gpu)

        self.nuke_box = QGroupBox("Nuke Version")
        self.nuke_box_layout = QHBoxLayout(self.nuke_box)

        self.btn_nuke_old = QPushButton("Nuke13-")
        self.btn_nuke_new = QPushButton("Nuke13+")

        self.nuke_box_layout.addWidget(self.btn_nuke_old)
        self.nuke_box_layout.addWidget(self.btn_nuke_new)

        self.render_nuke_layout.addWidget(self.render_box)
        self.render_nuke_layout.addWidget(self.nuke_box)

        # -------- External Links Box -------
        self.external_box = QGroupBox("External Links")
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

        # -------- Docs Box ---------
        self.docs_box = QGroupBox("Docs")
        self.docs_box_layout = QVBoxLayout(self.docs_box)

        readme_row = QHBoxLayout()
        self.readme_lbl = QLabel("No file")
        self.readme_browse_btn = QPushButton("Browse README.md")
        self.readme_browse_btn.clicked.connect(self.on_readme_browse_clicked)
        readme_row.addWidget(QLabel("README:"))
        readme_row.addWidget(self.readme_lbl)
        readme_row.addWidget(self.readme_browse_btn)

        extra1_row = QHBoxLayout()
        self.extra1_lbl = QLabel("No file")
        self.extra1_browse_btn = QPushButton("Browse")
        self.extra1_browse_btn.clicked.connect(self.on_extra1_browse_clicked)
        extra1_row.addWidget(QLabel("Extra Doc 1:"))
        extra1_row.addWidget(self.extra1_lbl)
        extra1_row.addWidget(self.extra1_browse_btn)

        extra2_row = QHBoxLayout()
        self.extra2_lbl = QLabel("No file")
        self.extra2_browse_btn = QPushButton("Browse")
        self.extra2_browse_btn.clicked.connect(self.on_extra2_browse_clicked)
        extra2_row.addWidget(QLabel("Extra Doc 2:"))
        extra2_row.addWidget(self.extra2_lbl)
        extra2_row.addWidget(self.extra2_browse_btn)

        self.docs_box_layout.addLayout(readme_row)
        self.docs_box_layout.addLayout(extra1_row)
        self.docs_box_layout.addLayout(extra2_row)

        # -------- Preview Images + Demo Video -----------
        self.media_box = QGroupBox("Preview Images & Demo Video")
        self.media_box_layout = QHBoxLayout(self.media_box)

        self.preview_btn_1 = QPushButton("Img 1")
        self.preview_btn_2 = QPushButton("Img 2")
        self.preview_btn_3 = QPushButton("Img 3")
        self.preview_btn_4 = QPushButton("Img 4")
        self.preview_btn_5 = QPushButton("Img 5")
        self.demo_video_btn = QPushButton("Demo Video")

        self.preview_btn_1.clicked.connect(self.on_preview_btn_1_clicked)
        self.preview_btn_2.clicked.connect(self.on_preview_btn_2_clicked)
        self.preview_btn_3.clicked.connect(self.on_preview_btn_3_clicked)
        self.preview_btn_4.clicked.connect(self.on_preview_btn_4_clicked)
        self.preview_btn_5.clicked.connect(self.on_preview_btn_5_clicked)
        self.demo_video_btn.clicked.connect(self.on_demo_video_btn_clicked)

        self.media_box_layout.addWidget(self.preview_btn_1)
        self.media_box_layout.addWidget(self.preview_btn_2)
        self.media_box_layout.addWidget(self.preview_btn_3)
        self.media_box_layout.addWidget(self.preview_btn_4)
        self.media_box_layout.addWidget(self.preview_btn_5)
        self.media_box_layout.addWidget(self.demo_video_btn)

        # -------------- ASSEMBLE LEFT --------------
        self.main_left_box.addWidget(self.filetype_box)
        self.main_left_box.addWidget(self.information_box)
        self.main_left_box.addWidget(self.sub_category_box)
        self.main_left_box.addLayout(self.render_nuke_layout)

        # -------------- ASSEMBLE RIGHT --------------
        self.main_right_box.addLayout(r_hbox_1)
        self.main_right_box.addWidget(self.docs_box)
        self.main_right_box.addWidget(self.external_box)
        self.main_right_box.addWidget(self.media_box)
        self.main_right_box.addWidget(self.btn_submit)

        self.submit_layout.addLayout(self.main_left_box)
        self.submit_layout.addLayout(self.main_right_box)


    def temp_subscribe_ui(self):
        subscribe_tab = QWidget()
        subscribe_tab_layout = QHBoxLayout(subscribe_tab)
        self.btn_subscribe = QPushButton("Subs")
        subscribe_tab_layout.addWidget(self.btn_subscribe)
        self.primary_tabs.addTab(subscribe_tab, "Sub")


    # SLOTS

    @Slot()
    def on_file_browse_clicked(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Select Main File", "",
            "Nuke files (*.gizmo *.py *.nk);;All files (*)"
        )
        if path:
            self.file_label.setText(os.path.basename(path))
            
    @Slot()
    def on_readme_browse_clicked(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Select README", "",
            "Markdown (*.md);;Text (*.txt);;All files (*)"
        )
        if path:
            self.readme_lbl.setText(os.path.basename(path))
            
            
    @Slot()
    def on_extra1_browse_clicked(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Select Extra Doc 1", "",
            "PDF (*.pdf);;All files (*)"
        )
        if path:
            self.extra1_lbl.setText(os.path.basename(path))

    @Slot()
    def on_extra2_browse_clicked(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Select Extra Doc 2", "",
            "PDF (*.pdf);;All files (*)"
        )
        if path:
            self.extra2_lbl.setText(os.path.basename(path))


    @Slot()
    def on_preview_btn_1_clicked(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Select Preview Image 1", "",
            "Images (*.png *.jpg *.jpeg);;All files (*)"
        )
        if path:
            self.preview_btn_1.setText(os.path.basename(path))

    @Slot()
    def on_preview_btn_2_clicked(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Select Preview Image 2", "",
            "Images (*.png *.jpg *.jpeg);;All files (*)"
        )
        if path:
            self.preview_btn_2.setText(os.path.basename(path))

    
    @Slot()
    def on_preview_btn_3_clicked(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Select Preview Image 3", "",
            "Images (*.png *.jpg *.jpeg);;All files (*)"
        )
        if path:
            self.preview_btn_3.setText(os.path.basename(path))

    
    @Slot()
    def on_preview_btn_4_clicked(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Select Preview Image 4", "",
            "Images (*.png *.jpg *.jpeg);;All files (*)"
        )
        if path:
            self.preview_btn_4.setText(os.path.basename(path))

    
    @Slot()
    def on_preview_btn_5_clicked(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Select Preview Image 5", "",
            "Images (*.png *.jpg *.jpeg);;All files (*)"
        )
        if path:
            self.preview_btn_5.setText(os.path.basename(path))

    @Slot()
    def on_demo_video_btn_clicked(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Select Demo Video", "",
            "Video (*.mp4 *.mov *.avi);;All files (*)"
        )
        if path:
            self.demo_video_btn.setText(os.path.basename(path))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = NodeVault_GUI()
    window.show()
    sys.exit(app.exec())