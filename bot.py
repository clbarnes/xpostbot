import praw
import re
import json
import webbrowser
import pickle
import time

POST_DELAY = 10  # seconds
CONFIG_PATH = 'config.json'
DONE_PATH = 'done.txt'
CLIENT_INFO_PATH = 'client_info.json'
ACCESS_INFO_PATH = 'access_information.pickle'


with open('config.json') as f:
    config = json.load(f)


def main():
    reddit = setup_reddit()
    done = get_done()
    new_done = set()

    filter_re = re.compile(config['filter'])

    for submission in get_new_submissions(reddit, config['source_subreddit']):
        if submission.id in done:
            continue

        if filter_re.match(submission.title):
            make_repost(reddit, config['target_subreddit'], submission)
            time.sleep(POST_DELAY)

        new_done.add(submission.id)

    with open('done.txt', 'w') as f:
        f.write('\n'.join(sorted(new_done)))

def setup_reddit():
    r = praw.Reddit(config['user_agent'])

    with open('client_info.json') as f:
        client_info = json.load(f)

    r.set_oauth_app_info(**client_info)

    r.set_access_credentials(**get_access_information(r))

    return r


def get_access_information(reddit):
    try:
        with open('access_information.pickle', 'rb') as f:
            refresh_token = pickle.load(f)['refresh_token']

        access_information = reddit.refresh_access_information(refresh_token)
    except FileNotFoundError:
        url = reddit.get_authorize_url(config['user_agent'], 'identity submit read', True)
        webbrowser.open(url)

        access_code = input('Enter access code from URL: ')

        access_information = reddit.get_access_information(access_code)

    with open('access_information.pickle', 'wb') as f:
        pickle.dump(access_information, f)

    return access_information


def get_done():
    try:
        with open('done.txt') as f:
            return set(line.strip() for line in f.readlines())
    except FileNotFoundError:
        return set()


def get_new_submissions(reddit, subreddit, count=30):
    subreddit = reddit.get_subreddit(subreddit)
    yield from subreddit.get_new(limit=count)


def make_repost(reddit, tgt_subreddit, submission):
    new_post = reddit.submit(
        tgt_subreddit,
        submission.title + ' (x-post from /r/{})'.format(submission.subreddit.display_name),
        url=submission.permalink
    )

    new_post.add_comment('Original post by /u/{}'.format(submission.author))


if __name__ == '__main__':
    main()
