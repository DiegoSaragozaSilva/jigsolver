import cv2

from preprocessor import *

def main():
    jigsaw = cv2.imread("sample_01.png") 

    preprocessor = Preprocessor()
    processed_jigsaw = preprocessor.process(jigsaw)

    cv2.imshow("Processed Image", processed_jigsaw)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return 0

if __name__ == "__main__":
    main()
