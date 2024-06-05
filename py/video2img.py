import cv2
import os
import tkinter as tk
from tkinter import filedialog
import shutil
from tqdm import tqdm

def clear_folder(folder_path):
    """ 清空指定文件夹 """
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
    os.makedirs(folder_path)

def save_frame(frame, output_folder, frame_num, video_name):
    # 创建文件名，包括视频名称和帧编号
    filename = os.path.join(output_folder, f"{video_name}_frame_{frame_num:04d}.jpg")
    # 保存图片
    cv2.imwrite(filename, frame)

def frame_difference(frame1, frame2, threshold=30):
    # 将帧转换为灰度图
    gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
    # 计算绝对差异
    diff = cv2.absdiff(gray1, gray2)
    # 计算差异的均值
    mean_diff = diff.mean()
    return mean_diff > threshold

def extract_significant_frames(video_path, output_folder_labeling, diff_threshold=30):
    # 创建输出文件夹
    if not os.path.exists(output_folder_labeling):
        os.makedirs(output_folder_labeling)
    
    # 打开视频文件
    cap = cv2.VideoCapture(video_path)
    
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))  # 获取视频总帧数
    frame_num = 0
    
    # 读取第一帧
    ret, prev_frame = cap.read()
    
    if not ret:
        print(f"Failed to read the video: {video_path}")
        return
    
    video_name = os.path.basename(video_path).split('.')[0]
    save_frame(prev_frame, output_folder_labeling, frame_num, video_name)
    frame_num += 1
    
    # 使用 tqdm 显示进度条
    with tqdm(total=total_frames, desc=f"Processing {video_name}") as pbar:
        while True:
            # 读取下一帧
            ret, current_frame = cap.read()
            
            if not ret:
                break
            
            # 如果当前帧与前一帧的差异超过阈值，则保存当前帧
            if frame_difference(prev_frame, current_frame, diff_threshold):
                save_frame(current_frame, output_folder_labeling, frame_num, video_name)
                prev_frame = current_frame
                frame_num += 1
            
            pbar.update(1)  # 更新进度条
    
    cap.release()
    print(f"Extracted {frame_num} significant frames from {video_path}.")

def main():
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口

    # 打开文件选择对话框
    video_paths = filedialog.askopenfilenames(title="选择视频文件", filetypes=[("MP4 files", "*.mp4"), ("All files", "*.*")])
    
    if not video_paths:
        print("未选择任何文件")
        return
    
    # 默认的输出文件夹
    current_dir = os.getcwd()
    output_folder_labeling_images = os.path.join(current_dir, "X-AnyLabeling", "images")
    output_folder_labeling_labels = os.path.join(current_dir, "X-AnyLabeling", "labels")
    
    # 清空上级目录下的 X-AnyLabeling\images 和 X-AnyLabeling\labels 文件夹
    clear_folder(output_folder_labeling_images)
    clear_folder(output_folder_labeling_labels)
    
    diff_threshold = 8  # 差异阈值，根据需要调整
    
    for video_path in video_paths:
        print(f"Processing video: {video_path}")
        extract_significant_frames(video_path, output_folder_labeling_images, diff_threshold)
    
    print("All videos processed.")

if __name__ == "__main__":
    main()