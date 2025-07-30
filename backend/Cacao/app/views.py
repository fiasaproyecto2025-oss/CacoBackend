from django.shortcuts import render
import joblib
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings
import os

# 🔍 Mensaje de depuración: Inicia carga del modelo
print("[DEBUG] Iniciando la carga del modelo...")

# Cargar el modelo .pkl
try:
    model_path = os.path.join(settings.STATICFILES_DIRS[0], 'models', 'modelo_Cacao.pkl')
    model = joblib.load(model_path)
    print(f"[DEBUG] Modelo cargado exitosamente desde: {model_path}")
except FileNotFoundError as e:
    print(f"[ERROR] No se encontró el archivo del modelo en: {model_path}")
    raise e
except Exception as e:
    print(f"[ERROR] Error inesperado al cargar el modelo: {str(e)}")
    raise e

# Definir los nombres de las variables de salida
output_columns = [
    'Altura de planta AP', 'Diametro de tallo DT', 'Numero de ramas NR'
]
						

@api_view(['POST'])
def predict_cacao(request):
    try:
        # 🔍 Depuración: Ver datos recibidos
        print("[DEBUG] Datos recibidos en la solicitud:", request.data)

        # Obtener los datos del cuerpo de la solicitud
        data = request.data

        # Asegurar que los valores sean numéricos
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

        # 🔍 Depuración: Ver datos que entran al modelo
        print("[DEBUG] Características para la predicción:", features)

        # Realizar la predicción
        prediction = model.predict([features])  # Devuelve un array 2D
        print("[DEBUG] Predicción realizada con éxito:", prediction)

        # Convertir la predicción en un diccionario con nombres de variables
        prediction_dict = {}
        
        # Guardar valores específicos de altura, diámetro y número de ramas
        prediction_dict["Altura de planta AP"] = prediction[0][0]
        prediction_dict["Diametro de tallo DT"] = prediction[0][1]
        prediction_dict["Numero de ramas NR"] = prediction[0][2]

        print("Variables:", prediction_dict)
        return Response({'prediction': prediction_dict})

    except KeyError as e:
        error_message = f"Falta la clave requerida en los datos: {str(e)}"
        print(f"[ERROR] {error_message}")
        return Response({'error': error_message})

    except Exception as e:
        print(f"[ERROR] Error durante la predicción: {str(e)}")
        return Response({'error': str(e)})