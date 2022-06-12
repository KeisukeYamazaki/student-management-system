import datetime
import glob
import os
import pathlib
import smtplib
from email.mime.text import MIMEText
from email.utils import formatdate
import ssl


FROM_ADDRESS = 'www.sunnyday.com'
MY_PASSWORD = 'google0com'
TO_ADDRESS = 'nickname_please@yahoo.co.jp'
BCC = ''
SUBJECT = 'smsログ'
BODY = ''


def create_message(from_addr, to_addr, bcc_addrs, subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Bcc'] = bcc_addrs
    msg['Date'] = formatdate()
    return msg


def send(from_addr, to_addrs, msg):
    smtpobj = smtplib.SMTP_SSL('smtp.gmail.com', 465, context=ssl.create_default_context(), timeout=10)
    smtpobj.login(FROM_ADDRESS, MY_PASSWORD)
    smtpobj.sendmail(from_addr, to_addrs, msg.as_string())
    smtpobj.close()


def send_log_mail():
    text = ''
    now = datetime.datetime.now()
    two_days = datetime.timedelta(days=2)
    # プロジェクトのルートディレクトリからlogsに移動(sms)
    os.chdir("logs")
    # logsの中のファイル名をリストで全て取得
    files = glob.glob("*")
    for log in files:
        p = pathlib.Path(log)
        # ログファイルが作られた時間をbtに設定
        bt = datetime.datetime.fromtimestamp(p.stat().st_mtime)
        # 2日以内に作られたファイルは読み込み、textに加える
        if bt > now - two_days:
            with open(log, 'r') as f:
                for line in f:
                    text += line
                # ファイルとファイルの間には2行の改行を入れる
                text += '\n\n'

    to_addr = TO_ADDRESS
    subject = SUBJECT
    body = text
    # ログファイルのtextをメールで送る
    msg = create_message(FROM_ADDRESS, to_addr, BCC, subject, body)
    send(FROM_ADDRESS, to_addr, msg)
