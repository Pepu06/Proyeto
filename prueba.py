import serial
import numpy as np
from tensorflow.keras.models import load_model
import pyautogui as pa
import joblib
import time

# Cargar el modelo entrenado y el label encoder
model = load_model('gesture_recognition_model.h5')
label_encoder = joblib.load('label_encoder.pkl')

data = [-4528,-12508,8516,3378,-277,3275,-4244,-12288,8652,4023,1027,3639,-5020,-11896,9268,4203,-286,3867,-5420,-10984,9832,3966,182,4000,-7112,-10644,10992,4725,-1593,4351,-4688,-9924,10764,2426,-910,3948,-6792,-9860,10720,3150,-388,3927,-6336,-9284,10480,3757,-108,3880,-7188,-8868,11816,3352,693,3570,-7612,-8024,12132,3112,661,3641]
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