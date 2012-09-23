from flask import Flask
import os

app = Flask(__name__)

try:
    with open(app['entropy']) as f:
        entropy = f.read()
except IOError:
    entropy = os.urandom(24)

app.secret_key = entropy

# blueprints

from minestatus.views import server

app.register_blueprint(server.mod)