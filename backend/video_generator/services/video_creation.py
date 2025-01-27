import subprocess
import os
import requests
from tempfile import NamedTemporaryFile, TemporaryDirectory
import re

def setup_directory(base_path="/app/data"):
    # Create a directory for storing all image files
    dir_path = os.path.join(base_path)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    return dir_path

def download_image(url, index, base_dir):
    try:
        # Validate or prepend scheme if missing
        if not url.startswith("http://") and not url.startswith("https://"):
            raise ValueError(f"Invalid URL '{url}' - No scheme supplied.")
        
        response = requests.get(url, timeout=10)  # Added a timeout for the request
        response.raise_for_status()  # Raise HTTPError for bad responses

        # Save the image locally
        file_path = os.path.join(base_dir, f"generated_image_{index}.png")
        with open(file_path, "wb") as file:
            file.write(response.content)
        return file_path
    except Exception as e:
        raise Exception(f"Request failed for image: {url} - Error: {str(e)}")







def create_video_from_images(image_sources, output_video, use_local_images=False):
    """
    Creates a video from a list of image sources (URLs or local paths).
    
    Args:
        image_sources (list): List of image URLs or local file paths.
        output_video (str): The name of the output video file.
        use_local_images (bool): If True, treat image_sources as local paths. If False, treat them as URLs.

    Returns:
        str: The path to the created video file.
    """
    base_dir = setup_directory()
    print(f"baseDir: {base_dir}");
    if use_local_images:
        # Treat the image_sources as local file paths
        local_image_paths = image_sources
    else:
        # Download images if they are URLs
        local_image_paths = [download_image(url, i, base_dir) for i, url in enumerate(image_sources)]
    
    print(f"Local file paths for creating video: {local_image_paths}")
    
    if local_image_paths:
        # Create a pattern for GStreamer to use the images
        base_path = os.path.join(base_dir, "generated_image_%d.png")  # Ensure the pattern is in the created directory

    # Sanitize the output video filename
    sanitized_filename = sanitize_filename(output_video)
    output_video_path = os.path.join(base_dir, sanitized_filename)

    # Ensure the output file ends with ".mp4"
    if not output_video_path.endswith(".mp4"):
        output_video_path += ".mp4"

    print(f"Video will be created at: {output_video_path}")

    # Define the GStreamer pipeline
    pipeline = (
        f"gst-launch-1.0 multifilesrc location='{base_path}' index=0 caps='image/png,framerate=1/2' "
        f"! pngdec ! videoconvert ! x264enc ! mp4mux ! filesink location={output_video_path}"
    )
    print(f"Running: {pipeline}")

    # Run the pipeline
    process = subprocess.run(pipeline, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if process.returncode != 0:
        raise Exception(f"Error in GStreamer pipeline: {process.stderr.decode('utf-8')}")
    
    return output_video_path




def sanitize_filename(filename):
    return re.sub(r'[^\w\-\.]', '_', filename)