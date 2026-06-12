import os, sys, pathlib
# Ensure the repository root is in sys.path for test imports
repo_root = pathlib.Path(__file__).resolve().parent.parent
if str(repo_root) not in sys.path:
    sys.path.append(str(repo_root))