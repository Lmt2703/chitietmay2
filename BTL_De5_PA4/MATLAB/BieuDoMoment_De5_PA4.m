%% =====================================================================
%  BÀI TẬP LỚN CHI TIẾT MÁY - ĐỀ 5 - PHƯƠNG ÁN 4
%  Hệ thống dẫn động xích tải: Động cơ - Đai thang - HGT trục vít - Nối trục
%  BÀI TẬP 4: VẼ BIỂU ĐỒ MÔMEN UỐN Mx, My VÀ MÔMEN XOẮN T CỦA 2 TRỤC
%  ---------------------------------------------------------------------
%  Quy ước dấu:
%   - Lực: dương theo chiều dương của trục tọa độ (giả định trên sơ đồ).
%   - Mômen tập trung: dương khi ngược chiều kim đồng hồ.
%   - Mômen uốn tại mặt cắt x: M(x) = sum F_i*(x - x_i) - sum C_j
%     (lấy các ngoại lực nằm bên trái mặt cắt).
%  Đơn vị: lực [N], chiều dài [mm], mômen [N.mm]
%  Lưu file với mã hóa UTF-8 (MATLAB R2020a trở lên hiển thị tiếng Việt).
%% =====================================================================
clc; clear; close all;

%% ===================== SỐ LIỆU CHUNG =================================
T1   = 124088.5;   % Mômen xoắn trên trục I (trục vít), N.mm
T2   = 1200835.7;  % Mômen xoắn trên trục II (trục bánh vít), N.mm
Frd  = 1831.7;     % Lực bộ truyền đai tác dụng lên trục I, N
Ft1  = 3102.2;     % Lực vòng trên trục vít (= Fa2), N
Fa1  = 6526.3;     % Lực dọc trục trên trục vít (= Ft2), N
Fr1  = 2375.4;     % Lực hướng tâm trên trục vít (= Fr2), N
Ft2  = Fa1;  Fa2 = Ft1;  Fr2 = Fr1;
dw1  = 80;         % Đường kính vòng chia trục vít, mm
dw2  = 368;        % Đường kính vòng chia bánh vít, mm
Fk   = 3002.1;     % Lực do nối trục vòng đàn hồi tác dụng lên trục II, N

%% ===================== TRỤC I (TRỤC VÍT) =============================
l11 = 75;  l12 = 180;  l13 = 180;          % mm
xP = 0; xA = l11; xW = l11 + l12; xB = l11 + l12 + l13;
Ma1 = Fa1*dw1/2;                            % mômen do Fa1 gây ra, N.mm

% --- Mặt phẳng đứng: Fr1 (+, hướng lên), Ma1 (+) ---
xF_y1 = xW;          F_y1 = Fr1;
xC_y1 = xW;          C_y1 = Ma1;
[RAy, RBy] = phanluc(xF_y1, F_y1, xC_y1, C_y1, xA, xB);

% --- Mặt phẳng ngang: Frd (+), Ft1 (+) ---
xF_x1 = [xP  xW];    F_x1 = [Frd  Ft1];
[RAx, RBx] = phanluc(xF_x1, F_x1, [], [], xA, xB);

fprintf('===== TRUC I =====\n');
fprintf('RAy = %10.2f N   RBy = %10.2f N\n', RAy, RBy);
fprintf('RAx = %10.2f N   RBx = %10.2f N\n', RAx, RBx);

% Toàn bộ lực (kể cả phản lực) trong từng mặt phẳng
xFy = [xF_y1 xA xB];   Fy = [F_y1 RAy RBy];
xFx = [xF_x1 xA xB];   Fx = [F_x1 RAx RBx];
xkey1 = [xP xA xW xB];
x1 = luoi(xP, xB, xkey1);

Mx1 = momen(x1, xFy, Fy, xC_y1, C_y1);     % mặt phẳng đứng
My1 = momen(x1, xFx, Fx, [], []);           % mặt phẳng ngang
Tz1 = T1*((x1 >= xP) & (x1 <= xW));         % mômen xoắn: từ bánh đai đến trục vít

figure('Name','Truc I','Color','w','Position',[50 50 900 900]);
subplot(3,1,1); vebieudo(x1, Mx1, xkey1, xFy, Fy, xC_y1, C_y1, ...
    'Trục I - Biểu đồ mômen uốn trong mặt phẳng đứng M_x (N.mm)', [0.00 0.45 0.74]);
subplot(3,1,2); vebieudo(x1, My1, xkey1, xFx, Fx, [], [], ...
    'Trục I - Biểu đồ mômen uốn trong mặt phẳng ngang M_y (N.mm)', [0.85 0.33 0.10]);
subplot(3,1,3); vebieuDoXoan(x1, Tz1, xkey1, ...
    'Trục I - Biểu đồ mômen xoắn T (N.mm)', [0.47 0.67 0.19]);
xlabel('Vị trí dọc trục x (mm)  [Bánh đai - Ổ A - Trục vít - Ổ B]');
print(gcf, 'BieuDoMoment_TrucI.png', '-dpng', '-r300');

%% ===================== TRỤC II (TRỤC BÁNH VÍT) =======================
l21 = 85;  l22 = 85;  l23 = 110;            % mm
xC = 0; xG = l21; xD = l21 + l22; xK = l21 + l22 + l23;
Ma2 = Fa2*dw2/2;

% --- Mặt phẳng đứng: Fr2 (-, hướng xuống), Ma2 (+) ---
xF_y2 = xG;          F_y2 = -Fr2;
xC_y2 = xG;          C_y2 = Ma2;
[RCy, RDy] = phanluc(xF_y2, F_y2, xC_y2, C_y2, xC, xD);

% --- Mặt phẳng ngang: Ft2 (-), Fk (+) ngược chiều Ft2 ---
xF_x2 = [xG  xK];    F_x2 = [-Ft2  Fk];
[RCx, RDx] = phanluc(xF_x2, F_x2, [], [], xC, xD);

fprintf('===== TRUC II =====\n');
fprintf('RCy = %10.2f N   RDy = %10.2f N\n', RCy, RDy);
fprintf('RCx = %10.2f N   RDx = %10.2f N\n', RCx, RDx);

xFy2 = [xF_y2 xC xD];  Fy2 = [F_y2 RCy RDy];
xFx2 = [xF_x2 xC xD];  Fx2 = [F_x2 RCx RDx];
xkey2 = [xC xG xD xK];
x2 = luoi(xC, xK, xkey2);

Mx2 = momen(x2, xFy2, Fy2, xC_y2, C_y2);
My2 = momen(x2, xFx2, Fx2, [], []);
Tz2 = T2*((x2 >= xG) & (x2 <= xK));         % mômen xoắn: từ bánh vít đến nối trục

figure('Name','Truc II','Color','w','Position',[100 50 900 900]);
subplot(3,1,1); vebieudo(x2, Mx2, xkey2, xFy2, Fy2, xC_y2, C_y2, ...
    'Trục II - Biểu đồ mômen uốn trong mặt phẳng đứng M_x (N.mm)', [0.00 0.45 0.74]);
subplot(3,1,2); vebieudo(x2, My2, xkey2, xFx2, Fx2, [], [], ...
    'Trục II - Biểu đồ mômen uốn trong mặt phẳng ngang M_y (N.mm)', [0.85 0.33 0.10]);
subplot(3,1,3); vebieuDoXoan(x2, Tz2, xkey2, ...
    'Trục II - Biểu đồ mômen xoắn T (N.mm)', [0.47 0.67 0.19]);
xlabel('Vị trí dọc trục x (mm)  [Ổ C - Bánh vít - Ổ D - Nối trục]');
print(gcf, 'BieuDoMoment_TrucII.png', '-dpng', '-r300');

%% ===== MÔMEN TƯƠNG ĐƯƠNG TẠI CÁC TIẾT DIỆN =====
sig1 = 55; sig2 = 50;   % [sigma] (MPa) trục I (40Cr) và trục II (thép 45)
fprintf('\n===== MOMEN TUONG DUONG & DUONG KINH TOI THIEU =====\n');
tdien(xkey1, xFy, Fy, xC_y1, C_y1, xFx, Fx, T1*([1 1 1 0]), sig1, 'I');
tdien(xkey2, xFy2, Fy2, xC_y2, C_y2, xFx2, Fx2, T2*([0 1 1 1]), sig2, 'II');

%% =====================================================================
%                        CÁC HÀM CON (LOCAL FUNCTIONS)
%% =====================================================================
function [RA, RB] = phanluc(xF, F, xC, C, xA, xB)
% Giải phản lực 2 gối tựa A, B của dầm tĩnh định
%   Sum M_A = 0 : sum F_i (x_i - xA) + sum C_j + RB (xB - xA) = 0
%   Sum F   = 0 : sum F_i + RA + RB = 0
    MF = sum(F .* (xF - xA)) + sum(C);
    RB = -MF / (xB - xA);
    RA = -sum(F) - RB;
end

function M = momen(x, xF, F, xC, C)
% Mômen uốn tại các mặt cắt x (lấy ngoại lực phía bên trái mặt cắt)
    M = zeros(size(x));
    for i = 1:numel(F)
        M = M + F(i) .* (x - xF(i)) .* (x > xF(i));
    end
    for j = 1:numel(C)
        M = M - C(j) .* (x > xC(j));
    end
    M(abs(M) < 1e-6) = 0;
end

function x = luoi(x0, x1, xkey)
% Tạo lưới điểm, nhân đôi điểm tại vị trí đặt lực để thể hiện bước nhảy
    x = linspace(x0, x1, 2001);
    x = sort([x, xkey, xkey + 1e-6]);
    x = x(x <= x1);
end

function vebieudo(x, M, xkey, xF, F, xC, C, tieude, mau)
    yl = max(abs(M)); if yl == 0, yl = 1; end
    fill([x fliplr(x)], [M zeros(size(M))], mau, 'FaceAlpha', 0.25, 'EdgeColor', 'none'); hold on;
    plot(x, M, 'Color', mau, 'LineWidth', 2);
    plot([x(1) x(end)], [0 0], 'k', 'LineWidth', 1.2);
    for k = 1:numel(xkey)
        ML = momen(xkey(k), xF, F, xC, C);          % giá trị bên trái
        MR = momen(xkey(k) + 1e-6, xF, F, xC, C);   % giá trị bên phải
        plot([xkey(k) xkey(k)], [-1.3*yl 1.3*yl], 'k:', 'LineWidth', 0.5);
        if abs(ML) > 1
            text(xkey(k), ML, sprintf('%.0f ', ML), 'HorizontalAlignment', 'right', ...
                'VerticalAlignment', vtri(ML), 'FontSize', 9, 'FontWeight', 'bold');
        end
        if abs(MR - ML) > 1 && abs(MR) > 1
            text(xkey(k), MR, sprintf(' %.0f', MR), 'HorizontalAlignment', 'left', ...
                'VerticalAlignment', vtri(MR), 'FontSize', 9, 'FontWeight', 'bold');
        end
    end
    grid on; box on; title(tieude); ylabel('M (N.mm)');
    xlim([x(1) x(end)]);
    ylim([-1.3*yl 1.3*yl]);
    hold off;
end

function vebieuDoXoan(x, Tz, xkey, tieude, mau)
    fill([x fliplr(x)], [Tz zeros(size(Tz))], mau, 'FaceAlpha', 0.25, 'EdgeColor', 'none'); hold on;
    plot(x, Tz, 'Color', mau, 'LineWidth', 2);
    plot([x(1) x(end)], [0 0], 'k', 'LineWidth', 1.2);
    for k = 1:numel(xkey), plot([xkey(k) xkey(k)], [0 1.3*max(Tz)], 'k:', 'LineWidth', 0.5); end
    text(mean(x(Tz > 0)), max(Tz), sprintf('T = %.0f N.mm', max(Tz)), ...
        'HorizontalAlignment', 'center', 'VerticalAlignment', 'bottom', 'FontSize', 9, 'FontWeight', 'bold');
    grid on; box on; title(tieude); ylabel('T (N.mm)');
    xlim([x(1) x(end)]); ylim([0 1.3*max(Tz)]);
    hold off;
end

function s = vtri(M)
    if M >= 0, s = 'bottom'; else, s = 'top'; end
end

function tdien(xkey, xFy, Fy, xCy, Cy, xFx, Fx, T, sig, ten)
    for k = 1:numel(xkey)
        Mx = max(abs([momen(xkey(k), xFy, Fy, xCy, Cy), momen(xkey(k) + 1e-6, xFy, Fy, xCy, Cy)]));
        My = max(abs([momen(xkey(k), xFx, Fx, [], []), momen(xkey(k) + 1e-6, xFx, Fx, [], [])]));
        Mtd = sqrt(Mx^2 + My^2 + 0.75*T(k)^2);
        d = (Mtd/(0.1*sig))^(1/3);
        fprintf('Truc %s - tiet dien %d: Mx = %9.0f  My = %9.0f  T = %9.0f  Mtd = %9.0f N.mm  d >= %6.2f mm\n', ...
            ten, k-1, Mx, My, T(k), Mtd, d);
    end
end
