from flask import Flask, request
import numpy as np
from tensorflow.keras.models import load_model
import pyautogui as pa
import joblib
import time

app = Flask(__name__)
model = load_model('gesture_recognition_model.h5')
label_encoder = joblib.load('label_encoder.pkl')

mouse_active = True
pa.FAILSAFE = False

@app.route('/', methods=['POST'])
def receive_data():
    global mouse_active

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

            # if max_probability >= 0.8:
            #     # Imprimir la predicción
            #     print(f"Movimiento detectado: {predicted_label}")

            #     if predicted_label == "R":
            #         pa.hotkey('alt', 'tab')
            #         mouse_active = False
            #     elif predicted_label == "D":
            #         pa.press('volumeup')
            #         mouse_active = False
            #     else:
            #         # Si no se detecta un gesto conocido, activa el control del mouse
            #         mouse_active = True
            if mouse_active:
            #     if mouse_active:
            #         # Controlar el mouse si está activado
                controlar_mouse(nueva_lista)
            else:
                print("No gesture detected")
            return "Data received successfully", 200
        else:
            return "Invalid JSON data", 400
    except Exception as e:
        return str(e), 500

def controlar_mouse(nueva_lista):
    try:
        x, y = nueva_lista[4], nueva_lista[5]  # Suponiendo que los datos del sensor incluyen las coordenadas x e y
        # Ajusta la sensibilidad según tus necesidades
        SENSITIVITY = 100
        x_movimiento = x * SENSITIVITY
        y_movimiento = y * SENSITIVITY

        # Obtiene la posición actual del mouse
        current_x, current_y = pa.position()

        # Calcula la nueva posición del mouse
        new_x = current_x + x_movimiento
        new_y = current_y + y_movimiento

        # Mueve el cursor del mouse a la nueva posición
        pa.moveTo(new_x, new_y)

    except Exception as e:
        print("Error al controlar el mouse:", str(e))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)