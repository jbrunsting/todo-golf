#!/usr/bin/python3

from http.server import HTTPServer, BaseHTTPRequestHandler
from http.cookies import SimpleCookie
from urllib.parse import parse_qs
from passlib.hash import pbkdf2_sha256

import secrets
import time

users = {}


class User:
    def __init__(self,
                 username,
                 pass_hash,
                 sessions=[]):
        self.username = username
        self.pass_hash = pass_hash
        self.sessions = [] # TODO: Use expiry


class H(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super(H, self).__init__(*args, **kwargs)

    def do_GET(self):
        cookies = SimpleCookie(self.headers.get('Cookie'))
        if 'username' in cookies and 'session_token' in cookies:
            username = cookies['username'].value
            session_token = cookies['session_token'].value
            if username in users:
                user = users[username]
                timestamp = time.time()
                if session_token in [s[0] for s in user.sessions if s[1] > timestamp]:
                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(
                        bytes("""
                        <html>
                            <head><title>TD</title></head>
                            <body>
                                <h1>Logged in as """ + str(username) + """</h1>
                            </body>
                        </html>
                    """, 'utf-8'))
                    return

        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"""
            <html>
                <head><title>TD</title></head>
                <body>
                    <h1>TD</h1>
                    <h2>Login</h2>
                    <form action="/login" method="post">
                        <input type="text" name="username">
                        <input type="text" name="password">
                        <input type="submit" value="Submit">
                    </form> 
                    <h2>Signup</h2>
                    <form action="/signup" method="post">
                        <input type="text" name="username">
                        <input type="text" name="password">
                        <input type="submit" value="Submit">
                    </form> 
                </body>
            </html>
        """)

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
        username = body[b'username'][0].decode('utf-8')
        password = body[b'password'][0].decode('utf-8')

        if self.path == '/login':
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

        self.send_response(404)
        self.send_header('Location', '/')
        self.end_headers()


HTTPServer(('localhost', 8080), H).serve_forever()
