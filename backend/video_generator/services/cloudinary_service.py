import cloudinary.uploader
import requests
from django.conf import settings
import os
# Initialize Cloudinary settings
cloudinary.config(
    cloud_name=settings.CLOUDINARY_CLOUD_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET,
)

def upload_image_to_cloudinary(image_url, image_filename):
    # Step 1: Download the image
    response = requests.get(image_url)
    data_dir = os.path.join(os.getcwd(), "data")  # Get the 'data' folder in the root directory
    os.makedirs(data_dir, exist_ok=True)  # Ensure the directory exists
    
    # Full path to save the image
    image_path = os.path.join(data_dir, image_filename)
    if response.status_code == 200:
        with open(image_path, 'wb') as f:
            f.write(response.content)

        # Step 2: Upload the image to Cloudinary
        upload_result = cloudinary.uploader.upload(image_filename)
        cloudinary_url = upload_result.get('secure_url')

        return cloudinary_url
    else:
        raise Exception(f"Failed to download image from {image_url}")

