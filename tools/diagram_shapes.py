from reportlab.platypus import Flowable
from reportlab.lib.colors import HexColor as C
from math import atan2,cos,sin

class Graph(Flowable):
 def __init__(self,kind,height=None):
  Flowable.__init__(self);self.kind=kind;self.width=512
  self.height={'topology':450,'login':425,'request':370,'distributed':345,'refresh':350,'activity':515,'logout':330,'deployment':420,'attacks':410,'partner':380}.get(kind,height or 350)
 def draw(self):
  self.c=self.canv
  if self.kind=='topology':self.topology();return
  if self.kind=='activity':self.activity();return
  if self.kind=='deployment':self.deployment();return
  if self.kind=='attacks':self.attacks();return
  self.sequence(self.kind)
 def text(self,x,y,t,size=8.5,color='#253f4b',align='center',bold=False):
  c=self.c;c.setFillColor(C(color));c.setFont('BodyBold' if bold else 'Body',size)
  for i,l in enumerate(t.split('\n')):
   if align=='left':c.drawString(x,y-i*11,l)
   else:c.drawCentredString(x,y-i*11,l)
 def rect(self,x,y,w,h,title,fill='#eef4f7',tag=None):
  c=self.c;c.setStrokeColor(C('#9eb6c2'));c.setFillColor(C(fill));c.roundRect(x,y,w,h,5,stroke=1,fill=1)
  n=title.count('\n')+1;self.text(x+w/2,y+h/2+(n-1)*5.5-3,title,8.7)
  if tag:
   c.setFillColor(C('#f7e4ba'));c.setStrokeColor(C('#c5a05f'));c.roundRect(x-9,y+h-10,26,17,4,stroke=1,fill=1);self.text(x+4,y+h-5,tag,8,bold=True)
 def arrow(self,x,y,xx,yy,label=None,dashed=False,color='#365f76'):
  c=self.c;c.setStrokeColor(C(color));c.setLineWidth(1.1)
  if dashed:c.setDash(4,3)
  c.line(x,y,xx,yy);c.setDash()
  a=atan2(yy-y,xx-x);s=5
  pa=c.beginPath();pa.moveTo(xx,yy);pa.lineTo(xx-s*cos(a-.5),yy-s*sin(a-.5));pa.moveTo(xx,yy);pa.lineTo(xx-s*cos(a+.5),yy-s*sin(a+.5));c.drawPath(pa)
  if label:self.text((x+xx)/2,(y+yy)/2+6,label,7.9)
 def topology(self):
  c=self.c
  # Trust zones make public entry and private application exposure explicit.
  c.setFillColor(C('#f5f7f8'));c.setStrokeColor(C('#d8e0e5'));c.roundRect(4,280,504,157,6,fill=1,stroke=1)
  self.text(16,423,'BROWSER AND PUBLIC ENTRY',8,align='left',bold=True)
  c.setFillColor(C('#f1f6f2'));c.setStrokeColor(C('#cbd9cf'));c.roundRect(4,7,504,262,6,fill=1,stroke=1)
  self.text(16,255,'PRIVATE SERVICES',8,align='left',bold=True)
  self.rect(162,379,188,34,'React shell and microfrontends',tag='A1')
  self.rect(162,330,188,33,'WAF and HTTPS load balancer',tag='A2')
  self.rect(162,285,188,30,'Public gateway routes')
  self.arrow(256,379,256,363);self.arrow(256,330,256,315)
  self.rect(25,191,157,41,'BFF replica 1\nSession and token handling',tag='A4')
  self.rect(330,191,157,41,'BFF replica 2\nSame session contract')
  self.arrow(221,285,104,232);self.arrow(291,285,409,232)
  self.text(256,245,'Cookie + CSRF',8)
  self.rect(199,187,114,48,'Redis\nShared sessions\nEncrypted token records',fill='#e6f0e8',tag='A5')
  self.arrow(182,210,199,210,dashed=True);self.arrow(330,210,313,210,dashed=True)
  self.rect(15,349,128,48,'External identity\nKeycloak / enterprise IdP',fill='#edf0f6',tag='A3')
  self.arrow(25,212,8,212,dashed=True)
  c.setStrokeColor(C('#365f76'));c.setDash(4,3);c.line(8,212,8,373);c.setDash()
  self.arrow(8,373,15,373,dashed=True)
  self.rect(188,103,169,48,'Authorization management\nRoles, permissions and policies\nControl plane only',fill='#f1edf6')
  self.arrow(103,191,103,71);self.arrow(408,191,408,71)
  self.text(62,134,'Bearer token',7.8);self.text(461,134,'Bearer token',7.8)
  self.rect(92,29,153,42,'Microservice 1\nJWT + local RBAC / ABAC',tag='A7')
  self.rect(330,29,153,42,'Microservice 2\nJWT + local RBAC / ABAC')
  self.arrow(223,103,210,71,dashed=True);self.arrow(325,103,365,71,dashed=True)
  self.text(256,86,'Versioned policy',7.8)
  self.text(256,15,'A6: each service validates JWTs',7.8)
  self.text(13,0,'Solid: business requests     Dashed: security state / OIDC calls',7.7,align='left')
 def sequence(self,kind):
  configs={
   'login':(['Browser','Public edge','BFF replica','Redis','Identity Provider'],[
    (0,1,'1  GET login'),(1,2,'2  Route login'),(2,3,'3  Save state'),(2,0,'4  302 to provider'),
    (0,4,'5  Login and MFA'),(4,0,'6  302 callback with code'),(0,1,'7  GET callback'),(1,2,'8  Route code'),
    (2,3,'9  Check state'),(2,4,'10  Code and verifier'),(4,2,'11  Tokens'),(2,3,'12  Save session'),(2,0,'13  Cookie and 302 UI')]),
   'request':(['Browser','BFF','Microservice 1','Business DB'],[
    (0,1,'1  Cookie and CSRF'),(1,1,'2  Validate session'),(1,2,'3  Bearer request'),
    (2,2,'4  JWT and freshness'),(2,2,'5  Local RBAC'),(2,3,'6  Read resource scope'),
    (3,2,'7  Scope and version'),(2,2,'8  Local ABAC'),(2,3,'9  Commit and audit'),
    (3,2,'10  Committed result'),(2,1,'11  Business response'),(1,0,'12  Business JSON')]),
   'distributed':(['Browser','BFF replica 1','BFF replica 2','Redis'],[
    (0,1,'1  Start login through public edge'),(1,3,'2  Shared pending OIDC state'),(0,2,'3  Callback reaches replica 2'),
    (2,3,'4  Read shared state'),(2,3,'5  Store rotated session and tokens'),(2,0,'6  Cookie and UI redirect'),
    (0,1,'7  API request reaches replica 1'),(1,3,'8  Read same committed session'),(1,0,'9  Authorized API response')]),
   'refresh':(['BFF replica 1','Redis','BFF replica 2','Identity Provider'],[
    (0,1,'1  Acquire lease'),(2,1,'2  Wait for owner'),(0,1,'3  Re-read version'),(0,3,'4  Refresh exchange'),
    (3,0,'5  New token pair'),(0,1,'6  Fenced token write'),(0,1,'7  Owner release'),(2,1,'8  Load new version'),
    (2,2,'9  Relay new access token')]),
   'partner':(['External system','Identity Provider','API edge','Microservice 1','Business DB'],[
    (0,1,'1  Client credentials'),(1,0,'2  Access token'),(0,2,'3  Bearer API call'),(2,3,'4  Fixed route'),
    (3,3,'5  JWT and local RBAC'),(3,4,'6  Read resource scope'),(4,3,'7  Scope and version'),
    (3,3,'8  Resource ABAC'),(3,4,'9  Authorized commit'),(3,0,'10  Response via edge')]),
   'logout':(['Browser','BFF replica','Redis','Identity Provider'],[
    (0,1,'1  POST logout and CSRF'),(1,2,'2  Invalidate shared session'),(1,2,'3  Delete token record'),
    (1,0,'4  Clear cookie; return logout URL'),(0,3,'5  Top-level OIDC logout'),(3,0,'6  Return to registered UI'),
    (0,1,'7  GET session'),(1,0,'8  401 unauthenticated')])}
  labels,steps=configs[kind];n=len(labels);xs=[48+i*(416/(n-1)) for i in range(n)]
  top=self.height-15
  for x,l in zip(xs,labels):
   self.rect(x-47,top-27,94,27,l,fill='#fff0a8')
   c=self.c;c.setStrokeColor(C('#817a60'));c.setDash(3,3);c.line(x,top-34,x,12);c.setDash()
  # UML-style activation bars show each participant active over its interaction span.
  for n,x in enumerate(xs):
   active=[j for j,(a,b,_) in enumerate(steps) if a==n or b==n]
   if active:
    span=(top-54-22)/max(len(steps)-1,1);y1=top-55-min(active)*span;y2=top-55-max(active)*span-10
    c.setFillColor(C('#fff6d2'));c.setStrokeColor(C('#b7a65d'));c.rect(x-3,y2,6,max(12,y1-y2),stroke=1,fill=1)
  step=(top-54-22)/max(len(steps)-1,1)
  for i,(a,b,l) in enumerate(steps):
   y=top-55-i*step
   if a==b:
    c=self.c;c.setStrokeColor(C('#365f76'));c.line(xs[a],y,xs[a]+19,y);c.line(xs[a]+19,y,xs[a]+19,y-8);self.arrow(xs[a]+19,y-8,xs[a],y-8)
    # Labels above self calls avoid crossing neighbouring lifelines.
    self.text(xs[a]-5,y+6,l,7.7)
   else:
    is_return=(i+1) in {'login':{4,6,11,13},'request':{7,10,11,12},'distributed':{6,9},'refresh':{5},'logout':{4,6,8},'partner':{2,7,10}}[kind]
    self.arrow(xs[a],y,xs[b],y,dashed=is_return,color='#484334')
    self.text((xs[a]+xs[b])/2,y+6,l,7.9)
 def activity(self):
  def diamond(x,y,label):
   c=self.c;c.setFillColor(C('#e9f0f4'));c.setStrokeColor(C('#91aab9'))
   p=c.beginPath();p.moveTo(x,y+21);p.lineTo(x+65,y);p.lineTo(x,y-21);p.lineTo(x-65,y);p.close();c.drawPath(p,stroke=1,fill=1)
   self.text(x,y+3,label,8)
  self.rect(163,474,186,29,'Receive browser API request')
  self.arrow(256,474,256,455)
  checks=[(434,'Session valid?','401 / sign in'),(374,'CSRF valid if\nrequired?','403 / no relay'),(314,'Token ready after\nrefresh if needed?','401 or 503'),(254,'JWT valid?','401 / no work'),(194,'Policy / entitlements\nvalid?','503 / no work'),(134,'Local RBAC allow?','403 / no work'),(74,'Local ABAC allow?','403 or concealed 404')]
  for i,(y,label,deny) in enumerate(checks):
   diamond(256,y,label);self.rect(365,y-14,144,28,deny,fill='#f9ece8');self.arrow(321,y,365,y,'No',color='#a6644e')
   if i<len(checks)-1:self.arrow(256,y-21,256,checks[i+1][0]+21,'Yes')
  self.arrow(256,53,256,30,'Yes')
  self.rect(153,0,206,30,'Validate input; commit and audit',fill='#e6f0e8')
  self.text(10,429,'BFF',8,align='left',bold=True)
  self.text(10,249,'Microservice',8,align='left',bold=True)
  self.text(10,69,'Resource policy',8,align='left',bold=True)
  self.text(10,145,'Policy must be valid;',7.5,align='left')
  self.text(10,134,'expired data: 503',7.5,align='left')

 def deployment(self):
  self.rect(138,361,236,38,'WAF / HTTPS ALB / public edge')
  for x in [12,180,348]:
   c=self.c;c.setFillColor(C('#f2f6f3'));c.setStrokeColor(C('#c5d6ca'));c.roundRect(x,97,152,231,5,fill=1,stroke=1)
  for i,x in enumerate([12,180,348]):
   self.text(x+76,113,'Private EKS zone '+str(i+1),9,bold=True)
   self.rect(x+10,239,132,42,'BFF replica '+str(i+1)+'\nSession / refresh / relay')
   self.rect(x+10,126,132,51,'Microservice replica\nJWT + local RBAC\nand resource ABAC')
   self.arrow(256,361,x+76,281)
   self.arrow(x+76,239,x+76,177,'Bearer')
  self.rect(12,26,152,46,'Shared Redis\nPrivate TLS / ACL')
  self.rect(180,26,152,46,'Policy management\nVersioned distribution')
  self.rect(348,26,152,46,'Private business DB\nTransactions and audit')
  self.text(256,7,'No mandatory internal gateway or central decision round trip',8.3)
  self.text(256,91,'Shared services below are logical; traffic may cross zones',7.8)
 def attacks(self):
  entries=[('A1 Browser / MFE','CSP, encoding, approved remotes'),('A2 Public edge','TLS, limits, trusted proxy headers'),('A3 SSO callback','State, nonce, PKCE, exact redirect'),('A4 BFF session / relay','CSRF, rotation, destination allowlist'),('A5 Redis / refresh','ACL, TLS, encryption, fenced writes'),('A6 Service JWT boundary','Issuer, audience, expiry, caller checks'),('A7 Local RBAC and ABAC','Permission + authoritative scope'),('A8 Authorization administration','Signed policy, freshness, audit'),('A9 Kubernetes / delivery','Least privilege, provenance, isolation')]
  for i,(title,control) in enumerate(entries):
   y=365-i*39
   self.rect(8,y,198,29,title)
   self.arrow(206,y+14,231,y+14)
   self.rect(237,y,267,29,control,fill='#eef4ec')
  self.text(256,4,'Control location and ownership follow the resource boundary',8.2)
