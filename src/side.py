import cv2
import numpy as np

from utils import SideType, SidePosition


class Side:

    def __init__(self, points: np.ndarray, type: SideType):
        self.points = points
        self.length = cv2.arcLength(points, False)
        self.type = type

        M = cv2.moments(self.points)
        self.center = [int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"])]

        self.can_attach_piece = self.type != SideType.FLAT
        self.position = None

    def attach_piece(self):
        self.can_attach_piece = False

    def set_position(self, position: SidePosition):
        self.position = position
