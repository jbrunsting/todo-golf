#!/usr/bin/python3

from http.server import HTTPServer, BaseHTTPRequestHandler
from http.cookies import SimpleCookie
from urllib.parse import parse_qs
from passlib.hash import pbkdf2_sha256

import secrets
import time
import uuid
import os


class Entry:
    def __init__(self, id, label, done=False):
        self.id = id
        self.label = label
        self.done = done


class User:
    def __init__(self, username, pass_hash=None, sessions=[]):
        self.username = username
        self.pass_hash = pass_hash
        self.sessions = []
        self.entries = {}

    def save(self):
        f = open(self.username + '.user', 'w+')
        f.write(self.pass_hash + '\n')
        f.write(str(len(self.sessions)) + '\n')
        for s in self.sessions:
            f.write(s[0].replace('\n', '\a') + ',' + str(s[1]) + '\n')
        f.write(str(len(self.entries.values())) + '\n')
        for e in self.entries.values():
            f.write(str(e.done) + ',' + e.id + ',' + e.label + '\n')

    def load(self):
        f = open(self.username + '.user', 'r')
        self.pass_hash = f.readline()[:-1]
        self.sessions = []
        ns = int(f.readline())
        for i in range(ns):
            s = f.readline()[:-1].split(',', 1)
            self.sessions.append((s[0].replace('\a', '\n'), s[1]))
        self.entries = {}
        ne = int(f.readline()[:-1])
        for i in range(ne):
            e = f.readline()[:-1].split(',', 2)
            self.entries[e[1]] = Entry(e[1], e[2], e[0] == 'True')


users = {}

for f in os.listdir('.'):
    if f.endswith('.user'):
        users[f[:-5]] = User(f[:-5])
        users[f[:-5]].load()


class H(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super(H, self).__init__(*args, **kwargs)

    def get_auth_user(self):
        cookies = SimpleCookie(self.headers.get('Cookie'))
        if 'username' in cookies and 'session_token' in cookies:
            username = cookies['username'].value
            session_token = cookies['session_token'].value
            if username in users:
                user = users[username]
                timestamp = time.time()
                if session_token in [
                        s[0] for s in user.sessions if float(s[1]) > timestamp
                ]:
                    return user
        return None

    def get_entry_html(self, e):
        return '''
        <form style="display:inline-block" action="/toggle_done/''' + e.id + '''" method="post">
            <input style="background:none;border:none;cursor:pointer" type="submit" value="''' + ('&#9745' if e.done else '&#9744') + '''">
        </form>
        <p style="display:inline-block;width:calc(100% - 100px);overflow-wrap:break-word;text-decoration:''' + ('line-through' if e.done else '') + '''">''' + e.label + '''</p> 
        <form style="display:inline-block;float:right;margin:16px" action="/delete_entry/''' + e.id + '''" method="post">
            <input style="background:none;border:none;cursor:pointer" type="submit" value='x'>
        </form>
        '''

    def render_home(self, error=None):
        self.wfile.write(bytes('''
            <html>
                <head><title>TD</title></head>
                <body style="max-width:800px;margin:auto;padding:16px">
                    <h2>TODO</h2>''' +
                    ('<p>' + error + '</p>' if error else '')
                    + '''<form style="float:left" action="/signup" method="post">
                        <label for="username">Username</label>
                        <input style="display:block" type="text" name="username">
                        <label for="password">Password</label>
                        <input style="display:block" type="password" name="password">
                        <input type="submit" value="Signup">
                    </form> 
                    <form style="float:right" action="/login" method="post">
                        <label for="username">Username</label>
                        <input style="display:block" type="text" name="username">
                        <label for="password">Password</label>
                        <input style="display:block" type="password" name="password">
                        <input type="submit" value="Login">
                    </form> 
                </body>
            </html>
        ''', 'utf-8'))

    def do_GET(self):
        user = self.get_auth_user()
        if user:
            self.send_response(200)
            self.end_headers()
            self.wfile.write(
                bytes('''
                <html>
                    <head><title>TD</title></head>
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
                            '<li style="display:block;border-top:1px solid black;">' + self.get_entry_html(e) + '</li>'
                    for e in user.entries.values()
                ]) + '''</ul>
                        <form action="/new_entry" method="post">
                            <input style="width:100%;margin-right:-45px;padding-right:45px" type="text" name="label">
                            <input style="width:35px;padding:0;margin:0;cursor:pointer;background:none;border:none" type="submit" value="+">
                        </form> 
                    </body>
                </html>
            ''', 'utf-8'))
            return

        self.send_response(200)
        self.end_headers()
        self.render_home()

    def create_session_go_home(self, user):
        session_token = secrets.token_urlsafe()
        user.sessions.append((session_token, time.time() + 60 * 60 * 24 * 30))
        user.save()

        cookie = SimpleCookie()
        cookie['username'] = user.username
        cookie['session_token'] = session_token
        self.send_response(301)
        self.send_header('Set-Cookie', cookie.output(header='', sep=''))
        self.send_header('Location', '/')
        self.end_headers()

    def do_POST(self):
        content_len = int(self.headers.get('Content-Length'))
        body = parse_qs(self.rfile.read(content_len))

        if self.path == '/login':
            username = body[b'username'][0].decode('utf-8')
            password = body[b'password'][0].decode('utf-8')

            if username not in users:
                self.send_response(404)
                self.end_headers()
                self.render_home('Username or password incorrect')
                return

            user = users[username]
            print("Verifying hash " + user.pass_hash)
            if pbkdf2_sha256.verify(password, user.pass_hash):
                self.create_session_go_home(user)
                return
            else:
                self.send_response(401)
                self.end_headers()
                self.render_home('Username or password incorrect')
                return
        elif self.path == '/logout':
            cookie = SimpleCookie()
            cookie['session_token'] = ''
            self.send_response(301)
            self.send_header('Set-Cookie', cookie.output(header='', sep=''))
            self.send_header('Location', '/')
            self.end_headers()
        elif self.path == '/signup':
            username = body[b'username'][0].decode('utf-8')
            password = body[b'password'][0].decode('utf-8')

            if username in users:
                self.send_response(400)
                self.end_headers()
                self.render_home('Username \'' + username + '\' already taken')
                return
            else:
                pass_hash = pbkdf2_sha256.encrypt(
                    password, rounds=200000, salt_size=16)
                users[username] = User(username, pass_hash)
                self.create_session_go_home(users[username])
                return
        elif self.path == '/reset_password':
            user = self.get_auth_user()
            password = body[b'password'][0].decode('utf-8')
            new_password = body[b'new_password'][0].decode('utf-8')
            if user:
                if pbkdf2_sha256.verify(password, user.pass_hash):
                    user.pass_hash = pbkdf2_sha256.encrypt(
                        new_password, rounds=200000, salt_size=16)
                    user.sessions = []
                    user.save()
                else:
                    self.send_response(401)
                    self.end_headers()
                    self.wfile.write(b'Password incorrect')
                    return
        elif self.path == '/new_entry':
            user = self.get_auth_user()
            if user:
                label = body[b'label'][0].decode('utf-8')
                id = str(uuid.uuid4())
                user.entries[id] = Entry(id, label)
                user.save()
        elif self.path.startswith('/toggle_done'):
            user = self.get_auth_user()
            id = self.path.split('/', 2)[2]
            user.entries[id].done = not user.entries[id].done
            user.save()
        elif self.path.startswith('/delete_entry'):
            user = self.get_auth_user()
            id = self.path.split('/', 2)[2]
            del user.entries[id]
            user.save()
        else:
            self.send_response(404)
            self.send_header('Location', '/')
            self.end_headers()
            return

        self.send_response(301)
        self.send_header('Location', '/')
        self.end_headers()


HTTPServer(('localhost', 8080), H).serve_forever()
