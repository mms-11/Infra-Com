import socket
import random

# Configurações do servidor
server_address = ('localhost', 10000)
buffer_size = 1024

# Criando o socket UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(server_address)

print("Servidor aguardando conexão...")

def simulate_packet_loss():
    return random.choice([True, False])

while True:
    data, address = sock.recvfrom(buffer_size)
    print(f"Recebido: {data} de {address}")
    
    if simulate_packet_loss():
        print("ACK perdido (simulado).")
        continue
    
    ack = b'ACK'
    sent = sock.sendto(ack, address)
    print(f"Enviado: {ack} para {address}")
