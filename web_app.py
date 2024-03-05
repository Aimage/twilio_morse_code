import os
from flask import Flask, request
from twilio.rest import Client
from morse.encoder import message_to_morse_sound
from config import SOUND_BASE_PATH

account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')


def create_twilio_api_client():
    client = Client(account_sid, auth_token)
    return client


def make_twilio_call(client,
                     to='',
                     from_="",
                     stream_url=''):
    stream_url = stream_url
    call = client.calls.create(
                        twiml=f'<Response><Play>{stream_url}</Play></Response>',
                        to=to,
                        from_=from_
                    )

app = Flask('__name__')


@app.route("/hello")
def hello():
    return "hello"


@app.route("/tomorseaudio")
def tomorseaudio():
    text = request.args.get("text", "")
    if text:
        message_to_morse_sound(text, SOUND_BASE_PATH, "static/output.ogg")
    return f"'{text}' translated to morse code", 200


@app.route("/sendmorse")
def morse_stream():
    to = request.args.get("to", "")
    from_ = request.args.get("from", "")
    base_url = request.base_url
    stream_url = f"{base_url}/static/output.ogg"
    if to and from_:
        client = create_twilio_api_client()
        make_twilio_call(client, to=to, from_=from_, stream_url=stream_url)
        return "audio morse code sent", 200
    return "Query parameter 'to' and 'from' should be a valid phone number", 400


if __name__ == '__main__':
    app.run()
