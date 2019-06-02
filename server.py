#!/usr/bin/python3

import http.server
import os
import secrets
import time
import uuid
from http.cookies import SimpleCookie
from urllib.parse import parse_qs

from passlib.hash import pbkdf2_sha256 as sha

r = 200000
d = 'utf-8'
us = {}

for n in os.listdir('.'):
    if not n.endswith('.u'): continue
    f = open(n[:-2] + '.u', 'r')
    u = [f.readline()[:-1], [], {}]
    us[n[:-2]] = u
    for i in range(int(f.readline())):
        s = f.readline()[:-1].split(',', 1)
        u[1].append((s[0].replace('\a', '\n'), float(s[1])))
    for i in range(int(f.readline())):
        e = f.readline()[:-1].split(',', 2)
        u[2][e[1]] = [e[2], e[0] == 'True']


def get_u(s):
    cs = SimpleCookie(s.headers.get('Cookie'))
    if 'a' in cs and 'b' in cs:
        a = cs['a'].value
        if a in us:
            u = us[a]
            timestamp = time.time()
            if cs['b'].value in [s[0] for s in u[1] if s[1] > timestamp]:
                return (u, a)
    return ('', '')


def w(s, b):
    return s.wfile.write(
        bytes(
            '<title>TD</title><body style="max-width:800px;margin:auto;padding:16px">'
            + b + '</body>', d))


def h(s, error=None):
    form = c(
        ')Signup" style="float:left">Username<input style="display:block" type="text" name="a">Password<input style="display:block" type="password" name="b">(value="Signup"></form>'
    )
    w(s, '<h2>TODO</h2>' + ('<p>' + error + '</p>' if error else '') + form +
      form.replace('left', 'right').replace('Signup', 'Login'))


def c(s):
    return s.replace('^', 'display:inline-block;').replace(
        '@', 'background:none;border:none;cursor:pointer').replace(
            '(', '<input type="submit" ').replace(
                ')', '<form method="post" action="/')


def g(s):
    u, a = get_u(s)
    s.send_response(200)
    s.end_headers()
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
<input type="checkbox" style="display:none"/>
<h2 style="^margin:0">TODO</h2>
<p style="cursor:pointer;float:right;margin:8px">&#9881</p>
<div>
)l">
(style="float:right" value="Logout">
</form> 
)r">
Password
<input type="password" name="b">
New password
<input type="password" name="c">
(value="Reset password">
</form> 
</div>
</label>
<ul style="padding:0">''') + ''.join([
          c('<li style="display:block;border-top:1px solid black;">)e_t/') +
          k + c('" style="^">(style="@" value="&#974') + str(4 + int(e[1])) +
          c('''">
</form>
<p style="^width:calc(100% - 100px);overflow-wrap:break-word;text-decoration:'''
            ) + ('line-through' if e[1] else '') + '''">''' + e[0] + c('''</p>
)e_d/''') + k + c('''" style="^float:right;margin:16px">
(style="@" value='x'>
</form>
''') + '</li>' for k, e in u[2].items()
      ]) + c('''</ul>
)n">
<input type="text" style="^width:100%;margin-right:-45px;padding-right:45px" name="l">
(style="^@" value="+">
</form>'''))


def create_session_cookie(a):
    b = secrets.token_urlsafe()
    us[a][1].append((b, time.time() + 7**8))
    c, c['a'], c['b'] = SimpleCookie(), a, b
    return c


def p(s):
    body, u, p = parse_qs(s.rfile.read(int(
        s.headers.get('Content-Length')))), get_u(s), s.path
    u, n = u
    a, b = [body.get(c, [b''])[0].decode(d) for c in [b'a', b'b']]
    c = err = None
    if p == '/Login':
        if a in us and sha.verify(b, us[a][0]):
            u, c = us[a], create_session_cookie(a)
        else:
            err = 'Username or password incorrect'
    elif p == '/Signup':
        if a in us:
            err = 'Username %s already taken' % (a)
        else:
            us[a] = [sha.encrypt(b, rounds=r, salt_size=16), [], {}]
            u, c = us[a], create_session_cookie(a)
    elif p == '/l':
        c, c['a'], c['b'] = SimpleCookie(), '', ''
    if u and p == '/r':
        if sha.verify(body[b'b'][0].decode(), u[0]):
            u[0] = sha.encrypt(body[b'c'][0].decode(d), rounds=r, salt_size=16)
            u[1] = []
        else:
            s.send_response(401)
            s.end_headers()
            return s.wfile.write(b'<p>Password incorrect</p>')
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
        s.send_response(200)
        s.end_headers()
        h(s, err)
    else:
        f = open((a or n) + '.u', 'w+')
        f.write(u[0] + '\n')
        timestamp = time.time()
        u[1] = [s for s in u[1] if s[1] > timestamp]
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
