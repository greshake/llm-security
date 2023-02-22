from flask import Flask
from injection import Needle

needle = Needle()
app = Flask(__name__)