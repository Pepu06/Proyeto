import requests
import pyautogui
import time
import webbrowser


url = "http://192.168.199.1:8080"  # Reemplaza con la dirección IP y el puerto del ESP8266

while True:
    response = requests.get(url)
    if response.status_code == 200:
        data = response.text.strip().split(',')
        aceleracion_x = data[0]
        aceleracion_y = data[1]

        print(aceleracion_x, aceleracion_y)
        # webbrowser.open('https://www.youtube.com')
        #print(data)
    else:
        print("Error al obtener datos. Código de estado:", response.status_code)
# except requests.exceptions.RequestException as e:
#     print("Error de conexión:", e)