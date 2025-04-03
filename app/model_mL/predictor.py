import joblib 
import os

# Obtener la ruta al directorio donde están los modelos
modelo_dir = os.path.join(os.path.dirname(__file__), 'model_mL')

# Cargar el modelo y el vectorizador
model_lr = joblib.load(os.path.join(modelo_dir, 'modelo_logistico.pkl'))
vector = joblib.load(os.path.join(modelo_dir, 'vectorizador_tfidf.pkl'))

emociones = {
    0:'tristeza',
    1:'felicidad',
    2:'amor',
    3:'enfado',
    4:'miedo',
    5:'sorpresa'
    }

def prediccion_diario(texto):
    X_vectored = vector.transform([texto])
    prediccion = model_lr.predict(X_vectored)[0]
    return emociones[prediccion]