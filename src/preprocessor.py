import cv2
import numpy as np
from matplotlib import pyplot as plt
import imutils


class Preprocessor:
    debug_mode = None

    def __init__(self, debug_mode=False):
        self.debug_mode = debug_mode

    def process(self, image):
        image = cv2.copyMakeBorder(
            image, 5, 5, 5, 5, cv2.BORDER_CONSTANT, value=[255, 255, 255]
        )
        image = imutils.resize(image, width=1280)
        # image = cv2.resize(image, (1280, 720))
        image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        image_blur = cv2.bilateralFilter(image_gray, 11, 200, 200)
        image_threshold = cv2.adaptiveThreshold(
            image_blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 19, 2
        )

        kernel = np.ones((3, 3), dtype=np.uint8)
        image_opening = cv2.morphologyEx(
            image_threshold, cv2.MORPH_OPEN, kernel, iterations=2
        )

        image_background = cv2.dilate(image_opening, kernel, iterations=3)

        image_distance = cv2.distanceTransform(image_threshold, cv2.DIST_L2, 5)
        cv2.normalize(image_distance, image_distance, 0.0, 0.1, cv2.NORM_MINMAX)
        ret, image_foreground = cv2.threshold(
            image_distance, 0.5 * image_distance.max(), 255, 0
        )
        image_foreground = np.uint8(image_foreground)

        image_unknown = cv2.subtract(image_background, image_foreground)

        num_markers, markers, stats, centroids = cv2.connectedComponentsWithStats(
            image_foreground, 4, cv2.CV_32S
        )
        markers = markers + 1
        markers[image_unknown == 255] = 0

        image_watershed = image.copy()
        markers = cv2.watershed(image_watershed, markers)

        lowest_area_index = 0
        lowest_area = np.inf
        for i in range(num_markers):
            if stats[i, cv2.CC_STAT_AREA] < lowest_area and (stats[i, cv2.CC_STAT_LEFT] == 0 and stats[i, cv2.CC_STAT_TOP] == 0):
                lowest_area = stats[i, cv2.CC_STAT_AREA]
                lowest_area_index = i
            # print(f"MARKER {i}")
            # print(f"- X Y W H ({stats[i, cv2.CC_STAT_LEFT]}, {stats[i, cv2.CC_STAT_TOP]}, {stats[i, cv2.CC_STAT_WIDTH]}, {stats[i, cv2.CC_STAT_HEIGHT]})")
            # print(f"- AREA {stats[i, cv2.CC_STAT_AREA]}")
            # print(f"- CENTER ({centroids[i][0]}, {centroids[i][1]})")
            # plt.imshow((markers == i).astype("uint8") * 255)
            # plt.show()

        image_watershed[markers == lowest_area_index] = [0, 0, 255]

        red_mask = cv2.inRange(
            image_watershed, np.array([0, 0, 255]), np.array([0, 0, 255])
        )
        image_watershed = cv2.bitwise_and(
            image_watershed, image_watershed, mask=red_mask
        )
        image_watershed = cv2.cvtColor(image_watershed, cv2.COLOR_BGR2GRAY)

        ret, image_watershed_threshold = cv2.threshold(
            image_watershed, 0, 255, cv2.THRESH_BINARY_INV
        )

        contours, hierarchy = cv2.findContours(
            image_watershed_threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
        )
        image_contours = np.zeros(image.shape, dtype=np.uint8)
        cv2.drawContours(
            image_contours, sorted(contours, key=cv2.contourArea)[:-1], -1, 255, -1
        )

        if self.debug_mode:
            figure = plt.figure(figsize=(12, 6))
            figure.add_subplot(3, 3, 1)
            plt.imshow(image_blur)
            figure.add_subplot(3, 3, 2)
            plt.imshow(image_threshold)
            figure.add_subplot(3, 3, 3)
            plt.imshow(image_distance)
            figure.add_subplot(3, 3, 4)
            plt.imshow(markers)
            figure.add_subplot(3, 3, 5)
            plt.imshow(image_watershed)
            figure.add_subplot(3, 3, 6)
            plt.imshow(image_watershed_threshold)
            figure.add_subplot(3, 3, 7)
            plt.imshow(image_contours)
            plt.show()

        return cv2.cvtColor(image_contours, cv2.COLOR_BGR2GRAY)

    def correct_perspective(self):
        pass
