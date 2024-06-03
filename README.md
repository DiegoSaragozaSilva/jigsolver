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
