from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import math

OUT=Path('output/assets'); OUT.mkdir(exist_ok=True)
S=2
FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
BOLD='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
INK='#24394A'; MUTED='#526779'; LINE='#668193'
BLUE=('#E9F1F8','#527CA0'); TEAL=('#E5F2EF','#41857B'); GREEN=('#EDF3E7','#6A8D53'); PURPLE=('#F0EBF5','#8B74A3'); SAND=('#FAF0DE','#B38D4A'); RED=('#F8ECE7','#AD6D58')
def font(n,b=False): return ImageFont.truetype(BOLD if b else FONT,round(n*S))
class Board:
 def __init__(self,name,title,subtitle,h=1000):
  self.name=name;self.w=1600;self.h=h
  self.im=Image.new('RGB',(self.w*S,h*S),'#FFFFFF');self.d=ImageDraw.Draw(self.im)
  self.d.rectangle((0,0,1600*S,10*S),fill='#397C78')
  title_size=31
  while self.d.textlength(title,font=font(title_size,True))>1472*S: title_size-=1
  self.text(64,40,title,title_size,True)
  self.text(64,87,subtitle,17,color=MUTED)
 def rect(self,xy,fill,outline=None,r=12,width=1): self.d.rounded_rectangle(tuple(round(v*S) for v in xy),radius=r*S,fill=fill,outline=outline,width=width*S)
 def text(self,x,y,t,size=18,b=False,color=INK,anchor=None): self.d.text((round(x*S),round(y*S)),t,font=font(size,b),fill=color,anchor=anchor,spacing=6*S)
 def wrapped(self,t,n,maxw,b=False):
  out=[]
  for par in t.split('\n'):
   cur=''
   for word in par.split():
    nxt=(cur+' '+word).strip()
    if self.d.textlength(nxt,font=font(n,b))>maxw*S and cur:out.append(cur);cur=word
    else:cur=nxt
   out.append(cur)
  return out
 def box(self,x,y,w,h,title,body='',palette=BLUE):
  bg,border=palette;self.rect((x,y,x+w,y+h),bg,border,width=2)
  self.text(x+20,y+16,title,21,True)
  yy=y+53
  for line in self.wrapped(body,17,w-40): self.text(x+20,yy,line,17);yy+=25
  if yy>y+h+4:raise ValueError((self.name,title,'overflow',yy,y+h))
 def arrow(self,pts,label='',at=None,color=LINE,dash=False):
  coords=[(x*S,y*S) for x,y in pts]
  for a,b in zip(coords,coords[1:]):
   if dash:
    dist=math.dist(a,b);n=max(1,int(dist/(10*S)))
    for k in range(0,n,2):
     f=k/n;g=min((k+1)/n,1);self.d.line((a[0]+(b[0]-a[0])*f,a[1]+(b[1]-a[1])*f,a[0]+(b[0]-a[0])*g,a[1]+(b[1]-a[1])*g),fill=color,width=2*S)
   else:self.d.line((a,b),fill=color,width=2*S)
  (ax,ay),(bx,by)=coords[-2:];ang=math.atan2(by-ay,bx-ax);length=11*S
  self.d.polygon([(bx,by),(bx-length*math.cos(ang-.45),by-length*math.sin(ang-.45)),(bx-length*math.cos(ang+.45),by-length*math.sin(ang+.45))],fill=color)
  if label:
   x,y=at or ((pts[0][0]+pts[-1][0])/2,(pts[0][1]+pts[-1][1])/2)
   lines=self.wrapped(label,16,430)
   y-=23*(len(lines)-1)
   width=max(self.d.textlength(t,font=font(16)) for t in lines)/S+16
   self.rect((x-width/2,y-4,x+width/2,y+len(lines)*23+4),'#FFFFFF',r=3)
   for k,t in enumerate(lines): self.text(x,y+k*23,t,16,anchor='mt')
 def note(self,x,y,w,text,palette=TEAL):
  lines=self.wrapped(text,17,w-34)
  self.rect((x,y,x+w,y+len(lines)*25+28),palette[0],palette[1],r=8)
  for i,line in enumerate(lines):self.text(x+17,y+12+i*25,line,17)
 def save(self):
  self.d.line((64*S,(self.h-54)*S,1536*S,(self.h-54)*S),fill='#D6E0E5',width=S)
  self.text(64,self.h-38,'AOBP  |  Architecture specification 2.3  |  02 November 2026',13,color=MUTED)
  self.text(1536,self.h-38,'Illustrative topology · proposed controls',13,color=MUTED,anchor='rt')
  self.im.save(OUT/(self.name+'.png'),dpi=(220,220))

b=Board('01_secure_access_architecture','Secure browser access: where the BFF belongs','Separate UI deployments, one browser origin, server-held OAuth credentials.',1090)
b.rect((450,430,1100,945),'#F7FAFB','#CCDCE2');b.text(470,442,'PRIVATE EKS APPLICATION BOUNDARY',14,True,color=MUTED)
b.box(570,145,410,110,'Browser · React shell + MFEs','Draws screens; holds opaque cookie only',BLUE)
b.box(570,295,410,110,'AWS WAF + ALB','HTTPS entry and host/path routing',BLUE)
b.arrow([(775,255),(775,295)],'HTTPS',at=(1040,267))
b.box(60,470,370,145,'Independent static UI','Shell and versioned remote assets\nNo protected operational data',BLUE)
b.arrow([(570,350),(245,350),(245,470)],'Static files',at=(285,370))
b.box(570,470,410,110,'Spring Cloud API Gateway','Route limits, traffic controls and tracing',BLUE)
b.arrow([(775,405),(775,470)],'Dynamic / login / WebSocket',at=(782,423))
b.box(570,645,410,125,'Spring Boot BFF','Validates session + CSRF\nRefreshes and relays server-held token',TEAL)
b.arrow([(775,580),(775,645)],'Opaque browser session cookie',at=(775,601))
b.box(1150,470,390,140,'Keycloak → BAC SSO','Corporate sign-in and MFA\nBFF code exchange / renewal',PURPLE)
b.arrow([(980,682),(1095,682),(1095,540),(1150,540)],'OIDC back channel',at=(1325,635),color=PURPLE[1])
b.box(1150,740,390,140,'Shared sensitive state','Redis: sessions + authorized clients\nCoordinated refresh; TLS + ACLs',SAND)
b.arrow([(980,720),(1060,720),(1060,810),(1150,810)],'Session / token state',at=(1300,698),color=SAND[1])
b.box(570,835,410,110,'Private business APIs','Validate JWT + enforce RBAC / ABAC',GREEN)
b.arrow([(775,770),(775,835)],'Authorization: Bearer <access token>',at=(775,790),color=TEAL[1])
b.note(60,670,370,'Browser business requests always use the BFF. Static assets bypass it. Approved machine integrations use their own gateway route.')
b.note(60,950,1480,'Responses return along the reverse path. The gateway forwards the browser session cookie; only the BFF constructs the private API request with the user access token.')
b.save()

def sequence(name,title,subtitle,actors,rows,notes,h=1180):
 b=Board(name,title,subtitle,h)
 xs=[130+i*(1340/(len(actors)-1)) for i in range(len(actors))]
 for x,(title,body,pal) in zip(xs,actors):
  b.rect((x-95,145,x+95,245),pal[0],pal[1],width=2)
  b.text(x,161,title,17,True,anchor='mt')
  for j,line in enumerate(b.wrapped(body,15,166)): b.text(x,195+j*21,line,15,anchor='mt')
  b.arrow([(x,245),(x,h-185)],dash=True,color='#BCCBD4')
 for i,(a,z,label,pal) in enumerate(rows):
  yy=285+i*75
  if a==z:
   x=xs[a];b.arrow([(x,yy),(x+60,yy),(x+60,yy+28),(x,yy+28)],color=pal)
   b.text(x+78,yy-8,label,16)
  else:
   b.arrow([(xs[a],yy),(xs[z],yy)],label,at=((xs[a]+xs[z])/2,yy-29),color=pal)
  b.rect((35,yy-17,66,yy+14),'#E7F0F3',r=15);b.text(50,yy-1,str(i+1),15,True,anchor='mm')
 b.note(65,h-154,1470,notes)
 b.save()

sequence('02_sso_login_flow','SSO login: from first visit to a safe browser session','Browser redirects are different from the private server-to-server token exchange.',
 [('Browser','React UI',BLUE),('ALB + gateway','Entry routing',BLUE),('BFF','OIDC client',TEAL),('Identity','Keycloak + SSO',PURPLE),('Shared store','Session / tokens',SAND)],
 [(0,2,'Open BFF login through ALB + gateway',LINE),(2,4,'Save state, nonce and PKCE verifier',SAND[1]),(2,0,'Redirect to Keycloak authorization endpoint',PURPLE[1]),(0,3,'Corporate sign-in / MFA when required',PURPLE[1]),(3,0,'Redirect with one-use code + state',PURPLE[1]),(0,2,'Callback through ALB + gateway',LINE),(2,3,'Validate transaction; exchange code + PKCE privately',TEAL[1]),(3,2,'Tokens returned to BFF only',TEAL[1]),(2,4,'Save tokens and rotate session ID',SAND[1]),(2,0,'Set opaque cookie; redirect to clean UI URL',LINE)],
 'The browser sees a temporary callback code, never an API access/refresh/ID token. All browser-to-BFF arrows traverse ALB and gateway; they are condensed here to keep the login sequence readable.',h=1260)

sequence('03_business_request','A business request: cookie at the front, token at the API','Example: read authorized flight information; a write also requires CSRF and business checks.',
 [('Browser','React screen',BLUE),('ALB + gateway','Route and limits',BLUE),('BFF','Session owner',TEAL),('Shared store','Session / tokens',SAND),('Private API','Business authority',GREEN)],
 [(0,1,'GET /bff/api/v1/flights + session cookie',LINE),(1,2,'Forward approved route and cookie',LINE),(2,3,'Validate session; load fresh token or coordinate renewal',SAND[1]),(3,2,'Current session + authorized-client version',SAND[1]),(2,4,'New request: Authorization: Bearer <access token>',TEAL[1]),(4,2,'After JWT + RBAC/ABAC checks: authorized result',GREEN[1]),(2,1,'Safe business response; no OAuth tokens',LINE),(1,0,'Return data to React over HTTPS',LINE)],
 'The BFF removes browser cookies and untrusted identity headers before calling an allowlisted private API. A hidden UI button is never permission enforcement. Denials and errors return through the same route.',h=1100)

sequence('04_distributed_bff_refresh','Distributed BFF: shared sessions and controlled renewal','Two requests for the same session can reach different replicas. Refresh rotation needs coordination.',
 [('Request A','BFF pod A',TEAL),('Request B','BFF pod B',TEAL),('Shared store','Version + lease',SAND),('Keycloak','Token endpoint',PURPLE)],
 [(0,2,'Read session/token version; acquire bounded lease',SAND[1]),(1,2,'Same session arrives; wait within request deadline',SAND[1]),(0,3,'Reread current state; refresh protected credential',PURPLE[1]),(3,0,'New access token + rotated refresh token',PURPLE[1]),(0,2,'Atomic save: version + live session generation',SAND[1]),(2,1,'Read committed new credential version',SAND[1]),(0,2,'Release lease only if still owner',SAND[1]),(1,2,'Both replicas use shared updated state',TEAL[1])],
 'Logout/absolute expiry wins: an in-flight refresh cannot recreate revoked state. Redis failover can lose recent writes or leases; ambiguous rotation outcomes require safe reconciliation or a new login, never a replay loop.',h=1100)

b=Board('05_eks_deployment','AWS EKS deployment: entry, private workloads and data','Three-zone reference. Replica counts are starting resilience proposals, not measured capacity.',1220)
b.box(65,145,360,105,'Approved users','Corporate network / approved connectivity',BLUE)
b.box(550,145,500,105,'Regional entry · WAF + ALB','Route 53 + ACM; internal ALB by default',BLUE)
b.arrow([(425,197),(550,197)],'HTTPS',at=(485,167))
b.rect((65,315,1535,930),'#F8FAFB','#BCD0DA',width=2);b.text(85,332,'PRIVATE EKS WORKER SUBNETS · NO PUBLIC POD ENDPOINTS',17,True)
for i,(zone,x) in enumerate([('Availability Zone A',95),('Availability Zone B',580),('Availability Zone C',1065)]):
 b.rect((x,385,x+440,885),'#FFFFFF','#D6E0E5');b.text(x+20,402,zone,20,True)
 b.box(x+20,465,400,88,'Gateway replica','aobp-edge · ALB IP target',BLUE)
 b.box(x+20,615,400,88,'BFF replica','aobp-apps · gateway ingress only',TEAL)
 b.box(x+20,765,400,88,'Business API replicas','Private services · JWT + policy',GREEN)
 b.arrow([(x+220,553),(x+220,615)],color=LINE)
 b.arrow([(x+220,703),(x+220,765)],color=TEAL[1])
b.arrow([(800,250),(800,285),(495,285),(495,450),(315,450),(315,465)])
b.arrow([(800,285),(980,285),(980,450),(800,450),(800,465)])
b.arrow([(800,285),(1465,285),(1465,450),(1285,450),(1285,465)])
b.note(95,895,1410,'Requests may cross zones. Private ClusterIP Services provide discovery; ALB IP targets address gateway pods directly. Independently deployed static UI workloads use separate ALB path targets.')
b.box(65,1010,450,105,'Private session store','Multi-AZ Redis; TLS, ACLs, failover tests',SAND)
b.box(575,1010,450,105,'Private identity + data','Keycloak / identity DB; business DBs',PURPLE)
b.box(1085,1010,450,105,'Load Balancer Controller','Reconciles Ingress; no request proxy',BLUE)
b.arrow([(1310,1010),(1560,1010),(1560,285),(1050,285),(1050,205)],dash=True,color=BLUE[1])
b.save()

sequence('06_partner_integration','Machine integration: its own identity and API route','A partner system does not sign in as an airport employee and does not use the browser BFF.',
 [('Partner','Dedicated client',BLUE),('Keycloak','Machine tokens',PURPLE),('ALB + gateway','Partner route',BLUE),('Private API','JWT + scope',GREEN)],
 [(0,1,'Client credentials with approved client authentication',PURPLE[1]),(1,0,'Short-lived machine access token',PURPLE[1]),(0,2,'HTTPS /api/v1/flights + Authorization: Bearer',LINE),(2,3,'Validate machine client / scope; forward approved API',LINE),(3,2,'Revalidate JWT + resource permission; return result',GREEN[1]),(2,0,'Return only authorized partner data',LINE),(0,1,'Obtain new machine token when required',PURPLE[1])],
 'No BFF session, employee password or human refresh token is shared. Partner routes require approved clients and scopes; a different hostname or CORS configuration alone is not an authentication control.',h=1020)

b=Board('07_security_boundaries','Security boundaries: attack points and practical defenses','The BFF reduces browser token theft; each remaining boundary still needs its own controls.',1240)
cards=[('A · Browser / MFE','XSS or compromised remote code','CSP, safe output, controlled releases\nNo OAuth tokens in JavaScript',BLUE),('B · Cookie session','Forged change request / CSRF','Secure + HttpOnly cookie; CSRF token\nOrigin validation and bounded lifetime',TEAL),('C · Edge / callback','Spoofing, overload or code leakage','WAF, route limits, trusted forwarding\nState / nonce / PKCE; safe logging',BLUE),('D · BFF / shared store','Credential theft or arbitrary proxying','Private encrypted store, ACLs, rotation\nOutbound host and path allowlists',SAND),('E · Business API','Unauthorized record or field access','JWT validation + current RBAC / ABAC\nTrusted resource scope; safe DTOs',GREEN),('F · Data / audit','Injection, bulk export or tampering','Parameterized SQL, restricted DB roles\nBounded exports; durable protected audit',GREEN),('G · Live WebSocket','Stale or unauthorized event delivery','Authorize subscribe and delivery\nLogout fan-out; bounded expiry checks',TEAL),('H · Partner integration','Stolen machine credential / overreach','Dedicated client, scopes, quotas\nRotation; resource checks in API',PURPLE)]
for i,(title,risk,controls,pal) in enumerate(cards):
 x=65+(i%2)*760;y=155+(i//2)*230
 b.box(x,y,710,200,title,risk+'\n\n'+controls,pal)
b.note(65,1090,1470,'Acceptance evidence: cross-site writes denied, wrong-audience tokens rejected, cross-terminal data blocked, logout races fenced, socket entitlements revoked, and retained logs free of credentials and callback codes.')
b.save()
print('Created',len(list(OUT.glob('*.png'))),'PNG diagrams at 3200-pixel width')
