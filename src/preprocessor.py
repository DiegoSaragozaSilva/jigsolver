import cv2
import random
import numpy as np

class Preprocessor:
    gaussian_kernel = (5, 5)
    threshold_max_value = 255
    threshold_method = cv2.ADAPTIVE_THRESH_MEAN_C
    def __init__(self):
        pass

    def process(self, image):
        image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        image_blur = cv2.GaussianBlur(image_gray, self.gaussian_kernel, cv2.BORDER_DEFAULT)
        # image_threshold = cv2.threshold(image_blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        image_threshold = cv2.adaptiveThreshold(image_blur, self.threshold_max_value, self.threshold_method, cv2.THRESH_BINARY, 15, 5)
        image_canny = cv2.Canny(image_threshold, 30, 150)
        contours, hierarchy = cv2.findContours(image_canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        image_contours = np.zeros((image_threshold.shape[0], image_threshold.shape[1], 3), dtype = np.uint8)
        for i in range(len(contours)):
            cv2.drawContours(image_contours, contours, i, (123, 0, 0), 2, cv2.LINE_8, hierarchy, 0)

        image_contours_blur = cv2.GaussianBlur(image_contours, self.gaussian_kernel, cv2.BORDER_DEFAULT)

        floodfill_mask = np.zeros((image_contours_blur.shape[0] + 2, image_contours_blur.shape[1] + 2), dtype = np.uint8)
        cv2.floodFill(image_contours_blur, floodfill_mask, (0, 0), 123)

        image_masked = cv2.inRange(image_contours_blur, 122, 124)

        return image_masked

    def correct_perspective(self):
        pass
