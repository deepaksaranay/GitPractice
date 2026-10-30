import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt, numpy as np, os
D=os.path.join(os.path.dirname(os.path.abspath(__file__)),'figs')
plt.rcParams.update({'font.size':9,'font.family':'DejaVu Sans'})
NAVY='#1b2a49'; OR='#b3470f'
def save(f,n): f.tight_layout(); f.savefig(f'{D}/{n}.png',dpi=170); plt.close(f)

# stress strain
f,ax=plt.subplots(figsize=(6.4,3.6))
e=np.array([0,0.20,0.24,0.27,0.30,0.55,0.9,1.3,1.6,1.85,2.0])
sg=np.array([0,200,215,260,225,228,320,390,420,395,345])
ax.plot(e,sg,color=NAVY,lw=2)
tr=np.linspace(1.6,2.0,20); ax.plot(tr,420+(tr-1.6)*150,'--',color=OR,lw=1.3,label='True stress (keeps rising)')
pts=[(0.20,200,'A Proportional limit',(0.55,70)),(0.24,215,'B Elastic limit',(0.55,115)),(0.30,225,'D Lower yield point',(0.55,160)),(0.27,260,'C Upper yield point',(0.32,320)),(1.6,420,'E Ultimate stress – necking starts',(0.95,470)),(2.0,345,'F Fracture',(1.75,270))]
for x,y,t,o in pts:
    ax.plot(x,y,'o',color=OR,ms=4); ax.annotate(t,(x,y),xytext=o,fontsize=7.5,arrowprops=dict(arrowstyle='-',color='grey',lw=.6))
ax.text(0.75,255,'Strain hardening',fontsize=7.5,color='grey',rotation=22)
ax.set_xlim(0,2.15); ax.set_ylim(0,520)
ax.set_xlabel('Strain'); ax.set_ylabel('Engineering stress'); ax.set_title('Stress–strain curve of mild steel (schematic, not to scale)'); ax.set_xticks([]); ax.set_yticks([]); ax.legend(fontsize=7,loc='lower right')
save(f,'stress_strain')

# SFD BMD SS beam UDL & cantilever point load
f,axs=plt.subplots(2,2,figsize=(6.6,3.8))
x=np.linspace(0,1,100)
axs[0,0].fill_between(x,0.5-x,color='#9ab',alpha=.7); axs[0,0].set_title('SS beam, UDL – SFD (linear)',fontsize=8)
axs[1,0].fill_between(x,x*(1-x)*4,color='#e8b07a',alpha=.8); axs[1,0].set_title('BMD (parabola, max wL²/8 at centre)',fontsize=8)
axs[0,1].fill_between(x,np.ones_like(x),color='#9ab',alpha=.7); axs[0,1].set_title('Cantilever, end load W – SFD (constant)',fontsize=8)
axs[1,1].fill_between(x,-(1-x),color='#e8b07a',alpha=.8); axs[1,1].set_title('BMD (linear, max WL at fixed end)',fontsize=8)
for a in axs.flat: a.axhline(0,color='k',lw=.8); a.set_xticks([]); a.set_yticks([])
save(f,'sfd_bmd')

# Otto & Diesel pV
f,axs=plt.subplots(1,2,figsize=(6.6,3))
g=1.4; v1,v2=6,1
def ad(va,vb,pa): v=np.linspace(va,vb,60); return v,pa*(va/v)**g
# Otto
p1=1; v,p=ad(v1,v2,p1); p2=p[-1]; p3=p2*2.2; vv,pp=ad(v2,v1,p3)
a=axs[0]; a.plot(v,p,color=NAVY); a.plot([v2,v2],[p2,p3],color=OR); a.plot(vv,pp,color=NAVY); a.plot([v1,v1],[pp[-1],p1],color=OR)
a.set_title('Otto: 2 isentropic + 2 const-V',fontsize=8)
for (xx,yy,t) in [(v1,p1,'1'),(v2,p2,'2'),(v2,p3,'3'),(v1,pp[-1],'4')]: a.annotate(t,(xx,yy),fontsize=8,color='r')
# Diesel
v,p=ad(16,1,1); p2=p[-1]; v3=2.2; vv,pp=ad(v3,16,p2)
a=axs[1]; a.plot(v,p,color=NAVY); a.plot([1,v3],[p2,p2],color=OR); a.plot(vv,pp,color=NAVY); a.plot([16,16],[pp[-1],1],color=OR)
a.set_title('Diesel: const-p heat addition',fontsize=8)
for (xx,yy,t) in [(16,1,'1'),(1,p2,'2'),(v3,p2,'3'),(16,pp[-1],'4')]: a.annotate(t,(xx,yy),xytext=(3,3),textcoords='offset points',fontsize=8,color='r')
for a in axs: a.set_xlabel('V'); a.set_ylabel('p'); a.set_xticks([]); a.set_yticks([])
save(f,'cycles')

# VCR p-h
f,ax=plt.subplots(figsize=(5.6,3.2))
h=np.linspace(0,1,100); dome_l=np.linspace(0.2,0.55,50); dome_r=np.linspace(0.55,0.85,50)
ax.plot(dome_l,np.log(1+ (dome_l-0.2)*25),color='grey'); ax.plot(dome_r,np.log(1+(0.85-dome_r)*26.4),color='grey')
pL,pH=np.log(1+0.2*25)*0.35,np.log(1+0.2*25)*0.8
h1,h3=0.8,0.33; h2=0.93
ax.plot([h3,h3],[pH,pL],color=OR,lw=2); ax.plot([h3,h1],[pL,pL],color=NAVY,lw=2); ax.plot([h1,h2],[pL,pH],color=NAVY,lw=2); ax.plot([h2,h3],[pH,pH],color=NAVY,lw=2)
for x,y,t in [(h1,pL,'1'),(h2,pH,'2'),(h3,pH,'3'),(h3,pL,'4')]: ax.annotate(t,(x,y),xytext=(4,4),textcoords='offset points',color='r')
ax.text(0.5,pL-0.12,'Evaporator (RE = h1 − h4)',fontsize=7.5,ha='center'); ax.text(0.6,pH+0.05,'Condenser',fontsize=7.5,ha='center')
ax.text(h3-0.02,(pL+pH)/2,'Throttle\n(h const)',fontsize=7,ha='right'); ax.text(h2+0.01,(pL+pH)/2,'Compressor\n(s const)',fontsize=7)
ax.set_xlabel('Enthalpy h'); ax.set_ylabel('log p'); ax.set_xticks([]); ax.set_yticks([]); ax.set_title('Simple VCR cycle on p–h chart',fontsize=9)
save(f,'vcr')

# psychro processes
f,ax=plt.subplots(figsize=(6.4,3.8))
t=np.linspace(0,46,200); ps=0.6108*np.exp(17.27*t/(t+237.3)); ws=0.622*ps/(101.325-ps)
ax.plot(t,ws,color='grey'); ax.text(13.5,0.0128,'Saturation curve (100% RH)',fontsize=7,rotation=33,color='grey')
c=(30,0.010); ax.plot(*c,'ko'); ax.text(30.4,0.0092,'O',fontsize=8)
arr=[((44,0.010),'Sensible heating',(40.5,0.0090)),((18,0.010),'Sensible cooling',(11.0,0.0103)),((30,0.019),'Humidification',(30.4,0.0193)),((30,0.004),'Dehumidification',(30.4,0.0033)),
     ((15,0.0085),'Cooling & dehumidification',(4.0,0.0072)),((42,0.017),'Heating &\nhumidification',(40.5,0.0178)),((22,0.0132),'Evaporative cooling\n(along WBT line)',(11.0,0.0150))]
for (x,y),lab,(tx,ty) in arr:
    ax.annotate('',xy=(x,y),xytext=c,arrowprops=dict(arrowstyle='->',color=OR,lw=1.2)); ax.text(tx,ty,lab,fontsize=7)
ax.set_xlim(0,48); ax.set_ylim(0,0.03)
ax.set_xlabel('Dry bulb temperature →'); ax.set_ylabel('Specific humidity ω →'); ax.set_xticks([]); ax.set_yticks([]); ax.set_title('Psychrometric processes from state O (schematic)',fontsize=9)
save(f,'psychro')

# Fe-C simplified
f,ax=plt.subplots(figsize=(6.2,3.8))
ax.plot([0,0.8,2.0],[910,723,1147],color=NAVY)  # A3 and Acm
ax.plot([0.025,6.67],[723,723],color=NAVY); ax.plot([2.0,6.67],[1147,1147],color=NAVY)
ax.plot([0,4.3,6.67],[1539,1147,1550],color=NAVY,ls='--'); ax.plot([0,2.0],[1495,1147],color=NAVY,lw=.8)
ax.plot([0,0.025],[910,723],color=NAVY,lw=.8)
for x,y,s in [(0.8,723,'Eutectoid 0.8%C, 723°C'),(4.3,1147,'Eutectic 4.3%C, 1147°C'),(2.0,1147,'2.0%C')]:
    ax.plot(x,y,'o',color=OR); ax.annotate(s,(x,y),xytext=(5,-12),textcoords='offset points',fontsize=7)
ax.text(0.6,1000,'γ (Austenite)',fontsize=8); ax.text(0.15,600,'α + Pearlite',fontsize=7); ax.text(1.2,600,'Pearlite + Fe₃C',fontsize=7)
ax.text(3.2,900,'γ + Fe₃C',fontsize=7); ax.text(2.5,1350,'Liquid',fontsize=8); ax.text(4.6,600,'Pearlite + Fe₃C\n(+ ledeburite)',fontsize=7)
ax.axvline(2.0,color='grey',ls=':',lw=.8); ax.text(0.7,450,'STEEL',fontsize=8,color=OR); ax.text(3.8,450,'CAST IRON',fontsize=8,color=OR)
ax.set_xlim(0,6.8); ax.set_ylim(400,1600); ax.set_xlabel('% Carbon'); ax.set_ylabel('Temperature °C'); ax.set_title('Iron–carbon diagram (simplified)',fontsize=9)
save(f,'fec')
print('ok')
