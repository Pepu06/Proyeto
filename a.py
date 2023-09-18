from flask import Flask, request
import numpy as np
from tensorflow.keras.models import load_model
import pyautogui as pa
import joblib
import time

app = Flask(__name__)
model = load_model('gesture_recognition_model.h5')
label_encoder = joblib.load('label_encoder.pkl')


@app.route('/', methods=['POST'])
def receive_data():
    print("Hace el gesto ahora")
    time.sleep(100)
    try:
        data = request.json  # Obtener los datos JSON del cuerpo de la solicitud
        if data:
            array = []
            i = 0
            while i < 10:
                array.append(data)
                i = i + 1

            cadena = str(array)
            cadena_sin_corchetes = cadena.replace('[', '').replace(']', '')
            nueva_lista = eval(cadena_sin_corchetes)

            print("Received data:", nueva_lista)
            x_padded = np.array([nueva_lista])
        
            # Realizar la predicción
            predictions = model.predict(x_padded)
        
            # Obtener la probabilidad máxima de predicción
            max_probability = np.max(predictions)
            predicted_label = label_encoder.inverse_transform(np.argmax(predictions, axis=1))[0]
        
            if max_probability >= 0.8:
            # Imprimir la predicción
                print(f"Movimiento detectado: {predicted_label}")
            
                if predicted_label == "R":
                    pa.hotkey('alt', 'tab')
                if predicted_label == "D":
                    pa.press('volumeup')
            else:
                print("No gesture detected")
            time.sleep(5000)
            return "Data received successfully", 200
        else:
            return "Invalid JSON data", 400
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
