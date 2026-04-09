"""
Node Vault - A PySide6 GUI application for managing and submitting 
Nuke Gizmos, Scripts, and Templates into a categorized library.
"""

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

# --- Global Path Configurations ---
ROOT_FOLDER = r"H:\Gamut\Projects\node_vault"

MEDIA_FOLDER = os.path.join(ROOT_FOLDER, "media")
ICON_FOLDER = os.path.join(MEDIA_FOLDER, "icons")

OUTPUT_FOLDER = os.path.join(ROOT_FOLDER, "output")
GIZMO_FOLDER = os.path.join(OUTPUT_FOLDER, "Gizmos")
TEMPLATE_FOLDER = os.path.join(OUTPUT_FOLDER, "Template")
SCRIPT_FOLDER = os.path.join(OUTPUT_FOLDER, "Scripts")

USERNAME = os.getlogin()

# --- Media Files ---
THUMBNAIL_FILE = os.path.join(MEDIA_FOLDER, "heavily_compressed.png")
IMAGE_ICON_PATH = os.path.join(ICON_FOLDER, "image_icon.png")
VIDEO_ICON_PATH = os.path.join(ICON_FOLDER, "video_icon.png")

FIXED_POLICY = QSizePolicy.Policy.Fixed


class NodeVault_GUI(QWidget):
    """Main application window for Node Vault."""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Node Vault")
        self.resize(1300, 600)
        
        # Initialize necessary output directories
        try:
            os.makedirs(GIZMO_FOLDER, exist_ok=True)
            print(f"Gizmo Folder created > {GIZMO_FOLDER}")
            os.makedirs(TEMPLATE_FOLDER, exist_ok=True)
            print(f"Template Folder created > {TEMPLATE_FOLDER}")
            os.makedirs(SCRIPT_FOLDER, exist_ok=True)
            print(f"Script Folder created > {SCRIPT_FOLDER}")
        except Exception as e:
            print(f"{e}")
            
        # Data storage for submission tracking
        self.main_file = []
        self.attached_images = []
        self.attached_video = []
        self.extra_docs = []
        
        # Build the user interface
        self.initUI()
        
    def initUI(self):
        """Initializes the main layout and primary tabs."""
        # -------------- MAIN LAYOUT --------------
        self.main_layout = QVBoxLayout(self)

        # -------------- PRIMARY TABS (Library / Submit) --------------
        self.primary_tabs = QTabWidget()

        self.library_tab = QWidget()
        self.submit_tab = QWidget()

        self.primary_tabs.addTab(self.library_tab, "Library")
        self.primary_tabs.addTab(self.submit_tab, "Submit")

        # Build sub-interfaces
        self.init_library_ui()
        self.init_submit_ui()

        # -------------- ASSEMBLE MAIN WINDOW --------------
        self.main_layout.addWidget(self.primary_tabs)

    def init_library_ui(self):
        """Constructs the Library tab interface containing categories and files."""
        # -------------- LIBRARY TAB LAYOUT --------------
        self.library_master_layout = QHBoxLayout(self.library_tab)

        # -------------- CATEGORY PANEL (Tree View) --------------
        self.category_panel = QTreeView()
        self.category_panel.setFixedWidth(300)

        # Set up category hierarchy model
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(["Category"])

        self.template_item = QStandardItem("Templates")
        self.gizmos_item = QStandardItem("Gizmos")
        self.deep_item = QStandardItem("Deep")
        self.image_item = QStandardItem("Image")
        self.draw_item = QStandardItem("Draw")
        self.time_item = QStandardItem("Time")
        self.channel_item = QStandardItem("Channel")
        self.filter_item = QStandardItem("Filter")
        self.tricks_item = QStandardItem("Tricks")
        self.misc_item = QStandardItem("Misc")

        # Assemble tree view nodes
        model.appendRow(self.template_item)
        model.appendRow(self.gizmos_item)
        
        self.gizmos_item.appendRow(self.deep_item)
        self.gizmos_item.appendRow(self.image_item)
        self.gizmos_item.appendRow(self.draw_item)
        self.gizmos_item.appendRow(self.time_item)
        self.gizmos_item.appendRow(self.channel_item)
        self.gizmos_item.appendRow(self.filter_item)

        model.appendRow(self.tricks_item)
        model.appendRow(self.misc_item)

        self.category_panel.setModel(model)

        # -------------- ACTIVE FILTER BAR --------------
        self.tabs = QTabWidget()
        self.all_tab = QWidget()
        self.temp_tab = QWidget()

        self.tabs.addTab(self.all_tab, "All")
        self.tabs.addTab(self.temp_tab, "Temp")

        # -------------- GIZMO GRID (inside All filter) --------------
        self.files_grid_layout = QGridLayout()

        MAX_ROWS = 4
        MAX_COLS = 4

        # Populate grid with placeholder thumbnails
        for row in range(MAX_ROWS):
            for col in range(MAX_COLS):
                thumb = QLabel()
                thumb.setPixmap(QPixmap(THUMBNAIL_FILE))
                self.files_grid_layout.addWidget(thumb, row, col)

        self.all_tab.setLayout(self.files_grid_layout)

        # -------------- CONTENT AREA LAYOUT --------------
        self.right_panel_layout = QVBoxLayout()
        self.right_panel_layout.addWidget(self.tabs)

        # -------------- ASSEMBLE LIBRARY TAB --------------
        self.library_master_layout.addWidget(self.category_panel)
        self.library_master_layout.addLayout(self.right_panel_layout)

    def init_submit_ui(self):
        """Constructs the Submit tab interface for uploading new assets."""
        # -------------- MASTER SUBMIT LAYOUT --------------
        self.submit_master_layout = QVBoxLayout(self.submit_tab)
        
        # Header Title
        self.submit_lbl = QLabel("Submit to Dataset")
        title_font = self.submit_lbl.font()
        title_font.setPointSize(14)
        title_font.setBold(True)
        self.submit_lbl.setFont(title_font)
        
        self.submit_master_layout.addWidget(self.submit_lbl)
        self.submit_master_layout.addSpacing(10)

        # Two-column layout for forms
        self.columns_layout = QHBoxLayout()
        self.main_left_box = QVBoxLayout()
        self.main_right_box = QVBoxLayout()

        # -------------- LEFT COLUMN: BASIC INFO --------------
        self.information_box = QGroupBox("Basic Info")
        self.information_box_layout = QHBoxLayout(self.information_box)

        left_form = QFormLayout()
        right_form = QFormLayout()

        self.filename_le = QLineEdit()
        self.author_le = QLineEdit()
        self.version_le = QLineEdit()
        self.tagline_le = QLineEdit()
        
        # Pre-fill and lock author field
        self.author_le.setText(USERNAME)
        self.author_le.setReadOnly(True)
        
        left_form.addRow("File Name:", self.filename_le)
        left_form.addRow("Version:", self.version_le)
        right_form.addRow("Author:", self.author_le)
        right_form.addRow("Tagline:", self.tagline_le)

        self.information_box_layout.addLayout(left_form)
        self.information_box_layout.addLayout(right_form)

        # -------------- LEFT COLUMN: FILE TYPES --------------
        self.filetype_box = QGroupBox("File Types")
        self.filetype_box_layout = QHBoxLayout(self.filetype_box) 
        
        self.filetype_bg = QButtonGroup(self)
        self.filetype_bg.setExclusive(True)
        
        self.gizmo_btn = QPushButton("Gizmo")
        self.script_btn = QPushButton("Script")
        self.template_btn = QPushButton("Template")
        
        # Make the buttons checkable and add to group
        for btn in [self.gizmo_btn, self.script_btn, self.template_btn]:
            btn.setCheckable(True)
            self.filetype_bg.addButton(btn)
            self.filetype_box_layout.addWidget(btn)

        # -------------- LEFT COLUMN: MAIN FILE --------------
        file_group = QGroupBox("Main File")
        file_layout = QVBoxLayout(file_group)
        
        self.file_label = QLabel("No file selected")
        self.file_browse_btn = QPushButton("Browse")
        self.file_browse_btn.clicked.connect(self.on_file_browse_clicked)
        
        file_layout.addWidget(self.file_label)
        file_layout.addWidget(self.file_browse_btn)

        # -------------- LEFT COLUMN: DESCRIPTION --------------
        desc_group = QGroupBox("Description")
        desc_layout = QVBoxLayout(desc_group)
        self.desc_edit = QTextEdit()
        self.desc_edit.setPlaceholderText("Enter description…")
        desc_layout.addWidget(self.desc_edit)

        # -------------- LEFT COLUMN: SUB-CATEGORY OPTIONS --------------
        self.sub_category_box = QGroupBox("Sub Category")
        self.sub_category_layout = QHBoxLayout(self.sub_category_box)

        self.subcategory_bg = QButtonGroup(self)
        self.btn_deep = QPushButton("Deep")
        self.btn_draw = QPushButton("Draw")
        self.btn_time = QPushButton("Time")
        self.btn_image = QPushButton("Image")
        self.btn_channel = QPushButton("Channel")
        self.btn_filter = QPushButton("Filter")
        
        for btn in [self.btn_deep, self.btn_draw, self.btn_time, self.btn_image, self.btn_channel, self.btn_filter]:
            btn.setCheckable(True)
            self.subcategory_bg.addButton(btn)
            self.sub_category_layout.addWidget(btn)
            
        # -------------- LEFT COLUMN: RENDER + NUKE VERSION --------------
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

        # -------------- RIGHT COLUMN: DOCS --------------
        self.docs_box = QGroupBox("Docs")
        self.docs_box_layout = QVBoxLayout(self.docs_box)

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
        
        self.docs_box_layout.addLayout(extra1_row)
        self.docs_box_layout.addLayout(extra2_row)

        # -------------- RIGHT COLUMN: EXTERNAL LINKS --------------
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

        # -------------- RIGHT COLUMN: PREVIEW IMAGES & DEMO VIDEO --------------
        self.media_box = QGroupBox("Preview Images & Demo Video")
        self.media_box_layout = QHBoxLayout(self.media_box)
        self.image_icon = QIcon(IMAGE_ICON_PATH)
        self.video_icon = QIcon(VIDEO_ICON_PATH)

        self.preview_btn_1 = QPushButton()
        self.preview_btn_2 = QPushButton()
        self.preview_btn_3 = QPushButton()
        self.preview_btn_4 = QPushButton()
        self.preview_btn_5 = QPushButton()
        self.demo_video_btn = QPushButton()
        
        add_image_buttons = [
            self.preview_btn_1, self.preview_btn_2, 
            self.preview_btn_3, self.preview_btn_4, self.preview_btn_5
        ]
        
        # Configure image buttons
        for each_image_btn in add_image_buttons:
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
        
        # Connect media buttons
        self.preview_btn_1.clicked.connect(self.on_preview_btn_1_clicked)
        self.preview_btn_2.clicked.connect(self.on_preview_btn_2_clicked)
        self.preview_btn_3.clicked.connect(self.on_preview_btn_3_clicked)
        self.preview_btn_4.clicked.connect(self.on_preview_btn_4_clicked)
        self.preview_btn_5.clicked.connect(self.on_preview_btn_5_clicked)
        self.demo_video_btn.clicked.connect(self.on_demo_video_btn_clicked)

        for each in add_image_buttons:
            self.media_box_layout.addWidget(each)
        self.media_box_layout.addWidget(self.demo_video_btn)

        # -------------- ASSEMBLE SUBMIT LAYOUT --------------
        # Add components to left box
        self.main_left_box.addWidget(self.information_box)
        self.main_left_box.addWidget(self.filetype_box)

        file_desc_layout = QHBoxLayout()
        file_desc_layout.addWidget(file_group)
        file_desc_layout.addWidget(desc_group)
        self.main_left_box.addLayout(file_desc_layout)
        
        self.main_left_box.addWidget(self.sub_category_box)
        self.main_left_box.addLayout(self.render_nuke_layout)
        
        # Add components to right box
        self.main_right_box.addWidget(self.docs_box)
        self.main_right_box.addWidget(self.external_box)
        self.main_right_box.addWidget(self.media_box)
        
        # Final Submit Button configuration
        self.btn_submit = QPushButton("SUBMIT")
        self.btn_submit.setMinimumHeight(40) 
        self.btn_submit.setMinimumWidth(400)
        
        btn_font = self.btn_submit.font()
        btn_font.setBold(True)
        self.btn_submit.setFont(btn_font)
        self.btn_submit.clicked.connect(self.on_submit_clicked)

        # Add columns to master layout
        self.columns_layout.addLayout(self.main_left_box)
        self.columns_layout.addLayout(self.main_right_box)
        
        self.submit_master_layout.addLayout(self.columns_layout)
        self.submit_master_layout.addWidget(self.btn_submit, alignment=Qt.AlignCenter)
        self.submit_master_layout.addStretch()


    # ***************** FUNCTIONS *******************

    def on_img_btn_clicked(self, button):
        """Handles image selection and applies it to the corresponding button."""
        path, _ = QFileDialog.getOpenFileName(
            self, "Select Preview Image", "",
            "Images (*.png *.jpg *.jpeg);;All files (*)"
        )
        if path:
            filename = os.path.basename(path)
            print(path)
            thumbnail = QIcon(path)
            button.setIcon(thumbnail)
            button.setIconSize(QSize(100, 100))
            self.attached_images.append(path)

    def on_video_btn_clicked(self, button):
        """Handles video selection and updates the button label."""
        path, _ = QFileDialog.getOpenFileName(
            self, "Select Demo Video", "",
            "Video (*.mp4 *.mov *.avi);;All files (*)"
        )
        if path:
            filename = os.path.basename(path)
            button.setText(filename)
            self.attached_video.append(path)

    def on_doc_btn_clicked(self, button):
        """Handles document selection and updates the label."""
        path, _ = QFileDialog.getOpenFileName(
            self, "Select Extra Document", "",
            "PDF (*.pdf);;All files (*)"
        )
        if path:
            filename = os.path.basename(path)
            button.setText(filename)
            self.extra_docs.append(path)
            
    # *********** UPDATE GUI > LABEL / STATUS  ******************
    
    # ------- Label Update: IMAGE & VIDEO BOX -----------
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

    # ------- Label Update: Main File -----------
    @Slot()
    def on_file_browse_clicked(self):
        """Browses for the primary Nuke/Python file."""
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            "Select Main File", 
            "", 
            "All Files (*);;Python Files (*.py);;Nuke Files (*.nk)"
        )
        if file_path:
            self.main_file = file_path
            self.file_label.setText(os.path.basename(file_path))      
            
    # ------- Label Update: Extra Docs -----------
    @Slot()
    def on_extra1_browse_clicked(self):
        self.on_doc_btn_clicked(self.extra1_lbl)
        
    @Slot()
    def on_extra2_browse_clicked(self):
        self.on_doc_btn_clicked(self.extra2_lbl)
        
    @Slot() 
    def save_json(self):
        """Validates inputs, packages data, and saves JSON along with media files."""
        # -------- ERROR LIST & VALIDATION ------------
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
            
        # --- Display Error Message ---
        if len(errors) != 0:
            error_string = "\n".join(f"- {each}" for each in errors)
            QMessageBox.critical(self, "Validation Errors", f"Please fix the following:\n{error_string}")
            return
        
        # -------- DATA PACKAGING ------------
        submission_id = str(uuid.uuid4())
        
        filetype = self.filetype_bg.checkedButton().text()
        folder_map = {
            "Gizmo": GIZMO_FOLDER,
            "Script": SCRIPT_FOLDER,
            "Template": TEMPLATE_FOLDER
        }
        
        save_dir = os.path.join(folder_map[filetype], submission_id)
        submitted_time = datetime.datetime.now().isoformat(timespec='seconds')

        filename = self.filename_le.text().strip()
        author = self.author_le.text()
        version = self.version_le.text().strip() or "v001"
        sub_category = self.subcategory_bg.checkedButton().text()
        render_type = self.render_bg.checkedButton().text()
        nuke_version = self.nuke_bg.checkedButton().text()
        description = self.desc_edit.toPlainText().strip()
        tagline = self.tagline_le.text().strip() 
        
        repo_link = self.repo_link.text()
        issues_link = self.issues_link.text()
        website_link = self.website_link.text()
        extra_link = self.extra_link.text()
        
        # Construct JSON dictionary
        data = {
            "uuid": submission_id,
            "submitted": submitted_time,
            "filetype": filetype,
            "filename": filename,
            "author": author,
            "version": version,
            "sub_category": sub_category,
            "render": render_type,
            "nuke_version": nuke_version,
            "description": description,
            "tagline": tagline,
            "extra_docs": self.extra_docs,
            "repo_link": repo_link,
            "issues_link": issues_link,
            "website": website_link,
            "extra_link": extra_link,
            "attached_images": self.attached_images,
            "attached_video": self.attached_video
        }
        
        # -------- FILE SAVING & COPYING ------------
        os.makedirs(save_dir, exist_ok=True)
        json_filename = os.path.join(save_dir, f"{submission_id}.json")
        
        try:
            # Write JSON metafile
            with open(json_filename, "w") as file:
                json.dump(data, file, indent=4)
                
            # Copy Main File
            file_extension = os.path.splitext(self.main_file)[1]
            new_filename = f"{submission_id}{file_extension}" 
            dst_path = os.path.join(save_dir, new_filename)
            shutil.copy(src=self.main_file, dst=dst_path)
            
            # Copy Extra Docs
            for docs_file in data["extra_docs"]:
                docs_folder = os.path.join(save_dir, "Docs")
                os.makedirs(docs_folder, exist_ok=True)
                shutil.copy(src=docs_file, dst=docs_folder)
            
            # Copy Attached Images
            for image_file in data["attached_images"]:
                image_folder = os.path.join(save_dir, "Images")
                os.makedirs(image_folder, exist_ok=True)
                shutil.copy(src=image_file, dst=image_folder)
                
            # Copy Attached Videos
            for video_file in data["attached_video"]:
                video_folder = os.path.join(save_dir, "Videos")
                os.makedirs(video_folder, exist_ok=True)
                shutil.copy(src=video_file, dst=video_folder)
                
            QMessageBox.information(self, "Info", "The file has been submitted successfully.")
            
        except Exception as e:
            print(f"Error > {e}")
        
    def on_submit_clicked(self):
        """Triggers the JSON save and validation process."""
        self.save_json()

# --- Application Entry Point ---
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NodeVault_GUI()
    window.show()
    sys.exit(app.exec())