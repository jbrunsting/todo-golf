#!/usr/bin/python3

import http.server
import os
import secrets
import time
import uuid
from http.cookies import SimpleCookie as v
from urllib.parse import parse_qs

from passlib.hash import pbkdf2_sha256 as sha

k = 200000
d = 'utf-8'
us = {}

for n in [f for f in os.listdir('.') if f.endswith('.u')]:
    f = open(n, 'r')
    r = f.readline
    us[n[:-2]] = u = [r()[:-1], [], {}]
    for i in range(int(r())):
        s = r()[:-1].split(',', 1)
        u[1].append((s[0].replace('\a', '\n'), float(s[1])))
    for i in range(int(r())):
        e = r()[:-1].split(',', 2)
        u[2][e[1]] = [e[2], e[0] == 'True']


def z(s):
    c = v(s.headers.get('Cookie'))
    if 'a' in c and 'b' in c:
        a = c['a'].value
        if a in us and c['b'].value in [
                s[0] for s in us[a][1] if s[1] > time.time()
        ]:
            return (us[a], a)
    return ('', '')


w = lambda s, b: s.wfile.write(bytes(
        c('<title>TODOZtitle><body]max-width:800px;W:auto;padding:16px">%s</body>'
          % b), d))


def c(s, b=0):
    if b > 5:
        return s
    for e in zip(
            '[^@?_!]ZYXMQAWBGIFV',
            c('<I typeY|Finline-block;|background:none;border:none;M|[submit"|<X methodYpost" actionY/|Q[pQ" nameY| GY|</|="|form|cursor:pointer|assword|Username|margin|right|style|input|display:|Signup',
              b + 1).split('|')):
        s = s.replace(*e)
    return s


f = c('_uV"]float:left">A[text"]Fblock" nameYa">P!b"]Fblock">?valueYV">ZX>')


h = lambda s, e='' : w(s, '<h2>TODO</h2><p>%s</p>%s%s' % (e, f, f.replace('left', c('B')).replace(c('V'), 'Login')))


def r(s, c, k=''):
    s.send_response(c)
    k and s.send_header('Set-Cookie', k.output(header='', sep=''))
    k != '' and s.send_header('Location', '/')
    s.end_headers()


def g(s):
    u, a = z(s)
    r(s, 200)
    if not u:
        return h(s)

    w(s,
      c('<G>I:checked~div{Fblock}div{Fnone}I{Fblock}ZG><label>[checkbox"]Fnone"/><h2]^W:0">TODOZh2><p]M;float:B;W:8px">&#9881Zp><div>_l">?GYfloat:B" valueYLogout">ZX>_r">P!b">New p!c">?valueYReset pQ">ZX> Zdiv>Zlabel><ul]padding:0">'
        ) +
      ''.join(
          c('<li]Fblock;border-top:1px solid black;">_et/%s"]^">?GY@" valueY&#974%s">ZX><p]^width:calc(100%% - 100px);overflow-wrap:break-word;text-decoration:%s">%sZp>_ed/%s"]^float:B;W:16px">?GY@" valueYx">ZX>Zli>'
            ) % (k, 4 + int(e[1]), e[1] and 'line-through', e[0], k)
          for k, e in u[2].items()) +
      c('Zul>_n">[text"]^width:100%;W-B:-45px;padding-B:45px" nameYl">?GY^@" valueY+">ZX>'
        ))


def x(a):
    b = secrets.token_urlsafe()
    us[a][1].append((b, time.time() + 7**8))
    c, c['a'], c['b'] = v(), a, b
    return c


def p(s):
    o, u, p = parse_qs(s.rfile.read(int(
        s.headers.get('Content-Length')))), z(s), s.path
    u, n = u
    a, b, i = [o.get(y, [b''])[0].decode(d) for y in [b'a', b'b', b'c']]
    y = err = None
    if p[1:3] == 'uL' and (a not in us or not sha.verify(b, us[a][0])):
        err = c('A or pQ incorrect')
    if p[1:3] == 'uS':
        if a in us:
            err = 'A %s already taken' % (a)
        else:
            us[a] = [sha.encrypt(b, rounds=k, salt_size=16), [], {}]
    if (p[1:3] == 'uL' or p[1:3] == 'uS') and not err:
        u, y = us[a], x(a)
    if p == '/l':
        y, y['a'], y['b'] = v(), '', ''
    if u and p == '/r':
        if not sha.verify(b, u[0]):
            r(s, 401)
            return w(s, c('<p>PQ incorrect</p>'))
        u[0] = sha.encrypt(i, rounds=k, salt_size=16)
        u[1] = []
    if u and p == '/n':
        id = str(uuid.uuid4())
        u[2][id] = [o[b'l'][0].decode(d), False]
    if u and p[1:2] == 'e':
        id = p.split('/', 2)[2]
        u[2][id][1] = not u[2][id][1]
        if p[2:3] == 'd':
            del u[2][id]
    if err:
        r(s, 200)
        return h(s, err)
    f = open((a or n) + '.u', 'w+')
    f.write(u[0] + '\n')
    u[1] = [s for s in u[1] if s[1] > time.time()]
    f.write('%s\n%s%s\n%s' %
            (len(u[1]), ''.join(
                '%s,%s\n' % (s[0].replace('\n', '\a'), s[1]) for s in u[1]),
             len(u[2].values()),
             ''.join('%s,%s,%s\n' % (e[1], k, e[0]) for k, e in u[2].items())))
    r(s, 301, y)


class H(http.server.BaseHTTPRequestHandler):
    def do_GET(s):
        g(s)

    def do_POST(s):
        p(s)


http.server.HTTPServer(('localhost', 8080), H).serve_forever()
