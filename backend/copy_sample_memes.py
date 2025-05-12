import os
import random
import shutil

# Source directory
meme_dir = os.path.join('datasets', 'meme', 'memotion_dataset_7k', 'images')
# Target directory
target_dir = os.path.join('..', 'frontend', 'public', 'memes')

# Make sure target directory exists
os.makedirs(target_dir, exist_ok=True)

# Get all image files from source directory
image_files = []
for ext in ['.jpg', '.jpeg', '.png', '.gif']:
    image_files.extend([f for f in os.listdir(meme_dir) if f.lower().endswith(ext)])

# Select random images
if image_files:
    selected_files = random.sample(image_files, min(20, len(image_files)))
    
    # Copy files to target directory
    for i, file_name in enumerate(selected_files):
        source_path = os.path.join(meme_dir, file_name)
        target_path = os.path.join(target_dir, f'meme_{i+1}{os.path.splitext(file_name)[1]}')
        shutil.copy2(source_path, target_path)
        print(f'Copied {file_name} to {target_path}')
    
    print(f'Successfully copied {len(selected_files)} meme images to frontend/public/memes/')
else:
    print('No image files found in source directory') 