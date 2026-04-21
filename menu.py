import os
import nuke

NODEVAULT_ICON = os.path.join(os.path.dirname(NV_Tool.__file__), "media", "icons", "ICON_NodeVault.png")
NODEVAULT_USER_FOLDER = os.path.expanduser("~/.nuke/NodeVault_User")
toolbar = nuke.toolbar("Nodes").addMenu("Node Vault", icon = NODEVAULT_ICON)


# --- Subscribed gizmos ---
if not os.listdir(NODEVAULT_USER_FOLDER):
    toolbar.addCommand("No Gizmos Subscribed", "pass")
else:
    for filename in os.listdir(NODEVAULT_USER_FOLDER):
        if filename.endswith(".gizmo"):
            node_name = filename.replace(".gizmo", "")
            toolbar.addCommand(node_name, f"nuke.createNode('{node_name}')")