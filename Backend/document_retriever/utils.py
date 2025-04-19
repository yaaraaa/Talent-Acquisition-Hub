import os
import shutil

# Clear contents of a folder without removing the folder itself
def clear_directory(dir):   
    if os.path.exists(dir):
        for filename in os.listdir(dir):
            file_path = os.path.join(dir, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)  # Remove files or symbolic links
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)  # Remove directories
            except Exception as e:
                print(f"Failed to delete {file_path}. Reason: {e}")
