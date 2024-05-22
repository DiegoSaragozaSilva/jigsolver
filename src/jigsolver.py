import cv2

import matplotlib.pyplot as plt
from preprocessor import Preprocessor
from jigsaw import Jigsaw


def main():
    # Show the original image
    jigsaw_image = cv2.imread("jigsaw-samples/sample_4.png")

    preprocessor = Preprocessor(debug_mode=False)
    processed_jigsaw_image = preprocessor.process(jigsaw_image)

    jigsaw = Jigsaw(jigsaw_image, processed_jigsaw_image, debug_mode=False)
    # jigsaw.visualize()
    # for piece in jigsaw.pieces:
    #     piece.visualize()
    jigsaw.solve()

    return 0


if __name__ == "__main__":
    main()
