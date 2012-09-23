from flask import Flask
import os

app = Flask(__name__)
app.config.from_object('msconfig')

try:
    with open(app.config['ENTROPY']) as f:
        entropy = f.read()
except IOError:
    if app.config.get('online', False):
        print 'Warning: using os.urandom as secret key'
    
    entropy = os.urandom(24)

app.secret_key = entropy

# blueprints

from minestatus.views import server

app.register_blueprint(server.mod)