import cv2
import numpy as np
import imutils

from matplotlib import pyplot as plt
from skimage.metrics import structural_similarity


from side import Side
from piece import Piece
from utils import SidePosition, SideType, PieceType


class Jigsaw:
    def __init__(self, original_image, processed_image, debug_mode=False):
        self.processed_image = processed_image
        self.pieces: list[Piece] = []
        self.debug_mode = debug_mode

        # Fit original image shape to the processed one
        self.original_image = cv2.copyMakeBorder(
            original_image, 5, 5, 5, 5, cv2.BORDER_CONSTANT, value=[255, 255, 255]
        )
        # self.original_image = cv2.resize(original_image, (1280, 720))
        self.original_image = imutils.resize(self.original_image, width=1280)

        contours, hierarchy = cv2.findContours(
            processed_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )
        for contour in contours:
            # Piece processed image
            contour_bb = cv2.boundingRect(contour)
            piece_mask = processed_image[
                contour_bb[1] : contour_bb[1] + contour_bb[3],
                contour_bb[0] : contour_bb[0] + contour_bb[2],
            ]
            image_mask = np.zeros_like(processed_image)
            image_mask[
                contour_bb[1] : contour_bb[1] + contour_bb[3],
                contour_bb[0] : contour_bb[0] + contour_bb[2],
            ] = piece_mask
            piece_image = image_mask[
                contour_bb[1] : contour_bb[1] + contour_bb[3],
                contour_bb[0] : contour_bb[0] + contour_bb[2],
            ]
            piece_image = cv2.copyMakeBorder(
                piece_image, 25, 25, 25, 25, cv2.BORDER_CONSTANT, value=[0, 0, 0]
            )

            _contours, _ = cv2.findContours(
                piece_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE
            )
            piece_contour = max(_contours, key=cv2.contourArea)

            final_piece_image = np.zeros(piece_image.shape, dtype=np.uint8)
            cv2.drawContours(final_piece_image, [piece_contour], -1, 255, -1)

            # Piece original image
            piece_mask = self.original_image[
                contour_bb[1] : contour_bb[1] + contour_bb[3],
                contour_bb[0] : contour_bb[0] + contour_bb[2],
            ]
            image_mask = np.zeros_like(self.original_image)
            image_mask[
                contour_bb[1] : contour_bb[1] + contour_bb[3],
                contour_bb[0] : contour_bb[0] + contour_bb[2],
            ] = piece_mask
            original_piece_image = image_mask[
                contour_bb[1] : contour_bb[1] + contour_bb[3],
                contour_bb[0] : contour_bb[0] + contour_bb[2],
            ]
            original_piece_image = cv2.copyMakeBorder(
                original_piece_image,
                25,
                25,
                25,
                25,
                cv2.BORDER_CONSTANT,
                value=[0, 0, 0],
            )

            piece = Piece(final_piece_image, original_piece_image, piece_contour)
            self.pieces.append(piece)

        for piece in self.pieces:
            piece.classify()

    def visualize(self):
        figure = plt.figure(figsize=(12, 6))
        figure.add_subplot(1, 2, 1)
        plt.imshow(self.original_image)
        figure.add_subplot(1, 2, 2)
        plt.imshow(self.processed_image)
        plt.show()

    def solve(self):
        self.board, self.pieces_to_place = self._initialize_board()
        self._place_first_corner()
        self._place_borders()
        return self.board

    def _calculate_jigsaw_dimensions(
        self, border_pieces_amount: int
    ) -> tuple[int, int]:
        # border_pieces_amount = 2 * (rows + columns) - 4 (since corners are counted twice)
        # rows + columns = (border_pieces_amount + 4) / 2
        total = (border_pieces_amount + 4) / 2

        # Iterate to find the pair (rows, columns) such that rows * columns is minimized
        # And both values should be as close as possible to each other
        best_rows, best_columns = 1, int(total - 1)
        min_diff = abs(best_rows - best_columns)

        for rows in range(1, int(total)):
            columns = total - rows
            if columns.is_integer():
                columns = int(columns)
                diff = abs(rows - columns)
                if diff < min_diff:
                    min_diff = diff
                    best_rows, best_columns = rows, columns

        return best_rows, best_columns

    def _initialize_board(self) -> tuple[list[list[Piece]], list[Piece]]:
        # Calculate number of rows and columns
        flat_sides = 0
        for piece in self.pieces:
            for side in piece.sides:
                if side.type == SideType.FLAT:
                    flat_sides += 1

                    break

        rows, cols = self._calculate_jigsaw_dimensions(border_pieces_amount=flat_sides)

        # Create empty board
        board = [[None for _ in range(cols)] for _ in range(rows)]
        pieces_to_place = self.pieces.copy()

        return board, pieces_to_place

    def _get_matching_coefficient(self, side_1: Side, side_2: Side) -> float:
        # Ensure the points are in the correct shape for OpenCV
        contour1 = side_1.points.reshape((-1, 1, 2)).astype(np.int32)
        contour2 = side_2.points.reshape((-1, 1, 2)).astype(np.int32)

        # Calculate the match shape value using cv2.matchShapes
        """ matching_coefficient = cv2.matchShapes(
            contour1, contour2, cv2.CONTOURS_MATCH_I1, 0.0
        ) """
        side_image_trimmed_1 = cv2.cvtColor(
            side_1.side_image_trimmed, cv2.COLOR_BGR2GRAY
        )
        side_image_trimmed_2 = cv2.cvtColor(
            side_2.side_image_trimmed, cv2.COLOR_BGR2GRAY
        )

        # resize image 2 to the size of image 1
        side_image_trimmed_2 = cv2.resize(
            side_image_trimmed_2, side_image_trimmed_1.shape[::-1]
        )

        #
        matching_coefficient = 1 - structural_similarity(
            side_image_trimmed_1, side_image_trimmed_2, gradient=False
        )

        if self.debug_mode:
            # Determine the size of the canvas
            canvas_size = (500, 500)
            canvas = np.zeros(canvas_size, dtype=np.uint8)

            # Show the images compared in cavas
            canvas[: side_image_trimmed_1.shape[0], : side_image_trimmed_1.shape[1]] = (
                side_image_trimmed_1
            )
            canvas[
                : side_image_trimmed_2.shape[0],
                side_image_trimmed_1.shape[1] : side_image_trimmed_1.shape[1]
                + side_image_trimmed_2.shape[1],
            ] = side_image_trimmed_2

            # Draw the contours on the canvas
            # cv2.drawContours(canvas, [contour1], -1, (255, 0, 0), 2)  # Blue contour
            # cv2.drawContours(canvas, [contour2], -1, (0, 255, 0), 2)  # Green contour

            # Add the matching coefficient value to the canvas
            text_position = (10, 30)  # Position of the text on the canvas
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 1
            font_color = (255, 255, 255)  # White color for the text
            font_thickness = 2

            text = f"Matching Coefficient: {matching_coefficient:.4f}"
            cv2.putText(
                canvas,
                text,
                text_position,
                font,
                font_scale,
                font_color,
                font_thickness,
            )

            # Show the canvas with the contours and matching coefficient
            cv2.imshow("Contours", canvas)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        return matching_coefficient

    def _set_first_corner_piece_positions(self, corner_piece: Piece) -> Piece:
        # Find the flat sides of the corner piece
        flat_sides = [
            index
            for index, side in enumerate(corner_piece.sides)
            if side.type == SideType.FLAT
        ]

        # Assign positions to the flat sides and their opposite sides
        corner_piece.sides[flat_sides[0]].set_position(SidePosition.LEFT)
        corner_piece.sides[(flat_sides[0] + 2) % 4].set_position(SidePosition.RIGHT)

        if flat_sides[1] == (flat_sides[0] + 1) % 4:
            corner_piece.sides[flat_sides[1]].set_position(SidePosition.BOTTOM)
            corner_piece.sides[(flat_sides[1] + 2) % 4].set_position(SidePosition.TOP)
        else:
            corner_piece.sides[flat_sides[1]].set_position(SidePosition.TOP)
            corner_piece.sides[(flat_sides[1] + 2) % 4].set_position(
                SidePosition.BOTTOM
            )

        return corner_piece

    def _place_first_corner(self):
        # Find and remove the first corner piece from the pieces to place
        corner_piece = next(
            piece for piece in self.pieces_to_place if piece.type == PieceType.CORNER
        )
        self.pieces_to_place.remove(corner_piece)

        # Place the corner piece at the top-left corner of the board
        self.board[0][0] = self._set_first_corner_piece_positions(
            corner_piece=corner_piece
        )

    def _set_border_piece_positions(
        self,
        border_piece: Piece,
        flat_side_index: int,
        attach_side_position: SidePosition,
        attach_side_index: int,
    ) -> Piece:
        # Assign positions to the flat side and the attached side
        border_piece.sides[attach_side_index].set_position(attach_side_position)
        border_piece.sides[attach_side_index].attach_piece()

        flat_side_position = SidePosition.turn_clockwise(attach_side_position)
        border_piece.sides[flat_side_index].set_position(flat_side_position)

        # Assign the opposite positions
        border_piece.sides[(flat_side_index + 2) % 4].set_position(
            SidePosition.opposite(flat_side_position)
        )
        border_piece.sides[(attach_side_index + 2) % 4].set_position(
            SidePosition.opposite(attach_side_position)
        )

        return border_piece

    def _find_candidates(self, next_side_type: SideType, piece_type: PieceType):
        return [
            piece
            for piece in self.pieces_to_place
            if piece.type == piece_type
            and any(
                side.type == next_side_type and side.can_attach_piece
                for side in piece.sides
            )
        ]

    def _place_border_piece(
        self,
        current_side: Side,
        board_pos: tuple[int, int],
    ):

        next_side_type = SideType.opposite(current_side.type)

        # Filter candidates with the required next_side_type and can_attach_piece
        candidates = self._find_candidates(
            next_side_type=next_side_type, piece_type=PieceType.BORDER
        )

        # Find the best match based on the matching coefficient
        best_match = None
        best_coefficient = float("inf")
        attachment_side_index = 0
        flat_side_index = 0

        for piece in candidates:
            candidate_flat_side_index = next(
                index
                for index, side in enumerate(piece.sides)
                if side.type == SideType.FLAT
            )
            oposite_flat_side_index = (candidate_flat_side_index + 2) % 4

            for i, side in enumerate(piece.sides):
                if (
                    side.type == next_side_type
                    and side.can_attach_piece
                    and i != oposite_flat_side_index
                ):
                    coefficient = self._get_matching_coefficient(
                        side_1=current_side, side_2=side
                    )
                    if coefficient < best_coefficient:
                        best_match = piece
                        best_coefficient = coefficient
                        attachment_side_index = i
                        flat_side_index = next(
                            index
                            for index, side in enumerate(piece.sides)
                            if side.type == SideType.FLAT
                        )

        # Remove the best match from pieces_to_place
        self.pieces_to_place.remove(best_match)

        # Set positions of the sides for the best match
        best_match = self._set_border_piece_positions(
            border_piece=best_match,
            flat_side_index=flat_side_index,
            attach_side_position=SidePosition.opposite(current_side.position),
            attach_side_index=attachment_side_index,
        )

        # Place the best match on the board
        self.board[board_pos[0]][board_pos[1]] = best_match

    def _set_corner_piece_positions(
        self,
        corner_piece: Piece,
        attach_side_position: SidePosition,
        attach_side_index: int,
    ) -> Piece:
        # Assign positions to the flat side and the attached side
        corner_piece.sides[attach_side_index].set_position(attach_side_position)
        corner_piece.sides[attach_side_index].attach_piece()

        first_flat_side_position = SidePosition.turn_clockwise(attach_side_position)
        second_flat_side_position = SidePosition.turn_clockwise(
            first_flat_side_position
        )
        remaining_side_position = SidePosition.turn_counter_clockwise(
            attach_side_position
        )

        i = (
            1
            if corner_piece.sides[(attach_side_index + 1) % 4].type == SideType.FLAT
            else -1
        )
        corner_piece.sides[(attach_side_index + i) % 4].set_position(
            first_flat_side_position
        )
        corner_piece.sides[(attach_side_index + 2 * i) % 4].set_position(
            second_flat_side_position
        )
        corner_piece.sides[(attach_side_index + 3 * i) % 4].set_position(
            remaining_side_position
        )

        return corner_piece

    def _place_corner_piece(
        self,
        current_side: Side,
        board_pos: tuple[int, int],
    ) -> Piece:

        next_side_type = SideType.opposite(current_side.type)

        candidates = self._find_candidates(
            next_side_type=next_side_type, piece_type=PieceType.CORNER
        )

        # Find the best match based on the matching coefficient
        best_match = None
        best_coefficient = float("inf")
        attachment_side_index = 0

        for piece in candidates:
            for i, side in enumerate(piece.sides):
                if side.type == next_side_type and side.can_attach_piece:
                    coefficient = self._get_matching_coefficient(
                        side_1=current_side, side_2=side
                    )
                    if coefficient < best_coefficient:
                        best_match = piece
                        best_coefficient = coefficient
                        attachment_side_index = i

        # Remove the best match from pieces_to_place
        self.pieces_to_place.remove(best_match)

        # Set positions of the sides for the best match
        best_match = self._set_corner_piece_positions(
            corner_piece=best_match,
            attach_side_position=SidePosition.opposite(current_side.position),
            attach_side_index=attachment_side_index,
        )

        # Place the best match on the board
        self.board[board_pos[0]][board_pos[1]] = best_match

    def _is_position_filled(self, pos: tuple[int, int]) -> bool:
        # Check if the given position is filled
        return self.board[pos[0]][pos[1]] is not None

    def _is_position_corner(self, pos: tuple[int, int]) -> bool:
        # Check if the given position is a corner piece
        return pos in {
            (0, 0),
            (0, len(self.board[0]) - 1),
            (len(self.board) - 1, 0),
            (len(self.board) - 1, len(self.board[0]) - 1),
        }

    def _is_board_full(self) -> bool:
        # Check if the board is full
        return all(all(cell is not None for cell in row) for row in self.board)

    def _place_borders(self):
        def place_border_for_positions(
            positions, side_position, adjust_row, adjust_col
        ):
            nonlocal current_piece
            for pos in positions:
                if self._is_position_filled(pos=pos):
                    continue

                current_side_to_attach_index = next(
                    index
                    for index, side in enumerate(current_piece.sides)
                    if side.position == side_position
                )
                current_piece.sides[current_side_to_attach_index].attach_piece()
                self.board[pos[0] + adjust_row][pos[1] + adjust_col] = current_piece
                current_side_to_attach = current_piece.sides[
                    current_side_to_attach_index
                ]

                if self._is_position_corner(pos=pos):
                    self._place_corner_piece(
                        current_side=current_side_to_attach,
                        board_pos=pos,
                    )
                else:
                    self._place_border_piece(
                        current_side=current_side_to_attach,
                        board_pos=pos,
                    )

                current_piece = self.board[pos[0]][pos[1]]

        current_piece = self.board[0][0]
        top_positions = [(0, i) for i in range(1, len(self.board[0]))]
        right_positions = [
            (i, len(self.board[0]) - 1) for i in range(1, len(self.board))
        ]
        bottom_positions = [
            (len(self.board) - 1, i) for i in range(len(self.board[0]) - 2, -1, -1)
        ]

        left_positions = (
            []
            if self._is_board_full()
            else [(i, 0) for i in range(len(self.board) - 2, -1, -1)]
        )

        place_border_for_positions(top_positions, SidePosition.RIGHT, 0, -1)
        place_border_for_positions(right_positions, SidePosition.BOTTOM, -1, 0)
        place_border_for_positions(bottom_positions, SidePosition.LEFT, 0, 1)
        place_border_for_positions(left_positions, SidePosition.TOP, 1, 0)
