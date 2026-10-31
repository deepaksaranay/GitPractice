import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt, numpy as np, os
D=os.path.join(os.path.dirname(os.path.abspath(__file__)),'figs'); os.makedirs(D,exist_ok=True)
plt.rcParams.update({'font.size':9,'font.family':'DejaVu Sans'})
NAVY='#1b2a49'; OR='#b3470f'; GR='#2f855a'; PU='#6b46c1'; GY='#666666'; RD='#c53030'
def save(f,n): f.tight_layout(); f.savefig(f'{D}/{n}.png',dpi=170); plt.close(f)
def clean(ax):
    ax.set_xticks([]); ax.set_yticks([])
    for s in ('top','right'): ax.spines[s].set_visible(False)

# 1. Processes on p-V (expansion from a common state)
f,ax=plt.subplots(figsize=(6.2,4)); V=np.linspace(1,3,200)
ax.plot([1,3],[1,1],color=NAVY,lw=2,label='Isobaric (n = 0)')
ax.plot(V,1/V,color=GR,lw=2,label='Isothermal (n = 1)')
ax.plot(V,V**-1.2,color=PU,lw=2,label='Polytropic (1 < n < γ)')
ax.plot(V,V**-1.4,color=OR,lw=2,label='Adiabatic (n = γ)')
ax.plot([1,1],[1,0.15],color=RD,lw=2,label='Isochoric (n = ∞)')
ax.plot(1,1,'ko'); ax.text(1.03,1.03,'Initial state',fontsize=8)
ax.set_xlabel('Volume V'); ax.set_ylabel('Pressure p'); clean(ax); ax.set_xlim(0.8,3.1); ax.set_ylim(0,1.2)
ax.legend(fontsize=8); ax.set_title('Expansion processes pVⁿ = C from the same state')
save(f,'processes')

# 2. Carnot cycle p-v and T-s
f,(a1,a2)=plt.subplots(1,2,figsize=(7.2,3.4))
g=1.4; V1=1; V2=2; T1=1.0; T2=0.6
V3=V2*(T1/T2)**(1/(g-1)); V4=V1*(T1/T2)**(1/(g-1))
v=np.linspace(V1,V2,50); a1.plot(v,T1/v,color=OR,lw=2)
v=np.linspace(V2,V3,50); a1.plot(v,T1/V2*(V2/v)**g,color=NAVY,lw=2)
v=np.linspace(V3,V4,50); a1.plot(v,T2/v,color=GR,lw=2)
v=np.linspace(V4,V1,50); a1.plot(v,T2/V4*(V4/v)**g,color=PU,lw=2)
for (x,y,t) in [(V1,T1/V1,'1'),(V2,T1/V2,'2'),(V3,T2/V3,'3'),(V4,T2/V4,'4')]: a1.plot(x,y,'ko',ms=3); a1.text(x+0.05,y+0.02,t)
a1.set_xlabel('v'); a1.set_ylabel('p'); clean(a1); a1.set_title('p–v diagram')
a2.plot([1,2],[1,1],color=OR,lw=2); a2.plot([2,2],[1,0.6],color=NAVY,lw=2); a2.plot([2,1],[0.6,0.6],color=GR,lw=2); a2.plot([1,1],[0.6,1],color=PU,lw=2)
a2.fill_between([1,2],0.6,1,color=OR,alpha=0.12); a2.text(1.32,0.78,'Net work',fontsize=8)
for (x,y,t) in [(1,1,'1'),(2,1,'2'),(2,0.6,'3'),(1,0.6,'4')]: a2.text(x+0.03,y+0.02,t)
a2.text(1.3,1.04,'Q₁ = T₁Δs at T₁',fontsize=8,color=OR); a2.text(1.3,0.52,'Q₂ = T₂Δs at T₂',fontsize=8,color=GR)
a2.set_xlim(0.7,2.4); a2.set_ylim(0.4,1.2); a2.set_xlabel('s'); a2.set_ylabel('T'); clean(a2); a2.set_title('T–s diagram (rectangle)')
save(f,'carnot')

# 3. Phase (T-v) diagram of water
f,ax=plt.subplots(figsize=(6.2,4))
xl=np.linspace(0.1,0.35,60); Tl=0.2+0.8*(1-((0.35-xl)/0.25)**2)
xr=np.linspace(0.35,0.95,80); Tr=0.2+0.8*(1-((xr-0.35)/0.6)**1.6)
ax.plot(xl,Tl,color=NAVY,lw=2); ax.plot(xr,Tr,color=NAVY,lw=2)
ax.plot(0.35,1.0,'ro'); ax.text(0.37,1.02,'Critical point (374.14 °C, 22.09 MPa)',fontsize=8,color=RD)
for Tp,c in [(0.5,OR),(0.75,GR)]:
    xa=xl[np.argmin(abs(Tl-Tp))]; xb=xr[np.argmin(abs(Tr-Tp))]
    m=(Tl<=Tp)&(Tl>=0.22); ax.plot(xl[m]-0.012,Tl[m],color=c,lw=1.6); ax.plot([xa,xb],[Tp,Tp],color=c,lw=1.6); ax.plot([xb,xb+0.25],[Tp,Tp+0.22],color=c,lw=1.6)
ax.plot([0.25,0.35,0.6],[0.8,1.08,1.3],color=PU,lw=1.6,ls='--'); ax.text(0.6,1.28,'Supercritical p',fontsize=8,color=PU)
ax.text(0.05,0.6,'Compressed\n(subcooled)\nliquid',fontsize=8); ax.text(0.42,0.55,'Wet steam\n(liquid + vapour)',fontsize=8)
ax.text(0.78,0.75,'Superheated\nvapour',fontsize=8)
ax.text(0.12,0.24,'Sat. liquid line\n(x = 0)',fontsize=7,color=NAVY); ax.text(0.72,0.33,'Sat. vapour line (x = 1)',fontsize=7,color=NAVY)
ax.set_xlabel('Specific volume v'); ax.set_ylabel('Temperature T'); clean(ax); ax.set_ylim(0.15,1.4); ax.set_xlim(0,1.15)
ax.set_title('T–v diagram of water with constant-pressure lines')
save(f,'phase')

# 4. Otto and Diesel p-V
f,(a1,a2)=plt.subplots(1,2,figsize=(7.2,3.4)); r=8; Vc=1; Vt=r*Vc
v=np.linspace(Vt,Vc,60); a1.plot(v,(Vt/v)**g,color=NAVY,lw=2)
p2=r**g; p3=p2*2.2; a1.plot([Vc,Vc],[p2,p3],color=OR,lw=2)
v=np.linspace(Vc,Vt,60); a1.plot(v,p3*(Vc/v)**g,color=GR,lw=2); a1.plot([Vt,Vt],[p3*(Vc/Vt)**g,1],color=PU,lw=2)
a1.text(Vc+0.2,(p2+p3)/2,'Q₁ at\nconstant V',fontsize=8,color=OR); a1.text(Vt-1.2,4,'Q₂ at\nconst V',fontsize=8,color=PU)
a1.set_title('Otto cycle'); a1.set_xlabel('V'); a1.set_ylabel('p'); clean(a1)
r=16; Vt=r*Vc; p2=r**g; rc=2.2
v=np.linspace(Vt,Vc,60); a2.plot(v,(Vt/v)**g,color=NAVY,lw=2); a2.plot([Vc,rc*Vc],[p2,p2],color=OR,lw=2)
v=np.linspace(rc*Vc,Vt,60); a2.plot(v,p2*(rc*Vc/v)**g,color=GR,lw=2); a2.plot([Vt,Vt],[p2*(rc*Vc/Vt)**g,1],color=PU,lw=2)
a2.text(rc*Vc+0.3,p2*1.01,'Q₁ at constant p',fontsize=8,color=OR); a2.set_title('Diesel cycle'); a2.set_xlabel('V'); a2.set_ylabel('p'); clean(a2)
save(f,'otto_diesel')

# 5. Brayton T-s
f,ax=plt.subplots(figsize=(6.2,3.8))
s=np.linspace(0,1,50); ax.plot(s,1.8*np.exp(s*0.8)/np.exp(0.0),color=OR,lw=2)
ax.plot(s,1.0*np.exp(s*0.8),color=GR,lw=2)
ax.plot([0,0],[1.0,1.8],color=NAVY,lw=2); ax.plot([1,1],[np.exp(0.8),1.8*np.exp(0.8)],color=PU,lw=2)
ax.plot([0,0.12],[1.0,1.95],color=NAVY,lw=1,ls='--'); ax.plot([1,1.1],[1.8*np.exp(0.8),np.exp(0.8)*1.05],color=PU,lw=1,ls='--')
for (x,y,t) in [(0,1.0,'1'),(0,1.8,'2'),(1,1.8*np.exp(0.8),'3'),(1,np.exp(0.8),'4')]: ax.text(x-0.06,y,t,fontsize=10)
ax.text(0.35,2.6,'Heat addition at constant p (combustor)',fontsize=8,color=OR,rotation=18)
ax.text(0.35,1.1,'Heat rejection at constant p',fontsize=8,color=GR,rotation=10)
ax.text(-0.25,1.35,'Compressor\n(isentropic)',fontsize=8,color=NAVY); ax.text(1.03,3.0,'Turbine',fontsize=8,color=PU)
ax.text(0.15,1.95,"2' (actual)",fontsize=7); ax.text(1.12,2.3,"4' (actual)",fontsize=7)
ax.set_xlabel('Entropy s'); ax.set_ylabel('Temperature T'); clean(ax); ax.set_xlim(-0.35,1.4); ax.set_title('Brayton (Joule) cycle – ideal and actual')
save(f,'brayton')

# 6. Valve timing diagram (four-stroke SI)
f,ax=plt.subplots(figsize=(5,5)); ax.set_aspect('equal'); ax.axis('off')
def arc(r,a0,a1,c,lab,lp):
    t=np.radians(np.linspace(a0,a1,100)); ax.plot(r*np.sin(t),r*np.cos(t),color=c,lw=3)
    ax.text(lp[0],lp[1],lab,color=c,fontsize=8,ha='center')
# angle measured clockwise from TDC (top); BDC at 180
arc(1.0,-10,180+40,GR,'Suction (IVO 10° bTDC → IVC 40° aBDC)',(0,-1.45))
arc(0.8,180+40,360-30,NAVY,'Compression',(-1.25,0.0))
arc(0.65,-30,0,OR,'Ignition 30° bTDC',(-0.25,0.85))
arc(0.6,0,180-45,PU,'Expansion',(0.35,-0.05))
arc(0.45,180-45,360+15,RD,'Exhaust (EVO 45° bBDC → EVC 15° aTDC)',(0,1.35))
ax.plot([0,0],[-1.15,1.15],color='k',lw=0.8,ls=':'); ax.text(0,1.18,'TDC',ha='center',fontsize=9,weight='bold'); ax.text(0,-1.27,'BDC',ha='center',fontsize=9,weight='bold')
ax.text(0.95,1.05,'Valve overlap\n25° around TDC',fontsize=7,color=GY,ha='center')
ax.set_xlim(-1.7,1.6); ax.set_ylim(-1.6,1.5); ax.set_title('Typical valve timing diagram – four-stroke SI engine')
save(f,'valve_timing')

# 7. Rankine cycle on T-s
f,ax=plt.subplots(figsize=(6.2,4))
s=np.linspace(0,1,100); sl=s[s<=0.45]; sr=s[s>=0.45]
Tl=0.2+0.8*(1-((0.45-sl)/0.45)**2); Tr=0.2+0.8*(1-((sr-0.45)/0.55)**1.4)
ax.plot(sl,Tl,color=GY,lw=1.5); ax.plot(sr,Tr,color=GY,lw=1.5)
Tb=0.7; xa=sl[np.argmin(abs(Tl-Tb))]; xb=sr[np.argmin(abs(Tr-Tb))]
ax.plot([0.05,0.06],[0.3,0.33],color=NAVY,lw=2)
ax.plot([0.06,0.1,xa],[0.33,0.5,Tb],color=OR,lw=2); ax.plot([xa,xb],[Tb,Tb],color=OR,lw=2); ax.plot([xb,0.88],[Tb,0.98],color=OR,lw=2)
ax.plot([0.88,0.88],[0.98,0.3],color=PU,lw=2); ax.plot([0.88,0.05],[0.3,0.3],color=GR,lw=2)
ax.text(0.89,1.0,'1 (superheated)',fontsize=8); ax.text(0.89,0.26,'2',fontsize=9); ax.text(0.0,0.26,'3',fontsize=9); ax.text(0.0,0.35,'4',fontsize=9)
ax.text(0.3,Tb+0.03,'Boiler (constant p)',fontsize=8,color=OR); ax.text(0.9,0.6,'Turbine\n(isentropic)',fontsize=8,color=PU)
ax.text(0.35,0.24,'Condenser (constant p, constant T)',fontsize=8,color=GR); ax.text(0.07,0.42,'Pump',fontsize=8,color=NAVY)
ax.set_xlabel('Entropy s'); ax.set_ylabel('Temperature T'); clean(ax); ax.set_ylim(0.15,1.1); ax.set_xlim(-0.05,1.35)
ax.set_title('Rankine cycle with superheat (T–s)')
save(f,'rankine')

# 8. Reciprocating compressor p-V with clearance
f,ax=plt.subplots(figsize=(6.2,3.8)); n=1.3; Vc=0.1; Vt=1.1; p1=1; p2=6
V2=Vt*(p1/p2)**(1/n); V4=Vc*(p2/p1)**(1/n)
v=np.linspace(Vt,V2,60); ax.plot(v,p1*(Vt/v)**n,color=NAVY,lw=2)
ax.plot([V2,Vc],[p2,p2],color=OR,lw=2); v=np.linspace(Vc,V4,60); ax.plot(v,p2*(Vc/v)**n,color=PU,lw=2); ax.plot([V4,Vt],[p1,p1],color=GR,lw=2)
for (x,y,t) in [(Vt,p1,'1'),(V2,p2,'2'),(Vc,p2,'3'),(V4,p1,'4')]: ax.text(x+0.02,y+0.12,t)
ax.annotate('',xy=(0,0.4),xytext=(Vc,0.4),arrowprops=dict(arrowstyle='<->')); ax.text(0.0,0.2,'V_c',fontsize=8)
ax.annotate('',xy=(Vc,0.4),xytext=(Vt,0.4),arrowprops=dict(arrowstyle='<->')); ax.text(0.55,0.2,'Swept volume V_s',fontsize=8)
ax.annotate('',xy=(V4,1.5),xytext=(Vt,1.5),arrowprops=dict(arrowstyle='<->',color=GR)); ax.text(0.6,1.65,'Effective suction volume (V₁ − V₄)',fontsize=8,color=GR)
ax.text(0.45,p2+0.15,'Delivery',fontsize=8,color=OR); ax.text(0.2,3,'Re-expansion\nof clearance air',fontsize=8,color=PU); ax.text(0.75,2.2,'Compression\npVⁿ = C',fontsize=8,color=NAVY)
ax.set_xlabel('Volume V'); ax.set_ylabel('Pressure p'); clean(ax); ax.set_ylim(0,7); ax.set_xlim(-0.05,1.25)
ax.set_title('Indicator diagram – single-stage compressor with clearance')
save(f,'compressor')

# 9. VCR on p-h
f,ax=plt.subplots(figsize=(6.2,4))
h=np.linspace(0,1,100); hl=h[h<=0.4]; hr=h[h>=0.4]
pl=0.1+0.9*(1-((0.4-hl)/0.4)**2); pr=0.1+0.9*(1-((hr-0.4)/0.6)**1.3)
ax.plot(hl,pl,color=GY,lw=1.5); ax.plot(hr,pr,color=GY,lw=1.5)
pe=0.3; pc=0.75; h3=hl[np.argmin(abs(pl-pc))]; h1=hr[np.argmin(abs(pr-pe))]
ax.plot([h3,h3],[pc,pe],color=PU,lw=2); ax.plot([h3,h1],[pe,pe],color=GR,lw=2)
ax.plot([h1,h1+0.18],[pe,pc],color=NAVY,lw=2); ax.plot([h1+0.18,h3],[pc,pc],color=OR,lw=2)
ax.text(h1+0.19,pc+0.02,'2',fontsize=10); ax.text(h1+0.01,pe-0.06,'1',fontsize=10); ax.text(h3-0.04,pc+0.02,'3',fontsize=10); ax.text(h3-0.04,pe-0.06,'4',fontsize=10)
ax.text(0.35,pc+0.03,'Condenser',color=OR,fontsize=8); ax.text(0.35,pe-0.07,'Evaporator (refrigerating effect h₁ − h₄)',color=GR,fontsize=8)
ax.text(h3-0.15,0.5,'Expansion\nvalve\n(h const)',color=PU,fontsize=8); ax.text(h1+0.12,0.45,'Compressor\n(s const)',color=NAVY,fontsize=8)
ax.set_xlabel('Enthalpy h'); ax.set_ylabel('Pressure p (log scale)'); clean(ax); ax.set_xlim(-0.05,1.0); ax.set_ylim(0.05,1.05)
ax.set_title('Simple vapour compression cycle on p–h chart')
save(f,'vcr')

# 10. Psychrometric chart (schematic, real saturation curve)
f,ax=plt.subplots(figsize=(6.4,4.2)); t=np.linspace(0,45,200)
ps=0.61094*np.exp(17.625*t/(t+243.04)); P=101.325
for phi in [0.2,0.4,0.6,0.8,1.0]:
    w=0.622*phi*ps/(P-phi*ps)*1000; ax.plot(t,w,color=NAVY if phi==1 else GY,lw=2 if phi==1 else 0.8)
    import numpy as _n; i=int(_n.argmin(abs(w-24))) if w.max()>24 else int(_n.argmin(abs(t-40))); ax.text(t[i]+0.4,w[i]-1.6,f'{int(phi*100)}%',fontsize=7,color=NAVY if phi==1 else GY)
x0,y0=27,12
arr=lambda dx,dy,c,lab,off: (ax.annotate('',xy=(x0+dx,y0+dy),xytext=(x0,y0),arrowprops=dict(arrowstyle='->',color=c,lw=1.8)),ax.text(x0+dx+off[0],y0+dy+off[1],lab,color=c,fontsize=7))
arr(10,0,OR,'Sensible heating',(-3,0.6)); arr(-10,0,NAVY,'Sensible cooling',(-6,0.6)); arr(0,6,GR,'Humidification',(-4,0.6))
arr(-9,-4.5,PU,'Cooling & dehumidification',(-12,-1.4)); arr(-7,3,RD,'Evaporative cooling (WBT const)',(-18,0.8)); arr(7,-3,GY,'Chemical dehumidification',(-9,-2.6))
ax.plot(x0,y0,'ko'); ax.set_xlabel('Dry bulb temperature (°C)'); ax.set_ylabel('Specific humidity ω (g/kg dry air)')
ax.set_xlim(0,45); ax.set_ylim(0,30); ax.set_title('Psychrometric chart (schematic) – basic processes'); ax.spines['top'].set_visible(False); ax.spines['left'].set_visible(False)
ax.yaxis.tick_right(); ax.yaxis.set_label_position('right')
save(f,'psychro')

# 11. Pool boiling curve
f,ax=plt.subplots(figsize=(6.2,3.8))
x=np.array([1,5,10,20,30,60,120,300,1000]); y=np.array([1e3,7e3,1e5,6e5,1e6,1e5,2e4,5e4,4e5])
xs=np.logspace(0,3,300); ys=10**np.interp(np.log10(xs),np.log10(x),np.log10(y))
ax.loglog(xs,ys,color=NAVY,lw=2)
ax.plot(30,1e6,'o',color=RD); ax.text(34,1.1e6,'Critical heat flux (burnout)',fontsize=8,color=RD)
ax.plot(120,2e4,'o',color=PU); ax.text(130,1.3e4,'Leidenfrost point (min. flux)',fontsize=8,color=PU)
for xx,lab in [(5,'Free\nconv.'),(30,'Nucleate'),(120,'Transition'),(1000,'Film')]: ax.axvline(xx,color=GY,lw=0.6,ls=':')
ax.text(1.5,3e5,'Free\nconvection',fontsize=8); ax.text(7,2e3,'Nucleate\nboiling',fontsize=8); ax.text(40,3e3,'Transition',fontsize=8); ax.text(250,1.5e3,'Film\nboiling',fontsize=8)
ax.annotate('',xy=(1000,1e6),xytext=(30,1e6),arrowprops=dict(arrowstyle='->',color=RD,ls='--')); ax.text(150,1.6e6,'jump in heat-flux control',fontsize=7,color=RD)
ax.set_xlabel('Excess temperature ΔT_e = T_s − T_sat (°C)'); ax.set_ylabel('Heat flux q (W/m²)'); ax.set_ylim(5e2,5e6)
ax.set_title('Pool boiling curve for water at 1 atm (Nukiyama)')
save(f,'boiling')

# 12. Planck distribution
f,ax=plt.subplots(figsize=(6.2,3.8)); lam=np.linspace(0.2,10,600)*1e-6
C1=3.742e-16; C2=1.4388e-2
for T,c in [(5800,OR),(3000,RD),(2000,PU),(1000,NAVY)]:
    E=C1/(lam**5*(np.exp(C2/(lam*T))-1)); ax.semilogy(lam*1e6,E*1e-6,color=c,lw=1.8,label=f'{T} K')
Ts=np.array([1000,2000,3000,5800]); lm=2898/Ts; Em=C1/((lm*1e-6)**5*(np.exp(C2/(lm*1e-6*Ts))-1))*1e-6
ax.semilogy(lm,Em,'k--',lw=1,label='Wien: λ_max T = 2898 μm·K')
ax.axvspan(0.4,0.7,color='y',alpha=0.2); ax.text(0.42,1e-1,'Visible',fontsize=8)
ax.set_xlim(0,10); ax.set_ylim(1e-2,1e8); ax.set_xlabel('Wavelength λ (μm)'); ax.set_ylabel('E_bλ (W/m²·μm)'); ax.legend(fontsize=7)
ax.set_title('Black-body spectral emissive power (Planck)')
save(f,'planck')

# 13. Heat exchanger temperature profiles
f,(a1,a2)=plt.subplots(1,2,figsize=(7.2,3.2)); x=np.linspace(0,1,50)
a1.plot(x,150-50*(1-np.exp(-2*x))/(1-np.exp(-2)),color=RD,lw=2,label='Hot')
a1.plot(x,30+(80-30)*(1-np.exp(-2*x))/(1-np.exp(-2)),color=NAVY,lw=2,label='Cold')
a1.set_title('Parallel flow'); a1.legend(fontsize=7); a1.set_xlabel('Length'); a1.set_ylabel('Temperature (°C)')
a1.annotate('ΔT₁ = 120',(0.02,90),fontsize=8); a1.annotate('ΔT₂ = 20',(0.7,88),fontsize=8)
a2.plot(x,150-50*x,color=RD,lw=2,label='Hot →'); a2.plot(x,80-50*x,color=NAVY,lw=2,label='← Cold')
a2.set_title('Counter flow'); a2.legend(fontsize=7); a2.set_xlabel('Length'); a2.annotate('ΔT = 70 throughout\n(equal capacity rates)',(0.25,108),fontsize=8)
for a in (a1,a2): a.set_ylim(20,160); a.spines['top'].set_visible(False); a.spines['right'].set_visible(False)
save(f,'hx')
print('figs done')
