#!/usr/bin/env python3
import praw
import sys

# Returns all content from a given user

reddit = praw.Reddit(site_name='DEFAULT')

def get_redditor(username):
    return praw.models.Redditor(reddit, sys.argv[1])

def exists(user):
    try:
        user.comment_karma
        return True
    except:
        return False

def get_posts(user):
    return user.new(limit=None)

def print_usage():
    print('usage: userdump.py <username>')

def main():
    if len(sys.argv) != 2:
        print_usage()
        exit(2)
    
    username = sys.argv[1]
    user = get_redditor(username)
    if exists(user):
        posts = get_posts(user)
        for post in posts:
            print('[{}]'.format(post.permalink))
            if type(post) is praw.models.Submission:
                print(post.title)
                print(post.selftext)
                print()
            elif type(post) is praw.models.Comment:
                print(post.body)
                print()
    else:
        print('User {} does not exist, is shadowbanned, or somehow has no karma score.'.format(username))

if __name__ == '__main__':
    main()