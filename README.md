# xpostbot
A framework for a reddit bot which scrapes new posts in one subreddit and reposts them to another under certain circumstances

## Customising

Copy `client_info.json_EXAMPLE` to `client_info.json` and fill it in using the steps [here](http://praw.readthedocs.io/en/latest/pages/oauth.html#a-step-by-step-oauth-guide).

Copy `config.json_EXAMPLE` to `config.json` and fill it in as you see fit. The bot will look for new submissions in `source_subreddit`, check if the submission title is a complete match for the regex in `filter`, and if so, cross-post it to `target_subreddit`.

## Usage

`python bot.py`

If it's your first time running the bot (and assuming the config files are filled in correctly), a web page will open asking you to allow it to use your account. Click 'Allow'. 

## Other notes

Only run this bot on hardware you control, as it requires some secret information to be stored in insecure text or pickle files.
