import io
import arabic_reshaper
from bidi.algorithm import get_display
from django.conf import settings
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle

FONT_PATH = settings.BASE_DIR / 'fonts' / 'Vazirmatn-Regular.ttf'
pdfmetrics.registerFont(TTFont('Vazirmatn', str(FONT_PATH)))


def fa_text(text):
    """آماده‌سازی متن فارسی برای نمایش صحیح در PDF (اتصال حروف + راست‌به‌چپ)"""
    reshaped = arabic_reshaper.reshape(str(text))
    return get_display(reshaped)


def build_pdf_table(title, headers, rows, footer_text=None):
    """
    ساخت یک PDF شامل عنوان، جدول با سرستون، و در صورت وجود یک خط جمع/توضیح در پایان.
    headers: لیست رشته‌ها
    rows: لیست از لیست‌ها (هر ردیف یک لیست از رشته‌ها)
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=1.5 * cm, leftMargin=1.5 * cm)

    title_style = ParagraphStyle('title', fontName='Vazirmatn', fontSize=16, alignment=1, spaceAfter=20)
    footer_style = ParagraphStyle('footer', fontName='Vazirmatn', fontSize=12, alignment=2, spaceBefore=15)

    elements = [Paragraph(fa_text(title), title_style)]

    table_data = [[fa_text(h) for h in headers]]
    for row in rows:
        table_data.append([fa_text(cell) for cell in row])

    table = Table(table_data, hAlign='CENTER')
    table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Vazirmatn'),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#333333')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
    ]))
    elements.append(table)

    if footer_text:
        elements.append(Spacer(1, 10))
        elements.append(Paragraph(fa_text(footer_text), footer_style))

    doc.build(elements)
    buffer.seek(0)
    return buffer