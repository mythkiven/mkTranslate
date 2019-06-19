# -*- coding: utf-8 -*-

class Translated(object):
    def __init__(self, src, dest, origin, text, pronunciation, extra_data=None):
        self.src = src
        self.dest = dest
        self.origin = origin
        self.text = text
        self.pronunciation = pronunciation
        self.extra_data = extra_data

    def __str__(self):
        return self.__unicode__()

    def __unicode__(self):
        return u'Translated(src={src}, dest={dest}, text={text}, pronunciation={pronunciation}, 'u'extra_data={extra_data})'.format(
            src=self.src, dest=self.dest, text=self.text, pronunciation=self.pronunciation,extra_data='"' + repr(self.extra_data)[:10] + '..."')

class Detected(object):
    def __init__(self, lang, confidence):
        self.lang = lang
        self.confidence = confidence

    def __str__(self):
        return self.__unicode__()

    def __unicode__(self):
        return u'Detected(lang={lang}, confidence={confidence})'.format(lang=self.lang, confidence=self.confidence)