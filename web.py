#!/usr/bin/env python

import os
from flask import Flask, request, Response
from twilio import twiml
from twilio.rest import TwilioRestClient


app = Flask(__name__)
sentry_client = None
try:
    from raven.contrib.flask import Sentry
    sentry_client = Sentry(app, dsn=os.environ.get('SENTRY_DSN'))
except:
    pass

ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
TWILIO_NUMBER = os.environ.get('TWILIO_NUMBER')
twilio_client = TwilioRestClient(
    os.environ.get('TWILIO_SID'),
    os.environ.get('TWILIO_TOKEN')
)


@app.route('/' + ACCESS_TOKEN, methods=['GET'])
def handle_text(access_token):
    text_content = request.form['Body']

    resp = twiml.Response()
    resp.message(text_content)
    return Response(str(resp), mimetype='text/xml')


if __name__ == '__main__':
    app.run(debug=True)
