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
BLOG_URL = config.get('keys', 'blog_url')
BLOG_URL = '{}{}'.format('https%3A%2F%2F', BLOG_URL)
# print(BLOG_URL)
# BLOG_URL = urlib2.quote_plus('https://googleblog.blogspot.com/')
MAX_POSTS = config.get('settings', 'max_posts')
MAX_COMMENTS = config.get('settings', 'max_comments')

# parameters passed to the GET request used to get the blog's ID
first_payload = {'key': API_KEY}

# a hacky way to do this, but it works for now
r = requests.get('https://www.googleapis.com/blogger/v3/blogs/byurl?url={}%2F&key={}'
                 .format(BLOG_URL, API_KEY))

json_getID = r.json()
BLOG_ID = json_getID['id']

print(BLOG_ID)

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
