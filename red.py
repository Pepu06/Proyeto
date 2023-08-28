import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from keras.utils import to_categorical
from keras.models import Sequential
from keras.layers import Dense
from sklearn.model_selection import train_test_split
import joblib
import matplotlib.pyplot as plt
from keras.models import load_model

# Cargar los datos desde el archivo CSV
data = pd.read_csv('datos_arduino_completo.csv')

mov = data.groupby('Gesture')

tipos = []

for gesture, group_data in mov:
    try:
        tipo = group_data["Type"].iloc[1]
        if tipo is not None:
            tipos.append(tipo)
    except Exception as e:
        print(f"Error en el grupo {gesture}: {e}. Se salteará este grupo.")
        continue

x = [np.array(mov.get_group(g).drop(["Gesture", "Type", "Time"], axis=1)).flatten() for g in data["Gesture"].unique()]

# Encontrar la longitud máxima
max_length = max(len(sample) for sample in x)

# Rellenar los datos para que tengan la misma longitud
x_padded = np.array([np.pad(sample, (0, max_length - len(sample))) for sample in x])

y = tipos

label_encoder = LabelEncoder()
encoded_y = label_encoder.fit_transform(y)

# Convertir las etiquetas a codificación one-hot
one_hot_y = to_categorical(encoded_y)

# Dividir los datos en conjuntos de entrenamiento y prueba
x_train, x_test, y_train, y_test = train_test_split(x_padded, one_hot_y, test_size=0.2, random_state=42)

# Definir la arquitectura de la red neuronal
model = Sequential()
model.add(Dense(64, input_dim=x_train.shape[1], activation='relu'))
model.add(Dense(32, activation='relu'))
model.add(Dense(len(label_encoder.classes_), activation='softmax'))  # Capa de salida con activación softmax

model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# Entrenar el modelo
history = model.fit(x_train, y_train, epochs=50, batch_size=16, validation_split=0.2)

# Evaluar el modelo en los datos de prueba
loss, accuracy = model.evaluate(x_test, y_test)
print("Porcentaje de precisión en los datos de prueba:", accuracy * 100, "%")

# Visualizar el historial de pérdida
# plt.xlabel("# Época")
# plt.ylabel("Magnitud de pérdida")
# plt.plot(history.history["loss"])
# plt.show()

# Guardar el modelo entrenado
model.save('gesture_recognition_model.h5')

# Guardar el label encoder para uso futuro en la inferencia
joblib.dump(label_encoder, 'label_encoder.pkl')
