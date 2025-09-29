import paho.mqtt.client as mqtt
from flask import Flask, jsonify, render_template
import threading
import json
import sqlite3
from datetime import datetime

# Importa nossas funções de "Machine Learning"
from ml_models import identificar_tipo_moto, reconhecer_placa

# --- Configurações ---
MQTT_BROKER = "broker.mqtt-dashboard.com"
MQTT_PORT = 1883
MQTT_TOPIC = "mottu/patio/+/status"
DATABASE_FILE = "patio.db"  # Nome do arquivo do nosso banco de dados


# --- Banco de Dados ---
def init_db():
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    # Cria a tabela se ela não existir
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vagas (
            id_vaga TEXT PRIMARY KEY,
            status TEXT NOT NULL,
            moto_id TEXT,
            tipo_moto_ml TEXT,
            placa_ml TEXT,
            ultimo_update TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


# --- Cliente MQTT ---
def on_message(client, userdata, message):
    try:
        topic_parts = message.topic.split('/')
        vaga_id = topic_parts[2]

        # Agora, esperamos um JSON como payload
        payload_json = json.loads(message.payload.decode("utf-8"))
        status = payload_json.get("status_ocupacao")
        moto_id = payload_json.get("moto_id")

        print(f"--- MENSAGEM MQTT RECEBIDA --- Vaga: {vaga_id}")

        tipo_moto = None
        placa = None

        if status == "ocupada":
            print(f"  Vaga OCUPADA pela moto IoT ID: {moto_id}.")
            tipo_moto = identificar_tipo_moto(moto_id)
            placa = reconhecer_placa("path/to/image.jpg")
            print(f"  [ML] Tipo de Moto Identificado: {tipo_moto}")
            print(f"  [ML] Placa Reconhecida: {placa}")
        else:
            print(f"  Vaga LIVRE.")

        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute('''
            REPLACE INTO vagas (id_vaga, status, moto_id, tipo_moto_ml, placa_ml, ultimo_update)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (vaga_id, status, moto_id, tipo_moto, placa, timestamp))

        conn.commit()
        conn.close()
        print(f"  Dados da vaga {vaga_id} salvos no banco de dados.")
        print("--------------------------------\n")

    except Exception as e:
        print(f"Erro ao processar mensagem: {e}")


mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqtt_client.on_message = on_message
mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
thread = threading.Thread(target=mqtt_client.loop_forever)
thread.start()

# --- Servidor Flask ---
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


# Esta é a sua API, que o dashboard usa para pegar os dados
@app.route('/status_patio')
def get_status_patio():
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM vagas")
    vagas = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify(vagas)


# --- Execução ---
if __name__ == '__main__':
    init_db()
    mqtt_client.subscribe(MQTT_TOPIC)
    print("Backend iniciado. Ouvindo MQTT e pronto para receber conexões na API.")
    app.run(host='0.0.0.0', port=5000, debug=False)