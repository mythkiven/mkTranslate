# -*- coding: utf-8 -*-
"""
A Translation module.

You can translate text using this module.
"""
import requests
import random

from mkTranslation import utils,network
from mkTranslation.network import TimeoutAdapter,TokenAcquirer
from mkTranslation.utils import PY3
from mkTranslation.constants import DEFAULT_USER_AGENT, LANGCODES, LANGUAGES, SPECIAL_CASES
from mkTranslation.model import Translated, Detected


EXCLUDES = ('en', 'ca', 'fr')


class mkTranslator(object):
    """Google Translate ajax API implementation class

    You have to create an instance of Translator to use this API

    :param service_urls: google translate url list. URLs will be used randomly.
                         For example ``['translate.google.com', 'translate.google.co.kr']``
    :type service_urls: a sequence of strings

    :param user_agent: the User-Agent header to send when making requests.
    :type user_agent: :class:`str`

    :param proxies: proxies configuration. 
                    Dictionary mapping protocol or protocol and host to the URL of the proxy 
                    For example ``{'http': 'foo.bar:3128', 'http://host.name': 'foo.bar:4012'}``
    :type proxies: dictionary

    :param timeout: Definition of timeout for Requests library.
                    Will be used by every request.
    :type timeout: number or a double of numbers
    """

    def __init__(self, service_urls=None, user_agent=DEFAULT_USER_AGENT,
                 proxies=None, timeout=None):

        self.session = requests.Session()
        if proxies is not None:
            self.session.proxies = proxies
        self.session.headers.update({
            'User-Agent': user_agent,
        })
        if timeout is not None:
            self.session.mount('https://', TimeoutAdapter(timeout))
            self.session.mount('http://', TimeoutAdapter(timeout))

        self.service_urls = service_urls or ['translate.google.com']
        self.token_acquirer = TokenAcquirer(session=self.session, host=self.service_urls[0])

        # Use HTTP2 Adapter if hyper is installed
        try:  # pragma: nocover
            from hyper.contrib import HTTP20Adapter
            self.session.mount(urls.BASE, HTTP20Adapter())
        except ImportError:  # pragma: nocover
            pass

    def _pick_service_url(self):
        if len(self.service_urls) == 1:
            return self.service_urls[0]
        return random.choice(self.service_urls)

    def _translate(self, text, dest, src):
        if not PY3 and isinstance(text, str):  # pragma: nocover
            text = text.decode('utf-8')

        token = self.token_acquirer.do(text)
        params = utils.build_params(query=text, src=src, dest=dest,
                                    token=token)
        url = network.TRANSLATE.format(host=self._pick_service_url())
        r = self.session.get(url, params=params)
        data = 'cannot tx !!!'
        if(r.text):
            data = utils.format_json(r.text)
        return data

    def _parse_extra_data(self, data):
        response_parts_name_mapping = {
            0: 'translation',
            1: 'all-translations',
            2: 'original-language',
            5: 'possible-translations',
            6: 'confidence',
            7: 'possible-mistakes',
            8: 'language',
            11: 'synonyms',
            12: 'definitions',
            13: 'examples',
            14: 'see-also',
        }

        extra = {}

        for index, category in response_parts_name_mapping.items():
            extra[category] = data[index] if (index < len(data) and data[index]) else None

        return extra

    def translate(self, text, dest='en', src='auto'):
        dest = dest.lower().split('_', 1)[0]
        src = src.lower().split('_', 1)[0]

        if src != 'auto' and src not in LANGUAGES:
            if src in SPECIAL_CASES:
                src = SPECIAL_CASES[src]
            elif src in LANGCODES:
                src = LANGCODES[src]
            else:
                raise ValueError('invalid source language')

        if dest not in LANGUAGES:
            if dest in SPECIAL_CASES:
                dest = SPECIAL_CASES[dest]
            elif dest in LANGCODES:
                dest = LANGCODES[dest]
            else:
                raise ValueError('invalid destination language')

        if isinstance(text, list):
            result = []
            for item in text:
                translated = self.translate(item, dest=dest, src=src)
                result.append(translated)
            return result

        origin = text
        data = self._translate(text, dest, src)

        # this code will be updated when the format is changed.
        translated = ''.join([d[0] if d[0] else '' for d in data[0]])

        extra_data = self._parse_extra_data(data)

        # actual source language that will be recognized by Google Translator when the
        # src passed is equal to auto.
        try:
            src = data[2]
        except Exception:  # pragma: nocover
            pass

        pron = origin
        try:
            pron = data[0][1][-2]
        except Exception:  # pragma: nocover
            pass
        if not PY3 and isinstance(pron, unicode) and isinstance(origin, str):  # pragma: nocover
            origin = origin.decode('utf-8')
        if dest in EXCLUDES and pron == origin:
            pron = translated

        # for python 2.x compatbillity
        if not PY3:  # pragma: nocover
            if isinstance(src, str):
                src = src.decode('utf-8')
            if isinstance(dest, str):
                dest = dest.decode('utf-8')
            if isinstance(translated, str):
                translated = translated.decode('utf-8')

        # put final values into a new Translated object
        result = Translated(src=src, dest=dest, origin=origin,
                            text=translated, pronunciation=pron, extra_data=extra_data)

        return result

    def detect(self, text):
        if isinstance(text, list):
            result = []
            for item in text:
                lang = self.detect(item)
                result.append(lang)
            return result

        data = self._translate(text, dest='en', src='auto')

        # actual source language that will be recognized by Google Translator when the
        # src passed is equal to auto.
        src = ''
        confidence = 0.0
        try:
            src = ''.join(data[8][0])
            confidence = data[8][-2][0]
        except Exception:  # pragma: nocover
            pass
        result = Detected(lang=src, confidence=confidence)

        return result
