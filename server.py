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
        u[2][e[1]] = [e[1], e[2], e[0] == 'True']


class H(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super(H, self).__init__(*args, **kwargs)

    def get_u(self):
        cs = SimpleCookie(self.headers.get('Cookie'))
        if 'a' in cs and 'b' in cs:
            a = cs['a'].value
            if a in us:
                u = us[a]
                timestamp = time.time()
                if cs['b'].value in [s[0] for s in u[1] if s[1] > timestamp]:
                    return u
        return None

    def write_html(self, b):
        return self.wfile.write(
            bytes(
                '<title>TD</title><body style="max-width:800px;margin:auto;padding:16px">'
                + b + '</body>', d))

    def render_home(self, error=None):
        form = '''
        <form style="float:left" action="/Signup" method="post">
            Username
            <input style="display:block" type="text" name="a">
            Password
            <input style="display:block" type="password" name="b">
            <input type="submit" value="Signup">
        </form>'''
        self.write_html('<h2>TODO</h2>' + (
            '<p>' + error + '</p>' if error else ''
        ) + form + form.replace('left', 'right').replace('Signup', 'Login'))

    def do_GET(self):
        u = self.get_u()
        self.send_response(200)
        self.end_headers()
        if not u:
            return self.render_home()

        self.write_html('''
        <style>
            input:checked~div{display: block}
            div{display:none}
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
                    <input style="display:block" type="password" name="b">
                    New password
                    <input style="display:block" type="password" name="c">
                    <input type="submit" value="Reset password">
                </form> 
            </div>
        </label>
        <ul style="padding:0">''' + ''.join([
            '<li style="display:block;border-top:1px solid black;"><form style="display:inline-block" action="/e_t/'
            + e[0] +
            '" method="post"><input style="background:none;border:none;cursor:pointer" type="submit" value="&#974'
            + str(4 + int(e[2])) + '''">
                </form>
                <p style="display:inline-block;width:calc(100% - 100px);overflow-wrap:break-word;text-decoration:'''
            + ('line-through' if e[2] else '') + '''">''' + e[1] + '''</p> 
                <form style="display:inline-block;float:right;margin:16px" action="/e_d/'''
            + e[0] + '''" method="post">
                    <input style="background:none;border:none;cursor:pointer" type="submit" value='x'>
                </form>
                ''' + '</li>' for e in u[2].values()
        ]) + '''</ul>
        <form action="/n" method="post">
            <input style="width:100%;margin-right:-45px;padding-right:45px" type="text" name="l">
            <input style="width:35px;padding:0;margin:0;cursor:pointer;background:none;border:none" type="submit" value="+">
        </form>''')

    def create_session_cookie(self, a):
        b = secrets.token_urlsafe()
        us[a][1].append((b, time.time() + 7**8))
        c, c['a'], c['b'] = SimpleCookie(), a, b
        return c

    def do_POST(self):
        body, u = parse_qs(
            self.rfile.read(int(
                self.headers.get('Content-Length')))), self.get_u()
        a, b = [body.get(c, [b''])[0].decode(d) for c in [b'a', b'b']]
        c = err = None

        if self.path == '/Login':
            if a in us:
                u = us[a]
                if pbkdf2_sha256.verify(b, us[a][0]):
                    c = self.create_session_cookie(a)
                else:
                    err = (401, 'Username or password incorrect')
            else:
                err = (404, 'Username or password incorrect')
        elif self.path == '/Signup':
            if a in us:
                err = (400, 'Username \'' + a + '\' already taken')
            else:
                us[a] = [
                    a,
                    pbkdf2_sha256.encrypt(b, rounds=r, salt_size=16), [], {}
                ]
                u, c = us[a], self.create_session_cookie(a)
        elif self.path == '/l':
            c, c['a'], c['b'] = SimpleCookie(), '', ''
        elif self.path == '/r':
            if u:
                if pbkdf2_sha256.verify(body[b'b'][0].decode(), u[0]):
                    u[0] = pbkdf2_sha256.encrypt(
                        body[b'c'][0].decode(d), rounds=r, salt_size=16)
                    u[1] = []
                else:
                    self.send_response(401)
                    self.end_headers()
                    return self.wfile.write(b'<p>Password incorrect</p>')
        elif self.path == '/n':
            if u:
                id = str(uuid.uuid4())
                u[2][id] = [id, body[b'l'][0].decode(d), False]
        elif self.path.startswith('/e_t') or self.path.startswith('/e_d'):
            id = self.path.split('/', 2)[2]
            u[2][id][2] = not u[2][id][2]
            if self.path.startswith('/e_d'):
                del u[2][id]
        else:
            err = (404, '')

        if err:
            self.send_response(err[0])
            self.end_headers()
            self.render_home(err[1])
        else:
            f = open(a + '.u', 'w+')
            f.write(u[0] + '\n')
            timestamp = time.time()
            u[1] = [s for s in u[1] if s[1] > timestamp]
            f.write(
                str(len(u[1])) + '\n' + ''.join(
                    s[0].replace('\n', '\a') + ',' + str(s[1]) + '\n'
                    for s in u[1]) + str(len(u[2].values())) + '\n' + ''.join(
                        str(e[2]) + ',' + e[0] + ',' + e[1] + '\n'
                        for e in u[2].values()))
            self.send_response(301)
            if c:
                self.send_header('Set-Cookie', c.output(header='', sep=''))
            self.send_header('Location', '/')
            self.end_headers()


HTTPServer(('localhost', 8080), H).serve_forever()
