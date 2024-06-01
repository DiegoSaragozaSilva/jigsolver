import cv2
import numpy as np

from piece import Piece
from math import atan2, degrees
from utils import SidePosition


class JigsawPuzzleBoardViewer:
    def __init__(self, board: list[list[Piece]], debug_mode=False):
        self.board = board
        self.debug_mode = debug_mode
        self.calculate_canvas_size()

    def calculate_canvas_size(self):
        total_height = sum(
            max(piece.original_image.shape[0] for piece in row) for row in self.board
        )
        total_width = max(
            sum(piece.original_image.shape[1] for piece in row) for row in self.board
        )
        self.canvas = np.zeros((total_height + 25, total_width + 25, 3), dtype=np.uint8)

    def display_board(self):
        current_y = 0
        for index, row in enumerate(self.board):
            max_row_height = max(piece.original_image.shape[0] for piece in row)
            current_x = 0
            for piece in row:
                rotated_image = self.rotate_piece_to_top(piece)
                # Show the piece original and rotated, drawing the top side center point
                top_side = next(
                    side for side in piece.sides if side.position == SidePosition.TOP
                )
                top_side_contours = top_side.points

                if self.debug_mode:

                    # Draw the top side contours
                    cv2.drawContours(
                        piece.original_image,
                        [top_side_contours],
                        -1,
                        (0, 255, 0),
                        2,
                    )
                    cv2.imshow("Piece Original", piece.original_image)

                    cv2.imshow("Piece Rotated", rotated_image)

                    # Wait for esc key to close the windows
                    if cv2.waitKey(0) == 27:
                        cv2.destroyAllWindows()

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
        top_side_center = next(
            side.center for side in piece.sides if side.position == SidePosition.TOP
        )

        piece_center = piece.center

        dx = top_side_center[0] - piece_center[0]
        dy = top_side_center[1] - piece_center[1]

        angle = atan2(-dy, dx)
        rotation_degrees = degrees(angle) - 90

        rotated_image = self.rotate_image(piece.original_image, -rotation_degrees)
        return rotated_image

    def rotate_image(self, image, angle):
        # Get the image dimensions
        (h, w) = image.shape[:2]
        # Calculate the center of the image
        center = (w / 2, h / 2)
        # Get the rotation matrix
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        # Perform the rotation
        rotated = cv2.warpAffine(image, M, (w, h))
        return rotated
