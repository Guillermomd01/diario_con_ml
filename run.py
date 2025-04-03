from datetime import datetime
from flask import Flask, redirect, render_template, request, url_for
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
    """matplotlib.use('Agg')  
    import matplotlib.pyplot as plt
    import os
    emociones = db.session.query(Diario.emocion,Diario.id).all()
    
    if emociones:
        id = [e[1] for e in emociones]
        emociones_lista = [e[0] for e in emociones]
        plt.scatter(id, emociones_lista, color='blue', alpha=0.5)
        plt.title('Estadistica de emociones')
        plt.xlabel('ID de la entrada')
        plt.ylabel('Emocion ')
        plt.grid(True)
        
        grafica = 'grafica_emociones.png'
        plt.savefig(os.path.join('app/static', grafica))
        plt.close()"""
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

if __name__=="__main__":
    db.Base.metadata.create_all(bind=db.engine)
    app.run(debug=True)
