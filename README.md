# Travel image downloader

Downloads all images from the Travel all time subreddit into a picture directory.
Currently classifies country of the picture by checking top comments of the post and matching for country by most mentions

## Usage
1. Create virtualenv and download dependencies
```
virtualenv venv -p python3
source venv/bin/activate
pip install -r requirements.txt
```

You need to register for a Reddit Client ID and Secret. 

```
CLIENT_ID='YOUR CLIENT ID' CLIENT_SECRET='YOUR CLIENT SECRET' python app.py <# of pics> [--hot]
```

TODO
1. Take output directory from args
2. Choose between Hot or Top 
3. Organize images by country accurately (difficult)
4. Add directory clean option
5. Don't download repeats

Questions
How to classify image by country from title