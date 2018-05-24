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

def main():
    # How many pictures to download
    pic_count = 15

    if len(sys.argv) == 2:
        pic_count = sys.argv[1]

    # Create picture directory
    picture_dir = os.path.join(os.getcwd(), 'pics')

    if not os.path.exists(picture_dir):
        os.makedirs(picture_dir)

    for submission in travel_subreddit.hot(limit=pic_count):
        # TODO: handle imgur links 
        # Only download jpg
        if submission.url.endswith('.jpg'):
            words = nltk.word_tokenize(submission.title)
            space_separated_title = ' '.join(words)

            print("{}".format(space_separated_title))
            places = geograpy.get_place_context(text=space_separated_title)
            print(places.countries, places.country_mentions)

            underscored_title = space_separated_title.replace(' ', '_')

            title = re.sub(r'\W+', '', underscored_title) + '.jpg'
            filepath = os.path.join(picture_dir, title)

            # save_image(filepath, submission.url)

if __name__ == "__main__":
    sys.exit(main())
