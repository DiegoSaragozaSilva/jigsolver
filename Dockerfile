FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Update CA certificates and install dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates \
    && update-ca-certificates

# Copy the requirements file into the container
COPY requirements.txt /app/requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install OpenCV dependencies
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

# Copy the source code folder into the container
COPY src /app

# Expose port 8000 to the host
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
