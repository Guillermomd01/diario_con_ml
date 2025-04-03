from datetime import datetime
from flask import Flask, redirect, render_template, request, url_for,session
from app.models import Diario
from app.model_mL.predictor import prediccion_diario
from app import db
from plotly import utils
from json import dumps
import pandas as pd

app=Flask(__name__,template_folder='app/templates',static_folder='app/static')

@app.route("/")
def home():
    import matplotlib
    import plotly.express as px
    
    emociones = db.session.query(Diario.emocion,Diario.id).all()    
    texto = db.session.query(Diario.frase).all()
    id = [e[1] for e in emociones]
    emociones_lista = [e[0] for e in emociones]
    entrada = [t[0] for t in texto]  
        
    df_plot = pd.DataFrame({
    'ID': id,
    'Emocion': emociones_lista,
    'Frase':entrada
    })

    import plotly.express as px

    fig = px.scatter(df_plot, x='ID', y='Emocion',title='Distribucion de emociones',hover_data={'ID': False, 'Emocion': False,'Frase':True} )

    graph_html = fig.to_html(full_html=False)
    return render_template('index.html',chart_image=graph_html )

@app.route("/crear-entrada",methods=["POST"])
def crear():
    
    pred_emocion = prediccion_diario(texto = request.form["sentimientos"])
    
    fecha_obj = datetime.today()
    entrada = Diario(frase=request.form["sentimientos"],emocion=pred_emocion,fecha=fecha_obj)
    db.session.add(entrada)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/pop_up',methods=['POST'])
def pop_up():
    
    
    frase  = request.form(['sentimientos'])
    emocion = session.get('pred_emocion')
    
    consejos = {
    'tristeza':'Es normal tener dias tristes, aprender de ellos te ayudsará mucho',
    'felicidad': 'Disfruta este momento de algria al máximo',
    'amor': 'Dicen que el amor mueve montañas.¿Será verdad?',
    'enfado': 'La mejor forma de reducir el enfado es respirar hasta 10',
    'miedo': 'EL ser humano solo tiene dos miedos innatos: A las alturas y a los ruidos fuertes',
    'sorpresa':'Las sorpresas no te las esperas'
    }
    
    consejo = consejos.get(emocion)
    
    return render_template('index.html',frase=frase,emocion=emocion,consejo=consejo)

if __name__=="__main__":
    db.Base.metadata.create_all(bind=db.engine)
    app.run(debug=True)
