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
    cs = SimpleCookie(s.headers.get('Cookie'))
    if 'a' in cs and 'b' in cs:
        a = cs['a'].value
        if a in us:
            u = us[a]
            if cs['b'].value in [s[0] for s in u[1] if s[1] > time.time()]:
                return (u, a)
    return ('', '')


def w(s, b):
    return s.wfile.write(
        bytes(
            c('<title>TODO</title><body]max-width:800px;margin:auto;padding:16px">'
              ) + b + '</body>', d))


def h(s, error=None):
    form = c(
        ')uSignup"]float:left">Username[text"]display:block" name="a">P!b"]display:block">(value="Signup"></form>'
    )
    w(s, '<h2>TODO</h2>' + ('<p>' + error + '</p>' if error else '') + form +
      form.replace('left', 'right').replace('Signup', 'Login'))


def c(s, b=0):
    if b > 5: return s
    return s.replace('^', 'display:inline-block;').replace(
        '@', 'background:none;border:none;cursor:pointer').replace(
            '(', c('[submit" ', b + 1)).replace(
                ')', '<form method="post" action="/').replace(
                    '!', c('assword[password" name="', b + 1)).replace(
                        '[', '<input type="').replace(']', ' style="')


def r(s, c):
    s.send_response(c)
    s.end_headers()


def g(s):
    u, a = z(s)
    r(s, 200)
    if not u:
        return h(s)

    w(s,
      c('''
<style>
input:checked~div{display: block}
div{display:none}
input{display:block}
</style>
<label>
[checkbox"]display:none"/>
<h2]^margin:0">TODO</h2>
<p]cursor:pointer;float:right;margin:8px">&#9881</p>
<div>
)l">
(style="float:right" value="Logout">
</form> 
)r">
P!b">
New p!c">
(value="Reset password">
</form> 
</div>
</label>
<ul]padding:0">''') + ''.join([
          c('<li]display:block;border-top:1px solid black;">)e_t/') + k +
          c('"]^">(style="@" value="&#974') + str(4 + int(e[1])) +
          c('"></form><p]^width:calc(100% - 100px);overflow-wrap:break-word;text-decoration:'
            ) + ('line-through'
                 if e[1] else '') + '">' + e[0] + c('</p>)e_d/') + k +
          c('"]^float:right;margin:16px">(style="@" value="x"></form>') +
          '</li>' for k, e in u[2].items()
      ]) +
      c('</ul>)n">[text"]^width:100%;margin-right:-45px;padding-right:45px" name="l">(style="^@" value="+"></form>'
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
    if p[1:3] == 'uL':
        if a not in us or not sha.verify(b, us[a][0]):
            err = 'Username or password incorrect'
    elif p[1:2] == 'u':
        if a in us:
            err = 'Username %s already taken' % (a)
        else:
            us[a] = [sha.encrypt(b, rounds=k, salt_size=16), [], {}]
    if p[1:2] == 'u' and not err:
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
    t = p[3:4]
    if u and p[1:3] == 'e_':
        id = p.split('/', 2)[2]
        u[2][id][1] = not u[2][id][1]
        if t == 'd':
            del u[2][id]
    if err:
        r(s, 200)
        h(s, err)
        return
    f = open((a or n) + '.u', 'w+')
    f.write(u[0] + '\n')
    u[1] = [s for s in u[1] if s[1] > time.time()]
    f.write(
        str(len(u[1])) + '\n' + ''.join(
            s[0].replace('\n', '\a') + ',' + str(s[1]) + '\n'
            for s in u[1]) + str(len(u[2].values())) + '\n' + ''.join(
                str(e[1]) + ',' + k + ',' + e[0] + '\n'
                for k, e in u[2].items()))
    s.send_response(301)
    if c:
        s.send_header('Set-Cookie', c.output(header='', sep=''))
    s.send_header('Location', '/')
    s.end_headers()


class H(http.server.BaseHTTPRequestHandler):
    def do_GET(s):
        g(s)

    def do_POST(s):
        p(s)


http.server.HTTPServer(('localhost', 8080), H).serve_forever()
