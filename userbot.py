#############################################################################################################
#                                                                                                           #
#                                                                                                           #            
#                                                   IMPORT                                                  # 
#                                                                                                           #
#                                                                                                           #
#############################################################################################################

from pyrogram import Client, errors, filters
from pyrogram import enums
from pyrogram.errors import FloodWait
from spotipy.oauth2 import SpotifyOAuth
import time
import asyncio
import spotipy
import random

#############################################################################################################
#                                                                                                           #
#                                                                                                           #            
#                                             DEFINING VARIABLES                                            # 
#                                                                                                           #
#                                                                                                           #
#############################################################################################################


#defining telegram session
api_id = 123456 #put here your api id
api_hash = "abcd123456" #put here your api hash
ub = Client("ub", api_id=api_id, api_hash=api_hash) 

#defining spotipy session
cid = "abcd123456" #set here your client id
secret = "abcd123456" #set here your client secret
r_uri = "https://google.com/"
scope = "ugc-image-upload user-read-currently-playing user-read-playback-state user-modify-playback-state app-remote-control streaming playlist-read-private playlist-read-collaborative playlist-modify-private playlist-modify-public user-follow-modify user-follow-read user-read-playback-position user-top-read user-read-recently-played user-library-modify user-library-read user-read-email"
token = SpotifyOAuth(client_id=cid,client_secret=secret,redirect_uri=r_uri,scope=scope)
sp = spotipy.Spotify(auth_manager=token)

#just usefull things
allowed=[1780793442] #set here your id, and eventullay ids of other people that you want to control your spotify
pre=["/","."] #set here what prefixes you want your commands to work with


#############################################################################################################
#                                                                                                           #
#                                                                                                           #            
#                                                SPOTIFY                                                    # 
#                                                                                                           #
#                                                                                                           #
#############################################################################################################


@ub.on_message(filters.command("song", prefixes=pre))
async def nowcmd(client,message):
    if message.from_user.id in allowed:
        track = sp.current_user_playing_track()
        try:
            artist= track["item"]["artists"][0]["name"]
            name = track["item"]["name"]
            t_id = track["item"]["id"]
            await ub.send_message(message.chat.id, f"🎶 @{ub.me.username} __is listening to...__\n\n**{name}** `by` {artist}\n\n🔗 [LINK](https://open.spotify.com/intl-it/track/{t_id})", disable_web_page_preview=True)
        except:
            await ub.send_message(message.chat.id, f"🎶 @{ub.me.username} is not currently listening anything")


@ub.on_message(filters.command("set", prefixes=pre))
async def songcmd(client,message):
    if message.from_user.id in allowed:
        search = message.text.split(' ',1)[1]
        try:
            track = sp.search(q=search, limit=1, type="track")
            t_id = track['tracks']['items'][0]['id']
            sp.add_to_queue(t_id)
            sp.next_track()
            time.sleep(1)
            track = sp.current_user_playing_track()
            artist= track["item"]["artists"][0]["name"]
            name=track["item"]["name"]
            t_id = track["item"]["id"]
            await ub.send_message(message.chat.id, f"🎶 Now __playing...__\n\n**{name}** `by` {artist}\n\n🔗 [LINK](https://open.spotify.com/intl-it/track/{t_id})", disable_web_page_preview=True)
        except Exception as e:
            print(str(e))
            await ub.send_message(message.chat.id, f"Error trying to play")


@ub.on_message(filters.command("add", prefixes=pre))
async def addcmd(client,message):
    if message.from_user.id in allowed:
        search = message.text.split(' ',1)[1]
        try:
            track = sp.search(q=search, limit=1, type="track")
            t_id = track['tracks']['items'][0]['id']
            sp.add_to_queue(t_id)
            await ub.send_message(message.chat.id, f"{search} added to queue..")
        except Exception as e:
            print(str(e))
            await ub.send_message(message.chat.id, f"Error adding to queue, probably wasn't listing to anything")

@ub.on_message(filters.command("next", prefixes=pre))
async def nextcmd(client,message):
    if message.from_user.id in allowed:
        try:
            sp.next_track()
            time.sleep(1)
            track = sp.current_user_playing_track()
            artist= track["item"]["artists"][0]["name"]
            name=track["item"]["name"]
            t_id = track["item"]["id"]
            await ub.send_message(message.chat.id, f"🎶 Just __skipped to...__\n\n**{name}** `by` {artist}\n\n🔗 [LINK](https://open.spotify.com/intl-it/track/{t_id})", disable_web_page_preview=True)
        except:
            await ub.send_message(message.chat.id, f"Error while trying to skip song, probably wasn't listing to anything")

@ub.on_message(filters.command("pause", prefixes=pre))
async def pausecmd(client,message):
    if message.from_user.id in allowed:
        try:
            sp.pause_playback()
            await ub.send_message(message.chat.id, f"Successfully paused.")
        except:
            await ub.send_message(message.chat.id, f"Error while trying to pause, probably wasn't listing to anything")


@ub.on_message(filters.command("back", prefixes=pre))
async def back(client,message):
    if message.from_user.id in allowed:
        try:
            sp.previous_track()
            time.sleep(1)
            track = sp.current_user_playing_track()
            artist= track["item"]["artists"][0]["name"]
            name=track["item"]["name"]
            t_id = track["item"]["id"]
            await ub.send_message(message.chat.id, f"🎶 Just __went back to...__\n\n**{name}** `by` {artist}\n\n🔗 [LINK](https://open.spotify.com/intl-it/track/{t_id})", disable_web_page_preview=True)
        except:
            await ub.send_message(message.chat.id, f"Error while trying to back song, probably wasn't listing to anything")

@ub.on_message(filters.command("play", prefixes=pre))
async def playcmd(client,message):
    if message.from_user.id in allowed:
        try:
            sp.start_playback()
            await ub.send_message(message.chat.id, f"Successfully played.")
        except Exception as e:
            await ub.send_message(message.chat.id, f"Error while trying to play song, probably wasn't listing to anything")

#############################################################################################################
#                                                                                                           #
#                                                                                                           #            
#                                           END OF LOOP                                                     # 
#                                                                                                           #
#                                                                                                           #
#############################################################################################################


print("online")
ub.run()
