
import socket
import time
import random

# Configurações do cliente
server_address = ('localhost', 10000)
buffer_size = 1024
timeout = 1  # 1 segundo

# Criando o socket UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(timeout)

def simulate_packet_loss():
    return random.choice([True, False])

def rdt_send(data):
    while True:
        if simulate_packet_loss():
            print("Pacote perdido (simulado).")
            continue
        
        print(f"Enviando: {data}")
        sent = sock.sendto(data, server_address)
        
        try:
            ack, server = sock.recvfrom(buffer_size)
            print(f"Recebido: {ack}")
            if ack == b'ACK':
                print("ACK recebido, transmissão concluída.")
                break
        except socket.timeout:
            print("Timeout, reenviando pacote...")

data = b'Hello, World!'
rdt_send(data)