#!/usr/bin/python3
import http.server as z,os,secrets,time,uuid,urllib.parse
from http.cookies import SimpleCookie as v
from passlib.hash import pbkdf2_sha256 as q
k,d,j,l,s=200000,'utf-8',{},time.time,['']
def x(i):
	s[0]=f.readline()[:-1].split(',',2)
	return s[0][i]
m=lambda:range(int(x(0)))
for n in os.listdir('.'):
	if n[-2:]=='.u':f=open(n,'r');j[n[:-2]]=[x(0),[(x(0).replace('\a','\n'),float(s[0][1]))for i in m()],{s[0][1]:[x(2),s[0][0]=='True']for i in m()}]
def c(s,b=0):
	if b>5:return s
	for e in zip('ABCEFGHIJKMQVWXYZjqz[]?@$`',c('||||||||||||||||||||||||',b +1).split('|')):print(e);s=s.replace(*e)
	return s
def r(s,b,x=200,k=''):h=s.send_header;s.send_response(x);k and h('Set-Cookie',k.output(header='',sep=''));k!=''and h('Location','/');s.end_headers();b and s.wfile.write(bytes(c('<title>TODO</title><body style="max-width:800px;margin:auto;padding:16px">%s</body>'%b),d))
def p(s,e):
	u,n='',''
	w=s.headers.get
	x=v(w('Cookie'))
	if'a'in x and'b'in x:n=x['a'].value;u=j.get(n,[[]]);u[1]=[s for s in u[1]if s[1]>l()];u=x['b'].value in[s[0]for s in u[1]]and u
	if e and u:return r(s,c('<style>input:checked~div{display:block;display:inline-bloc}div{display:none}input{display:block;display:inline-bloc}</style><label><input type="checkbox" style="display:none"/><h2 style="display:block;display:inline-block;margin:0">TODO</h2><p style="cursor:pointer;float:right;margin:8px">&#9881</p><div><form method="post" action="l"><input type="submit"style="float:right" value="Logout"></form><form method="post" action="r">Password<input type="password" name="b">New password<input type="password" name="c"><input type="submit"value="Reset password"></form> </div></label><ul style=";padding:0">')+''.join(c('<li style="display:block;display:inline-bloc;border-top:1px solid black;"><form method="post" action="et%s" style="display:block;display:inline-block;"><input type="submit"style="background:none;border:none;cursor:pointer" value="&#974%s"></form><p style="display:block;display:inline-block;width:calc(100%% - 100px);overflow-wrap:break-word;text-decoration:%s">%s</p><form method="post" action="ed%s" style="display:block;display:inline-block;float:right;margin:16px"><input type="submit"style="background:none;border:none;cursor:pointer" value="x"></form></li>')%(k,4+int(e[1]),e[1]and'line-through',e[0],k)for k,e in u[2].items())+c('</ul><form method="post" action="n"><input type="text" style="display:block;display:inline-block;width:100%;margin-right:-45px;padding-right:45px" name="l"><input type="submit"style="display:block;display:inline-block;background:none;border:none;cursor:pointer" value="+"></form>'))
	o,p=urllib.parse.parse_qs(s.rfile.read(int(w('Content-Length')or'0'))),s.path
	a,b,i=[o.get(y,[b''])[0].decode(d)for y in[b'a',b'b',b'c']]
	a,x=a.replace('.','').replace('/',''),p[1:2]
	y=None
	if p[1:3]=='uL':
		if not(a in j and q.verify(b,j[a][0])):e=c('Username or password incorrect')
	elif x=='u':
		if a in j:e='Username %s already taken'%(a)
		else:j[a]=[q.encrypt(b,rounds=k,salt_size=16),[],{}]
	elif not u:e=' '
	f=c('<form method="post" action="uSignup" style="float:left">Username<input type="text" style="display:block;display:inline-bloc" name="a">Password<input type="password" name="b" style="display:block;display:inline-bloc"><input type="submit"value="Signup"></form>')
	if e:return r(s,c('<h2>TODO</h2><p>%s</p>%s%s')%(e,f,f.replace('left',c('right')).replace(c('Signup'),'Login')))
	if x=='u':t=secrets.token_urlsafe();j[a][1].append((t,l()+7**8));y,y['a'],y['b'],u=v(),a,t,j[a]
	if x=='l':y,y['a'],y['b']=v(),'',''
	if x=='r':
		if q.verify(b,u[0])<1:return r(s,c('<p>Password incorrect</p>'),401)
		u[0:2]=[q.encrypt(i,rounds=k,salt_size=16),[]]
	m=u[2]
	if x=='n':m[str(uuid.uuid4())]=[o[b'l'][0].decode(d),False]
	i=p[3:]
	if x=='e':
		if i not in m:return r(s,'',404)
		m[i][1]=m[i][1]<1
		if p[2:3]=='d':del m[i]
	f=open((a or n)+'.u','w+')
	f.write(u[0]+'\n')
	f.write(c('%s\n%s%s\n%s')%(len(u[1]),''.join('%s,%s\n'%(s[0].replace('\n','\a'),s[1])for s in u[1]),len(m.values()),''.join('%s,%s,%s\n'%(e[1],k,e[0])for k,e in m.items())))
	r(s,'',301,y)
class H(z.BaseHTTPRequestHandler):
	def do_GET(s):p(s,' ')
	def do_POST(s):p(s,'')
z.HTTPServer(('localhost',8080),H).serve_forever()
