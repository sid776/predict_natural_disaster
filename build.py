import os
import shutil
from pathlib import Path

def build_static_files():
    # Create docs directory if it doesn't exist
    docs_dir = Path('docs')
    docs_dir.mkdir(exist_ok=True)
    
    # Copy necessary files to docs directory
    files_to_copy = [
        'app.py',
        'quantum_model.py',
        'requirements.txt',
        'README.md',
        'index.html'
    ]
    
    for file in files_to_copy:
        if os.path.exists(file):
            shutil.copy2(file, docs_dir / file)
    
    # Copy templates directory
    if os.path.exists('templates'):
        shutil.copytree('templates', docs_dir / 'templates', dirs_exist_ok=True)
    
    print("Build completed successfully!")

if __name__ == '__main__':
    build_static_files() 