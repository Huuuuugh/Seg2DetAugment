import json
import cv2
import numpy as np
import random
import os
import pandas as pd
import shutil


def cut(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 20, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    max_contour = max(contours, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(max_contour)
    cut = image[y:y + h, x:x + w]
    return cut, [x, y, w, h]


def rotate(image, angle):
    center = (image.shape[1] / 2, image.shape[0] / 2)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 20, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    max_contour = max(contours, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(max_contour)
    origin_corner_position = [[0, 0], [0, h], [w, 0], [h, w]]
    rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1)
    for index, point in enumerate(origin_corner_position):
        origin_corner_position[index] = np.matmul(rotation_matrix, np.array([point[0], point[1], 1]).T)
    boundingBox = cv2.boundingRect(np.array(origin_corner_position, dtype=np.int32))
    rotation_matrix[0][2] += (boundingBox[2] - w) / 2
    rotation_matrix[1][2] += (boundingBox[3] - h) / 2
    rotated_image = cv2.warpAffine(image, rotation_matrix, (boundingBox[2], boundingBox[3]))
    gray = cv2.cvtColor(rotated_image, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 20, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    max_contour = max(contours, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(max_contour)
    return rotated_image, (x, y, w, h)


def insert(bkg, img):
    x = random.randint(0, bkg.shape[1] - img.shape[1])
    y = random.randint(0, bkg.shape[0] - img.shape[0])
    w = img.shape[1]
    h = img.shape[0]
    mb = img[:, :, 0]
    mg = img[:, :, 1]
    mr = img[:, :, 2]
    img[np.bitwise_and(np.bitwise_and(mb < 30, mg < 30), mr < 30)] = 0
    bkg[y:y + h, x:x + w][img != 0] = 0
    bkg[y:y + h, x:x + w] += img
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 20, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    max_contour = max(contours, key=cv2.contourArea)
    xx, yy, w, h = cv2.boundingRect(max_contour)
    xx += x
    yy += y
    return bkg, (xx, yy, w, h)


class Item:
    def __init__(self, label, img, pts):
        self.label = label
        pts = np.array(pts, int)
        mask = np.zeros(img.shape)
        mask = cv2.fillPoly(mask, [pts], (255, 255, 255))
        img[mask == 0] = 0
        self.cut = cut(img)[0]

    def get(self):
        image, _ = rotate(self.cut, random.randint(0, 180))
        return image


def delete_folder(path):
    try:
        shutil.rmtree(path)
    except OSError as e:
        pass


def loadLabel(f):
    with open(f, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data


def checkIOU(bboxes, threshold=0.5):
    for i in range(len(bboxes)):
        bbox_i = bboxes[i]
        for j in range(i + 1, len(bboxes)):
            bbox_j = bboxes[j]
            x1_i, y1_i, w_i, h_i = bbox_i
            x2_i, y2_i = x1_i + w_i, y1_i + h_i
            x1_j, y1_j, w_j, h_j = bbox_j
            x2_j, y2_j = x1_j + w_j, y1_j + h_j
            x1_intersection = max(x1_i, x1_j)
            y1_intersection = max(y1_i, y1_j)
            x2_intersection = min(x2_i, x2_j)
            y2_intersection = min(y2_i, y2_j)
            minArea = min(w_i * h_i, w_j * h_j)
            intersection_area = max(0, x2_intersection - x1_intersection) * max(0, y2_intersection - y1_intersection)
            iou = intersection_area / minArea
            if iou > threshold:
                return True
    return False


def getNames(everythings):
    return [i.label for i in everythings]


def saveLabel(bboxs, types, filename, bkg, dics):
    inttype = [dics[i] for i in types]
    bboxdf = pd.DataFrame(bboxs, columns=["x", "y", "w", "h"])
    bboxdf["cx"] = bboxdf["x"] + (bboxdf["w"] / 2)
    bboxdf["cy"] = bboxdf["y"] + (bboxdf["h"] / 2)
    bboxdf["cx"] /= bkg.shape[1]
    bboxdf["w"] /= bkg.shape[1]
    bboxdf["cy"] /= bkg.shape[0]
    bboxdf["h"] /= bkg.shape[0]
    bboxdf["t"] = inttype
    bboxdf = bboxdf.loc[:, ["t", "cx", "cy", "w", "h"]]
    with open(f"{filename}.txt", "w+") as f:
        for i in np.array(bboxdf):
            f.write("{:d} {} {} {} {}\n".format(int(i[0]), i[1], i[2], i[3], i[4]))


def resize_image(image, max_size):
    height, width = image.shape[:2]
    if height <= max_size and width <= max_size:
        return image
    if height > width:
        scale = max_size / height
    else:
        scale = max_size / width
    new_height = int(height * scale)
    new_width = int(width * scale)
    resized_image = cv2.resize(image, (new_width, new_height))
    return resized_image


def chooseTypeIndices(everythings, dic):
    t = random.choice(list(dic.keys()))
    return [i for i, item in enumerate(getNames(everythings)) if item == t]


def chooseEqually(everythings, dic):
    idx = chooseTypeIndices(everythings, dic)
    return random.choice(idx)


def data_augmentation(dics, output_folder, path2labels, path2imgs, path2bkgs, counts=3, threshold=0.5, num_images=100):
    delete_folder(output_folder)
    os.mkdir(output_folder)
    os.mkdir(os.path.join(output_folder, "label"))
    os.mkdir(os.path.join(output_folder, "img"))

    delete_folder(os.path.join(path2labels, ".ipynb_checkpoints"))
    delete_folder(os.path.join(path2imgs, ".ipynb_checkpoints"))
    delete_folder(os.path.join(path2bkgs, ".ipynb_checkpoints"))

    bkgs = []
    for i in os.listdir(path2bkgs):
        bkgs.append(cv2.imread(os.path.join(path2bkgs, i)))

    everythings = []
    alllabels = list(set([i.split('.')[0] for i in os.listdir(path2labels)]))

    for lab in alllabels:
        lab += ".json"
        data = loadLabel(os.path.join(path2labels, lab))
        ig = cv2.imread(os.path.join(path2imgs, data['imagePath']))
        for i in data["shapes"]:
            everythings.append(Item(i["label"], np.array(ig), i["points"]))

    indices = [i for i, item in enumerate(getNames(everythings)) if item in list(dics.keys())]

    for mj in range(num_images):
        while True:
            bboxs = []
            types = []
            bkg = np.array(random.choice(bkgs))
            for i in range(counts):
                i = chooseEqually(everythings, dics)
                merge, (x, y, w, h) = insert(bkg, resize_image(everythings[i].get(), 1024))
                bboxs.append([x, y, w, h])
                types.append(everythings[i].label)

            if not checkIOU(bboxs, threshold):
                saveLabel(bboxs, types, os.path.join(output_folder, "label", f"{mj}"), bkg, dics)
                cv2.imwrite(os.path.join(output_folder, "img", f"{mj}.jpg"), merge)
                break
    