# import nuke
import os
import sys

home_dir = os.path.expanduser("~")
nuke_dir = os.path.join(home_dir, ".nuke")
print(nuke_dir)