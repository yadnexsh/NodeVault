    def init_detailed_ui(self):
        
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

        self.detailed_tab_layout.addLayout(left_layout, 7)      # 7 and 3 are like strech values whichare working here as percent
        self.detailed_tab_layout.addLayout(right_layout, 3)
        self.subscribe.clicked.connect(self.copy_object_file)
        
    def copy_object_file(self):
        subscribe_btn = self.sender()
        