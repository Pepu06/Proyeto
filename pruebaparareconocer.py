from flask import Flask, request
import pyautogui as pa
import numpy as np
from tensorflow.keras.models import load_model
import joblib

app = Flask(__name__)

# Cargar el modelo entrenado y el label encoder
model = load_model('gesture_recognition_model.h5')
label_encoder = joblib.load('label_encoder.pkl')

# Disable PyAutoGUI fail-safe
pa.FAILSAFE = False
pa.moveTo(683, 384)

@app.route('/', methods=['POST'])
def receive_data():
    try:
        data = request.json
        if data:
            print(data)  # Load JSON data from the request

            
            
            # acel_x = data[0]
            # acel_y = data[1]
            # acel_z = data[2]
            # gyro_x = data[3]
            # gyro_y = data[4]
            # gyro_z = data[5]

            # print(acel_x, acel_y, acel_z, gyro_x, gyro_y, gyro_z)


        #     while True:
        #         try:
        #             input("Presiona Enter para realizar el gesto...")
        #             print("Esperando 1 segundo para el gesto...")
        #             time.sleep(0.5)  # Esperar 0.5 segundos
        
        #             print("Realizando el gesto...")

        #             data = list(map(int, line.split(',')))
        #             # Preprocesar los datos de prueba
        #             x_padded = np.array([data])
        
        # # Realizar la predicción
        #             predictions = model.predict(x_padded)
        
        # # Decodificar las predicciones usando el label encoder
        #             predicted_labels = label_encoder.inverse_transform(np.argmax(predictions, axis=1))
        
        # # Imprimir la predicción
        #             print(f"Movimiento detectado: {predicted_labels[0]}")

        #         except KeyboardInterrupt:
        #             # Detener el bucle con Ctrl+C
        #             break
        #         except Exception as e:
        #             print(f"Error: {e}")

            return "Data received successfully", 200
        else:
            return "Invalid JSON data", 400

    except Exception as e:
        return str(e), 500 

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)