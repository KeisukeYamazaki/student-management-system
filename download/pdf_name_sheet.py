import glob
import os

import PyPDF2
from reportlab.lib.colors import black
from reportlab.lib.pagesizes import B4
from reportlab.platypus import Table
from reportlab.platypus import TableStyle

from download.pdf_utils import init_pdf, draw_h_line
from download.pdf_utils import MarginFrame


def count_up():
    x = 0
    while True:
        yield x
        x += 1


def merge_pdf_in_dir(file_name):
    # pdf拡張子のファイルを取得
    files = glob.glob('*.pdf')
    # 並べ替える
    files.sort()

    # 結合する
    merger = PyPDF2.PdfFileMerger()
    for pdf in files:
        if not PyPDF2.PdfFileReader(pdf).isEncrypted:
            merger.append(pdf)
    # 保存
    merger.write(file_name)
    merger.close()


def delete_files(filename):
    # ファイルの取得
    file_list = glob.glob(filename)
    # ファイルを削除
    for file in file_list:
        os.remove(file)


def make_pdf_name_sheets(file_name, home_room, students):

    heavy = 'Heavy'
    medium = 'Medium'
    normal = 'Normal'
    light = 'Light'

    # 土台を作成
    c = init_pdf(file_name, B4, ls=True)

    # B4余白少なめ
    margin_frame = MarginFrame(30, 970, 680, 30)

    # 方眼
    # margin_frame.set_grid(c, light)

    # メモ欄の作成
    memo = [['メモ']]
    table = Table(memo, colWidths=margin_frame.right_limit - margin_frame.left_limit, rowHeights=170)
    table.setStyle(TableStyle([
        ('FONT', (0, 0), (0, 0), normal, 9),
        ('BOX', (0, 0), (0, 0), 0.75, black),
        ("VALIGN", (0, 0), (0, 0), "TOP"),
        ("ALIGN", (0, 0), (0, 0), "LEFT"),
    ]))
    table.wrapOn(c, 30, 30)
    table.drawOn(c, 30, 30)

    # 表を作成
    data = []
    for i in range(23):
        rows = []
        for j in range(39):
            rows.append('')
        data.append(rows)

    # データ挿入1
    data[0][0] = '日付'

    # データ挿入2
    for i in range(2):
        for j in range(4, 39, 7):
            data[i][j] = '/' if i == 0 else 'HR'

    # データ挿入3
    data[1][0] = home_room

    # データ挿入4
    data[2][0] = '　/　　　〜'

    # データ挿入5
    for i in range(5, 39):
        if i % 7 == 4:
            continue
        if i == 5:
            string = '点'
        elif string == '点':
            string = '宿'
        else:
            string = '点'
        data[2][i] = string

    # データ挿入6: インデックス番号
    for i in range(1, 21):
        data[i + 2][0] = i

    # データ挿入7: 名前
    i = 3
    for student in students:
        data[i][1] = '{} {}'.format(student.last_name, student.first_name)
        i += 1

    # 列幅の設定
    col_width = [15]  # １列目
    for _ in range(38):
        col_width.append(24.3)

    table = Table(data, colWidths=col_width, rowHeights=20)

    # スタイルの設定
    COL_MAX = 38
    ROW_MAX = 22
    style_list = [
        ('FONT', (0, 0), (COL_MAX, ROW_MAX), normal, 9),
        ('FONT', (0, 1), (0, 1), medium, 14),  # クラス
        ('FONT', (1, 3), (3, ROW_MAX), normal, 10),  # 名前
        ('BOX', (0, 0), (COL_MAX, ROW_MAX), 0.75, black),
        ('BOX', (0, 3), (3, ROW_MAX), 1.75, black),  # 1〜4列目
        ('BOX', (0, 0), (COL_MAX, 0), 1.75, black),  # 1行目
        ('BOX', (0, 0), (COL_MAX, 2), 1.75, black),  # 1〜3行目
        ('INNERGRID', (4, 0), (COL_MAX, ROW_MAX), 0.75, black),
        ('INNERGRID', (0, 3), (COL_MAX, ROW_MAX), 0.75, black),
        ('VALIGN', (0, 0), (COL_MAX, ROW_MAX), 'MIDDLE'),
        ('ALIGN', (0, 0), (COL_MAX, ROW_MAX), 'CENTER'),
        ('ALIGN', (0, 2), (0, 2), 'RIGHT'),  # / ~
    ]

    # 太線: 日付の区切り(5〜11列目以降)
    i = 4
    while i < 38:
        if not i == 4:
            i += 1
        box = ('BOX', (i, 0), (i + 6, 22), 1.75, black)
        style_list.append(box)
        i += 6

    # セル結合1: 日付、クラス、 / ~
    for i in range(3):
        span = ('SPAN', (0, i), (3, i))
        style_list.append(span)

    # セル結合2: 1行目-日付記入欄
    i = 4
    while i < 38:
        if not i == 4:
            i += 1
        span = ('SPAN', (i, 0), (i + 6, 0))
        style_list.append(span)
        i += 6

    # セル結合3: HR
    for i in range(4, 39, 7):
        span = ('SPAN', (i, 1), (i, 2))
        style_list.append(span)

    # セル結合4: 2行目-科目記入欄
    i = 5
    while i < 38:
        if i % 7 == 4:
            i += 1
            continue
        span = ('SPAN', (i, 1), (i + 1, 1))
        i += 2
        style_list.append(span)

    # セル結合5: 名前欄
    for i in range(3, 23):
        span = ('SPAN', (1, i), (3, i))
        style_list.append(span)

    table.setStyle(TableStyle(style_list))

    table.wrapOn(c, 30, 220)
    table.drawOn(c, 30, 220)

    draw_h_line(c, 0.75, 90, 30, 640, set_dash=True)

    # Canvasに書き込み
    c.showPage()
    # ファイル保存
    c.save()
