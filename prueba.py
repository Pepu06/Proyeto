from flask import Flask, request
import pyautogui as pa

app = Flask(__name__)

pa.FAILSAFE = False
pa.moveTo(683, 384)

@app.route('/', methods=['POST'])
def receive_data():
    try:
        data = request.form.to_dict()  # Convert form data to dictionary
        acel_x = float(data.get('accelerometer_x', 0))
        acel_y = float(data.get('accelerometer_y', 0))
        acel_z = float(data.get('accelerometer_z', 0))
        gyro_x = float(data.get('gyro_x', 0))
        gyro_y = float(data.get('gyro_y', 0))
        gyro_z = float(data.get('gyro_z', 0))

        print("Acelerómetro X:", acel_x)
        print("Acelerómetro Y:", acel_y)
        print("Acelerómetro Z:", acel_z)
        print("Giroscopio X:", gyro_x)
        print("Giroscopio Y:", gyro_y)
        print("Giroscopio Z:", gyro_z)

        rango_ac_x = 32767
        rango_ac_y = 32767
        rango_mouse_x, rango_mouse_y = pa.size()

        cambio_x = (acel_x / rango_ac_x) * rango_mouse_x
        cambio_y = (acel_y / rango_ac_y) * rango_mouse_y

        x_actual, y_actual = pa.position()
        nueva_x = x_actual + cambio_x
        nueva_y = y_actual + cambio_y

        pa.moveTo(nueva_x, nueva_y, 0.2)

        return "Mouse movido correctamente"
    except (ValueError, TypeError):
        return "Datos incorrectos: deben ser números"
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
