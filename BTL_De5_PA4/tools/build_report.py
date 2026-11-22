# -*- coding: utf-8 -*-
"""Tạo file thuyết minh BTL Chi tiết máy hoàn chỉnh (.docx) - Đề 5, Phương án 4
Đúng quy định trình bày Khoa Cơ Khí - ĐH Bách Khoa TP.HCM, công thức Microsoft Equation (OMML).
"""
import os, sys
from lxml import etree
import latex2mathml.converter
import docx
from docx import Document
from docx.shared import Cm, Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.enum.section import WD_SECTION_START
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls

sys.path.insert(0, os.path.dirname(__file__))
import calc
R = calc.R

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
FIG = os.path.join(BASE, 'figures')
MATLAB_FILE = os.path.join(BASE, 'MATLAB', 'BieuDoMoment_De5_PA4.m')
OUT_DOCX = os.path.join(BASE, 'ThuyetMinh_BTL_CTM_De5_PA4.docx')

XSL_PATH = r'C:\Program Files\Microsoft Office\root\Office16\MML2OMML.XSL'
_xsl = etree.XSLT(etree.parse(XSL_PATH))

def latex_to_omml(tex: str):
    mml_str = latex2mathml.converter.convert(tex)
    mml_xml = etree.fromstring(mml_str.encode('utf-8'))
    omml_xml = _xsl(mml_xml).getroot()
    # Set Times New Roman / Cambria Math cleanly
    return omml_xml

def fnum(val, dec=2):
    s = f'{val:,.{dec}f}'
    return s.replace(',', ' ').replace('.', ',')

def setup_page(sec, header_text=None, show_page_num=True, first_diff=False):
    sec.page_width = Cm(21.0)
    sec.page_height = Cm(29.7)
    sec.left_margin = Cm(3.0)
    sec.right_margin = Cm(2.0)
    sec.top_margin = Cm(2.0)
    sec.bottom_margin = Cm(2.0)
    sec.header_distance = Cm(1.25)
    sec.footer_distance = Cm(1.25)
    sec.different_first_page_header_footer = first_diff

    hdr = sec.header
    hdr.is_linked_to_previous = False
    p_h = hdr.paragraphs[0]
    p_h.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_h.paragraph_format.first_line_indent = Cm(0)
    p_h.paragraph_format.space_before = Pt(0)
    p_h.paragraph_format.space_after = Pt(2)
    p_h.text = ''
    if header_text:
        r = p_h.add_run(header_text)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(10)
        r.font.italic = True
        r.font.color.rgb = RGBColor(0x40, 0x40, 0x40)
        # bottom border on header
        pPr = p_h._p.get_or_add_pPr()
        pBdr = parse_xml(f'<w:pBdr {nsdecls("w")}><w:bottom w:val="single" w:sz="4" w:space="2" w:color="888888"/></w:pBdr>')
        pPr.append(pBdr)

    ftr = sec.footer
    ftr.is_linked_to_previous = False
    p_f = ftr.paragraphs[0]
    p_f.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_f.paragraph_format.first_line_indent = Cm(0)
    p_f.paragraph_format.space_before = Pt(0)
    p_f.paragraph_format.space_after = Pt(0)
    p_f.text = ''
    if show_page_num:
        run = p_f.add_run()
        run.font.name = 'Times New Roman'
        run.font.size = Pt(11)
        fld1 = parse_xml(r'<w:fldChar %s w:fldCharType="begin"/>' % nsdecls('w'))
        instr = parse_xml(r'<w:instrText %s xml:space="preserve"> PAGE </w:instrText>' % nsdecls('w'))
        fld2 = parse_xml(r'<w:fldChar %s w:fldCharType="separate"/>' % nsdecls('w'))
        fld3 = parse_xml(r'<w:fldChar %s w:fldCharType="end"/>' % nsdecls('w'))
        run._r.extend([fld1, instr, fld2, fld3])
    clear_page_border(sec)

def clear_page_border(sec):
    sectPr = sec._sectPr
    for el in list(sectPr.findall(qn('w:pgBorders'))):
        sectPr.remove(el)
    pgBorders = parse_xml(
        f'<w:pgBorders {nsdecls("w")} w:offsetFrom="page">'
        '<w:top w:val="none"/><w:bottom w:val="none"/>'
        '<w:left w:val="none"/><w:right w:val="none"/>'
        '</w:pgBorders>'
    )
    sectPr.append(pgBorders)

def add_page_border(sec):
    sectPr = sec._sectPr
    pgBorders = parse_xml(
        f'<w:pgBorders {nsdecls("w")} w:offsetFrom="page">'
        '<w:top w:val="double" w:sz="12" w:space="18" w:color="1F4E79"/>'
        '<w:bottom w:val="double" w:sz="12" w:space="18" w:color="1F4E79"/>'
        '<w:left w:val="double" w:sz="12" w:space="18" w:color="1F4E79"/>'
        '<w:right w:val="double" w:sz="12" w:space="18" w:color="1F4E79"/>'
        '</w:pgBorders>'
    )
    sectPr.append(pgBorders)

def set_font_tnr(run, size=12, bold=False, italic=False, color=None):
    run.font.name = 'Times New Roman'
    rPr = run._r.get_or_add_rPr()
    rFonts = rPr.find(qn('w:rFonts'))
    if rFonts is None:
        rFonts = OxmlElement('w:rFonts')
        rPr.insert(0, rFonts)
    rFonts.set(qn('w:ascii'), 'Times New Roman')
    rFonts.set(qn('w:hAnsi'), 'Times New Roman')
    rFonts.set(qn('w:cs'), 'Times New Roman')
    run.font.size = Pt(size)
    run.bold = bold
    run.italic = italic
    if color:
        run.font.color.rgb = color

import re

_SUB_RE = re.compile(r'([A-Za-zΑ-Ωα-ωστρβηαγΔΦΨΩ])_([A-Za-z0-9đĐστρβ,+-]+)')

def add_formatted_runs(p, text, size=12, bold=False, italic=False, color=None):
    pos = 0
    for m in _SUB_RE.finditer(text):
        # Skip filenames like BieuDoMoment_De5_PA4.m
        if m.start() > 0 and text[m.start()-1].isalnum() and len(m.group(2)) > 4:
            continue
        if m.start() > pos:
            r = p.add_run(text[pos:m.start()])
            set_font_tnr(r, size=size, bold=bold, italic=italic, color=color)
        r_base = p.add_run(m.group(1))
        set_font_tnr(r_base, size=size, bold=bold, italic=italic, color=color)
        r_sub = p.add_run(m.group(2))
        set_font_tnr(r_sub, size=size, bold=bold, italic=italic, color=color)
        r_sub.font.subscript = True
        pos = m.end()
    if pos < len(text):
        r = p.add_run(text[pos:])
        set_font_tnr(r, size=size, bold=bold, italic=italic, color=color)

def add_p(doc, text='', bold=False, italic=False, align=WD_ALIGN_PARAGRAPH.JUSTIFY,
          indent=1.0, space_before=3, space_after=3, size=12, color=None):
    p = doc.add_paragraph()
    p.alignment = align
    pf = p.paragraph_format
    pf.first_line_indent = Cm(indent)
    pf.space_before = Pt(space_before)
    pf.space_after = Pt(space_after)
    pf.line_spacing = 1.2
    if text:
        if 'BieuDoMoment' in text:
            r = p.add_run(text)
            set_font_tnr(r, size=size, bold=bold, italic=italic, color=color)
        else:
            add_formatted_runs(p, text, size=size, bold=bold, italic=italic, color=color)
    return p

def add_mixed(doc, parts, align=WD_ALIGN_PARAGRAPH.JUSTIFY, indent=1.0, space_before=3, space_after=3):
    """parts: list of ('t', str, bold, italic) or ('m', latex_str)"""
    p = doc.add_paragraph()
    p.alignment = align
    pf = p.paragraph_format
    pf.first_line_indent = Cm(indent)
    pf.space_before = Pt(space_before)
    pf.space_after = Pt(space_after)
    pf.line_spacing = 1.2
    for item in parts:
        if item[0] == 't':
            txt = item[1]
            b = item[2] if len(item) > 2 else False
            it = item[3] if len(item) > 3 else False
            r = p.add_run(txt)
            set_font_tnr(r, size=12, bold=b, italic=it)
        elif item[0] == 'm':
            p._p.append(latex_to_omml(item[1]))
    return p

def add_eq(doc, tex, num_str):
    """Add centered OMML equation with right-aligned equation number using a borderless 3-col table."""
    tbl = doc.add_table(rows=1, cols=3)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    widths = [Cm(1.5), Cm(12.5), Cm(2.0)]
    for cell, w in zip(tbl.rows[0].cells, widths):
        cell.width = w
        cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        tcPr = cell._tc.get_or_add_tcPr()
        tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="20" w:type="dxa"/><w:bottom w:w="20" w:type="dxa"/><w:left w:w="0" w:type="dxa"/><w:right w:w="0" w:type="dxa"/></w:tcMar>')
        tcPr.append(tcMar)
    # Remove all borders
    tblPr = tbl._tbl.tblPr
    tblBorders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        '<w:top w:val="none"/><w:left w:val="none"/><w:bottom w:val="none"/>'
        '<w:right w:val="none"/><w:insideH w:val="none"/><w:insideV w:val="none"/>'
        '</w:tblBorders>'
    )
    tblPr.append(tblBorders)

    p_mid = tbl.rows[0].cells[1].paragraphs[0]
    p_mid.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_mid.paragraph_format.first_line_indent = Cm(0)
    p_mid.paragraph_format.space_before = Pt(2)
    p_mid.paragraph_format.space_after = Pt(2)
    p_mid._p.append(latex_to_omml(tex))

    p_num = tbl.rows[0].cells[2].paragraphs[0]
    p_num.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_num.paragraph_format.first_line_indent = Cm(0)
    p_num.paragraph_format.space_before = Pt(2)
    p_num.paragraph_format.space_after = Pt(2)
    r = p_num.add_run(f'({num_str})')
    set_font_tnr(r, size=12)

def add_h1(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    pf = p.paragraph_format
    pf.first_line_indent = Cm(0)
    pf.space_before = Pt(6)
    pf.space_after = Pt(8)
    pf.keep_with_next = True
    r = p.add_run(text)
    set_font_tnr(r, size=14, bold=True, color=RGBColor(0x1F, 0x4E, 0x79))
    return p

def add_h2(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    pf = p.paragraph_format
    pf.first_line_indent = Cm(0)
    pf.space_before = Pt(8)
    pf.space_after = Pt(4)
    pf.keep_with_next = True
    r = p.add_run(text)
    set_font_tnr(r, size=13, bold=True, color=RGBColor(0x1F, 0x4E, 0x79))
    return p

def add_h3(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    pf = p.paragraph_format
    pf.first_line_indent = Cm(0)
    pf.space_before = Pt(6)
    pf.space_after = Pt(3)
    pf.keep_with_next = True
    r = p.add_run(text)
    set_font_tnr(r, size=12, bold=True)
    return p

def add_table(doc, headers, rows, caption=None, col_widths=None, font_size=11):
    if caption:
        pc = add_p(doc, caption, bold=True, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER,
                   indent=0, space_before=6, space_after=3, size=11)
        pc.paragraph_format.keep_with_next = True
    tbl = doc.add_table(rows=1 + len(rows), cols=len(headers))
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    tblPr = tbl._tbl.tblPr
    tblPr.append(parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        '<w:top w:val="single" w:sz="6" w:color="1F4E79"/>'
        '<w:bottom w:val="single" w:sz="6" w:color="1F4E79"/>'
        '<w:left w:val="single" w:sz="4" w:color="BFBFBF"/>'
        '<w:right w:val="single" w:sz="4" w:color="BFBFBF"/>'
        '<w:insideH w:val="single" w:sz="4" w:color="BFBFBF"/>'
        '<w:insideV w:val="single" w:sz="4" w:color="BFBFBF"/>'
        '</w:tblBorders>'
    ))
    # Header row
    trPr = tbl.rows[0]._tr.get_or_add_trPr()
    trPr.append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))
    for j, h in enumerate(headers):
        cell = tbl.rows[0].cells[j]
        if col_widths: cell.width = Cm(col_widths[j])
        cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        cell._tc.get_or_add_tcPr().append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="D9E2F3"/>'))
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.first_line_indent = Cm(0)
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.keep_with_next = True
        add_formatted_runs(p, str(h), size=font_size, bold=True)
    # Data rows
    for i, row in enumerate(rows):
        for j, val in enumerate(row):
            cell = tbl.rows[i + 1].cells[j]
            if col_widths: cell.width = Cm(col_widths[j])
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            if i % 2 == 1:
                cell._tc.get_or_add_tcPr().append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="F7F9FC"/>'))
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if j > 0 else WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.first_line_indent = Cm(0)
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2)
            add_formatted_runs(p, str(val), size=font_size)
    return tbl

def add_figure(doc, img_name, caption, width_cm=15.0):
    path = os.path.join(FIG, img_name)
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.first_line_indent = Cm(0)
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.keep_with_next = True
    p.add_run().add_picture(path, width=Cm(width_cm))
    pc = add_p(doc, caption, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER,
               indent=0, space_before=2, space_after=6, size=11)
    return p

def draw_cover_page(doc):
    add_p(doc, 'ĐẠI HỌC QUỐC GIA THÀNH PHỐ HỒ CHÍ MINH', bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, indent=0, size=13, space_before=6, space_after=2)
    add_p(doc, 'TRƯỜNG ĐẠI HỌC BÁCH KHOA', bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, indent=0, size=14, space_before=0, space_after=2)
    add_p(doc, 'KHOA CƠ KHÍ – BỘ MÔN THIẾT KẾ MÁY', bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, indent=0, size=12, space_before=0, space_after=6)
    add_p(doc, '─────────────── ★ ───────────────', align=WD_ALIGN_PARAGRAPH.CENTER, indent=0, size=12, space_before=0, space_after=40)

    add_p(doc, 'BÁO CÁO BÀI TẬP LỚN', bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, indent=0, size=20, space_before=10, space_after=6, color=RGBColor(0x1F, 0x4E, 0x79))
    add_p(doc, 'MÔN HỌC: CHI TIẾT MÁY', bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, indent=0, size=15, space_before=0, space_after=24)

    add_p(doc, 'ĐỀ SỐ 5 – PHƯƠNG ÁN 4', bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, indent=0, size=16, space_before=0, space_after=8, color=RGBColor(0x8B, 0x00, 0x00))
    add_p(doc, 'THIẾT KẾ HỆ THỐNG DẪN ĐỘNG XÍCH TẢI', bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, indent=0, size=16, space_before=0, space_after=6, color=RGBColor(0x1F, 0x4E, 0x79))
    add_p(doc, '(Động cơ điện – Bộ truyền đai thang – Hộp giảm tốc trục vít trụ – Nối trục đàn hồi – Xích tải)', italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, indent=0, size=12, space_before=0, space_after=54)

    # Info block
    tbl = doc.add_table(rows=5, cols=2)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    tbl._tbl.tblPr.append(parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        '<w:top w:val="none"/><w:left w:val="none"/><w:bottom w:val="none"/>'
        '<w:right w:val="none"/><w:insideH w:val="none"/><w:insideV w:val="none"/>'
        '</w:tblBorders>'
    ))
    info = [
        ('Giảng viên hướng dẫn:', '............................................................'),
        ('Sinh viên thực hiện:', '............................................................'),
        ('Mã số sinh viên:', '............................................................'),
        ('Lớp / Nhóm:', '............................................................'),
        ('Học kỳ / Năm học:', '............................................................'),
    ]
    for i, (k, v) in enumerate(info):
        c0, c1 = tbl.rows[i].cells
        c0.width = Cm(5.5); c1.width = Cm(9.5)
        p0 = c0.paragraphs[0]; p0.paragraph_format.first_line_indent = Cm(0); p0.paragraph_format.space_after = Pt(6)
        set_font_tnr(p0.add_run(k), size=12, bold=True)
        p1 = c1.paragraphs[0]; p1.paragraph_format.first_line_indent = Cm(0); p1.paragraph_format.space_after = Pt(6)
        set_font_tnr(p1.add_run(v), size=12)

    add_p(doc, '', indent=0, space_before=80, space_after=0)
    add_p(doc, 'TP. Hồ Chí Minh, năm 2026', bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, indent=0, size=12, space_before=20, space_after=0)

def build():
    doc = Document()
    # Set default Normal style
    st = doc.styles['Normal']
    st.font.name = 'Times New Roman'
    st.font.size = Pt(12)

    # ===================== TRANG BÌA & TRANG 1 (GIỐNG NHAU) =====================
    sec0 = doc.sections[0]
    setup_page(sec0, header_text=None, show_page_num=False)
    add_page_border(sec0)
    draw_cover_page(doc)
    doc.add_page_break()
    draw_cover_page(doc)

    # ===================== TRANG 2: ĐẦU ĐỀ BÀI TẬP LỚN =====================
    sec_de = doc.add_section(WD_SECTION_START.NEW_PAGE)
    setup_page(sec_de, header_text=None, show_page_num=False)
    add_p(doc, 'TRƯỜNG ĐẠI HỌC BÁCH KHOA TP. HCM – KHOA CƠ KHÍ', bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, indent=0, size=12, space_before=0, space_after=2)
    add_p(doc, 'BỘ MÔN THIẾT KẾ MÁY', bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, indent=0, size=12, space_before=0, space_after=6)
    add_p(doc, 'BÀI TẬP LỚN CHI TIẾT MÁY – ĐỀ SỐ 5 (PHƯƠNG ÁN 4)', bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, indent=0, size=13, space_before=4, space_after=2, color=RGBColor(0x1F, 0x4E, 0x79))
    add_p(doc, 'THIẾT KẾ HỆ THỐNG DẪN ĐỘNG XÍCH TẢI', bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, indent=0, size=13, space_before=0, space_after=6)

    add_figure(doc, 'SoDo_De5.png', 'Hình 0.1. Sơ đồ hệ thống dẫn động xích tải và sơ đồ tải trọng (Đề số 5)', width_cm=14.5)

    add_p(doc, 'Hệ thống dẫn động xích tải gồm: 1 – Động cơ điện; 2 – Bộ truyền đai thang; 3 – Hộp giảm tốc trục vít trụ (trục vít nằm trên bánh vít); 4 – Nối trục đàn hồi; 5 – Bộ phận công tác (Xích tải). Chiều quay như hình vẽ.', indent=0.8)
    add_table(doc,
        ['Thông số thiết kế', 'Ký hiệu', 'Giá trị', 'Đơn vị'],
        [
            ['Lực vòng trên xích tải', 'F', '7500', 'N'],
            ['Vận tốc xích tải', 'v', '1,05', 'm/s'],
            ['Số răng đĩa xích tải dẫn', 'Z', '9', 'răng'],
            ['Bước xích tải', 'p', '110', 'mm'],
            ['Thời gian phục vụ', 'L', '5', 'năm'],
            ['Chế độ làm việc', '—', 'Quay 1 chiều, 2 ca/ngày, tải va đập nhẹ (300 ngày/năm, 8 giờ/ca)', '—'],
            ['Chế độ tải trọng bậc 1', 'T₁ ; t₁', 'T₁ = T ; t₁ = 15 s', 'N.mm ; s'],
            ['Chế độ tải trọng bậc 2', 'T₂ ; t₂', 'T₂ = 0,5T ; t₂ = 48 s', 'N.mm ; s'],
            ['Sai số vòng quay trục công tác cho phép', '[Δn]', '≤ ±5%', '%'],
        ],
        caption='Bảng 0.1. Số liệu thiết kế Đề số 5 – Phương án 4',
        col_widths=[6.5, 2.2, 5.5, 1.8], font_size=10.5
    )
    add_p(doc, 'Yêu cầu nội dung thuyết minh: Chương 1 – Chọn động cơ điện và phân phối tỉ số truyền; Chương 2 – Thiết kế bộ truyền đai thang; Chương 3 – Thiết kế bộ truyền trục vít trụ; Chương 4 – Thiết kế 2 trục trong hộp giảm tốc, tính chọn then và vẽ biểu đồ mômen bằng MATLAB; Chương 5 – Tính chọn 2 cặp ổ lăn và nối trục vòng đàn hồi.', indent=0.8, space_before=6)

    # ===================== TRANG 3: MỤC LỤC, DANH MỤC HÌNH, BẢNG =====================
    sec_toc = doc.add_section(WD_SECTION_START.NEW_PAGE)
    setup_page(sec_toc, header_text='MỤC LỤC – DANH MỤC HÌNH ẢNH VÀ BẢNG BIỂU', show_page_num=True)
    add_h1(doc, 'MỤC LỤC')
    toc_rows = [
        ('CHƯƠNG 1. CHỌN ĐỘNG CƠ ĐIỆN VÀ PHÂN PHỐI TỈ SỐ TRUYỀN', 'Chương 1'),
        ('   1.1. Xác định công suất động cơ điện', ''),
        ('   1.2. Chọn động cơ điện', ''),
        ('   1.3. Phân phối tỉ số truyền', ''),
        ('   1.4. Tính toán thông số động học và lập bảng đặc tính', ''),
        ('CHƯƠNG 2. THIẾT KẾ BỘ TRUYỀN ĐAI THANG', 'Chương 2'),
        ('   2.1. Thông số ban đầu và chọn loại đai', ''),
        ('   2.2. Xác định đường kính bánh đai và kiểm tra vận tốc', ''),
        ('   2.3. Khoảng cách trục, chiều dài đai và góc ôm', ''),
        ('   2.4. Xác định số đai và kích thước bánh đai', ''),
        ('   2.5. Lực căng ban đầu và lực tác dụng lên trục', ''),
        ('   2.6. Tổng hợp thông số bộ truyền đai thang', ''),
        ('CHƯƠNG 3. THIẾT KẾ BỘ TRUYỀN TRỤC VÍT – BÁNH VÍT', 'Chương 3'),
        ('   3.1. Thông số ban đầu', ''),
        ('   3.2. Chọn vật liệu và xác định ứng suất cho phép', ''),
        ('   3.3. Tính toán khoảng cách trục và các thông số hình học', ''),
        ('   3.4. Kiểm nghiệm vận tốc trượt, hiệu suất và độ bền tiếp xúc', ''),
        ('   3.5. Kiểm nghiệm độ bền uốn răng bánh vít', ''),
        ('   3.6. Xác định các lực ăn khớp', ''),
        ('   3.7. Kiểm nghiệm độ cứng trục vít', ''),
        ('   3.8. Tính nhiệt và chọn dầu bôi trơn', ''),
        ('   3.9. Tổng hợp thông số bộ truyền trục vít – bánh vít', ''),
        ('CHƯƠNG 4. THIẾT KẾ HAI TRỤC TRONG HỘP GIẢM TỐC VÀ TÍNH CHỌN THEN', 'Chương 4'),
        ('   4.1. Chọn vật liệu và xác định khoảng cách gối đỡ', ''),
        ('   4.2. Thiết kế Trục I (Trục vít)', ''),
        ('   4.3. Thiết kế Trục II (Trục bánh vít)', ''),
        ('   4.4. Chương trình MATLAB vẽ biểu đồ mômen hai trục', ''),
        ('CHƯƠNG 5. TÍNH CHỌN Ổ LĂN VÀ NỐI TRỤC VÒNG ĐÀN HỒI', 'Chương 5'),
        ('   5.1. Tính chọn cặp ổ lăn cho Trục I', ''),
        ('   5.2. Tính chọn cặp ổ lăn cho Trục II', ''),
        ('   5.3. Tính chọn và kiểm nghiệm nối trục vòng đàn hồi', ''),
        ('TÀI LIỆU THAM KHẢO', 'Cuối báo cáo'),
    ]
    for title, tag in toc_rows:
        is_main = not title.startswith('   ')
        add_p(doc, title, bold=is_main, indent=0 if is_main else 0.6, space_before=2 if is_main else 1, space_after=1, size=11)

    add_h2(doc, 'DANH MỤC HÌNH ẢNH')
    figs_list = [
        'Hình 0.1. Sơ đồ hệ thống dẫn động xích tải và sơ đồ tải trọng (Đề số 5)',
        'Hình 4.1. Sơ đồ đặt lực và phản lực gối tựa Trục I (Trục vít)',
        'Hình 4.2. Biểu đồ mômen uốn Mx, My và mômen xoắn T của Trục I (vẽ bằng MATLAB)',
        'Hình 4.3. Bản vẽ kết cấu Trục I (Trục vít liền trục)',
        'Hình 4.4. Sơ đồ đặt lực và phản lực gối tựa Trục II (Trục bánh vít)',
        'Hình 4.5. Biểu đồ mômen uốn Mx, My và mômen xoắn T của Trục II (vẽ bằng MATLAB)',
        'Hình 4.6. Bản vẽ kết cấu Trục II (Trục bánh vít)',
    ]
    for s in figs_list:
        add_p(doc, s, indent=0.5, space_before=1, space_after=1, size=11)

    add_h2(doc, 'DANH MỤC BẢNG BIỂU')
    tbls_list = [
        'Bảng 0.1. Số liệu thiết kế Đề số 5 – Phương án 4',
        'Bảng 1.1. Thông số kỹ thuật động cơ điện 4A132S4Y3',
        'Bảng 1.2. Bảng đặc tính động học và công suất của hệ thống dẫn động',
        'Bảng 2.1. Bảng tổng hợp thông số thiết kế bộ truyền đai thang',
        'Bảng 3.1. Bảng tổng hợp thông số bộ truyền trục vít – bánh vít',
        'Bảng 4.1. Mômen tương đương và đường kính tối thiểu tại các tiết diện Trục I',
        'Bảng 4.2. Kết quả kiểm nghiệm độ bền mỏi các tiết diện Trục I',
        'Bảng 4.3. Mômen tương đương và đường kính tối thiểu tại các tiết diện Trục II',
        'Bảng 4.4. Kết quả kiểm nghiệm độ bền mỏi các tiết diện Trục II',
        'Bảng 5.1. Thông số ổ đũa côn một dãy 7310 lắp trên Trục I',
        'Bảng 5.2. Thông số ổ đũa côn một dãy 7213 lắp trên Trục II',
        'Bảng 5.3. Thông số kích thước cơ bản của nối trục vòng đàn hồi',
    ]
    for s in tbls_list:
        add_p(doc, s, indent=0.5, space_before=1, space_after=1, size=11)

    # ===================== CHƯƠNG 1 =====================
    sec1 = doc.add_section(WD_SECTION_START.NEW_PAGE)
    setup_page(sec1, header_text='Chương 1. Chọn động cơ điện và phân phối tỉ số truyền', show_page_num=True)
    add_h1(doc, 'CHƯƠNG 1. CHỌN ĐỘNG CƠ ĐIỆN VÀ PHÂN PHỐI TỈ SỐ TRUYỀN')

    add_h2(doc, '1.1. Xác định công suất động cơ điện')
    add_p(doc, 'Công suất lớn nhất (tải trọng danh nghĩa) trên trục đĩa xích tải dẫn được xác định theo [1], [2]:')
    add_eq(doc, rf'P_{{\max}} = \frac{{F \cdot v}}{{1000}} = \frac{{7500 \times 1{{,}}05}}{{1000}} = {fnum(R["Pmax"], 3)}\ \text{{(kW)}}', '1.1')

    add_p(doc, 'Do tải trọng làm việc thay đổi theo bậc (bậc 1: T₁ = T trong t₁ = 15 s; bậc 2: T₂ = 0,5T trong t₂ = 48 s), công suất đẳng trị trên trục máy công tác là:')
    add_eq(doc, rf'P_{{dt}} = P_{{\max}} \sqrt{{\frac{{\left(\frac{{T_1}}{{T}}\right)^2 t_1 + \left(\frac{{T_2}}{{T}}\right)^2 t_2}}{{t_1 + t_2}}}} = 7{{,}}875 \sqrt{{\frac{{1^2 \times 15 + 0{{,}}5^2 \times 48}}{{15 + 48}}}} = {fnum(R["Pdt"], 3)}\ \text{{(kW)}}', '1.2')

    add_p(doc, 'Hiệu suất chung của toàn bộ hệ thống dẫn động (gồm 1 bộ truyền đai thang, 1 cặp trục vít – bánh vít, 2 cặp ổ lăn và 1 nối trục đàn hồi), tra Bảng 2.3 tài liệu [2]:')
    add_mixed(doc, [
        ('t', '– Hiệu suất bộ truyền đai thang để hở: '), ('m', r'\eta_d = 0{,}95'), ('t', ';'),
    ], indent=1.0)
    add_mixed(doc, [
        ('t', '– Hiệu suất bộ truyền trục vít – bánh vít (sơ bộ với '), ('m', r'z_1 = 4'), ('t', ' mối ren): '), ('m', r'\eta_{tv} = 0{,}85'), ('t', ';'),
    ], indent=1.0)
    add_mixed(doc, [
        ('t', '– Hiệu suất một cặp ổ lăn: '), ('m', r'\eta_{ol} = 0{,}99'), ('t', '; hiệu suất nối trục đàn hồi: '), ('m', r'\eta_k = 1{,}0'), ('t', '.'),
    ], indent=1.0)
    add_eq(doc, rf'\eta = \eta_d \cdot \eta_{{tv}} \cdot \eta_{{ol}}^2 \cdot \eta_k = 0{{,}}95 \times 0{{,}}85 \times 0{{,}}99^2 \times 1{{,}}0 = {fnum(R["eta"], 3)}', '1.3')

    add_p(doc, 'Công suất cần thiết trên trục động cơ điện:')
    add_eq(doc, rf'P_{{ct}} = \frac{{P_{{dt}}}}{{\eta}} = \frac{{{fnum(R["Pdt"], 3)}}}{{{fnum(R["eta"], 3)}}} = {fnum(R["Pct"], 3)}\ \text{{(kW)}}', '1.4')

    add_h2(doc, '1.2. Chọn động cơ điện')
    add_p(doc, 'Số vòng quay làm việc của trục đĩa xích tải dẫn (với z = 9 răng, bước xích p = 110 mm):')
    add_eq(doc, rf'n_{{lv}} = \frac{{60000 \cdot v}}{{z \cdot p}} = \frac{{60000 \times 1{{,}}05}}{{9 \times 110}} = {fnum(R["nlv"], 2)}\ \text{{(vg/ph)}}', '1.5')

    add_p(doc, 'Chọn sơ bộ tỉ số truyền của bộ truyền đai thang u_đ = 2 và hộp giảm tốc trục vít một cấp u_tv = 10 ÷ 15, suy ra tỉ số truyền chung sơ bộ u_sb = 20 ÷ 30. Số vòng quay sơ bộ của động cơ điện:')
    add_eq(doc, r'n_{sb} = n_{lv} \cdot u_{sb} = 63{,}64 \times (20 \div 30) = 1273 \div 1909\ \text{(vg/ph)}', '1.6')

    add_p(doc, 'Chọn động cơ điện không đồng bộ 3 pha xoay chiều có tốc độ đồng bộ 1500 vg/ph, thỏa mãn điều kiện P_đc ≥ P_ct = 6,514 kW và điều kiện mở máy T_k / T_dn ≥ T_1 / T_dt. Tra Phụ lục P1.3 tài liệu [2], ta chọn động cơ 4A132S4Y3 với các thông số như Bảng 1.1.')
    add_table(doc,
        ['Kiểu động cơ', 'Công suất P_đc (kW)', 'Vận tốc quay n_đc (vg/ph)', 'cos φ', 'Hiệu suất η (%)', 'T_max/T_dn', 'T_k/T_dn', 'Đường kính trục d_đc (mm)'],
        [['4A132S4Y3', '7,5', '1455', '0,86', '87,5', '2,2', '2,0', '38']],
        caption='Bảng 1.1. Thông số kỹ thuật động cơ điện 4A132S4Y3 [2]',
        col_widths=[2.5, 2.0, 2.2, 1.4, 1.9, 1.9, 1.8, 2.3], font_size=10
    )
    add_mixed(doc, [
        ('t', 'Kiểm tra điều kiện mở máy và quá tải ngắn hạn: '),
        ('m', rf'P_{{\text{{đc}}}} = 7{{,}}5\ \text{{kW}} > P_{{ct}} = {fnum(R["Pct"], 3)}\ \text{{kW}}'),
        ('t', '; tỉ số mở máy '),
        ('m', rf'T_k/T_{{dn}} = 2{{,}}0 > P_0/P_{{\text{{đc}}}} = {fnum(R["qua_tai"], 2)}'),
        ('t', ' (thỏa mãn).'),
    ])

    add_h2(doc, '1.3. Phân phối tỉ số truyền')
    add_p(doc, 'Tỉ số truyền toàn bộ của hệ thống dẫn động:')
    add_eq(doc, rf'u_t = \frac{{n_{{\text{{đc}}}}}}{{n_{{lv}}}} = \frac{{1455}}{{63{{,}}64}} = {fnum(R["ut"], 3)}', '1.7')
    add_p(doc, 'Chọn tỉ số truyền của bộ truyền đai thang u_đ = 2,0 (nằm trong dãy tiêu chuẩn và tối ưu cho đai thang [1]). Tỉ số truyền sơ bộ của hộp giảm tốc trục vít:')
    add_eq(doc, rf'u_{{tv,sb}} = \frac{{u_t}}{{u_d}} = \frac{{{fnum(R["ut"], 3)}}}{{2{{,}}0}} = {fnum(R["utv_sb"], 3)}', '1.8')
    add_p(doc, 'Với u_tv,sb = 11,432 (nằm trong khoảng 8 ÷ 15), chọn số mối ren trục vít z₁ = 4 để đạt hiệu suất cao; số răng bánh vít z₂ = u_tv,sb · z₁ = 11,432 × 4 = 45,73 → chọn z₂ = 46 răng (thỏa mãn z₂ ≥ 28 tránh cắt chân răng). Khi đó tỉ số truyền chính xác của bộ truyền trục vít là:')
    add_eq(doc, rf'u_{{tv}} = \frac{{z_2}}{{z_1}} = \frac{{46}}{{4}} = 11{{,}}5', '1.9')

    add_h2(doc, '1.4. Tính toán thông số động học và lập bảng đặc tính')
    add_p(doc, 'Để tính toán độ bền cho các bộ truyền và trục theo tải trọng lớn nhất (tải trọng danh nghĩa P_lv = P_max = 7,875 kW), ta tính công suất, số vòng quay và mômen xoắn trên từng trục ngược từ trục công tác về trục động cơ [1], [2]:')
    add_eq(doc, rf'P_{{II}} = \frac{{P_{{lv}}}}{{\eta_k \cdot \eta_{{ol}}}} = \frac{{7{{,}}875}}{{1{{,}}0 \times 0{{,}}99}} = {fnum(R["P2"], 3)}\ \text{{(kW)}}', '1.10')
    add_eq(doc, rf'P_{{I}} = \frac{{P_{{II}}}}{{\eta_{{tv}} \cdot \eta_{{ol}}}} = \frac{{{fnum(R["P2"], 3)}}}{{0{{,}}85 \times 0{{,}}99}} = {fnum(R["P1"], 3)}\ \text{{(kW)}}', '1.11')
    add_eq(doc, rf'P_{{\text{{đc,tt}}}} = \frac{{P_{{I}}}}{{\eta_d}} = \frac{{{fnum(R["P1"], 3)}}}{{0{{,}}95}} = {fnum(R["P0"], 3)}\ \text{{(kW)}}', '1.12')
    add_p(doc, 'Số vòng quay và mômen xoắn (T = 9,55×10⁶·P/n, đơn vị N.mm) trên các trục được tổng hợp trong Bảng 1.2.')
    add_table(doc,
        ['Thông số', 'Trục động cơ', 'Trục I (Trục vít)', 'Trục II (Bánh vít)', 'Trục công tác'],
        [
            ['Công suất P (kW)', fnum(R['P0'], 3), fnum(R['P1'], 3), fnum(R['P2'], 3), fnum(R['P_lv'], 3)],
            ['Tỉ số truyền u', 'u_đ = 2,0', 'u_tv = 11,5', 'u_k = 1,0', '—'],
            ['Số vòng quay n (vg/ph)', fnum(R['n0'], 1), fnum(R['n1'], 2), fnum(R['n2'], 2), fnum(R['n2'], 2)],
            ['Mômen xoắn T (N.mm)', fnum(R['T0'], 1), fnum(R['T1'], 1), fnum(R['T2'], 1), fnum(R['Tlv'], 1)],
        ],
        caption='Bảng 1.2. Bảng đặc tính động học và công suất của hệ thống dẫn động',
        col_widths=[4.4, 2.9, 2.9, 2.9, 2.9], font_size=10.5
    )

    # ===================== CHƯƠNG 2 =====================
    sec2 = doc.add_section(WD_SECTION_START.NEW_PAGE)
    setup_page(sec2, header_text='Chương 2. Thiết kế bộ truyền đai thang', show_page_num=True)
    add_h1(doc, 'CHƯƠNG 2. THIẾT KẾ BỘ TRUYỀN ĐAI THANG')

    add_h2(doc, '2.1. Thông số ban đầu và chọn loại đai')
    add_mixed(doc, [
        ('t', 'Thông số đầu vào bộ truyền đai thang: công suất truyền '),
        ('m', rf'P_1 = {fnum(R["P0"], 3)}\ \text{{kW}}'),
        ('t', ', số vòng quay bánh dẫn '),
        ('m', r'n_1 = 1455\ \text{vg/ph}'),
        ('t', ', mômen xoắn '),
        ('m', rf'T_1 = {fnum(R["T0"]/1000, 2)}\ \text{{N.m}}'),
        ('t', ', tỉ số truyền '),
        ('m', r'u_d = 2{,}0'),
        ('t', '. Dựa vào đồ thị chọn tiết diện đai thang (Hình 4.22, Bảng 4.3 tài liệu [1]), ta chọn đai thang thường loại '),
        ('t', 'B', True),
        ('t', ' có các thông số kích thước: '),
        ('m', r'b_p = 14\ \text{mm},\ b_0 = 17\ \text{mm},\ h = 10{,}5\ \text{mm},\ y_0 = 4\ \text{mm},\ A = 138\ \text{mm}^2,\ d_{\min} = 140\ \text{mm}'),
        ('t', '.'),
    ])

    add_h2(doc, '2.2. Xác định đường kính bánh đai và kiểm tra vận tốc')
    add_p(doc, 'Đường kính bánh đai dẫn d₁:')
    add_eq(doc, r'd_1 \approx 1{,}2 \cdot d_{\min} = 1{,}2 \times 140 = 168\ \text{(mm)}', '2.1')
    add_p(doc, 'Chọn theo dãy tiêu chuẩn: d₁ = 160 mm. Kiểm tra vận tốc vòng của đai:')
    add_eq(doc, rf'v_1 = \frac{{\pi \cdot d_1 \cdot n_1}}{{60000}} = \frac{{\pi \times 160 \times 1455}}{{60000}} = {fnum(R["v1"], 2)}\ \text{{(m/s)}} < [v] = 25\ \text{{(m/s)}}', '2.2')
    add_p(doc, 'Vận tốc đai nằm trong giới hạn cho phép, chấp nhận d₁ = 160 mm. Chọn hệ số trượt đàn hồi ξ = 0,02, đường kính bánh đai bị dẫn d₂ là:')
    add_eq(doc, rf'd_2 = u_d \cdot d_1 \cdot (1 - \xi) = 2{{,}}0 \times 160 \times (1 - 0{{,}}02) = {fnum(R["d2_tt"], 1)}\ \text{{(mm)}}', '2.3')
    add_p(doc, 'Chọn theo dãy tiêu chuẩn: d₂ = 315 mm. Khi đó tỉ số truyền thực tế của bộ truyền đai là:')
    add_eq(doc, rf'u_{{d,tt}} = \frac{{d_2}}{{d_1(1 - \xi)}} = \frac{{315}}{{160 \times 0{{,}}98}} = {fnum(R["ud_tt"], 3)}', '2.4')
    add_p(doc, 'Kiểm tra sai số vòng quay thực tế trên trục máy công tác:')
    add_eq(doc, rf'n_{{lv,tt}} = \frac{{n_{{\text{{đc}}}}}}{{u_{{d,tt}} \cdot u_{{tv}}}} = \frac{{1455}}{{{fnum(R["ud_tt"], 3)} \times 11{{,}}5}} = {fnum(R["n2_tt"], 2)}\ \text{{(vg/ph)}}', '2.5')
    add_eq(doc, rf'\Delta n = \frac{{|n_{{lv,tt}} - n_{{lv}}|}}{{n_{{lv}}}} \times 100\% = \frac{{|{fnum(R["n2_tt"], 2)} - 63{{,}}64|}}{{63{{,}}64}} \times 100\% = {fnum(abs(R["sai_so"]), 2)}\% < [\Delta n] = 5\%', '2.6')

    add_h2(doc, '2.3. Khoảng cách trục, chiều dài đai và góc ôm')
    add_p(doc, 'Với u_đ = 2, theo bảng chọn sơ bộ khoảng cách trục (Chương 4 [1]), lấy a_sb = 1,2·d₂ = 1,2 × 315 = 378 mm. Chiều dài đai tính toán theo a_sb:')
    add_eq(doc, rf'L_{{tt}} = 2a_{{sb}} + \frac{{\pi(d_1 + d_2)}}{{2}} + \frac{{(d_2 - d_1)^2}}{{4a_{{sb}}}} = 2 \times 378 + \frac{{\pi(160 + 315)}}{{2}} + \frac{{(315 - 160)^2}}{{4 \times 378}} = {fnum(R["L_tt"], 1)}\ \text{{(mm)}}', '2.7')
    add_p(doc, 'Chọn chiều dài đai theo tiêu chuẩn: L = 1600 mm. Kiểm tra số vòng chạy của đai trong 1 giây:')
    add_eq(doc, rf'i = \frac{{v_1}}{{L/1000}} = \frac{{{fnum(R["v1"], 2)}}}{{1{{,}}6}} = {fnum(R["i_s"], 2)}\ \text{{(s}}^{{-1}}\text{{)}} < [i] = 10\ \text{{(s}}^{{-1}}\text{{)}}', '2.8')
    add_p(doc, 'Tính chính xác lại khoảng cách trục a theo chiều dài đai tiêu chuẩn L = 1600 mm:')
    add_eq(doc, rf'k = L - \frac{{\pi(d_1 + d_2)}}{{2}} = 1600 - \frac{{\pi(160 + 315)}}{{2}} = {fnum(R["kL"], 2)}\ \text{{(mm)}};\quad \Delta = \frac{{d_2 - d_1}}{{2}} = 77{{,}}5\ \text{{(mm)}}', '2.9')
    add_eq(doc, rf'a = \frac{{k + \sqrt{{k^2 - 8\Delta^2}}}}{{4}} = \frac{{{fnum(R["kL"], 2)} + \sqrt{{{fnum(R["kL"], 2)}^2 - 8 \times 77{{,}}5^2}}}}{{4}} = {fnum(R["a"], 2)}\ \text{{(mm)}}', '2.10')
    add_mixed(doc, [
        ('t', 'Kiểm tra điều kiện khoảng cách trục: '),
        ('m', rf'0{{,}}55(d_1 + d_2) + h = {fnum(R["amin"], 2)}\ \text{{mm}} \le a = {fnum(R["a"], 2)}\ \text{{mm}} \le 2(d_1 + d_2) = 950\ \text{{mm}}'),
        ('t', ' (thỏa mãn). Tính góc ôm đai trên bánh dẫn:'),
    ])
    add_eq(doc, rf'\alpha_1 = 180^\circ - 57^\circ \frac{{d_2 - d_1}}{{a}} = 180^\circ - 57^\circ \frac{{315 - 160}}{{{fnum(R["a"], 2)}}} = {fnum(R["alpha1"], 2)}^\circ > [\alpha_1] = 120^\circ', '2.11')

    add_h2(doc, '2.4. Xác định số đai và kích thước bánh đai')
    add_p(doc, 'Số dây đai z được xác định theo điều kiện khả năng kéo [1]:')
    add_eq(doc, r'z \ge \frac{P_1}{[P_0] \cdot C_\alpha \cdot C_u \cdot C_L \cdot C_z \cdot C_r \cdot C_v}', '2.12')
    add_p(doc, 'Trong đó các thông số và hệ số tra theo giáo trình [1]:')
    add_mixed(doc, [('t', '– Công suất có ích cho phép của 1 đai loại B ('), ('m', r'd_1 = 160\ \text{mm},\ v_1 = 12{,}19\ \text{m/s},\ L_0 = 2240\ \text{mm}'), ('t', '): '), ('m', r'[P_0] = 4{,}0\ \text{kW}'), ('t', ';')], indent=1.0)
    add_mixed(doc, [('t', '– Hệ số góc ôm: '), ('m', rf'C_\alpha = 1{{,}}24\left(1 - e^{{-\alpha_1/110}}\right) = 1{{,}}24\left(1 - e^{{-{fnum(R["alpha1"], 2)}/110}}\right) = {fnum(R["Ca"], 3)}'), ('t', ';')], indent=1.0)
    add_mixed(doc, [('t', '– Hệ số tỉ số truyền ('), ('m', r'u_d = 2'), ('t', '): '), ('m', r'C_u = 1{,}13'), ('t', '; hệ số chế độ làm việc (2 ca, tải va đập nhẹ): '), ('m', r'C_r = 0{,}90'), ('t', ';')], indent=1.0)
    add_mixed(doc, [('t', '– Hệ số chiều dài đai: '), ('m', rf'C_L = \sqrt[6]{{L / L_0}} = \sqrt[6]{{1600 / 2240}} = {fnum(R["CL"], 3)}'), ('t', ';')], indent=1.0)
    add_mixed(doc, [('t', '– Hệ số vận tốc: '), ('m', rf'C_v = 1 - 0{{,}}05(0{{,}}01 v_1^2 - 1) = 1 - 0{{,}}05(0{{,}}01 \times 12{{,}}19^2 - 1) = {fnum(R["Cv"], 3)}'), ('t', ';')], indent=1.0)
    add_mixed(doc, [('t', '– Hệ số phân bố tải trọng giữa các đai (giả sử '), ('m', r'z = 2 \div 3'), ('t', '): '), ('m', r'C_z = 0{,}95'), ('t', '.')], indent=1.0)
    add_eq(doc, rf'z \ge \frac{{{fnum(R["P0"], 3)}}}{{4{{,}}0 \times {fnum(R["Ca"], 3)} \times 1{{,}}13 \times {fnum(R["CL"], 3)} \times 0{{,}}95 \times 0{{,}}90 \times {fnum(R["Cv"], 3)}}} = {fnum(R["z_tt"], 2)} \Rightarrow \text{{chọn }} z = 3\ \text{{đai}}', '2.13')
    add_p(doc, 'Giá trị z = 3 thỏa mãn giả sử chọn C_z = 0,95 và z ≤ 6. Với đai loại B, tra Bảng 4.4 [1] có e = 19 mm, f = 12,5 mm, h₀ = 4,2 mm. Chiều rộng bánh đai và đường kính ngoài bánh đai:')
    add_eq(doc, r'B = (z - 1)e + 2f = (3 - 1) \times 19 + 2 \times 12{,}5 = 63\ \text{(mm)}', '2.14')
    add_eq(doc, r'd_{a1} = d_1 + 2h_0 = 160 + 2 \times 4{,}2 = 168{,}4\ \text{(mm)};\quad d_{a2} = d_2 + 2h_0 = 315 + 2 \times 4{,}2 = 323{,}4\ \text{(mm)}', '2.15')

    add_h2(doc, '2.5. Lực căng ban đầu và lực tác dụng lên trục')
    add_p(doc, 'Chọn ứng suất căng đai ban đầu σ₀ = 1,5 MPa [1], lực căng ban đầu của bộ truyền đai:')
    add_eq(doc, r'F_0 = \sigma_0 \cdot z \cdot A = 1{,}5 \times 3 \times 138 = 621\ \text{(N)}', '2.16')
    add_p(doc, 'Lực tác dụng lên trục và ổ lăn (theo công thức gần đúng trong [1], Ví dụ BTL):')
    add_eq(doc, rf'F_{{r\text{{đ}}}} = 3 F_0 \sin\left(\frac{{\alpha_1}}{{2}}\right) = 3 \times 621 \times \sin\left(\frac{{{fnum(R["alpha1"], 2)}^\circ}}{{2}}\right) = {fnum(R["Fr_d"], 1)}\ \text{{(N)}}', '2.17')

    add_h2(doc, '2.6. Tổng hợp thông số bộ truyền đai thang')
    add_table(doc,
        ['Thông số', 'Ký hiệu', 'Giá trị', 'Thông số', 'Ký hiệu', 'Giá trị'],
        [
            ['Loại đai thang', '—', 'Loại B', 'Số dây đai', 'z', '3 đai'],
            ['Đường kính bánh dẫn', 'd₁', '160 mm', 'Chiều rộng bánh đai', 'B', '63 mm'],
            ['Đường kính bánh bị dẫn', 'd₂', '315 mm', 'Đường kính ngoài', 'd_a1 / d_a2', '168,4 / 323,4 mm'],
            ['Khoảng cách trục', 'a', f'{fnum(R["a"], 2)} mm', 'Góc ôm bánh nhỏ', 'α₁', f'{fnum(R["alpha1"], 2)}°'],
            ['Chiều dài đai tiêu chuẩn', 'L', '1600 mm', 'Lực căng ban đầu', 'F₀', '621 N'],
            ['Vận tốc đai', 'v₁', f'{fnum(R["v1"], 2)} m/s', 'Lực tác dụng lên trục', 'F_rđ', f'{fnum(R["Fr_d"], 1)} N'],
        ],
        caption='Bảng 2.1. Bảng tổng hợp thông số thiết kế bộ truyền đai thang',
        col_widths=[4.0, 1.8, 2.2, 4.0, 1.8, 2.2], font_size=10
    )

    # ===================== CHƯƠNG 3 =====================
    sec3 = doc.add_section(WD_SECTION_START.NEW_PAGE)
    setup_page(sec3, header_text='Chương 3. Thiết kế bộ truyền trục vít – bánh vít', show_page_num=True)
    add_h1(doc, 'CHƯƠNG 3. THIẾT KẾ BỘ TRUYỀN TRỤC VÍT – BÁNH VÍT')

    add_h2(doc, '3.1. Thông số ban đầu')
    add_mixed(doc, [
        ('t', 'Công suất trục vít '), ('m', rf'P_1 = {fnum(R["P1"], 3)}\ \text{{kW}}'),
        ('t', '; số vòng quay '), ('m', rf'n_1 = {fnum(R["n1"], 2)}\ \text{{vg/ph}}'),
        ('t', '; mômen xoắn trục vít '), ('m', rf'T_1 = {fnum(R["T1"], 1)}\ \text{{N.mm}}'),
        ('t', '; mômen xoắn bánh vít '), ('m', rf'T_2 = {fnum(R["T2"], 1)}\ \text{{N.mm}}'),
        ('t', '; tỉ số truyền '), ('m', r'u_{tv} = 11{,}5'),
        ('t', ' ('), ('m', r'z_1 = 4,\ z_2 = 46'),
        ('t', '); tổng số giờ làm việc '), ('m', r'L_h = 5 \times 300 \times 2 \times 8 = 24000\ \text{giờ}'), ('t', '.'),
    ])

    add_h2(doc, '3.2. Chọn vật liệu và xác định ứng suất cho phép')
    add_p(doc, 'Dự đoán sơ bộ vận tốc trượt trong vùng ăn khớp theo [2]:')
    add_eq(doc, rf'v_{{s,sb}} = 4{{,}}5 \cdot 10^{{-5}} \cdot n_1 \cdot \sqrt[3]{{T_2}} = 4{{,}}5 \times 10^{{-5}} \times 727{{,}}5 \times \sqrt[3]{{1200835{{,}}7}} = {fnum(R["vs_sb"], 2)}\ \text{{(m/s)}}', '3.1')
    add_p(doc, 'Vì 2 m/s ≤ v_s,sb ≤ 5 m/s, theo Chương 7 [1] và [2] ta chọn vật liệu:')
    add_p(doc, '– Bánh vít: Đồng thanh nhôm sắt (đồng thanh không thiếc) БрАЖ9-4 đúc trong khuôn kim loại, có σ_b = 500 MPa, σ_ch = 200 MPa.', indent=1.0)
    add_p(doc, '– Trục vít: Thép hợp kim 40Cr tôi bề mặt đạt độ rắn HRC 45 ÷ 50, mài và đánh bóng ren đạt độ nhám R_a = 0,63 ÷ 0,32 μm.', indent=1.0)

    add_p(doc, 'Ứng suất tiếp xúc cho phép sơ bộ của bánh vít đồng thanh không thiếc БрАЖ9-4 khi ăn khớp với trục vít tôi HRC ≥ 45 [2]:')
    add_eq(doc, rf'[\sigma_H]_{{sb}} = 300 - 25 v_{{s,sb}} = 300 - 25 \times {fnum(R["vs_sb"], 2)} = {fnum(R["sH_sb"], 2)}\ \text{{(MPa)}}', '3.2')

    add_p(doc, 'Ứng suất uốn cho phép của răng bánh vít (làm việc một chiều):')
    add_eq(doc, rf'N_{{FE}} = 60 n_2 L_h \left[\left(\frac{{T_1}}{{T}}\right)^9 \frac{{t_1}}{{t_1+t_2}} + \left(\frac{{T_2}}{{T}}\right)^9 \frac{{t_2}}{{t_1+t_2}}\right] = 60 \times 63{{,}}26 \times 24000 \left[1^9 \frac{{15}}{{63}} + 0{{,}}5^9 \frac{{48}}{{63}}\right] = 2{{,}}18 \times 10^7\ \text{{chu kỳ}}', '3.3')
    add_eq(doc, rf'K_{{FL}} = \sqrt[9]{{\frac{{10^6}}{{N_{{FE}}}}}} = \sqrt[9]{{\frac{{10^6}}{{2{{,}}18 \times 10^7}}}} = {fnum(R["KFL"], 3)}', '3.4')
    add_eq(doc, rf'[\sigma_F] = (0{{,}}25\sigma_{{ch}} + 0{{,}}08\sigma_b) K_{{FL}} = (0{{,}}25 \times 200 + 0{{,}}08 \times 500) \times {fnum(R["KFL"], 3)} = {fnum(R["sF"], 2)}\ \text{{(MPa)}}', '3.5')

    add_h2(doc, '3.3. Tính toán khoảng cách trục và các thông số hình học')
    add_p(doc, 'Chọn hệ số đường kính trục vít theo tiêu chuẩn q = 10 (thỏa mãn q ≈ (0,25 ÷ 0,3)z₂ = 11,5 ÷ 13,8, chọn tiêu chuẩn gần nhất q = 10 để bộ truyền gọn và tăng góc nâng ren). Hệ số tải trọng K_H = K_v · K_β [1], [2]:')
    add_mixed(doc, [
        ('t', '– Hệ số tập trung tải trọng (với '), ('m', r'\theta = 70,\ T_m/T_{\max} = (1 \times 15 + 0{,}5 \times 48)/63 = 0{,}619'), ('t', '): '),
        ('m', rf'K_\beta = 1 + (z_2/\theta)^3 (1 - T_m/T_{{\max}}) = 1 + (46/70)^3(1 - 0{{,}}619) = {fnum(R["Kb"], 3)}'), ('t', ';'),
    ])
    add_mixed(doc, [
        ('t', '– Hệ số tải trọng động (chọn cấp chính xác 7, '), ('m', r'v_s > 3\ \text{m/s}'), ('t', '): '),
        ('m', r'K_v = 1{,}10'), ('t', ' ⇒ '), ('m', rf'K_H = K_F = K_v \cdot K_\beta = 1{{,}}10 \times {fnum(R["Kb"], 3)} = {fnum(R["KH"], 3)}'), ('t', '.'),
    ])
    add_p(doc, 'Khoảng cách trục sơ bộ theo độ bền tiếp xúc (Chương 7 [1]):')
    add_eq(doc, rf'a_w = \left(1 + \frac{{q}}{{z_2}}\right)\sqrt[3]{{\left(\frac{{170}}{{[\sigma_H]_{{sb}}}}\right)^2 \frac{{T_2 K_H}}{{q/z_2}}}} = \left(1 + \frac{{10}}{{46}}\right)\sqrt[3]{{\left(\frac{{170}}{{{fnum(R["sH_sb"], 2)}}}\right)^2 \frac{{1200835{{,}}7 \times {fnum(R["KH"], 3)}}}{{10/46}}}} = {fnum(R["aw_tt"], 2)}\ \text{{(mm)}}', '3.6')
    add_p(doc, 'Môđun dọc trục vít (bằng môđun ngang bánh vít):')
    add_eq(doc, rf'm = \frac{{2a_w}}{{q + z_2}} = \frac{{2 \times {fnum(R["aw_tt"], 2)}}}{{10 + 46}} = {fnum(R["m_tt"], 2)}\ \text{{(mm)}}', '3.7')
    add_p(doc, 'Chọn môđun tiêu chuẩn (dãy ưu tiên 1): m = 8 mm, hệ số dịch chỉnh x = 0. Khi đó khoảng cách trục chính xác là:')
    add_eq(doc, r'a_w = \frac{m(q + z_2)}{2} = \frac{8 \times (10 + 46)}{2} = 224\ \text{(mm)}', '3.8')

    add_p(doc, 'Các thông số hình học chủ yếu của trục vít và bánh vít (Bảng 7.2 [1]):')
    add_mixed(doc, [('t', '– Đường kính vòng chia trục vít: '), ('m', r'd_1 = m \cdot q = 8 \times 10 = 80\ \text{mm}'), ('t', '; đường kính đỉnh: '), ('m', r'd_{a1} = d_1 + 2m = 96\ \text{mm}'), ('t', '; đường kính đáy: '), ('m', r'd_{f1} = d_1 - 2{,}4m = 60{,}8\ \text{mm}'), ('t', ';')])
    add_mixed(doc, [('t', '– Góc nâng ren trục vít: '), ('m', rf'\gamma = \arctan\left(\frac{{z_1}}{{q}}\right) = \arctan\left(\frac{{4}}{{10}}\right) = {fnum(R["gamma"], 2)}^\circ'), ('t', ';')])
    add_mixed(doc, [('t', '– Chiều dài phần cắt ren trục vít ('), ('m', r'z_1 = 4 \Rightarrow C_1 = 12{,}5,\ C_2 = 0{,}09'), ('t', '): '), ('m', rf'b_1 \ge (12{{,}}5 + 0{{,}}09 \times 46) \times 8 = {fnum(R["b1_tt"], 1)}\ \text{{mm}} \Rightarrow \text{{chọn }} b_1 = 140\ \text{{mm}}'), ('t', ';')])
    add_mixed(doc, [('t', '– Đường kính vòng chia bánh vít: '), ('m', r'd_2 = m \cdot z_2 = 8 \times 46 = 368\ \text{mm}'), ('t', '; đường kính đỉnh: '), ('m', r'd_{a2} = d_2 + 2m = 384\ \text{mm}'), ('t', '; đường kính đáy: '), ('m', r'd_{f2} = d_2 - 2{,}4m = 348{,}8\ \text{mm}'), ('t', ';')])
    add_mixed(doc, [('t', '– Đường kính lớn nhất bánh vít: '), ('m', r'd_{aM2} \le d_{a2} + \frac{6m}{z_1 + 2} = 384 + \frac{48}{6} = 392\ \text{mm}'), ('t', ';')])
    add_mixed(doc, [('t', '– Bề rộng bánh vít ('), ('m', r'z_1 = 4'), ('t', '): '), ('m', r'b_2 \le 0{,}67 d_{a1} = 0{,}67 \times 96 = 64{,}32\ \text{mm} \Rightarrow \text{chọn } b_2 = 64\ \text{mm}'), ('t', '; góc ôm: '), ('m', rf'2\delta = 2\arcsin\left(\frac{{64}}{{96 - 4}}\right) = {fnum(R["delta2"], 1)}^\circ'), ('t', '.')])

    add_h2(doc, '3.4. Kiểm nghiệm vận tốc trượt, hiệu suất và độ bền tiếp xúc')
    add_p(doc, 'Vận tốc trượt thực tế trong vùng ăn khớp:')
    add_eq(doc, rf'v_s = \frac{{\pi d_1 n_1}}{{60000 \cos\gamma}} = \frac{{\pi \times 80 \times 727{{,}}5}}{{60000 \times \cos({fnum(R["gamma"], 2)}^\circ)}} = {fnum(R["vs"], 2)}\ \text{{(m/s)}}', '3.9')
    add_p(doc, 'Giá trị v_s = 3,28 m/s nằm trong khoảng 2 ÷ 5 m/s, phù hợp với vật liệu đồng thanh không thiếc đã chọn. Với v_s = 3,28 m/s, tra góc ma sát thay thế ρ\' ≈ 2,0°, hiệu suất bộ truyền trục vít (có xét tổn hao khuấy dầu):')
    add_eq(doc, rf"\eta_{{tv}} = 0{{,}}95 \frac{{\tan\gamma}}{{\tan(\gamma + \rho')}} = 0{{,}}95 \frac{{\tan 21{{,}}80^\circ}}{{\tan(21{{,}}80^\circ + 2{{,}}0^\circ)}} = {fnum(R['eta_tv_tt'], 3)} \approx 0{{,}}85\ \text{{(phù hợp sơ bộ)}}", '3.10')
    add_p(doc, 'Ứng suất tiếp xúc cho phép chính xác theo v_s = 3,28 m/s:')
    add_eq(doc, rf'[\sigma_H] = 300 - 25 v_s = 300 - 25 \times {fnum(R["vs"], 2)} = {fnum(R["sH_cp"], 2)}\ \text{{(MPa)}}', '3.11')
    add_p(doc, 'Kiểm nghiệm ứng suất tiếp xúc trên mặt răng bánh vít (Chương 7 [1]):')
    add_eq(doc, rf'\sigma_H = \frac{{480}}{{d_2}}\sqrt{{\frac{{K_H T_2}}{{d_1}}}} = \frac{{480}}{{368}}\sqrt{{\frac{{{fnum(R["KH"], 3)} \times 1200835{{,}}7}}{{80}}}} = {fnum(R["sH"], 2)}\ \text{{(MPa)}} \le [\sigma_H] = {fnum(R["sH_cp"], 2)}\ \text{{(MPa)}}', '3.12')
    add_p(doc, 'Kết luận: Bộ truyền trục vít – bánh vít thỏa mãn điều kiện bền tiếp xúc.')

    add_h2(doc, '3.5. Kiểm nghiệm độ bền uốn răng bánh vít')
    add_p(doc, 'Số răng tương đương của bánh vít:')
    add_eq(doc, rf'z_v = \frac{{z_2}}{{\cos^3\gamma}} = \frac{{46}}{{\cos^3(21{{,}}80^\circ)}} = {fnum(R["zv"], 2)}', '3.13')
    add_p(doc, 'Tra hệ số dạng răng theo z_v = 57,47 (Bảng 7.8 [2]): Y_F = 1,413. Kiểm nghiệm ứng suất uốn tại chân răng bánh vít:')
    add_eq(doc, rf'\sigma_F = \frac{{1{{,}}5 Y_F K_F T_2}}{{z_2 q m^3}} = \frac{{1{{,}}5 \times 1{{,}}413 \times {fnum(R["KF"], 3)} \times 1200835{{,}}7}}{{46 \times 10 \times 8^3}} = {fnum(R["sF_tt"], 2)}\ \text{{(MPa)}} \le [\sigma_F] = {fnum(R["sF"], 2)}\ \text{{(MPa)}}', '3.14')
    add_p(doc, 'Kết luận: Răng bánh vít hoàn toàn thỏa mãn điều kiện bền uốn.')

    add_h2(doc, '3.6. Xác định các lực ăn khớp')
    add_p(doc, 'Các lực tác dụng lên trục vít và bánh vít được xác định theo Chương 7 [1]:')
    add_eq(doc, rf'F_{{t1}} = F_{{a2}} = \frac{{2 T_1}}{{d_1}} = \frac{{2 \times 124088{{,}}5}}{{80}} = {fnum(R["Ft1"], 1)}\ \text{{(N)}}', '3.15')
    add_eq(doc, rf'F_{{a1}} = F_{{t2}} = \frac{{2 T_2}}{{d_2}} = \frac{{2 \times 1200835{{,}}7}}{{368}} = {fnum(R["Fa1"], 1)}\ \text{{(N)}}', '3.16')
    add_eq(doc, rf'F_{{r1}} = F_{{r2}} = F_{{t2}} \tan\alpha = {fnum(R["Ft2"], 1)} \times \tan 20^\circ = {fnum(R["Fr1"], 1)}\ \text{{(N)}}', '3.17')

    add_h2(doc, '3.7. Kiểm nghiệm độ cứng trục vít')
    add_p(doc, 'Khoảng cách giữa hai gối đỡ trục vít l = 360 mm (xấp xỉ d₂ = 368 mm). Mômen quán tính tương đương của tiết diện trục vít [2]:')
    add_eq(doc, rf'J_e = \frac{{\pi d_{{f1}}^4}}{{64}}\left(0{{,}}375 + 0{{,}}625\frac{{d_{{a1}}}}{{d_{{f1}}}}\right) = \frac{{\pi \times 60{{,}}8^4}}{{64}}\left(0{{,}}375 + 0{{,}}625 \times \frac{{96}}{{60{{,}}8}}\right) = {fnum(R["Je"], 0)}\ \text{{(mm}}^4\text{{)}}', '3.18')
    add_p(doc, 'Độ võng của trục vít tại vị trí ăn khớp (với E = 2,1×10⁵ MPa):')
    add_eq(doc, rf'f = \frac{{l^3 \sqrt{{F_{{t1}}^2 + F_{{r1}}^2}}}}{{48 E J_e}} = \frac{{360^3 \sqrt{{{fnum(R["Ft1"], 1)}^2 + {fnum(R["Fr1"], 1)}^2}}}}{{48 \times 2{{,}}1 \times 10^5 \times {fnum(R["Je"], 0)}}} = {fnum(R["f_tv"], 3)}\ \text{{(mm)}} \le [f] = (0{{,}}005 \div 0{{,}}01)m = 0{{,}}04 \div 0{{,}}08\ \text{{(mm)}}', '3.19')
    add_p(doc, 'Kết luận: Trục vít hoàn toàn thỏa mãn điều kiện độ cứng.')

    add_h2(doc, '3.8. Tính nhiệt và chọn dầu bôi trơn')
    add_p(doc, 'Diện tích bề mặt thoát nhiệt gần đúng của vỏ hộp giảm tốc trục vít (với a_w = 0,224 m) [2]:')
    add_eq(doc, rf'A = 20 a_w^{{1{{,}}7}} = 20 \times 0{{,}}224^{{1{{,}}7}} = {fnum(R["At"], 3)}\ \text{{(m}}^2\text{{)}}', '3.20')
    add_p(doc, 'Chọn hệ số tỏa nhiệt K_T = 13 W/(m²·°C), hệ số kể đến thoát nhiệt qua đáy hộp xuống bệ máy ψ = 0,25, nhiệt độ môi trường t₀ = 25 °C. Nhiệt độ dầu bôi trơn làm việc ổn định (Chương 7 [1]):')
    add_eq(doc, rf't_1 = t_0 + \frac{{1000 P_1 (1 - \eta_{{tv}})}}{{K_T A (1 + \psi)}} = 25 + \frac{{1000 \times {fnum(R["P1"], 3)} \times (1 - {fnum(R["eta_tv_tt"], 3)})}}{{13 \times {fnum(R["At"], 3)} \times (1 + 0{{,}}25)}} = {fnum(R["tdau"], 1)}^\circ\text{{C}} \le [t_1] = 90^\circ\text{{C}}', '3.21')
    add_p(doc, 'Nhiệt độ dầu nằm trong giới hạn cho phép, không cần làm mát cưỡng bức (chỉ cần gân tản nhiệt đúc liền vỏ hộp). Với v_s = 3,28 m/s và trục vít nằm trên bánh vít, chọn phương pháp bôi trơn ngâm dầu (bánh vít nhúng sâu vào dầu, mang dầu lên bôi trơn vùng ăn khớp), sử dụng dầu công nghiệp ISO VG 220 (độ nhớt động học ở 40 °C là 220 cSt).')

    add_h2(doc, '3.9. Tổng hợp thông số bộ truyền trục vít – bánh vít')
    add_table(doc,
        ['Thông số', 'Ký hiệu', 'Giá trị', 'Thông số', 'Ký hiệu', 'Giá trị'],
        [
            ['Khoảng cách trục', 'a_w', '224 mm', 'Số mối ren / số răng', 'z₁ / z₂', '4 / 46'],
            ['Môđun tiêu chuẩn', 'm', '8 mm', 'Hệ số đường kính', 'q', '10'],
            ['Góc nâng ren trục vít', 'γ', f'{fnum(R["gamma"], 2)}°', 'Vận tốc trượt thực', 'v_s', f'{fnum(R["vs"], 2)} m/s'],
            ['Đường kính chia TV / BV', 'd₁ / d₂', '80 / 368 mm', 'Hiệu suất thực tế', 'η_tv', f'{fnum(R["eta_tv_tt"], 3)}'],
            ['Đường kính đỉnh TV / BV', 'd_a1 / d_a2', '96 / 384 mm', 'Ứng suất tiếp xúc', 'σ_H / [σ_H]', f'{fnum(R["sH"], 1)} / {fnum(R["sH_cp"], 1)} MPa'],
            ['Đường kính đáy TV / BV', 'd_f1 / d_f2', '60,8 / 348,8 mm', 'Ứng suất uốn', 'σ_F / [σ_F]', f'{fnum(R["sF_tt"], 1)} / {fnum(R["sF"], 1)} MPa'],
            ['Chiều dài ren / bề rộng BV', 'b₁ / b₂', '140 / 64 mm', 'Lực ăn khớp F_t1 / F_a1 / F_r1', '—', f'{fnum(R["Ft1"], 0)} / {fnum(R["Fa1"], 0)} / {fnum(R["Fr1"], 0)} N'],
        ],
        caption='Bảng 3.1. Bảng tổng hợp thông số bộ truyền trục vít – bánh vít',
        col_widths=[4.2, 1.8, 2.0, 4.0, 1.8, 2.2], font_size=9.5
    )

    # ===================== CHƯƠNG 4 =====================
    sec4 = doc.add_section(WD_SECTION_START.NEW_PAGE)
    setup_page(sec4, header_text='Chương 4. Thiết kế hai trục trong hộp giảm tốc và tính chọn then', show_page_num=True)
    add_h1(doc, 'CHƯƠNG 4. THIẾT KẾ HAI TRỤC TRONG HỘP GIẢM TỐC VÀ TÍNH CHỌN THEN')

    add_h2(doc, '4.1. Chọn vật liệu và xác định khoảng cách gối đỡ')
    add_p(doc, '– Trục I (trục vít chế tạo liền trục): Thép hợp kim 40Cr tôi cải thiện (phần ren tôi bề mặt HRC 45 ÷ 50), có giới hạn bền σ_b = 850 MPa, ứng suất uốn cho phép [σ] = 55 MPa [1], [2].')
    add_p(doc, '– Trục II (trục bánh vít): Thép 45 thường hóa, có giới hạn bền σ_b = 600 MPa, ứng suất uốn cho phép [σ] = 50 MPa [1], [2].')
    add_p(doc, 'Căn cứ vào chiều rộng bánh đai B = 63 mm, chiều dài cắt ren b₁ = 140 mm, bề rộng bánh vít b₂ = 64 mm, chiều dài mayơ bánh vít l_m2 = 110 mm, chiều dài mayơ nối trục l = 140 mm và chiều rộng sơ bộ ổ lăn, ta chọn kích thước chiều dài dọc trục như sau:')
    add_p(doc, '– Trục I: khoảng cách từ tâm bánh đai đến ổ A là l₁₁ = 75 mm; từ ổ A đến giữa trục vít là l₁₂ = 180 mm; từ giữa trục vít đến ổ B là l₁₃ = 180 mm (tổng khoảng cách giữa hai ổ l = 360 mm, phù hợp phần kiểm nghiệm độ cứng Chương 3).', indent=1.0)
    add_p(doc, '– Trục II: khoảng cách từ ổ C đến giữa bánh vít là l₂₁ = 85 mm; từ giữa bánh vít đến ổ D là l₂₂ = 85 mm; từ ổ D đến giữa nối trục đàn hồi là l₂₃ = 110 mm.', indent=1.0)

    add_h2(doc, '4.2. Thiết kế Trục I (Trục vít)')
    add_h3(doc, '4.2.1. Sơ đồ đặt lực và tính phản lực gối tựa')
    add_p(doc, 'Trục vít nằm trên bánh vít, lực hướng tâm F_r1 = 2375,4 N hướng thẳng đứng lên trên (+y); lực dọc trục F_a1 = 6526,3 N gây ra mômen uốn tập trung trong mặt phẳng đứng:')
    add_eq(doc, rf'M_{{a1}} = F_{{a1}} \frac{{d_1}}{{2}} = 6526{{,}}3 \times \frac{{80}}{{2}} = {fnum(R["Ma1"], 1)}\ \text{{(N.mm)}}', '4.1')
    add_p(doc, 'Trong mặt phẳng ngang (Oxz), lực căng đai F_rđ = 1831,7 N và lực vòng F_t1 = 3102,2 N đặt tại tiết diện bánh đai (x = 0) và tiết diện trục vít (x = 255 mm). Sơ đồ đặt lực thể hiện trên Hình 4.1.')
    add_figure(doc, 'SoDoLuc_TrucI.png', 'Hình 4.1. Sơ đồ đặt lực và phản lực gối tựa Trục I (Trục vít)', width_cm=15.0)

    add_p(doc, 'Viết phương trình cân bằng tĩnh học trong mặt phẳng đứng (Oxy):')
    add_eq(doc, rf'\sum M_A = F_{{r1}} \cdot 180 + M_{{a1}} + R_{{By}} \cdot 360 = 0 \Rightarrow R_{{By}} = \frac{{-(2375{{,}}4 \times 180 + 261051{{,}}2)}}{{360}} = {fnum(R["RBy"], 2)}\ \text{{(N)}}', '4.2')
    add_eq(doc, rf'\sum F_y = R_{{Ay}} + F_{{r1}} + R_{{By}} = 0 \Rightarrow R_{{Ay}} = -2375{{,}}4 - ({fnum(R["RBy"], 2)}) = {fnum(R["RAy"], 2)}\ \text{{(N)}}', '4.3')
    add_p(doc, 'Phương trình cân bằng trong mặt phẳng ngang (Oxz):')
    add_eq(doc, rf'\sum M_A = -F_{{r\text{{đ}}}} \cdot 75 + F_{{t1}} \cdot 180 + R_{{Bx}} \cdot 360 = 0 \Rightarrow R_{{Bx}} = \frac{{1831{{,}}7 \times 75 - 3102{{,}}2 \times 180}}{{360}} = {fnum(R["RBx"], 2)}\ \text{{(N)}}', '4.4')
    add_eq(doc, rf'\sum F_x = F_{{r\text{{đ}}}} + R_{{Ax}} + F_{{t1}} + R_{{Bx}} = 0 \Rightarrow R_{{Ax}} = {fnum(R["RAx"], 2)}\ \text{{(N)}}', '4.5')

    add_h3(doc, '4.2.2. Biểu đồ mômen uốn và mômen xoắn Trục I (vẽ bằng MATLAB)')
    add_p(doc, 'Sử dụng chương trình MATLAB (trình bày tại Mục 4.4), ta thu được biểu đồ mômen uốn trong mặt phẳng đứng M_x, mặt phẳng ngang M_y và mômen xoắn T của Trục I như Hình 4.2.')
    add_figure(doc, 'BieuDoMoment_TrucI.png', 'Hình 4.2. Biểu đồ mômen uốn Mx, My và mômen xoắn T của Trục I (vẽ bằng MATLAB)', width_cm=14.8)

    add_h3(doc, '4.2.3. Tính mômen tương đương và chọn đường kính các đoạn Trục I')
    add_p(doc, 'Mômen tương đương và đường kính tối thiểu tại từng tiết diện được tính theo thuyết bền thế năng biến đổi hình dáng [1]:')
    add_eq(doc, r'M_{td} = \sqrt{M_x^2 + M_y^2 + 0{,}75 T^2};\qquad d \ge \sqrt[3]{\frac{M_{td}}{0{,}1[\sigma]}}', '4.6')
    s1 = R['sec1']
    add_table(doc,
        ['Tiết diện', 'Vị trí', 'M_x (N.mm)', 'M_y (N.mm)', 'T (N.mm)', 'M_td (N.mm)', 'd_min (mm)', 'd chọn (mm)'],
        [
            ['1-0', 'Bánh đai', '0', '0', fnum(s1['1-0']['T'], 0), fnum(s1['1-0']['Mtd'], 0), fnum(s1['1-0']['dmin'], 2), '40'],
            ['1-1', 'Ổ lăn A', '0', fnum(s1['1-1']['My'], 0), fnum(s1['1-1']['T'], 0), fnum(s1['1-1']['Mtd'], 0), fnum(s1['1-1']['dmin'], 2), '50'],
            ['1-2', 'Trục vít', fnum(s1['1-2']['Mx'], 0), fnum(s1['1-2']['My'], 0), fnum(s1['1-2']['T'], 0), fnum(s1['1-2']['Mtd'], 0), fnum(s1['1-2']['dmin'], 2), 'd_f1 = 60,8'],
            ['1-3', 'Ổ lăn B', '0', '0', '0', '0', '0', '50'],
        ],
        caption='Bảng 4.1. Mômen tương đương và đường kính tối thiểu tại các tiết diện Trục I',
        col_widths=[1.6, 2.0, 2.0, 2.0, 2.0, 2.2, 2.0, 2.2], font_size=9.5
    )
    add_p(doc, 'Đường kính lắp ổ lăn A và B chọn đồng nhất theo tiêu chuẩn ổ lăn d_11 = d_13 = 50 mm; đầu trục lắp bánh đai chọn d_10 = 40 mm (có vai trục định vị bánh đai); tại phần cắt ren trục vít có đường kính chân ren d_f1 = 60,8 mm > d_min = 42,35 mm (đảm bảo bền và dễ lắp ổ).')

    add_h3(doc, '4.2.4. Tính chọn và kiểm nghiệm then bằng trên Trục I')
    k0 = R['keys'][0]
    add_p(doc, 'Trên Trục I chỉ có một mối ghép then bằng tại tiết diện lắp bánh đai (d = 40 mm; trục vít chế tạo liền trục). Chọn vật liệu then là thép 45 có ứng suất dập cho phép [σ_d] = 100 MPa, ứng suất cắt cho phép [τ_c] = 60 MPa. Theo TCVN 2261–77, chọn then bằng hai đầu tròn: b = 12 mm, h = 8 mm, t₁ = 5,0 mm, t₂ = 3,3 mm, chiều dài then L = 56 mm (chiều dài làm việc l₁ = L − b = 44 mm). Kiểm nghiệm bền dập và bền cắt:')
    add_eq(doc, rf'\sigma_d = \frac{{2 T_1}}{{d \cdot l_1 (h - t_1)}} = \frac{{2 \times 124088{{,}}5}}{{40 \times 44 \times (8 - 5)}} = {fnum(k0["sd"], 2)}\ \text{{(MPa)}} < [\sigma_d] = 100\ \text{{(MPa)}}', '4.7')
    add_eq(doc, rf'\tau_c = \frac{{2 T_1}}{{d \cdot l_1 \cdot b}} = \frac{{2 \times 124088{{,}}5}}{{40 \times 44 \times 12}} = {fnum(k0["tc"], 2)}\ \text{{(MPa)}} < [\tau_c] = 60\ \text{{(MPa)}}', '4.8')

    add_h3(doc, '4.2.5. Kiểm nghiệm độ bền mỏi Trục I và vẽ kết cấu trục')
    add_p(doc, 'Kiểm nghiệm hệ số an toàn mỏi tại các tiết diện nguy hiểm theo công thức Chương 8 [1]:')
    add_eq(doc, r's = \frac{s_\sigma \cdot s_\tau}{\sqrt{s_\sigma^2 + s_\tau^2}} \ge [s] = 1{,}5 \div 2{,}5;\quad s_\sigma = \frac{\sigma_{-1}}{\frac{K_\sigma \sigma_a}{\varepsilon_\sigma \beta} + \psi_\sigma \sigma_m};\quad s_\tau = \frac{\tau_{-1}}{\frac{K_\tau \tau_a}{\varepsilon_\tau \beta} + \psi_\tau \tau_m}', '4.9')
    add_p(doc, 'Với thép 40Cr (σ_b = 850 MPa): σ_-1 = 0,436·σ_b = 370,6 MPa, τ_-1 = 0,22·σ_b = 187,0 MPa, ψ_σ = 0,05, ψ_τ = 0, β = 0,8. Vì trục quay một chiều nên σ_m = 0, σ_a = M/W_x, τ_a = τ_m = T/(2W_o). Kết quả kiểm nghiệm các tiết diện Trục I được tổng hợp ở Bảng 4.2.')
    rows_f1 = []
    for r in R['fat1']['rows']:
        if r['skip']:
            rows_f1.append([r['sec'], fnum(r['d'], 1), '0', '0', '—', '—', '—', '—', '—'])
        else:
            ss_s = '∞' if r['ss'] > 1e5 else fnum(r['ss'], 2)
            rows_f1.append([r['sec'], fnum(r['d'], 1), fnum(r['M'], 0), fnum(r['T'], 0),
                            fnum(r['sa'], 2), fnum(r['tmax'], 2), ss_s, fnum(r['st'], 2), fnum(r['s'], 2)])
    add_table(doc,
        ['Tiết diện', 'd (mm)', 'M (N.mm)', 'T (N.mm)', 'σ_max (MPa)', 'τ_max (MPa)', 's_σ', 's_τ', 's'],
        rows_f1,
        caption='Bảng 4.2. Kết quả kiểm nghiệm độ bền mỏi các tiết diện Trục I',
        col_widths=[1.6, 1.5, 2.0, 2.0, 2.0, 2.0, 1.6, 1.6, 1.7], font_size=9.5
    )
    add_p(doc, 'Tại mọi tiết diện, hệ số an toàn s ≥ 6,19 > [s] = 1,5 ÷ 2,5 → Trục I hoàn toàn đủ bền mỏi. Bản vẽ kết cấu Trục I thể hiện trên Hình 4.3.')
    add_figure(doc, 'KetCau_TrucI.png', 'Hình 4.3. Bản vẽ kết cấu Trục I (Trục vít liền trục)', width_cm=15.0)

    # ---- 4.3 Trục II ----
    add_h2(doc, '4.3. Thiết kế Trục II (Trục bánh vít)')
    add_h3(doc, '4.3.1. Sơ đồ đặt lực và tính phản lực gối tựa')
    add_p(doc, 'Các lực từ bánh vít tác dụng lên Trục II gồm: F_t2 = 6526,3 N, F_r2 = 2375,4 N (hướng xuống −y), F_a2 = 3102,2 N gây mômen uốn tập trung trong mặt phẳng đứng:')
    add_eq(doc, rf'M_{{a2}} = F_{{a2}} \frac{{d_2}}{{2}} = 3102{{,}}2 \times \frac{{368}}{{2}} = {fnum(R["Ma2"], 1)}\ \text{{(N.mm)}}', '4.10')
    add_p(doc, 'Tại đầu ra lắp nối trục vòng đàn hồi (chọn ở Chương 5 có đường kính vòng tròn qua tâm chốt D₀ = 200 mm), lực vòng tại chốt và lực hướng tâm phụ do nối trục tác dụng lên trục (lấy ngược chiều F_t2 theo chiều nguy hiểm nhất):')
    add_eq(doc, rf'F_{{tk}} = \frac{{2 T_2}}{{D_0}} = \frac{{2 \times 1200835{{,}}7}}{{200}} = {fnum(R["Ftk"], 1)}\ \text{{(N)}};\quad F_k = 0{{,}}25 F_{{tk}} = {fnum(R["Fk"], 1)}\ \text{{(N)}}', '4.11')
    add_figure(doc, 'SoDoLuc_TrucII.png', 'Hình 4.4. Sơ đồ đặt lực và phản lực gối tựa Trục II (Trục bánh vít)', width_cm=15.0)

    add_p(doc, 'Giải các phương trình cân bằng tĩnh học cho Trục II:')
    add_eq(doc, rf'\sum M_C = -F_{{r2}} \cdot 85 + M_{{a2}} + R_{{Dy}} \cdot 170 = 0 \Rightarrow R_{{Dy}} = {fnum(R["RDy"], 2)}\ \text{{(N)}};\quad R_{{Cy}} = {fnum(R["RCy"], 2)}\ \text{{(N)}}', '4.12')
    add_eq(doc, rf'\sum M_C = -F_{{t2}} \cdot 85 + F_k \cdot 280 + R_{{Dx}} \cdot 170 = 0 \Rightarrow R_{{Dx}} = {fnum(R["RDx"], 2)}\ \text{{(N)}};\quad R_{{Cx}} = {fnum(R["RCx"], 2)}\ \text{{(N)}}', '4.13')

    add_h3(doc, '4.3.2. Biểu đồ mômen uốn và mômen xoắn Trục II (vẽ bằng MATLAB)')
    add_figure(doc, 'BieuDoMoment_TrucII.png', 'Hình 4.5. Biểu đồ mômen uốn Mx, My và mômen xoắn T của Trục II (vẽ bằng MATLAB)', width_cm=14.8)

    add_h3(doc, '4.3.3. Tính mômen tương đương và chọn đường kính các đoạn Trục II')
    s2 = R['sec2']
    add_table(doc,
        ['Tiết diện', 'Vị trí', 'M_x (N.mm)', 'M_y (N.mm)', 'T (N.mm)', 'M_td (N.mm)', 'd_min (mm)', 'd chọn (mm)'],
        [
            ['2-0', 'Ổ lăn C', '0', '0', '0', '0', '0', '65'],
            ['2-1', 'Bánh vít', fnum(s2['2-1']['Mx'], 0), fnum(s2['2-1']['My'], 0), fnum(s2['2-1']['T'], 0), fnum(s2['2-1']['Mtd'], 0), fnum(s2['2-1']['dmin'], 2), '70'],
            ['2-2', 'Ổ lăn D', '0', fnum(s2['2-2']['My'], 0), fnum(s2['2-2']['T'], 0), fnum(s2['2-2']['Mtd'], 0), fnum(s2['2-2']['dmin'], 2), '65'],
            ['2-3', 'Nối trục', '0', '0', fnum(s2['2-3']['T'], 0), fnum(s2['2-3']['Mtd'], 0), fnum(s2['2-3']['dmin'], 2), '63'],
        ],
        caption='Bảng 4.3. Mômen tương đương và đường kính tối thiểu tại các tiết diện Trục II',
        col_widths=[1.6, 2.0, 2.0, 2.0, 2.1, 2.2, 2.0, 2.1], font_size=9.5
    )

    add_h3(doc, '4.3.4. Tính chọn và kiểm nghiệm then bằng trên Trục II')
    k1, k2 = R['keys'][1], R['keys'][2]
    add_p(doc, 'Chọn vật liệu then là thép 45 ([σ_d] = 100 MPa, [τ_c] = 60 MPa), kích thước tra theo TCVN 2261–77:')
    add_p(doc, f'1) Then tại vị trí lắp bánh vít (d = 70 mm): b = 20 mm, h = 12 mm, t₁ = 7,5 mm, t₂ = 4,9 mm, L = 100 mm, l₁ = 80 mm:', indent=1.0)
    add_eq(doc, rf'\sigma_d = \frac{{2 \times 1200835{{,}}7}}{{70 \times 80 \times (12 - 7{{,}}5)}} = {fnum(k1["sd"], 2)}\ \text{{MPa}} < 100\ \text{{MPa}};\quad \tau_c = \frac{{2 \times 1200835{{,}}7}}{{70 \times 80 \times 20}} = {fnum(k1["tc"], 2)}\ \text{{MPa}} < 60\ \text{{MPa}}', '4.14')
    add_p(doc, f'2) Then tại vị trí lắp nối trục đàn hồi (d = 63 mm): b = 18 mm, h = 11 mm, t₁ = 7,0 mm, t₂ = 4,4 mm, L = 125 mm, l₁ = 107 mm:', indent=1.0)
    add_eq(doc, rf'\sigma_d = \frac{{2 \times 1200835{{,}}7}}{{63 \times 107 \times (11 - 7)}} = {fnum(k2["sd"], 2)}\ \text{{MPa}} < 100\ \text{{MPa}};\quad \tau_c = \frac{{2 \times 1200835{{,}}7}}{{63 \times 107 \times 18}} = {fnum(k2["tc"], 2)}\ \text{{MPa}} < 60\ \text{{MPa}}', '4.15')

    add_h3(doc, '4.3.5. Kiểm nghiệm độ bền mỏi Trục II và vẽ kết cấu trục')
    add_p(doc, 'Với thép 45 (σ_b = 600 MPa): σ_-1 = 261,6 MPa, τ_-1 = 132,0 MPa, ψ_σ = 0,05, ψ_τ = 0, β = 0,8. Kết quả kiểm nghiệm mỏi các tiết diện Trục II trình bày trong Bảng 4.4.')
    rows_f2 = []
    for r in R['fat2']['rows']:
        if r['skip']:
            rows_f2.append([r['sec'], fnum(r['d'], 1), '0', '0', '—', '—', '—', '—', '—'])
        else:
            ss_s = '∞' if r['ss'] > 1e5 else fnum(r['ss'], 2)
            rows_f2.append([r['sec'], fnum(r['d'], 1), fnum(r['M'], 0), fnum(r['T'], 0),
                            fnum(r['sa'], 2), fnum(r['tmax'], 2), ss_s, fnum(r['st'], 2), fnum(r['s'], 2)])
    add_table(doc,
        ['Tiết diện', 'd (mm)', 'M (N.mm)', 'T (N.mm)', 'σ_max (MPa)', 'τ_max (MPa)', 's_σ', 's_τ', 's'],
        rows_f2,
        caption='Bảng 4.4. Kết quả kiểm nghiệm độ bền mỏi các tiết diện Trục II',
        col_widths=[1.6, 1.5, 2.0, 2.0, 2.0, 2.0, 1.6, 1.6, 1.7], font_size=9.5
    )
    add_p(doc, 'Tại mọi tiết diện, hệ số an toàn s ≥ 3,49 > [s] = 1,5 ÷ 2,5 → Trục II hoàn toàn đủ bền mỏi. Bản vẽ kết cấu Trục II thể hiện trên Hình 4.6.')
    add_figure(doc, 'KetCau_TrucII.png', 'Hình 4.6. Bản vẽ kết cấu Trục II (Trục bánh vít)', width_cm=15.0)

    add_h2(doc, '4.4. Chương trình MATLAB vẽ biểu đồ mômen hai trục')
    add_p(doc, 'Mã nguồn MATLAB (file BieuDoMoment_De5_PA4.m) giải phản lực gối tựa, tính mômen tương đương, đường kính tối thiểu và vẽ biểu đồ mômen uốn M_x, M_y, mômen xoắn T cho cả hai trục (xuất ảnh 300 DPI):')
    code_txt = open(MATLAB_FILE, 'r', encoding='utf-8').read()
    # Add code block in a single-cell shaded box
    tbl_c = doc.add_table(rows=1, cols=1)
    tbl_c.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl_c.rows[0].cells[0]
    cell.width = Cm(16.0)
    cell._tc.get_or_add_tcPr().append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="F4F6F9"/>'))
    tbl_c._tbl.tblPr.append(parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        '<w:top w:val="single" w:sz="4" w:color="BFBFBF"/><w:bottom w:val="single" w:sz="4" w:color="BFBFBF"/>'
        '<w:left w:val="single" w:sz="12" w:color="1F4E79"/><w:right w:val="single" w:sz="4" w:color="BFBFBF"/>'
        '</w:tblBorders>'
    ))
    pc = cell.paragraphs[0]
    pc.alignment = WD_ALIGN_PARAGRAPH.LEFT
    pc.paragraph_format.first_line_indent = Cm(0)
    pc.paragraph_format.line_spacing = 1.05
    pc.paragraph_format.space_before = Pt(3)
    pc.paragraph_format.space_after = Pt(3)
    rc = pc.add_run(code_txt)
    rc.font.name = 'Consolas'
    rc.font.size = Pt(8.5)

    # ===================== CHƯƠNG 5 =====================
    sec5 = doc.add_section(WD_SECTION_START.NEW_PAGE)
    setup_page(sec5, header_text='Chương 5. Tính chọn ổ lăn và nối trục vòng đàn hồi', show_page_num=True)
    add_h1(doc, 'CHƯƠNG 5. TÍNH CHỌN Ổ LĂN VÀ NỐI TRỤC VÒNG ĐÀN HỒI')

    add_h2(doc, '5.1. Tính chọn cặp ổ lăn cho Trục I')
    b1 = R['b1']
    add_p(doc, 'Tổng lực hướng tâm tác dụng lên ổ A và ổ B của Trục I:')
    add_eq(doc, rf'F_{{rA}} = \sqrt{{R_{{Ax}}^2 + R_{{Ay}}^2}} = \sqrt{{({fnum(R["RAx"], 2)})^2 + ({fnum(R["RAy"], 2)})^2}} = {fnum(R["FrA"], 1)}\ \text{{(N)}}', '5.1')
    add_eq(doc, rf'F_{{rB}} = \sqrt{{R_{{Bx}}^2 + R_{{By}}^2}} = \sqrt{{({fnum(R["RBx"], 2)})^2 + ({fnum(R["RBy"], 2)})^2}} = {fnum(R["FrB"], 1)}\ \text{{(N)}}', '5.2')
    add_mixed(doc, [
        ('t', 'Tỉ số lực dọc trục trên lực hướng tâm: '),
        ('m', rf'F_{{a1}} / F_{{rB}} = 6526{{,}}3 / {fnum(R["FrB"], 1)} = {fnum(R["Fa1"]/R["FrB"], 2)} \gg 0{{,}}3'),
        ('t', '. Vì trục vít chịu lực dọc trục rất lớn, ta chọn cặp '),
        ('t', 'ổ đũa côn một dãy', True),
        ('t', ' (ký hiệu '), ('t', '7310', True), ('t', ', đường kính trong d = 50 mm, lắp đối nhau kiểu chữ "O" để tăng độ cứng vững cho trục vít). Thông số ổ 7310 (Bảng P2.11 [2]):'),
    ])
    add_table(doc,
        ['Ký hiệu ổ', 'd (mm)', 'D (mm)', 'T (mm)', 'α (độ)', 'e = 1,5 tan α', 'C (kN)', 'C₀ (kN)'],
        [['7310', '50', '110', '29,25', '12,95°', fnum(b1['e'], 3), '96,6', '75,9']],
        caption='Bảng 5.1. Thông số ổ đũa côn một dãy 7310 lắp trên Trục I [2]',
        col_widths=[2.0, 1.6, 1.8, 1.8, 2.0, 2.6, 2.1, 2.1], font_size=10
    )
    add_p(doc, 'Lực dọc trục phụ do lực hướng tâm sinh ra trên hai ổ đũa côn:')
    add_eq(doc, rf'S_A = 0{{,}}83 e F_{{rA}} = 0{{,}}83 \times {fnum(b1["e"], 3)} \times {fnum(R["FrA"], 1)} = {fnum(b1["SL"], 1)}\ \text{{(N)}};\quad S_B = 0{{,}}83 e F_{{rB}} = {fnum(b1["SR"], 1)}\ \text{{(N)}}', '5.3')
    add_p(doc, 'Lực dọc trục F_a1 = 6526,3 N hướng về ổ B. Tổng lực dọc trục tác dụng lên từng ổ:')
    add_eq(doc, rf'\sum F_{{aA}} = \max(S_B - F_{{a1}},\ S_A) = {fnum(b1["FaL_used"], 1)}\ \text{{(N)}};\quad \sum F_{{aB}} = \max(S_A + F_{{a1}},\ S_B) = {fnum(b1["FaR_used"], 1)}\ \text{{(N)}}', '5.4')
    add_p(doc, 'Chọn vòng trong quay V = 1, hệ số tải trọng động K_σ = 1,1 (va đập nhẹ), hệ số nhiệt độ K_t = 1,0. Xác định tải trọng động quy đổi trên từng ổ (với Y = 0,4 / tan α = 1,74):')
    add_mixed(doc, [('t', '– Ổ A: '), ('m', rf'\sum F_{{aA}} / (V F_{{rA}}) = {fnum(b1["L"]["ratio"], 3)} \le e \Rightarrow X = 1,\ Y = 0 \Rightarrow Q_A = 1 \times {fnum(R["FrA"], 1)} \times 1{{,}}1 = {fnum(b1["L"]["Q"], 1)}\ \text{{(N)}}'), ('t', ';')])
    add_mixed(doc, [('t', '– Ổ B: '), ('m', rf'\sum F_{{aB}} / (V F_{{rB}}) = {fnum(b1["R"]["ratio"], 2)} > e \Rightarrow X = 0{{,}}4,\ Y = 1{{,}}74 \Rightarrow Q_B = (0{{,}}4 \times {fnum(R["FrB"], 1)} + 1{{,}}74 \times {fnum(b1["FaR_used"], 1)}) \times 1{{,}}1 = {fnum(b1["R"]["Q"], 1)}\ \text{{(N)}}'), ('t', '.')])
    add_p(doc, 'Vì Q_B > Q_A nên ta tính khả năng tải cho ổ B (ổ đũa có bậc đường cong mỏi m = 10/3). Tải trọng tương đương theo chế độ tải bậc:')
    add_eq(doc, rf'Q_E = Q_B \sqrt[10/3]{{1^{{10/3}}\frac{{15}}{{63}} + 0{{,}}5^{{10/3}}\frac{{48}}{{63}}}} = {fnum(R["fac_life"], 3)} \times {fnum(b1["R"]["Q"], 1)} = {fnum(b1["QE"], 1)}\ \text{{(N)}}', '5.5')
    add_p(doc, 'Tuổi thọ quy đổi và khả năng tải động tính toán:')
    add_eq(doc, rf'L = \frac{{60 n_1 L_h}}{{10^6}} = \frac{{60 \times 727{{,}}5 \times 24000}}{{10^6}} = {fnum(b1["Lm"], 1)}\ \text{{(triệu vòng)}}', '5.6')
    add_eq(doc, rf'C_{{tt}} = Q_E \cdot L^{{3/10}} = {fnum(b1["QE"]/1000, 2)} \times {fnum(b1["Lm"], 1)}^{{0{{,}}3}} = {fnum(b1["Ctt"], 2)}\ \text{{(kN)}} < C = 96{{,}}6\ \text{{(kN)}}', '5.7')
    add_p(doc, 'Kiểm nghiệm khả năng tải tĩnh (với X₀ = 0,5, Y₀ = 0,22 / tan α = 0,96):')
    add_eq(doc, rf'Q_{{0B}} = \max(0{{,}}5 F_{{rB}} + Y_0 \sum F_{{aB}};\ F_{{rB}}) = \max({fnum(b1["Q0a"]/1000, 2)};\ {fnum(R["FrB"]/1000, 2)}) = {fnum(b1["Q0"]/1000, 2)}\ \text{{(kN)}} < C_0 = 75{{,}}9\ \text{{(kN)}}', '5.8')
    add_p(doc, 'Kết luận: Cặp ổ đũa côn một dãy 7310 lắp trên Trục I thỏa mãn cả độ bền động và độ bền tĩnh.')

    add_h2(doc, '5.2. Tính chọn cặp ổ lăn cho Trục II')
    b2 = R['b2']
    add_p(doc, 'Tổng lực hướng tâm tác dụng lên ổ C và ổ D của Trục II:')
    add_eq(doc, rf'F_{{rC}} = \sqrt{{R_{{Cx}}^2 + R_{{Cy}}^2}} = \sqrt{{{fnum(R["RCx"], 2)}^2 + {fnum(R["RCy"], 2)}^2}} = {fnum(R["FrC"], 1)}\ \text{{(N)}}', '5.9')
    add_eq(doc, rf'F_{{rD}} = \sqrt{{R_{{Dx}}^2 + R_{{Dy}}^2}} = \sqrt{{({fnum(R["RDx"], 2)})^2 + ({fnum(R["RDy"], 2)})^2}} = {fnum(R["FrD"], 1)}\ \text{{(N)}}', '5.10')
    add_p(doc, 'Với F_a2 / F_rC = 3102,2 / 6910,8 = 0,45 > 0,3 và đường kính ngỗng trục d = 65 mm, ta chọn cặp ổ đũa côn một dãy 7213 lắp kiểu chữ "O". Thông số ổ 7213 (Bảng P2.11 [2]) cho ở Bảng 5.2.')
    add_table(doc,
        ['Ký hiệu ổ', 'd (mm)', 'D (mm)', 'T (mm)', 'α (độ)', 'e = 1,5 tan α', 'C (kN)', 'C₀ (kN)'],
        [['7213', '65', '120', '24,75', '13,83°', fnum(b2['e'], 3), '91,3', '75,0']],
        caption='Bảng 5.2. Thông số ổ đũa côn một dãy 7213 lắp trên Trục II [2]',
        col_widths=[2.0, 1.6, 1.8, 1.8, 2.0, 2.6, 2.1, 2.1], font_size=10
    )
    add_p(doc, 'Tính lực dọc trục phụ và tổng lực dọc trục (F_a2 = 3102,2 N hướng về ổ C):')
    add_eq(doc, rf'S_C = 0{{,}}83 e F_{{rC}} = {fnum(b2["SR"], 1)}\ \text{{(N)}};\quad S_D = 0{{,}}83 e F_{{rD}} = {fnum(b2["SL"], 1)}\ \text{{(N)}}', '5.11')
    add_eq(doc, rf'\sum F_{{aC}} = \max(S_D + F_{{a2}},\ S_C) = {fnum(b2["FaR_used"], 1)}\ \text{{(N)}};\quad \sum F_{{aD}} = \max(S_C - F_{{a2}},\ S_D) = {fnum(b2["FaL_used"], 1)}\ \text{{(N)}}', '5.12')
    add_p(doc, 'Tải trọng động quy đổi trên từng ổ (với Y = 1,625, K_σ = 1,1, K_t = 1,0):')
    add_mixed(doc, [('t', '– Ổ C: '), ('m', rf'\sum F_{{aC}} / (V F_{{rC}}) = {fnum(b2["R"]["ratio"], 3)} > e \Rightarrow X = 0{{,}}4,\ Y = 1{{,}}625 \Rightarrow Q_C = {fnum(b2["R"]["Q"], 1)}\ \text{{(N)}}'), ('t', ';')])
    add_mixed(doc, [('t', '– Ổ D: '), ('m', rf'\sum F_{{aD}} / (V F_{{rD}}) = {fnum(b2["L"]["ratio"], 3)} \le e \Rightarrow X = 1,\ Y = 0 \Rightarrow Q_D = {fnum(b2["L"]["Q"], 1)}\ \text{{(N)}}'), ('t', '.')])
    add_p(doc, 'Tính cho ổ C chịu tải lớn hơn (Q_C = 10089,2 N):')
    add_eq(doc, rf'Q_E = {fnum(R["fac_life"], 3)} \times {fnum(b2["R"]["Q"], 1)} = {fnum(b2["QE"], 1)}\ \text{{(N)}};\quad L = \frac{{60 \times 63{{,}}26 \times 24000}}{{10^6}} = {fnum(b2["Lm"], 1)}\ \text{{(triệu vòng)}}', '5.13')
    add_eq(doc, rf'C_{{tt}} = {fnum(b2["QE"]/1000, 2)} \times {fnum(b2["Lm"], 1)}^{{0{{,}}3}} = {fnum(b2["Ctt"], 2)}\ \text{{(kN)}} < C = 91{{,}}3\ \text{{(kN)}}', '5.14')
    add_eq(doc, rf'Q_{{0C}} = \max(0{{,}}5 F_{{rC}} + Y_0 \sum F_{{aC}};\ F_{{rC}}) = {fnum(b2["Q0"]/1000, 2)}\ \text{{(kN)}} < C_0 = 75{{,}}0\ \text{{(kN)}}', '5.15')
    add_p(doc, 'Kết luận: Cặp ổ đũa côn một dãy 7213 lắp trên Trục II thỏa mãn điều kiện tải động và tải tĩnh.')

    add_h2(doc, '5.3. Tính chọn và kiểm nghiệm nối trục vòng đàn hồi')
    nt = R['nt']
    add_p(doc, 'Nối trục lắp ở đầu ra Trục II (d = 63 mm) nối với trục dẫn xích tải. Chọn hệ số chế độ làm việc cho xích tải k = 1,5 (Bảng 16.1 [2]). Mômen xoắn tính toán:')
    add_eq(doc, rf'T_t = k \cdot T_2 = 1{{,}}5 \times 1200{{,}}84 = {fnum(R["Tt_nt"]/1000, 2)}\ \text{{(N.m)}}', '5.16')
    add_p(doc, 'Tra Bảng 16.10a và 16.10b tài liệu [2], chọn nối trục vòng đàn hồi có mômen cho phép [T] = 2000 N.m > T_t = 1801,25 N.m và đường kính lỗ trục d = 63 mm. Các kích thước cơ bản của nối trục cho ở Bảng 5.3.')
    add_table(doc,
        ['[T] (N.m)', 'd (mm)', 'D (mm)', 'd_m (mm)', 'L (mm)', 'l (mm)', 'D₀ (mm)', 'Z (chốt)', 'd_c (mm)', 'l₁ / l₂ / l₃ (mm)'],
        [['2000', '63', '260', '120', '286', '140', '200', '8', '24', '52 / 24 / 44']],
        caption='Bảng 5.3. Thông số kích thước cơ bản của nối trục vòng đàn hồi [2]',
        col_widths=[1.7, 1.3, 1.5, 1.6, 1.5, 1.4, 1.6, 1.5, 1.5, 2.4], font_size=9.5
    )
    add_p(doc, 'Kiểm nghiệm sức bền dập của vòng cao su đàn hồi và sức bền uốn của chốt thép (với [σ_d] = 2 ÷ 4 MPa, [σ_u] = 60 ÷ 80 MPa, l₀ = l₁ + l₂/2 = 64 mm) [2]:')
    add_eq(doc, rf'\sigma_d = \frac{{2 k T_2}}{{Z D_0 d_c l_3}} = \frac{{2 \times 1{{,}}5 \times 1200835{{,}}7}}{{8 \times 200 \times 24 \times 44}} = {fnum(R["sd_nt"], 2)}\ \text{{(MPa)}} \le [\sigma_d] = 2 \div 4\ \text{{(MPa)}}', '5.17')
    add_eq(doc, rf'\sigma_u = \frac{{k T_2 l_0}}{{0{{,}}1 d_c^3 D_0 Z}} = \frac{{1{{,}}5 \times 1200835{{,}}7 \times 64}}{{0{{,}}1 \times 24^3 \times 200 \times 8}} = {fnum(R["su_nt"], 2)}\ \text{{(MPa)}} \le [\sigma_u] = 60 \div 80\ \text{{(MPa)}}', '5.18')
    add_p(doc, 'Kết luận: Nối trục vòng đàn hồi đã chọn hoàn toàn thỏa mãn điều kiện bền dập vòng đàn hồi và bền uốn chốt.')

    # ===================== TÀI LIỆU THAM KHẢO =====================
    sec_ref = doc.add_section(WD_SECTION_START.NEW_PAGE)
    setup_page(sec_ref, header_text='Tài liệu tham khảo', show_page_num=True)
    add_h1(doc, 'TÀI LIỆU THAM KHẢO')
    refs = [
        ('[1] ', 'Nguyễn Hữu Lộc (2020), ', 'Giáo trình Cơ sở thiết kế máy', ', NXB Đại học Quốc gia TP. Hồ Chí Minh, TP. Hồ Chí Minh.'),
        ('[2] ', 'Trịnh Chất, Lê Văn Uyển (2007), ', 'Tính toán thiết kế hệ dẫn động cơ khí (Tập 1 & 2)', ', NXB Giáo dục, Hà Nội.'),
        ('[3] ', 'Nguyễn Bá Dương, Nguyễn Văn Lẫm, Hoàng Văn Ngọc, Lê Đắc Phong (1978), ', 'Tập bản vẽ Chi tiết máy', ', NXB Đại học và Trung học chuyên nghiệp, Hà Nội.'),
        ('[4] ', 'Trần Hữu Quế, Đặng Văn Cứ, Nguyễn Văn Tuấn (2007), ', 'Vẽ kỹ thuật cơ khí (Tập 1 & 2)', ', NXB Giáo dục, Hà Nội.'),
        ('[5] ', 'Ninh Đức Tốn (2001), ', 'Dung sai và lắp ghép', ', NXB Giáo dục, Hà Nội.'),
    ]
    for num, auth, title, pub in refs:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        pf = p.paragraph_format
        pf.left_indent = Cm(1.0)
        pf.first_line_indent = Cm(-1.0)
        pf.space_before = Pt(3)
        pf.space_after = Pt(4)
        pf.line_spacing = 1.2
        set_font_tnr(p.add_run(num), bold=True)
        set_font_tnr(p.add_run(auth))
        set_font_tnr(p.add_run(title), italic=True)
        set_font_tnr(p.add_run(pub))

    doc.save(OUT_DOCX)
    print('Saved DOCX:', OUT_DOCX)

if __name__ == '__main__':
    build()
