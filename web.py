#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from flask import Flask, request, Response, abort
from twilio import twiml
from twilio.rest import TwilioRestClient
from raven.contrib.flask import Sentry
from simsimi import SimSimi, SimSimiException


app = Flask(__name__)

ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
assert ACCESS_TOKEN

TWILIO_NUMBER = os.environ.get('TWILIO_NUMBER')
twilio_client = TwilioRestClient(
    os.environ.get('TWILIO_SID'),
    os.environ.get('TWILIO_TOKEN')
)
sentry_client = Sentry(app, dsn=os.environ.get('SENTRY_DSN'))
simsimi_client = SimSimi(os.environ.get('SIMSIMI_KEY'))


@app.route('/' + ACCESS_TOKEN, methods=['GET'])
def handle_text():
    try:
        text_content = request.args['Body']
    except KeyError:
        abort(400)

    resp = twiml.Response()
    try:
        simsimi_resp = simsimi_client.get_response(text_content)
        resp.message(simsimi_resp)
    except SimSimiException:
        sentry_client.captureException()
        resp.message(u'哦')
    return Response(resp.toxml(), mimetype='text/xml')


if __name__ == '__main__':
    app.run(debug=True)
