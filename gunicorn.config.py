import os.path

base_path = os.path.split(os.path.abspath(__file__))[0]

bind = '0.0.0.0:9600'
workers = 1
keepalive = 1
#user = 'minestatus'
errorlog = os.path.join(base_path, 'log/error.log')
loglevel = 'warning'
proc_name = 'minecheck gunicorn'
