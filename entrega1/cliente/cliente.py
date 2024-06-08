import socket

def main():
    # Configuração do cliente
    host = '127.0.0.1'  # Endereço IP do servidor
    port = 12345        # Porta do servidor
    buffer_size = 1024

    # Criação do socket UDP
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Nome do arquivo a ser enviado
    file_name = 'test.txt'  # Altere para o nome do arquivo desejado

    # Envia o nome do arquivo para o servidor
    client_socket.sendto(file_name.encode(), (host, port))

    # Envia o arquivo em pacotes
    with open(file_name, 'rb') as f:
        while True:
            data = f.read(buffer_size)
            if not data:
                break
            client_socket.sendto(data, (host, port))
    
    print(f"Arquivo {file_name} enviado ao servidor.")

    # Recebe o arquivo modificado de volta
    new_file_name = "new_" + file_name
    with open(new_file_name, 'wb') as f:
        while True:
            data, addr = client_socket.recvfrom(buffer_size)
            if not data:
                break
            f.write(data)
            if len(data) < buffer_size:
                break
    
    print(f"Arquivo modificado {new_file_name} recebido do servidor.")

    # Fecha o socket do cliente
    client_socket.close()

if __name__ == "__main__":
    main()
