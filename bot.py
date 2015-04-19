#!/usr/bin/env python

import logging
import json
import tweepy
import sys
from random import randint
import urllib
import datetime
import os
import json
import requests
import time



class Bot():
    def __init__(self):
        self.consumer_key = "RvuAcphYmyxFTDHcjx6uVGkXI"
        self.consumer_secret = "b9KoTuJfykWLxbOPEoYwVrTUhLSJ7ilT4Fa68KvWofZhiJ7Pyp"
        self.access_token = "3163520989-78cV3Z3on4GYZDgCT5yh54Ps9MVeykDZxX1JUvo"
        self.access_token_secret = "QxTQdsvVzKZovroViovrtNXwGc2p3dlkdyhsf25eIaoo7"
        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.access_token, self.access_token_secret)
        self.api = tweepy.API(auth)


def pushTwitter(media,text=''):
    b = Bot()
    api = b.api
    t = api.update_with_media(media, status=text)


if __name__ == '__main__':
    pushTwitter(media)