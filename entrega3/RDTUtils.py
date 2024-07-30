import socket
import os
from pathlib import Path

directory = Path(os.path.dirname(__file__)).as_posix() + '/'

bufferSize = 1024
timeout = 0.1 # em segundos

#baseado em RDTComm, modificada para o uso na entrega3
#ao invés de utilizar arquivos, apenas obtem variaveis

class RDTServer:
    def __init__(self):
        self.host = '127.0.0.1'  # Endereço IP do servidor
        self.port = 8080       # Porta do servidor

        # Criação do socket UDP
        self.UDPSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.UDPSocket.settimeout(timeout)

        self.UDPSocket.bind((self.host, self.port))
        print("Servidor UDP com RDT3.0 iniciado.")

    def send(self, fileName):
        # Envia o arquivo em pacotes
        if self.function == 'server':
            fileName = dirPrefixReceive + "server/new_" + fileName
        else:
            fileName = dirPrefixSend + fileName

        seqnum = 1
        with open(fileName, 'rb') as f:
            while True:
                data = f.read(bufferSize-1)
                seqnum = (seqnum + 1) % 2
                if not data:
                    break

                # molda o pacote no formato (numero de sequência, payload)
                datapacket = seqnum.to_bytes(1,'big') + data

                if self.function == 'server':
                    while True:

                        self.UDPSocket.sendto(datapacket, self.addrRecv)
                        print(f"Pacote de dados com num. de seq. {seqnum} enviado pelo servidor")

                        try:
                            ack, server = self.UDPSocket.recvfrom(4)
                            if ack == b'ACK'+seqnum.to_bytes(1,'big'):
                                print(f"ACK{seqnum} recebido corretamente pelo servidor.")
                                break
                            else:
                                print(f"ACK{seqnum} duplicado recebido pelo servidor, reenviando pacote...")
                                continue
                        except socket.timeout:
                            print("Timeout, reenviando pacote...")
                            continue
                else:
                    while True:

                        self.UDPSocket.sendto(datapacket, (self.host, self.port))
                        print(f"Pacote de dados com num. de seq. {seqnum} enviado pelo cliente")

                        try:
                            ack, server = self.UDPSocket.recvfrom(4)
                            if ack == b'ACK'+seqnum.to_bytes(1,'big'):
                                print(f"ACK{seqnum} recebido corretamente pelo cliente.")
                                break
                            else:
                                print(f"ACK{seqnum} duplicado recebido pelo cliente, reenviando pacote...")
                                continue

                        except socket.timeout:
                            print("Timeout, reenviando pacote...")
                            continue
        
        print(f"Arquivo {fileName} enviado.")

    def receive(self, fileName):
        # recebe 

        if self.function == 'server':
            new_file_name = dirPrefixReceive + "server/new_" + fileName
        else:
            new_file_name = dirPrefixReceive + "client/new_" + fileName

        seqnum = 0
        with open(new_file_name, 'wb') as f:
            if self.function == 'server':
                while True:
                    while True:
                        try:
                            datapacket, addr = self.UDPSocket.recvfrom(bufferSize)
                            break
                        except socket.timeout: # receptor rdt nao tem timeout
                            continue

                    packetseqnum, data = datapacket[0], datapacket[1:] # divide o pacote (seq,payload) em seus dois componentes

                    if(packetseqnum == seqnum):
                        self.UDPSocket.sendto(b'ACK'+seqnum.to_bytes(1,'big'), self.addrRecv)
                        print(f"ACK{seqnum} enviado pelo servidor")
                        seqnum = (seqnum + 1) % 2
                    else: 
                        self.UDPSocket.sendto(b'ACK'+((seqnum+1)%2).to_bytes(1,'big'), self.addrRecv)
                        print(f"ACK{(seqnum+1)%2} enviado pelo servidor")
                        continue

                    if not data:
                        break
                    f.write(data)
                    if len(data) < bufferSize-1:
                        break
            else:
                while True:
                    while True:
                        try:
                            datapacket, addr = self.UDPSocket.recvfrom(bufferSize)
                            break
                        except socket.timeout:
                            continue

                    packetseqnum, data = datapacket[0], datapacket[1:] # divide o pacote (seq,payload) em seus dois componentes

                    if(packetseqnum == seqnum):
                        self.UDPSocket.sendto(b'ACK'+seqnum.to_bytes(1,'big'), (self.host, self.port))
                        print(f"ACK{seqnum} enviado pelo cliente")
                        seqnum = (seqnum + 1) % 2
                    else: 
                        print(f"Pacote de dados duplicado recebido, reenviando ACK{(seqnum+1)%2}...")
                        self.UDPSocket.sendto(b'ACK'+((seqnum+1)%2).to_bytes(1,'big'), (self.host, self.port))
                        print(f"ACK{(seqnum+1)%2} enviado pelo cliente")
                        continue

                    if not data:
                        break
                    f.write(data)
                    if len(data) < bufferSize-1:
                        break
        
        print(f"Arquivo modificado {new_file_name} recebido do servidor.")

    def close(self):
        # Fecha o socket do cliente
        self.UDPSocket.close()