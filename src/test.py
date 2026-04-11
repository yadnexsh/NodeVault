import os

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

FILETYPE_FOLDERS = ["Gizmos", "Scripts", "Template"]

# for each in FILETYPE_FOLDERS:
#     if not each in os.listdir(OUTPUT_FOLDER):
#         each_folder = os.path.join(OUTPUT_FOLDER,f"{each}")
#         os.makedirs(each_folder)
#         print(f"Created {each} folder.")
#     else:
#         print(f"{each} folder already exists.")

import json
from pprint import pprint
folder_name = os.listdir(GIZMO_FOLDER)
print(folder_name)

def read_json():
    folder_name = os.listdir(GIZMO_FOLDER)

    for each in folder_name:
        filename = os.path.join(each, f"{each}.json")
        each_folder_path = os.path.join(GIZMO_FOLDER, filename)
        print(each_folder_path)
        
read_json()
        

def read_json():
    folder_name = os.listdir(GIZMO_FOLDER)
    for each in folder_name:
        filename = f"{each}.json"
        each_folder = os.path.join(GIZMO_FOLDER, each)
        each_json = os.path.join(each_folder, filename)
        # print(each_json)
    with open(each_json, "r") as file:
        data = json.load(file)
    return data
data = read_json()
        
def extrac_value(data):
    filetype = data["filetype"]
    FILETYPES = ["Gizmos", "Script", "Template"] 
    # if filetype in FILETYPES:
    #     print(filetype)
    if filetype == "Gizmo":
        print("Gizmo")
    if filetype == "Script":
        print("Script")
    if filetype == "Template":
        print("Template")
    
    
    
extrac_value(data)