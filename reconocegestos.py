import serial
import numpy as np
from tensorflow.keras.models import load_model
import pyautogui as pa
import joblib
import time

# Cargar el modelo entrenado y el label encoder
model = load_model('gesture_recognition_model.h5')
label_encoder = joblib.load('label_encoder.pkl')

# Inicializar la conexión con el puerto serial del Arduino
arduino_port = 'COM3'  # Cambiar al puerto correcto en tu sistema
baud_rate = 115200
ser = serial.Serial(arduino_port, baud_rate, timeout=1)

# Leer datos del puerto serial y predecir gestos
while True:
    try:
        input("Presiona Enter para realizar el gesto...")
        print("Esperando 1 segundo para el gesto...")
        time.sleep(0.5)  # Esperar 0.5 segundos
        
        print("Realizando el gesto...")

        # Leer todas las líneas disponibles en el puerto serial y quedarse con la última
        while ser.in_waiting:
            line = ser.readline().decode('utf-8').strip()
        
        data = list(map(int, line.split(',')))
        print(data)
        # Preprocesar los datos de prueba
        x_padded = np.array([data])
        
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
            
    except KeyboardInterrupt:
        # Detener el bucle con Ctrl+C
        break
    except Exception as e:
        print(f"Error: {e}")

# Cerrar la conexión con el puerto serial
ser.close()