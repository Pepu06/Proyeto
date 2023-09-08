from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['POST'])
def receive_data():
    try:
        data = request.json  # Obtener los datos JSON del cuerpo de la solicitud
        if data:
            # Aquí puedes procesar los datos como desees, como almacenarlos en una base de datos o imprimirlos en la consola
            print("Received data:", data)
            return "Data received successfully", 200
        else:
            return "Invalid JSON data", 400
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
