import socket
import os

def main():
    # Configuração do servidor
    host = '127.0.0.1'  # Endereço IP do servidor
    port = 12345        # Porta do servidor
    buffer_size = 1024

    # Criação do socket UDP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((host, port))

    print(f"Servidor UDP iniciado em {host}:{port}")

    # Recebe o nome do arquivo
    data, client_address = server_socket.recvfrom(buffer_size)
    file_name = data.decode()
    print(f"Recebendo arquivo {file_name} de {client_address}")

    # Recebe o arquivo em pacotes e grava localmente
    with open(file_name, 'wb') as f:
        while True:
            data, addr = server_socket.recvfrom(buffer_size)
            if not data:
                break
            f.write(data)
            if len(data) < buffer_size:
                break

    print(f"Arquivo {file_name} recebido e salvo com sucesso.")

    # Altera o nome do arquivo para enviar de volta
    new_file_name = "new_" + file_name
    os.rename(file_name, new_file_name)

    # Envia o arquivo de volta ao cliente
    with open(new_file_name, 'rb') as f:
        while True:
            data = f.read(buffer_size)
            if not data:
                break
            server_socket.sendto(data, client_address)
    
    print(f"Arquivo {new_file_name} enviado de volta ao cliente.")

    # Fecha o socket do servidor
    server_socket.close()

if __name__ == "__main__":
    main()
