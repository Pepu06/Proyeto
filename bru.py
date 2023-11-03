from flask import Flask, request, jsonify
import pyautogui

app = Flask(__name__)
pyautogui.FAILSAFE = False

@app.route('/', methods=['POST'])
def receive_data():
    try:
        data = request.get_json(force=True)  # Indica que se espera un JSON
        print(data)
        
        vx = float(data[0]) * 3
        vy = float(data[1]) * 3

        # Mover el mouse suavizado
        pyautogui.move(vx, vy)
                
        return 'Data received successfully', 200
    except Exception as e:
        return f'Error: {str(e)}', 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)  # Ejecuta Flask en el puerto 8080
