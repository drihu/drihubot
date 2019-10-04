import os
import requests
from dotenv import load_dotenv

load_dotenv()
MUSIXMATCH_API_KEY = os.getenv('MUSIXMATCH_API_KEY')
PAGE_ACCESS_TOKEN = os.getenv('PAGE_ACCESS_TOKEN')

def handle_message(sender_psid='', received_message=''):
    if received_message['text']:
        message_text = received_message['text']
        songs = lyrics_match_songs(message_text)
        text = f'Those lyrics match with the following songs ({len(songs)} results): '

        first = True
        for song in songs:
            track_name = song['track_name']
            artist_name = song['artist_name']
            if first:
                text += f'{track_name} by {artist_name}'
                first = False
            else:
                text += f'; {track_name} by {artist_name}'

        print(text)
        response = {
            'text': text
        }

    call_send_api(sender_psid, response)


def handle_postback(sender_psid='', received_postback=''):
    return 'Hello'


def call_send_api(sender_psid='', response=''):
    request_body = {
        'recipient': {
            'id': sender_psid
        },
        'message': response
    }

    requests.post(
        url='https://graph.facebook.com/v2.6/me/messages',
        params={'access_token': PAGE_ACCESS_TOKEN},
        json=request_body
    )


def lyrics_match_songs(lyrics=''):
    songs = []
    response = requests.get(
        url='https://api.musixmatch.com/ws/1.1/track.search',
        params={
            'format': 'json',
            'callback': 'callback',
            'q_lyrics': lyrics,
            'quorum_factor': 1,
            'apikey': MUSIXMATCH_API_KEY
        }
    )

    track_list = response.json()['message']['body']['track_list']

    for track_element in track_list:
        songs.append({
            'track_name': track_element['track']['track_name'],
            'artist_name': track_element['track']['artist_name']
        })

    return songs
