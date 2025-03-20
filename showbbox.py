import cv2
import os


def draw_bboxes(image, labels, img_width, img_height):
    for label in labels:
        class_id, x_center, y_center, width, height = map(float, label.split())
        x_center = int(x_center * img_width)
        y_center = int(y_center * img_height)
        width = int(width * img_width)
        height = int(height * img_height)
        x1 = int(x_center - width / 2)
        y1 = int(y_center - height / 2)
        x2 = int(x_center + width / 2)
        y2 = int(y_center + height / 2)
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(image, str(int(class_id)), (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
    return image


def main():
    img_dir = 'output/img'
    label_dir = 'output/label'
    img_files = sorted(os.listdir(img_dir))

    for img_file in img_files:
        img_path = os.path.join(img_dir, img_file)
        image = cv2.imread(img_path)
        if image is None:
            print(f"无法读取图像: {img_path}")
            continue
        img_height, img_width, _ = image.shape

        label_file = os.path.splitext(img_file)[0] + '.txt'
        label_path = os.path.join(label_dir, label_file)

        if os.path.exists(label_path):
            with open(label_path, 'r') as f:
                labels = f.readlines()

            image = draw_bboxes(image, labels, img_width, img_height)

        cv2.imshow('Image with BBoxes', image)

        cv2.waitKey(0)

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
