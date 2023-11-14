from flask import Flask, request
import threading
import pyautogui
import numpy as np
from tensorflow.keras.models import load_model
import joblib
import time

# Cargar el modelo entrenado y el label encoder
model = load_model('gesture_recognition_model.h5')
label_encoder = joblib.load('label_encoder.pkl')
app = Flask(__name__)
pyautogui.FAILSAFE = False

datos = []
gyro = [0, 0]
presentacion_switch = False

def presentaciones():
    global datos
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
    predicted_label = label_encoder.inverse_transform(np.argmax(predictions, axis=1))[0]
        
        # Imprimir la predicción
    print(f"Movimiento detectado: {predicted_label}")
                        
    if predicted_label == "R":
        pyautogui.press('right')
        # time.sleep(0.2)
        # pyautogui.keyUp('right')
    elif predicted_label == "D":
        print("Nada")
    elif predicted_label == "U":
        print("Nada")
    elif predicted_label == "L":
        pyautogui.press('left')
        # time.sleep(0.2)
        # pyautogui.keyUp('left')
    elif predicted_label == "F":
        print("Nada")

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
    predicted_label = label_encoder.inverse_transform(np.argmax(predictions, axis=1))[0]
        
        # Imprimir la predicción
    print(f"Movimiento detectado: {predicted_label}")
                        
    if predicted_label == "R":
        pyautogui.hotkey('alt', 'tab')
    elif predicted_label == "D":
        pyautogui.press('volumedown')
    elif predicted_label == "U":
        pyautogui.press('volumeup')
    elif predicted_label == "L":
        pyautogui.press('volumemute')
    elif predicted_label == "F":
        print("Nada")

@app.route('/', methods=['POST'])
def receive_data():
    global datos, gyro, presentacion_switch
    try:
        data = request.get_json(force=True)
        vx = int(data[0]) * 2.8
        vy = int(data[1]) * 2.2
        gesto = int(data[2])
        click = int(data[4])
        presentacion = int(data[3])
        gyro = [vx, vy]

        if len(datos) <= 11:
            datos.append(gyro)

        if len(datos) > 11:
            del datos[0]
            del datos[1]

        if (presentacion_switch == False) and (gesto == 1):
            thread = threading.Thread(target=gestos_normales)
            
            thread.start()
        
        if presentacion == True:
            presentacion_switch = not presentacion_switch
            print(presentacion_switch)
        
        if (presentacion_switch == True) and (gesto == 1):
            thread = threading.Thread(target=presentaciones)
            
            thread.start()

        if click == 1:
            pyautogui.click()


        # Mover el mouse suavizado
        pyautogui.move(vx, vy)
                        
        return 'Data received successfully', 200
    except Exception as e:
        return f'Error: {str(e)}', 400
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
