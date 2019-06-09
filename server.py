#!/usr/bin/python3

import http.server
import os
import secrets
import time
import uuid
from http.cookies import SimpleCookie as v
from urllib.parse import parse_qs

from passlib.hash import pbkdf2_sha256 as q

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
    c('<title>TODOZtitle><body]max-width:800px;W:auto;padding:16px">%sZbody>'
    % b), d))


def c(s, b=0):
    if b > 5:
        return s
    for e in zip(
            '[^@?_!]ZYXMQAWBGIFVJKC',
            c('<I typeY|Finline-block;|background:none;border:none;M|[submit"|<X methodYpost" actionY/|Q[pQ" JY| GY|</|="|form|cursor:pointer|assword|UserJ|margin|right|style|input|display:|Signup|name|%s|value',
              b + 1).split('|')):
        s = s.replace(*e)
    return s


f = c('_uV"]float:left">A[text"]Fblock" JYa">P!b"]Fblock">?CYV">ZX>')


h = lambda s, e='' : w(s, c('<h2>TODOZh2><p>KZp>KK') % (e, f, f.replace('left', c('B')).replace(c('V'), 'Login')))


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
      c('<G>I:checked~div{Fblock}div{Fnone}I{Fblock}ZG><label>[checkbox"]Fnone"/><h2]^W:0">TODOZh2><p]M;float:B;W:8px">&#9881Zp><div>_l">?GYfloat:B" CYLogout">ZX>_r">P!b">New p!c">?CYReset pQ">ZX> Zdiv>Zlabel><ul]padding:0">'
        ) +
      ''.join(
          c('<li]Fblock;border-top:1px solid black;">_et/K"]^">?GY@" CY&#974K">ZX><p]^width:calc(100%% - 100px);overflow-wrap:break-word;text-decoration:K">KZp>_ed/K"]^float:B;W:16px">?GY@" CYx">ZX>Zli>'
            ) % (k, 4 + int(e[1]), e[1] and 'line-through', e[0], k)
          for k, e in u[2].items()) +
      c('Zul>_n">[text"]^width:100%;W-B:-45px;padding-B:45px" JYl">?GY^@" CY+">ZX>'
        ))


def p(s):
    o, u, p = parse_qs(s.rfile.read(int(
        s.headers.get('Content-Length')))), z(s), s.path
    u, n = u
    a, b, i = [o.get(y, [b''])[0].decode(d) for y in [b'a', b'b', b'c']]
    y = err = None
    if p[1:3] == 'uL' and (a not in us or not q.verify(b, us[a][0])):
        err = c('A or pQ incorrect')
    if p[1:3] == 'uS':
        if a in us:
            err = 'A %s already taken' % (a)
        else:
            us[a] = [q.encrypt(b, rounds=k, salt_size=16), [], {}]
    if (p[1:3] == 'uL' or p[1:3] == 'uS') and not err:
        t = secrets.token_urlsafe()
        us[a][1].append((t, time.time() + 7**8))
        y, y['a'], y['b'], u = v(), a, t, us[a]
    if p == '/l':
        y, y['a'], y['b'] = v(), '', ''
    if u and p == '/r':
        if not q.verify(b, u[0]):
            r(s, 401)
            return w(s, c('<p>PQ incorrectZp>'))
        u[0] = q.encrypt(i, rounds=k, salt_size=16)
        u[1] = []
    if u and p == '/n':
        u[2][str(uuid.uuid4())] = [o[b'l'][0].decode(d), False]
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
    f.write(
        c('K\nKK\nK') %
        (len(u[1]),
         ''.join('%s,%s\n' % (s[0].replace('\n', '\a'), s[1]) for s in u[1]),
         len(u[2].values()), ''.join(
             '%s,%s,%s\n' % (e[1], k, e[0]) for k, e in u[2].items())))
    r(s, 301, y)


class H(http.server.BaseHTTPRequestHandler):
    def do_GET(s):
        g(s)

    def do_POST(s):
        p(s)


http.server.HTTPServer(('localhost', 8080), H).serve_forever()
