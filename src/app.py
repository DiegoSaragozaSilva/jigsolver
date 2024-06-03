import io
import cv2
import numpy as np

from PIL import Image
from fastapi import FastAPI, File, UploadFile, Query
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware


from jigsaw import Jigsaw
from preprocessor import Preprocessor
from board_viwer import JigsawPuzzleBoardViewer

app = FastAPI(
    title="Jigsaw Puzzle Solver",
    description="A Jigsaw Puzzle Solver using OpenCV and Python",
    version="0.1",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000"
    ],  # Allows all origins, or specify a list of origins you want to allow
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


@app.post("/solve-jigsaw/")
async def solve_jigsaw_endpoint(
    file: UploadFile = File(...), distance_threshold: int = Query(150)
):
    # Read the image file
    image_data = np.frombuffer(await file.read(), np.uint8)
    jigsaw_image = cv2.imdecode(image_data, cv2.IMREAD_COLOR)

    # Read numpy array image with OpenCV
    preprocessor = Preprocessor(debug_mode=False)

    # Process the image
    processed_jigsaw_image = preprocessor.process(jigsaw_image)

    # Solve the jigsaw
    jigsaw = Jigsaw(
        original_image=jigsaw_image,
        processed_image=processed_jigsaw_image,
        distance_threshold=distance_threshold,
        debug_mode=False,
    )
    solved_jigsaw = jigsaw.solve()

    # Get the solved image
    board_viewer = JigsawPuzzleBoardViewer(solved_jigsaw)

    # Create a PIL image from the solved board
    solved_image = Image.fromarray(board_viewer.canvas)

    # Save the solved image to a BytesIO object
    img_byte_arr = io.BytesIO()
    solved_image.save(img_byte_arr, format="JPEG")
    img_byte_arr.seek(0)

    # Return the solved image
    return StreamingResponse(img_byte_arr, media_type="image/jpeg")
