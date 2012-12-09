from flask import Flask
from flask.ext.bootstrap import Bootstrap

app = Flask(__name__)


app.debug = True

Bootstrap(app)



