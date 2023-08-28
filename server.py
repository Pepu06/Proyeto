from flask import Flask, request
import pyautogui as pa
import json

app = Flask(__name__)

# Disable PyAutoGUI fail-safe
pa.FAILSAFE = False
pa.moveTo(683, 384)

@app.route('/', methods=['POST'])
def receive_data():
    if request.method == 'POST':
        try:
            data = request.get_json()
            print(data)
            text = json.dumps(data, separators=",")
            print(text)  # Load JSON data from the request
            print(type(data[1]))
            
            acel_x = float(data.get('acel_x', 0))
            acel_y = float(data.get('acel_y', 0))
            print(f"Aceleración X: {acel_x}, Aceleración Y: {acel_y}")

            # Mapping range for accelerometer data in X and Y axes
            rango_ac_x = 32767  # Adjust as per X-axis accelerometer range
            rango_ac_y = 32767  # Adjust as per Y-axis accelerometer range

            # Get the screen size
            rango_mouse_x, rango_mouse_y = pa.size()

            cambio_x = (acel_x / rango_ac_x) * rango_mouse_x
            cambio_y = (acel_y / rango_ac_y) * rango_mouse_y

            # Get the current mouse position
            x_actual, y_actual = pa.position()

            # Calculate the new mouse position
            nueva_x = x_actual + cambio_x
            nueva_y = y_actual + cambio_y

            # Move the mouse to the new position
            pa.moveTo(nueva_x, nueva_y, duration=0.2)

            return "Mouse movido correctamente"
        except (ValueError, TypeError) as e:
            return f"Datos incorrectos: {e}"
        except Exception as e:
            return f"Error interno: {e}"
    else:
        return "No se recibieron datos o los datos son incorrectos"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
