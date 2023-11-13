from flask import Flask, request, jsonify
import pyautogui
import numpy as np
import pyautogui as pa
from tensorflow.keras.models import load_model
import joblib
import time

# Cargar el modelo entrenado y el label encoder
model = load_model('gesture_recognition_model.h5')
label_encoder = joblib.load('label_encoder.pkl')
app = Flask(__name__)
pyautogui.FAILSAFE = False


datos = []
@app.route('/', methods=['POST'])
def receive_data():
    global datos
    try:
        data = request.get_json(force=True)  # Indica que se espera un JSON
        flattened_datos = []

        vx = int(data[0]) * 2.8
        vy = int(data[1]) * 2.2
        alternar = int(data[2])
        presentacion = int(data[3])

        gyro = [vx, vy]

        if (len(datos) <= 11):
            datos.append(gyro)

        if(len(datos) > 11):
            del datos[0]
            del datos[1]

        def gestos_normales():
            for _ in range(10):
                if len(datos) <= 11:
                    datos.append(gyro)

                if len(datos) > 11:
                    del datos[0]
                    del datos[1]

                flattened_datos = [item for sublist in datos for item in sublist]

            x_padded = np.array([flattened_datos])
            predictions = model.predict(x_padded)
            
            # Obtener la probabilidad máxima de predicción
            #max_probability = np.max(predictions)
            predicted_label = label_encoder.inverse_transform(np.argmax(predictions, axis=1))[0]
            
            #if max_probability >= 0.9:
            # Imprimir la predicción
            print(f"Movimiento detectado: {predicted_label}")
                            
            if predicted_label == "R":
                pa.hotkey('alt', 'tab')
            if predicted_label == "D":
                pa.press('volumedown')
            if predicted_label == "U":
                pa.press('volumeup')
            if predicted_label == "L":
                pa.press('volumemute')
            if predicted_label == "F":
                print("Nada")

        def gestos_presentacion():
            x_padded = np.array([flattened_datos])
            predictions = model.predict(x_padded)
            
            # Obtener la probabilidad máxima de predicción
            max_probability = np.max(predictions)
            predicted_label = label_encoder.inverse_transform(np.argmax(predictions, axis=1))[0]
            
            if max_probability >= 0.9:
            # Imprimir la predicción
                print(f"Movimiento detectado: {predicted_label}")
                            
                if predicted_label == "R":
                    pa.hotkey('alt', 'tab')
                if predicted_label == "D":
                    pa.press('volumedown')
                if predicted_label == "U":
                    pa.press('volumeup')
                if predicted_label == "L":
                    pa.press('volumemute')
                if predicted_label == "F":
                    print("Nada")


        if (alternar == 1):
            gestos_normales()

        #if(presentacion == 1):
        #    gestos_presentacion()

        
        # Mover el mouse suavizado
        pyautogui.move(vx, vy)
                        
        return 'Data received successfully', 200
    except Exception as e:
        return f'Error: {str(e)}', 400
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)  # Ejecuta Flask en el puerto 8080
