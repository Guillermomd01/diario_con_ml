from datetime import datetime
from flask import Flask, redirect, render_template, request, url_for
import db
from models import Diario

app=Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/crear-entrada",methods=["POST"])
def crear():
    fecha_obj = datetime.today()
    entrada = Diario(frase=request.form["sentimientos"],emocion=None,fecha=fecha_obj)
    db.session.add(entrada)
    db.session.commit()
    return redirect(url_for('home'))

if __name__=="__main__":
    db.Base.metadata.create_all(bind=db.engine)
    app.run(debug=True)
