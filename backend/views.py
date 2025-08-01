from pathlib import Path
import joblib
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Subir hasta carpeta 'App_Caco'
BASE_DIR = Path(__file__).resolve().parent.parent

# Ruta correcta al modelo dentro de App_Caco\Cacao\models\
model_path = BASE_DIR / 'Cacao' / 'models' / 'modelo_Cacao.pkl'

print("[DEBUG] Iniciando la carga del modelo...")
print(f"[DEBUG] Ruta completa del modelo: {model_path}")

try:
    model = joblib.load(model_path)
    print(f"[DEBUG] Modelo cargado exitosamente desde: {model_path}")
except FileNotFoundError as e:
    print(f"[ERROR] No se encontró el archivo del modelo en: {model_path}")
    raise e
except Exception as e:
    print(f"[ERROR] Error inesperado al cargar el modelo: {str(e)}")
    raise e


# Nombres de las variables de salida
output_columns = [
    'Altura de planta AP', 'Diametro de tallo DT', 'Numero de ramas NR'
]

@api_view(['POST'])
def predict_cacao(request):
    try:
        print("[DEBUG] Datos recibidos en la solicitud:", request.data)

        data = request.data

        # Convertir a float y armar las características
        try:
            features = [
                float(data.get('TEMPERATURA_AMBIENTAL', 0)),
                float(data.get('HUMEDAD_AMBIENTAL', 0)),
                float(data.get('HUMEDAD_SUELO', 0)),
                float(data.get('PRESION_ATMOSFERICA', 0)),
                float(data.get('TEMPERATURA_SUELO', 0)),
                float(data.get('INDICE_DE_LLUVIA', 0)),
                float(data.get('GENOTIPO', 0)),
                float(data.get('DIAS', 0)),
                float(data.get('pH', 0)),
                float(data.get('ARENA', 0)),
                float(data.get('LIMO', 0)),
                float(data.get('ARCILLA', 0)),
                float(data.get('CLASETEXTUAL', 0)),
                float(data.get('NITROGENO', 0))
            ]
        except ValueError as e:
            print(f"[ERROR] Error al convertir los datos: {str(e)}")
            return Response({'error': 'Datos inválidos, asegúrese de enviar valores numéricos.'})

        print("[DEBUG] Características para la predicción:", features)

        prediction = model.predict([features])  # Predicción (array 2D)
        print("[DEBUG] Predicción realizada con éxito:", prediction)

        prediction_dict = {
            "Altura de planta AP": prediction[0][0],
            "Diametro de tallo DT": prediction[0][1],
            "Numero de ramas NR": prediction[0][2]
        }

        print("[DEBUG] Variables predichas:", prediction_dict)

        return Response({'prediction': prediction_dict})

    except KeyError as e:
        error_message = f"Falta la clave requerida en los datos: {str(e)}"
        print(f"[ERROR] {error_message}")
        return Response({'error': error_message})

    except Exception as e:
        print(f"[ERROR] Error durante la predicción: {str(e)}")
        return Response({'error': str(e)})
