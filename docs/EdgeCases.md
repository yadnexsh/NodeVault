Looking at your save_json() and related submit UI code, here are the edge cases I found:
Validation / Logic Bugs

save_dir used before assignment — If no filetype button is checked, save_dir is never defined, but the code continues and will crash with UnboundLocalError when os.makedirs(save_dir) is called. The QMessageBox shows but doesn't return early.

Same problem for sub_category, render_type, nuke_version — You show a message but never return, so all three validations fire in sequence even after the first failure, and execution still reaches os.makedirs.

filename can be empty — If the user leaves "File Name" blank, filename is "" and you still write the JSON silently with a blank filename.

Main file is never saved to JSON — You browse a file and update self.file_label, but the actual file path is never stored in self.main_file or included in data. The submission has no reference to the actual .gizmo/.py/.nk file.

self.extra_docs uses filename as key — If the user picks two different files with the same filename (from different folders), the second silently overwrites the first.

State / Reset Issues

attached_images, attached_video, extra_docs are never cleared between submissions — If the user submits twice in one session, stale attachments from the first run bleed into the second JSON.

UI fields are never reset after a successful submit — The form stays populated, making it easy to accidentally re-submit the same data.

Button labels after file pick are never reset — preview_btn_1 etc. show the filename after picking, but if the user re-opens and picks a different file, the old entry in self.attached_images stays (duplicate key issue above).

File System / IO

No check that the picked main file actually exists at write time — The path could be stale if the file was moved between Browse and Submit.

GIZMO_FOLDER, SCRIPT_FOLDER, TEMPLATE_FOLDER are hardcoded — If those directories don't exist and makedirs fails partway, you get an unhandled exception (though this one is minor given your environment).

Typo in JSON key — "submiited" (double i) — small but will cause issues if anything parses that key by name.