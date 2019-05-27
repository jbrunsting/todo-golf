#!/usr/bin/python3

from http.server import HTTPServer, BaseHTTPRequestHandler
from http.cookies import SimpleCookie
from urllib.parse import parse_qs
from passlib.hash import pbkdf2_sha256

import secrets
import time
import uuid
import os


def save(u):
    f = open(u[0] + '.u', 'w+')
    f.write(u[1] + '\n')
    timestamp = time.time()
    u[2] = [s for s in u[2] if s[1] > timestamp]
    f.write(str(len(u[2])) + '\n' + ''.join(s[0].replace('\n', '\a') + ',' + str(s[1]) + '\n' for s in u[2]) + str(len(u[3].values())) + '\n' + ''.join(str(e[2]) + ',' + e[0] + ',' + e[1] + '\n' for e in u[3].values()))

def load(u):
    f = open(u[0] + '.u', 'r')
    u[1] = f.readline()[:-1]
    u[2] = []
    ns = int(f.readline())
    for i in range(ns):
        s = f.readline()[:-1].split(',', 1)
        u[2].append((s[0].replace('\a', '\n'), float(s[1])))
    u[3] = {}
    ne = int(f.readline()[:-1])
    for i in range(ne):
        e = f.readline()[:-1].split(',', 2)
        u[3][e[1]] = [e[1], e[2], e[0] == 'True']


us = {}

for f in os.listdir('.'):
    if f.endswith('.u'):
        us[f[:-2]] = [f[:-2], None, [], {}]
        load(us[f[:-2]])


class H(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super(H, self).__init__(*args, **kwargs)

    def get_u(self):
        cookies = SimpleCookie(self.headers.get('Cookie'))
        if 'uname' in cookies and 'session_token' in cookies:
            uname = cookies['uname'].value
            if uname in us:
                u = us[uname]
                timestamp = time.time()
                if cookies['session_token'].value in [
                        s[0] for s in u[2] if s[1] > timestamp
                ]:
                    return u
        return None

    def get_entry_html(self, e):
        return '''
        <form style="display:inline-block" action="/e_t/''' + e[0] + '''" method="post">
            <input style="background:none;border:none;cursor:pointer" type="submit" value="''' + (
            '&#9745' if e[2] else '&#9744') + '''">
        </form>
        <p style="display:inline-block;width:calc(100% - 100px);overflow-wrap:break-word;text-decoration:''' + (
                'line-through'
                if e[2] else '') + '''">''' + e[1] + '''</p> 
        <form style="display:inline-block;float:right;margin:16px" action="/e_d/''' + e[0] + '''" method="post">
            <input style="background:none;border:none;cursor:pointer" type="submit" value='x'>
        </form>
        '''

    def render_home(self, error=None):
        self.wfile.write(
            bytes('''
            <title>TD</title>
            <body style="max-width:800px;margin:auto;padding:16px">
                <h2>TODO</h2>''' + ('<p>' + error + '</p>' if error else '') +
                  '''<form style="float:left" action="/signup" method="post">
                    <label for="uname">Username</label>
                    <input style="display:block" type="text" name="uname">
                    <label for="password">Password</label>
                    <input style="display:block" type="password" name="password">
                    <input type="submit" value="Signup">
                </form> 
                <form style="float:right" action="/login" method="post">
                    <label for="uname">Username</label>
                    <input style="display:block" type="text" name="uname">
                    <label for="password">Password</label>
                    <input style="display:block" type="password" name="password">
                    <input type="submit" value="Login">
                </form> 
            </body>
        ''', 'utf-8'))

    def do_GET(self):
        u = self.get_u()
        if u:
            self.send_response(200)
            self.end_headers()
            self.wfile.write(
                bytes('''
                <title>TD</title>
                <body style="max-width:800px;margin:auto;padding:16px">
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
                            <form action="/logout" method="post">
                                <input style="float:right" type="submit" value="Logout">
                            </form> 
                            <form action="/reset_password" method="post">
                                <label for="password">Password</label>
                                <input style="display:block" type="password" name="password">
                                <label for="new_password">New password</label>
                                <input style="display:block" type="password" name="new_password">
                                <input type="submit" value="Reset password">
                            </form> 
                        </div>
                    </label>
                    <ul style="padding:0">''' + ''.join([
                    '<li style="display:block;border-top:1px solid black;">' +
                    self.get_entry_html(e) + '</li>'
                    for e in u[3].values()
                ]) + '''</ul>
                    <form action="/new_entry" method="post">
                        <input style="width:100%;margin-right:-45px;padding-right:45px" type="text" name="label">
                        <input style="width:35px;padding:0;margin:0;cursor:pointer;background:none;border:none" type="submit" value="+">
                    </form> 
                </body>
            ''', 'utf-8'))
            return

        self.send_response(200)
        self.end_headers()
        self.render_home()

    def create_session_cookie(self, u):
        session_token = secrets.token_urlsafe()
        u[2].append((session_token, time.time() + 7**8))
        cookie = SimpleCookie()
        cookie['uname'] = u[0]
        cookie['session_token'] = session_token
        return cookie

    def do_POST(self):
        content_len = int(self.headers.get('Content-Length'))
        body = parse_qs(self.rfile.read(content_len))
        u = self.get_u()
        uname = body.get(b'uname', [b''])[0].decode('utf-8')
        password = body.get(b'password', [b''])[0].decode('utf-8')
        cookie = err = None

        if self.path == '/login':
            if uname in us:
                u = us[uname]
                if pbkdf2_sha256.verify(password, u[1]):
                    cookie = self.create_session_cookie(u)
                else:
                    err = (401, 'Username or password incorrect')
            else:
                err = (404, 'Username or password incorrect')
        elif self.path == '/signup':
            if uname in us:
                err = (400, 'Username \'' + uname + '\' already taken')
            else:
                pass_hash = pbkdf2_sha256.encrypt(
                    password, rounds=200000, salt_size=16)
                u = [uname, pass_hash, [], {}]
                us[uname] = u
                cookie = self.create_session_cookie(us[uname])
        elif self.path == '/logout':
            cookie = SimpleCookie()
            cookie['session_token'] = ''
        elif self.path == '/reset_password':
            if u:
                if pbkdf2_sha256.verify(body[b'password'][0].decode('utf-8'),
                                        u[1]):
                    u.pass_hash = pbkdf2_sha256.encrypt(
                        body[b'new_password'][0].decode('utf-8'),
                        rounds=200000,
                        salt_size=16)
                    u[2] = []
                else:
                    self.send_response(401)
                    self.end_headers()
                    self.wfile.write(b'<p>Password incorrect</p>')
                    return
        elif self.path == '/new_entry':
            if u:
                label = body[b'label'][0].decode('utf-8')
                id = str(uuid.uuid4())
                u[3][id] = [id, label, False]
        elif self.path.startswith('/e_t') or self.path.startswith('/e_d'):
            id = self.path.split('/', 2)[2]
            if self.path.startswith('/e_t'):
                u[3][id][2] = not u[3][id][2]
            else:
                del u[3][id]
        else:
            err = (404, '')

        if err:
            self.send_response(err[0])
            self.end_headers()
            self.render_home(err[1])
        else:
            save(u)
            self.send_response(301)
            if cookie:
                self.send_header('Set-Cookie', cookie.output(header='', sep=''))
            self.send_header('Location', '/')
            self.end_headers()


HTTPServer(('localhost', 8080), H).serve_forever()
