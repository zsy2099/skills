#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
strategic-marketing-director / PPT 交付生成器 v1.0.0

把一份 deck.json 渲染成 16:9 的 .pptx 汇报稿，内置 12 套视觉主题。

用法:
    python generate_pptx.py --input deck.json --output deck.pptx
    python generate_pptx.py --input deck.json --output deck.pptx --style minimalism
    python generate_pptx.py --list-styles

deck.json 结构见 scripts/deck.example.json：
    style     视觉风格键（可被 --style 覆盖）
    cover     封面：title / scenario / subtitle / presenter / date
    sections  页面数组，每页 layout ∈ cover|agenda|metrics|bullets|two_column|table|timeline|section|closing

依赖: python-pptx>=1.0.2
"""

import argparse
import json
import math
import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# ---------------------------------------------------------------- 画布常量

SW, SH = 13.333, 7.5          # 16:9
MARGIN = 0.72
CW = SW - 2 * MARGIN          # 内容宽度 11.893
CN_FONT = "微软雅黑"
EN_FONT = "微软雅黑"


def C(hexstr):
    h = hexstr.lstrip("#")
    return RGBColor(int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


# ---------------------------------------------------------------- 12 套主题

THEMES = {
    "minimalism": dict(
        label="极简主义", bg="#FAFAF8", surface="#FFFFFF", primary="#1A1A1A",
        accent="#FFD60A", text="#1A1A1A", muted="#8C8C84", on_primary="#FFFFFF",
        rule="#E4E2DA", dark=False, mono=False),
    "modernism": dict(
        label="现代主义", bg="#FFFFFF", surface="#F4F4F2", primary="#DA1F26",
        accent="#1A1A1A", text="#141414", muted="#7A7A72", on_primary="#FFFFFF",
        rule="#D9D9D6", dark=False, mono=False),
    "brutalism": dict(
        label="新野兽派", bg="#FFFDF5", surface="#FFFFFF", primary="#FF3D7F",
        accent="#111111", text="#0A0A0A", muted="#5E5E58", on_primary="#FFFFFF",
        rule="#0A0A0A", dark=False, mono=False),
    "pixel": dict(
        label="像素风", bg="#0F0F16", surface="#1B1B26", primary="#39FF14",
        accent="#FFD60A", text="#EAEAF2", muted="#9A9AAE", on_primary="#0F0F16",
        rule="#2E2E3C", dark=True, mono=True),
    "maximalism": dict(
        label="极繁主义", bg="#FFF6FA", surface="#FFFFFF", primary="#E91E63",
        accent="#7C4DFF", text="#2A1620", muted="#8A6A78", on_primary="#FFFFFF",
        rule="#F3D3E0", dark=False, mono=False),
    "retro": dict(
        label="复古风", bg="#FBEFE0", surface="#FFF8EE", primary="#C05F2C",
        accent="#2E6B5E", text="#3A2418", muted="#8A6A52", on_primary="#FFF8EE",
        rule="#E5CDB4", dark=False, mono=False),
    "glassmorphism": dict(
        label="玻璃拟物", bg="#EEF2FF", surface="#FFFFFF", primary="#4A6CF7",
        accent="#7AA2FF", text="#16204A", muted="#6B78A8", on_primary="#FFFFFF",
        rule="#D6DDFB", dark=False, mono=False),
    "terminal": dict(
        label="终端风", bg="#08080A", surface="#121216", primary="#22C55E",
        accent="#22C55E", text="#D8F5E3", muted="#6E8F7A", on_primary="#08080A",
        rule="#1F2A22", dark=True, mono=True),
    "nordic": dict(
        label="北欧风", bg="#F7F5F1", surface="#FFFFFF", primary="#6E8B7A",
        accent="#C89F6B", text="#2C322E", muted="#8A8F88", on_primary="#FFFFFF",
        rule="#DFDCD4", dark=False, mono=False),
    "postmodern": dict(
        label="后现代主义", bg="#FFFFFF", surface="#F6F4FF", primary="#7C3AED",
        accent="#F59E0B", text="#171029", muted="#7A6E96", on_primary="#FFFFFF",
        rule="#E3DCFB", dark=False, mono=False),
    "futurism": dict(
        label="未来主义", bg="#05091A", surface="#0C1330", primary="#00E5FF",
        accent="#FF2E97", text="#E4F6FF", muted="#7C8FC4", on_primary="#05091A",
        rule="#1C2A55", dark=True, mono=False),
    "y2k": dict(
        label="Y2K千禧", bg="#F1F4FF", surface="#FFFFFF", primary="#7B5CFF",
        accent="#FF6FB5", text="#221A3D", muted="#6F6796", on_primary="#FFFFFF",
        rule="#DCD8FA", dark=False, mono=False),
}

# ---------------------------------------------------------------- 排版工具


def fit_size(text, w_in, h_in, max_pt, min_pt=10, line_spacing=1.35, cjk=1.02):
    """按框体尺寸估算可容纳的最大字号（中英混排近似）。"""
    w_pt, h_pt = w_in * 72.0, h_in * 72.0
    body = str(text or "")
    for pt in range(int(max_pt), int(min_pt) - 1, -1):
        cpl = max(1, int(w_pt / (pt * cjk)))
        lines = 0
        for seg in body.split("\n"):
            lines += max(1, math.ceil(len(seg) / cpl)) if seg else 1
        if lines * pt * line_spacing <= h_pt:
            return pt
    return min_pt


def textbox(slide, x, y, w, h, text, size, color, bold=False,
            align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, line=1.35, mono=False):
    box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = 0
    tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = anchor
    lines = str(text or "").split("\n")
    for i, seg in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = seg
        p.alignment = align
        p.line_spacing = line
        for r in p.runs:
            r.font.size = Pt(size)
            r.font.bold = bold
            r.font.color.rgb = color
            r.font.name = "Consolas" if mono else CN_FONT
    return box


def rect(slide, x, y, w, h, fill=None, line=None, shape=MSO_SHAPE.RECTANGLE,
         radius=None, line_w=1.0):
    sp = slide.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
    if radius is not None and shape == MSO_SHAPE.ROUNDED_RECTANGLE:
        try:
            sp.adjustments[0] = radius
        except Exception:
            pass
    if fill is None:
        sp.fill.background()
    else:
        sp.fill.solid()
        sp.fill.fore_color.rgb = fill
    if line is None:
        sp.line.fill.background()
    else:
        sp.line.color.rgb = line
        sp.line.width = Pt(line_w)
    sp.shadow.inherit = False
    sp.text_frame.text = ""
    return sp


def paint_bg(slide, theme):
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = C(theme["bg"])


def add_footer(slide, theme, page_no, total, kicker=""):
    muted = C(theme["muted"])
    if kicker:
        textbox(slide, MARGIN, SH - 0.5, CW * 0.8, 0.26,
                kicker, 10, muted, mono=theme["mono"])
    if page_no:
        textbox(slide, SW - MARGIN - 1.2, SH - 0.5, 1.2, 0.26,
                "%d / %d" % (page_no, total), 10, muted,
                align=PP_ALIGN.RIGHT, mono=theme["mono"])


def add_title(slide, theme, title, y=0.55, size=30):
    rect(slide, MARGIN, y - 0.06, 0.14, size / 26.0, fill=C(theme["primary"]))
    textbox(slide, MARGIN + 0.34, y - 0.10, CW - 0.34, size / 26.0 + 0.16,
            title, size, C(theme["text"]), bold=True,
            anchor=MSO_ANCHOR.MIDDLE, mono=theme["mono"])
    ly = y + size / 26.0 + 0.16
    rect(slide, MARGIN, ly, CW, 0.012, fill=C(theme["rule"]))
    return ly + 0.28


# ---------------------------------------------------------------- 版式

def layout_cover(prs, theme, data, page_no, total):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    paint_bg(s, theme)
    rect(s, 0, 0, 0.42, SH, fill=C(theme["primary"]))
    title = data.get("title", "")
    scenario = data.get("scenario", "")
    subtitle = data.get("subtitle", "")
    x = MARGIN + 0.45
    w = CW - 0.9

    ts = fit_size(title, w, 1.5, 54, 30)
    textbox(s, x, 1.55, w, 1.5, title, ts, C(theme["text"]), bold=True,
            anchor=MSO_ANCHOR.BOTTOM, mono=theme["mono"])
    if scenario:
        ss = fit_size(scenario, w, 0.7, 28, 16)
        textbox(s, x, 3.15, w, 0.7, scenario, ss, C(theme["primary"]),
                bold=True, mono=theme["mono"])
    if subtitle:
        textbox(s, x, 4.05, w, 1.3, subtitle, 15, C(theme["muted"]), line=1.55,
                mono=theme["mono"])
    rect(s, x, SH - 1.5, w, 0.014, fill=C(theme["rule"]))
    meta = "  |  ".join([v for v in [data.get("presenter", ""), data.get("date", "")] if v])
    if meta:
        textbox(s, x, SH - 1.32, w, 0.34, meta, 12, C(theme["muted"]), mono=theme["mono"])
    return s


def layout_agenda(prs, theme, sec, page_no, total):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    paint_bg(s, theme)
    y = add_title(s, theme, sec.get("title", "方案结构"))
    items = sec.get("items", [])
    n = max(1, len(items))
    h = min(0.86, (SH - 1.55 - y) / n - 0.14)
    size = int(min(19, max(13, h * 22)))
    for i, it in enumerate(items):
        yy = y + i * (h + 0.14)
        rect(s, MARGIN, yy, CW, h, fill=C(theme["surface"]),
             line=C(theme["rule"]), line_w=0.75)
        rect(s, MARGIN, yy, 0.075, h, fill=C(theme["primary"]))
        textbox(s, MARGIN + 0.32, yy, 0.8, h, "%02d" % (i + 1), size + 4,
                C(theme["primary"]), bold=True, anchor=MSO_ANCHOR.MIDDLE,
                mono=theme["mono"])
        textbox(s, MARGIN + 1.15, yy, CW - 1.5, h, it, size, C(theme["text"]),
                anchor=MSO_ANCHOR.MIDDLE, mono=theme["mono"])
    add_footer(s, theme, page_no, total, sec.get("kicker", ""))
    return s


def layout_metrics(prs, theme, sec, page_no, total):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    paint_bg(s, theme)
    y = add_title(s, theme, sec.get("title", "核心结论"))
    conclusion = sec.get("conclusion", "")
    if conclusion:
        ch = 0.95
        cs = fit_size(conclusion, CW, ch, 24, 14)
        textbox(s, MARGIN, y, CW, ch, conclusion, cs, C(theme["text"]), bold=True,
                line=1.4, mono=theme["mono"])
        y += ch + 0.12
    if sec.get("frameworks"):
        box = rect(s, MARGIN, y, CW, 0.42, fill=C(theme["surface"]),
                   line=C(theme["primary"]), line_w=0.75)
        textbox(s, MARGIN + 0.2, y, CW - 0.4, 0.42, "调用框架：" + sec["frameworks"],
                11.5, C(theme["primary"]), anchor=MSO_ANCHOR.MIDDLE, mono=theme["mono"])
        y += 0.68
    metrics = sec.get("metrics", [])[:4]
    if metrics:
        card_h = min(1.85, SH - 0.85 - y)
        gap = 0.26
        cw = (CW - gap * (len(metrics) - 1)) / len(metrics)
        for i, m in enumerate(metrics):
            cx = MARGIN + i * (cw + gap)
            rect(s, cx, y, cw, card_h, fill=C(theme["surface"]),
                 line=C(theme["rule"]), line_w=0.75)
            rect(s, cx, y, cw, 0.07, fill=C(theme["primary"]))
            num = str(m.get("num", ""))
            ns = fit_size(num, cw - 0.4, 0.85, 44, 22)
            textbox(s, cx + 0.2, y + 0.34, cw - 0.4, 0.85, num, ns,
                    C(theme["primary"]), bold=True, align=PP_ALIGN.CENTER,
                    mono=theme["mono"])
            textbox(s, cx + 0.2, y + 1.24, cw - 0.4, 0.5, m.get("label", ""), 12,
                    C(theme["muted"]), align=PP_ALIGN.CENTER, line=1.25,
                    mono=theme["mono"])
    add_footer(s, theme, page_no, total, sec.get("kicker", ""))
    return s


def layout_bullets(prs, theme, sec, page_no, total):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    paint_bg(s, theme)
    y = add_title(s, theme, sec.get("title", ""))
    items = sec.get("bullets", [])
    if sec.get("note"):
        textbox(s, MARGIN, y, CW, 0.34, sec["note"], 12.5, C(theme["primary"]),
                mono=theme["mono"])
        y += 0.5
    box_h = SH - 0.85 - y
    joined = "\n".join("▪  " + str(i) for i in items)
    size = fit_size(joined, CW - 0.4, box_h, 20, 11, line_spacing=1.5)
    box = s.shapes.add_textbox(Inches(MARGIN), Inches(y), Inches(CW), Inches(box_h))
    tf = box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = 0
    tf.margin_top = tf.margin_bottom = 0
    for i, it in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = "▪  " + str(it)
        p.line_spacing = 1.5
        p.space_after = Pt(9)
        for r in p.runs:
            r.font.size = Pt(size)
            r.font.color.rgb = C(theme["text"])
            r.font.name = "Consolas" if theme["mono"] else CN_FONT
    add_footer(s, theme, page_no, total, sec.get("kicker", ""))
    return s


def layout_two_column(prs, theme, sec, page_no, total):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    paint_bg(s, theme)
    y = add_title(s, theme, sec.get("title", ""))
    cols = [sec.get("left", {}), sec.get("right", {})]
    gap = 0.4
    cw = (CW - gap) / 2
    box_h = SH - 0.85 - y
    for ci, col in enumerate(cols):
        cx = MARGIN + ci * (cw + gap)
        rect(s, cx, y, cw, box_h, fill=C(theme["surface"]),
             line=C(theme["rule"]), line_w=0.75)
        rect(s, cx, y, cw, 0.07, fill=C(theme["primary"]))
        ctitle = col.get("title", "")
        if ctitle:
            textbox(s, cx + 0.3, y + 0.28, cw - 0.6, 0.45, ctitle, 16,
                    C(theme["primary"]), bold=True, mono=theme["mono"])
        items = col.get("bullets", [])
        joined = "\n".join("▪  " + str(i) for i in items)
        size = fit_size(joined, cw - 0.6, box_h - 0.95, 15, 10, line_spacing=1.45)
        box = s.shapes.add_textbox(Inches(cx + 0.3), Inches(y + 0.85),
                                   Inches(cw - 0.6), Inches(box_h - 0.95))
        tf = box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = 0
        for i, it in enumerate(items):
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            p.text = "▪  " + str(it)
            p.line_spacing = 1.45
            p.space_after = Pt(7)
            for r in p.runs:
                r.font.size = Pt(size)
                r.font.color.rgb = C(theme["text"])
                r.font.name = "Consolas" if theme["mono"] else CN_FONT
    add_footer(s, theme, page_no, total, sec.get("kicker", ""))
    return s


def layout_table(prs, theme, sec, page_no, total):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    paint_bg(s, theme)
    y = add_title(s, theme, sec.get("title", ""))
    headers = sec.get("headers", [])
    rows = sec.get("rows", [])
    if not headers:
        return s
    box_h = SH - 0.85 - y
    nrows, ncols = len(rows) + 1, len(headers)
    gt = s.shapes.add_table(nrows, ncols, Inches(MARGIN), Inches(y),
                            Inches(CW), Inches(box_h))
    tbl = gt.table
    total_w = Emu(int(Inches(CW)))
    for c in range(ncols):
        tbl.columns[c].width = Emu(int(total_w / ncols))
    row_h = Emu(int(Inches(box_h) / nrows))
    longest = max([len(str(h)) for h in headers] +
                  [len(str(c)) for r in rows for c in r] + [1])
    size = 15 if longest <= 14 else (13 if longest <= 22 else 11)
    for r in range(nrows):
        tbl.rows[r].height = row_h
        for c in range(ncols):
            cell = tbl.cell(r, c)
            cell.text = ""
            cell.margin_left = cell.margin_right = Inches(0.1)
            cell.margin_top = cell.margin_bottom = Inches(0.05)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            cell.fill.solid()
            if r == 0:
                cell.fill.fore_color.rgb = C(theme["primary"])
            else:
                cell.fill.fore_color.rgb = (C(theme["surface"]) if r % 2
                                            else C(theme["bg"]))
            txt = str(headers[c] if r == 0 else rows[r - 1][c])
            p = cell.text_frame.paragraphs[0]
            p.text = txt
            p.alignment = PP_ALIGN.LEFT if c == 0 else PP_ALIGN.LEFT
            for run in p.runs:
                run.font.size = Pt(size)
                run.font.bold = (r == 0)
                run.font.color.rgb = (C(theme["on_primary"]) if r == 0
                                      else C(theme["text"]))
                run.font.name = "Consolas" if theme["mono"] else CN_FONT
    add_footer(s, theme, page_no, total, sec.get("kicker", ""))
    return s


def layout_timeline(prs, theme, sec, page_no, total):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    paint_bg(s, theme)
    y = add_title(s, theme, sec.get("title", ""))
    stages = sec.get("stages", [])
    if not stages:
        return s
    n = len(stages)
    gap = 0.28
    cw = (CW - gap * (n - 1)) / n
    ch = min(2.5, SH - 0.95 - y)
    cy = y + (SH - 0.85 - y - ch) / 2
    rect(s, MARGIN, cy + 0.62, CW, 0.03, fill=C(theme["rule"]))
    for i, st in enumerate(stages):
        cx = MARGIN + i * (cw + gap)
        rect(s, cx + cw / 2 - 0.17, cy + 0.45, 0.34, 0.34,
             fill=C(theme["primary"]), shape=MSO_SHAPE.OVAL)
        textbox(s, cx + cw / 2 - 0.17, cy + 0.45, 0.34, 0.34, str(i + 1), 12,
                C(theme["on_primary"]), bold=True, align=PP_ALIGN.CENTER,
                anchor=MSO_ANCHOR.MIDDLE, mono=theme["mono"])
        textbox(s, cx, cy - 0.15, cw, 0.55, st.get("name", ""), 16,
                C(theme["text"]), bold=True, align=PP_ALIGN.CENTER,
                anchor=MSO_ANCHOR.BOTTOM, mono=theme["mono"])
        desc = st.get("desc", "")
        ds = fit_size(desc, cw - 0.24, 1.4, 12.5, 9.5, line_spacing=1.4)
        textbox(s, cx + 0.12, cy + 0.95, cw - 0.24, 1.4, desc, ds,
                C(theme["muted"]), align=PP_ALIGN.CENTER, line=1.4,
                mono=theme["mono"])
    add_footer(s, theme, page_no, total, sec.get("kicker", ""))
    return s


def layout_section(prs, theme, sec, page_no, total):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    paint_bg(s, theme)
    rect(s, 0, 0, SW, SH, fill=C(theme["primary"]))
    title = sec.get("title", "")
    ts = fit_size(title, CW - 1.0, 1.6, 46, 26)
    textbox(s, MARGIN + 0.2, 2.7, CW - 1.0, 1.6, title, ts,
            C(theme["on_primary"]), bold=True, anchor=MSO_ANCHOR.MIDDLE,
            mono=theme["mono"])
    if sec.get("note"):
        textbox(s, MARGIN + 0.2, 4.45, CW - 1.0, 0.5, sec["note"], 14,
                C(theme["on_primary"]), mono=theme["mono"])
    add_footer(s, theme, page_no, total, "")
    return s


def layout_closing(prs, theme, sec, page_no, total):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    paint_bg(s, theme)
    rect(s, 0, 0, SW, 0.16, fill=C(theme["primary"]))
    y = add_title(s, theme, sec.get("title", "下一步"), y=0.85)
    items = sec.get("bullets", [])
    joined = "\n".join("→  " + str(i) for i in items)
    size = fit_size(joined, CW, SH - 1.15 - y, 21, 12, line_spacing=1.6)
    box = s.shapes.add_textbox(Inches(MARGIN), Inches(y), Inches(CW),
                               Inches(SH - 1.15 - y))
    tf = box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = 0
    for i, it in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = "→  " + str(it)
        p.line_spacing = 1.6
        p.space_after = Pt(11)
        for r in p.runs:
            r.font.size = Pt(size)
            r.font.color.rgb = C(theme["text"])
            r.font.name = "Consolas" if theme["mono"] else CN_FONT
    add_footer(s, theme, page_no, total, sec.get("kicker", ""))
    return s


LAYOUTS = {
    "cover": layout_cover,
    "agenda": layout_agenda,
    "metrics": layout_metrics,
    "bullets": layout_bullets,
    "two_column": layout_two_column,
    "table": layout_table,
    "timeline": layout_timeline,
    "section": layout_section,
    "closing": layout_closing,
}


# ---------------------------------------------------------------- 主流程

def build(deck, out_path, style_override=None):
    style = (style_override or deck.get("style") or "minimalism").lower()
    if style not in THEMES:
        raise SystemExit("未知风格 %s，可用：%s" % (style, ", ".join(THEMES)))
    theme = THEMES[style]

    prs = Presentation()
    prs.slide_width = Inches(SW)
    prs.slide_height = Inches(SH)

    sections = list(deck.get("sections", []))
    total = len(sections) + 1

    layout_cover(prs, theme, deck.get("cover", {}), 0, total)
    for i, sec in enumerate(sections, start=1):
        kind = (sec.get("layout") or "bullets").lower()
        fn = LAYOUTS.get(kind, layout_bullets)
        if kind == "cover":
            continue
        fn(prs, theme, sec, i, total)

    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    prs.core_properties.title = deck.get("cover", {}).get("title", "")
    prs.save(out_path)
    return out_path, theme["label"], total


def main():
    ap = argparse.ArgumentParser(description="生成 16:9 汇报 PPTX")
    ap.add_argument("--input", "-i", required=False, help="deck.json 路径")
    ap.add_argument("--output", "-o", required=False, help="输出 .pptx 路径")
    ap.add_argument("--style", "-s", default=None, help="覆盖视觉风格")
    ap.add_argument("--list-styles", action="store_true", help="列出全部风格")
    args = ap.parse_args()

    if args.list_styles:
        for k, v in THEMES.items():
            print("%-16s %s" % (k, v["label"]))
        return

    if not args.input or not args.output:
        ap.error("需要 --input 和 --output（或 --list-styles）")

    with open(args.input, "r", encoding="utf-8") as f:
        deck = json.load(f)

    path, label, pages = build(deck, args.output, args.style)
    print("OK  style=%s  pages=%d  ->  %s" % (label, pages, path))


if __name__ == "__main__":
    main()
