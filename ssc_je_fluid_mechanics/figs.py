import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt, numpy as np, os
D=os.path.join(os.path.dirname(os.path.abspath(__file__)),'figs')
plt.rcParams.update({'font.size':9,'font.family':'DejaVu Sans'})
NAVY='#1b2a49'; OR='#b3470f'; GR='#2f855a'; PU='#6b46c1'; GY='#666666'
def save(f,n): f.tight_layout(); f.savefig(f'{D}/{n}.png',dpi=170); plt.close(f)

# rheology
f,ax=plt.subplots(figsize=(6.2,3.8)); x=np.linspace(0,1,100)
ax.plot(x,0.8*x,color=NAVY,lw=2,label='Newtonian (water, air)')
ax.plot(x,0.8*x**0.5,color=OR,lw=2,label='Pseudoplastic, n<1 (blood, paint)')
ax.plot(x,0.8*x**2,color=GR,lw=2,label='Dilatant, n>1 (starch, quicksand)')
ax.plot(x,0.3+0.6*x,color=PU,lw=2,label='Bingham plastic (toothpaste)')
ax.plot([0,1],[0,0],color=GY,lw=2,ls='--',label='Ideal fluid (τ = 0)')
ax.plot([0,0],[0,1],color='k',lw=2,label='Ideal solid')
ax.set_xlabel('Rate of shear strain du/dy'); ax.set_ylabel('Shear stress τ'); ax.set_xticks([]); ax.set_yticks([])
ax.set_xlim(-0.02,1.02); ax.set_ylim(-0.05,1.0); ax.legend(fontsize=7,loc='upper left'); ax.set_title('Rheological diagram')
ax.annotate('Yield stress τy',(0,0.3),xytext=(0.08,0.15),fontsize=7,arrowprops=dict(arrowstyle='->',color=GY))
save(f,'rheology')

# pressure references
f,ax=plt.subplots(figsize=(6.2,3.4))
ax.axhline(0,color='k',lw=1.5); ax.text(0.02,-0.12,'Absolute zero (perfect vacuum)',fontsize=8)
ax.axhline(1,color=NAVY,lw=1.5,ls='--'); ax.text(0.02,1.04,'Local atmospheric pressure',fontsize=8,color=NAVY)
ax.annotate('',xy=(0.3,1.8),xytext=(0.3,1),arrowprops=dict(arrowstyle='<->',color=OR)); ax.text(0.32,1.35,'Gauge pressure',color=OR,fontsize=8)
ax.annotate('',xy=(0.15,1.8),xytext=(0.15,0),arrowprops=dict(arrowstyle='<->',color=GR)); ax.text(0.17,0.5,'Absolute\npressure',color=GR,fontsize=8)
ax.plot(0.3,1.8,'o',color=OR); ax.text(0.33,1.8,'Point A (above atmospheric)',fontsize=8)
ax.annotate('',xy=(0.75,1),xytext=(0.75,0.4),arrowprops=dict(arrowstyle='<->',color=PU)); ax.text(0.77,0.7,'Vacuum (negative gauge)',color=PU,fontsize=8)
ax.annotate('',xy=(0.65,0.4),xytext=(0.65,0),arrowprops=dict(arrowstyle='<->',color=GR)); ax.text(0.52,0.18,'Absolute',color=GR,fontsize=8)
ax.plot(0.75,0.4,'o',color=PU); ax.text(0.78,0.36,'Point B (below atmospheric)',fontsize=8)
ax.set_xlim(0,1.25); ax.set_ylim(-0.25,2.1); ax.axis('off'); ax.set_title('Absolute, gauge and vacuum pressure')
save(f,'pressure_ref')

# vortex
f,axs=plt.subplots(1,2,figsize=(6.6,3)); r=np.linspace(0.05,1,200)
axs[0].plot(r,0.2/r,color=NAVY,lw=2); axs[0].set_title('Free vortex: V·r = const (irrotational)',fontsize=8); axs[0].set_ylim(0,2)
axs[1].plot(r,r,color=OR,lw=2); axs[1].set_title('Forced vortex: V = ωr (rotational)',fontsize=8)
for a in axs: a.set_xlabel('Radius r'); a.set_ylabel('Tangential velocity V'); a.set_xticks([]); a.set_yticks([])
save(f,'vortex')

# velocity profiles
f,ax=plt.subplots(figsize=(5.6,3.6)); y=np.linspace(-1,1,200)
ax.plot(1-y**2,y,color=NAVY,lw=2,label='Laminar: parabolic (V = umax/2)')
ax.plot((1-np.abs(y))**(1/7),y,color=OR,lw=2,label='Turbulent: 1/7 power law (V ≈ 0.82 umax)')
ax.axvline(0.5,color=NAVY,ls=':',lw=1); ax.axvline(0.817,color=OR,ls=':',lw=1)
ax.set_xlabel('u / umax'); ax.set_ylabel('r / R'); ax.legend(fontsize=7,loc='lower left'); ax.set_title('Velocity profiles in a pipe')
save(f,'profiles')

# moody-like
f,ax=plt.subplots(figsize=(6.4,3.8))
Re=np.logspace(2.8,3.36,50); ax.loglog(Re,64/Re,color=NAVY,lw=2,label='Laminar f = 64/Re')
Re2=np.logspace(3.6,8,200)
def colebrook(Re,e):
    f=0.02*np.ones_like(Re)
    for _ in range(50): f=(-2*np.log10(e/3.7+2.51/(Re*np.sqrt(f))))**-2
    return f
for e,c in [(0,'k'),(1e-4,GY),(1e-3,GR),(5e-3,OR),(2e-2,PU)]:
    ax.loglog(Re2,colebrook(Re2,e),color=c,lw=1.4,label=('smooth' if e==0 else f'ε/D = {e}'))
ax.axvspan(2000,4000,color='#eeeeee'); ax.text(2050,0.012,'Critical\nzone',fontsize=7)
ax.text(3e6,0.055,'Fully rough zone\n(f depends on ε/D only)',fontsize=7)
ax.set_xlabel('Reynolds number Re'); ax.set_ylabel('Darcy friction factor f'); ax.set_ylim(0.008,0.1); ax.legend(fontsize=6.5,loc='upper right',ncol=2); ax.set_title('Moody chart (schematic, from Colebrook equation)')
save(f,'moody')

# specific energy
f,ax=plt.subplots(figsize=(5.6,3.6)); q=1.0; yv=np.linspace(0.19,3,300); E=yv+q**2/(2*9.81*yv**2)
yc=(q**2/9.81)**(1/3); Ec=1.5*yc
ax.plot(E,yv,color=NAVY,lw=2); ax.plot([0,3],[0,3],color=GY,ls='--',lw=1); ax.text(2.3,2.45,'E = y',fontsize=7,color=GY)
ax.plot(Ec,yc,'o',color=OR); ax.annotate('Critical depth yc, Emin = 1.5 yc',(Ec,yc),xytext=(Ec+0.5,yc+0.45),fontsize=7.5,arrowprops=dict(arrowstyle='->'))
ax.text(1.6,1.9,'Subcritical (Fr < 1)',fontsize=8); ax.text(1.75,0.12,'Supercritical (Fr > 1)',fontsize=8)
ax.set_xlim(0,3); ax.set_ylim(0,3); ax.set_xlabel('Specific energy E'); ax.set_ylabel('Depth y'); ax.set_title('Specific energy curve (constant q)')
save(f,'specific_energy')

# turbine efficiency vs load
f,ax=plt.subplots(figsize=(5.8,3.5)); L=np.linspace(0.15,1.1,100)
def curve(L,peak,Lp,k): return peak-k*np.abs(L-Lp)**2.2*100
ax.plot(L*100,curve(L,90,0.9,0.13),color=NAVY,lw=2,label='Pelton (flattest)')
ax.plot(L*100,curve(L,92,0.85,0.2),color=GR,lw=2,label='Kaplan (double regulation)')
ax.plot(L*100,curve(L,93,0.85,0.55),color=OR,lw=2,label='Francis')
ax.plot(L*100,curve(L,92,0.95,1.3),color=PU,lw=2,label='Propeller (fixed blades)')
ax.set_ylim(40,100); ax.set_xlabel('Load (% of full load)'); ax.set_ylabel('Efficiency (%)'); ax.legend(fontsize=7); ax.set_title('Part-load efficiency of turbines (schematic)')
save(f,'turbine_eff')

# pump characteristics
f,ax=plt.subplots(figsize=(5.8,3.6)); Q=np.linspace(0,1.2,100)
H=1-0.45*Q**2; P=0.35+0.45*Q; eta=1.8*Q-0.9*Q**2
sysc=0.35+0.55*Q**2
ax.plot(Q,H,color=NAVY,lw=2,label='Head H'); ax.plot(Q,P,color=OR,lw=2,label='Power P'); ax.plot(Q,eta,color=GR,lw=2,label='Efficiency η')
ax.plot(Q,sysc,color=GY,ls='--',lw=1.4,label='System curve Hs + kQ²')
qi=np.sqrt(0.65/1.0); ax.plot(qi,1-0.45*qi**2,'ko'); ax.text(qi+0.02,1-0.45*qi**2+0.04,'Operating point',fontsize=7)
ax.plot(1.0,0.9,'o',color=GR); ax.text(0.85,0.95,'BEP',fontsize=7,color=GR)
ax.text(0.02,1.02,'Shut-off head',fontsize=7)
ax.set_xticks([]); ax.set_yticks([]); ax.set_xlabel('Discharge Q'); ax.set_ylim(0,1.15); ax.legend(fontsize=7,loc='lower right'); ax.set_title('Centrifugal pump characteristics (constant speed)')
save(f,'pump_curves')
print('ok')
