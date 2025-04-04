from datetime import datetime
from flask import Flask, render_template, request, session
from app.models import Diario
from app.model_mL.predictor import prediccion_diario
from app import db
import pandas as pd
import plotly.express as px

app=Flask(__name__,template_folder='app/templates',static_folder='app/static')

#Funcion para genearar grafico interactivo
def generar_grafico():
    datos = db.session.query(Diario.emocion,Diario.id,Diario.frase).all()
    emocion = [e[0] for e in datos]
    id = [i[1] for i in datos ]
    frase = [f[2] for f in datos]
    df_grafico = pd.DataFrame({
        'Id':id,
        'Frase':frase,
        'Emocion':emocion
    })
    fig = px.scatter(df_grafico,x='Id', y='Emocion',title='Estadistica de emociones', hover_data={'Id': False, 'Emocion': False,'Frase':True} )
    
    return fig.to_html(full_html=False)

#Creamos la home 
@app.route("/")
def home():
    graph_html= generar_grafico()
    
    return render_template('index.html',chart_image=graph_html )

#ruta que crear la entrada y devuelve popup y grafica
@app.route("/crear-entrada",methods=["POST"])
def crear():
    
    pred_emocion = prediccion_diario(texto = request.form["sentimientos"])
    
    fecha_obj = datetime.today()
    entrada = Diario(frase=request.form["sentimientos"],emocion=pred_emocion,fecha=fecha_obj)
    db.session.add(entrada)
    db.session.commit()

    consejos = {
    'tristeza':'Es normal tener dias tristes, aprender de ellos te ayudsará mucho',
    'felicidad': 'Disfruta este momento de alegria al máximo',
    'amor': 'Dicen que el amor mueve montañas.¿Será verdad?',
    'enfado': 'La mejor forma de reducir el enfado es respirar hasta 10',
    'miedo': 'El ser humano solo tiene dos miedos innatos: A las alturas y a los ruidos fuertes',
    'sorpresa':'Las sorpresas no te las esperas'
    }
    
    consejo = consejos.get(pred_emocion)
    graph_html= generar_grafico()

    return render_template('index.html',frase=request.form["sentimientos"],emocion=pred_emocion,consejo=consejo,chart_image=graph_html)

        
if __name__=="__main__":
    db.Base.metadata.create_all(bind=db.engine)
    app.run(debug=False)
