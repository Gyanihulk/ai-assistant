import logging
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from video_generator.models.image import Image
from video_generator.serializers.image import ImageSerializer

logger = logging.getLogger(__name__)

@api_view(['GET', 'POST'])
def image_list(request):
    if request.method == 'GET':
        images = Image.objects.all()
        serializer = ImageSerializer(images, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info(f"Image created successfully: {serializer.data['id']}")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            logger.error(f"Error during image creation: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
