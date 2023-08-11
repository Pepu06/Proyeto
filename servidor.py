from flask import Flask, request
import pyautogui as pa

app = Flask(__name__)

# Disable PyAutoGUI fail-safe
pa.FAILSAFE = False
pa.moveTo(683, 384)

@app.route('/', methods=['POST', 'GET'])
def receive_data():
    data = request.form.get('data').split(',')
    if data and len(data) >= 2:
        print(data)
        try:
            acel_x = float(data[0])
            acel_y = float(data[1])
            print(f"Aceleración X: {acel_x}, Aceleración Y: {acel_y}")

            # Mapping range for accelerometer data in X and Y axes
            rango_ac_x = 32767  # Adjust as per X-axis accelerometer range
            rango_ac_y = 32767  # Adjust as per Y-axis accelerometer range

            #Toma el rango de la pantalla
            rango_mouse_x, rango_mouse_y = pa.size()

            cambio_x = (acel_x / rango_ac_x) * rango_mouse_x
            cambio_y = (acel_y / rango_ac_y) * rango_mouse_y

            # Obtiene la posición actual del mouse
            x_actual, y_actual = pa.position()

            # Calcula la nueva posición del mouse
            nueva_x = x_actual + cambio_x
            nueva_y = y_actual + cambio_y

            # Mueve el mouse a la nueva posición
            pa.moveTo(nueva_x, nueva_y, 0.2)
            
            return "Mouse movido correctamente"
        except ValueError:
            return "Datos incorrectos: deben ser números"
    else:
        return "No se recibieron datos o los datos son incorrectos"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)