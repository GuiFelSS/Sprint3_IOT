import random

# Simula o modelo que já criamos para identificar o tipo da moto
def identificar_tipo_moto(caminho_imagem):
    tipos = ["Mottu-E", "Mottu-Pop", "Mottu-Sport"]
    # Por enquanto, retorna um tipo aleatório para simulação
    return random.choice(tipos)

# Simula o modelo de reconhecimento de placa que criamos
def reconhecer_placa(caminho_imagem):
    # Retorna uma placa de exemplo
    return "RFA4I58"