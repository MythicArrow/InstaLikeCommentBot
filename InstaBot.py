# Importing libraries
from instagrapi import Client
import openai

# Get OpenAI API key and token size from user input
# Find yours on OpenAI's website
openai.api_key = input("Enter your OpenAI API key: ")
max_tokens = int(input("Enter the maximum token size for comments (e.g., 20): "))

# Get Instagram credentials from user input
INSTAGRAM_USER = input("Enter your Instagram user id: ")
INSTAGRAM_PASSWORD = input("Enter your Instagram password: ")

# Initialize Instagram client and log in
client = Client()
client.login(INSTAGRAM_USER, INSTAGRAM_PASSWORD)

# Define hashtags
hashtag = "#instagram, #instagood, #love, #like, #photography, #follow, #instadaily, #photooftheday, #instalike, #fashion, #likeforlikes, #picoftheday, #beautiful, #followforfollowback, #insta, #trending, #art, #india, #bhfyp, #photo, #viral, #likes, #explore, #nature, #style, #happy, #followme, #explorepage, #model, #travel"

# Function to generate comments using OpenAI API
def generate_comment(media_caption, prompt):
    """Generate a comment using OpenAI API based on media caption."""
    complete_prompt = f"{prompt} '{media_caption}'"
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Choose the appropriate model
        messages=[{"role": "user", "content": complete_prompt}],
        max_tokens=max_tokens  # Use user-defined max tokens
    )
    
    comment = response.choices[0].message['content'].strip()
    return comment

# Get custom prompt for comments from the user
comment_prompt = input("Enter a custom prompt for generating comments (e.g., 'Write a funny comment for an Instagram post with this caption:'): ")

# Fetching media for the hashtag
medias = client.hashtag_medias_recent(hashtag, 20)

for i, media in enumerate(medias):
    # Liking the post
    client.media_like(media.id)
    print(f"Liked post number {i + 1} with hashtag {hashtag}")

    # Follow the user every 5 posts
    if i % 5 == 0:
        client.user_follow(media.user.pk)
        print(f"Followed user {media.user.username}")

        # Generate a comment based on the media's caption
        comment = generate_comment(media.caption, comment_prompt)
        client.media_comment(media.id, comment)
        print(f"Commented '{comment}' under post number {i + 1}")
