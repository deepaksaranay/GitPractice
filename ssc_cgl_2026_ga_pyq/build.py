import re, sys, glob, os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, PageBreak,
    Table, TableStyle, KeepTogether, Image, NextPageTemplate)
from reportlab.platypus.tableofcontents import TableOfContents

D='/usr/share/fonts/truetype/dejavu/'
pdfmetrics.registerFont(TTFont('S',D+'DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('SB',D+'DejaVuSans-Bold.ttf'))
pdfmetrics.registerFont(TTFont('M',D+'DejaVuSansMono.ttf'))
pdfmetrics.registerFont(TTFont('MB',D+'DejaVuSansMono-Bold.ttf'))
pdfmetrics.registerFontFamily('S',normal='S',bold='SB',italic='S',boldItalic='SB')
pdfmetrics.registerFontFamily('M',normal='M',bold='MB',italic='M',boldItalic='MB')

SRC=sys.argv[1]; OUT=sys.argv[2]
NAVY=colors.HexColor('#1b2a49'); 
st=lambda n,**k: ParagraphStyle(n,**k)
body=st('body',fontName='S',fontSize=10,leading=14.6,alignment=TA_JUSTIFY,spaceAfter=3.5)
bul=st('bul',parent=body,leftIndent=14,bulletIndent=3,bulletFontName='S',spaceAfter=1.8,alignment=0)
h1=st('h1',fontName='SB',fontSize=22,leading=27,textColor=colors.white)
h2=st('h2',fontName='SB',fontSize=13,leading=16,textColor=NAVY,spaceBefore=10,spaceAfter=4)
h3=st('h3',fontName='SB',fontSize=10.5,leading=13,textColor=colors.HexColor('#7a2e0e'),spaceBefore=6,spaceAfter=2)
fm=st('fm',fontName='S',fontSize=9.4,leading=13.4,alignment=0)
bx=st('bx',fontName='S',fontSize=9.6,leading=13.6,alignment=0)
cell=st('cell',fontName='S',fontSize=9,leading=12,alignment=0)
cellh=st('cellh',parent=cell,fontName='SB',textColor=colors.white)

def esc(t):
    t=t.replace('&','&amp;')
    t=re.sub(r'<(?!/?(b|i|sub|super|font|br)\b)','&lt;',t)
    return t

class Doc(BaseDocTemplate):
    def afterFlowable(self,f):
        if hasattr(f,'_toc'):
            lvl,txt=f._toc
            self.notify('TOCEntry',(lvl,txt,self.page))
    def __init__(s,fn):
        super().__init__(fn,pagesize=A4,leftMargin=1.8*cm,rightMargin=1.8*cm,topMargin=2*cm,bottomMargin=1.8*cm,
            title='SSC CGL 2026 GA - Reported Questions with Explanations',author='Prepared with Claude')
        fr=Frame(s.leftMargin,s.bottomMargin,s.width,s.height,id='f')
        s.cur=''
        s.addPageTemplates([PageTemplate(id='p',frames=[fr],onPageEnd=s.deco)])
    def beforeDocument(s):
        s.cur=''
    def deco(s,c,d):
        if d.page==1: return
        c.saveState()
        c.setFont('S',7.5); c.setFillColor(colors.grey)
        c.drawString(1.8*cm,A4[1]-1.2*cm,'SSC CGL 2026 Tier-1 • GA Reported Questions + Explanations')
        c.drawRightString(A4[0]-1.8*cm,A4[1]-1.2*cm,s.cur)
        c.setStrokeColor(colors.lightgrey); c.line(1.8*cm,A4[1]-1.35*cm,A4[0]-1.8*cm,A4[1]-1.35*cm)
        c.drawCentredString(A4[0]/2,1*cm,'– %d –'%d.page)
        c.restoreState()

from reportlab.platypus import Flowable
class SetCur(Flowable):
    def __init__(s,t): super().__init__(); s.t=t
    def wrap(s,a,b): return (0,0)
    def draw(s): doc.cur=s.t

def box(label,text,bg,bd):
    p=Paragraph('<b>%s</b> %s'%(label,esc(text)),bx)
    t=Table([[p]],colWidths=[17.4*cm])
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),bg),('BOX',(0,0),(-1,-1),0.8,bd),
        ('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4)]))
    return [t,Spacer(1,5)]

def fbox(lines):
    ps=[Paragraph(esc(l),fm) for l in lines]
    t=Table([[p] for p in ps],colWidths=[17.4*cm])
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),colors.HexColor('#fff8e1')),('BOX',(0,0),(-1,-1),0.8,colors.HexColor('#e0a800')),
        ('LINEBEFORE',(0,0),(0,-1),3,colors.HexColor('#e0a800')),
        ('LEFTPADDING',(0,0),(-1,-1),8),('TOPPADDING',(0,0),(-1,-1),1.2),('BOTTOMPADDING',(0,0),(-1,-1),1.2)]))
    return [t,Spacer(1,5)]

def tbl(rows):
    n=max(len(r) for r in rows); rows=[r+['']*(n-len(r)) for r in rows]; w=17.4*cm/n
    data=[[Paragraph(esc(c),cellh if i==0 else cell) for c in r] for i,r in enumerate(rows)]
    t=Table(data,colWidths=[w]*n,repeatRows=1)
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),NAVY),('GRID',(0,0),(-1,-1),0.4,colors.grey),
        ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#eef2f8')]),('VALIGN',(0,0),(-1,-1),'TOP'),
        ('TOPPADDING',(0,0),(-1,-1),2.5),('BOTTOMPADDING',(0,0),(-1,-1),2.5)]))
    return [t,Spacer(1,6)]

def banner(num,title):
    t=Table([[Paragraph('INTRODUCTION' if num=='0' else 'CHAPTER %s'%num,st('x',fontName='SB',fontSize=9,textColor=colors.HexColor('#ffcc66'))),],
             [Paragraph(esc(title),h1)]],colWidths=[17.4*cm])
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),NAVY),('LEFTPADDING',(0,0),(-1,-1),12),('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),10)]))
    return t

story=[]; doc=Doc(OUT)
toc=TableOfContents(); toc.levelStyles=[
    st('t0',fontName='SB',fontSize=10,leading=15,leftIndent=0),
    st('t1',fontName='S',fontSize=8.3,leading=11,leftIndent=14)]

# cover
story+= [Spacer(1,5*cm),Paragraph('SSC CGL 2026',st('c1',fontName='SB',fontSize=44,leading=50,alignment=TA_CENTER,textColor=NAVY)),
 Paragraph('GENERAL AWARENESS – ASKED QUESTIONS',st('c2',fontName='SB',fontSize=26,leading=32,alignment=TA_CENTER,textColor=colors.HexColor('#b3470f'))),
 Spacer(1,1*cm),Paragraph('Reported Questions with Explanations',st('c3',fontName='SB',fontSize=18,alignment=TA_CENTER)),
 Spacer(1,.4*cm),Paragraph('Tier-1 (30 Sep – Oct 2026, new pattern) • Static GS only • Chapter-wise',st('c4',fontName='S',fontSize=11,alignment=TA_CENTER,leading=16)),
 Spacer(1,1.5*cm),
 Paragraph('History • Art &amp; Culture • Polity • Geography • Economy • Science • Static GK – questions reported by candidates from SSC CGL 2026 Tier-1 shifts, compiled from coaching-site analyses, each with a full explanation',st('c5',fontName='S',fontSize=10,alignment=TA_CENTER,leading=15,textColor=colors.HexColor('#444444'))),
 Spacer(1,6*cm),
 Paragraph('Memory-based (candidate-recalled) questions, not an official SSC paper. Verify answers with the official SSC answer key when released. Explanations are original.',st('c6',fontName='S',fontSize=8.5,alignment=TA_CENTER,textColor=colors.grey,leading=12)),
 PageBreak(),
 Paragraph('Contents',st('tc',fontName='SB',fontSize=18,textColor=NAVY,spaceAfter=8)),toc,PageBreak()]

def flush_list(items):
    return [Paragraph(esc(i),bul,bulletText='•') for i in items]

chno=0
FORM=[];PYQ=[];curch=None
SKIP=('Read This First','Excluded','Sources')
for fn in sorted(glob.glob(SRC+'/*.txt')):
    lab=re.match(r'(\d+)([a-z]?)',os.path.basename(fn)); chlab=str(int(lab.group(1)))+lab.group(2).upper()
    lines=open(fn,encoding='utf8').read().split('\n')
    bl=[];fl=[];tr=[];para=[]
    def fl_all():
        global story
        if para: story.append(Paragraph(esc(' '.join(para)),body)); para.clear()
        if bl: story+=flush_list(bl); bl.clear(); story.append(Spacer(1,3))
        if fl: story+=fbox(fl); fl.clear()
        if tr: story+=tbl(tr); tr.clear()
    for ln in lines:
        s=ln.rstrip()
        if not s.strip(): fl_all(); continue
        if s.startswith('# '):
            fl_all(); chno+=1; curch=s[2:]
            if not curch.startswith(SKIP): FORM.append((curch,[])); PYQ.append((curch,[]))
            story.append(PageBreak())
            m=Paragraph('<a name="c%d"/>'%chno,body); m._toc=(0,s[2:] if chlab=='0' else '%s. %s'%(chlab,s[2:])); 
            sc=SetCur(s[2:])
            story.append(sc); story.append(m); story.append(banner(chlab,s[2:])); story.append(Spacer(1,8))
        elif s.startswith('## '):
            fl_all(); p=Paragraph(esc(s[3:]),h2); p._toc=(1,s[3:]); story.append(p)
        elif s.startswith('### '):
            fl_all(); story.append(Paragraph(esc(s[4:]),h3))
        elif s.startswith('- '):
            if para: fl_all()
            if fl or tr: fl_all()
            bl.append(s[2:])
        elif s.startswith('F: '):
            if bl or para or tr: fl_all()
            fl.append(s[3:])
            if curch and not curch.startswith(SKIP): FORM[-1][1].append(s[3:])
        elif s.startswith('|'):
            if bl or para or fl: fl_all()
            tr.append([c.strip() for c in s.strip().strip('|').split('|')])
        elif s.startswith('PYQ-TREND: '):
            if curch and not curch.startswith(SKIP): PYQ[-1][1].append(s[11:])
            fl_all(); story+=box('★ REVISE NEXT:',s[11:],colors.HexColor('#e8f1fb'),colors.HexColor('#2b6cb0'))
        elif s.startswith('TIP: '):
            fl_all(); story+=box('✔ TOPPER TRICK:',s[5:],colors.HexColor('#e9f7ec'),colors.HexColor('#2f855a'))
        elif s.startswith('WARN: '):
            fl_all(); story+=box('✖ COMMON MISTAKE:',s[6:],colors.HexColor('#fdecec'),colors.HexColor('#c53030'))
        elif s.startswith('RQ: '):
            fl_all(); story+=box('▶ REPORTED QUESTION:',s[4:],colors.HexColor('#fff3e6'),colors.HexColor('#dd6b20'))
        elif s.startswith('ANS: '):
            fl_all(); story+=box('✔ ANSWER:',s[5:],colors.HexColor('#e9f7ec'),colors.HexColor('#2f855a'))
        elif s.startswith('Q: '):
            fl_all(); story+=box('✎ DESCRIPTIVE Q:',s[3:],colors.HexColor('#f3ecfa'),colors.HexColor('#6b46c1'))
        elif s.startswith('FIG: '):
            fl_all()
            p=os.path.join(os.path.dirname(os.path.abspath(__file__)),'figs',s[5:].strip()+'.png')
            if os.path.exists(p):
                from PIL import Image as PI
                w,h=PI.open(p).size; W=11*cm
                story+=[Image(p,width=W,height=W*h/w,hAlign='CENTER'),Spacer(1,5)]
        elif s.strip()=='---':
            fl_all(); story.append(PageBreak())
        else:
            if bl or fl or tr: fl_all()
            para.append(s.strip())
    fl_all()


def appendix(title,sub,items,kind):
    global story
    story.append(PageBreak()); story.append(SetCur(title))
    m=Paragraph('',body); m._toc=(0,title); story.append(m)
    t=Table([[Paragraph('APPENDIX',st('x2',fontName='SB',fontSize=9,textColor=colors.HexColor('#ffcc66')))],[Paragraph(esc(title),h1)]],colWidths=[17.4*cm])
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),NAVY),('LEFTPADDING',(0,0),(-1,-1),12),('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),10)]))
    story+=[t,Spacer(1,6),Paragraph(esc(sub),body)]
    for ch,lst in items:
        if not lst: continue
        p=Paragraph(esc(ch),h2); p._toc=(1,ch); story.append(p)
        if kind=='f': story+=fbox(lst)
        else: story+=[Paragraph(esc(x),bul,bulletText='★') for x in lst]
appendix('Appendix A – One-Place Answer Sheet','Every yellow strip (answers and key facts) from the chapters, collected chapter by chapter.',FORM,'f')
appendix('Appendix B – What to Revise Next','All "revise next" boxes in one place, chapter-wise.',PYQ,'p')
doc.multiBuild(story)
print('done')
