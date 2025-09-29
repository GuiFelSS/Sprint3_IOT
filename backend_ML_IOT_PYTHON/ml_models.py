import random

# Simula o modelo que já criamos para identificar o tipo da moto
def identificar_tipo_moto(moto_id_iot):
    """
    Simula o modelo de ML mapeando o ID do IoT para o tipo da moto.
    Garante consistência entre o sensor IoT e a "visão computacional".
    """
    if moto_id_iot == "MOTTU-E":
        return "Mottu-E"
    elif moto_id_iot == "MOTTU-POP":
        return "Mottu-Pop"
    elif moto_id_iot == "MOTTU-SPORT":
        return "Mottu-Sport"
    else:
        # Retorna um valor padrão caso o ID não seja reconhecido
        return "Tipo Desconhecido"

# Simula o modelo de reconhecimento de placa que criamos
def reconhecer_placa(caminho_imagem):
    # Retorna uma placa de exemplo
    return "RFA4I58"