import os

from reportlab.lib import colors
from reportlab.lib.colors import gainsboro, black
from reportlab.lib.pagesizes import portrait
from reportlab.lib.pagesizes import landscape
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph
from reportlab.platypus import Table
from reportlab.platypus import TableStyle


base_path = os.getcwd()

GEN_SHIN_GOTHIC_HEAVY_TTF = base_path + "/download/fonts/GenShinGothic-Monospace-Heavy.ttf"
GEN_SHIN_GOTHIC_MEDIUM_TTF = base_path + "/download/fonts/GenShinGothic-Monospace-Medium.ttf"
GEN_SHIN_GOTHIC_NORMAL_TTF = base_path + "/download/fonts/GenShinGothic-Monospace-Normal.ttf"
GEN_SHIN_GOTHIC_LIGHT_TTF = base_path + "/download/fonts/GenShinGothic-Monospace-Light.ttf"


def init_pdf(file_name, size, ls=False):
    """init_pdf

         用紙を作成する

        Args:
            file_name (str): ファイルの名前
            size (str): 用紙のサイズ
            ls (bool): 用紙を横にする(ls=landscape)

        Returns:
           canvas : 土台となる用紙を返す
    """
    # フォント登録
    pdfmetrics.registerFont(TTFont('Heavy', GEN_SHIN_GOTHIC_HEAVY_TTF))
    pdfmetrics.registerFont(TTFont('Medium', GEN_SHIN_GOTHIC_MEDIUM_TTF))
    pdfmetrics.registerFont(TTFont('Normal', GEN_SHIN_GOTHIC_NORMAL_TTF))
    pdfmetrics.registerFont(TTFont('Light', GEN_SHIN_GOTHIC_LIGHT_TTF))

    # 白紙を返す
    if ls:
        return canvas.Canvas(file_name, pagesize=landscape(size))
    return canvas.Canvas(file_name, pagesize=portrait(size))


class MarginFrame:

    def __init__(self, left_limit, right_limit, top_limit, bottom_limit):
        self.left_limit = left_limit
        self.right_limit = right_limit
        self.top_limit = top_limit
        self.bottom_limit = bottom_limit
        self.center = (right_limit + 50) / 2

    def write_string(self, c, font, font_size, width, height, text, line=False):
        """write_string

         文字を書く

        Args:
            c (canvas): 対象のキャンバス
            font (str): フォントの名前
            font_size (int): フォントサイズ
            width (int): 横の位置
            height (int): 縦の位置
            text (str): 記載する文字列
            line (bool, option): 下線の有無(True: あり、False: なし)
        """
        c.setFont(font, font_size)  # setFont(登録済みフォント, サイズ)
        string_width = c.stringWidth(text, font, font_size)
        c.drawString(width, height, text)
        if line:
            c.line(width, height - 3, width + string_width, height - 3)

    def write_string_align(self, c, font, font_size, height, text, line=False, align='LEFT'):
        """write_string_align

         文字を書く（左右中央の指定をする）

        Args:
            c (canvas): 対象のキャンバス
            font (str): フォントの名前
            font_size (int): フォントサイズ
            height (int): 縦の位置
            text (str): 記載する文字列
            line (bool, option): 下線の有無(True: あり、False: なし)
            align (str, option): LEFT: 左寄せ、CENTER: 中央寄せ、RIGHT: 右寄せ
        """
        c.setFont(font, font_size)  # setFont(登録済みフォント, サイズ)
        string_width = c.stringWidth(text, font, font_size)

        if align == 'CENTER':
            c.drawCentredString(self.center, height, text)
        elif align == 'RIGHT':
            width = self.right_limit - string_width
            c.drawString(width, height, text)
        else:
            c.drawString(self.left_limit, height, text)

        if line:
            c.line(width, height - 3, width + string_width, height - 3)

    def set_grid(self, c, font):
        """set_grid

         方眼をセットする

        Args:
            c (canvas): 対象のキャンバス
            font (str): フォントの名前
        """
        c.setStrokeColor(gainsboro)
        c.setFont(font, 5)
        # 縦線
        for i in range(0, 1000, 20):
            if self.left_limit + i < self.right_limit:
                c.line(self.left_limit + i, self.top_limit, self.left_limit + i, self.bottom_limit)
                c.drawString(self.left_limit + i, self.top_limit + 5, str(self.left_limit + i))
            else:
                c.line(self.right_limit, self.top_limit, self.right_limit, self.bottom_limit)
                c.drawString(self.right_limit, self.top_limit + 5, str(self.right_limit))
                break

        # 横線
        for j in range(0, 1000, 20):
            if self.bottom_limit + j < self.top_limit:
                c.line(self.left_limit, self.bottom_limit + j, self.right_limit, self.bottom_limit + j)
                c.drawString(self.left_limit - 10, self.bottom_limit + j, str(self.bottom_limit + j))
            else:
                c.line(self.left_limit, self.top_limit, self.right_limit, self.top_limit)
                c.drawString(self.left_limit - 10, self.top_limit, str(self.top_limit))
                break

    def write_box_string(self, c, font, font_size, leading, text,
                         col_widths, width, height, box=False, margin=True, indent=0, row_heights=0):
        """write_box_string

         ボックスの中にテキストを入れて、配置する

        Args:
            c (canvas): 対象のキャンバス
            font (str): フォントの名前
            font_size (int): フォントサイズ
            leading (int): 行間の幅
            col_widths (int): 横幅
            width (int) : 横の位置
            height (int): 縦の位置
            text (str): 記載する文字列
            box (bool, option): True: 囲み線あり、False: 囲み線なし
            margin(bool, option): True: 左右の余白あり、False: 左右の余白なし
            indent (int, option): 最初の行にあけるマスの大きさ
            row_heights(int, option): ボックスの縦幅
        """

        style = ParagraphStyle(
            name='Normal',
            fontName=font,
            fontSize=font_size,
            leading=leading,
            firstLineIndent=indent,
            justifyLastLine=1
        )

        line1 = Paragraph(text, style)

        data = [
            [line1],
        ]

        if margin:
            if row_heights == 0:
                table = Table(data, colWidths=col_widths)
            else:
                table = Table(data, colWidths=col_widths, rowHeights=row_heights)
        else:
            if row_heights == 0:
                table = Table(data, colWidths=(col_widths + 10))
            else:
                table = Table(data, colWidths=col_widths + 10, rowHeights=row_heights)

        if box:
            table.setStyle(TableStyle([
                ('BOX', (0, 0), (0, 0), 1, colors.black),
                ('VALIGN', (0, 0), (0, 0), 'TOP'),
            ]))
        else:
            table.setStyle(TableStyle([
                ('VALIGN', (0, 0), (0, 0), 'TOP'),
            ]))

        if margin:
            table.wrapOn(c, width, height)
            table.drawOn(c, width, height)
        else:
            table.wrapOn(c, width - 6, height)
            table.drawOn(c, width - 6, height)


def write_string(c, font, font_size, width, height, text, line=False, charspace=0):
    """write_string

         文字を書く

        Args:
            c (canvas): 対象のキャンバス
            font (str): フォントの名前
            font_size (int): フォントサイズ
            width (int): 横の位置
            height (int): 縦の位置
            text (str): 記載する文字列
            line (bool, option): 下線の有無(True: あり、False: なし)
            charspace (int, option): 文字同士の間隔
    """
    text_obj = c.beginText()
    text_obj.setTextOrigin(width, height)
    text_obj.setFont(font, font_size)
    text_obj.setCharSpace(charspace)
    text_obj.textLine(text)
    c.drawText(text_obj)
    if line:
        string_width = c.stringWidth(text, font, font_size)
        c.line(width, height - 3, width + string_width, height - 3)


def write_lines(c, font, font_size, width, length, text, add_leading=2):
    """write_lines

         複数行の文字を書く

        Args:
            c (canvas): 対象のキャンバス
            font (str): フォントの名前
            font_size (int): フォントサイズ
            width (int): 横の位置
            length (int): 縦の位置
            text (str): 記載する文字列
            add_leading (int, option): 追加する行間
    """
    c.setFont(font, font_size)
    text_object = c.beginText()
    text_object.setTextOrigin(width, length)
    text_object.setLeading(font_size + add_leading)  # 行間の幅を指定
    text_object.textLines(text)  # テキストは複数行
    c.drawText(text_object)


def draw_h_line(c, line_wight, length, start_width, start_height, set_dash=False, color=black):
    c.setLineWidth(line_wight)
    c.setStrokeColor(color)
    if set_dash:
        c.setDash(1, 2)  # 点線
        # c.setDash(6, 3)  # 破線
    c.line(start_width, start_height, start_width + length, start_height)


def draw_v_line(c, line_wight, length, start_width, start_height, set_dash=False, color=black):
    c.setStrokeColor(color)
    c.setLineWidth(line_wight)
    if set_dash:
        c.setDash(1, 2)  # 点線
        # c.setDash(6, 3)  # 破線
    c.line(start_width, start_height, start_width, start_height + length)
