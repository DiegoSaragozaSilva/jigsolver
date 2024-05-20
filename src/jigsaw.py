import cv2
import numpy as np
from matplotlib import pyplot as plt

from piece import *

class Jigsaw:
    original_image = None
    processed_image = None
    pieces = None
    def __init__(self, original_image, processed_image):
        self.original_image = original_image
        self.processed_image = processed_image
        self.pieces = []
        
        contours, hierarchy = cv2.findContours(processed_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            contour_bb = cv2.boundingRect(contour)
            piece_mask = processed_image[contour_bb[1]:contour_bb[1] + contour_bb[3], contour_bb[0]:contour_bb[0] + contour_bb[2]]
            image_mask = np.zeros_like(processed_image)
            image_mask[contour_bb[1]:contour_bb[1] + contour_bb[3], contour_bb[0]:contour_bb[0] + contour_bb[2]] = piece_mask
            piece_image = image_mask[contour_bb[1]:contour_bb[1] + contour_bb[3], contour_bb[0]:contour_bb[0] + contour_bb[2]]
            piece_image = cv2.copyMakeBorder(piece_image, 25, 25, 25, 25, cv2.BORDER_CONSTANT, value = [0, 0, 0])

            _contours, hierarchy = cv2.findContours(piece_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
            piece_contour = max(_contours, key = cv2.contourArea)

            final_piece_image = np.zeros(piece_image.shape, dtype = np.uint8)
            cv2.drawContours(final_piece_image, [piece_contour], -1, 255, -1)

            piece = Piece(final_piece_image, piece_contour)
            self.pieces.append(piece)

        for piece in self.pieces:
            piece.classify()

    def visualize(self):
        figure = plt.figure(figsize = (12, 6))
        figure.add_subplot(1, 2, 1)
        plt.imshow(self.original_image)
        figure.add_subplot(1, 2, 2)
        plt.imshow(self.processed_image)
        plt.show()

    def solve(self):
       pass
        # def is_edge_piece(piece):
       #     return piece.type == PIECE_TYPE_BORDER or piece.type == PIECE_TYPE_CORNER
       # 
       # # Start solving the edge pieces
       # edge_pieces = list(filter(is_edge_piece, self.pieces))
       # for piece in edge_pieces:
       #     for side in piece.sides:
       #         # Ignore flat sides
       #         if side.type == SIDE_TYPE_FLAT:
       #             continue
       #         
       #         # Take paremeters for the matching side
       #         best_piece_match = None
       #         best_side_match = None
       #         best_length_distance = np.inf 
       #         best_centroid_distance = np.inf
       #         for _piece in edge_pieces:
       #             # Ignore the same piece
       #             if piece == _piece:
       #                 continue
       #             
       #             for _side in _piece.sides:
       #                 # Ignore pieces with the same side (head-head or hole-hole) and with flat sides
       #                 if side.type == _side.type or _side.type == SIDE_TYPE_FLAT:
       #                     continue

       #                 length_distance = cv2.matchShapes(side.points, _side.points, 1, 0.0) # abs(side.length - _side.length)
       #                 centroid_distance = np.linalg.norm(np.subtract(np.array(side.center), np.array(_side.center)))
       #                 if length_distance < best_length_distance:
       #                     best_length_distance = length_distance
       #                     best_piece_match = _piece
       #                     best_side_match = _side

       #         print(best_length_distance)

       #         figure = plt.figure(figsize = (12, 4)) 
       #         figure.add_subplot(1, 2, 1)
       #         piece_image = piece.image.copy()
       #         piece_image = cv2.cvtColor(piece_image, cv2.COLOR_GRAY2BGR)
       #         cv2.polylines(piece_image, np.int32([side.points]), isClosed = False, color = (255, 0, 0), thickness = 3)
       #         plt.imshow(piece_image)

       #         figure.add_subplot(1, 2, 2)
       #         piece_image = best_piece_match.image.copy()
       #         piece_image = cv2.cvtColor(piece_image, cv2.COLOR_GRAY2BGR)
       #         cv2.polylines(piece_image, np.int32([best_side_match.points]), isClosed = False, color = (255, 0, 0), thickness = 3)
       #         plt.imshow(piece_image)
       #         plt.show()
