from datetime import datetime
from flask import Flask, redirect, render_template, request, url_for
from app.models import Diario
from app.model_mL.predictor import prediccion_diario
from app import db


app=Flask(__name__)

@app.route("/")
def home():

    return render_template("index.html")

@app.route("/crear-entrada",methods=["POST"])
def crear():
    
    pred_emocion = prediccion_diario(texto = request.form["sentimientos"])
    
    fecha_obj = datetime.today()
    entrada = Diario(frase=request.form["sentimientos"],emocion=pred_emocion,fecha=fecha_obj)
    app.db.session.add(entrada)
    db.session.commit()
    return redirect(url_for('home'))

if __name__=="__main__":
    db.Base.metadata.create_all(bind=db.engine)
    app.run(debug=True)
