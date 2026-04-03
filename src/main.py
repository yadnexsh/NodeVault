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
    QButtonGroup
)
from PySide6.QtGui import QPixmap, QStandardItemModel, QStandardItem
from PySide6.QtCore import Qt, Slot
import sys
import os
import json
import datetime

image_file = r"H:\Gamut\Projects\node_vault\media\heavily_compressed.png"
OUTPUT_FOLDER = r"H:\Gamut\Projects\node_vault\output"
json_file = os.path.join(OUTPUT_FOLDER, "gizmo_file.json")
FIXED_POLICY = QSizePolicy.Policy.Fixed
GIZMO_PATH = r"H:\Gamut\Projects\node_vault\env\OUTPUT_FOLDER\files\Gizmos\gizmo_3_name"
USER_NUKE_PATH = r"H:\Gamut\Projects\node_vault\env\user_nuke"

class NodeVault_GUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Node Vault")
        self.resize(1300, 600)
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

        MAX_ROWS = 4
        MAX_COLS = 4

        for row in range(MAX_ROWS):
            for col in range(MAX_COLS):
                thumb = QLabel()
                thumb.setPixmap(QPixmap(image_file))
                self.files_grid_layout.addWidget(thumb, row, col)

        self.all_filter.setLayout(self.files_grid_layout)

        # -------------- CONTENT AREA LAYOUT  --------------
        self.right_panel_layout = QVBoxLayout()
        self.right_panel_layout.addWidget(self.filter_bar)

        # -------------- ASSEMBLE LIBRARY TAB --------------
        self.library_layout.addWidget(self.category_panel)
        self.library_layout.addLayout(self.right_panel_layout)


    def init_submit_ui(self):

        # -------------- MASTER SUBMIT LAYOUT --------------
        self.submit_master_layout = QVBoxLayout(self.submit_tab)
        
        # 1. Main Title at top left
        self.submit_lbl = QLabel("Submit to Dataset")
        title_font = self.submit_lbl.font()
        title_font.setPointSize(14)
        title_font.setBold(True)
        self.submit_lbl.setFont(title_font)
        
        self.submit_master_layout.addWidget(self.submit_lbl)
        self.submit_master_layout.addSpacing(10)


        self.columns_layout = QHBoxLayout()
        self.main_left_box = QVBoxLayout()
        self.main_right_box = QVBoxLayout()

        


        # -------- Information Box ---------------
        self.information_box = QGroupBox("X")
        self.information_box_layout = QHBoxLayout(self.information_box)

        left_form = QFormLayout()
        right_form = QFormLayout()

        self.filename_le = QLineEdit()
        self.author_le = QLineEdit()
        self.version_le = QLineEdit()
        self.tagline_le = QLineEdit()

        left_form.addRow("File Name:", self.filename_le)
        left_form.addRow("Version:", self.version_le)
        right_form.addRow("Author:", self.author_le)
        right_form.addRow("Tagline:", self.tagline_le)

        self.information_box_layout.addLayout(left_form)
        self.information_box_layout.addLayout(right_form)

        # ------------- File Type Box -----------
        self.filetype_box = QGroupBox("File Types")
        self.filetype_box_layout = QHBoxLayout(self.filetype_box) 
        
        self.filetype_bg = QButtonGroup(self)
        self.gizmo_btn = QPushButton("Gizmo")
        self.script_btn = QPushButton("Script")
        self.template_btn = QPushButton("Template")

        for btn in [self.gizmo_btn, self.script_btn, self.template_btn]:
            btn.setCheckable(True)
            self.filetype_bg.addButton(btn)
            self.filetype_box_layout.addWidget(btn)

        # ------------- Main File Box -----------
        file_group = QGroupBox("Main File")
        file_layout = QVBoxLayout(file_group)
        self.file_label = QLabel("No file selected")
        self.file_browse_btn = QPushButton("Browse")
        self.file_browse_btn.clicked.connect(self.on_file_browse_clicked)
        file_layout.addWidget(self.file_label)
        file_layout.addWidget(self.file_browse_btn)

        # ------------- Description Box -----------
        desc_group = QGroupBox("Description")
        desc_layout = QVBoxLayout(desc_group)
        self.desc_edit = QTextEdit()
        self.desc_edit.setPlaceholderText("Enter description…")
        self.desc_edit.setFixedHeight(80)
        desc_layout.addWidget(self.desc_edit)

        # --- Sub-Category Options  ---
        self.sub_category_box = QGroupBox("Sub Category")
        self.sub_category_layout = QHBoxLayout(self.sub_category_box)

        self.subcategory_bg = QButtonGroup(self)
        self.btn_deep    = QPushButton("Deep")
        self.btn_draw    = QPushButton("Draw")
        self.btn_time    = QPushButton("Time")
        self.btn_image   = QPushButton("Image")
        self.btn_channel = QPushButton("Channel")
        self.btn_filter  = QPushButton("Filter")

        for btn in [self.btn_deep, self.btn_draw, self.btn_time, self.btn_image, self.btn_channel, self.btn_filter]:
            btn.setCheckable(True)
            self.subcategory_bg.addButton(btn)
            self.sub_category_layout.addWidget(btn)
            



        # --- Render + Nuke Version  ---
        self.render_nuke_layout = QHBoxLayout()

        self.render_box = QGroupBox("Render")
        self.render_box_layout = QHBoxLayout(self.render_box)
        
        self.render_bg = QButtonGroup(self)
        self.btn_cpu = QPushButton("CPU")
        self.btn_gpu = QPushButton("GPU")
        
        for btn in [self.btn_cpu, self.btn_gpu]:
            btn.setCheckable(True)
            self.render_bg.addButton(btn)
            self.render_box_layout.addWidget(btn)

        self.nuke_box = QGroupBox("Nuke Version")
        self.nuke_box_layout = QHBoxLayout(self.nuke_box)
        
        self.nuke_bg = QButtonGroup(self)
        self.btn_nuke_old = QPushButton("Nuke13-")
        self.btn_nuke_new = QPushButton("Nuke13+")
        
        for btn in [self.btn_nuke_old, self.btn_nuke_new]:
            btn.setCheckable(True)
            self.nuke_bg.addButton(btn)
            self.nuke_box_layout.addWidget(btn)

        self.render_nuke_layout.addWidget(self.render_box)
        self.render_nuke_layout.addWidget(self.nuke_box)

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

        # -------- External Links Box -------
        self.external_box = QGroupBox("External Links")
        self.external_box_layout = QHBoxLayout(self.external_box)

        left_link_form = QFormLayout()
        right_link_form = QFormLayout()

        self.link_1 = QLineEdit()
        self.link_2 = QLineEdit()
        self.link_3 = QLineEdit()
        self.link_4 = QLineEdit()

        left_link_form.addRow("Repo:", self.link_1)
        left_link_form.addRow("Issues:", self.link_2)
        right_link_form.addRow("Website:", self.link_3)
        right_link_form.addRow("Extra:", self.link_4)

        self.external_box_layout.addLayout(left_link_form)
        self.external_box_layout.addLayout(right_link_form)

        # -------- Preview Images + Demo Video -----------
        self.media_box = QGroupBox("Preview Images & Demo Video")
        self.media_box_layout = QGridLayout(self.media_box)

        self.preview_btn_1 = QPushButton("Img 1")
        self.preview_btn_2 = QPushButton("Img 2")
        self.preview_btn_3 = QPushButton("Img 3")
        self.preview_btn_4 = QPushButton("Img 4")
        self.preview_btn_5 = QPushButton("Img 5")
        self.demo_video_btn = QPushButton("Demo Video")

        square_size = 65
        
        self.preview_btn_1.setFixedSize(square_size, square_size)
        self.preview_btn_2.setFixedSize(square_size, square_size)
        self.preview_btn_3.setFixedSize(square_size, square_size)
        self.preview_btn_4.setFixedSize(square_size, square_size)
        self.preview_btn_5.setFixedSize(square_size, square_size)
        self.demo_video_btn.setFixedSize(square_size, square_size)
        # ---------------------------

        self.preview_btn_1.clicked.connect(self.on_preview_btn_1_clicked)
        self.preview_btn_2.clicked.connect(self.on_preview_btn_2_clicked)
        self.preview_btn_3.clicked.connect(self.on_preview_btn_3_clicked)
        self.preview_btn_4.clicked.connect(self.on_preview_btn_4_clicked)
        self.preview_btn_5.clicked.connect(self.on_preview_btn_5_clicked)
        self.demo_video_btn.clicked.connect(self.on_demo_video_btn_clicked)

        self.media_box_layout.addWidget(self.preview_btn_1, 0, 0)
        self.media_box_layout.addWidget(self.preview_btn_2, 0, 1)
        self.media_box_layout.addWidget(self.preview_btn_3, 0, 2)
        self.media_box_layout.addWidget(self.preview_btn_4, 1, 0)
        self.media_box_layout.addWidget(self.preview_btn_5, 1, 1)
        self.media_box_layout.addWidget(self.demo_video_btn, 1, 2)


        #---

        self.main_left_box.addWidget(self.information_box)
        self.main_left_box.addWidget(self.filetype_box)

        file_desc_layout = QHBoxLayout()
        file_desc_layout.addWidget(file_group)
        file_desc_layout.addWidget(desc_group)
        self.main_left_box.addLayout(file_desc_layout)
        
        self.main_left_box.addWidget(self.sub_category_box)
        self.main_left_box.addLayout(self.render_nuke_layout)
        
        v_spacer_left = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)       # W H hdata policy and vdata policy
        self.main_left_box.addItem(v_spacer_left) 

# ++++
        self.main_right_box.addWidget(self.docs_box)
        self.main_right_box.addWidget(self.external_box)
        self.main_right_box.addWidget(self.media_box)
        
        v_spacer_right = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.main_right_box.addItem(v_spacer_right) 
        
        self.btn_submit = QPushButton("SUBMIT")
        self.btn_submit.setMinimumHeight(40) 
        self.btn_submit.setMinimumWidth(400)
        btn_font = self.btn_submit.font()
        btn_font.setBold(True)
        self.btn_submit.setFont(btn_font)
        
        self.btn_submit.clicked.connect(self.on_submit_clicked)


# ----
        self.columns_layout.addLayout(self.main_left_box)
        self.columns_layout.addLayout(self.main_right_box)
        
        self.submit_master_layout.addLayout(self.columns_layout)
        
        self.submit_master_layout.addWidget(self.btn_submit, alignment = Qt.AlignCenter)

# TEMP
    def temp_subscribe_ui(self):
        subscribe_tab = QWidget()
        subscribe_tab_layout = QHBoxLayout(subscribe_tab)
        self.btn_subscribe = QPushButton("Subs")
        subscribe_tab_layout.addWidget(self.btn_subscribe)
        self.primary_tabs.addTab(subscribe_tab, "Sub")

#------
    
    @Slot()
    def on_submit_clicked(self):
        filename = self.filename_le.text()
        if not filename:
            print("Submission failed: Filename is required!")
            return
        
        version = self.version_le.text() or "v001"
        
        filetype = "Unknown"
        if self.filetype_bg.checkedButton():
            filetype = self.filetype_bg.checkedButton().text()
            
        sub_category = "Unknown"
        if self.subcategory_bg.checkedButton():
            sub_category = self.subcategory_bg.checkedButton().text()
            
        render_type = "Unknown"
        if self.render_bg.checkedButton():
            render_type = self.render_bg.checkedButton().text()
            
        nuke_version = "Unknown"
        if self.nuke_bg.checkedButton():
            nuke_version = self.nuke_bg.checkedButton().text()
            
        readme_text = self.readme_lbl.text()
        if readme_text == "No file":
            readme = ""
        else:
            readme = readme_text
            
        extra_docs = []
        doc1_text = self.extra1_lbl.text()
        if doc1_text != "No file":
            extra_docs.append(doc1_text)
            
        doc2_text = self.extra2_lbl.text()
        if doc2_text != "No file":
            extra_docs.append(doc2_text)
            


# IMG AND VIDEO pending

        data = {
            "id": "pending",
            "submiited": datetime.datetime.now().isoformat(timespec='seconds'),
            "filetype": filetype,
            "filename": filename,
            "author": self.author_le.text(),
            "version": version,
            "sub_category": sub_category,
            "tags": [], 
            "render": render_type,
            "nuke_version": nuke_version,
            "description": self.desc_edit.toPlainText(),
            "tagline": self.tagline_le.text(),
            "readme": readme,
            "extra_docs": extra_docs,
            "repo_link": self.link_1.text(),
            "issues_link": self.link_2.text(),
            "website": self.link_3.text(),
            "extra_link": self.link_4.text(),
            "attached_images": "pending",
            "attached_video": "pending"
        }

        safe_filename = os.path.splitext(filename)[0]
        save_path = os.path.join(OUTPUT_FOLDER, f"{safe_filename}.json")
        
        try:
            os.makedirs(OUTPUT_FOLDER, exist_ok=True)
            with open(save_path, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=4)
            # print(f"Success! Saved data to: {save_path}")
        except Exception as e:
            print(f"Error saving file: {e}")


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
    window = NodeVault_GUI()
    window.show()
    sys.exit(app.exec())