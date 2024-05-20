import cv2

from preprocessor import *
from jigsaw import *

def main():
    jigsaw_image = cv2.imread("sample_03.png") 

    preprocessor = Preprocessor(debug_mode = True)
    processed_jigsaw_image = preprocessor.process(jigsaw_image)

    jigsaw = Jigsaw(jigsaw_image, processed_jigsaw_image)
    jigsaw.visualize()
    for piece in jigsaw.pieces:
        piece.visualize()
    jigsaw.solve()

    return 0

if __name__ == "__main__":
    main()
