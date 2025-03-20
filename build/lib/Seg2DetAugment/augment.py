import json
import cv2
import numpy as np
import random
import os
import pandas as pd
import shutil
import math


def cut(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 20, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    max_contour = max(contours, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(max_contour)
    cut = image[y:y + h, x:x + w]
    return cut, [x, y, w, h]


def rotate(image, angle):
    height, width = image.shape[:2]
    center = (width / 2, height / 2)
    rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1)
    cos = np.abs(rotation_matrix[0, 0])
    sin = np.abs(rotation_matrix[0, 1])
    new_width = int((height * sin) + (width * cos))
    new_height = int((height * cos) + (width * sin))
    rotation_matrix[0, 2] += (new_width / 2) - center[0]
    rotation_matrix[1, 2] += (new_height / 2) - center[1]
    rotated_image = cv2.warpAffine(image, rotation_matrix, (new_width, new_height))
    return rotated_image, rotation_matrix


def insert(bkg, img):
    x = random.randint(0, bkg.shape[1] - img.shape[1])
    y = random.randint(0, bkg.shape[0] - img.shape[0])
    mb = img[:, :, 0]
    mg = img[:, :, 1]
    mr = img[:, :, 2]
    img[np.bitwise_and(np.bitwise_and(mb < 30, mg < 30), mr < 30)] = 0
    bkg[y:y + img.shape[0], x:x + img.shape[1]][img != 0] = 0
    bkg[y:y + img.shape[0], x:x + img.shape[1]] += img
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 20, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    max_contour = max(contours, key=cv2.contourArea)
    xx, yy, w, h = cv2.boundingRect(max_contour)
    xx += x
    yy += y
    return bkg, (x, y,xx,yy,w,h)



class BBox:
    def __init__(self, bbox, label, points):
        self.bbox = bbox
        self.points = points
        self.label = label


class Point:
    def __init__(self, data, name):
        self.data = data
        self.name = name


class Item:
    def __init__(self, label, img, pts):
        self.label = label
        pts = np.array(pts, int)
        mask = np.zeros(img.shape)
        mask = cv2.fillPoly(mask, [pts], (255, 255, 255))
        img[mask == 0] = 0
        self.pts = pts
        self.mask = mask
        self.cut, [self.x, self.y, w, h] = cut(img)
        self.point = []

    def addPoint(self, point):
        point.data[0] -= self.x
        point.data[1] -= self.y
        self.point.append(point)

    def get(self):
        angle = random.randint(0, 180)
        image, rotation_matrix = rotate(self.cut, angle)
        points = rotate_points(self.point, rotation_matrix)
        return image, points


def distance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


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
        bbox_i = bboxes[i].bbox
        for j in range(i + 1, len(bboxes)):
            bbox_j = bboxes[j].bbox
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


def saveLabel(bboxs, filename, bkg, dics, pointsOrder):
    with open(f"{filename}.txt", "w+") as f:
        for box in bboxs:
            inttype = dics[box.label]
            x, y, w, h = box.bbox
            cx = x + (w / 2)
            cy = y + (h / 2)
            cx /= bkg.shape[1]
            w /= bkg.shape[1]
            cy /= bkg.shape[0]
            h /= bkg.shape[0]
            f.write("{:d} {} {} {} {} ".format(int(inttype), cx, cy, w, h))
            for pointName in pointsOrder:
                for wantToSave in box.points:
                    if pointName == wantToSave.name:
                        # print(pointName)
                        xa, ya = wantToSave.data
                        xa /= bkg.shape[1]
                        ya /= bkg.shape[0]
                        f.write("{} {} {} ".format(xa, ya, 2))
            f.write("\n")


def resize_image(image, max_size):
    height, width = image.shape[:2]
    if height <= max_size and width <= max_size:
        return image, 1.0
    if height > width:
        scale = max_size / height
    else:
        scale = max_size / width
    new_height = int(height * scale)
    new_width = int(width * scale)
    resized_image = cv2.resize(image, (new_width, new_height))
    return resized_image, scale


def resize_keypoints(keypoints, scale):
    resized_keypoints = []
    for keypoint in keypoints:
        x = int(keypoint.data[0] * scale)
        y = int(keypoint.data[1] * scale)
        resized_keypoints.append(Point([x, y], keypoint.name))
    return resized_keypoints


def chooseTypeIndices(everythings, dic):
    t = random.choice(list(dic.keys()))
    return [i for i, item in enumerate(getNames(everythings)) if item == t]


def chooseEqually(everythings, dic):
    idx = chooseTypeIndices(everythings, dic)
    return random.choice(idx)


def rotate_points(points, rotation_matrix):
    rotated_points = []
    for point in points:
        homogeneous_point = np.array([point.data[0], point.data[1], 1])
        rotated_point = np.matmul(rotation_matrix, homogeneous_point.T)
        rotated_points.append(Point(rotated_point[:2], point.name))
    return rotated_points


def data_augmentation(dics, output_folder, path2labels, path2imgs, path2bkgs, counts=3, threshold=0.5, num_images=100,
                      pointOrder=[]):
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
        pointsArr = []
        for i in data["shapes"]:
            if len(i["points"]) == 1:
                pointsArr.append(Point(i["points"][0], i["label"]))
            else:
                everythings.append(Item(i["label"], np.array(ig), i["points"]))
        selectedPoints = []
        if len(pointsArr) != 0:
            for thing in everythings:
                for pointPos in range(len(pointsArr)):
                    point = pointsArr[pointPos]
                    if thing.mask[int(point.data[1]), int(point.data[0]), 0] != 0:
                        thing.addPoint(point)
                        selectedPoints.append(pointPos)
        if len(selectedPoints) < len(pointsArr):
            pointsArr = np.array(pointsArr)
            restPoints = np.delete(pointsArr, selectedPoints, axis=0)
            for point in restPoints:
                min_dist = float('inf')
                closest_item = None
                for item in everythings:
                    for pts in item.pts:
                        dist = distance(pts, point.data)
                        if dist < min_dist:
                            min_dist = dist
                            closest_item = item
                if closest_item:
                    closest_item.addPoint(point)


    for mj in range(num_images):
        while True:
            bboxs = []
            bkg = np.array(random.choice(bkgs))
            for _ in range(counts):
                i = chooseEqually(everythings, dics)
                bkgh, bkgw, _ = bkg.shape
                img, pts = everythings[i].get()
                resized, scale = resize_image(img, min(bkgw, bkgh))
                bkg, (x, y,xx,yy,ww,hh) = insert(bkg, resized)

                new_pts = []
                for p in pts:
                    new_x = int(p.data[0] * scale + x)
                    new_y = int(p.data[1] * scale + y)
                    new_pts.append(Point([new_x, new_y], p.name))

                w, h = resized.shape[1], resized.shape[0]
                bboxs.append(BBox([xx, yy, ww, hh], everythings[i].label, new_pts))

            if not checkIOU(bboxs, threshold):
                saveLabel(bboxs, os.path.join(output_folder, "label", f"{mj}"), bkg, dics, pointOrder)
                cv2.imwrite(os.path.join(output_folder, "img", f"{mj}.jpg"), bkg)
                break
