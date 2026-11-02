from pathlib import Path
import re, html, textwrap
from reportlab.pdfgen import canvas
from reportlab.platypus import BaseDocTemplate,PageTemplate,Frame,Paragraph,Spacer,PageBreak,NextPageTemplate,Table,TableStyle,Image,KeepTogether,Preformatted
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4,A3,landscape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PIL import Image as PILImage

ROOT=Path('output'); MD=ROOT/'AOBP_Platform_Architecture_Design.md'
for name,file in [('Body','DejaVuSans.ttf'),('Body-Bold','DejaVuSans-Bold.ttf'),('Body-Oblique','DejaVuSans.ttf'),('Body-BoldOblique','DejaVuSans-Bold.ttf'),('Mono','DejaVuSansMono.ttf')]:
 pdfmetrics.registerFont(TTFont(name,'/usr/share/fonts/truetype/dejavu/'+file))
pdfmetrics.registerFontFamily('Body',normal='Body',bold='Body-Bold',italic='Body-Oblique',boldItalic='Body-BoldOblique')
INK=colors.HexColor('#24394A');TEAL=colors.HexColor('#397C78');BLUE=colors.HexColor('#E9F1F8');GRAY=colors.HexColor('#526779')
PW,PH=A4; LW,LH=landscape(A3); M=46; CW=PW-2*M
style=ParagraphStyle('Body',fontName='Body',fontSize=9.6,leading=14.6,textColor=INK,spaceAfter=8,splitLongWords=True,allowWidows=0,allowOrphans=0)
h1=ParagraphStyle('H1',parent=style,fontName='Body-Bold',fontSize=20,leading=25,spaceAfter=16,textColor=TEAL,keepWithNext=True)
h2=ParagraphStyle('H2',parent=style,fontName='Body-Bold',fontSize=12,leading=17,spaceBefore=13,spaceAfter=7,keepWithNext=True)
cell=ParagraphStyle('Cell',parent=style,fontSize=8,leading=11.6,spaceAfter=0,allowWidows=1,allowOrphans=1)
chead=ParagraphStyle('CellHead',parent=cell,fontName='Body-Bold',textColor=colors.white)
small=ParagraphStyle('Small',parent=style,fontSize=8,leading=11,textColor=GRAY)
code=ParagraphStyle('Code',fontName='Mono',fontSize=7,leading=10,textColor=INK,backColor=colors.HexColor('#F3F6F8'),borderPadding=9,spaceBefore=5,spaceAfter=10)

def inline(t):
 t=html.escape(t)
 t=re.sub(r'`([^`]+)`',lambda m:'<font name="Mono" size="8">'+m.group(1)+'</font>',t)
 t=re.sub(r'\*\*([^*]+)\*\*',r'<b>\1</b>',t)
 t=re.sub(r'\[([^\]]+)\]\((https?[^)]+)\)',r'<link href="\2" color="#397C78">\1</link>',t)
 return t

class Doc(BaseDocTemplate):
 def afterFlowable(self,flowable):
  if isinstance(flowable,Paragraph) and flowable.style.name=='H1' and re.match(r'^\d+\.',flowable.getPlainText()):
   txt=flowable.getPlainText();key='sec-'+txt.split('.')[0];self.canv.bookmarkPage(key);self.canv.addOutlineEntry(txt,key,0)
   self.notify('TOCEntry',(0,txt,self.page,key))

def page(c,d):
 w,h=c._pagesize
 c.setFillColor(TEAL);c.rect(0,h-7,w,7,fill=1,stroke=0)
 c.setFont('Body',8);c.setFillColor(GRAY)
 c.drawString(M,h-28,'AOBP PLATFORM  /  ARCHITECTURE & ENGINEERING SPECIFICATION')
 c.drawRightString(w-M,h-28,'VERSION 2.3')
 c.setStrokeColor(colors.HexColor('#D6E0E5'));c.line(M,37,w-M,37)
 c.setFont('Body',7.5);c.drawString(M,23,'Architecture baseline · 02 November 2026 · Implementation requires validation')
 c.drawRightString(w-M,23,str(d.page))

doc=Doc(str(ROOT/'AOBP_Platform_Architecture_Design.pdf'),pagesize=A4,leftMargin=M,rightMargin=M,topMargin=51,bottomMargin=49,title='AOBP Platform Architecture, API and Engineering Specification',author='AOBP Architecture',allowSplitting=1)
doc.addPageTemplates([PageTemplate(id='Text',frames=[Frame(M,49,CW,PH-100,id='text',leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0)],onPage=page,pagesize=A4),PageTemplate(id='Diagram',frames=[Frame(M,49,LW-2*M,LH-100,id='diagram',leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0)],onPage=page,pagesize=(LW,LH))])
story=[]
story.append(Spacer(1,60))
story.append(Paragraph('AOBP Platform',ParagraphStyle('Cover',parent=h1,fontSize=35,leading=42)))
story.append(Paragraph('Architecture, API and<br/>Engineering Specification',ParagraphStyle('SubCover',parent=style,fontSize=21,leading=29,spaceAfter=28)))
story.append(Paragraph('Secure browser access with BFF and corporate SSO',ParagraphStyle('CoverTag',parent=h2,fontSize=15,leading=21)))
story.append(Paragraph('AWS EKS · Application Load Balancer · Spring Cloud Gateway · Spring Boot BFF',style))
story.append(Spacer(1,25))
summary=Table([[Paragraph('<b>Selected browser business route</b><br/><br/>ALB → API Gateway → BFF → private business APIs',style)]],colWidths=[CW])
summary.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),colors.HexColor('#E5F2EF')),('BOX',(0,0),(-1,-1),.7,TEAL),('LEFTPADDING',(0,0),(-1,-1),16),('RIGHTPADDING',(0,0),(-1,-1),16),('TOPPADDING',(0,0),(-1,-1),15),('BOTTOMPADDING',(0,0),(-1,-1),10)]));story.append(summary)
story.append(Spacer(1,25))
story.append(Paragraph('Version 2.3 | 2 November 2026',h2))
story.append(Paragraph('Retains the source document\'s 23-section structure. Includes plain-language request journeys, implementation responsibilities, security risks, acceptance criteria and seven high-resolution architecture illustrations.',style))
story.append(Paragraph('Design status: architecture baseline for implementation and validation. Proposed values are distinguished from standards and measured operating results.',small))
story.append(PageBreak())
story.append(Paragraph('Document guide',h1))
story.append(Paragraph('The numbered sections retain the source organization. Diagram pages use a larger landscape sheet so their text remains readable when zoomed or printed.',style))
toc=TableOfContents();toc.levelStyles=[ParagraphStyle('TOC',fontName='Body',fontSize=9.5,leading=13,textColor=INK,spaceBefore=3,leftIndent=0,firstLineIndent=0,rightIndent=25)]
story.append(toc);story.append(PageBreak())

lines=MD.read_text().splitlines();i=next(k for k,v in enumerate(lines) if v.startswith('## 1.'))
figure_count=0
pending_figures=[]
def flush_figures():
 for caption,path in pending_figures:
  story.append(NextPageTemplate('Diagram'));story.append(PageBreak())
  story.append(Paragraph(caption,h2))
  file=ROOT/path;w,h=PILImage.open(file).size;ratio=min((LW-2*M)/w,(LH-146)/h)
  story.append(Image(str(file),width=w*ratio,height=h*ratio,hAlign='CENTER'))
  story.append(NextPageTemplate('Text'))
 pending_figures.clear()

while i<len(lines):
 ln=lines[i]
 if not ln.strip():i+=1;continue
 if ln.startswith('## '):
  if not ln.startswith('## 1.'):
   flush_figures()
   story.append(PageBreak())
  story.append(Paragraph(inline(ln[3:]),h1));i+=1;continue
 if ln.startswith('### '):story.append(Paragraph(inline(ln[4:]),h2));i+=1;continue
 if ln.startswith('```'):
  language=ln[3:];i+=1;block=[]
  while i<len(lines) and not lines[i].startswith('```'):
   line=lines[i].expandtabs(4)
   if len(line)>110:
    block.extend(textwrap.wrap(line,width=110,subsequent_indent='    ',replace_whitespace=False,drop_whitespace=False))
   else:block.append(line)
   i+=1
  story.append(Paragraph((language.upper() or 'REFERENCE')+' · illustrative specification',small))
  # One flowable per line permits reliable page breaks for long source examples.
  for j,line in enumerate(block):
   st=ParagraphStyle('CodeLine',parent=code,spaceBefore=0,spaceAfter=0,borderPadding=4)
   story.append(Preformatted(line or ' ',st))
  story.append(Spacer(1,12));i+=1;continue
 if ln.startswith('|'):
  rows=[]
  while i<len(lines) and lines[i].startswith('|'):
   raw=lines[i].strip().strip('|').split('|');i+=1
   if all(re.fullmatch(r'[\s:-]+',r) for r in raw):continue
   rows.append([r.strip() for r in raw])
  n=max(map(len,rows));rows=[r+['']*(n-len(r)) for r in rows]
  if n==2:weights=[.32,.68]
  elif n==3:weights=[.23,.36,.41]
  elif n==4:weights=[.21,.25,.25,.29]
  else:weights=[1/n]*n
  content=[[Paragraph(inline(c),chead if j==0 else cell) for c in row] for j,row in enumerate(rows)]
  tab=Table(content,colWidths=[CW*v for v in weights],repeatRows=1,hAlign='LEFT')
  tab.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),TEAL),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.HexColor('#F1F5F7'),colors.white]),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7),('LINEBELOW',(0,0),(-1,0),.5,TEAL),('LINEBELOW',(0,1),(-1,-1),.3,colors.HexColor('#D6E0E5'))]))
  story.extend([tab,Spacer(1,11)]);continue
 m=re.match(r'!\[(.*?)\]\((.*?)\)',ln)
 if m:
  caption,path=m.groups();figure_count+=1
  pending_figures.append((caption,path))
  story.append(Paragraph('<b>'+inline(caption)+'</b><br/>See the landscape diagram plate following this section.',small))
  i+=1;continue
 if re.match(r'^\d+\. ',ln):
  num,txt=ln.split('. ',1)
  st=ParagraphStyle('List',parent=style,leftIndent=18,firstLineIndent=-18)
  story.append(Paragraph('<b>'+num+'.</b> '+inline(txt),st));i+=1;continue
 if ln.startswith('- '):
  st=ParagraphStyle('Bullet',parent=style,leftIndent=12,firstLineIndent=-12)
  story.append(Paragraph('• '+inline(ln[2:]),st));i+=1;continue
 paras=[ln];i+=1
 while i<len(lines) and lines[i].strip() and not re.match(r'^(#{1,4} |```|\||!\[|\d+\. |- )',lines[i]):paras.append(lines[i]);i+=1
 story.append(Paragraph(inline(' '.join(paras)),style))

flush_figures()
doc.multiBuild(story)
print('Built PDF with',figure_count,'diagram plates')
