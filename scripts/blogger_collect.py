"""
This script will collect the contents of a specified Blogger or Blogspot
blog.  Specify which blog you would like to collect from and how many
posts you would like to collect from that blog in the accompanying
config file, found in the same directory as the collection script.
"""

# requests is the package we're goign to use to query the Blogger api
# json is the package we're going to use to create and manipulate JSON objects
# ConfigParser allows the script to read the configuration file
import requests
import json
from configparser import SafeConfigParser

# gets your configuration settings from the config file
config = SafeConfigParser()
config.read('../settings.cfg')
API_KEY = config.get('keys', 'api_key')
BLOG_ID = config.get('keys', 'blog_id')
MAX_POSTS = config.get('settings', 'max_posts')
MAX_COMMENTS = config.get('settings', 'max_comments')

# parameters to be passed to the GET request for posts
posts_payload = {'maxResults': MAX_POSTS, 'key': API_KEY}

# GET all posts up to maxposts value
posts = requests.get(
    'https://www.googleapis.com/blogger/v3/blogs/{}/posts?'
    .format(BLOG_ID), params=posts_payload)

# saves body to json object
jsonposts = posts.json()

print(posts)
print(len(jsonposts['items']))
print(posts.url)

# parameters to be passed to the GET request for comments
comments_payload = {'maxResults': MAX_COMMENTS, 'key': API_KEY}


# for each post in the json object, get the post's ID
# if the post has replies, get the replies and add them to the json object
for post in jsonposts['items']:
    postID = post['id']
    try:
        comments = requests.get(
            'https://www.googleapis.com/blogger/v3/blogs/{}/posts/{}/comments?'
            .format(BLOG_ID, postID), params=comments_payload)

        # for debugging, update later to be better status indicator
        print(comments)
        contents = comments.json()
        post['replies_body'] = contents['items']
    except:
        print("no comments found")

# saves the json object to a file
with open('../data/raw.json', 'w') as outfile:
    json.dump(jsonposts, outfile)

outfile.close()
