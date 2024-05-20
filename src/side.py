import cv2

SIDE_TYPE_HEAD = 0
SIDE_TYPE_HOLE = 1
SIDE_TYPE_FLAT = 2

class Side:
    points = None
    length = None
    center = None
    type = None
    def __init__(self, points, type):
        self.points = points
        self.length = cv2.arcLength(points, False)
        self.type = type

        M = cv2.moments(self.points)
        self.center = [int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"])]
