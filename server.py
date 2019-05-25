#!/usr/bin/python3

from http.server import HTTPServer, BaseHTTPRequestHandler
from http.cookies import SimpleCookie
from urllib.parse import parse_qs
from passlib.hash import pbkdf2_sha256

import secrets
import time
import uuid

users = {}


class Entry:
    def __init__(self, id, label, done=False):
        self.id = id
        self.label = label
        self.done = done


class User:
    def __init__(self, username, pass_hash, sessions=[]):
        self.username = username
        self.pass_hash = pass_hash
        self.sessions = []  # TODO: Use expiry
        self.entries = {}


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
                        s[0] for s in user.sessions if s[1] > timestamp
                ]:
                    return user
        return None

    def get_entry_html(self, e):
        return '''<p>''' + e.label + '''</p><form action="/update_entry/''' + e.id + '''" method="post">
            <input type="checkbox" name="done" ''' + ('checked'
                                                      if e.done else '') + '''>
            <input type="submit" value="Submit">
        </form><form action="/delete_entry/''' + e.id + '''" method="post">
            <input type="submit" value="Delete">
        </form>'''

    def do_GET(self):
        user = self.get_auth_user()
        if user:
            self.send_response(200)
            self.end_headers()
            self.wfile.write(
                bytes('''
                <html>
                    <head><title>TD</title></head>
                    <body>
                        <h1>Logged in as ''' + str(user.username) + '''</h1>
                    </body>
                    <ul>''' + ''.join([
                    '<li>' + self.get_entry_html(e) + '</li>'
                    for e in user.entries.values()
                ]) + '''</ul>
                    <h2>New entry</h2>
                    <form action="/new_entry" method="post">
                        <input type="text" name="label">
                        <input type="submit" value="Submit">
                    </form> 
                    <h2>Reset password</h2>
                    <form action="/reset_password" method="post">
                        <input type="password" name="password">
                        <input type="password" name="new_password">
                        <input type="submit" value="Submit">
                    </form> 
                </html>
            ''', 'utf-8'))
            return

        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'''
            <html>
                <head><title>TD</title></head>
                <body>
                    <h1>TD</h1>
                    <h2>Login</h2>
                    <form action="/login" method="post">
                        <input type="text" name="username">
                        <input type="password" name="password">
                        <input type="submit" value="Submit">
                    </form> 
                    <h2>Signup</h2>
                    <form action="/signup" method="post">
                        <input type="text" name="username">
                        <input type="password" name="password">
                        <input type="submit" value="Submit">
                    </form> 
                </body>
            </html>
        ''')

    def create_session_go_home(self, user):
        session_token = secrets.token_urlsafe()
        user.sessions.append((session_token, time.time() + 60 * 60 * 24 * 30))

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
                self.wfile.write(
                    bytes('User \'' + username + '\' not found', 'utf-8'))
                return

            user = users[username]
            if pbkdf2_sha256.verify(password, user.pass_hash):
                self.create_session_go_home(user)
                return
            else:
                self.send_response(401)
                self.end_headers()
                self.wfile.write(b'Password incorrect')
                return
        elif self.path == '/signup':
            username = body[b'username'][0].decode('utf-8')
            password = body[b'password'][0].decode('utf-8')

            if username in users:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(
                    bytes('Username \'' + username + '\' already taken ',
                          'utf-8'))
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
        elif self.path.startswith('/update_entry'):
            user = self.get_auth_user()
            id = self.path.split('/', 2)[2]
            if b'done' in body:
                done = body[b'done'][0].decode('utf-8') == 'on'
                user.entries[id].done = done
        elif self.path.startswith('/delete_entry'):
            user = self.get_auth_user()
            id = self.path.split('/', 2)[2]
            del user.entries[id]
        else:
            self.send_response(404)
            self.send_header('Location', '/')
            self.end_headers()

        self.send_response(301)
        self.send_header('Location', '/')
        self.end_headers()


HTTPServer(('localhost', 8080), H).serve_forever()
