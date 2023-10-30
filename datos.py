import serial
import csv

# Configura el puerto serial
arduino_port = 'COM3'  # Puerto COM5 en Windows
baud_rate = 115200     # Asegúrate de que coincide con la velocidad en el Arduino
ser = serial.Serial(arduino_port, baud_rate)

# Abre un archivo CSV para escribir los datos
csv_filename = 'datos_del_arduino.csv'
csv_file = open(csv_filename, 'w', newline='')
csv_writer = csv.writer(csv_file)

# Escribe encabezados en el archivo CSV
headers = ['Accel_X', 'Accel_Y', 'Accel_Z', 'Gyro_X', 'Gyro_Y', 'Gyro_Z', 'Time', 'Gesture', 'Type']
csv_writer.writerow(headers)

try:
    while True:
        # Lee una línea desde el puerto serial
        serial_data = ser.readline().decode().strip()

        print("Received data:", serial_data)

        # Divide los datos en partes (separados por comas)
        data_parts = serial_data.split(',')

        if len(data_parts) == 9:
            accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z, time, gesture, gesture_type = data_parts
            csv_writer.writerow([accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z, time, gesture, gesture_type])
            csv_file.flush()  # Forzar escritura en el archivo

except KeyboardInterrupt:
    # Cierra todo correctamente al presionar Ctrl+C
    ser.close()
    csv_file.close()