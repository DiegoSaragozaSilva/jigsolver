import cv2

from jigsaw import Jigsaw
from preprocessor import Preprocessor
from board_viwer import JigsawPuzzleBoardViewer


def main():
    # Show the original image
    jigsaw_image = cv2.imread("jigsaw-samples/sample_7.png")

    preprocessor = Preprocessor(debug_mode=False)
    processed_jigsaw_image = preprocessor.process(jigsaw_image)

    jigsaw = Jigsaw(jigsaw_image, processed_jigsaw_image, debug_mode=True)

    # jigsaw.visualize()
    # for piece in jigsaw.pieces:
    #     piece.visualize()

    solved_jigsaw = jigsaw.solve()

    board_viewer = JigsawPuzzleBoardViewer(solved_jigsaw)
    board_viewer.display_board()

    return 0


if __name__ == "__main__":
    main()
