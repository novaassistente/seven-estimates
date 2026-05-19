#!/usr/bin/env python3
"""Estimate for SJA Property Management - Bedroom Window Lock & Broken Section Removal.
Matches the Seven General Contractors estimate brand template
(see /home/luccas/Documents/Seven/estimates/14841-Densmore-Ave-N/build_estimate_pdf.py).
"""
from fpdf import FPDF
from fpdf.enums import XPos, YPos
from pathlib import Path
from decimal import Decimal, ROUND_HALF_UP

HERE = Path(__file__).parent
LOGO = HERE / "logo_on_black.png"
OUT  = HERE / "SJA-Bedroom-Window-Lock_Estimate.pdf"

BRAND_NAME    = "SEVEN GENERAL CONTRACTORS"
TAGLINE       = "Kitchen & Bathroom Remodeling Specialists"
LOCATION_LINE = "Bothell, WA  |  www.sevenremodel.com"
FOOTER_LINE   = "Seven General Contractors  -  Bothell, WA  -  140+ Five-Star Reviews  -  www.sevenremodel.com"

BLACK    = (15, 15, 15)
DARK     = (30, 30, 30)
GOLD     = (193, 161, 84)
GOLD_DK  = (164, 134, 60)
TEXT     = (45, 45, 45)
MUTED    = (110, 110, 110)
ROW_ALT  = (245, 245, 245)
LINE     = (210, 210, 210)
WHITE    = (255, 255, 255)

EST_NUMBER    = "SJA-BWL-2026-05-18"
EST_DATE      = "May 18, 2026"
VALID_UNTIL   = "June 17, 2026"
PREPARED_FOR  = "SJA Property Management"
ATTN_LINE     = "Attn: Maggie"
PROPERTY_LINES = [
    "Tenant unit - bedroom window",
    "(unit address on file with SJA)",
]
PROJECT_TITLE = "Bedroom Window - Unlock & Remove Broken Section"
PROJECT_DESC  = (
    "The tenant's bedroom window has a broken section. Seven General Contractors will attempt to unlock "
    "the window from the inside and remove the broken piece without disturbing the surrounding glass. "
    "This estimate covers the preferred (Option 1) path at a firm price of $700. Two contingent paths "
    "are documented below in case Option 1 is not viable - each contingent path will be re-quoted before "
    "any additional work proceeds."
)

SCOPE_GROUPS = [
    ("Option 1 - Unlock & extract broken section (preferred) - $700", [
        "Site visit and inspection of the bedroom window from inside the unit",
        "Unlock the window assembly and operate the sash to access the broken section",
        "Remove the broken piece carefully, with the goal of leaving the surrounding glass intact",
        "Clean the work area; bag and dispose of broken material",
        "Final operation test of the window and confirmation with tenant on completion",
    ]),
    ("Inherent risk disclosure", [
        "There is an inherent risk that the surrounding glass may be damaged during removal of the broken section",
        "If the glass comes through intact, the work is completed at the firm price of $700 (Option 1)",
        "If the glass is damaged during removal, or if full replacement is required outright, work pauses and we move to Option 2 (re-quoted)",
    ]),
]

CONTINGENT_INTRO = (
    "The following two paths are NOT included in the $700 price above. They apply only if Option 1 is not "
    "viable. In either case, Seven will pause work, evaluate, and send a written revised quote for approval "
    "before any additional work begins."
)

CONTINGENT = [
    (
        "Option 2 - Full replacement from the inside (contingent - re-quoted on site).",
        "If the glass is damaged during Option 1, or if it is already clear the window needs full "
        "replacement, Seven will first evaluate whether the replacement can be performed from inside the "
        "unit. If feasible from inside, a revised quote will be issued covering replacement glass/sash, "
        "labor, and any required hardware. Work resumes only after written approval.",
    ),
    (
        "Option 3 - Exterior access via boom truck / bucket lift (contingent - re-quoted on site).",
        "If replacement from the inside is not viable, exterior access will be required. This adds "
        "equipment rental for a boom truck (bucket lift), additional labor, and any traffic/parking "
        "coordination required by the building or city. Costs will be itemized and quoted separately "
        "before any equipment is mobilized.",
    ),
]

LINE_DETAIL = "Tenant bedroom window - Option 1 only"
SUBTOTAL_AMT = Decimal("700.00")
TAX_RATE     = Decimal("0.103")  # WA combined estimated; verify against tenant unit tax code before invoicing
TAX_AMOUNT   = (SUBTOTAL_AMT * TAX_RATE).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
TOTAL        = (SUBTOTAL_AMT + TAX_AMOUNT).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

INVESTMENT_ROWS = [
    ("Unlock window & remove broken section - firm price (Option 1)",
     LINE_DETAIL, SUBTOTAL_AMT),
    ("Subtotal", "", SUBTOTAL_AMT),
    ("Sales tax", "WA - 10.3% est.", TAX_AMOUNT),
]

TERMS = [
    "Payment is due upon project completion unless otherwise agreed in writing.",
    "Any change to the scope of work must be agreed upon in writing and may affect the total cost.",
    "All work is performed by Seven General Contractors owner-operator - no subcontractors.",
    "This estimate is valid for 30 days from the date issued.",
    "Permit fees, if required, are not included and will be billed separately.",
    "Sales tax rate reflects Washington state combined estimate for 2026; verify against the tenant unit's exact tax code before invoicing.",
    "Option 2 (interior replacement) and Option 3 (boom truck / exterior access) are NOT included in this estimate and require a separate written quote and approval before any related work begins.",
    "Seven is not responsible for pre-existing damage to the window frame, sash, or surrounding finishes. The Option 1 price assumes a normally operating window assembly that can be unlocked from the inside.",
]


def usd(amount: Decimal) -> str:
    return f"${amount:,.2f}"


class PDF(FPDF):
    def header(self):
        if self.page_no() != 1:
            self._mini_header()
            return

        top = 12
        if LOGO.exists():
            box = 24
            border = 1.4
            inner = box - 2 * border
            self.set_fill_color(*GOLD)
            self.rect(self.l_margin, top, box, box, "F")
            self.image(
                str(LOGO),
                x=self.l_margin + border,
                y=top + border,
                w=inner,
                h=inner,
            )
        self.set_xy(self.l_margin + 28, top + 1)
        self.set_font("Helvetica", "B", 16)
        self.set_text_color(*BLACK)
        self.cell(120, 7, BRAND_NAME, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_x(self.l_margin + 26)
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(*GOLD_DK)
        self.cell(120, 5, TAGLINE, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_x(self.l_margin + 26)
        self.set_font("Helvetica", "", 8.5)
        self.set_text_color(*MUTED)
        self.cell(120, 5, LOCATION_LINE, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_xy(self.w - self.r_margin - 60, top + 1)
        self.set_font("Helvetica", "B", 22)
        self.set_text_color(*GOLD)
        self.cell(60, 9, "ESTIMATE", align="R", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_xy(self.w - self.r_margin - 60, top + 11)
        self.set_font("Helvetica", "", 9)
        self.set_text_color(*MUTED)
        self.cell(60, 4.5, f"Date: {EST_DATE}", align="R", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_xy(self.w - self.r_margin - 60, top + 16)
        self.cell(60, 4.5, f"Est. #: {EST_NUMBER}", align="R", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_y(top + 24)
        self.set_draw_color(*GOLD)
        self.set_line_width(0.6)
        self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        self.set_line_width(0.2)
        self.set_y(top + 28)

    def _mini_header(self):
        top = 10
        self.set_xy(self.l_margin, top)
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(*BLACK)
        self.cell(0, 5, BRAND_NAME, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_font("Helvetica", "", 8)
        self.set_text_color(*MUTED)
        self.cell(0, 4, f"Estimate #{EST_NUMBER}  -  {EST_DATE}",
                 new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_y(top + 11)
        self.set_draw_color(*GOLD)
        self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        self.set_y(top + 14)

    def footer(self):
        self.set_y(-14)
        self.set_draw_color(*GOLD)
        self.set_line_width(0.3)
        self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        self.set_line_width(0.2)
        self.ln(1)
        self.set_font("Helvetica", "", 8)
        self.set_text_color(*MUTED)
        self.cell(0, 5, FOOTER_LINE, align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)


def avail(pdf):
    return pdf.w - pdf.l_margin - pdf.r_margin


def section_bar(pdf, title):
    pdf.ln(3)
    pdf.set_fill_color(*BLACK)
    pdf.set_text_color(*WHITE)
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(avail(pdf), 7.5, "  " + title.upper(), border=0, fill=True,
             new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(1.5)


def gold_subhead(pdf, text):
    pdf.ln(1)
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(*GOLD_DK)
    pdf.set_fill_color(*ROW_ALT)
    pdf.cell(avail(pdf), 6, "  " + text, border=0, fill=True,
             new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(0.5)


def bullet(pdf, text):
    pdf.set_x(pdf.l_margin)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(*TEXT)
    pdf.cell(6, 5.5, "-", new_x=XPos.RIGHT, new_y=YPos.TOP)
    pdf.multi_cell(avail(pdf) - 6, 5.5, text, new_x=XPos.LMARGIN, new_y=YPos.NEXT)


def para(pdf, text, font_size=10):
    pdf.set_x(pdf.l_margin)
    pdf.set_font("Helvetica", "", font_size)
    pdf.set_text_color(*TEXT)
    pdf.multi_cell(avail(pdf), 5.2, text, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(1)


def info_table(pdf, cols):
    col_w = avail(pdf) / 3
    y0 = pdf.get_y()

    pdf.set_fill_color(*ROW_ALT)
    pdf.set_text_color(*GOLD_DK)
    pdf.set_font("Helvetica", "B", 8.5)
    for i, (hdr, _) in enumerate(cols):
        pdf.set_xy(pdf.l_margin + i * col_w, y0)
        pdf.cell(col_w, 6, "  " + hdr.upper(), border=0, fill=True,
                 new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    body_y = y0 + 6
    body_h = 13
    pdf.set_fill_color(*WHITE)
    for i in range(3):
        pdf.set_xy(pdf.l_margin + i * col_w, body_y)
        pdf.cell(col_w, body_h, "", border=0, fill=False,
                 new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_text_color(*BLACK)
    pdf.set_font("Helvetica", "", 10)
    for i, (_, lines) in enumerate(cols):
        pdf.set_xy(pdf.l_margin + i * col_w + 2, body_y + 1.5)
        if lines:
            pdf.set_font("Helvetica", "B", 10)
            pdf.cell(col_w - 4, 5, lines[0], new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf.set_font("Helvetica", "", 10)
            for ln in lines[1:]:
                pdf.set_x(pdf.l_margin + i * col_w + 2)
                pdf.cell(col_w - 4, 5, ln, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_draw_color(*LINE)
    pdf.set_line_width(0.2)
    end_y = body_y + body_h
    pdf.line(pdf.l_margin, end_y, pdf.w - pdf.r_margin, end_y)
    pdf.set_y(end_y + 2)


def investment_table(pdf, rows):
    col_desc = avail(pdf) * 0.55
    col_det  = avail(pdf) * 0.25
    col_amt  = avail(pdf) - col_desc - col_det
    pdf.set_fill_color(*DARK)
    pdf.set_text_color(*WHITE)
    pdf.set_font("Helvetica", "B", 9.5)
    pdf.cell(col_desc, 7, "  Description", border=0, fill=True)
    pdf.cell(col_det,  7, "  Detail",      border=0, fill=True)
    pdf.cell(col_amt,  7, "Amount  ", border=0, fill=True, align="R",
             new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.set_text_color(*TEXT)
    pdf.set_font("Helvetica", "", 10)
    for idx, (desc, detail, amount) in enumerate(rows):
        is_subtotal = desc.lower() == "subtotal"
        bg = ROW_ALT if (idx % 2 == 0 and not is_subtotal) else WHITE
        pdf.set_fill_color(*bg)
        if is_subtotal:
            pdf.set_font("Helvetica", "B", 10)
        x_start = pdf.get_x()
        y_start = pdf.get_y()
        pdf.multi_cell(col_desc, 7, "  " + desc, border=0, fill=True,
                       new_x=XPos.RIGHT, new_y=YPos.TOP)
        pdf.set_xy(x_start + col_desc, y_start)
        pdf.cell(col_det,  7, "  " + (detail or ""), border=0, fill=True)
        amt_str = usd(amount) + "  " if amount is not None else "-  "
        pdf.cell(col_amt,  7, amt_str, border=0, fill=True, align="R",
                 new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        if is_subtotal:
            pdf.set_font("Helvetica", "", 10)

    pdf.set_fill_color(*GOLD)
    pdf.set_text_color(*WHITE)
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(col_desc + col_det, 9, "  TOTAL INVESTMENT (Option 1 only)", border=0, fill=True)
    pdf.cell(col_amt, 9, usd(TOTAL) + "  ", border=0, fill=True, align="R",
             new_x=XPos.LMARGIN, new_y=YPos.NEXT)


def signature_blocks(pdf):
    pdf.ln(8)
    col_w = avail(pdf) / 2
    y0 = pdf.get_y()

    pdf.set_text_color(*GOLD_DK)
    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(col_w, 6, "Client Acceptance",   border=0)
    pdf.cell(col_w, 6, "Authorized by Seven GC", border=0,
             new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.ln(7)
    sig_y = pdf.get_y()
    pdf.set_draw_color(*MUTED)
    pdf.line(pdf.l_margin, sig_y, pdf.l_margin + col_w - 8, sig_y)
    pdf.line(pdf.l_margin + col_w, sig_y, pdf.l_margin + 2 * col_w - 8, sig_y)

    pdf.line(pdf.l_margin + col_w - 4, y0, pdf.l_margin + col_w - 4, sig_y)

    pdf.ln(2)
    pdf.set_text_color(*MUTED)
    pdf.set_font("Helvetica", "", 9)
    pdf.cell(col_w, 5, "Signature                              Date", border=0)
    pdf.cell(col_w, 5, "Signature                              Date", border=0,
             new_x=XPos.LMARGIN, new_y=YPos.NEXT)


pdf = PDF(format="Letter", unit="mm")
pdf.set_margins(15, 42, 15)
pdf.set_auto_page_break(auto=True, margin=18)
pdf.add_page()

info_table(pdf, [
    ("PREPARED FOR",     [PREPARED_FOR, ATTN_LINE]),
    ("PROPERTY",         PROPERTY_LINES),
    ("VALID UNTIL",      [VALID_UNTIL]),
])

section_bar(pdf, "Project Overview")
gold_subhead(pdf, PROJECT_TITLE)
para(pdf, PROJECT_DESC)

section_bar(pdf, "Scope of Work")
for sub_title, items in SCOPE_GROUPS:
    gold_subhead(pdf, sub_title)
    for it in items:
        bullet(pdf, it)

section_bar(pdf, "Investment")
investment_table(pdf, INVESTMENT_ROWS)

section_bar(pdf, "Contingent Paths - Not Included in this Estimate")
para(pdf, CONTINGENT_INTRO)
for title, body in CONTINGENT:
    gold_subhead(pdf, title)
    para(pdf, body)

section_bar(pdf, "Terms & Conditions")
for t in TERMS:
    bullet(pdf, t)

signature_blocks(pdf)

pdf.output(str(OUT))
print(f"WROTE: {OUT}")
print(f"  Subtotal:   {usd(SUBTOTAL_AMT)}")
print(f"  Tax 10.3%:  {usd(TAX_AMOUNT)}")
print(f"  Total:      {usd(TOTAL)}")
