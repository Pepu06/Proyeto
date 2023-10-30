import tensorflow as tf

# Cargar el modelo de Keras
model = tf.keras.models.load_model('gesture_recognition_model.h5')

# Convertir el modelo a TensorFlow Lite
converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()

# Guardar el modelo de TensorFlow Lite en un archivo .tflite
with open('gesture_recognition_model.tflite', 'wb') as f:
    f.write(tflite_model)
