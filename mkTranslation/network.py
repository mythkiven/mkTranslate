# -*- coding: utf-8 -*-

import time
import re
import math
import sys
from requests.adapters import HTTPAdapter
from mkTranslation.utils import rshift,PY3,unicode

BASE = 'https://translate.google.com'
TRANSLATE = 'https://{host}/translate_a/single'

class TimeoutAdapter(HTTPAdapter):
    def __init__(self, timeout=None, *args, **kwargs):
        self.timeout = timeout
        super(TimeoutAdapter, self).__init__(*args, **kwargs)

    def send(self, *args, **kwargs):
        kwargs['timeout'] = self.timeout
        return super(TimeoutAdapter, self).send(*args, **kwargs)

class TokenAcquirer(object):

    RE_TKK = re.compile(r'tkk:\'(.+?)\'', re.DOTALL)
    RE_RAWTKK = re.compile(r'tkk:\'(.+?)\'', re.DOTALL)

    def __init__(self, tkk='0', session=None, host='translate.google.com'):
        self.session = session or requests.Session()
        self.tkk = tkk
        self.host = host if 'http' in host else 'https://' + host

    def _update(self):
        now = math.floor(int(time.time() * 1000) / 3600000.0)
        if self.tkk and int(self.tkk.split('.')[0]) == now:
            return

        r = self.session.get(self.host)

        raw_tkk = self.RE_TKK.search(r.text)
        if raw_tkk:
            self.tkk = raw_tkk.group(1)
            return

        code = unicode(self.RE_TKK.search(r.text).group(1)).replace('var ', '')
        if PY3:
            code = code.encode().decode('unicode-escape')
        else:
            code = code.decode('string_escape')

        if code:
            tree = ast.parse(code)
            visit_return = False
            operator = '+'
            n, keys = 0, dict(a=0, b=0)
            for node in ast.walk(tree):
                if isinstance(node, ast.Assign):
                    name = node.targets[0].id
                    if name in keys:
                        if isinstance(node.value, ast.Num):
                            keys[name] = node.value.n
                        elif isinstance(node.value, ast.UnaryOp) and \
                                isinstance(node.value.op, ast.USub):
                            keys[name] = -node.value.operand.n
                elif isinstance(node, ast.Return):
                    visit_return = True
                elif visit_return and isinstance(node, ast.Num):
                    n = node.n
                elif visit_return and n > 0:
                    if isinstance(node, ast.Add):
                        pass
                    elif isinstance(node, ast.Sub):
                        operator = '-'
                    elif isinstance(node, ast.Mult):
                        operator = '*'
                    elif isinstance(node, ast.Pow):
                        operator = '**'
                    elif isinstance(node, ast.BitXor):
                        operator = '^'
            clause = compile('{1}{0}{2}'.format(
                operator, keys['a'], keys['b']), '', 'eval')
            value = eval(clause, dict(__builtin__={}))
            result = '{}.{}'.format(n, value)

            self.tkk = result

    def _lazy(self, value):
        return lambda: value

    def _xr(self, a, b):
        size_b = len(b)
        c = 0
        while c < size_b - 2:
            d = b[c + 2]
            d = ord(d[0]) - 87 if 'a' <= d else int(d)
            d = rshift(a, d) if '+' == b[c + 1] else a << d
            a = a + d & 4294967295 if '+' == b[c] else a ^ d

            c += 3
        return a

    def acquire(self, text):
        a = []
        for i in text:
            val = ord(i)
            if val < 0x10000:
                a += [val]
            else:
                a += [
                    math.floor((val - 0x10000)/0x400 + 0xD800),
                    math.floor((val - 0x10000)%0x400 + 0xDC00)
                    ]

        b = self.tkk if self.tkk != '0' else ''
        d = b.split('.')
        b = int(d[0]) if len(d) > 1 else 0

        e = []
        g = 0
        size = len(text)
        while g < size:
            l = a[g]
            if l < 128:
                e.append(l)
            else:
                if l < 2048:
                    e.append(l >> 6 | 192)
                else:
                    if (l & 64512) == 55296 and g + 1 < size and \
                            a[g + 1] & 64512 == 56320:
                        g += 1
                        l = 65536 + ((l & 1023) << 10) + (a[g] & 1023)
                        e.append(l >> 18 | 240)
                        e.append(l >> 12 & 63 | 128)
                    else:
                        e.append(l >> 12 | 224)
                    e.append(l >> 6 & 63 | 128)
                e.append(l & 63 | 128)
            g += 1
        a = b
        for i, value in enumerate(e):
            a += value
            a = self._xr(a, '+-a^+6')
        a = self._xr(a, '+-3^+b+-f')
        a ^= int(d[1]) if len(d) > 1 else 0
        if a < 0:
            a = (a & 2147483647) + 2147483648
        a %= 1000000

        return '{}.{}'.format(a, a ^ b)

    def do(self, text):
        self._update()
        tk = self.acquire(text)
        return tk
