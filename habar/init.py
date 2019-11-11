from listen import listen
from flask import Flask, request, json

from settings import callback_confirmation_token

app = Flask(__name__)


@app.route('/',  methods=['POST'])
def processing():
    data = json.loads(request.data)
    if 'type' not in data.keys():
        return 'ok'
    if data['type'] == 'confirmation':
        return callback_confirmation_token
    elif data['type'] == 'message_new':
        l1 = listen()
        l1.choose()
        return 'ok'
    return 'ok'
