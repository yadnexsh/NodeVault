import nuke


from src.main import launch

menubar = nuke.menu("Nuke")
menu = menubar.addMenu("NodeVault")
# menu.addCommand("Test", nuke_test.create_simple_window)
menu.addCommand("NODE VALUT",launch)