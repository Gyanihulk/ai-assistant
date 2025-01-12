# Step 1: Use a base image with Python and GStreamer installed
FROM python:3.11-slim

# Step 2: Install required system dependencies
RUN apt-get update && apt-get install -y \
    gstreamer1.0-tools \
    gstreamer1.0-plugins-base \
    gstreamer1.0-plugins-good \
    gstreamer1.0-plugins-bad \
    gstreamer1.0-plugins-ugly \
    gstreamer1.0-libav \
    gobject-introspection \
    libgirepository1.0-dev \
    python3-gi \
    curl \
    build-essential \
    libffi-dev \
    libssl-dev \
    git

# Step 3: Set the working directory inside the container
WORKDIR /app

# Step 4: Copy the requirements.txt file and install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Step 5: Copy the entire Django project into the container
COPY . /app/

# Step 6: Expose the port that the Django app will run on (default 8000)
EXPOSE 8000

# Step 7: Run Django's development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
