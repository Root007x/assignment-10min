import os
from pathlib import Path


directories = [
    "src/__init__.py",
    "src/components/__init__.py",
    "src/utils/__init__.py",
    "src/config/__init__.py",
    "research/research.ipynb",
    "setup.py",
    "app.py" 
]

for directory in directories:
    file_path = Path(directory)
    file_dir, file_name = os.path.split(file_path)
     
    if file_dir != "":
        os.makedirs(file_dir)
    
    if (not os.path.exists(file_path)) or (os.path.getsize(file_path) == 0):
        with open(file_path, "w") as f:
            pass
    
    