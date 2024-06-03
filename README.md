# Jigsolver

## Description

Jigsolver is a web application that allows users to solve jigsaw puzzles. The user can upload an image of a unsolved jigsaw puzzle and the application will return the solved puzzle.

## How to run

To run the backend, you need to build the docker image and run it. You can do this by running the following commands:

Build the docker image:

```bash
docker build --pull --rm -f "Dockerfile" -t jigsolver:latest .
```

Run the docker image:

```bash
run -it --rm -p 8000:8000 jigsolver:latest
```

To run the frontend, you need to install the dependencies and run the development server. You can do this by running the following commands:

Install the dependencies:

```bash
cd frontend
npm install
```

Run the development server:

```bash
npm start
```

### Next Steps

* Upgrade the preprocessing stage to give more reliable results for the pieces segmentation;
* Upgrade the solving algorithm to give better results when solving edges and center pieces;
* Add a deskewing and dewarping algorithm to accept a more variety of images;
* Add a fontend feature to be able to move and select individual pieces and have a more intuitive solving process;
