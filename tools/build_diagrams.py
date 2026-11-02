"""Rebuild authorization-related diagram assets from shared vector drawing source."""
from pathlib import Path
import ast,sys,tempfile
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas
import fitz
from diagram_shapes import Graph
ROOT=Path(__file__).resolve().parents[1]
for n,f in [('Body','DejaVuSans.ttf'),('BodyBold','DejaVuSans-Bold.ttf')]:pdfmetrics.registerFont(TTFont(n,'/usr/share/fonts/truetype/dejavu/'+f))
TITLES={'topology':'Service authorization architecture','request':'Direct token relay and local authorization','activity':'Service authorization and denial paths','deployment':'AWS EKS and local authorization','attacks':'Attack points and control ownership','login':'SSO login sequence','distributed':'Distributed BFF sessions','refresh':'Coordinated token refresh','logout':'Shared-session logout','partner':'External system access and service authorization'}
def render(kind,path,svg=None):
 g=Graph(kind);w,h=568,g.height+125
 with tempfile.NamedTemporaryFile(suffix='.pdf') as temp:
  c=Canvas(temp.name,pagesize=(w,h));c.setFillColorRGB(1,1,1);c.rect(0,0,w,h,fill=1,stroke=0)
  c.setFillColorRGB(.13,.23,.29);c.setFont('BodyBold',16);c.drawString(28,h-32,TITLES[kind]);c.setFont('Body',8.5);c.drawString(28,h-51,'Central policy administration | Service-local RBAC and ABAC')
  g.drawOn(c,28,54)
  c.setFont('Body',7.4);c.drawString(28,24,'Business path: public edge -> BFF -> private service. Policy distribution is a separate control-plane flow.')
  c.save();pdf=fitz.open(temp.name);page=pdf[0];path.parent.mkdir(parents=True,exist_ok=True);raw=page.get_pixmap(matrix=fitz.Matrix(6,6)).tobytes('png');stage=path.with_suffix('.png.tmp');stage.write_bytes(raw);stage.replace(path)
  if svg:svg.write_text(page.get_svg_image(text_as_path=True))
  pdf.close()
central=ROOT/'docs/centralized-sso'
keys=[('topology','01_secure_access_architecture'),('login','02_sso_login_sequence'),('request','03_token_relay_sequence'),('distributed','04_distributed_bff_sessions'),('refresh','05_token_refresh_sequence'),('activity','06_request_activity_and_denials'),('logout','07_logout_sequence')]
for kind,stem in keys:render(kind,central/'images'/f'{stem}.png',central/'svg'/f'{stem}.svg')
for edition,entries in [('eks-bff',[('login','02_sso_login_flow'),('refresh','04_distributed_bff_refresh'),('topology','01_secure_access_architecture'),('request','03_business_request'),('deployment','05_eks_deployment'),('attacks','06_attack_points')]),('platform',[('login','02_sso_login_flow'),('refresh','04_distributed_bff_refresh'),('partner','06_partner_integration'),('topology','01_secure_access_architecture'),('request','03_business_request'),('deployment','05_eks_deployment'),('attacks','07_security_boundaries')])]:
 for kind,stem in entries:render(kind,ROOT/'docs'/edition/('assets' if edition=='platform' else 'diagrams')/f'{stem}.png')
# Keep editable message sources synchronized with the rendered sequence diagrams.
node=ast.parse((Path(__file__).parent/'diagram_shapes.py').read_text())
configs=ast.literal_eval(next(n.value for n in ast.walk(node) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='configs' for t in n.targets)))
import re
for kind,(labels,steps) in configs.items():
 
 if kind not in dict(keys):continue
 stem=dict(keys)[kind];lines=['sequenceDiagram','    autonumber']
 for i,label in enumerate(labels):lines.append(f'    participant P{i} as {label}')
 for index,(a,b,label) in enumerate(steps,1):
  ret=index in {'login':{4,6,11,13},'request':{7,10,11,12},'distributed':{6,9},'refresh':{5},'logout':{4,6,8}}[kind]
  lines.append(f'    P{a}'+('-->>' if ret else '->>')+f'P{b}: '+re.sub(r'^\d+\s+','',label))
 (central/'diagram-source'/f'{stem}.mmd').write_text('\n'.join(lines)+'\n')
 uml=['@startuml','skinparam shadowing false','skinparam ParticipantBackgroundColor #FFF0A8','skinparam ActivationBackgroundColor #FFF6D2','skinparam ArrowColor #484334','autonumber']
 for index,label in enumerate(labels):uml.append(f'participant "{label}" as P{index}')
 for index,(a,b,label) in enumerate(steps,1):
  ret=index in {'login':{4,6,11,13},'request':{7,10,11,12},'distributed':{6,9},'refresh':{5},'logout':{4,6,8}}[kind]
  uml.append(f'P{a}'+(' --> ' if ret else ' -> ')+f'P{b}: '+re.sub(r'^\d+\s+','',label))
 uml.append('@enduml');(central/'diagram-source'/f'{stem}.puml').write_text('\n'.join(uml)+'\n')

(central/'diagram-source/01_secure_access_architecture.mmd').write_text('''flowchart TD
  UI["React microfrontends"] --> Edge["ALB and optional edge gateway"]
  Edge --> BFF["BFF replicas"]
  BFF -->|Bearer token| M1["Microservice 1: JWT and local RBAC / ABAC"]
  BFF -->|Bearer token| M2["Microservice 2: JWT and local RBAC / ABAC"]
  BFF -.-> Redis["Shared sessions and encrypted tokens"]
  BFF -. OIDC .-> IdP["Enterprise SSO / Keycloak"]
  Admin["Authorization management"] -. Versioned policy .-> M1
  Admin -. Versioned policy .-> M2
''')
(central/'diagram-source/06_request_activity_and_denials.mmd').write_text('''flowchart TD
  A["Browser request"] --> B{"BFF session and required CSRF valid?"}
  B -->|No| B0["401 or 403; no relay"]
  B -->|Yes| C{"Usable token after safe refresh?"}
  C -->|No| C0["401 or 503"]
  C -->|Yes| D{"Service JWT valid?"}
  D -->|No| D0["401"]
  D -->|Yes| E{"Mandatory policy and entitlements valid?"}
  E -->|No| E0["503; fail closed"]
  E -->|Yes| F{"Local RBAC allows operation?"}
  F -->|No| F0["403"]
  F -->|Yes| G{"Local resource ABAC allows?"}
  G -->|No| G0["403 or concealed 404"]
  G -->|Yes| H["Validate input; commit and audit"]
''')
print('Rebuilt 20 PNGs, seven SVGs and seven editable diagram sources')
