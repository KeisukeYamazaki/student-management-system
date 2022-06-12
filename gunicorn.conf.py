# nginxとのデータのやりとりをこのソケットを介して行うために設定する
bind = '127.0.0.1:8000'

# gunicornのワーカープロセスをいくつ起動するかを設定(CPUの数（コアの数）+1ぐらいがいい)
workers = 2

# デフォルトは syncだが、今回は非同期処理のgevent
worker_class = 'gevent'

# デフォルトは30だが、ダウンロード時間が長いものはこれくらい取る
timeout = 60

worker_connections = 1000
max_requests = 1000

# 不具合あったときにTrueにして原因を追及する必要があるが、今はFalse
debug = False

# gunicornがデーモンとして動作するかの設定。
# Trueにしておけば、sshから抜けてもgunicornが起動し続けるため動作する。
daemon = True

# pidファイルの指定
pidfile = '/var/run/sms.pid'

# gunicrornが動作するユーザーとグループを指定
user = 'nginx'
group = 'nginx'

errorlog = '/var/log/gunicorn/sms-error.log'
accesslog = '/var/log/gunicorn/sms-access.log'

loglevel = 'info'
proc_name = 'sms'
