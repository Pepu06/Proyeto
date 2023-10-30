from flask import Flask, request, jsonify
import pyautogui
import csv

app = Flask(__name__)
pyautogui.FAILSAFE = False

# Abre un archivo CSV para escribir los datos
csv_filename = 'datos.csv'
csv_file = open(csv_filename, 'w', newline='')
csv_writer = csv.writer(csv_file)

# Escribe encabezados en el archivo CSV
headers = ['Gyro_X', 'Gyro_Y', 'Time', 'Gesture', 'Type']
csv_writer.writerow(headers)

@app.route('/', methods=['POST'])
def receive_data():
    try:
        data = request.get_json(force=True)  # Indica que se espera un JSON
        print(data)
        vx = (data[0] * 3)
        vy = (data[1] * 5)
        time = (data[2])
        gesture = (data[3])
        type = (data[4])

        csv_writer.writerow([vx, vy, time, gesture, type])
        csv_file.flush()  # Forzar escritura en el archivo
        
        # Opcional: muestra los valores de vx y vy en la consola
        print(f"vx: {vx}, vy: {vy}")
        
        return 'Data received successfully', 200
    except Exception as e:
        return f'Error: {str(e)}', 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)  # Ejecuta Flask en el puerto 8080