from models import Diario
from werkzeug.utils import redirect
from flask import Flask, render_template, request, url_for

app = Flask(__name__)
@app.route("/")
def home():
    return render_template("index.html")
