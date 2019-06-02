#!/usr/bin/python3

import os
import secrets
import time
import uuid
from http.cookies import SimpleCookie
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs

from passlib.hash import pbkdf2_sha256

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
    return (None, None)

def w(s, b):
    return s.wfile.write(
        bytes(
            '<title>TD</title><body style="max-width:800px;margin:auto;padding:16px">'
            + b + '</body>', d))

def h(s, error=None):
    form = '''
    <form style="float:left" action="/Signup" method="post">
        Username
        <input style="display:block" type="text" name="a">
        Password
        <input style="display:block" type="password" name="b">
        <input type="submit" value="Signup">
    </form>'''
    w(s, '<h2>TODO</h2>' + (
        '<p>' + error + '</p>' if error else ''
    ) + form + form.replace('left', 'right').replace('Signup', 'Login'))

def g(s):
    u, a = get_u(s)
    s.send_response(200)
    s.end_headers()
    if not u:
        return h(s)

    w(s, '''
    <style>
        input:checked~div{display: block}
        div{display:none}
        input{display:block}
    </style>
    <label>
        <input style="display:none" type="checkbox"/>
        <h2 style="display:inline-block;margin:0">TODO</h2>
        <p style="cursor:pointer;float:right;margin:8px">&#9881</p>
        <div>
            <form action="/l" method="post">
                <input style="float:right" type="submit" value="Logout">
            </form> 
            <form action="/r" method="post">
                Password
                <input type="password" name="b">
                New password
                <input type="password" name="c">
                <input type="submit" value="Reset password">
            </form> 
        </div>
    </label>
    <ul style="padding:0">''' + ''.join([
        '<li style="display:block;border-top:1px solid black;"><form style="display:inline-block" action="/e_t/'
        + k +
        '" method="post"><input style="background:none;border:none;cursor:pointer" type="submit" value="&#974'
        + str(4 + int(e[1])) + '''">
            </form>
            <p style="display:inline-block;width:calc(100% - 100px);overflow-wrap:break-word;text-decoration:'''
        + ('line-through' if e[1] else '') + '''">''' + e[0] + '''</p>
            <form style="display:inline-block;float:right;margin:16px" action="/e_d/'''
        + k + '''" method="post">
                <input style="background:none;border:none;cursor:pointer" type="submit" value='x'>
            </form>
            ''' + '</li>' for k, e in u[2].items()
    ]) + '''</ul>
    <form action="/n" method="post">
        <input style="display:inline-block;width:100%;margin-right:-45px;padding-right:45px" type="text" name="l">
        <input style="display:inline-block;cursor:pointer;background:none;border:none" type="submit" value="+">
    </form>''')

def create_session_cookie(a):
    b = secrets.token_urlsafe()
    us[a][1].append((b, time.time() + 7**8))
    c, c['a'], c['b'] = SimpleCookie(), a, b
    return c

def p(s):
    body, u, p = parse_qs(
        s.rfile.read(int(
            s.headers.get('Content-Length')))), get_u(s), s.path
    u, n = u
    a, b = [body.get(c, [b''])[0].decode(d) for c in [b'a', b'b']]
    c = err = None
    if p == '/Login':
        if a in us and pbkdf2_sha256.verify(b, us[a][0]):
            u, c = us[a], create_session_cookie(a)
        else:
            err = 'Username or password incorrect'
    elif p == '/Signup':
        if a in us:
            err = 'Username %s already taken' % (a)
        else:
            us[a] = [
                pbkdf2_sha256.encrypt(b, rounds=r, salt_size=16), [], {}
            ]
            u, c = us[a], create_session_cookie(a)
    elif p == '/l':
        c, c['a'], c['b'] = SimpleCookie(), '', ''
    if u and p == '/r':
        if pbkdf2_sha256.verify(body[b'b'][0].decode(), u[0]):
            u[0] = pbkdf2_sha256.encrypt(
                body[b'c'][0].decode(d), rounds=r, salt_size=16)
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


class H(BaseHTTPRequestHandler):
    def __init__(s, *args, **kwargs):
        super(H, s).__init__(*args, **kwargs)

    def do_GET(s):
        g(s)

    def do_POST(s):
        p(s)


HTTPServer(('localhost', 8080), H).serve_forever()
