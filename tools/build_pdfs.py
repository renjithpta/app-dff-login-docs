"""Build the three PDF editions from their authoritative Markdown and local images."""
from pathlib import Path
import re,html,textwrap
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,PageBreak,Table,TableStyle,Image,Preformatted,KeepTogether,CondPageBreak
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PIL import Image as PILImage
ROOT=Path(__file__).resolve().parents[1]
for n,f in [('Body','DejaVuSans.ttf'),('Bold','DejaVuSans-Bold.ttf'),('Mono','DejaVuSansMono.ttf')]:pdfmetrics.registerFont(TTFont(n,'/usr/share/fonts/truetype/dejavu/'+f))
pdfmetrics.registerFontFamily('Body',normal='Body',bold='Bold',italic='Body',boldItalic='Bold')
B=ParagraphStyle('Body',fontName='Body',fontSize=9.2,leading=13.6,spaceAfter=8,textColor=colors.HexColor('#263d4a'))
H=ParagraphStyle('Heading',parent=B,fontName='Bold',fontSize=16,leading=21,spaceBefore=12,spaceAfter=11,keepWithNext=True,textColor=colors.black)
S=ParagraphStyle('Subheading',parent=H,fontSize=11,leading=15,spaceBefore=10,spaceAfter=7)
T=ParagraphStyle('Title',parent=H,fontSize=24,leading=31)
CELL=ParagraphStyle('Cell',parent=B,fontSize=8,leading=11,spaceAfter=0)
CODE=ParagraphStyle('Code',fontName='Mono',fontSize=7,leading=10,spaceAfter=0)
SMALL=ParagraphStyle('Small',parent=B,fontSize=7.5,leading=10)
def inline(x):
 x=html.escape(x).replace('&lt;br&gt;','<br/>').replace('&lt;br/&gt;','<br/>')
 x=re.sub(r'\*\*(.+?)\*\*',r'<b>\1</b>',x)
 x=re.sub(r'`([^`]+)`',r'<font name="Mono" size="8">\1</font>',x)
 x=re.sub(r'\[([^\]]+)\]\((https?[^)]+)\)',r'<link href="\2" color="#315970">\1</link>',x)
 # Relative links remain readable; live repository links are in Markdown.
 x=re.sub(r'\[([^\]]+)\]\(([^)]+)\)',r'\1',x)
 return x
for edition,name in [('centralized-sso','AOBP_BFF_Centralized_SSO_Architecture'),('eks-bff','AOBP_BFF_Architecture_Design'),('platform','AOBP_Platform_Architecture_Design'),('.','api-standards')]:
 folder=ROOT/'docs'/edition;md=folder/(name+'.md');lines=md.read_text().splitlines();story=[];i=0
 while i<len(lines):
  ln=lines[i]
  if not ln.strip():i+=1;continue
  if ln.startswith('# '):story.append(Paragraph(inline(ln[2:]),T));i+=1;continue
  if ln.startswith('## '):
   if len(story)>2:story.append(CondPageBreak(150))
   story.append(Paragraph(inline(ln[3:]),H));i+=1;continue
  if ln.startswith('### '):story.append(Paragraph(inline(ln[4:]),S));i+=1;continue
  if ln.startswith('#### '):story.append(Paragraph(inline(ln[5:]),S));i+=1;continue
  if ln.startswith('```'):
   i+=1
   while i<len(lines) and not lines[i].startswith('```'):
    for v in textwrap.wrap(lines[i].expandtabs(4),width=106,replace_whitespace=False,drop_whitespace=False) or [' ']:story.append(Preformatted(v,CODE))
    i+=1
   story.append(Spacer(1,10));i+=1;continue
  if ln.startswith('|'):
   rows=[]
   while i<len(lines) and lines[i].startswith('|'):
    vals=re.split(r'(?<!\\)\|',lines[i].strip().strip('|'));i+=1
    if all(re.fullmatch(r'[\s:-]+',v) for v in vals):continue
    rows.append([v.strip().replace('\\|','|') for v in vals])
   n=max(map(len,rows));rows=[r+['']*(n-len(r)) for r in rows]
   weights={2:[.34,.66],3:[.23,.49,.28],4:[.20,.26,.27,.27]}.get(n,[1/n]*n)
   tab=Table([[Paragraph(inline(v),CELL) for v in r] for r in rows],colWidths=[512*w for w in weights],repeatRows=1,hAlign='LEFT')
   tab.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#e1ecf1')),('GRID',(0,0),(-1,-1),.4,colors.HexColor('#d9d9d9')),('VALIGN',(0,0),(-1,-1),'MIDDLE'),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6)]))
   story.extend([tab,Spacer(1,10)]);continue
  m=re.match(r'!\[(.*?)\]\((.*?)\)',ln)
  if m:
   caption,rel=m.groups();img=folder/rel;w,h=PILImage.open(img).size;ratio=min(512/w,480/h)
   story.extend([KeepTogether([Paragraph(inline(caption),S),Image(str(img),width=w*ratio,height=h*ratio)]),Spacer(1,12)]);i+=1;continue
  # Individual list lines preserve explicit numbering and safe paragraph wrapping.
  if re.match(r'^(?:\d+\. |- )',ln):story.append(Paragraph(inline(ln),B));i+=1;continue
  para=[ln];i+=1
  while i<len(lines) and lines[i].strip() and not re.match(r'^(?:#{1,4} |```|\||!\[|\d+\. |- )',lines[i]):para.append(lines[i]);i+=1
  story.append(Paragraph(inline(' '.join(para)),B))
 # Remove adjacent breaks generated around figures and following section headings.
 cleaned=[]
 for item in story:
  if isinstance(item,PageBreak) and (not cleaned or isinstance(cleaned[-1],PageBreak)):continue
  cleaned.append(item)
 if isinstance(cleaned[-1],PageBreak):cleaned.pop()
 def footer(c,d):
  c.saveState();c.setFont('Body',7);c.setFillColor(colors.HexColor('#647782'));c.drawString(50,28,'AOBP | Centrally managed policy; service-local RBAC and ABAC');c.drawRightString(562,28,str(d.page));c.restoreState()
 doc=SimpleDocTemplate(str(folder/(name+'.pdf')),pagesize=(612,792),leftMargin=50,rightMargin=50,topMargin=46,bottomMargin=48,title=name.replace('_',' '),author='AOBP Architecture')
 doc.build(cleaned,onFirstPage=footer,onLaterPages=footer)
 print(folder/(name+'.pdf'))
