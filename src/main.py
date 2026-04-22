from PySide2.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QSizePolicy,
    QLabel,
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
from PySide2.QtGui import QPixmap, QStandardItemModel, QStandardItem, QIcon, QDesktopServices
from PySide2.QtCore import Qt, Slot, QSize, QUrl

import sys
import os
import json
import datetime
import uuid
import shutil

# ============================================================
#  PATH CONSTANTS
# ============================================================
# All folder paths resolved once at import time.

CURRENT_FILEDIR = os.path.dirname(__file__)
ROOT_FOLDER = os.path.dirname(CURRENT_FILEDIR)

NUKE_FOLDER = os.path.join((os.path.expanduser("~")), ".nuke")
NODEVAULT_USER_FOLDER = os.path.join(NUKE_FOLDER, "NodeVault_User")

MEDIA_FOLDER = os.path.join(CURRENT_FILEDIR, "media")
ICON_FOLDER = os.path.join(MEDIA_FOLDER, "icons")

NODEVAULT_STUDIO_FOLDER =  os.path.join(ROOT_FOLDER, "NodeVault_Studio")
GIZMO_FOLDER = os.path.join(NODEVAULT_STUDIO_FOLDER,"Gizmos")

# ============================================================
#  MISC CONSTANTS
# ============================================================

USERNAME = os.getlogin()
ICON_IMAGE_PATH = os.path.join(ICON_FOLDER, "ICON_image.png")
FIXED_POLICY = QSizePolicy.Policy.Fixed
FILETYPE_FOLDERS = ["Gizmos"]

print("--" * 40)

# ============================================================
#  MAIN WINDOW
# ============================================================

class NodeVault_GUI(QWidget):
    
    def __init__(self):
        """
        Set up the main window, ensure required studio folders exist,
        and initialise attachment state lists.
        """
        super().__init__()
        self.setWindowTitle("Node Vault")
        self.resize(1300, 600)
        
        # ----------------------------------------------------------
        #  FOLDER SETUP  –  create NodeVault_Studio + sub-folders
        # ----------------------------------------------------------
        try:
            if os.path.exists(NODEVAULT_STUDIO_FOLDER):
                print("NODEVAULT_STUDIO_FOLDER folder exists")
            else:
                os.makedirs(NODEVAULT_STUDIO_FOLDER, exist_ok=True)
                print(f"Created NODEVAULT_STUDIO_FOLDER folder.")
                
            for each in FILETYPE_FOLDERS:
                if not each in os.listdir(NODEVAULT_STUDIO_FOLDER):
                    each_folder = os.path.join(NODEVAULT_STUDIO_FOLDER,f"{each}")
                    os.makedirs(each_folder)
                    print(f"Created {each} folder.")
                else:
                    print(f"{each} folder already exists.")
        except Exception as e:
            print(f"{e}")
            
        self.initUI()

        # ----------------------------------------------------------
        #  ATTACHMENT STATE  –  populated when the user browses files
        # ----------------------------------------------------------
        self.main_file = []
        self.attached_images = []
        self.extra_docs = []
        
    # ============================================================

    def initUI(self):
        """
        Build the top-level layout and the two primary tabs
        (Library and Submit).
        """

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

    # ============================================================

    def init_library_ui(self):
        """
        Build the Library tab: left category tree + right closable
        content tabs with a grid of gizmo buttons.
        """
        
        # -------------- LIBRARY TAB LAYOUT --------------
        self.library_master_layout = QHBoxLayout(self.library_tab)

        # -------------- CATEGORY PANEL (Tree View) --------------
        # Fixed-width tree showing Gizmo sub-categories.
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
        # Closable tab widget that holds the library grid and detail tabs.
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

        # Select Gizmo root by default and populate the grid.
        default_index = self.gizmos_item.index()
        self.category_panel.setCurrentIndex(default_index)
        self.on_category_panel_clicked(default_index)
        
    # ============================================================

    def init_submit_ui(self):
        """
        Build the Submit tab: all input groups (info, file type, main
        file, description, sub-category, render/nuke, docs, links, media).
        """

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
        # Name, version, author, and tagline fields.
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
        # Exclusive button group – currently only Gizmo is supported.
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
        # Browse and display the selected .gizmo file path.
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
        # Exclusive toggle buttons mapping to the tree categories.
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
        # Two independent exclusive groups placed side by side.
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
        # Up to two optional supplementary documents (PDF / DOC).
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
        # Optional repo, issues, website, and extra URL fields.
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
        # Five fixed-size image buttons; icons update when images are picked.
        self.media_box = QGroupBox("Preview Images & Demo Video")
        self.media_box_layout = QHBoxLayout(self.media_box)
        self.image_icon = QIcon(ICON_IMAGE_PATH)

        self.preview_btn_1 = QPushButton()
        self.preview_btn_2 = QPushButton()
        self.preview_btn_3 = QPushButton()
        self.preview_btn_4 = QPushButton()
        self.preview_btn_5 = QPushButton()

        self.IMAGE_BUTTONS = [self.preview_btn_1,self.preview_btn_2,self.preview_btn_3,self.preview_btn_4,self.preview_btn_5]
        for each_image_btn in self.IMAGE_BUTTONS:
            each_image_btn.setIcon(self.image_icon)
            each_image_btn.setIconSize(QSize(50, 50))

        square_size = 100
        
        self.preview_btn_1.setFixedSize(square_size, square_size)
        self.preview_btn_2.setFixedSize(square_size, square_size)
        self.preview_btn_3.setFixedSize(square_size, square_size)
        self.preview_btn_4.setFixedSize(square_size, square_size)
        self.preview_btn_5.setFixedSize(square_size, square_size)

        self.preview_btn_1.clicked.connect(self.on_preview_btn_1_clicked)
        self.preview_btn_2.clicked.connect(self.on_preview_btn_2_clicked)
        self.preview_btn_3.clicked.connect(self.on_preview_btn_3_clicked)
        self.preview_btn_4.clicked.connect(self.on_preview_btn_4_clicked)
        self.preview_btn_5.clicked.connect(self.on_preview_btn_5_clicked)

        for each in self.IMAGE_BUTTONS:
            self.media_box_layout.addWidget(each)

        # ----------------------------------------------------------
        #  ASSEMBLE LEFT + RIGHT COLUMNS
        # ----------------------------------------------------------

        self.main_left_box.addWidget(self.information_box)
        self.main_left_box.addWidget(self.filetype_box)

        file_desc_layout = QHBoxLayout()
        file_desc_layout.addWidget(file_group)
        file_desc_layout.addWidget(desc_group)
        self.main_left_box.addLayout(file_desc_layout)
        
        self.main_left_box.addWidget(self.sub_category_box)
        self.main_left_box.addLayout(self.render_nuke_layout)

        self.main_right_box.addWidget(self.docs_box)
        self.main_right_box.addWidget(self.external_box)
        self.main_right_box.addWidget(self.media_box)

        # ----------------------------------------------------------
        #  SUBMIT BUTTON
        # ----------------------------------------------------------
        
        self.btn_submit = QPushButton("SUBMIT")
        self.btn_submit.setMinimumHeight(40) 
        self.btn_submit.setMinimumWidth(400)
        btn_font = self.btn_submit.font()
        btn_font.setBold(True)
        self.btn_submit.setFont(btn_font)
        
        self.btn_submit.clicked.connect(self.on_submit_clicked)

        self.columns_layout.addLayout(self.main_left_box)
        self.columns_layout.addLayout(self.main_right_box)
        
        self.submit_master_layout.addLayout(self.columns_layout)
        self.submit_master_layout.addWidget(self.btn_submit, alignment = Qt.AlignCenter)
        self.submit_master_layout.addStretch()

    # ============================================================
    #  FILE DIALOG HELPERS
    # ============================================================

    def on_img_btn_clicked(self, button):
        """
        Open an image file dialog, set the button icon to a thumbnail,
        and append the path to attached_images.
        """
        path, _ = QFileDialog.getOpenFileName(
            self, "Select Preview Image", "",
            "Images (*.png *.jpg *.jpeg)"
        )
        if path:
            filename = os.path.basename(path)
            thumbnail = QIcon(path)
            button.setIcon(thumbnail)
            button.setIconSize(QSize(100, 100))
            self.attached_images.append(path)

    def on_doc_btn_clicked(self, button):
        """
        Open a document file dialog, update the label text,
        and append the path to extra_docs.
        """
        path, _ = QFileDialog.getOpenFileName(
            self, "Select Extra Document", "",
            "PDF (*.pdf);;Doc File (*.doc)"
        )
        if path:
            filename = os.path.basename(path)
            button.setText(filename)
            self.extra_docs.append(path)

    # ============================================================
    #  PREVIEW IMAGE BUTTON SLOTS
    # ============================================================
    # Each slot delegates to on_img_btn_clicked with its own button.
            
    # @Slot()
    def on_preview_btn_1_clicked(self):
        self.on_img_btn_clicked(self.preview_btn_1)
        
    # @Slot()
    def on_preview_btn_2_clicked(self):
        self.on_img_btn_clicked(self.preview_btn_2)
        
    # @Slot()
    def on_preview_btn_3_clicked(self):
        self.on_img_btn_clicked(self.preview_btn_3)
        
    # @Slot()
    def on_preview_btn_4_clicked(self):
        self.on_img_btn_clicked(self.preview_btn_4)
        
    # @Slot()
    def on_preview_btn_5_clicked(self):
        self.on_img_btn_clicked(self.preview_btn_5)

    # ============================================================
    #  MAIN FILE + EXTRA DOCS SLOTS
    # ============================================================

    # @Slot()
    def on_file_browse_clicked(self):
        """
        Open a .gizmo file dialog and update the file label
        with the selected filename.
        """
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            "Select Main File", 
            "", 
            "gizmo Files (*.gizmo)"
        )
        if file_path:
            self.main_file = file_path
            self.file_label.setText(os.path.basename(file_path))      
            
    # @Slot()
    def on_extra1_browse_clicked(self):
        self.on_doc_btn_clicked(self.extra1_lbl)
        
    # @Slot()
    def on_extra2_browse_clicked(self):
        self.on_doc_btn_clicked(self.extra2_lbl)

    # ============================================================
    #  SAVE / SUBMIT
    # ============================================================
        
    # @Slot() 
    def save_json(self):
        """
        Validate all required fields, build the metadata dict, create
        the submission folder, write the JSON, and copy all attached files.
        Clears the form on success.
        """
        
        # ----------------------------------------------------------
        #  VALIDATE INPUTS  –  collect errors before writing anything
        # ----------------------------------------------------------
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

        # ----------------------------------------------------------
        #  VERSION FIELD  –  must be a positive integer
        # ----------------------------------------------------------
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

        # ----------------------------------------------------------
        #  SHOW ERRORS  –  abort if any validation failed
        # ----------------------------------------------------------
        if len(errors) != 0:
            error_string = "\n".join(f"- {each}" for each in errors)
            QMessageBox.critical(self, "Validation Errors", f"Please fix the following:\n{error_string}")
            return
        
        # ----------------------------------------------------------
        #  BUILD METADATA DICT
        # ----------------------------------------------------------
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
            "attached_images": self.attached_images
        }

        # ----------------------------------------------------------
        #  CREATE SUBMISSION FOLDER
        # ----------------------------------------------------------
        folder_map = {
            "Gizmo" : GIZMO_FOLDER,
        }
        
        try:
            save_dir = os.path.join(folder_map[filetype], self.submission_id)
            os.makedirs(save_dir, exist_ok=True) 
        except Exception as e:
            QMessageBox.critical(self, "Errors", f"Error > {e}")

        # ----------------------------------------------------------
        #  WRITE JSON + COPY FILES
        # ----------------------------------------------------------
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
                
            save_msg = "The file has been submitted successfully."
            print(save_msg)
            QMessageBox.information(self, "Info", save_msg)
            
            # ----------------------------------------------------------
            #  CLEAR FORM AFTER SUCCESSFUL SUBMISSION
            # ----------------------------------------------------------

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
            self.extra_docs = []
            
            for each in self.IMAGE_BUTTONS:
                each.setIcon(self.image_icon)
                each.setIconSize(QSize(50, 50))
            
        except Exception as e:
            QMessageBox.critical(self, "Errors", f"Error > {e}")

    # ============================================================
    #  LIBRARY – CATEGORY PANEL CLICK
    # ============================================================

    # @Slot() 
    def on_category_panel_clicked(self, index):
        """
        Filter the gizmo grid to show only items whose filetype or
        sub_category matches the clicked tree node label.
        """
        # Always switch back to the Library tab when browsing categories.
        current = self.tabs.currentIndex()
        if current != 0:
            self.tabs.setCurrentIndex(0)
    
        folder_name = os.listdir(GIZMO_FOLDER)
        
        MAX_COLS = 10
        counter = 0
        
        clicked_row = index.data()
        print("clicked_row", clicked_row)
        
        square_size = 85
        
        # ----------------------------------------------------------
        #  CLEAR EXISTING GRID WIDGETS
        # ----------------------------------------------------------
        while self.files_grid_layout.count():
            item = self.files_grid_layout.takeAt(0)
            item.widget().deleteLater()
        
        # ----------------------------------------------------------
        #  POPULATE GRID  –  one button per matching submission
        # ----------------------------------------------------------
        for each in folder_name:
            json_filename = f"{each}.json"
            each_folder_path = os.path.join(GIZMO_FOLDER, each)
            each_json = os.path.join(each_folder_path, json_filename)
            if not os.path.isdir(each_folder_path): 
                continue
            if not os.path.exists(each_json):  
                continue   
            with open(each_json, "r") as file:
                data = json.load(file)
                submission_id = data["uuid"]
                filename = data["filename"]
                filetype = data["filetype"]
                sub_category = data["sub_category"]
            
            if clicked_row == filetype or clicked_row == sub_category:
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

    # ============================================================
    #  LIBRARY – GIZMO DETAIL TAB
    # ============================================================
    
    # # @Slot()
    def on_gizmo_button_clicked(self):
        """
        Read the submission JSON and open a new detail tab showing
        description, metadata, links, preview images, and docs.
        """
        button = self.sender()
        submission_id = button.property("submission_id")
        filetype_folder = os.path.join(GIZMO_FOLDER, submission_id)
        json_path = os.path.join(filetype_folder, f"{submission_id}.json")
            
        with open(json_path, "r") as file:
            data = json.load(file)
            
        # ----------------------------------------------------------
        #  BUILD DETAIL TAB LAYOUT
        # ----------------------------------------------------------
        self.detailed_tab = QWidget()        
        self.detailed_tab_layout = QHBoxLayout(self.detailed_tab)
        
        left_layout = QVBoxLayout()
        right_layout = QVBoxLayout()

        # -------- Left : Header --------
        header_row = QHBoxLayout()
        
        self.det_filename = QLabel(data["filename"])
        filename_font = self.det_filename.font()
        filename_font.setBold(True)
        filename_font.setPointSize(24)
        self.det_filename.setFont(filename_font)
        
        self.det_author = QLabel(f"by {data['author']}")
        header_row.addWidget(self.det_filename)
        header_row.addWidget(self.det_author)
        header_row.addStretch()
        
        self.det_tagline = QLabel(data['tagline'])
        self.det_desc = QTextEdit()
        self.det_desc.setPlainText(data["description"])
        self.det_desc.setReadOnly(True)

        left_layout.addLayout(header_row)
        left_layout.addWidget(self.det_tagline)
        left_layout.addWidget(self.det_desc)

        # -------- Right : Node Info --------
        info_label = QLabel("Node Info")
        info_font = info_label.font()
        info_font.setBold(True)
        info_label.setFont(info_font)
        
        info_form = QFormLayout()
        info_form.addRow("Version:", QLabel(str(data["version"])))
        info_form.addRow("Submitted:", QLabel(str(data["submitted"])))

        right_layout.addWidget(info_label)
        right_layout.addLayout(info_form)

        # -------- Right : Resources --------
        # Show a button for each non-empty link; hide section if none exist.
        res_label = QLabel("Resources")
        res_font = res_label.font()
        res_font.setBold(True)
        res_label.setFont(res_font)
        right_layout.addWidget(res_label)

        has_any_link = False
        for key, label in [
            ("repo_link",   "Repo"),
            ("issues_link", "Issue"),
            ("website",     "Website"),
            ("extra_link",  "Extra"),
        ]:
            link_val = data.get(key, "").strip()
            if link_val:
                has_any_link = True
                btn = QPushButton(label)
                btn.setProperty("object_id", submission_id)
                btn.setProperty("link_key", key)
                btn.clicked.connect(self.open_link)
                right_layout.addWidget(btn)

        if not has_any_link:
            none_lbl = QLabel("No links available")
            none_lbl.setStyleSheet("color: gray;")
            right_layout.addWidget(none_lbl)

        # -------- Right : Subscribe --------
        self.subscribe = QPushButton("Subscribe")
        self.subscribe.setProperty("object_id", submission_id)
        self.subscribe.clicked.connect(self.copy_object_file)
        right_layout.addWidget(self.subscribe)
        
        right_layout.addStretch()
        
        # --------- Preview Images ---------
        # Scan the Images sub-folder and render thumbnail buttons.
        images_label = QLabel("Preview Images")
        right_layout.addWidget(images_label)

        image_folder = os.path.join(filetype_folder, "Images")
        if os.path.isdir(image_folder):
            images = []
            for f in os.listdir(image_folder):
                if f.endswith((".png", ".jpg", ".jpeg")):
                    images.append(f)
            if images:
                images_grid = QHBoxLayout()
                for img_file in images:
                    img_path = os.path.join(image_folder, img_file)
                    btn = QPushButton()
                    pixmap = QPixmap(img_path).scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                    btn.setIcon(QIcon(pixmap))
                    btn.setIconSize(QSize(80, 80))
                    btn.setFixedSize(85, 85)
                    btn.setProperty("img_path", img_path)
                    btn.clicked.connect(self.open_image)
                    images_grid.addWidget(btn)
                right_layout.addLayout(images_grid)
            else:
                right_layout.addWidget(QLabel("None"))
        else:
            right_layout.addWidget(QLabel("None"))

        # --------- Extra Docs ---------
        # Scan the Docs sub-folder and render a button per document.
        docs_label = QLabel("Extra Docs")
        right_layout.addWidget(docs_label)

        docs_folder = os.path.join(filetype_folder, "Docs")
        if os.path.isdir(docs_folder):
            docs = []
            for f in os.listdir(docs_folder):
                if f.endswith(".pdf") or f.endswith(".doc"):
                    docs.append(f)
            if docs:
                for doc_file in docs:
                    doc_path = os.path.join(docs_folder, doc_file)
                    btn = QPushButton(doc_file)
                    btn.setProperty("doc_path", doc_path)
                    btn.clicked.connect(self.open_doc)
                    right_layout.addWidget(btn)
            else:
                right_layout.addWidget(QLabel("None"))
        else:
            right_layout.addWidget(QLabel("None"))

        # -------- Assemble --------
        self.detailed_tab_layout.addLayout(left_layout, 7)  
        self.detailed_tab_layout.addLayout(right_layout, 3)

        index = self.tabs.addTab(self.detailed_tab, data["filename"])
        self.tabs.setCurrentIndex(index)

    # ============================================================
    #  SUBSCRIBE / COPY TO USER FOLDER
    # ============================================================
    
    # # @Slot()   
    def copy_object_file(self):
        """
        Copy the .gizmo file from the studio folder into the user's
        NodeVault_User folder under its human-readable filename.
        """
        subscribe_btn = self.sender()
        object_id = subscribe_btn.property("object_id")
        filetype_folder = os.path.join(GIZMO_FOLDER, object_id)
        print("filetype_folder", filetype_folder)
        for each in os.listdir(filetype_folder):
            if each.endswith(".gizmo"):
                object_file = os.path.join(filetype_folder, each)
                
        object_folder = os.path.join(GIZMO_FOLDER , object_id)
        object_json = os.path.join(object_folder, f"{object_id}.json")
        
        with open(object_json, "r") as file:
            data = json.load(file)
            
        object_filename = data["filename"]
            
        try:
            os.makedirs(NODEVAULT_USER_FOLDER, exist_ok=True)
            dst_named_path = os.path.join(NODEVAULT_USER_FOLDER, f"{object_filename}.gizmo")

            shutil.copy(src=object_file, dst=dst_named_path) 
            
            QMessageBox.information(self, "Info", f"Subscribed to {object_filename}")
        except Exception as e:
            print(f"{e}")

    # ============================================================
    #  TAB / LINK / FILE OPENERS
    # ============================================================
    
    # @Slot()
    def close_tabs(self, index):
        """
        Prevent closing the root Library tab (index 0);
        remove any other tab normally.
        """
        if index == 0:
            QMessageBox.critical(self, "Error", "You cant close ALL Tab")
        else:
            self.tabs.removeTab(index)
            
    # @Slot()
    def open_link(self):
        """
        Read the link value from the submission JSON and open it
        in the system's default browser via QDesktopServices.
        """
        btn = self.sender()
        object_id = btn.property("object_id")
        link_key = btn.property("link_key")
        
        object_json = os.path.join(GIZMO_FOLDER, object_id, f"{object_id}.json")
        with open(object_json, "r") as file:
            data = json.load(file)
        
        link = data.get(link_key, "").strip()
        if link:
            QDesktopServices.openUrl(QUrl(link))
        else:
            print(f"No link available for {link_key}")
            
    # @Slot()
    def open_doc(self):
        """
        Open the stored doc path with the OS default application.
        """
        btn = self.sender()
        doc_path = btn.property("doc_path")
        if doc_path and os.path.exists(doc_path):
            QDesktopServices.openUrl(QUrl.fromLocalFile(doc_path))
            
    # @Slot()
    def open_image(self):
        """
        Open the stored image path with the OS default application.
        """
        btn = self.sender()
        img_path = btn.property("img_path")
        if img_path and os.path.exists(img_path):
            QDesktopServices.openUrl(QUrl.fromLocalFile(img_path))

    # ============================================================
    #  SUBMIT BUTTON SLOT
    # ============================================================
            
    def on_submit_clicked(self):
        """Delegate to save_json which handles validation and file I/O."""
        self.save_json()

# ============================================================
#  ENTRY POINTS
# ============================================================

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