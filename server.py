#!/usr/bin/python3

from http.server import HTTPServer, BaseHTTPRequestHandler
from http.cookies import SimpleCookie
from urllib.parse import parse_qs
from passlib.hash import pbkdf2_sha256

import secrets
import time
import uuid
import os

d = 'utf-8'
us = {}

for f in os.listdir('.'):
    if not f.endswith('.u'): continue
    u = [f[:-2], None, [], {}]
    us[f[:-2]] = u
    f = open(u[0] + '.u', 'r')
    u[1] = f.readline()[:-1]
    u[2] = []
    for i in range(int(f.readline())):
        s = f.readline()[:-1].split(',', 1)
        u[2].append((s[0].replace('\a', '\n'), float(s[1])))
    u[3] = {}
    for i in range(int(f.readline())):
        e = f.readline()[:-1].split(',', 2)
        u[3][e[1]] = [e[1], e[2], e[0] == 'True']


class H(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super(H, self).__init__(*args, **kwargs)

    def get_u(self):
        cookies = SimpleCookie(self.headers.get('Cookie'))
        if 'a' in cookies and 'b' in cookies:
            a = cookies['a'].value
            if a in us:
                u = us[a]
                timestamp = time.time()
                if cookies['b'].value in [
                        s[0] for s in u[2] if s[1] > timestamp
                ]:
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
            <label for="a">Username</label>
            <input style="display:block" type="text" name="a">
            <label for="b">Password</label>
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
            self.render_home()
            return

        self.write_html('''
        <style>
            input:checked ~ div {
                display: block;
            }
            div {
                display: none;
            }
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
                    <label for="b">Password</label>
                    <input style="display:block" type="password" name="b">
                    <label for="c">New password</label>
                    <input style="display:block" type="password" name="c">
                    <input type="submit" value="Reset password">
                </form> 
            </div>
        </label>
        <ul style="padding:0">''' + ''.join([
            '<li style="display:block;border-top:1px solid black;">' + '''
                <form style="display:inline-block" action="/e_t/''' + e[0] +
            '''" method="post">
                    <input style="background:none;border:none;cursor:pointer" type="submit" value="&#974'''
            + str(4 + int(e[2])) + '''">
                </form>
                <p style="display:inline-block;width:calc(100% - 100px);overflow-wrap:break-word;text-decoration:'''
            + ('line-through' if e[2] else '') + '''">''' + e[1] + '''</p> 
                <form style="display:inline-block;float:right;margin:16px" action="/e_d/'''
            + e[0] + '''" method="post">
                    <input style="background:none;border:none;cursor:pointer" type="submit" value='x'>
                </form>
                ''' + '</li>' for e in u[3].values()
        ]) + '''</ul>
        <form action="/n" method="post">
            <input style="width:100%;margin-right:-45px;padding-right:45px" type="text" name="label">
            <input style="width:35px;padding:0;margin:0;cursor:pointer;background:none;border:none" type="submit" value="+">
        </form>''')

    def create_session_cookie(self, u):
        b = secrets.token_urlsafe()
        u[2].append((b, time.time() + 7**8))
        cookie = SimpleCookie()
        cookie['a'] = u[0]
        cookie['b'] = b
        return cookie

    def do_POST(self):
        content_len = int(self.headers.get('Content-Length'))
        body = parse_qs(self.rfile.read(content_len))
        u = self.get_u()
        a, b = [body.get(c, [b''])[0].decode(d) for c in [b'a', b'b']]
        cookie = err = None

        if self.path == '/Login':
            if a in us:
                u = us[a]
                if pbkdf2_sha256.verify(b, u[1]):
                    cookie = self.create_session_cookie(u)
                else:
                    err = (401, 'Username or password incorrect')
            else:
                err = (404, 'Username or password incorrect')
        elif self.path == '/Signup':
            if a in us:
                err = (400, 'Username \'' + a + '\' already taken')
            else:
                pass_hash = pbkdf2_sha256.encrypt(
                    b, rounds=200000, salt_size=16)
                u = [a, pass_hash, [], {}]
                us[a] = u
                cookie = self.create_session_cookie(us[a])
        elif self.path == '/l':
            cookie = SimpleCookie()
            cookie['a'] = ''
            cookie['b'] = ''
        elif self.path == '/r':
            if u:
                if pbkdf2_sha256.verify(body[b'b'][0].decode(), u[1]):
                    u.pass_hash = pbkdf2_sha256.encrypt(
                        body[b'c'][0].decode(d), rounds=200000, salt_size=16)
                    u[2] = []
                else:
                    self.send_response(401)
                    self.end_headers()
                    self.wfile.write(b'<p>Password incorrect</p>')
                    return
        elif self.path == '/n':
            if u:
                label = body[b'label'][0].decode(d)
                id = str(uuid.uuid4())
                u[3][id] = [id, label, False]
        elif self.path.startswith('/e_t') or self.path.startswith('/e_d'):
            id = self.path.split('/', 2)[2]
            u[3][id][2] = not u[3][id][2]
            if self.path.startswith('/e_d'):
                del u[3][id]
        else:
            err = (404, '')

        if err:
            self.send_response(err[0])
            self.end_headers()
            self.render_home(err[1])
        else:
            f = open(u[0] + '.u', 'w+')
            f.write(u[1] + '\n')
            timestamp = time.time()
            u[2] = [s for s in u[2] if s[1] > timestamp]
            f.write(
                str(len(u[2])) + '\n' + ''.join(
                    s[0].replace('\n', '\a') + ',' + str(s[1]) + '\n'
                    for s in u[2]) + str(len(u[3].values())) + '\n' + ''.join(
                        str(e[2]) + ',' + e[0] + ',' + e[1] + '\n'
                        for e in u[3].values()))
            self.send_response(301)
            if cookie:
                self.send_header('Set-Cookie', cookie.output(
                    header='', sep=''))
            self.send_header('Location', '/')
            self.end_headers()


HTTPServer(('localhost', 8080), H).serve_forever()
