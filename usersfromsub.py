#!/usr/bin/env python3
import praw
import sys

# Returns a list of users who posted or commented in the current top [number] posts on a given subreddit

reddit = praw.Reddit(site_name='DEFAULT')

def get_users(sub, n): # this section copy/pasted from praw manual, with slight modifications
    users = []
    for submission in reddit.subreddit(sub).hot(limit=n):
        if submission.stickied:
            continue
        users.append(submission.author)
        submission.comments.replace_more(limit=None)
        comment_queue = submission.comments[:] 
        while comment_queue:
            comment = comment_queue.pop(0)
            users.append(comment.author)
            comment_queue.extend(comment.replies)

    unique_users = []
    for user in users:
        if user not in unique_users:
            unique_users.append(user)
    return unique_users

def print_usage():
    print('usage: usersfromsub.py <subreddit> [number]')

def main():
    if len(sys.argv) not in [2, 3]:
        print_usage()
        exit(2)
    n = 10
    if len(sys.argv) == 3:
        try:
            n = int(sys.argv[2])
        except:
            print_usage()
            exit(2)
    subname = sys.argv[1]
    users = get_users(subname, n)
    for user in users:
        try:
            print(user.name)
        except:
            print(user)

if __name__ == '__main__':
    main()