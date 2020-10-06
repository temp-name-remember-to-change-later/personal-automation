#!/usr/bin/env python3
import praw
import sys
import getopt

reddit = praw.Reddit(site_name='DEFAULT')

def print_titles(sub, n):
    for submission in reddit.subreddit(sub).new(limit=n):
        print(submission.title)

def print_selftexts(sub, n):
    for submission in reddit.subreddit(sub).new(limit=n):
        print(submission.selftext)

def print_comments(sub, n): # copy/pasted from praw 
    for submission in reddit.subreddit(sub).new(limit=n):
        submission.comments.replace_more(limit=None)
        comment_queue = submission.comments[:] 
        while comment_queue:
            comment = comment_queue.pop(0)
            print(comment.body)
            comment_queue.extend(comment.replies)

def main(argv):
    title = False
    body = False
    comments = False
    subreddit = ''
    n = 0
    try:
        opts, args = getopt.getopt(argv, "htbcs:n:", ['title', 'titles', 'selftext', 'body', 'comments', 'sub=', 'subreddit='])
    except getopt.GetoptError:
        print('usage: scoopreddit.py -[tbc] -s <subreddit> -n <number>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('usage: scoopreddit.py -[t/b/c] -s <subreddit> -n <number>')
            sys.exit()
        elif opt in ['-t', '--title', '--titles']:
            title = True
        elif opt in ['-b', '--body']:
            body = True
        elif opt in ['-c', '--comments']:
            comments = True
        elif opt in ['-s', '--sub', '--subreddit']:
            subreddit = arg
        elif opt == '-n':
            n = int(arg)

    if subreddit == '' or n == 0 or (title and body) or (body and comments) or (title and comments) or (not title and not body and not comments):
        print('usage: scoopreddit.py -[t/b/c] -s <subreddit> -n <number>')
        sys.exit(2)

    if title: 
        print_titles(subreddit, n)
    elif body: 
        print_selftexts(subreddit, n)
    elif comments: 
        print_comments(subreddit, n)

if __name__ == '__main__':
    main(sys.argv[1:])