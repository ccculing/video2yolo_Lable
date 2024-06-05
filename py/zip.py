import os
import shutil
import zipfile
import random
from tqdm import tqdm

def clear_and_create_dir(directory):
    if os.path.exists(directory):
        shutil.rmtree(directory)
    os.makedirs(directory)

def copy_images_with_progress(src_dir, dst_dirs):
    images = [f for f in os.listdir(src_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))]
    for filename in tqdm(images, desc="Copying images"):
        src_file = os.path.join(src_dir, filename)
        for dst_dir in dst_dirs:
            dst_file = os.path.join(dst_dir, filename)
            shutil.copy(src_file, dst_file)

def copy_files_with_progress(src_dir, dst_dirs):
    files = os.listdir(src_dir)
    for filename in tqdm(files, desc="Copying labels"):
        src_file = os.path.join(src_dir, filename)
        for dst_dir in dst_dirs:
            dst_file = os.path.join(dst_dir, filename)
            shutil.copy(src_file, dst_file)

def zip_directory_with_progress(folder_path, zip_filename):
    file_paths = []
    # 获取所有文件路径
    for root, _, files in os.walk(folder_path):
        for file in files:
            file_paths.append(os.path.join(root, file))
    
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path in tqdm(file_paths, desc="Zipping files"):
            arcname = os.path.relpath(file_path, folder_path)
            zipf.write(file_path, arcname)

def main():
    # 获取当前脚本文件夹的上一级目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    
    # 设置源目录和目标目录
    src_images_dir = os.path.join(parent_dir, 'X-AnyLabeling', 'images')
    src_labels_dir = os.path.join(parent_dir, 'X-AnyLabeling', 'labels')
    
    dst_images_train_dir = os.path.join(parent_dir, 'human', 'images', 'train')
    dst_images_val_dir = os.path.join(parent_dir, 'human', 'images', 'val')
    dst_labels_train_dir = os.path.join(parent_dir, 'human', 'labels', 'train')
    dst_labels_val_dir = os.path.join(parent_dir, 'human', 'labels', 'val')

    # 清空并创建目标文件夹
    clear_and_create_dir(dst_images_train_dir)
    clear_and_create_dir(dst_images_val_dir)
    clear_and_create_dir(dst_labels_train_dir)
    clear_and_create_dir(dst_labels_val_dir)
    
    # 复制图片文件到 train 和 val 文件夹
    copy_images_with_progress(src_images_dir, [dst_images_train_dir, dst_images_val_dir])

    # 复制标签文件到 train 和 val 文件夹
    copy_files_with_progress(src_labels_dir, [dst_labels_train_dir, dst_labels_val_dir])
    
    # 打包 human 文件夹为 ZIP 文件
    human_dir = os.path.join(parent_dir, 'human')
    zip_filename = os.path.join(parent_dir, 'human.zip')
    zip_directory_with_progress(human_dir, zip_filename)
    
    print(f"All files copied and {human_dir} directory zipped to {zip_filename}.")

if __name__ == "__main__":
    main()