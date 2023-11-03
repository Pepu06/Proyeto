import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from keras.utils import to_categorical
from keras.models import Sequential
from keras.layers import Dense
import joblib
from sklearn.model_selection import KFold

# Cargar los datos desde el archivo CSV
data = pd.read_csv('datos.csv')

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

# Definir la arquitectura de la red neuronal
model = Sequential()
model.add(Dense(64, input_dim=x_padded.shape[1], activation='relu'))
model.add(Dense(32, activation='relu'))
model.add(Dense(len(label_encoder.classes_), activation='softmax'))  # Capa de salida con activación softmax

model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# Configuración de validación cruzada k-fold
k_fold = KFold(n_splits=10, shuffle=True, random_state=42)

# Lista para almacenar las puntuaciones de precisión en cada división
scores = []

# Realizar la validación cruzada k-fold
for train_indices, test_indices in k_fold.split(x_padded):
    x_train, x_test = x_padded[train_indices], x_padded[test_indices]
    y_train, y_test = one_hot_y[train_indices], one_hot_y[test_indices]

    # Entrenar el modelo en esta división
    history = model.fit(x_train, y_train, epochs=50, batch_size=16, validation_split=0.2)

    # Evaluar el modelo en los datos de prueba de esta división
    _, accuracy = model.evaluate(x_test, y_test)
    scores.append(accuracy)

# Calcular y mostrar la precisión promedio
mean_accuracy = np.mean(scores)
print(f"Precisión promedio en {k_fold.n_splits}-fold cross-validation: {mean_accuracy * 100:.2f}%")

# Guardar el modelo entrenado
model.save('gesture_recognition_model.h5')

# Guardar el label encoder para uso futuro en la inferencia
joblib.dump(label_encoder, 'label_encoder.pkl')