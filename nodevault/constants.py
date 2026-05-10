from PySide2 import __all__
import os
from PySide2.QtWidgets import QSizePolicy

#  PATH CONSTANTS
# --------------------
# All folder paths resolved once at import time.

CURRENT_FILEDIR = os.path.dirname(__file__)
ROOT_FOLDER = os.path.dirname(CURRENT_FILEDIR)

NUKE_FOLDER = os.path.join((os.path.expanduser("~")), ".nuke")
NODEVAULT_USER_FOLDER = os.path.join(NUKE_FOLDER, "NodeVault_User")

MEDIA_FOLDER = os.path.join(CURRENT_FILEDIR, "media")
ICON_FOLDER = os.path.join(MEDIA_FOLDER, "icons")

NODEVAULT_STUDIO_FOLDER =  os.path.join(ROOT_FOLDER, "NodeVault_Studio")
GIZMO_FOLDER = os.path.join(NODEVAULT_STUDIO_FOLDER,"Gizmos")


#  MISC CONSTANTS
# --------------------

USERNAME = os.getlogin()
ICON_IMAGE_PATH = os.path.join(ICON_FOLDER, "ICON_image.png")
FIXED_POLICY = QSizePolicy.Policy.Fixed
FILETYPE_FOLDERS = ["Gizmos"]


__all__ = [
    "CURRENT_FILEDIR",
    "ROOT_FOLDER",
    "NUKE_FOLDER",
    "NODEVAULT_USER_FOLDER",
    "MEDIA_FOLDER",
    "ICON_FOLDER",
    "NODEVAULT_STUDIO_FOLDER",
    "GIZMO_FOLDER",
    "USERNAME",
    "ICON_IMAGE_PATH",
    "FIXED_POLICY",
    "FILETYPE_FOLDERS",
]   