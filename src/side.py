import cv2
import numpy as np

from utils import SideType, SidePosition


class Side:

    def __init__(
        self,
        points: np.ndarray,
        type: SideType,
        side_image_trimmed: np.ndarray,
        position: SidePosition,
    ):
        self.points = points
        self.length = cv2.arcLength(points, False)
        self.type = type
        self.side_image_trimmed = side_image_trimmed

        self.center = [np.average(self.points, axis=0), np.average(self.points, axis=1)]

        self.can_attach_piece = self.type != SideType.FLAT
        self.position = position

    def attach_piece(self):
        self.can_attach_piece = False

    def set_position(self, position: SidePosition):
        self.position = position
