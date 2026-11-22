# -*- coding: utf-8 -*-
"""Tính toán BTL Chi tiết máy - Đề 5, Phương án 4
Hệ thống dẫn động xích tải: Động cơ - Đai thang - HGT trục vít - Nối trục - Xích tải
"""
import math
R = {}  # kết quả

# ===================== SỐ LIỆU =====================
F, v, z, p, Lnam = 7500.0, 1.05, 9, 110.0, 5
t1, t2 = 15.0, 48.0
k1, k2 = 1.0, 0.5           # T1 = T, T2 = 0.5T
ngay, ca, gio = 300, 2, 8
Lh = Lnam * ngay * ca * gio  # giờ
R.update(F=F, v=v, z=z, p=p, Lnam=Lnam, t1=t1, t2=t2, k2=k2, Lh=Lh)

# ===================== CHƯƠNG 1 =====================
Pmax = F * v / 1000
kdt = math.sqrt((k1**2 * t1 + k2**2 * t2) / (t1 + t2))
Pdt = Pmax * kdt
eta_d, eta_tv, eta_ol, eta_k = 0.95, 0.85, 0.99, 1.0
eta = eta_d * eta_tv * eta_ol**2 * eta_k
Pct = Pdt / eta
nlv = 60000 * v / (z * p)
R.update(Pmax=Pmax, kdt=kdt, Pdt=Pdt, eta_d=eta_d, eta_tv=eta_tv, eta_ol=eta_ol,
         eta_k=eta_k, eta=eta, Pct=Pct, nlv=nlv)
# Động cơ 4A132S4Y3
Pdc, ndc, TkTdn = 7.5, 1455, 2.0
ut = ndc / nlv
ud = 2.0
utv_sb = ut / ud
z1 = 4
z2 = round(utv_sb * z1)
utv = z2 / z1
R.update(Pdc=Pdc, ndc=ndc, TkTdn=TkTdn, ut=ut, ud=ud, utv_sb=utv_sb, z1=z1, z2=z2, utv=utv)
# Công suất các trục (theo tải lớn nhất)
P_lv = Pmax
P2 = P_lv / (eta_k * eta_ol)
P1 = P2 / (eta_tv * eta_ol)
P0 = P1 / eta_d
n0 = ndc
n1 = n0 / ud
n2 = n1 / utv
n_lv = n2
T = lambda P, n: 9.55e6 * P / n
R.update(P_lv=P_lv, P2=P2, P1=P1, P0=P0, n0=n0, n1=n1, n2=n2,
         T0=T(P0, n0), T1=T(P1, n1), T2=T(P2, n2), Tlv=T(P_lv, n2))
R['qua_tai'] = P0 / Pdc

# ===================== CHƯƠNG 2: ĐAI THANG =====================
# Đai loại B
bp, b0, h, y0, A = 14, 17, 10.5, 4, 138
dmin = 140
d1_sb = 1.2 * dmin
d1 = 160.0
v1 = math.pi * d1 * n0 / 60000
xi = 0.02
d2_tt = ud * d1 * (1 - xi)
d2 = 315.0
ud_tt = d2 / (d1 * (1 - xi))
a_sb = 1.2 * d2
amin, amax = 0.55 * (d1 + d2) + h, 2 * (d1 + d2)
L_tt = 2 * a_sb + math.pi * (d1 + d2) / 2 + (d2 - d1) ** 2 / (4 * a_sb)
L = 1600.0
i_s = v1 / (L / 1000)
k = L - math.pi * (d1 + d2) / 2
Dl = (d2 - d1) / 2
a = (k + math.sqrt(k**2 - 8 * Dl**2)) / 4
alpha1 = 180 - 57 * (d2 - d1) / a
Ca = 1.24 * (1 - math.exp(-alpha1 / 110))
P0_cp, L0 = 4.0, 2240.0
Cu = 1.13
CL = (L / L0) ** (1 / 6)
Cz = 0.95
Cr = 0.9
Cv = 1 - 0.05 * (0.01 * v1**2 - 1)
C = Ca * Cu * CL * Cz * Cr * Cv
z_tt = P0 / (P0_cp * C)
zd = math.ceil(z_tt)
e_r, f_r, b_r = 19, 12.5, 4.2
B = (zd - 1) * e_r + 2 * f_r
da1_d = d1 + 2 * b_r
da2_d = d2 + 2 * b_r
sigma0 = 1.5
F0 = sigma0 * zd * A
Fr_d = 3 * F0 * math.sin(math.radians(alpha1 / 2))
Ft_d = 1000 * P0 / v1
R.update(d1=d1, d1_sb=d1_sb, v1=v1, d2_tt=d2_tt, d2=d2, ud_tt=ud_tt, a_sb=a_sb, amin=amin,
         amax=amax, L_tt=L_tt, L=L, i_s=i_s, kL=k, Dl=Dl, a=a, alpha1=alpha1, Ca=Ca, P0_cp=P0_cp,
         L0=L0, Cu=Cu, CL=CL, Cz=Cz, Cr=Cr, Cv=Cv, C=C, z_tt=z_tt, zd=zd, B=B, da1_d=da1_d,
         da2_d=da2_d, F0=F0, Fr_d=Fr_d, Ft_d=Ft_d, A=A, h=h)
# kiểm tra lại tỉ số truyền & sai số vòng quay
n1_tt = n0 / ud_tt
n2_tt = n1_tt / utv
sai_so = (n2_tt - nlv) / nlv * 100
R.update(n1_tt=n1_tt, n2_tt=n2_tt, sai_so=sai_so)

# ===================== CHƯƠNG 3: TRỤC VÍT =====================
T1 = R['T1']; T2 = R['T2']
vs_sb = 4.5e-5 * n1 * T2 ** (1 / 3)
# BrAZh9-4 đúc khuôn kim loại: sigma_b=500, sigma_ch=200; trục vít 40Cr tôi HRC 45-50
sb_bv, sch_bv = 500.0, 200.0
sH_sb = 300 - 25 * vs_sb
# ứng suất uốn cho phép
sum_t = t1 + t2
NFE = 60 * n2 * Lh * ((k1**9) * t1 / sum_t + (k2**9) * t2 / sum_t)
KFL = (1e6 / NFE) ** (1 / 9)
sF0 = 0.25 * sch_bv + 0.08 * sb_bv
sF = sF0 * KFL
# hệ số tải
q = 10.0
theta = 70
Tm_Tmax = (k1 * t1 + k2 * t2) / sum_t
Kb = 1 + (z2 / theta) ** 3 * (1 - Tm_Tmax)
Kv = 1.1
KH = Kb * Kv
aw_tt = (1 + q / z2) * ((170 / sH_sb) ** 2 * T2 * KH / (q / z2)) ** (1 / 3)
m_tt = 2 * aw_tt / (q + z2)
m = 8.0
aw = m * (q + z2) / 2
x = 0.0
R.update(vs_sb=vs_sb, sH_sb=sH_sb, NFE=NFE, KFL=KFL, sF0=sF0, sF=sF, q=q, theta=theta,
         Tm_Tmax=Tm_Tmax, Kb=Kb, Kv=Kv, KH=KH, aw_tt=aw_tt, m_tt=m_tt, m=m, aw=aw, x=x)
# kích thước
dw1 = m * q
da1 = dw1 + 2 * m
df1 = dw1 - 2.4 * m
dw2 = m * z2
da2 = dw2 + 2 * m
df2 = dw2 - 2.4 * m
daM2 = da2 + 6 * m / (z1 + 2)
b2max = 0.67 * da1
b2 = 64.0
b1_tt = (12.5 + 0.09 * z2) * m
b1 = 140.0
gamma = math.degrees(math.atan(z1 / q))
delta = math.degrees(math.asin(b2 / (da1 - 0.5 * m)))
R.update(dw1=dw1, da1=da1, df1=df1, dw2=dw2, da2=da2, df2=df2, daM2=daM2, b2max=b2max,
         b2=b2, b1_tt=b1_tt, b1=b1, gamma=gamma, delta2=2 * delta)
# vận tốc trượt thực, hiệu suất
vs = math.pi * dw1 * n1 / (60000 * math.cos(math.radians(gamma)))
rho = 2.0  # độ, góc ma sát thay thế (đồng thanh không thiếc, vs ~ 3.3 m/s)
eta_tv_tt = 0.95 * math.tan(math.radians(gamma)) / math.tan(math.radians(gamma + rho))
sH_cp = 300 - 25 * vs
v2 = math.pi * dw2 * n2 / 60000
sH = 480 / dw2 * math.sqrt(KH * T2 / dw1)
zv = z2 / math.cos(math.radians(gamma)) ** 3
YF = 1.40 + (1.45 - 1.40) * (60 - zv) / 10 if zv <= 60 else 1.40
KF = KH
sF_tt = 1.5 * YF * KF * T2 / (z2 * q * m**3)
R.update(vs=vs, rho=rho, eta_tv_tt=eta_tv_tt, sH_cp=sH_cp, v2=v2, sH=sH, zv=zv, YF=YF,
         KF=KF, sF_tt=sF_tt)
# lực
Ft1 = 2 * T1 / dw1
Fa2 = Ft1
Ft2 = 2 * T2 / dw2
Fa1 = Ft2
Fr1 = Ft2 * math.tan(math.radians(20))
Fr2 = Fr1
R.update(Ft1=Ft1, Fa1=Fa1, Ft2=Ft2, Fa2=Fa2, Fr1=Fr1, Fr2=Fr2)
# độ cứng trục vít
l_tv = 360.0
E = 2.1e5
Je = math.pi * df1**4 / 64 * (0.375 + 0.625 * da1 / df1)
f_tv = l_tv**3 * math.sqrt(Ft1**2 + Fr1**2) / (48 * E * Je)
f_cp = (0.005 * m, 0.01 * m)
R.update(l_tv=l_tv, Je=Je, f_tv=f_tv, f_cp=f_cp)
# nhiệt
At = 20 * (aw / 1000) ** 1.7
KT, psi, t0 = 13.0, 0.25, 25.0
eta_use = eta_tv_tt
tdau = t0 + 1000 * P1 * (1 - eta_use) / (KT * At * (1 + psi))
R.update(At=At, KT=KT, psi=psi, t0=t0, tdau=tdau)

# ===================== CHƯƠNG 4: TRỤC =====================
def beam(L_pos, forces, couples, supports):
    """forces: list (x, F) (+ dương theo chiều dương trục y hoặc z)
    couples: list (x, C) (+ ngược chiều kim đồng hồ)
    supports: (xA, xB) -> trả về RA, RB"""
    xA, xB = supports
    # Sum M_A = 0: sum F_i (x_i - xA) + sum C + RB (xB - xA) = 0
    MF = sum(Fi * (xi - xA) for xi, Fi in forces) + sum(Ci for _, Ci in couples)
    RB = -MF / (xB - xA)
    RA = -sum(Fi for _, Fi in forces) - RB
    return RA, RB

def moment_at(xs, forces, couples):
    """M(x) = sum_{xi<x} F_i (x - xi) - sum_{xj<x} C_j  (lấy bên trái)"""
    out = []
    for X in xs:
        M = sum(Fi * (X - xi) for xi, Fi in forces if xi < X - 1e-9)
        M -= sum(Cj for xj, Cj in couples if xj < X - 1e-9)
        out.append(M)
    return out

# ---- Trục I ----
l11 = 75.0          # puli -> ổ A
l12 = 180.0         # ổ A -> trục vít
l13 = 180.0         # trục vít -> ổ B
xP, xA, xW, xB = 0.0, l11, l11 + l12, l11 + l12 + l13
Ma1 = Fa1 * dw1 / 2
# Mặt phẳng đứng (y): Fr1 hướng lên (+), Ma1 (+)
fy1 = [(xW, +Fr1)]
cy1 = [(xW, +Ma1)]
RAy, RBy = beam(None, fy1, cy1, (xA, xB))
# Mặt phẳng ngang (z): Fr_d (+), Ft1 (+)
fz1 = [(xP, +Fr_d), (xW, +Ft1)]
RAx, RBx = beam(None, fz1, [], (xA, xB))
R.update(l11=l11, l12=l12, l13=l13, Ma1=Ma1, RAy=RAy, RBy=RBy, RAx=RAx, RBx=RBx)
FY1 = fy1 + [(xA, RAy), (xB, RBy)]
FX1 = fz1 + [(xA, RAx), (xB, RBx)]
secs1 = {'1-0': xP, '1-1': xA, '1-2': xW, '1-3': xB}
def Mx_left_right(X, F_, C_):
    l = moment_at([X], F_, C_)[0]
    r = moment_at([X + 1e-6], F_, C_)[0]
    return l, r
sec1 = {}
for s_, X in secs1.items():
    myl, myr = Mx_left_right(X, FY1, cy1)
    mzl, mzr = Mx_left_right(X, FX1, [])
    sec1[s_] = dict(x=X, Mx=max(abs(myl), abs(myr)), My=max(abs(mzl), abs(mzr)),
                    Mx_l=myl, Mx_r=myr, My_l=mzl, My_r=mzr,
                    T=T1 if X <= xW + 1e-6 else 0.0)
# mômen xoắn trên trục I: từ puli đến trục vít
for s_ in sec1:
    sec1[s_]['T'] = T1 if sec1[s_]['x'] <= xW else 0.0
R['sec1'] = sec1

# ---- Trục II ----
l21 = 85.0   # ổ C -> bánh vít
l22 = 85.0   # bánh vít -> ổ D
l23 = 110.0  # ổ D -> nối trục
xC, xG, xD, xK = 0.0, l21, l21 + l22, l21 + l22 + l23
Ma2 = Fa2 * dw2 / 2
# chọn nối trục (xem chương 5): D0 = 200 mm
D0_nt = 200.0
Ftk = 2 * T2 / D0_nt
Fk = 0.25 * Ftk
# Mặt phẳng đứng: Fr2 hướng xuống (-), Ma2 (+)
fy2 = [(xG, -Fr2)]
cy2 = [(xG, +Ma2)]
RCy, RDy = beam(None, fy2, cy2, (xC, xD))
# Mặt phẳng ngang: Ft2 (-), Fk (+) ngược chiều Ft2
fz2 = [(xG, -Ft2), (xK, +Fk)]
RCx, RDx = beam(None, fz2, [], (xC, xD))
R.update(l21=l21, l22=l22, l23=l23, Ma2=Ma2, D0_nt=D0_nt, Ftk=Ftk, Fk=Fk,
         RCy=RCy, RDy=RDy, RCx=RCx, RDx=RDx)
FY2 = fy2 + [(xC, RCy), (xD, RDy)]
FX2 = fz2 + [(xC, RCx), (xD, RDx)]
secs2 = {'2-0': xC, '2-1': xG, '2-2': xD, '2-3': xK}
sec2 = {}
for s_, X in secs2.items():
    myl, myr = Mx_left_right(X, FY2, cy2)
    mzl, mzr = Mx_left_right(X, FX2, [])
    sec2[s_] = dict(x=X, Mx=max(abs(myl), abs(myr)), My=max(abs(mzl), abs(mzr)),
                    Mx_l=myl, Mx_r=myr, My_l=mzl, My_r=mzr, T=T2 if X >= xG else 0.0)
R['sec2'] = sec2
R['beam1'] = dict(FY=FY1, CY=cy1, FX=FX1, xs=[xP, xA, xW, xB])
R['beam2'] = dict(FY=FY2, CY=cy2, FX=FX2, xs=[xC, xG, xD, xK])

# đường kính
s_tv = 55.0   # [sigma] trục I (40Cr)
s_tr2 = 50.0  # [sigma] trục II (thép 45)
for secs, sig in ((sec1, s_tv), (sec2, s_tr2)):
    for s_, d_ in secs.items():
        Mtd = math.sqrt(d_['Mx']**2 + d_['My']**2 + 0.75 * d_['T']**2)
        d_['Mtd'] = Mtd
        d_['dmin'] = (Mtd / (0.1 * sig)) ** (1 / 3)
R.update(s_tv=s_tv, s_tr2=s_tr2)

# ---- Chọn đường kính các đoạn trục ----
D1 = {'1-0': 40.0, '1-1': 50.0, '1-2': df1, '1-3': 50.0}
D2 = {'2-0': 65.0, '2-1': 70.0, '2-2': 65.0, '2-3': 63.0}
for s_, d_ in D1.items(): sec1[s_]['d'] = d_
for s_, d_ in D2.items(): sec2[s_]['d'] = d_

# ---- Then bằng (TCVN 2261-77) ----
sd_cp, tc_cp = 100.0, 60.0
keys = [
    # tên, trục, d, b, h, t1, t2, L, T, kiểu đầu
    dict(ten='Bánh đai (trục I)', d=40.0, b=12, h=8, t1=5.0, t2=3.3, L=56, T=T1),
    dict(ten='Bánh vít (trục II)', d=70.0, b=20, h=12, t1=7.5, t2=4.9, L=100, T=T2),
    dict(ten='Nối trục (trục II)', d=63.0, b=18, h=11, t1=7.0, t2=4.4, L=125, T=T2),
]
for kk in keys:
    kk['l1'] = kk['L'] - kk['b']
    kk['sd'] = 2 * kk['T'] / (kk['d'] * kk['l1'] * (kk['h'] - kk['t1']))
    kk['tc'] = 2 * kk['T'] / (kk['d'] * kk['l1'] * kk['b'])
R.update(keys=keys, sd_cp=sd_cp, tc_cp=tc_cp)

# ---- Kiểm nghiệm mỏi ----
def eps_table(d, alloy=False):
    if alloy:
        tb = [(20, .83, .89), (30, .77, .81), (40, .73, .75), (50, .70, .73), (70, .65, .70), (100, .59, .59)]
    else:
        tb = [(20, .92, .89), (30, .88, .81), (40, .85, .78), (50, .81, .76), (70, .76, .73), (100, .70, .70)]
    for (da, sa, ta), (db, sb_, tb_) in zip(tb[:-1], tb[1:]):
        if da <= d <= db:
            r = (d - da) / (db - da)
            return sa + r * (sb_ - sa), ta + r * (tb_ - ta)
    return tb[-1][1], tb[-1][2]

def fatigue(sec, sb, alloy, info):
    s_1, t_1 = 0.436 * sb, 0.22 * sb
    psi_s, psi_t, beta = 0.05, 0.0, 0.8
    rows = []
    for s_, dct in sec.items():
        typ = info.get(s_)
        if typ is None:
            rows.append(dict(sec=s_, skip=True, **dct)); continue
        d = dct['d']
        M = math.hypot(dct['Mx'], dct['My'])
        Tq = dct['T']
        es, et = eps_table(d, alloy)
        if typ == 'then':
            b, t1k = info[s_ + 'bt']
            Wx = math.pi * d**3 / 32 - b * t1k * (d - t1k)**2 / (2 * d)
            Wo = math.pi * d**3 / 16 - b * t1k * (d - t1k)**2 / (2 * d)
            Ks, Kt = 1.75, 1.5
        elif typ == 'ol':
            Wx = math.pi * d**3 / 32; Wo = math.pi * d**3 / 16
            Ks, Kt = 2.0 * es, 1.5 * et  # Kσ/εσ = 2.0 ; Kτ/ετ = 1.5 (lắp có độ dôi)
        else:  # chân ren trục vít
            Wx = math.pi * d**3 / 32; Wo = math.pi * d**3 / 16
            Ks, Kt = 1.75, 1.5
        sa = M / Wx
        tmax = Tq / Wo
        ta = tm = tmax / 2
        ss = s_1 / (Ks * sa / (es * beta) + psi_s * 0) if sa > 0 else float('inf')
        st = t_1 / (Kt * ta / (et * beta) + psi_t * tm) if ta > 0 else float('inf')
        if math.isinf(ss): s = st
        elif math.isinf(st): s = ss
        else: s = ss * st / math.sqrt(ss**2 + st**2)
        rows.append(dict(sec=s_, skip=False, d=d, M=M, T=Tq, Wx=Wx, Wo=Wo, Ks=Ks, Kt=Kt, es=es, et=et,
                         sa=sa, tmax=tmax, ta=ta, ss=ss, st=st, s=s, typ=typ))
    return dict(s_1=s_1, t_1=t_1, psi_s=psi_s, psi_t=psi_t, beta=beta, rows=rows)

sb1, sb2 = 850.0, 600.0
fat1 = fatigue(sec1, sb1, True, {'1-0': 'then', '1-0bt': (12, 5.0), '1-1': 'ol', '1-2': 'ren'})
fat2 = fatigue(sec2, sb2, False, {'2-1': 'then', '2-1bt': (20, 7.5), '2-2': 'ol', '2-3': 'then', '2-3bt': (18, 7.0)})
R.update(sb1=sb1, sb2=sb2, fat1=fat1, fat2=fat2)

# ===================== CHƯƠNG 5: Ổ LĂN, NỐI TRỤC =====================
Ksig, Kt_, V = 1.1, 1.0, 1.0
fac_life = ((1.0) * t1 / sum_t + (k2 ** (10 / 3)) * t2 / sum_t) ** (3 / 10)
def bearing_pair(FrX, FrY, Fa, n, brg):
    """FrX: (R1x,R1y) ổ chịu dọc trục cùng chiều Fa là ổ 2"""
    pass
# Trục I: Fa1 hướng về ổ B
FrA = math.hypot(RAx, RAy); FrB = math.hypot(RBx, RBy)
brg1 = dict(ky_hieu='7310', d=50, D=110, T=29.25, C=96.6, C0=75.9, alpha=12.95)
brg2 = dict(ky_hieu='7213', d=65, D=120, T=24.75, C=91.3, C0=75.0, alpha=13.83)
def tapered(FrL, FrR, Fa_toward_R, n, brg, names):
    al = math.radians(brg['alpha'])
    e = 1.5 * math.tan(al)
    Y = 0.4 / math.tan(al)
    Y0 = 0.22 / math.tan(al)
    SL, SR = 0.83 * e * FrL, 0.83 * e * FrR
    FaR = SL + Fa_toward_R
    FaR_used = max(FaR, SR)
    FaL = SR - Fa_toward_R
    FaL_used = max(FaL, SL)
    out = dict(e=e, Y=Y, Y0=Y0, SL=SL, SR=SR, FaR=FaR, FaR_used=FaR_used, FaL=FaL, FaL_used=FaL_used,
               FrL=FrL, FrR=FrR, names=names)
    for side, Fr_, Fa_ in (('L', FrL, FaL_used), ('R', FrR, FaR_used)):
        ratio = Fa_ / (V * Fr_)
        if ratio <= e: X, Yy = 1.0, 0.0
        else: X, Yy = 0.4, Y
        Q = (X * V * Fr_ + Yy * Fa_) * Ksig * Kt_
        out[side] = dict(ratio=ratio, X=X, Y=Yy, Q=Q, Fr=Fr_, Fa=Fa_)
    Qmax = max(out['L']['Q'], out['R']['Q'])
    side = 'L' if out['L']['Q'] >= out['R']['Q'] else 'R'
    QE = Qmax * fac_life
    Lm = 60 * n * Lh / 1e6
    Ctt = QE * Lm ** (3 / 10) / 1000
    Fr_s, Fa_s = out[side]['Fr'], out[side]['Fa']
    Q0a = 0.5 * Fr_s + Y0 * Fa_s
    Q0 = max(Q0a, Fr_s)
    out.update(Qmax=Qmax, side=side, QE=QE, Lm=Lm, Ctt=Ctt, Q0a=Q0a, Q0=Q0, brg=brg)
    return out
b1 = tapered(FrA, FrB, Fa1, n1, brg1, ('A', 'B'))
b2 = tapered(FrB if False else math.hypot(RDx, RDy), math.hypot(RCx, RCy), Fa2, n2, brg2, ('D', 'C'))
R.update(Ksig=Ksig, Kt_=Kt_, fac_life=fac_life, FrA=FrA, FrB=FrB,
         FrC=math.hypot(RCx, RCy), FrD=math.hypot(RDx, RDy), b1=b1, b2=b2)
# nối trục vòng đàn hồi
k_nt = 1.5
Tt_nt = k_nt * T2
nt = dict(T=2000, d=63, D=260, dm=120, L=286, l=140, d1=110, D0=200, Z=8, nmax=2300,
          dc=24, ren='M16', D2=32, lc=95, l1=52, l2=24, l3=44, h=2)
sd_nt = 2 * k_nt * T2 / (nt['Z'] * nt['D0'] * nt['dc'] * nt['l3'])
l0 = nt['l1'] + nt['l2'] / 2
su_nt = k_nt * T2 * l0 / (0.1 * nt['dc']**3 * nt['D0'] * nt['Z'])
R.update(k_nt=k_nt, Tt_nt=Tt_nt, nt=nt, sd_nt=sd_nt, l0=l0, su_nt=su_nt)

if __name__ == '__main__':
    import json
    def fmt(o):
        if isinstance(o, float): return round(o, 3)
        if isinstance(o, dict): return {k_: fmt(v_) for k_, v_ in o.items()}
        if isinstance(o, (list, tuple)): return [fmt(i) for i in o]
        return o
    print(json.dumps(fmt(R), indent=1, ensure_ascii=False))
