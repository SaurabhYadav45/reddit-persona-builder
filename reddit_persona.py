import praw
import re
from datetime import datetime, timezone
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize Reddit API client
reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent=os.getenv("REDDIT_USER_AGENT")
)

# Initialize OpenAI client
openai_client = OpenAI(api_key = os.getenv("OPENAI_API_KEY"))

# Function to extract username from reddit profile url
def extract_username(url):
    """Extract Reddit username from a profile URL.

    Args:
        url (str): Reddit user profile URL (e.g., 'https://www.reddit.com/user/kojied/').

    Returns:
        str: The extracted username.

    Raises:
        ValueError: If the URL is invalid.
    """
    pattern = r"https://www\.reddit\.com/user/([A-Za-z0-9_-]+)/?"
    match = re.match(pattern, url)
    if not match:
        raise ValueError("Invalid Reddit profile URL")
    print("Something:", match.group(1))
    return match.group(1)


# function to scrape user posts and comments
def scrape_user_data(username):
    """Scrape posts and comments for the given Reddit user.

    Args:
        username (str): Reddit username.

    Returns:
        tuple: List of posts and list of comments, each as dictionaries with id, title/body, subreddit, and created time.
    """
    user = reddit.redditor(username)
    posts = []
    comments = []

    # Scrape up to 100 posts
    for submission in user.submissions.new(limit=20):
        posts.append({
            "id": submission.id,
            "title": submission.title,
            "body": submission.selftext[:500] if submission.selftext else '',
            "subreddit": submission.subreddit.display_name,
            "created": datetime.fromtimestamp(submission.created_utc)
        })

    # Scrape up to 100 comments
    for comment in user.comments.new(limit=10):
        comments.append({
            "id": comment.id,
            "body": comment.body[:500] if comment.body else '',
            "subreddit": comment.submission.subreddit.display_name,
            "created": datetime.fromtimestamp(comment.created_utc)
        })
    # print("\nPost:", posts[0])
    # print("\nComment:", comments[0])
    return posts, comments

# function to generate user persona based on posts and comments
def generate_persona(posts, comments):
    """Generate user persona using an LLM, with citations using Post IDs and Comment IDs.

    Args:
        posts (list): List of post dictionaries with id, title, body, subreddit.
        comments (list): List of comment dictionaries with id, body, subreddit.

    Returns:
        str: Formatted persona in markdown with citations.
    """

    # Format the content with IDs for proper citation
    context = "## User Posts:\n"
    for post in posts[:20]:  # Limit to avoid token limits
        context += (
            f"Post ID: {post['id']}\n"
            f"Subreddit: {post['subreddit']}\n"
            f"Title: {post['title']}\n"
            f"Body: {post['body']}\n\n"
        )

    context += "## User Comments:\n"
    for comment in comments[:10]:
        context += (
            f"Comment ID: {comment['id']}\n"
            f"Subreddit: {comment['subreddit']}\n"
            f"Comment: {comment['body']}\n\n"
        )

    # Persona prompt with clear instruction to cite the ID
    prompt = f"""
You are an AI assistant that builds user personas from Reddit data.

Based on the following Reddit user's activity, generate a detailed user persona using at least 5 distinct characteristics, grouped under these markdown headings:

- ## Interests
- ## Personality Traits
- ## Demographics (if inferable)
- ## Location (if inferable)
- ## Hobbies
- ## Behavioural
- ## Frustrations or Beliefs

Instructions:
1. Use only the provided content to generate insights. Do not infer anything not clearly supported by the user's post or comment content.

2. For **each point**, include the source **(Post ID: xxx)** or **(Comment ID: yyy)** that supports your inference. 
Only use the actual Post IDs or Comment IDs already provided. Do NOT guess or write "XXX".

Example:
- Enjoys open-world games: Frequently discusses Skyrim strategies (Comment ID: abcd123).

Reddit User Activity:
{context}
"""

    # Call the LLM
    response = openai_client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=1500
    )

    return response.choices[0].message.content



# Save persona function
def format_account_age(created_datetime):
    """Returns account age in years."""
    now = datetime.now(timezone.utc)
    delta = now - created_datetime
    return f"{delta.days // 365} years"

# Function to format and save the user person
def save_persona(username, persona, created_datetime):
    """Save the persona to a well-structured .txt file inside 'sample' folder.

    Args:
        username (str): Reddit username.
        persona (str): LLM-generated markdown content.
        created_datetime (datetime): User's account creation time.

    Returns:
        str: Filename of the saved persona.
    """
    folder = "sample"
    os.makedirs(folder, exist_ok=True)
    account_age = format_account_age(created_datetime)

    header = f"""
**Username:** {username}   
**Account Age:** {account_age}  

"""

    footer = f"""---

*Persona generated from publicly available Reddit comments and posts.*
All statements are AI-inferred and cite specific Post or Comment IDs.
"""
    full_content = header + persona.strip() + "\n\n" + footer

    # Construct full file path inside 'sample/' folder
    filename = os.path.join(folder, f"{username}_persona.txt")

    with open(filename, "w", encoding="utf-8") as f:
        f.write(full_content)

    print(f"[✔] Persona saved to: {filename}")
    return filename
