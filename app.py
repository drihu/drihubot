""" Micro web framework """
import os
from dotenv import load_dotenv
from flask import Flask, request, Response
from handlers import handle_message, handle_postback

load_dotenv()
app = Flask(__name__)

PAGE_ACCESS_TOKEN = os.getenv('PAGE_ACCESS_TOKEN')
APP_HOST = os.getenv('APP_HOST')
APP_PORT = os.getenv('APP_PORT')

"""------------------------------
ROUTES
------------------------------"""
@app.route('/')
def index():
    """ GET / """
    return '<h1>drihubot</h1>'


@app.route('/webhook', methods=['POST'])
def post_webhook():
    """ POST /webhook """
    body = request.json
    if body['object'] == 'page':
        for entry in body['entry']:
            webhook_event = entry['messaging'][0]
            print(webhook_event)
            sender_psid = webhook_event['sender']['id']
            print('Sender PSID: ' + sender_psid)

            if webhook_event['message']:
                handle_message(sender_psid, webhook_event['message'])
            elif webhook_event['postback']:
                handle_postback(sender_psid, webhook_event['postback'])

        return Response(status=200, response='EVENT_RECEIVED')

    return Response(status=404)


@app.route('/webhook', methods=['GET'])
def get_webhook():
    """ GET /webhook """
    VERIFY_TOKEN = os.getenv('VERIFY_TOKEN')
    mode = request.args.get('hub.mode', '')
    token = request.args.get('hub.verify_token', '')
    challenge = request.args.get('hub.challenge', '')
    if mode and token:
        if mode == 'subscribe' and token == VERIFY_TOKEN:
            print('WEBHOOK_VERIFIED')
            return Response(status=200, response=challenge)
        else:
            return Response(status=403)
    else:
        return Response(status=403)


if __name__ == '__main__':
    app.run(port=APP_PORT, host=APP_HOST)
