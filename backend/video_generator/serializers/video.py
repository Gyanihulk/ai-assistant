
from rest_framework import serializers
from video_generator.models.video import Video
from video_generator.models.image import Image
from video_generator.services.prompt_generation import generate_prompts
from video_generator.services.image_generation import generate_image, download_image
from video_generator.services.audio_generation import generate_audio, download_audio

# from video_generator.services.video_generation import generate_video_with_sora
from video_generator.services.video_creation import create_video_from_images
from video_generator.services.cloudinary_service import upload_image_to_cloudinary
import os
class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['id', 'title', 'description', 'published_at', 'length_seconds', 'topic', 'orientation']  # Include orientation
        



class VideoGenerationSerializer(serializers.Serializer):
    topic = serializers.CharField(max_length=100)
    length_seconds = serializers.IntegerField()
    video_file = serializers.CharField(read_only=True)  # The generated video file path
    
    def create(self, validated_data):
        topic = validated_data.get('topic')
        length_seconds = validated_data.get('length_seconds')

        num_images = length_seconds // 2  # Example: 1 image every 2 seconds
        print(f"Topic: {topic}, Length (seconds): {length_seconds},no of images: {num_images}") 
        
        
        # Step 1: Generate prompts using GPT
        prompts = generate_prompts(topic, num_prompts=num_images)
        
        image_filenames = []
        
        # Step 2: Generate images and save them
        for i, prompt in enumerate(prompts):
            image_url = generate_image(prompt)
            image_filename = f"generated_image_{i}.png"
            local_image_path = os.path.join("/app/data", image_filename)  

            # Upload to Cloudinary and get the Cloudinary URL
            cloudinary_url = upload_image_to_cloudinary(image_url, image_filename)
            # print(f"Generated prompt: {prompt}")
            # print(f"Uploaded to Cloudinary: {cloudinary_url}")
            # Save the Cloudinary URL instead of the local image URL
            image=Image.objects.create(prompt=prompt, image_url=cloudinary_url)
            print(f"saved Image {image.image_url}")
            image_filenames.append(local_image_path)
            
            text_input = "Hello, this is a test for generating audio using OpenAI."
            audio_file_name = "test_audio.mp3"

            # Generate the audio
            audio_saved_url = generate_audio(text_input)

            # Download and save the audio
            # saved_audio_path = download_audio(audio_url, audio_file_name)
            print(f"Audio saved at: {audio_saved_url}")
            
            
            
            
            
        print(f"local file image for creating video: {image_filenames}")
        # Step 3: Create the video using GStreamer
        video_filename = f"{topic}_video"
        try:
            output_video_path = create_video_from_images(image_filenames, video_filename,True)
            print(f"Video created at: {output_video_path}")
        except Exception as e:
            print(f"Error creating video: {e}")
            raise

        # Step 4: Save the video metadata to the database
        video = Video.objects.create(
            title=f"{topic} Video",
            description=f"A video generated about {topic}",
            length_seconds=length_seconds,
            topic=topic,
            video_file=output_video_path
        )

        return video




class VideoFromImagesSerializer(serializers.Serializer):
    video_title = serializers.CharField(max_length=200)
    description = serializers.CharField(max_length=1000)
    topic = serializers.CharField(max_length=100)

    def create(self, validated_data):
        video_title = validated_data.get('video_title')
        description = validated_data.get('description')
        topic = validated_data.get('topic')

        # Fetch the first 5 images related to the topic from the database
        images = Image.objects.all().order_by('-id')[:5]
        print(f"{len(images)}")
        if len(images) == 0:
            raise serializers.ValidationError("No images found for the given topic.")

        image_files = [img.image_url for img in images]

        # Assuming 'create_video_from_images' accepts a list of image filenames
        video_file_path = create_video_from_images(image_files, video_title)
        print(f"{video_file_path}")
        # Save the video metadata to the database
        video = Video.objects.create(
            title=video_title,
            description=description,
            length_seconds=len(images) * 2,  # Assuming each image represents 2 seconds of video
            topic=topic,
            video_file=video_file_path
        )

        return video

    # def validate(self, data):
    #     # Check if there are at least 5 images for the topic
    #     if Image.objects.filter(video__topic=data['topic']).count() < 5:
    #         raise serializers.ValidationError("There are fewer than 5 images available for the given topic.")
    #     return data