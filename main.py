import os
from dotenv import load_dotenv
from ytmusicapi import YTMusic, OAuthCredentials
import streamMusic

load_dotenv()

client_secret = os.getenv('client_secret')
client_id = os.getenv('client_id')

ytmusic = YTMusic('oauth.json', oauth_credentials=OAuthCredentials(client_id=client_id, client_secret=client_secret))

user_inp = input("Which song do you want to listen to?\n> ")

search_result = ytmusic.search(user_inp)
top_result_video_id = search_result[0]["videoId"]
uri = f"https://youtu.be/{top_result_video_id}"
total_time = int(search_result[0]["duration_seconds"])
title = search_result[0]["title"]
artists = ""

for a in search_result[0]['artists']:
    if (artists == ""):
        artists += a['name']
    else:
        artists += f", {a['name']}"

streamMusic.play_and_rewrite(uri, total_time, title, artists)
