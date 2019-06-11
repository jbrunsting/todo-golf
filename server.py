#!/usr/bin/python3
import http.server,os,secrets,time,uuid,urllib.parse
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
	for e in zip('[^@?_!]ZYXMQAWBGIFVJKCH$`Àjqz',c('<I typeY|Finline-`;|background:none;border:none;M|[submit"|<X methodYpost" actionY/|Q[pQ" JY| GY|</|="|form|cursor:pointer|assword|UserJ|margin|right|style|input|display:|Signup|name|%s|valueY|TODOZ|float:|block|;padding|width:|Q incorrect|">ZX>',b +1).split('|')):s=s.replace(*e)
	return s
def r(s,b,x=200,k=''):h=s.send_header;s.send_response(x);k and h('Set-Cookie',k.output(header='',sep=''));k!=''and h('Location','/');s.end_headers();b and s.wfile.write(bytes(c('<title>Htitle><body]max-j800px;W:autoÀ:16px">%sZbody>'%b),d))
def p(s,e):
	u,n='',''
	x=v(s.headers.get('Cookie'))
	if'a'in x and'b'in x:n=x['a'].value;u=j.get(n,[[]]);u[1]=[s for s in u[1]if s[1]>l()];u=x['b'].value in[s[0]for s in u[1]]and u
	if e and u:return r(s,c('<G>I:checked~div{F`}div{Fnone}I{F`}ZG><label>[checkbox"]Fnone"/><h2]^W:0">Hh2><p]M;$B;W:8px">&#9881Zp><div>_l">?GY$B" CLogoutz_r">P!b">New p!c">?CReset pQz Zdiv>Zlabel><ul]À:0">')+''.join(c('<li]F`;border-top:1px solid black;">_etK"]^">?GY@" C&#974Kz<p]^jcalc(100%% - 100px);overflow-wrap:break-word;text-decoration:K">KZp>_edK"]^$B;W:16px">?GY@" CxzZli>')%(k,4+int(e[1]),e[1]and'line-through',e[0],k)for k,e in u[2].items())+c('Zul>_n">[text"]^j100%;W-B:-45pxÀ-B:45px" JYl">?GY^@" C+z'))
	o,p=urllib.parse.parse_qs(s.rfile.read(int(s.headers.get('Content-Length')or'0'))),s.path
	a,b,i=[o.get(y,[b''])[0].decode(d)for y in[b'a',b'b',b'c']]
	a,x=a.replace('.','').replace('/',''),p[1:2]
	y=None
	if p[1:3]=='uL':
		if not(a in j and q.verify(b,j[a][0])):e=c('A or pq')
	elif x=='u':
		if a in j:e='A %s already taken'%(a)
		else:j[a]=[q.encrypt(b,rounds=k,salt_size=16),[],{}]
	elif not u:e=' '
	f=c('_uV"]$left">A[text"]F`" JYa">P!b"]F`">?CVz')
	if e:return r(s,c('<h2>Hh2><p>KZp>KK')%(e,f,f.replace('left',c('B')).replace(c('V'),'Login')))
	if x=='u':t=secrets.token_urlsafe();j[a][1].append((t,l()+7**8));y,y['a'],y['b'],u=v(),a,t,j[a]
	if x=='l':y,y['a'],y['b']=v(),'',''
	if x=='r':
		if q.verify(b,u[0])<1:return r(s,c('<p>PqZp>'),401)
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
	f.write(c('K\nKK\nK')%(len(u[1]),''.join('%s,%s\n'%(s[0].replace('\n','\a'),s[1])for s in u[1]),len(m.values()),''.join('%s,%s,%s\n'%(e[1],k,e[0])for k,e in m.items())))
	r(s,'',301,y)
class H(http.server.BaseHTTPRequestHandler):
	def do_GET(s):p(s,' ')
	def do_POST(s):p(s,'')
http.server.HTTPServer(('localhost',8080),H).serve_forever()
