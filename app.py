import praw
import geograpy
import requests
import re
import nltk

import sys
import os.path

nltk.download('maxent_ne_chunker')
nltk.download('words')

CLIENT_ID = os.environ['CLIENT_ID']
CLIENT_SECRET = os.environ['CLIENT_SECRET']

reddit = praw.Reddit(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    user_agent='travel image downloader by /u/makingausernamehard')

travel_subreddit = reddit.subreddit('travel')

def save_image(filepath, url):
    with open(filepath, 'wb') as handle:
        response = requests.get(url, stream=True)

        if not response.ok:
            print(response)

        for block in response.iter_content(1024):
            if not block:
                break

            handle.write(block)

        print("File {} created".format(filepath))

def create_dir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)

def main():
    # How many pictures to download
    pic_count = 15

    if len(sys.argv) >= 2:
        pic_count = int(sys.argv[1])

    # Create picture directory
    picture_dir = os.path.join(os.getcwd(), 'pics')
    create_dir(picture_dir)

    # Create unknown location directory
    unknown_location_dir = os.path.join(picture_dir, 'unknown')
    create_dir(unknown_location_dir)

    listing = travel_subreddit.top(limit=pic_count)

    if len(sys.argv) >= 3 and sys.argv[2] == "--hot":
        listing = travel_subreddit.hot(limit=pic_count)

    # Preprocess list (remove all non image posts)

    for submission in listing:
        # TODO: handle imgur links 
        # Only download jpg
        if submission.url.endswith('.jpg'):
            # Combine all comments into one text to search for correct country
            search_str = ""

            # Get all top level comments and add to search string
            for comment in list(submission.comments):
                if hasattr(comment, 'body'):
                    search_str += comment.body

            places = geograpy.get_place_context(text=search_str)
            
            if places.countries:
                # Get the country with the highest mentions 
                country = max(places.country_mentions, key=lambda item:item[1])[0]

                country_dir = os.path.join(picture_dir, country)

                create_dir(country_dir)
            else:
                country = "unknown"

            # Clean up title for filename
            words = nltk.word_tokenize(submission.title)
            space_separated_title = ' '.join(words)
            underscored_title = space_separated_title.replace(' ', '_')

            title = re.sub(r'\W+', '', underscored_title) + '.jpg'
            filepath = os.path.join(picture_dir, country, title)

            save_image(filepath, submission.url)

if __name__ == "__main__":
    sys.exit(main())
