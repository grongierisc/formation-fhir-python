import sys
import os

# EAI python source directories
_TEST_DIR = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(_TEST_DIR, ".."))
sys.path.insert(0, os.path.join(_TEST_DIR, "../../python"))
sys.path.insert(0, os.path.join(_TEST_DIR, "../../python/EAI"))
