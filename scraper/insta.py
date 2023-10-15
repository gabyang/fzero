from instagrapi import Client
import os
from dotenv import load_dotenv
import pandas as pd
import json

load_dotenv()

acc = os.getenv('ACCOUNT_USERNAME')
password = os.getenv('ACCOUNT_PASSWORD')
cl = Client()
print(acc, password)
# cl.login(acc, password)

# cl.dump_settings("session.json")


########################################################################################################################

from instagrapi.exceptions import LoginRequired
import logging

logger = logging.getLogger()

def login_user():
    """
    Attempts to login to Instagram using either the provided session information
    or the provided username and password.
    """

    session = cl.load_settings("session.json")

    login_via_session = False
    login_via_pw = False

    if session:
        try:
            cl.set_settings(session)
            cl.login(acc, password)

            # check if session is valid
            try:
                cl.get_timeline_feed()
            except LoginRequired:
                logger.info("Session is invalid, need to login via username and password")

                old_session = cl.get_settings()

                # use the same device uuids across logins
                cl.set_settings({})
                cl.set_uuids(old_session["uuids"])

                cl.login(acc, password)
            login_via_session = True
        except Exception as e:
            logger.info("Couldn't login user using session information: %s" % e)

    if not login_via_session:
        try:
            logger.info("Attempting to login via username and password. username: %s" % acc)
            if cl.login(acc, password):
                login_via_pw = True
        except Exception as e:
            logger.info("Couldn't login user using username and password: %s" % e)

    if not login_via_pw and not login_via_session:
        raise Exception("Couldn't login user with either password or session")

###############################################################################################################################

login_user()


# user_id = cl.user_id_from_username(acc)
# medias = cl.user_medias(user_id, 20)
# info = cl.user_info_by_username('linguatrip_com')
# print(info)

# user_media_post = cl.user_medias('1334087929', 1)
# print(user_media_post)

# 2906931016075190889_1334087929

# print(cl.media_comments('2906931016075190889_1334087929', 1))
# json_string = json.dumps(python_object)

data_list =[]
# convert array into dataframe
for c in cl.media_comments('2906931016075190889_1334087929', 0):
    if c.user.username == 'linguatrip_com':
        continue
    c_dict = {
        "date and time": c.created_at_utc,
        "from": c.user.username,
        "comment": c.text
    }
    data_list.append(c_dict)

DF = pd.DataFrame(data_list)

# # save the dataframe as a csv file
DF.to_csv("instagram_data.csv")

