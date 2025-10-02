# MONITORAMENTO DE PÁTIO DE MOTOS COM IOT E IA - SPRINT 3 MOTTU

### INTEGRANTES
● Alexsandro Macedo: RM557068 ● Guilherme Felipe da Silva Souza: RM558282 ● Leonardo Faria Salazar: RM557484


Este projeto é uma solução completa para o monitoramento em tempo real de um pátio de motocicletas, 
utilizando tecnologias de Internet das Coisas (IoT) para a detecção de ocupação e Inteligencia
Artificial (IA) para identificação de placas e modelos de motos.

## DESCRIÇÃO
O sistema simula um ambiente de pátio onde vagas de estacionamento são equipadas com sensores IoT.
Quando uma moto ocupa uma vaga, o sistema é notificado em tempo real. Em seguida, modelos de Machine
Learning são acionados para reconhecer a placa e classificar o tipo da motocicleta. Todas essas
informações são armazenadas em um banco de dados e exibidas em um dashboard web dinâmico.

## FUNCIONALIDADES
- **DETECÇÃO DE OCUPAÇÃO VIA IoT:** Um dispositivo simulado (ESP32) com sensore ultrassônico detecta
  a presença de veículos nas vagas.

- **COMUNICAÇÃO EM TEMPO REAL:** O status de cada vaga é enviado em tempo real para um broker MQTT,
  garantindo a comunicação instantânea.

- **RECONHECIMENTO DE PLACA:** Um modelo de Visão Computacional, utiliza `easyocr` e `OpenCV`,
  extrai e corrige os caracteres da placa da moto.

- **IDENTIFICAÇÃO DE MODELO:** Um modelo de Deep Learning treinado com `TensorFlow` e `EficientNet`
  classifica as motos em diferentes tipos (ex: Mottu-E, Mottu-Pop, Mottu-Sport).

- **DASHBOARD INTERATIVO:** Uma interace web desenvolvida com Flask e JQuery exibe o status de
  cada vaga do pátio, atualizando-se automaticamente a cada 3 segundos.

- **PERSISTÊNCIA DE DADOS:** Todas as informações das vagas, incluindo status, ID da moto, placa
  e modelo identificados, são armazenadas em um banco de dados SQLite.

## ARQUITETURA E COMPONENTES
### HARDWARE (Simulação no Wokwi)
O circuito IoT foi simulado na plataforma Wokwi e é composto pelos seguintes componentes:

- **MICROCONTROLADOR (ESP32):** O cérebro da operação, reponsavel por ler os sensores, processar
  os dados e comunicar-se via WI-FI.

- **SENSORES ULTRASSÔNICO:** Utilizando para medir a distância e detectar se a vaga está "livre"
  ou "ocupada" com base em um limiar pré-definido.

- **POTENCIÔMETRO DESLIZANTE:** Simula a identificação de diferentes motos. O valor lido do
  potenciômetro pe mapeado para um dos três tipos de moto (MOTTU-E, MOTTU-POP, MOTTU-SPORT).

- **BUZZER:** Fornece feedback sonoro, sendo ativado quando uma mensagem é recebida no tópico de
  comando MQTT, funcionando como um sistema de alerta.

### SOFTWARE E COMUNICAÇÃO
1. **DISPOSITIVO IOT:** O sensor ultrassônico no ESP32 mede a distância. se for menor que `DISTANCIA_MAX_OCUPACAO`, a vaga é considerada "ocupada".
2. **BROKER MQTT:** O ESP32 publica uma mensagem JSON a cada 5 segundos no tópico `mottu/patio/{id_vaga}/status` com o status da vaga e o ID da moto.
3. **BACKEND FLASK(`main.py`):**
   - Um cliente MQTT se inscreve no tópico para receber as atualizações.
   - Ao receber uma mensagem de "ocupada", as funções de ML (`ml_models.py`) são chamadas para analisar a imagem da moto (simulada no código).
   - Os dados (status, placas, tipo) são salvos no banco de dados `patio.db`.
4. **FRONTEND:** 
   - A página web faz uma requisição a vada 3 segundos para a rota `/status_patio` da API Flask.
   - Os dados recebidos (em formato JSON) são usados para renderizar dinamicamente o status de cada vaga, alterando cor e informações exibidas.

## TECNOLOGIAS UTILIZADAS
- **BACKEND:** Python, Flask
- **MACHINE LEARNING:** TensorFlow, Keras, `easyocr`, `OpenCV`
- **IoT (Simulação):** Wokwi (Simulador de ESP32), C++ (Arduino)
- **COMUNICAÇÃO:** MQTT (Paho MQTT Client, PubSubClient)
- **Banco de Dados:** SQLite
- **FRONTEND:** HTML, CSS, JavaScript
- **AMBIENTE DE DESENVOLVIMENTO:** Google Colab, jupyter Notebook

## COMO EXECUTAR O PROJETO
### Pré-requisitos
- Python 3.8+
- Wokwi para simulação do IoT (ou um ESP32 físico)
- Um broker MQTT público (ex: `broker.mqtt-dashboard.com`) ou local.

### 1. Simulador IoT
1. Abra o arquivo `Simulador_IOT/src/sketch.ino` no Wokwi ou na IDE do Arduino.
2. Compile e execute a simulação. O dispositivo começará a enviar dados para o broker MQTT.

### 2.Backend
1. Navegue até a pasta `backend_ML_IOT_PYTHON`.
2. Crie e ative um ambiente virtual:
  ```
  python -m venv venv
  source venv/bin/activate  # No Windows: venv\Scripts\activate
  ```
3. Instale as dependências:
  ```
  pip install flask paho-mqtt easyocr opencv-python tensorflow
  ```
4. Inicialize o banco de dados (será criado o arquivo `patio.db`):
  ```
  python main.py
  ```
5. Inicie o servidor Flask:
  ```
  python main.py
  ```
6. Acesse `http://127.0.0.1:5000` em seu navegador para ver o dashboard.

## ESTRUTURA DO PROJETO
```
backend_challenge2025/
├── Simulador_IOT/
│   ├── src/sketch.ino          # Código do dispositivo IoT simulado
│   └── diagram.json            # Definição do circuito no Wokwi
├── backend_ML_IOT_PYTHON/
│   ├── main.py                 # Aplicação principal Flask e cliente MQTT
│   ├── ml_models.py            # Funções de simulação dos modelos de ML
│   ├── patio.db                # Banco de dados SQLite
│   └── templates/
│       └── index.html          # Dashboard web
├── Leitura_Placas.ipynb        # Notebook para desenvolvimento do OCR de placas
└── modelo_da_entrega2_Challenge2025.ipynb # Notebook do modelo de classificação de motos
```
## IMAGENS

### DISPOSITIVO IoT funcionando
<div align="center">
  <img src="/imagens/Captura de tela 2025-10-01 210249.png" alt="DISPOSITIVO IoT"/>
</div>

### Atualização em tempo real
### Vaga ocupada
<div align="center">
  <img src="/imagens/Captura de tela 2025-10-01 210331.png" alt="Vaga ocupada"/>
</div>

### Vaga livre
<div align="center">
  <img src="/imagens/Captura de tela 2025-10-01 210346.png" alt="Vaga livre"/>
</div>
