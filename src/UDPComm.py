import socket

bufferSize = 1024

dirPrefixSend = "files/send/"
dirPrefixReceive = "files/received/"

class UDPComm:
    def __init__(self, function='client'):
        self.host = '127.0.0.1'  # Endereço IP do servidor
        self.port = 12345        # Porta do servidor
        self.function = function

        # Criação do socket UDP
        self.UDPSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        if function == 'server':
            self.UDPSocket.bind((self.host, self.port))
            print("Servidor UDP iniciado.")

    def sendFile(self, fileName):
        # Envia o arquivo em pacotes
        if self.function == 'server':
            fileName = dirPrefixReceive + "server/new_" + fileName
        else:
            fileName = dirPrefixSend + fileName

        with open(fileName, 'rb') as f:
            while True:
                data = f.read(bufferSize)
                if not data:
                    break
                if self.function == 'server':
                    self.UDPSocket.sendto(data, self.addrRecv)
                else:
                    self.UDPSocket.sendto(data, (self.host, self.port))
        
        print(f"Arquivo {fileName} enviado.")

    def sendFileName(self, fileName):
        # Envia o nome do arquivo para o servidor
        if self.function == 'server':
            self.UDPSocket.sendto(fileName.encode(), self.addrRecv)
            print(f"Nome do arquivo {fileName} enviado.")
        else:
            self.UDPSocket.sendto(fileName.encode(), (self.host, self.port))
            print(f"Nome do arquivo {fileName} enviado.")

    def receiveFile(self, fileName):
        # Recebe o arquivo modificado de volta

        if self.function == 'server':
            new_file_name = dirPrefixReceive + "server/new_" + fileName
        else:
            new_file_name = dirPrefixReceive + "client/new_" + fileName
    
        with open(new_file_name, 'wb') as f:
            while True:
                data, addr = self.UDPSocket.recvfrom(bufferSize)
                if not data:
                    break
                f.write(data)
                if len(data) < bufferSize:
                    break
        
        print(f"Arquivo modificado {new_file_name} recebido do servidor.")

    def receiveFileName(self):
        # Recebe o nome do arquivo
        data, addr = self.UDPSocket.recvfrom(bufferSize)
        self.addrRecv = addr
        return data.decode()

    def close(self):
        # Fecha o socket do cliente
        self.UDPSocket.close()