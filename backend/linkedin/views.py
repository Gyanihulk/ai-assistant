from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import SuggestionSerializer
from .enums import SuggestionItemEnum
from .services.prompt_generation import generate_prompts,generate_comment,analyze_post_data,suggest_reply
import logging
from .models import AnalyzedPost
logger = logging.getLogger(__name__)
@api_view(['POST'])
def generate_suggestion(request):
    serializer = SuggestionSerializer(data=request.data)
    if serializer.is_valid():
        suggestion_item = serializer.validated_data['suggestion_item']
        content = serializer.validated_data['content']

        # Call the service function to generate the suggestion
        generated_suggestion = generate_prompts(suggestion_item, content)

        return Response({
            "message": "Suggestion generated successfully",
            "data": {
                "suggestion_item": suggestion_item,
                "content": content,
                "generated_suggestion": generated_suggestion
            }
        }, status=status.HTTP_201_CREATED)
    else:
        available_choices = [item.value for item in SuggestionItemEnum]
        return Response({
            "errors": serializer.errors,
            "available_choices": available_choices
        }, status=status.HTTP_400_BAD_REQUEST)
        



@api_view(['POST'])
def generate_suggested_reply(request):
    """
    API to generate a suggested reply for a LinkedIn conversation.

    Expected JSON body:
    {
        "conversation": [
            {
                "name": "User Name",
                "message": "Message text"
            },
            ...
        ]
    }
    """
    # Get the conversation from the request body
    conversation = request.data.get('conversation', [])

    # Validate input
    if not conversation or not isinstance(conversation, list):
        return Response(
            {"error": "Conversation must be a list of messages."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        # Generate the suggested reply
        suggested_reply = suggest_reply(conversation)

        # Return the generated reply
        return Response(
            {
                "message": "Suggested reply generated successfully.",
                "suggested_reply": suggested_reply,
            },
            status=status.HTTP_200_OK,
        )

    except Exception as e:
        return Response(
            {"error": f"Error generating suggested reply: {e}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

@api_view(['POST'])
def generate_post_comment(request):
    """
    API to generate a comment for a LinkedIn post.

    Expected JSON body:
    {
        "postContent": "Content of the LinkedIn post",
        "existingComments": [
            {
                "commentText": "Existing comment text",
                "userName": "User Name",
                "userProfileURL": "https://www.linkedin.com/in/username",
                "dataId": "data-id"
            },
            ...
        ]
    }
    """
    post_content = request.data.get('postContent')
    existing_comments = request.data.get('existingComments', [])

    if not post_content:
        return Response(
            {"error": "Post content is required."},
            status=status.HTTP_400_BAD_REQUEST,
        )


    # Generate the comment using the service function
    generated_comment = generate_comment(post_content, existing_comments)

    return Response(
        {
            "message": "Comment generated successfully.",
            "generated_comment": generated_comment,
        },
        status=status.HTTP_200_OK,
    )
    
    
@api_view(['POST'])
def analyze_post(request):
    """
    API to analyze a LinkedIn post, categorize it, and generate a comment.

    Expected JSON body:
    {
        "postId": "urn:li:activity:7284150165433720832",
        "url": "https://www.linkedin.com/in/aryan-mittal-0077?miniProfileUrn=...",
        "name": "Aryan Mittal",
        "content": "Post content",
        "reactions": {
            "likes": "335",
            "comments": "7 comments",
            "shares": "0"
        },
        "mediaUrl": null,
        "comments": [
            {
                "commentText": "Existing comment text",
                "userName": "User Name",
                "userProfileURL": "https://www.linkedin.com/in/username",
                "dataId": "data-id"
            },
            ...
        ]
    }
    """
    post_data = request.data

    # Validate required fields
    if not all(key in post_data for key in ["postId", "content", "comments"]):
        return Response(
            {"error": "postId, content, and comments are required fields."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Extract post details
    post_id = post_data["postId"]
    content = post_data["content"]
    comments = post_data.get("comments", [])
    logger.info("starting analysing post postId",post_data)
    # Analyze the post using the service function
    analyzed_data = analyze_post_data(content, comments)
    logger.info("Analyzed post in view: %s", analyzed_data)

 # Save the analyzed data into the database
    post_instance, created = AnalyzedPost.objects.update_or_create(
        post_id=post_id,
        defaults={
            "url": post_data.get("url"),
            "name": post_data.get("name"),
            "content": content,
            "reactions": post_data.get("reactions", {}),
            "media_url": post_data.get("mediaUrl"),
            "comments": comments,
            "categories": analyzed_data["categories"],
            "analysis": analyzed_data["analysis"],
            "generated_comment": analyzed_data["generated_comment"],
        },
    )

    if created:
        logger.info("New post saved to the database: %s", post_id)
    else:
        logger.info("Existing post updated in the database: %s", post_id)

    # Combine analyzed data with the input post details
    response_data = {
        "postId": post_id,
        "url": post_instance.url,
        "name": post_instance.name,
        "content": post_instance.content,
        "reactions": post_instance.reactions,
        "mediaUrl": post_instance.media_url,
        "comments": post_instance.comments,
        "analyzed": {
            "categories": post_instance.categories,
            "analysis": post_instance.analysis,
            "generated_comment": post_instance.generated_comment,
        },
    }



    return Response(
        {
            "message": "Post analyzed successfully.",
            "data": response_data,
        },
        status=status.HTTP_200_OK,
    )

