#!/usr/bin/python
import praw
from praw.exceptions import APIException
import re
import os
import time


def main():
    reddit = praw.Reddit('NoMobileArticlesBot')

    if not os.path.isfile('posts_replied_to.txt'):
        posts_replied_to = []

    else:
        # Read the file into a list and remove any empty values
        with open('posts_replied_to.txt', 'r') as f:
            posts_replied_to = f.read()
            posts_replied_to = posts_replied_to.split('\n')
            posts_replied_to = list(filter(None, posts_replied_to))

    subreddit = reddit.subreddit('wikipedia')
    for submission in subreddit.hot(limit=100):
        print(submission.title, submission.id, submission.url)

        if submission.url.startswith('https://en.m.wikipedia.org/') and \
           (submission.id not in posts_replied_to):
            slug = submission.url.split('/')[-1]
            main_url = 'https://en.wikipedia.org/wiki/{}'.format(slug)
            print('Bot replying to: ', submission.title)
            try:
                submission.reply(
                    'Hi. You linked to the mobile version of this ' +
                    'article. The main one is at: ' + main_url)
            except APIException:
                print('hit rate limit, waiting 10 minutes.')
                time.sleep(600)
                submission.reply(
                    'Hi. You linked to the mobile version of this ' +
                    'article. The main one is at: ' + main_url)

            posts_replied_to.append(submission.id)
            # Write our updated list back to the file
            with open('posts_replied_to.txt', 'w') as f:
                for post_id in posts_replied_to:
                    f.write(post_id + '\n')

            time.sleep(60)

    print('waiting 10 hours')
    time.sleep(36000)

if __name__ == '__main__':
    while True:
        main()
