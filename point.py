from Seg2DetAugment import data_augmentation

# 定义类别映射
dics = {
    'chizi': 0,
}

pointOrder=["ruijiao","zhijiao"]

# 运行数据增强
data_augmentation(
    dics=dics,
    output_folder="output",
    path2labels="lbs-1",
    path2imgs="lbs-1",
    path2bkgs="bkgs",
    counts=3,        # 每张图像对象数量
    threshold=0.5,   # 重叠阈值
    num_images=100,   # 生成图像总数
    pointOrder=pointOrder
)