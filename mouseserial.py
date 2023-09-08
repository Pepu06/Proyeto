import serial
import pyautogui as pa

# Disable PyAutoGUI fail-safe
pa.FAILSAFE = False
pa.moveTo(683, 384)

# Define the serial port configuration
ser = serial.Serial('COM3', 115200)  # Replace 'COMx' with your Arduino's serial port

while True:
    try:
        # Read data from the Arduino over the serial port
        data = ser.readline().decode().strip().split(',')
        print(data)  # Print the received data

        # Parse the data (assuming it's comma-separated)
        if len(data) > 2:
            acel_x, acel_y, acel_z, gyro_x, gyro_y, gyro_z = map(int, data)

            print(acel_x)

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

    except (ValueError, TypeError) as e:
        print(f"Data error: {e}")
    except Exception as e:
        print(f"Error: {e}")
