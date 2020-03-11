import os
import sys

# This path setup is very important when you have src and test under main directory
current_dir = os.path.dirname(__file__)
sys.path.insert(0, current_dir)
sys.path.insert(0, current_dir + '/../src')
