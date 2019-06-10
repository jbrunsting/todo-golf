#!/usr/bin/python3
import http.server,os,secrets,time,uuid,urllib.parse
from http.cookies import SimpleCookie as v
from passlib.hash import pbkdf2_sha256 as q
k,d,j,l,s=200000,'utf-8',{},time.time,['']
for n in os.listdir('.'):
	if n[-2:]!='.u':continue
	f=open(n,'r')
	def x(c):s[0]=r()[:-1].split(',',c)
	m,r=lambda:range(int(r())),f.readline
	j[n[:-2]]=u=[r()[:-1],[x(1)or(s[0][0].replace('\a','\n'),float(s[0][1]))for i in m()],{s[0][1]:x(2)or[s[0][2],s[0][0]=='True']for i in m()}]
def z(s):
	c=v(s.headers.get('Cookie'))
	if'a'in c and'b'in c:
		a=c['a'].value
		if a in j and c['b'].value in[s[0]for s in j[a][1]if s[1]>l()]:return(j[a],a)
	return'',''
def c(s,b=0):
	if b>5:return s
	for e in zip('[^@?_!]ZYXMQAWBGIFVJKCH$`',c('<I typeY|Finline-`;|background:none;border:none;M|[submit"|<X methodYpost" actionY/|Q[pQ" JY| GY|</|="|form|cursor:pointer|assword|UserJ|margin|right|style|input|display:|Signup|name|%s|value|TODO|float:|block',b +1).split('|')):s=s.replace(*e)
	return s
w,f,h=lambda s,b:s.wfile.write(bytes(c('<title>HZtitle><body]max-width:800px;W:auto;padding:16px">%sZbody>'%b),d)),c('_uV"]$left">A[text"]F`" JYa">P!b"]F`">?CYV">ZX>'),lambda s,e='':w(s,c('<h2>HZh2><p>KZp>KK')%(e,f,f.replace('left',c('B')).replace(c('V'),'Login')))
def r(s,c,k=''):s.send_response(c);k and s.send_header('Set-Cookie',k.output(header='',sep=''));k!=''and s.send_header('Location','/');s.end_headers()
def g(s):
	u,a=z(s)
	r(s,200)
	if not u:return h(s)
	w(s,c('<G>I:checked~div{F`}div{Fnone}I{F`}ZG><label>[checkbox"]Fnone"/><h2]^W:0">HZh2><p]M;$B;W:8px">&#9881Zp><div>_l">?GY$B" CYLogout">ZX>_r">P!b">New p!c">?CYReset pQ">ZX> Zdiv>Zlabel><ul]padding:0">')+''.join(c('<li]F`;border-top:1px solid black;">_etK"]^">?GY@" CY&#974K">ZX><p]^width:calc(100%% - 100px);overflow-wrap:break-word;text-decoration:K">KZp>_edK"]^$B;W:16px">?GY@" CYx">ZX>Zli>')%(k,4+int(e[1]),e[1]and'line-through',e[0],k)for k,e in u[2].items())+c('Zul>_n">[text"]^width:100%;W-B:-45px;padding-B:45px" JYl">?GY^@" CY+">ZX>'))
def p(s):
	o,u,p=urllib.parse.parse_qs(s.rfile.read(int(s.headers.get('Content-Length')))),z(s),s.path
	u,n=u
	a,b,i=[o.get(y,[b''])[0].decode(d)for y in [b'a',b'b',b'c']]
	a=a.replace('.','').replace('/','')
	y=e=None
	if p[1:3]=='uL':
		if not(a in j and q.verify(b,j[a][0])):e=c('A or pQ incorrect')
	elif p[1:2]=='u':
		if a in j:e='A %s already taken'%(a)
		else:j[a]=[q.encrypt(b,rounds=k,salt_size=16),[],{}]
	if e:return r(s,200)or h(s,e)
	if p[1:2]=='u':t=secrets.token_urlsafe();j[a][1].append((t,l()+7**8));y,y['a'],y['b'],u=v(),a,t,j[a]
	if p=='/l':y,y['a'],y['b']=v(),'',''
	if p=='/r':
		if not q.verify(b,u[0]):return r(s,401)or w(s,c('<p>PQ incorrectZp>'))
		u[0:2]=[q.encrypt(i,rounds=k,salt_size=16),[]]
	if p=='/n':u[2][str(uuid.uuid4())]=[o[b'l'][0].decode(d),False]
	if p[1:2]=='e':
		i=p[3:]
		if i not in u[2]:return r(s,404)
		u[2][i][1]=u[2][i][1]<1
		if p[2:3]=='d':del u[2][i]
	f=open((a or n)+'.u','w+')
	f.write(u[0]+'\n')
	u[1]=[s for s in u[1]if s[1]>l()]
	f.write(c('K\nKK\nK')%(len(u[1]),''.join('%s,%s\n'%(s[0].replace('\n','\a'),s[1])for s in u[1]),len(u[2].values()),''.join('%s,%s,%s\n'%(e[1],k,e[0])for k,e in u[2].items())))
	r(s,301,y)
class H(http.server.BaseHTTPRequestHandler):
	def do_GET(s):g(s)
	def do_POST(s):p(s)
http.server.HTTPServer(('localhost',8080),H).serve_forever()
