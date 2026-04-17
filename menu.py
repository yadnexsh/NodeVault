


from src.main import launch


menubar = nuke.menu("Nuke")
menu = menubar.addMenu("NodeVault")
menu.addCommand("NodeVault", launch)


