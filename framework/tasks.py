import pinboard
from math import floor
import random
import time, datetime
import gmail
from framework.celery.celery import celery

# Secret:
pinboard_token = 'username:token'
gmail_username = "yourusername@gmail.com"
gmail_password = "yourpassword"
to_who = "yourusername_or_other@whatever.com"

@celery.task
def fetch_pinboard():
    # create pinboard connection (using username/password)
    d = pinboard.open(token=pinboard_token)
    dates = d.dates()
    nb_dates = len(dates)
    posts = []

    text = "<h2>Pinboard 10 random picked links:</h2><br/>"

    while(len(posts) < 10):
        nb_random_date = int(floor(random.random() * nb_dates))
        random_date = dates[nb_random_date:nb_random_date+1][0]["date"]
        all_posts = d.posts(date=random_date)
        random_int = int(floor(random.random() * len(all_posts)))

        post = all_posts[random_int]
        posts.append(post)

        t = time.mktime(post['time_parsed'])
        text += '<p style="font-size:80%; color: #666;margin-bottom: 0px;">' + time.strftime("%Y-%m-%d", time.localtime(t)) + "</p>"
        text += '<p style="margin-bottom: 0px;">'+post["description"]+"</p>"
        text += '<a href="' + post["href"] +'">' + post["href"] + "</a>" + "<br/><hr/><br/>"

    text += "<br/>"

    gm = gmail.GMail(gmail_username,gmail_password)
    msg = gmail.Message('Today 10 random links', to=to_who,html=text)
    gm.send(msg)