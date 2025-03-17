# Seg2DecAugment

 [![PyPI](https://img.shields.io/pypi/v/Seg2DecAugment.svg)](https://pypi.org/project/Seg2DecAugment/) [![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT) [![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/Huuuuugh/Seg2DecAugment/ci.yml?branch=main)](https://github.com/Huuuuugh/Seg2DecAugment/actions)

## 中文介绍

### 概述

Seg2DecAugment 是一个 Python 包，用于将语义分割数据转换为目标检测数据，并提供高级数据增强功能。该工具通过旋转、背景替换等操作，生成具有旋转不变性和复杂背景适应性的检测数据集，有效提升模型在复杂场景下的鲁棒性。

### 核心优势

1. **旋转不变性增强**：通过轮廓追踪技术保持旋转后边界框的精准性
2. **复杂背景适配**：支持动态背景替换和多物体叠加
3. **标注效率提升**：只需少量语义分割标注即可生成大规模检测数据集

### 典型应用场景

- 工业质检中的多角度物体检测
- 垃圾分类场景的复杂背景适应
- 遥感图像的多姿态目标识别

### 安装方法

```bash
pip install Seg2DecAugment
```

## 数据集制作

安装anylabeling

```
COPYconda create -n anylabeling python=3.8 anaconda
conda activate anylabeling
```

CPU：

```
COPYpip install anylabeling
```

GPU:

```
COPYpip install anylabeling-gpu
```

安装完毕后使用指令运行

```
COPYanylabeling
```

在你下次需要执行的时候，你只需要这样做

```
COPYconda activate anylabeling
anylabeling
```

准备好你要标注的图片文件夹，点击这里选择你的图片文件夹

![image-20250315135502879](https://huugh.cn/images/%E4%BD%BF%E7%94%A8%E8%AF%AD%E4%B9%89%E5%88%86%E5%89%B2%E7%9A%84%E5%8A%9E%E6%B3%95%E5%A2%9E%E5%BC%BA%E7%9B%AE%E6%A0%87%E6%A3%80%E6%B5%8B%E7%9A%84%E6%95%B0%E6%8D%AE%E9%9B%86/image-20250315135502879.png)

然后点击这个大脑，开启SAM标注

![image-20250315135548616](https://huugh.cn/images/%E4%BD%BF%E7%94%A8%E8%AF%AD%E4%B9%89%E5%88%86%E5%89%B2%E7%9A%84%E5%8A%9E%E6%B3%95%E5%A2%9E%E5%BC%BA%E7%9B%AE%E6%A0%87%E6%A3%80%E6%B5%8B%E7%9A%84%E6%95%B0%E6%8D%AE%E9%9B%86/image-20250315135548616.png)

选择一个你想要的模型，模型是自动从网上下载的，如果失败请使用特殊方法下载（本文不介绍）

![image-20250315135613385](https://huugh.cn/images/%E4%BD%BF%E7%94%A8%E8%AF%AD%E4%B9%89%E5%88%86%E5%89%B2%E7%9A%84%E5%8A%9E%E6%B3%95%E5%A2%9E%E5%BC%BA%E7%9B%AE%E6%A0%87%E6%A3%80%E6%B5%8B%E7%9A%84%E6%95%B0%E6%8D%AE%E9%9B%86/image-20250315135613385.png)

然后点+Point按钮，点击物体即可

![image-20250315135828523](https://huugh.cn/images/%E4%BD%BF%E7%94%A8%E8%AF%AD%E4%B9%89%E5%88%86%E5%89%B2%E7%9A%84%E5%8A%9E%E6%B3%95%E5%A2%9E%E5%BC%BA%E7%9B%AE%E6%A0%87%E6%A3%80%E6%B5%8B%E7%9A%84%E6%95%B0%E6%8D%AE%E9%9B%86/image-20250315135828523.png)

没问题就点击finish，如果有问题，可以用-Point在误标记的地方点击，它会自动重新计算。![image-20250315135848748](https://huugh.cn/images/%E4%BD%BF%E7%94%A8%E8%AF%AD%E4%B9%89%E5%88%86%E5%89%B2%E7%9A%84%E5%8A%9E%E6%B3%95%E5%A2%9E%E5%BC%BA%E7%9B%AE%E6%A0%87%E6%A3%80%E6%B5%8B%E7%9A%84%E6%95%B0%E6%8D%AE%E9%9B%86/image-20250315135848748.png)

写入你希望的名称，同一个物体的名称必须相同

![image-20250315135959313](https://huugh.cn/images/%E4%BD%BF%E7%94%A8%E8%AF%AD%E4%B9%89%E5%88%86%E5%89%B2%E7%9A%84%E5%8A%9E%E6%B3%95%E5%A2%9E%E5%BC%BA%E7%9B%AE%E6%A0%87%E6%A3%80%E6%B5%8B%E7%9A%84%E6%95%B0%E6%8D%AE%E9%9B%86/image-20250315135959313.png)

完成所有标记后，请你所有标签和图片将会存放在同一个文件夹内，像我这样子

![image-20250315140118317](https://huugh.cn/images/%E4%BD%BF%E7%94%A8%E8%AF%AD%E4%B9%89%E5%88%86%E5%89%B2%E7%9A%84%E5%8A%9E%E6%B3%95%E5%A2%9E%E5%BC%BA%E7%9B%AE%E6%A0%87%E6%A3%80%E6%B5%8B%E7%9A%84%E6%95%B0%E6%8D%AE%E9%9B%86/image-20250315140118317.png)

然后，像我这样准备几张空白的背景图，背景图请尽可能制造一些差异。

### 快速开始

```python
from Seg2DecAugment import data_augmentation

# 定义类别映射
dics = {
    'battery': 0,
    'bottle': 1,
    # ... 其他类别
}

# 运行数据增强
data_augmentation(
    dics=dics,
    output_folder="output",
    path2labels="path/to/labels",
    path2imgs="path/to/images",
    path2bkgs="path/to/backgrounds",
    counts=3,        # 每张图像对象数量
    threshold=0.5,   # 重叠阈值
    num_images=100   # 生成图像总数
)
```

### 输出结构

```plaintext
output/
├── label/
│   ├── 0.txt
│   └── ...
└── img/
    ├── 0.jpg
    └── ...
```

### 参数说明

| 参数名          | 描述               | 默认值 |
| --------------- | ------------------ | ------ |
| `dics`          | 类别标签映射       | 必需   |
| `output_folder` | 输出目录路径       | 必需   |
| `path2labels`   | 输入分割标签路径   | 必需   |
| `path2imgs`     | 输入原图路径       | 必需   |
| `path2bkgs`     | 背景图像路径       | 必需   |
| `counts`        | 单图最大物体数     | 3      |
| `threshold`     | 重叠检测阈值 (IOU) | 0.5    |
| `num_images`    | 生成图像总数       | 100    |

### Overview

Seg2DecAugment is a Python package for converting semantic segmentation data into object detection datasets with advanced augmentation capabilities. It generates rotation-invariant and complex-background-adaptive detection datasets through operations like rotation and background replacement, significantly improving model robustness in challenging scenarios.

### Key Advantages

1. **Rotation Invariance**：Maintains precise bounding boxes after rotation using contour tracking
2. **Complex Background Adaptation**：Supports dynamic background replacement and multi-object overlay
3. **Annotation Efficiency**：Generates large-scale detection datasets from minimal segmentation annotations

### Typical Use Cases

- Multi-angle industrial quality inspection
- Complex background adaptation for waste sorting
- Multi-pose object recognition in remote sensing images

### Installation

```bash
pip install Seg2DecAugment
```

### Quick Start

```python
from Seg2DecAugment import data_augmentation

# Define class mappings
dics = {
    'battery': 0,
    'bottle': 1,
    # ... other classes
}

# Run data augmentation
data_augmentation(
    dics=dics,
    output_folder="output",
    path2labels="path/to/labels",
    path2imgs="path/to/images",
    path2bkgs="path/to/backgrounds",
    counts=3,        # Max objects per image
    threshold=0.5,   # Overlap threshold
    num_images=100   # Total images to generate
)
```

### Output Structure

```plaintext
output/
├── label/
│   ├── 0.txt
│   └── ...
└── img/
    ├── 0.jpg
    └── ...
```

### Parameter Explanation



| Parameter       | Description                         | Default  |
| --------------- | ----------------------------------- | -------- |
| `dics`          | Class label mappings                | required |
| `output_folder` | Output directory path               | required |
| `path2labels`   | Path to input segmentation labels   | required |
| `path2imgs`     | Path to input original images       | required |
| `path2bkgs`     | Path to background images           | required |
| `counts`        | Maximum objects per generated image | 3        |
| `threshold`     | Overlap detection threshold (IOU)   | 0.5      |
| `num_images`    | Total number of images to generate  | 100      |



### 许可证/Licence



本项目采用 MIT 许可证 开源。

