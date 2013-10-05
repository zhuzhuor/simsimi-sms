#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from guess_language.guess_language import guessLanguage


class SimSimiException(Exception):
    def __init__(self, code, msg):
        self.code = code
        self.msg = msg

    def __str__(self):
        return str(self.code) + ' - ' + self.msg


def is_ascii(s):
    try:
        s.decode('ascii')
    except Exception:
        return False
    else:
        return True


class SimSimi:
    def __init__(self,
                 key,
                 default_lang='ch',  # not zh
                 trial_key=False,
                 filter_rate='0.0'):
        self.__key = key
        self.default_lang = default_lang
        self.filter_rate = filter_rate
        if trial_key:
            self.url = 'http://sandbox.api.simsimi.com/request.p'
        else:
            self.url = 'http://api.simsimi.com/request.p'

    def get_response(self, text):
        lang = guessLanguage(text)
        if 'UNKNOWN' == lang:
            if is_ascii(text):
                lang = 'en'
            else:
                lang = self.default_lang
        elif lang == 'zh':
            lang == 'ch'  # see http://developer.simsimi.com/lclist

        # only to handle en, fr, zh in my case
        if lang not in ('ch', 'en', 'fr'):
            lang = self.default_lang

        payload = {
            'key': self.__key,
            'text': text,
            'lc': lang,
            'ft': self.filter_rate
        }
        resp = requests.get(self.url, params=payload)
        print resp.url
        resp_json = resp.json()
        if resp_json['result'] == 100:
            return resp_json['response']
        else:
            raise SimSimiException(resp_json['result'], resp_json['msg'])


if __name__ == '__main__':
    import os
    SIMSIMI_KEY = os.environ.get('SIMSIMI_KEY')
    ss = SimSimi(SIMSIMI_KEY)
    print ss.get_response(u'你好')
    print ss.get_response('Hello world!')
