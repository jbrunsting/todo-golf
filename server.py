#!/usr/bin/python3

import http.server
import os
import secrets
import time
import uuid
from http.cookies import SimpleCookie
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
    c = SimpleCookie(s.headers.get('Cookie'))
    if 'a' in c and 'b' in c:
        a = c['a'].value
        if a in us and c['b'].value in [
                s[0] for s in us[a][1] if s[1] > time.time()
        ]:
            return (us[a], a)
    return ('', '')


def w(s, b):
    return s.wfile.write(
        bytes(
            c('<title>TODOZtitle><body]max-width:800px;margin:auto;padding:16px">'
              ) + b + '</body>', d))


def h(s, e=None):
    f = c(
        '_uSignup"]float:left">Username[text"]display:block" name="a">P!b"]display:block">?value="Signup">Zform>'
    )
    w(s, '<h2>TODO</h2>' + ('<p>%s</p>' % e if e else '') + f +
      f.replace('left', 'right').replace('Signup', 'Login'))


def c(s):
    v = ['[', '<input type="']
    p = '^|display:inline-block;|@|background:none;border:none;cursor:pointer|?|[submit"|_|<form method="post" action="/|!|assword[password" name="|]| style="|Z|</'.replace(*v[0:2]).split('|') + v
    for i in range(8):
        s = s.replace(*p[i * 2:i * 2 + 2])
    return s


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
      c('<style>input:checked~div{display:block}div{display:none}input{display:block}Zstyle><label>[checkbox"]display:none"/><h2]^margin:0">TODOZh2><p]cursor:pointer;float:right;margin:8px">&#9881Zp><div>_l">?style="float:right" value="Logout">Zform>_r">P!b">New p!c">?value="Reset password">Zform> Zdiv>Zlabel><ul]padding:0">'
        ) +
      ''.join(
          c('<li]display:block;border-top:1px solid black;">_et/%s"]^">?style="@" value="&#974%s">Zform><p]^width:calc(100%% - 100px);overflow-wrap:break-word;text-decoration:%s">%sZp>_ed/%s"]^float:right;margin:16px">?style="@" value="x">Zform>Zli>'
            ) % (k, 4 + int(e[1]), e[1] and 'line-through', e[0], k)
          for k, e in u[2].items()) +
      c('Zul>_n">[text"]^width:100%;margin-right:-45px;padding-right:45px" name="l">?style="^@" value="+">Zform>'
        ))


def x(a):
    b = secrets.token_urlsafe()
    us[a][1].append((b, time.time() + 7**8))
    c, c['a'], c['b'] = SimpleCookie(), a, b
    return c


def p(s):
    body, u, p = parse_qs(s.rfile.read(int(
        s.headers.get('Content-Length')))), z(s), s.path
    u, n = u
    a, b, i = [body.get(c, [b''])[0].decode(d) for c in [b'a', b'b', b'c']]
    c = err = None
    if p[1:3] == 'uL' and (a not in us or not sha.verify(b, us[a][0])):
        err = 'Username or password incorrect'
    if p[1:3] == 'uS':
        if a in us:
            err = 'Username %s already taken' % (a)
        else:
            us[a] = [sha.encrypt(b, rounds=k, salt_size=16), [], {}]
    if (p[1:3] == 'uL' or p[1:3] == 'uS') and not err:
        u, c = us[a], x(a)
    if p == '/l':
        c, c['a'], c['b'] = SimpleCookie(), '', ''
    if u and p == '/r':
        if not sha.verify(b, u[0]):
            r(s, 401)
            return s.wfile.write(b'<p>Password incorrect</p>')
        u[0] = sha.encrypt(i, rounds=k, salt_size=16)
        u[1] = []
    if u and p == '/n':
        id = str(uuid.uuid4())
        u[2][id] = [body[b'l'][0].decode(d), False]
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
    r(s, 301, c)


class H(http.server.BaseHTTPRequestHandler):
    def do_GET(s):
        g(s)

    def do_POST(s):
        p(s)


http.server.HTTPServer(('localhost', 8080), H).serve_forever()
