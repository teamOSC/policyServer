import twitter

api = twitter.Api(consumer_key='2RJYLeeXVWftefdtvkKwIO7Wl', 
                  consumer_secret='3aZefjttWKg5ONDN4Zk6B2fmuCO1i5EZMmsuQf1bTHcA8QJr3Q',
                  access_token_key='136962040-numg6UfhgDhJCLyF1zLoIohN7xqik6DStR0nHNUO',
                  access_token_secret='ofTjnhSaKLxY5s8cPI5gI13xPfnVRCNItc8yIJ4ZjgTTP')

def fetchTweet(user):
    numbers = 10
    statuses = api.GetUserTimeline(screen_name = user, count = numbers)

    '''tweet = ""
    for s in statuses:
        tweet = tweet + s.text
    return tweet'''

    return statuses