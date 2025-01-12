import openai
import os

openai_api_key = os.getenv("OPENAI_API_KEY")
# Load the OpenAI API key
if not openai_api_key:
    raise ValueError("OPENAI_API_KEY environment variable is not set.")
openai.api_key = openai_api_key


def generate_prompts(suggestion_item, content):
    """
    Generates personalized LinkedIn suggestions based on the suggestion type and content.

    Parameters:
        suggestion_item (str): Type of suggestion (e.g., post, comment, message, reply).
        content (str): Main content or idea for the suggestion.

    Returns:
        str: Generated LinkedIn suggestion.
    """
    print(f"Generating LinkedIn suggestion for: {suggestion_item}, Content: {content}")

    # Personal and professional details for personalization
    personal_details = """
    Adamya Kumar
    Portfolio | kumar.adamya2000@gmail.com | +91 7017368626 | Github | Linkedin
    EDUCATION
    - IIIT BANGALORE & UPGRAD: Post Graduate Diploma in Data Science
      (Jun 2021 – Dec 2021 | Bangalore, India)
    - GURUKUL KANGRI HARIDWAR: Masters in Business Administration | Finance
      (May 2019 – Apr 2021 | Haridwar, India)
    - GURUKUL KANGRI HARIDWAR: Bachelors of Technology | Computer Science
      (Jun 2015 – Apr 2019 | Haridwar, India)
    PROFESSIONAL EXPERIENCE
    - APPFOSTER: Software Engineer II (Apr 2022 – Present | Noida, India)
      Highlights: Built a Chrome extension integrated with LinkedIn, engineered HR SaaS applications, improved real-time interactions by 40%.
    - CAPLINE SERVICES: Associate (Aug 2021 – Apr 2022 | Noida, India)
    - ITDA: Training Desk Analyst (Jan 2021 – May 2021 | Dehradun, India)
    SKILLS
    - Languages: JavaScript, Python, PHP
    - Frameworks: React, Node.js, GraphQL, Laravel
    - Databases: PostgreSQL, MongoDB
    - Cloud: AWS, Azure
    """

    try:
        # Generate the suggestion using OpenAI API
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a LinkedIn assistant and a professional copywriter."},
                {
                    "role": "user",
                    "content": f"""
                            Generate a {suggestion_item} tailored for LinkedIn. 
                            The content should highlight achievements, skills, or projects of Adamya Kumar. 
                            The topic is: {content}.
                            Use the following details for personalization:
                            {personal_details}
                            """
                },
            ],
        )
        # Extract and return the generated suggestion
        suggestion = response.choices[0].message.content.strip()
        print(f"Generated Suggestion: {suggestion}")
        return suggestion

    except Exception as e:
        print(f"Error generating suggestion: {e}")
        return "Error generating suggestion. Please try again."


def generate_comment(post_content, existing_comments, max_length=150):
    """
    Generates a small comment related to the post content and existing comments.

    Parameters:
        post_content (str): The main content of the post.
        existing_comments (list): List of existing comments.
        max_length (int): Maximum character length for the generated comment.
    Returns:
        str: Generated comment for the post.
    """
    try:
        # Combine existing comments for context
        comments_context = "\n".join(
            [f"Comment: {comment['commentText']}" for comment in existing_comments]
        )

        # OpenAI API call to generate a comment
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a professional LinkedIn assistant."},
                {
                    "role": "user",
                    "content": f"""
Generate a small comment for a LinkedIn post based on the following data:
Post Content:
{post_content}

Existing Comments:
{comments_context}

The comment should be engaging, professional, and limited to {max_length} characters.
"""
                },
            ],
        )

        # Extract the generated comment
        generated_comment = response.choices[0].message.content.strip()
        print(f"Generated Comment: {generated_comment}")
        return generated_comment

    except Exception as e:
        print(f"Error generating comment: {e}")
        return "Error generating comment. Please try again."

def analyze_post_data(post_content, existing_comments, max_length=150):
    """
    Analyzes a LinkedIn post, categorizes it, and generates a comment.

    Parameters:
        post_content (str): The main content of the post.
        existing_comments (list): List of existing comments.
        max_length (int): Maximum character length for the generated comment.

    Returns:
        dict: Analyzed data including categories and a generated comment.
    """
    try:
        # Prepare comments context for the analysis
        comments_context = "\n".join(
            [f"Comment: {comment['commentText']}" for comment in existing_comments]
        )

        # Use OpenAI API to analyze the post and generate data
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a professional LinkedIn post analyzer."},
                {
                    "role": "user",
                    "content": f"""
Analyze the following LinkedIn post content and existing comments:
Post Content:
{post_content}

Existing Comments:
{comments_context}

Provide:
1. Categories for the post (e.g., professional, inspirational, technical).
2. A short, engaging comment limited to {max_length} characters.
Output the result as a JSON object.
"""
                },
            ],
        )


        # Parse the API response
        result = response.choices[0].message.content.strip()
        print(f"chatgpr response {result}")

        # Convert JSON string to dictionary and normalize keys
        parsed_result = eval(result)
        return {
            "categories": parsed_result.get("Post Categories", []),
            "analysis": parsed_result.get("Analysis", {}),
            "generated_comment": parsed_result.get("Suggested Comment", "No comment generated."),
        }

    except Exception as e:
        print(f"Error analyzing post: {e}")
        return {
            "categories": ["Error"],
            "generated_comment": "Error generating comment. Please try again.",
        }

