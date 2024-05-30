import cv2
import numpy as np

from piece import Piece
from math import atan2, pi
from utils import SidePosition


class JigsawPuzzleBoardViewer:
    def __init__(self, board: list[list[Piece]]):
        self.board = board
        self.calculate_canvas_size()

    def calculate_canvas_size(self):
        # Determine the total canvas size based on maximum row height and total column width
        total_height = sum(
            max(piece.original_image.shape[0] for piece in row) for row in self.board
        )
        total_width = max(
            sum(piece.original_image.shape[1] for piece in row) for row in self.board
        )
        # Initialize the canvas with 3 channels for a color image
        self.canvas = np.zeros((total_height + 25, total_width + 25, 3), dtype=np.uint8)

    def display_board(self):
        current_y = 0
        for index, row in enumerate(self.board):
            # Reverse the order of pieces in every second row
            # if index % 2 == 1:  # Assuming rows are 0-indexed
            #     row = list(reversed(row))

            max_row_height = max(piece.original_image.shape[0] for piece in row)
            current_x = 0
            for piece in row:
                # cv2.imshow("Piece", piece.original_image)
                # cv2.waitKey(0)
                rotated_image = self.rotate_piece_to_top(piece)
                # cv2.imshow("Rotated Piece", rotated_image)
                # cv2.waitKey(0)

                self.canvas[
                    current_y : current_y + rotated_image.shape[0],
                    current_x : current_x + rotated_image.shape[1],
                ] = rotated_image
                current_x += rotated_image.shape[1]
            current_y += max_row_height

        cv2.imshow("Jigsaw Puzzle Board", self.canvas)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def rotate_piece_to_top(self, piece):
        # Find the center of the top side and the piece's center
        top_side_center = next(
            side.center for side in piece.sides if side.position == SidePosition.TOP
        )[0]
        piece_center = piece.center

        # Calculate the vector from piece center to top side center
        dx = top_side_center[0] - piece_center[0]
        dy = top_side_center[1] - piece_center[1]

        # Calculate the angle in radians
        angle = atan2(-dy, dx)
        target_angle = pi / 2  # 90 degrees, target angle for the top

        # Determine number of 90-degree rotations needed
        rotations_needed = int(round((target_angle - angle) / (pi / 2))) % 4

        image = piece.original_image
        for _ in range(rotations_needed):
            image = self.rotate_image_90_clockwise(image)
        return image

    def rotate_image_90_clockwise(self, image):
        return cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
