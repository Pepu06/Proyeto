import serial
import pyautogui as pa

# Constants and Configuration
COM_PORT = 'COM3'  # Replace with your Arduino's serial port
BAUD_RATE = 115200
ACCELEROMETER_RANGE = 32767  # Adjust as per accelerometer range
SENSITIVITY_SCALE = 1000000.0  # Adjust this value to control sensitivity

# Disable PyAutoGUI fail-safe
pa.FAILSAFE = False
pa.moveTo(683, 384)
spil = 0

# Define the serial port configuration
ser = serial.Serial(COM_PORT, BAUD_RATE)

while True:
    try:
        # Read data from the Arduino over the serial port
        data = ser.readline().decode().strip().split(',')
        data = [int(x) for x in data]

        # Asegurémonos de que data tenga exactamente 60 elementos
        if len(data) != 60:
            print("El array data debe tener 60 elementos.")
        else:
            # Inicializamos una lista vacía para almacenar los 10 subarrays
            subarrays = []

            # Dividimos data en 10 subarrays de 6 elementos cada uno
            for i in range(10):
                start_idx = i * 6
                end_idx = start_idx + 6
                subarray = data[start_idx:end_idx]
                subarrays.append(subarray)

            # Imprimimos los 10 subarrays
            for i, subarray in enumerate(subarrays):
                print(f"Subarray {i + 1}: {subarray}")

            # Check if the received data has the expected format
            for data in subarrays:
                if len(data) == 6:
                    acel_x, acel_y, acel_z, gyro_x, gyro_y, gyro_z = data

        # Get the screen size
                    screen_width, screen_height = pa.size()

        # Calculate mouse movement with adjusted logic
                    if spil == 0:
                        old_x = acel_z
                        old_z = acel_x
                        spil += 1
                    new_x = acel_x - old_x
                    new_z = acel_z - old_z
                    mouse_x = (new_x / ACCELEROMETER_RANGE) * screen_width
                    mouse_y = (new_z / ACCELEROMETER_RANGE) * screen_height
                    pa.move(mouse_x, -mouse_y, 0,1)
                    old_x = new_x
                    old_z = new_z

    except (ValueError, TypeError) as e:
        print(f"Data error: {e}")
    except Exception as e:
        print(f"Error: {e}")