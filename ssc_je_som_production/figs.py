import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt, numpy as np, os
from matplotlib.patches import Circle, Polygon, Rectangle
D=os.path.join(os.path.dirname(os.path.abspath(__file__)),'figs'); os.makedirs(D,exist_ok=True)
plt.rcParams.update({'font.size':9,'font.family':'DejaVu Sans'})
NAVY='#1b2a49'; OR='#b3470f'; GR='#2f855a'; PU='#6b46c1'; GY='#666666'; RD='#c53030'
def save(f,n): f.tight_layout(); f.savefig(f'{D}/{n}.png',dpi=170); plt.close(f)
def clean(ax):
    ax.set_xticks([]); ax.set_yticks([])
    for s in ('top','right'): ax.spines[s].set_visible(False)

# 1. Stress-strain curve of mild steel
f,ax=plt.subplots(figsize=(6.4,4))
e=[0,0.10,0.115,0.13,0.135,0.30,0.70,1.00,1.15]; s=[0,0.55,0.58,0.66,0.60,0.61,0.92,1.0,0.80]
ax.plot(e[:2],s[:2],color=NAVY,lw=2)
x=np.linspace(0.10,0.13,20); ax.plot(x,np.interp(x,[0.10,0.115,0.13],[0.55,0.58,0.66]),color=NAVY,lw=2)
ax.plot([0.13,0.135,0.30],[0.66,0.60,0.61],color=NAVY,lw=2)
x=np.linspace(0.30,1.0,60); ax.plot(x,0.61+0.39*np.sin((x-0.30)/0.70*np.pi/2),color=NAVY,lw=2)
x=np.linspace(1.0,1.15,20); ax.plot(x,1.0-0.20*((x-1.0)/0.15)**1.5,color=NAVY,lw=2)
x=np.linspace(0.30,1.15,60); ax.plot(x,0.61+0.39*np.sin(np.clip((x-0.30)/0.70,0,1.2)*np.pi/2)+np.where(x>1,0.35*(x-1)/0.15,0),color=GY,lw=1.2,ls='--')
pts=[(0.10,0.55,'A Proportional limit'),(0.115,0.58,'B Elastic limit'),(0.13,0.66,'C Upper yield'),(0.135,0.60,'D Lower yield'),(1.0,1.0,'E Ultimate stress'),(1.15,0.80,'F Fracture')]
for x0,y0,t in pts: ax.plot(x0,y0,'o',color=OR,ms=4)
ax.text(0.20,0.28,'A Proportional limit\nB Elastic limit\nC Upper yield point\nD Lower yield point',fontsize=7.5,color=OR)
ax.text(0.86,1.04,'E Ultimate stress',fontsize=8,color=OR); ax.text(1.0,0.72,'F Fracture',fontsize=8,color=OR)
ax.text(0.15,0.72,'Yielding',fontsize=8,color=GY); ax.text(0.55,0.70,'Strain hardening',fontsize=8,color=GY); ax.text(1.02,0.90,'Necking',fontsize=8,color=GY)
ax.text(0.95,1.20,'True stress–strain (dashed)',fontsize=7.5,color=GY)
ax.annotate('Slope = E',(0.05,0.28),xytext=(0.12,0.20),fontsize=8,arrowprops=dict(arrowstyle='->',color=GY))
ax.set_xlabel('Strain'); ax.set_ylabel('Stress'); clean(ax); ax.set_xlim(0,1.3); ax.set_ylim(0,1.3)
ax.set_title('Engineering stress–strain curve of mild steel (not to scale)')
save(f,'stress_strain')

# 2. Mohr's circle
f,ax=plt.subplots(figsize=(6.2,4.4)); sx,sy,t=80,-40,30; C=(sx+sy)/2; R=np.hypot((sx-sy)/2,t)
th=np.linspace(0,2*np.pi,300); ax.plot(C+R*np.cos(th),R*np.sin(th),color=NAVY,lw=2)
ax.axhline(0,color='k',lw=0.8); ax.axvline(0,color='k',lw=0.8)
ax.plot([sx,sy],[-t,t],color=OR,lw=1.5); ax.plot(sx,-t,'o',color=OR); ax.plot(sy,t,'o',color=OR)
ax.text(sx+3,-t-8,'X (σx, −τxy)',fontsize=8,color=OR); ax.text(sy-28,t+4,'Y (σy, τxy)',fontsize=8,color=OR)
ax.plot(C,0,'ko',ms=3); ax.text(C-6,-9,'C',fontsize=9)
ax.plot([C+R,C-R],[0,0],'o',color=GR); ax.text(C+R+2,4,'σ₁',color=GR,fontsize=10); ax.text(C-R-14,4,'σ₂',color=GR,fontsize=10)
ax.plot([C,C],[0,R],color=PU,lw=1.5,ls='--'); ax.text(C+2,R+3,'τ_max = R',color=PU,fontsize=9)
ax.text(C-R,-R-12,'Centre = (σx + σy)/2,   R = √[((σx − σy)/2)² + τxy²]',fontsize=8)
ax.set_aspect('equal'); ax.set_xlabel('Normal stress σ'); ax.set_ylabel('Shear stress τ'); ax.set_title("Mohr's circle for plane stress (σx = 80, σy = −40, τ = 30 MPa)")
ax.set_xlim(C-R-30,C+R+30); ax.set_ylim(-R-20,R+15)
save(f,'mohr')

# 3. Failure loci
f,ax=plt.subplots(figsize=(5.4,5.2)); th=np.linspace(0,2*np.pi,400)
hexx=[1,1,0,-1,-1,0,1]; hexy=[0,1,1,0,-1,-1,0]; ax.plot(hexx,hexy,color=RD,lw=2,label='Max shear (Tresca) – hexagon')
a=np.sqrt(2); b=np.sqrt(2/3)
u=a*np.cos(th); v=b*np.sin(th); ax.plot((u-v)/np.sqrt(2),(u+v)/np.sqrt(2),color=NAVY,lw=2,label='Distortion energy (von Mises) – ellipse')
ax.plot([1,1,-1,-1,1],[1,-1,-1,1,1],color=GR,lw=1.5,ls='--',label='Max principal stress (Rankine) – square')
ax.axhline(0,color='k',lw=0.6); ax.axvline(0,color='k',lw=0.6)
ax.set_xlabel('σ₁/σ_y'); ax.set_ylabel('σ₂/σ_y'); ax.set_aspect('equal'); ax.set_xlim(-1.5,1.5); ax.set_ylim(-1.5,1.7)
ax.legend(fontsize=7,loc='upper left'); ax.set_title('Failure envelopes in plane stress')
save(f,'failure')

# 4. SFD and BMD
f,axs=plt.subplots(3,2,figsize=(7.2,5.4),sharex='col')
L=1; x=np.linspace(0,L,200)
ax=axs[0,0]; ax.plot([0,1],[0,0],color='k',lw=3); ax.plot(0,-0.05,'^',color='k',ms=9); ax.plot(1,-0.05,'o',color='k',ms=7)
for xi in np.linspace(0.05,0.95,10): ax.annotate('',xy=(xi,0.02),xytext=(xi,0.25),arrowprops=dict(arrowstyle='->',color=OR))
ax.set_title('SSB with UDL w'); ax.set_ylim(-0.2,0.35); ax.axis('off')
ax=axs[1,0]; ax.fill_between(x,0.5-x,color=NAVY,alpha=0.3); ax.plot(x,0.5-x,color=NAVY); ax.axhline(0,color='k',lw=0.6); ax.text(0.02,0.42,'+wL/2',fontsize=8); ax.text(0.82,-0.45,'−wL/2',fontsize=8); ax.set_ylabel('SF'); ax.set_yticks([])
ax=axs[2,0]; ax.fill_between(x,x*(1-x)/2,color=OR,alpha=0.3); ax.plot(x,x*(1-x)/2,color=OR); ax.axhline(0,color='k',lw=0.6); ax.text(0.38,0.135,'wL²/8',fontsize=8); ax.set_ylabel('BM'); ax.set_yticks([]); ax.set_xticks([])
ax=axs[0,1]; ax.plot([0,1],[0,0],color='k',lw=3); ax.add_patch(Rectangle((-0.04,-0.2),0.04,0.4,color=GY)); ax.annotate('',xy=(1,0.02),xytext=(1,0.28),arrowprops=dict(arrowstyle='->',color=OR,lw=2)); ax.text(0.9,0.3,'W',color=OR)
ax.set_title('Cantilever with end load W'); ax.set_xlim(-0.1,1.1); ax.set_ylim(-0.25,0.4); ax.axis('off')
ax=axs[1,1]; ax.fill_between(x,0.5,color=NAVY,alpha=0.3); ax.plot(x,0.5+0*x,color=NAVY); ax.axhline(0,color='k',lw=0.6); ax.text(0.4,0.55,'+W (constant)',fontsize=8); ax.set_yticks([]); ax.set_ylim(-0.1,0.8)
ax=axs[2,1]; ax.fill_between(x,-(1-x)*0.5,color=OR,alpha=0.3); ax.plot(x,-(1-x)*0.5,color=OR); ax.axhline(0,color='k',lw=0.6); ax.text(0.03,-0.45,'−WL (hogging)',fontsize=8); ax.set_yticks([]); ax.set_xticks([])
save(f,'sfd_bmd')

# 5. Bending stress distribution
f,(a1,a2)=plt.subplots(1,2,figsize=(6.6,3.4),gridspec_kw={'width_ratios':[1,1.6]})
a1.add_patch(Rectangle((0.3,0),0.4,1,fill=False,lw=2,ec=NAVY)); a1.plot([0.15,0.85],[0.5,0.5],'--',color=RD); a1.text(0.72,0.53,'N.A.',color=RD,fontsize=8)
a1.text(0.43,1.03,'b',fontsize=9); a1.text(0.2,0.75,'d',fontsize=9); a1.set_xlim(0,1); a1.set_ylim(-0.1,1.15); a1.axis('off'); a1.set_title('Cross-section')
y=np.linspace(0,1,20); a2.plot([0,0],[0,1],color='k',lw=1); a2.plot((y-0.5)*2,y,color=NAVY,lw=2)
for yi in np.linspace(0,1,9): a2.annotate('',xy=((yi-0.5)*2,yi),xytext=(0,yi),arrowprops=dict(arrowstyle='->',color=OR,lw=1))
a2.text(-1.2,0.02,'σ_max (tension, below N.A. in sagging)',fontsize=7.5); a2.text(0.15,0.95,'σ_max (compression)',fontsize=7.5)
a2.plot([-1.3,1.3],[0.5,0.5],'--',color=RD); a2.text(0.6,0.43,'σ = 0 at N.A.',fontsize=8,color=RD)
a2.text(-1.25,0.6,'σ = My/I',fontsize=10,color=NAVY); a2.set_xlim(-1.4,1.4); a2.axis('off'); a2.set_title('Bending stress varies linearly with y')
save(f,'bending')

# 6. Shear stress distribution
f,axs=plt.subplots(1,3,figsize=(7.4,3.0))
y=np.linspace(-1,1,100)
ax=axs[0]; ax.plot(1.5*(1-y**2),y,color=NAVY,lw=2); ax.axvline(0,color='k',lw=0.8); ax.axvline(1,color=GY,ls=':'); ax.text(1.02,-0.9,'τ_avg',fontsize=7,color=GY); ax.text(0.6,0.05,'1.5 τ_avg',fontsize=8,color=OR); ax.set_title('Rectangle'); ax.axis('off')
ax=axs[1]; ax.plot((4/3)*(1-y**2),y,color=NAVY,lw=2); ax.axvline(0,color='k',lw=0.8); ax.axvline(1,color=GY,ls=':'); ax.text(0.45,0.05,'4/3 τ_avg',fontsize=8,color=OR); ax.set_title('Circle'); ax.axis('off')
ax=axs[2]; yy=np.linspace(-1,1,200); web=np.abs(yy)<0.8
tau=np.where(web,1.0+0.6*(1-(yy/0.8)**2),0.25*(1-((np.abs(yy)-0.8)/0.2)))
tau=np.where(np.abs(yy)>=0.8,0.25*(1-(np.abs(yy)-0.8)/0.2),tau)
ax.plot(tau,yy,color=NAVY,lw=2); ax.axvline(0,color='k',lw=0.8); ax.text(0.95,0.05,'max in web\nat N.A.',fontsize=7.5,color=OR); ax.text(0.3,0.85,'jump at\nflange–web',fontsize=7,color=GY); ax.set_title('I-section'); ax.axis('off')
save(f,'shear_dist')

# 7. Euler end conditions
f,axs=plt.subplots(1,4,figsize=(7.4,3.6)); y=np.linspace(0,1,100)
cases=[('Both hinged\nL_e = L',np.sin(np.pi*y),'h','h'),('Fixed–free\nL_e = 2L',1-np.cos(np.pi*y/2),'f','n'),('Both fixed\nL_e = L/2',(1-np.cos(2*np.pi*y))/2,'f','f'),('Fixed–hinged\nL_e = 0.7L',None,'f','h')]
for ax,(t,sh,b,tp) in zip(axs,cases):
    if sh is None:
        k=4.4934; sh=np.sin(k*y)-k*y*np.cos(k)+ (k*np.cos(k)-k)*0+0
        sh=(np.sin(k*(1-y))-(1-y)*np.sin(k)) ; sh=sh/np.max(np.abs(sh))
    ax.plot(0.25*sh,y,color=NAVY,lw=2); ax.plot([0,0],[0,1],':',color=GY)
    if b=='f': ax.add_patch(Rectangle((-0.25,-0.06),0.5,0.06,color=GY))
    else: ax.plot(0,-0.03,'^',color='k',ms=9)
    if tp=='f': ax.add_patch(Rectangle((-0.25,1.0),0.5,0.06,color=GY))
    elif tp=='h': ax.plot(0,1.03,'v',color='k',ms=9)
    ax.annotate('',xy=(0.25*sh[-1],1.0),xytext=(0.25*sh[-1],1.25),arrowprops=dict(arrowstyle='->',color=OR,lw=2))
    ax.set_title(t,fontsize=8.5); ax.set_xlim(-0.4,0.4); ax.set_ylim(-0.1,1.3); ax.axis('off')
f.suptitle('Buckled shapes and effective lengths (P_e = π²EI/L_e²)',fontsize=9.5)
save(f,'euler')

# 8. Simplified Fe-Fe3C diagram
f,ax=plt.subplots(figsize=(6.6,4.6))
ax.plot([0,0.022],[912,727],color=NAVY,lw=1.5)                 # alpha/alpha+gamma
ax.plot([0,0.8],[912,727],color=NAVY,lw=1.5)                   # A3
ax.plot([0.8,2.14],[727,1147],color=NAVY,lw=1.5)               # Acm
ax.plot([0.022,6.67],[727,727],color=RD,lw=1.5)                # A1
ax.plot([2.14,6.67],[1147,1147],color=RD,lw=1.5)               # eutectic line
ax.plot([0,0.5,4.3],[1539,1495,1147],color=OR,lw=1.5)          # liquidus left
ax.plot([4.3,6.67],[1147,1252],color=OR,lw=1.5)                # liquidus right
ax.plot([0.17,2.14],[1495,1147],color=GR,lw=1.5)               # solidus
ax.plot([0.1,0.5],[1495,1495],color=RD,lw=1.5)                 # peritectic
ax.plot([0,0.17],[1394,1495],color=GY,lw=1)
ax.plot([0.8,0.8],[600,727],':',color=GY); ax.plot([4.3,4.3],[600,1147],':',color=GY); ax.plot([2.14,2.14],[600,1147],':',color=GY)
for (x,y,t) in [(0.8,727,'Eutectoid 727 °C, 0.8% C'),(4.3,1147,'Eutectic 1147 °C, 4.3% C'),(0.17,1495,'Peritectic ≈ 1495 °C')]:
    ax.plot(x,y,'ko',ms=4)
ax.text(0.9,690,'Eutectoid 727 °C, 0.8% C (pearlite)',fontsize=7.5); ax.text(4.0,1170,'Eutectic 1147 °C, 4.3% C\n(ledeburite)',fontsize=7.5)
ax.text(0.3,1515,'Peritectic ≈ 1495 °C',fontsize=7.5)
ax.text(0.9,980,'Austenite γ',fontsize=9,color=NAVY); ax.text(2.6,1300,'Liquid',fontsize=9,color=OR)
ax.text(0.15,760,'α + γ',fontsize=8); ax.text(1.4,850,'γ + Fe₃C',fontsize=8); ax.text(3.5,1000,'γ + Fe₃C + ledeburite',fontsize=8)
ax.text(0.1,640,'α + Pearlite',fontsize=8); ax.text(1.0,640,'Pearlite + Fe₃C',fontsize=8); ax.text(4.0,640,'Pearlite + Fe₃C + transformed ledeburite',fontsize=7)
ax.text(1.0,1250,'γ + L',fontsize=8); ax.text(5.2,1170,'L + Fe₃C',fontsize=8)
ax.axvline(2.14,color=GY,lw=0.6,ls='--'); ax.text(0.5,560,'← Steels',fontsize=8,color=GY); ax.text(2.4,560,'Cast irons →',fontsize=8,color=GY)
ax.set_xlim(0,6.8); ax.set_ylim(540,1600); ax.set_xlabel('Carbon (wt %)'); ax.set_ylabel('Temperature (°C)')
ax.set_title('Iron–iron carbide diagram (simplified)')
save(f,'fe_c')

# 9. Merchant circle
f,ax=plt.subplots(figsize=(5.4,5.2)); ax.set_aspect('equal')
R=1.0; c=np.array([0,0]); th=np.linspace(0,2*np.pi,300); ax.plot(R*np.cos(th),R*np.sin(th),color=GY,lw=1)
alpha=np.radians(10); beta=np.radians(35); phi=np.radians(45+5-17.5)
ang_R=np.pi/2+ (beta-alpha)  # resultant direction from vertical reference
P=np.array([0,-R]); Q=np.array([0,R])  # diameter = resultant
ax.plot([P[0],Q[0]],[P[1],Q[1]],color='k',lw=2); ax.text(0.05,0.0,'R',fontsize=10)
# Fc horizontal component and Ft vertical: decompose diameter by a horizontal/vertical pair from P
Fc_end=np.array([R*np.sin(2*0.6),R*np.cos(2*0.6)])
def comp(a,col,l1,l2):
    X=np.array([R*np.sin(2*a),-R*np.cos(2*a)])
    ax.plot([P[0],X[0]],[P[1],X[1]],color=col,lw=1.8); ax.plot([X[0],Q[0]],[X[1],Q[1]],color=col,lw=1.8)
    m1=(P+X)/2; m2=(X+Q)/2; ax.text(m1[0]+0.03,m1[1],l1,color=col,fontsize=9); ax.text(m2[0]+0.03,m2[1],l2,color=col,fontsize=9)
comp(np.radians(55),OR,'F_c','F_t'); comp(np.radians(-30),NAVY,'N','F'); comp(np.radians(25),GR,'F_s','N_s')
ax.text(-1.0,-1.25,'Resultant R is the diameter; F_c–F_t (measured), F–N (rake face),\nF_s–N_s (shear plane) are perpendicular pairs.  μ = F/N = tanβ',fontsize=7.5)
ax.set_xlim(-1.2,1.3); ax.set_ylim(-1.45,1.2); ax.axis('off'); ax.set_title("Merchant's circle diagram (schematic)")
save(f,'merchant')

# 10. Tool life curves
f,(a1,a2)=plt.subplots(1,2,figsize=(7.2,3.2))
T=np.linspace(5,200,100)
for C,n,lab,col in [(80,0.125,'HSS (n ≈ 0.125)',OR),(300,0.25,'Carbide (n ≈ 0.25)',NAVY),(1000,0.5,'Ceramic (n ≈ 0.5)',GR)]:
    a1.plot(T,C/T**n,color=col,lw=2,label=lab); a2.loglog(T,C/T**n,color=col,lw=2,label=lab)
a1.set_xlabel('Tool life T (min)'); a1.set_ylabel('Cutting speed V (m/min)'); a1.legend(fontsize=7); a1.set_title('VTⁿ = C')
a2.set_xlabel('log T'); a2.set_ylabel('log V'); a2.set_title('Straight lines on log–log scale (slope −n)')
save(f,'tool_life')
print('figs done')
