from reddit_persona import extract_username, scrape_user_data, generate_persona, save_persona, reddit
from datetime import datetime, timezone

# Main function
def main():
    """Main function to process Reddit user profile and generate persona."""
    urls = [
        "https://www.reddit.com/user/kojied/",
        # "https://www.reddit.com/user/Hungry-Move-6603/"
    ]

    for url in urls:
        try:
            # get the username 
            username = extract_username(url)
            print(f"Processing user: {username}")
            # get the posts and comments to that username
            posts, comments = scrape_user_data(username)
            # generate persona based on posts and comments
            persona = generate_persona(posts, comments)
            # save the persona in a text file
            user_created_utc = reddit.redditor(username).created_utc
            created_datetime = datetime.fromtimestamp(user_created_utc, tz=timezone.utc)

            filename = save_persona(username, persona, created_datetime)
            print(f"Persona saved to {filename}")
            # print("final persona response:\n",persona)
        except Exception as e:
            print(f"Error processing {url}: {str(e)}")

if __name__ == "__main__":
    main()