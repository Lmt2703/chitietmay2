# -*- coding: utf-8 -*-
"""Sinh toàn bộ hình vẽ kỹ thuật và biểu đồ mômen (300 DPI) cho BTL Đề 5 - Phương án 4"""
import os, sys, shutil
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches

sys.path.insert(0, os.path.dirname(__file__))
import calc
R = calc.R

OUT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'figures'))
os.makedirs(OUT, exist_ok=True)

# Copy sơ đồ đầu đề gốc Đề 5
src_sodo = r'C:\Users\hoang\.gemini\antigravity\brain\e97e6356-1596-48a5-96a3-fa46c082f691\scratch\Dau_de_bai_img6.png'
if os.path.exists(src_sodo):
    shutil.copyfile(src_sodo, os.path.join(OUT, 'SoDo_De5.png'))

plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False

def momen_arr(x, forces, couples):
    M = np.zeros_like(x, dtype=float)
    for xi, Fi in forces:
        M += Fi * (x - xi) * (x > xi)
    for xj, Cj in couples:
        M -= Cj * (x > xj)
    M[np.abs(M) < 1e-6] = 0.0
    return M

def luoi(x0, x1, xkey):
    x = np.linspace(x0, x1, 2001)
    x = np.sort(np.concatenate([x, xkey, np.array(xkey) + 1e-6]))
    return x[x <= x1]

def plot_moment_3(xkey, labels, FY, CY, FX, Tval, Tmask, title_prefix, xlabel_txt, fname):
    x = luoi(xkey[0], xkey[-1], xkey)
    Mx = momen_arr(x, FY, CY)
    My = momen_arr(x, FX, [])
    Tz = Tval * Tmask(x)

    fig, axes = plt.subplots(3, 1, figsize=(8.2, 8.6), dpi=300)
    colors = ['#0072BD', '#D95319', '#77AC30']
    titles = [
        f'{title_prefix} - Biểu đồ mômen uốn trong mặt phẳng đứng $M_x$ (N.mm)',
        f'{title_prefix} - Biểu đồ mômen uốn trong mặt phẳng ngang $M_y$ (N.mm)',
        f'{title_prefix} - Biểu đồ mômen xoắn $T$ (N.mm)'
    ]

    for idx, (ax, Y, col, ttl, is_T) in enumerate(zip(axes, [Mx, My, Tz], colors, titles, [False, False, True])):
        ax.fill_between(x, Y, 0, color=col, alpha=0.25)
        ax.plot(x, Y, color=col, lw=2.0)
        ax.axhline(0, color='k', lw=1.1)
        yl = np.max(np.abs(Y)) if np.max(np.abs(Y)) > 0 else 1.0
        for xk in xkey:
            ax.axvline(xk, color='k', ls=':', lw=0.6)
        if not is_T:
            forces = FY if idx == 0 else FX
            couples = CY if idx == 0 else []
            for xk in xkey:
                ML = momen_arr(np.array([xk]), forces, couples)[0]
                MR = momen_arr(np.array([xk + 1e-6]), forces, couples)[0]
                if abs(ML) > 1:
                    va = 'bottom' if ML >= 0 else 'top'
                    dy = 0.04 * yl if ML >= 0 else -0.04 * yl
                    ax.text(xk - 3, ML + dy, f'{ML:,.0f}', ha='right', va=va, fontsize=8.5, fontweight='bold')
                if abs(MR - ML) > 1 and abs(MR) > 1:
                    va = 'bottom' if MR >= 0 else 'top'
                    dy = 0.04 * yl if MR >= 0 else -0.04 * yl
                    ax.text(xk + 3, MR + dy, f'{MR:,.0f}', ha='left', va=va, fontsize=8.5, fontweight='bold')
            ax.set_ylim(-1.32 * yl, 1.32 * yl)
            ax.set_ylabel('M (N.mm)', fontsize=9)
        else:
            pos = x[Y > 0]
            if len(pos):
                ax.text(np.mean(pos), yl * 1.04, f'T = {yl:,.0f} N.mm', ha='center', va='bottom',
                        fontsize=8.5, fontweight='bold')
            ax.set_ylim(0, 1.32 * yl)
            ax.set_ylabel('T (N.mm)', fontsize=9)

        ax.set_xlim(xkey[0], xkey[-1])
        ax.set_xticks(xkey)
        ax.set_xticklabels([f'{lb}\n({xk:.0f})' for lb, xk in zip(labels, xkey)], fontsize=8)
        ax.set_title(ttl, fontsize=10, fontweight='bold', pad=5)
        ax.grid(True, ls='--', alpha=0.35)

    axes[2].set_xlabel(xlabel_txt, fontsize=9, fontweight='bold')
    fig.tight_layout(h_pad=1.2)
    outp = os.path.join(OUT, fname)
    fig.savefig(outp, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print('Saved', outp)

# 1. Biểu đồ mômen Trục I
b1 = R['beam1']
plot_moment_3(
    b1['xs'], ['Puli', 'Ổ A', 'Trục vít', 'Ổ B'],
    b1['FY'], b1['CY'], b1['FX'], R['T1'],
    lambda x: (x >= b1['xs'][0]) & (x <= b1['xs'][2]),
    'Trục I', 'Vị trí dọc trục x (mm)', 'BieuDoMoment_TrucI.png'
)

# 2. Biểu đồ mômen Trục II
b2 = R['beam2']
plot_moment_3(
    b2['xs'], ['Ổ C', 'Bánh vít', 'Ổ D', 'Nối trục'],
    b2['FY'], b2['CY'], b2['FX'], R['T2'],
    lambda x: (x >= b2['xs'][1]) & (x <= b2['xs'][3]),
    'Trục II', 'Vị trí dọc trục x (mm)', 'BieuDoMoment_TrucII.png'
)

# 3. Sơ đồ đặt lực Trục I & Trục II
def draw_fbd(xs, names, v_forces, h_forces, couple_info, T_seg, title, fname):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8.2, 4.8), dpi=300)
    L = xs[-1]
    pad = L * 0.10

    def draw_plane(ax, forces, couple, subtitle, plane_lbl):
        ax.plot([xs[0], xs[-1]], [0, 0], 'k-', lw=3.0)
        for xk, nm in zip(xs, names):
            ax.plot(xk, 0, 'ko', ms=5)
            ax.text(xk, -0.35, nm, ha='center', va='top', fontsize=8.5, fontweight='bold')
            if 'Ổ' in nm:
                tri = patches.Polygon([[xk-L*0.018, -0.22], [xk+L*0.018, -0.22], [xk, -0.02]],
                                      closed=True, fc='#d9e2ec', ec='k', lw=1.0)
                ax.add_patch(tri)
        for xk, val, lbl, col in forces:
            sgn = 1 if val >= 0 else -1
            y0, y1 = (-0.75*sgn, -0.06*sgn) if False else (0.06*sgn, 0.78*sgn)
            # arrow points in direction of sign
            if sgn > 0:
                ax.annotate('', xy=(xk, 0.80), xytext=(xk, 0.08),
                            arrowprops=dict(arrowstyle='->', color=col, lw=2.0))
                ax.text(xk, 0.85, f'{lbl} = {abs(val):.1f} N', ha='center', va='bottom',
                        fontsize=8, color=col, fontweight='bold')
            else:
                ax.annotate('', xy=(xk, -0.80), xytext=(xk, -0.08),
                            arrowprops=dict(arrowstyle='->', color=col, lw=2.0))
                ax.text(xk, -0.85, f'{lbl} = {abs(val):.1f} N', ha='center', va='top',
                        fontsize=8, color=col, fontweight='bold')
        if couple is not None:
            xc, cval, clbl = couple
            arc = patches.Arc((xc, 0), L*0.08, 0.65, angle=0, theta1=-60, theta2=120, color='#7b2cbf', lw=1.8)
            ax.add_patch(arc)
            ax.text(xc + L*0.045, 0.35, f'{clbl} = {cval:,.0f} N.mm', ha='left', va='center',
                    fontsize=8, color='#7b2cbf', fontweight='bold')
        # dimensions
        for a, b in zip(xs[:-1], xs[1:]):
            y_d = -1.25
            ax.annotate('', xy=(b, y_d), xytext=(a, y_d),
                        arrowprops=dict(arrowstyle='<->', color='#444', lw=1.0))
            ax.text((a+b)/2, y_d - 0.05, f'{b-a:.0f} mm', ha='center', va='top', fontsize=8, color='#333')
        ax.set_xlim(-pad, L + pad)
        ax.set_ylim(-1.60, 1.35)
        ax.axis('off')
        ax.set_title(f'{subtitle} ({plane_lbl})', fontsize=9.5, fontweight='bold', pad=2)

    draw_plane(ax1, v_forces, couple_info, f'{title} - Sơ đồ lực mặt phẳng đứng', 'Oxy')
    draw_plane(ax2, h_forces, None, f'{title} - Sơ đồ lực mặt phẳng ngang', 'Oxz')
    fig.tight_layout(h_pad=0.6)
    outp = os.path.join(OUT, fname)
    fig.savefig(outp, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print('Saved', outp)

draw_fbd(
    b1['xs'], ['Puli (1-0)', 'Ổ A (1-1)', 'Trục vít (1-2)', 'Ổ B (1-3)'],
    [(b1['xs'][1], R['RAy'], 'R_Ay', '#0072BD'),
     (b1['xs'][2], R['Fr1'], 'F_r1', '#D95319'),
     (b1['xs'][3], R['RBy'], 'R_By', '#0072BD')],
    [(b1['xs'][0], R['Fr_d'], 'F_rđ', '#2ca02c'),
     (b1['xs'][1], R['RAx'], 'R_Ax', '#0072BD'),
     (b1['xs'][2], R['Ft1'], 'F_t1', '#D95319'),
     (b1['xs'][3], R['RBx'], 'R_Bx', '#0072BD')],
    (b1['xs'][2], R['Ma1'], 'M_a1'), None,
    'Trục I (Trục vít)', 'SoDoLuc_TrucI.png'
)

draw_fbd(
    b2['xs'], ['Ổ C (2-0)', 'Bánh vít (2-1)', 'Ổ D (2-2)', 'Nối trục (2-3)'],
    [(b2['xs'][0], R['RCy'], 'R_Cy', '#0072BD'),
     (b2['xs'][1], -R['Fr2'], 'F_r2', '#D95319'),
     (b2['xs'][2], R['RDy'], 'R_Dy', '#0072BD')],
    [(b2['xs'][0], R['RCx'], 'R_Cx', '#0072BD'),
     (b2['xs'][1], -R['Ft2'], 'F_t2', '#D95319'),
     (b2['xs'][2], R['RDx'], 'R_Dx', '#0072BD'),
     (b2['xs'][3], R['Fk'], 'F_k', '#2ca02c')],
    (b2['xs'][1], R['Ma2'], 'M_a2'), None,
    'Trục II (Trục bánh vít)', 'SoDoLuc_TrucII.png'
)

# 4. Bản vẽ kết cấu trục I và trục II
def draw_shaft(segments, keyways, title, fname, worm_idx=None):
    """segments: list of (length, diameter, label)"""
    fig, ax = plt.subplots(figsize=(8.4, 3.6), dpi=300)
    total_L = sum(s[0] for s in segments)
    max_D = max(s[1] for s in segments)
    x = 0.0
    # Centerline
    ax.plot([-18, total_L + 18], [0, 0], 'r-.', lw=0.9)
    for idx, (L_s, D_s, lbl) in enumerate(segments):
        r = D_s / 2.0
        fc = '#e8eef5' if idx != worm_idx else '#d8e4f0'
        rect = patches.Rectangle((x, -r), L_s, D_s, fc=fc, ec='k', lw=1.4)
        ax.add_patch(rect)
        if idx == worm_idx:
            # Draw worm thread lines
            n_th = 10
            xs_t = np.linspace(x + 8, x + L_s - 8, n_th)
            for xt in xs_t:
                ax.plot([xt - 5, xt + 5], [-r, r], 'k-', lw=0.7, alpha=0.7)
            ax.plot([x, x + L_s], [R['df1']/2, R['df1']/2], 'k--', lw=0.8)
            ax.plot([x, x + L_s], [-R['df1']/2, -R['df1']/2], 'k--', lw=0.8)
        # Diameter label above
        ax.annotate(f'Ø{D_s:.0f}\n({lbl})', xy=(x + L_s/2, r), xytext=(x + L_s/2, max_D/2 + 18),
                    ha='center', va='bottom', fontsize=7.5, fontweight='bold',
                    arrowprops=dict(arrowstyle='->', lw=0.7, color='#555'))
        # Length dimension below
        yd = -max_D/2 - 18
        ax.plot([x, x], [-r, yd - 4], 'k-', lw=0.5, alpha=0.6)
        ax.plot([x + L_s, x + L_s], [-r, yd - 4], 'k-', lw=0.5, alpha=0.6)
        ax.annotate('', xy=(x + L_s, yd), xytext=(x, yd),
                    arrowprops=dict(arrowstyle='<->', lw=0.8, color='k'))
        ax.text(x + L_s/2, yd - 3, f'{L_s:.0f}', ha='center', va='top', fontsize=8)
        x += L_s

    # Keyways (rounded slot)
    for kx0, kL, kb, klbl in keyways:
        slot = patches.FancyBboxPatch((kx0, -kb/2), kL, kb,
                                      boxstyle=f'round,pad=0,rounding_size={kb/2}',
                                      fc='white', ec='#0055aa', lw=1.2)
        ax.add_patch(slot)
        ax.text(kx0 + kL/2, 0, klbl, ha='center', va='center', fontsize=6.5, color='#0055aa', fontweight='bold')

    # Total length
    yd2 = -max_D/2 - 38
    ax.annotate('', xy=(total_L, yd2), xytext=(0, yd2),
                arrowprops=dict(arrowstyle='<->', lw=1.0, color='#0055aa'))
    ax.text(total_L/2, yd2 - 3, f'Tổng chiều dài L = {total_L:.0f} mm', ha='center', va='top',
            fontsize=8.5, fontweight='bold', color='#0055aa')

    ax.set_xlim(-22, total_L + 22)
    ax.set_ylim(-max_D/2 - 55, max_D/2 + 48)
    ax.set_aspect('equal', adjustable='datalim')
    ax.axis('off')
    ax.set_title(title, fontsize=10, fontweight='bold', pad=4)
    fig.tight_layout()
    outp = os.path.join(OUT, fname)
    fig.savefig(outp, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print('Saved', outp)

# Kết cấu Trục I (tổng 495 mm: đầu puli 65, cổ trục 40, vai+ổ A 70, phần ren trục vít 140, cổ vai 120, ổ B 60)
# Căn khớp chính xác: giữa puli (x=32.5), ổ A (x=107.5 => l11=75), giữa ren (x=287.5 => l12=180), ổ B (x=467.5 => l13=180)
draw_shaft(
    [(65, 40, 'Lắp puli'), (95, 50, 'Lắp ổ A'), (58, 56, 'Vai trục'),
     (140, 96, 'Ren trục vít'), (58, 56, 'Vai trục'), (79, 50, 'Lắp ổ B')],
    [(5, 56, 12, '12x8')],
    'Kết cấu Trục I (Trục vít liền trục, thép 40Cr)', 'KetCau_TrucI.png', worm_idx=3
)

# Kết cấu Trục II (ổ C 45, vai 30, bánh vít 110, vai 30, ổ D 45, nối trục 140 => tổng 400 mm)
draw_shaft(
    [(55, 65, 'Lắp ổ C'), (110, 70, 'Lắp bánh vít'), (18, 80, 'Vai'),
     (57, 65, 'Lắp ổ D'), (140, 63, 'Lắp nối trục')],
    [(60, 100, 20, '20x12'), (248, 125, 18, '18x11')],
    'Kết cấu Trục II (Trục bánh vít, thép 45)', 'KetCau_TrucII.png', worm_idx=None
)
