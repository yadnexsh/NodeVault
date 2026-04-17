from PySide2.QtWidgets import (
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
    QMessageBox,
    QFrame
)
from PySide2.QtGui import QPixmap, QStandardItemModel, QStandardItem, QIcon
from PySide2.QtCore import Qt, Slot, QSize
import sys
import os
import json
import datetime
import uuid
import shutil

CURRENT_FILEDIR = os.path.dirname(__file__)
ROOT_FOLDER = os.path.dirname(CURRENT_FILEDIR)

MEDIA_FOLDER = os.path.join(CURRENT_FILEDIR, "media")
ICON_FOLDER = os.path.join(MEDIA_FOLDER, "icons")

NUKE_FOLDER = os.path.join((os.path.expanduser("~")), ".nuke")
OUTPUT_FOLDER =  os.path.join(NUKE_FOLDER, "NodeVault_output")
GIZMO_FOLDER = os.path.join(OUTPUT_FOLDER,"Gizmos")

USERNAME = os.getlogin()

ICON_IMAGE_PATH = os.path.join(ICON_FOLDER, "ICON_image.png")
ICON_VIDEO_PATH = os.path.join(ICON_FOLDER, "ICON_video.png")

FIXED_POLICY = QSizePolicy.Policy.Fixed
FILETYPE_FOLDERS = ["Gizmos"]


class NodeVault_GUI(QWidget):
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Node Vault")
        self.resize(1300, 600)
        
        try:
            if os.path.exists(OUTPUT_FOLDER):
                print("Output folder exists")
            else:
                os.makedirs(OUTPUT_FOLDER, exist_ok=True)
                print(f"Created Output folder.")
                
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
        self.init_submit_ui()

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

        self.gizmos_item = QStandardItem("Gizmo")
        self.deep_item = QStandardItem("Deep")
        self.image_item = QStandardItem("Image")
        self.draw_item = QStandardItem("Draw")
        self.time_item = QStandardItem("Time")
        self.channel_item = QStandardItem("Channel")
        self.filter_item = QStandardItem("Filter")

        model.appendRow(self.gizmos_item)
        self.gizmos_item.appendRow(self.deep_item)
        self.gizmos_item.appendRow(self.image_item)
        self.gizmos_item.appendRow(self.draw_item)
        self.gizmos_item.appendRow(self.time_item)
        self.gizmos_item.appendRow(self.channel_item)
        self.gizmos_item.appendRow(self.filter_item)

        self.category_panel.setModel(model)
        self.category_panel.expandAll()
        
        self.category_panel.clicked.connect(self.on_category_panel_clicked)
        
        # -------------- ACTIVE FILTER BAR --------------
        self.tabs = QTabWidget()

        self.library_tab = QWidget()


        self.tabs.addTab(self.library_tab, "Library")
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tabs)

        # -------------- GIZMO GRID (inside All filter) --------------
        self.files_grid_layout = QGridLayout()
        self.library_tab.setLayout(self.files_grid_layout)

        # -------------- CONTENT AREA LAYOUT  --------------
        self.right_panel_layout = QVBoxLayout()
        self.right_panel_layout.addWidget(self.tabs)

        # -------------- ASSEMBLE LIBRARY TAB --------------
        self.library_master_layout.addWidget(self.category_panel)
        self.library_master_layout.addLayout(self.right_panel_layout)
        
        
    def init_submit_ui(self):

        # -------------- MASTER SUBMIT LAYOUT --------------
        self.submit_master_layout = QVBoxLayout(self.submit_tab)
        
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
        self.information_box = QGroupBox("Basic Info")
        self.information_box_layout = QHBoxLayout(self.information_box)

        left_form = QFormLayout()
        right_form = QFormLayout()

        self.filename_le = QLineEdit()
        self.author_le = QLineEdit()
        self.version_le = QLineEdit()
        self.tagline_le = QLineEdit()
        self.author_le.setText(USERNAME)
        self.author_le.setReadOnly(True)
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
        self.filetype_bg.setExclusive(True)
        
        self.gizmo_btn = QPushButton("Gizmo")

        # Making The buttons Clickable
        for btn in [self.gizmo_btn]:
            btn.setCheckable(True)
            btn.setChecked(True)     
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
        desc_layout.addWidget(self.desc_edit)

        # --- Sub-Category Options  ---
        self.sub_category_box = QGroupBox("Sub Category")
        self.sub_category_layout = QHBoxLayout(self.sub_category_box)

        self.subcategory_bg = QButtonGroup(self)
        self.btn_deep = QPushButton("Deep")
        self.btn_draw = QPushButton("Draw")
        self.btn_time = QPushButton("Time")
        self.btn_image = QPushButton("Image")
        self.btn_channel = QPushButton("Channel")
        self.btn_filter = QPushButton("Filter")
        
        # Making The buttons Clickable
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
        
        # Making The buttons Clickable
        for btn in [self.btn_nuke_old, self.btn_nuke_new]:
            btn.setCheckable(True)
            self.nuke_bg.addButton(btn)
            self.nuke_box_layout.addWidget(btn)

        self.render_nuke_layout.addWidget(self.render_box)
        self.render_nuke_layout.addWidget(self.nuke_box)

        # -------- Docs Box ---------
        self.docs_box = QGroupBox("Docs")
        self.docs_box_layout = QVBoxLayout(self.docs_box)


        self.extra1_row_layout = QHBoxLayout()
        self.extra1_lbl = QLabel("No file selected")
        self.extra1_browse_btn = QPushButton("Browse")
        self.extra1_browse_btn.clicked.connect(self.on_extra1_browse_clicked)
        self.extra1_row_layout.addWidget(QLabel("Extra Doc 1:"))
        self.extra1_row_layout.addWidget(self.extra1_lbl)
        self.extra1_row_layout.addWidget(self.extra1_browse_btn)

        self.extra2_row_layout = QHBoxLayout()
        self.extra2_lbl = QLabel("No file selected")
        self.extra2_browse_btn = QPushButton("Browse")
        self.extra2_browse_btn.clicked.connect(self.on_extra2_browse_clicked)
        self.extra2_row_layout.addWidget(QLabel("Extra Doc 2:"))
        self.extra2_row_layout.addWidget(self.extra2_lbl)
        self.extra2_row_layout.addWidget(self.extra2_browse_btn)
        
        self.docs_box_layout.addLayout(self.extra1_row_layout)
        self.docs_box_layout.addLayout(self.extra2_row_layout)

        # -------- External Links Box -------
        self.external_box = QGroupBox("External Links")
        self.external_box_layout = QHBoxLayout(self.external_box)

        left_link_form = QFormLayout()
        right_link_form = QFormLayout()

        self.repo_link = QLineEdit()
        self.issues_link = QLineEdit()
        self.website_link = QLineEdit()
        self.extra_link = QLineEdit()

        left_link_form.addRow("Repo:", self.repo_link)
        left_link_form.addRow("Issues:", self.issues_link)
        right_link_form.addRow("Website:", self.website_link)
        right_link_form.addRow("Extra:", self.extra_link)

        self.external_box_layout.addLayout(left_link_form)
        self.external_box_layout.addLayout(right_link_form)

        # -------- Preview Images + Demo Video -----------
        self.media_box = QGroupBox("Preview Images & Demo Video")
        self.media_box_layout = QHBoxLayout(self.media_box)
        self.image_icon = QIcon(ICON_IMAGE_PATH)
        self.video_icon = QIcon(ICON_VIDEO_PATH)

        self.preview_btn_1 = QPushButton()
        self.preview_btn_2 = QPushButton()
        self.preview_btn_3 = QPushButton()
        self.preview_btn_4 = QPushButton()
        self.preview_btn_5 = QPushButton()
        self.demo_video_btn = QPushButton()
        self.IMAGE_BUTTONS = [self.preview_btn_1,self.preview_btn_2,self.preview_btn_3,self.preview_btn_4,self.preview_btn_5]
        for each_image_btn in self.IMAGE_BUTTONS:
            each_image_btn.setIcon(self.image_icon)
            each_image_btn.setIconSize(QSize(50, 50))
            
        self.demo_video_btn.setIcon(self.video_icon)
        self.demo_video_btn.setIconSize(QSize(50, 50))
        
        square_size = 100
        
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

        for each in self.IMAGE_BUTTONS:
            self.media_box_layout.addWidget(each)
        self.media_box_layout.addWidget(self.demo_video_btn)

        self.main_left_box.addWidget(self.information_box)
        self.main_left_box.addWidget(self.filetype_box)

        file_desc_layout = QHBoxLayout()
        file_desc_layout.addWidget(file_group)
        file_desc_layout.addWidget(desc_group)
        self.main_left_box.addLayout(file_desc_layout)
        
        self.main_left_box.addWidget(self.sub_category_box)
        self.main_left_box.addLayout(self.render_nuke_layout)

# ++++
        self.main_right_box.addWidget(self.docs_box)
        self.main_right_box.addWidget(self.external_box)
        self.main_right_box.addWidget(self.media_box)

        
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
        self.submit_master_layout.addStretch()
        
    # ***************** FUNC *******************

    def on_img_btn_clicked(self, button):
        path, _ = QFileDialog.getOpenFileName(
            self, "Select Preview Image", "",
            "Images (*.png *.jpg *.jpeg)"
        )
        if path:
            filename = os.path.basename(path)
            print(path)
            thumbnail = QIcon(path)
            button.setIcon(thumbnail)
            button.setIconSize(QSize(100, 100))
            self.attached_images.append(path)

    def on_video_btn_clicked(self, button):
        path, _ = QFileDialog.getOpenFileName(
            self, "Select Demo Video", "",
            "Video (*.mp4 *.mov *.avi)"
        )
        if path:
            filename = os.path.basename(path)
            button.setText(filename)
            self.attached_video.append(path)

    def on_doc_btn_clicked(self, button):
        path, _ = QFileDialog.getOpenFileName(
            self, "Select Extra Document", "",
            "PDF (*.pdf);;Doc File (*.doc)"
        )
        if path:
            filename = os.path.basename(path)
            button.setText(filename)
            self.extra_docs.append(path)
            
    # *********** UPDATE GUI > LABEL / STATUS  ******************
    
    # ------- Label Update : IMAGE & VIDEO BOX -----------
    @Slot()
    def on_preview_btn_1_clicked(self):
        self.on_img_btn_clicked(self.preview_btn_1)
        
    @Slot()
    def on_preview_btn_2_clicked(self):
        self.on_img_btn_clicked(self.preview_btn_2)
        
    @Slot()
    def on_preview_btn_3_clicked(self):
        self.on_img_btn_clicked(self.preview_btn_3)
        
    @Slot()
    def on_preview_btn_4_clicked(self):
        self.on_img_btn_clicked(self.preview_btn_4)
        
    @Slot()
    def on_preview_btn_5_clicked(self):
        self.on_img_btn_clicked(self.preview_btn_5)
        
    @Slot()
    def on_demo_video_btn_clicked(self):
        self.on_video_btn_clicked(self.demo_video_btn)

    # ------- Label Update : Main File -----------
    @Slot()
    def on_file_browse_clicked(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            "Select Main File", 
            "", 
            "Python Files (*.py);;Nuke Files (*.nk);;gizmo Files (*.gizmo)"
        )
        if file_path:
            self.main_file = file_path
            self.file_label.setText(os.path.basename(file_path))      
            
    # ------- Label Update : Extra Docs  -----------
    
    @Slot()
    def on_extra1_browse_clicked(self):
        self.on_doc_btn_clicked(self.extra1_lbl)
        
    @Slot()
    def on_extra2_browse_clicked(self):
        self.on_doc_btn_clicked(self.extra2_lbl)
        
    @Slot() 
    def save_json(self):
        
        # -------- ERROR LIST + VALIDATE INPUTS ------------
        errors = []
        
        if not self.main_file:
            e = "Please select a Main File."
            errors.append(e)
        
        if not self.filetype_bg.checkedButton():
            e = "Please select a File Type"
            errors.append(e)

        if not self.subcategory_bg.checkedButton():            
            e = "Please select Sub Category"
            errors.append(e)

        if not self.render_bg.checkedButton():            
            e = "Please select a Render Type."
            errors.append(e)

        if not self.nuke_bg.checkedButton():            
            e = "Please select a Nuke Version."
            errors.append(e)

        if not self.filename_le.text().strip():            
            e = "Please enter a File Name."
            errors.append(e)
            
        self.submission_id = str(uuid.uuid4())
        
        filetype = self.filetype_bg.checkedButton().text()

        submitted_time = datetime.datetime.now().isoformat(timespec='seconds')

        filename = self.filename_le.text().strip()
        author = self.author_le.text()
        version = 0 

        try:
            version_text = self.version_le.text().strip()
            if not version_text:
                errors.append("Version field is empty.")
            else:
                version = int(version_text)
                if version <= 0:
                    errors.append("Version cannot be negative.")
        except ValueError:
            errors.append("Version must be a whole number.")
        except Exception as e:
            errors.append(f"Version error: {e}")

        # - -- ERROR MSG ----
        if len(errors) != 0:
            error_string = "\n".join(f"- {each}" for each in errors)
            QMessageBox.critical(self, "Validation Errors", f"Please fix the following:\n{error_string}")
            return
        
        sub_category = self.subcategory_bg.checkedButton().text()
        render_type = self.render_bg.checkedButton().text()
        nuke_version = self.nuke_bg.checkedButton().text()
        description = self.desc_edit.toPlainText().strip()
        tagline = self.tagline_le.text().strip() 
        
        repo_link = self.repo_link.text()
        issues_link = self.issues_link.text()
        website_link = self.website_link.text()
        extra_link = self.extra_link.text()
        
        data = {
            "uuid": self.submission_id,
            "submitted": submitted_time,
            "filetype": filetype,
            "filename": filename,
            "author": author,
            "version": version,
            "sub_category": sub_category,
            "render": render_type,
            "nuke_version": nuke_version,
            "description": description ,
            "tagline": tagline ,
            "extra_docs": self.extra_docs,
            "repo_link": repo_link,
            "issues_link": issues_link,
            "website": website_link,
            "extra_link": extra_link,
            "attached_images": self.attached_images,
            "attached_video": self.attached_video
        }
        
        # Make Folder for Json File & Write JSON in it
        folder_map = {
            "Gizmo" : GIZMO_FOLDER,
        }
        
        try:
            save_dir = os.path.join(folder_map[filetype], self.submission_id)
            os.makedirs(save_dir, exist_ok=True) 
        except Exception as e:
            QMessageBox.critical(self, "Errors", f"Error > {e}")

            
        json_filename = os.path.join(save_dir, f"{self.submission_id}.json")
        
        try:
            with open(json_filename, "w") as file:
                json.dump(data, file, indent=4)
                
            file_extension = os.path.splitext(self.main_file)[1]
            new_filename = f"{self.submission_id}{file_extension}" 
            dst_path = os.path.join(save_dir, new_filename)
            shutil.copy(src=self.main_file, dst=dst_path)
            
            for docs_file in data["extra_docs"]:
                docs_folder = os.path.join(save_dir, "Docs")
                os.makedirs(docs_folder, exist_ok=True)
                shutil.copy(src=docs_file, dst=docs_folder)
            
            for image_file in data["attached_images"]:
                image_folder = os.path.join(save_dir, "Images")
                os.makedirs(image_folder, exist_ok=True)
                shutil.copy(src=image_file, dst=image_folder)
                
            for video_file in data["attached_video"]:
                video_folder = os.path.join(save_dir, "Videos")
                os.makedirs(video_folder, exist_ok=True)
                shutil.copy(src=video_file, dst=video_folder)
                
            QMessageBox.information(self, "Info", "The file has been submitted successfully.")
            
            # ----------- CLEARING AFTER SUBMITTING THE DATA ----------
            TEXT_FIELDS = [self.filename_le, self.version_le, self.tagline_le, self.repo_link, self.issues_link, self.website_link, self.extra_link , self.desc_edit]
            for each in TEXT_FIELDS:
                each.clear()
                
            LABEL_FIELDS = [self.file_label,self.extra1_lbl, self.extra2_lbl]

            for each in LABEL_FIELDS:
                label = each.text()
                each.setText("No file selected")
                    
            BUTTON_FIELDS = [self.subcategory_bg, self.render_bg, self.nuke_bg]
            for each in BUTTON_FIELDS:
                if each.checkedButton():
                    each.setExclusive(False)
                    each.checkedButton().setChecked(False)
                    each.setExclusive(True)
            
            self.main_file = []  
            self.attached_images = []
            self.attached_video = []
            self.extra_docs = []
            
            for each in self.IMAGE_BUTTONS:
                each.setIcon(self.image_icon)
                each.setIconSize(QSize(50, 50))
                
            self.demo_video_btn.setText("")
            self.demo_video_btn.setIcon(self.video_icon)
            self.demo_video_btn.setIconSize(QSize(50, 50))
            
        except Exception as e:
            QMessageBox.critical(self, "Errors", f"Error > {e}")

    
    @Slot() 
    def on_category_panel_clicked(self, index):
        
        folder_name = os.listdir(GIZMO_FOLDER)
        
        MAX_COLS = 10
        counter = 0
        
        clicked_text = index.data()
        print(clicked_text)
        
        square_size = 85
        
        while self.files_grid_layout.count():
            item = self.files_grid_layout.takeAt(0)
            item.widget().deleteLater()
        
        for each in folder_name:
            json_filename = f"{each}.json"
            each_folder_path = os.path.join(GIZMO_FOLDER, each)
            each_json = os.path.join(each_folder_path, json_filename)
            
            with open(each_json, "r") as file:
                data = json.load(file)
                submission_id = data["uuid"]
                filename = data["filename"]
                filetype = data["filetype"]
                sub_category = data["sub_category"]
            
            if clicked_text == filetype or clicked_text == sub_category:
                col = counter % MAX_COLS
                row = counter // MAX_COLS
                each = QPushButton(filename)
                each.setProperty("submission_id" , submission_id)
                each.clicked.connect(self.on_gizmo_button_clicked)
                each.setFixedSize(square_size, square_size)
                self.files_grid_layout.addWidget(each, row, col)
                
                counter += 1

        if counter > 0:
            self.files_grid_layout.setColumnStretch(MAX_COLS, 1)
            self.files_grid_layout.setRowStretch(row + 1, 1)
            
    def on_gizmo_button_clicked(self):
        
        button = self.sender()
        submission_id = button.property("submission_id")
        filetype_folder = os.path.join(GIZMO_FOLDER, submission_id)
        json_path = os.path.join(filetype_folder, f"{submission_id}.json")
            
        with open(json_path, "r") as file:
            data = json.load(file)
            
        # -----------------------------------------------
        self.detailed_tab = QWidget()        
        self.detailed_tab_layout = QHBoxLayout(self.detailed_tab)
        
        left_layout = QVBoxLayout()
        
        header_row = QHBoxLayout()
        
        self.det_filename = QLabel()
        filename_font = self.det_filename.font()
        filename_font.setBold(True)
        filename_font.setPointSize(24)
        self.det_filename.setFont(filename_font)
        
        self.det_author = QLabel()
        
        header_row.addWidget(self.det_filename)
        header_row.addWidget(self.det_author)
        header_row.addStretch()
        
        self.det_tagline = QLabel()
        desc_label = QLabel()
        self.det_desc = QTextEdit()
        self.det_desc.setReadOnly(True)

        left_layout.addLayout(header_row)
        left_layout.addWidget(self.det_tagline)
        left_layout.addWidget(desc_label)
        left_layout.addWidget(self.det_desc)

        right_layout = QVBoxLayout()

        # -------- Node Info Group -------------
        info_label = QLabel("Node Info")
        info_form = QFormLayout()
        info_form.addRow("Version", QLabel("v2.02.03"))
        info_form.addRow("Submitted", QLabel("16 Feb 2026"))
        info_form.addRow("Size", QLabel("23kb"))

        # --------- Resources Group -------
        res_label = QLabel("Resources")
        self.res_repo = QPushButton("Repo")
        self.res_issue = QPushButton("Issue")
        self.res_docs = QPushButton("Docs")
        self.subscribe = QPushButton("subscribe")
        right_layout.addWidget(info_label)
        right_layout.addLayout(info_form)
        right_layout.addWidget(res_label)
        right_layout.addWidget(self.res_repo)
        right_layout.addWidget(self.res_issue)
        right_layout.addWidget(self.res_docs)
        right_layout.addWidget(self.subscribe)
        right_layout.addStretch() 
        self.detailed_tab_layout.addLayout(left_layout, 7)  
        self.detailed_tab_layout.addLayout(right_layout, 3)
        self.subscribe.setProperty("object_id", submission_id)
        self.subscribe.clicked.connect(self.copy_object_file)
        
        
        self.det_filename.setText(data["filename"])
        self.det_author.setText(f"by {data['author']}")
        self.det_tagline.setText(data['tagline']) 
        self.det_desc.setPlainText(data["description"])
        index = self.tabs.indexOf(self.detailed_tab)
        index = self.tabs.addTab(self.detailed_tab, data["filename"])
        self.tabs.setCurrentIndex(index)

    def copy_object_file(self):
        subscribe_btn = self.sender()
        object_id = subscribe_btn.property("object_id")
        filetype_folder = os.path.join(GIZMO_FOLDER, object_id)
        print(filetype_folder)
        for each in os.listdir(filetype_folder):
            if each.endswith(".gizmo"):
                file = os.path.join(filetype_folder, each)


        
        shutil.copy(src=file, dst=nodevault_folder)
        
    def close_tabs(self, index):
        if index == 0:
            QMessageBox.critical(self, "Error", "You cant close ALL Tab")
        else:
            self.tabs.removeTab(index)

    def on_submit_clicked(self):
        self.save_json()

window =  None

def launch():
    global window
    window = NodeVault_GUI()
    window.show()
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NodeVault_GUI()
    window.show()
    sys.exit(app.exec_())