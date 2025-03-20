import cv2
import numpy as np
import os

def visualize_yolo_keypoints(image_path, label_path, num_keypoints):
    # 读取图像
    image = cv2.imread(image_path)
    height, width, _ = image.shape

    # 读取标签文件
    with open(label_path, 'r') as f:
        lines = f.readlines()

    for line in lines:
        data = line.strip().split()
        class_id = int(data[0])
        # 解析边界框信息
        x_center = float(data[1]) * width
        y_center = float(data[2]) * height
        box_width = float(data[3]) * width
        box_height = float(data[4]) * height
        x1 = int(x_center - box_width / 2)
        y1 = int(y_center - box_height / 2)
        x2 = int(x_center + box_width / 2)
        y2 = int(y_center + box_height / 2)

        # 绘制边界框
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)

        # 解析关键点信息
        keypoints_data = data[5:]
        for i in range(num_keypoints):
            keypoint_x = float(keypoints_data[3 * i]) * width
            keypoint_y = float(keypoints_data[3 * i + 1]) * height
            visibility = int(keypoints_data[3 * i + 2])
            cv2.circle(image, (int(keypoint_x), int(keypoint_y)), 5, (0, 255, 0), -1)

    return image

# 示例使用
image_folder = 'output/img'
label_folder = 'output/label'
num_keypoints = 3  # 关键点数量，根据实际情况修改

image_files = os.listdir(image_folder)
for image_file in image_files:
    image_path = os.path.join(image_folder, image_file)
    label_file = os.path.splitext(image_file)[0] + '.txt'
    label_path = os.path.join(label_folder, label_file)

    if os.path.exists(label_path):
        visualized_image = visualize_yolo_keypoints(image_path, label_path, num_keypoints)
        cv2.imshow('YOLO Keypoints Visualization', visualized_image)
        cv2.waitKey(0)

cv2.destroyAllWindows()
    