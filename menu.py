import os
import nuke
import nodevault.main

# src.main.__file__ correctly returns the path to your src/main.py file
# os.path.dirname gets the 'src' folder. Then we just add media/icons/...
NODEVAULT_ICON = os.path.join(os.path.dirname(src.main.__file__), "media", "icons", "ICON_NodeVault.png")
NODEVAULT_USER_FOLDER = os.path.expanduser("~/.nuke/NodeVault_User")

# --- Nuke Top Menu ---
# This adds the menu to the top bar in Nuke
top_menu = nuke.menu("Nuke").addMenu("Node Vault")
top_menu.addCommand("Launch Node Vault", "src.main.launch()", icon=NODEVAULT_ICON)

# --- Nodes Toolbar (Left Menu) ---
toolbar = nuke.toolbar("Nodes").addMenu("Node Vault", icon=NODEVAULT_ICON)

# --- Subscribed gizmos ---
# It's safer to create the directory if it doesn't exist to prevent os.listdir from crashing
if not os.path.exists(NODEVAULT_USER_FOLDER):
    os.makedirs(NODEVAULT_USER_FOLDER)

if not os.listdir(NODEVAULT_USER_FOLDER):
    toolbar.addCommand("No Gizmos Subscribed", "pass")
else:
    for filename in os.listdir(NODEVAULT_USER_FOLDER):
        if filename.endswith(".gizmo"):
            node_name = filename.replace(".gizmo", "")
            toolbar.addCommand(node_name, f"nuke.createNode('{node_name}')")