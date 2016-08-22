# blogger_scraper

###Step 1

First, open `settings.cfg` in a text editor.  Fill in information for each value.  You'll need to get an API Key from Google (instructions on how to do this will be added here later).  For `max_posts` and `max_comments`, enter an integer no larger than 500.

###Step 2

Use the included `environment.yml` file to create an anaconda environment, then run each of the three scripts in the following order:
1. blogger_collect.py (retrieves data based on parameters specified in `settings.cfg` 
2. blogger_parse.py (gets the data you probably want out of the raw data dump)
3. blogger_toCSV.py (exports the parsed data to a human-readable spreadsheet)
