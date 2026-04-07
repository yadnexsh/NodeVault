    
import os
    def save_json(self):
        
        submission_id = str(uuid.uuid4())
        
        filename = self.filename_le.text()
        if not filename:
            print("Submission failed: Filename is required!")
            return
        filetype = "Unknown"
        if self.filetype_bg.checkedButton():
            filetype = self.filetype_bg.checkedButton().text()
            if filetype == "Gizmo":
                save_dir = os.path.join(GIZMO_FOLDER, submission_id)
            if filetype == "Script":
                save_dir = os.path.join(SCRIPT_FOLDER, submission_id)
            if filetype == "Template":
                save_dir = os.path.join(TEMPLATE_FOLDER, submission_id)
        else:
            QMessageBox.information(self, "Info", "Select the filetype")
        os.makedirs(save_dir, exist_ok=True)
        json_filepath = os.path.join(save_dir, f"{submission_id}.json")
        os.makedirs(save_dir, exist_ok=True)
        version = self.version_le.text() or "v001"
        
        sub_category = "Unknown"
        if self.subcategory_bg.checkedButton():
            sub_category = self.subcategory_bg.checkedButton().text()
        else:
            QMessageBox.information(self, "Info", "Select the Sub Category")    
            
        render_type = "Unknown"
        if self.render_bg.checkedButton():
            render_type = self.render_bg.checkedButton().text()
        else:
            QMessageBox.information(self, "Info", "Select the Render Type")

        nuke_version = "Unknown"
        if self.nuke_bg.checkedButton():
            nuke_version = self.nuke_bg.checkedButton().text()
        else:
            QMessageBox.information(self, "Info", "Select the Nuke Version")
            
        readme_text = self.readme_lbl.text()
        if readme_text == "No file":
            readme = "None"
        else:
            readme = readme_text
            
            
    # @Slot()
    # def on_submit_clicked(self ):
        
    #     submission_id = str(uuid.uuid4())
    #     # save_dir = os.path.join(ROOT_FOLDER, submission_id)
        
    #     filename = self.filename_le.text()
    #     if not filename:
    #         print("Submission failed: Filename is required!")
    #         return
        
    #     version = self.version_le.text() or "v001"
        
        filetype = "Unknown"
        if self.filetype_bg.checkedButton():
            filetype = self.filetype_bg.checkedButton().text()
            if filetype == "Gizmo":
                save_dir = os.path.join(GIZMO_FOLDER, submission_id)
            if filetype == "Script":
                save_dir = os.path.join(SCRIPT_FOLDER, submission_id)
            if filetype == "Template":
                save_dir = os.path.join(TEMPLATE_FOLDER, submission_id)
        else:
            QMessageBox.information(self, "Info", "Select the filetype")
                
    #     os.makedirs(save_dir, exist_ok=True)
    #     filepath = os.path.join(save_dir, f"{submission_id}.json")
    #     os.makedirs(save_dir, exist_ok=True)
                
        sub_category = "Unknown"
        if self.subcategory_bg.checkedButton():
            sub_category = self.subcategory_bg.checkedButton().text()
        else:
            QMessageBox.information(self, "Info", "Select the Sub Category")    
            
        render_type = "Unknown"
        if self.render_bg.checkedButton():
            render_type = self.render_bg.checkedButton().text()
        else:
            QMessageBox.information(self, "Info", "Select the Render Type")

        nuke_version = "Unknown"
        if self.nuke_bg.checkedButton():
            nuke_version = self.nuke_bg.checkedButton().text()
        else:
            QMessageBox.information(self, "Info", "Select the Nuke Version")
            
    #     readme_text = self.readme_lbl.text()
    #     if readme_text == "No file":
    #         readme = "None"
    #     else:
    #         readme = readme_text
            
    #     extra_docs = []
    #     doc1_text = self.extra1_lbl.text()
    #     if doc1_text != "No file":
    #         extra_docs.append(doc1_text)
            
    #     doc2_text = self.extra2_lbl.text()
    #     if doc2_text != "No file":
    #         extra_docs.append(doc2_text)
        
    #     # attached_images = []
    #     DEFAULT_LABELS = ["Img 1", "Img 2", "Img 3", "Img 4", "Img 5"]
    #     for btn in [self.preview_btn_1, self.preview_btn_2, self.preview_btn_3, self.preview_btn_4, self.preview_btn_5]:
    #         text = btn.text()
    #         # if text not in DEFAULT_LABELS:
    #         #     attached_images.append(text)
                
    #     attached_video = ""
    #     if "Demo Video" not in self.demo_video_btn.text():
    #         attached_video = self.demo_video_btn.text()


    #     data = {
    #         "uuid": submission_id,
    #         "submiited": datetime.datetime.now().isoformat(timespec='seconds'),
    #         "filetype": filetype,
    #         "filename": filename,
    #         "author": self.author_le.text(),
    #         "version": version,
    #         "sub_category": sub_category,
    #         "tags": [], 
    #         "render": render_type,
    #         "nuke_version": nuke_version,
    #         "description": self.desc_edit.toPlainText(),
    #         "tagline": self.tagline_le.text(),
    #         "readme": readme,
    #         "extra_docs": extra_docs,
    #         "repo_link": self.link_1.text(),
    #         "issues_link": self.link_2.text(),
    #         "website": self.link_3.text(),
    #         "extra_link": self.link_4.text(),
    #         "attached_images": attached_images,
    #         "attached_video": attached_video
    #     }

        try:
            with open(filepath, "w") as file:
                json.dump(data, file, indent=4)
                QMessageBox.information(self, "Info", "The file has been submitted successfully.")
            print(f"Data successfully saved at > {filepath}")
        except Exception as e:
            print(f"Error > {e}")
