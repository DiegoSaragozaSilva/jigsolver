import cv2
import numpy as np

from piece import Piece
from math import atan2, degrees
from utils import SidePosition

# from rembg import remove


class JigsawPuzzleBoardViewer:
    def __init__(self, board: list[list[Piece]], debug_mode=False):
        self.board = board
        self.debug_mode = debug_mode
        self.rotate_and_crop_pieces()
        self.calculate_canvas_size()
        self.build_canvas()

    def calculate_canvas_size(self):
        total_height = sum(
            max(piece.final_image.shape[0] for piece in row) for row in self.board
        )
        total_width = max(
            sum(piece.final_image.shape[1] for piece in row) for row in self.board
        )
        self.canvas = np.zeros((total_height + 25, total_width + 25, 3), dtype=np.uint8)

    def rotate_and_crop_pieces(self):
        for _, row in enumerate(self.board):
            for piece in row:
                rotated_image = self.rotate_piece_to_top(piece)
                final_image = self.crop_to_content(rotated_image)

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
                    cv2.imshow("Piece Final", final_image)

                    # Wait for esc key to close the windows
                    if cv2.waitKey(0) == 27:
                        cv2.destroyAllWindows()

                piece.final_image = final_image

    def build_canvas(self):
        current_y = 0
        for _, row in enumerate(self.board):
            max_row_height = max(piece.final_image.shape[0] for piece in row)
            current_x = 0
            for piece in row:
                self.canvas[
                    current_y : current_y + piece.final_image.shape[0],
                    current_x : current_x + piece.final_image.shape[1],
                ] = piece.final_image
                current_x += piece.final_image.shape[1]
            current_y += max_row_height

    def display_board(self):
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

    def crop_to_content(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(
            thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )
        x, y, w, h = cv2.boundingRect(contours[0])
        return image[y : y + h, x : x + w]
