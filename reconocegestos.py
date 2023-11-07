import serial
import numpy as np
from tensorflow.keras.models import load_model
import pyautogui as pa
import joblib
import time

# Cargar el modelo entrenado y el label encoder
model = load_model('gesture_recognition_model.h5')
label_encoder = joblib.load('label_encoder.pkl')

data = [-63.23,-1.29,-86.77,-2.01,-92.58,-6.11,-108.85,-1.90,-78.53,21.37,-91.93,15.31,-25.58,30.11,-76.47,-0.45,-36.81,6.19,-42.65,-0.73]
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
        pa.press('volumedown')
    if predicted_label == "U":
        pa.press('volumeup')
    if predicted_label == "L":
        pa.press('volumemute')
    if predicted_label == "F":
        pa.press('win')