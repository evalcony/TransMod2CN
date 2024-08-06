#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
MIT License

Copyright (c) 2016 Arnaud Aliès

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import sys
import re
import utils
from pygtrans import Translate

if (sys.version_info[0] < 3):
    import urllib2
    import urllib
    import HTMLParser
else:
    import html
    import urllib.request
    import urllib.parse

agent = {'User-Agent':
         "Mozilla/4.0 (\
compatible;\
MSIE 6.0;\
Windows NT 5.1;\
SV1;\
.NET CLR 1.1.4322;\
.NET CLR 2.0.50727;\
.NET CLR 3.0.04506.30\
)"}

class GoogleTrans:
    def __init__(self, from_lang, to_lang):
        self.name = 'google'
        self.PROXY_URL = utils.read_config('appconf.ini')['google']['proxy']
        self.from_lang = from_lang
        self.to_lang = to_lang

    def unescape(self, text):
        if (sys.version_info[0] < 3):
            parser = HTMLParser.HTMLParser()
        else:
            parser = html
        return (parser.unescape(text))

    def batch_translate(self, to_translate):
        client = Translate(proxies={'https': self.PROXY_URL})
        google_res = client.translate(to_translate, target=self.to_lang)
        res = []
        for g in google_res:
            res.append(g.translatedText)
        return res

    def translate(self, to_translate):

        to_language = self.to_lang
        from_language = self.from_lang

        """Returns the translation using google translate
        you must shortcut the language you define
        (French = fr, English = en, Spanish = es, etc...)
        if not defined it will detect it or use english by default

        Example:
        print(translate("salut tu vas bien?", "en"))
        hello you alright?
        """
        base_link = "http://translate.google.com/m?tl=%s&sl=%s&q=%s"
        # print('sys.version_info=' + str(sys.version_info[0]))
        if (sys.version_info[0] < 3):
            to_translate = urllib.quote_plus(to_translate)
            link = base_link % (to_language, from_language, to_translate)

            proxy_handler = urllib2.ProxyHandler({'http': self.PROXY_URL, 'https': self.PROXY_URL})
            opener = urllib2.build_opener(proxy_handler)
            req = urllib2.Request(link, headers=agent)
            raw_data = opener.open(req).read()
        else:
            to_translate = urllib.parse.quote(to_translate)
            link = base_link % (to_language, from_language, to_translate)

            proxy = urllib.request.ProxyHandler({'http': self.PROXY_URL, 'https': self.PROXY_URL})
            opener = urllib.request.build_opener(proxy)

            request = urllib.request.Request(link, headers=agent)
            resp = opener.open(request)
            raw_data = resp.read()

        data = raw_data.decode("utf-8")
        expr = r'(?s)class="(?:t0|result-container)">(.*?)<'
        re_result = re.findall(expr, data)
        if (len(re_result) == 0):
            result = ""
        else:
            result = self.unescape(re_result[0])
        return (result)

if __name__ == '__main__':
    # text = "[76], I want to know why we're here. I never let anyone use some... [21] on me, taking the group away from [78] and her [27]!"
    # text = "hello world"
    # res = GoogleTrans("auto", "zh-CN").translate(text)
    # print(res)
    texts = ['hello', 'world']
    print(GoogleTrans("auto", "zh-CN").batch_translate(texts))