import socket

bufferSize = 1024
timeout = 2 # em segundos

#baseado em RDTComm, modificada para o uso na entrega3
#ao invés de utilizar arquivos, apenas obtem variaveis

class Server:
    def __init__(self, portr = 8080, ports = 8081):
        #Inicialização do servidor
        self.host = '127.0.0.1'  # Endereço IP do servidor
        self.portr = portr       # Porta de recebimento do servidor
        self.ports = ports       # Porta de recepção do servidor

        self.UDPSocketR = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.UDPSocketR.settimeout(timeout)

        self.UDPSocketS = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.UDPSocketS.settimeout(timeout)

        self.UDPSocketR.bind((self.host, self.portr))
        self.UDPSocketS.bind((self.host, self.ports))
        #print(f"Servidor inicializado nas portas {portr} (R) e {ports} (S).")


    def send(self, payload: str, addr):
        # envia os dados em pacotes para addr, payload tratada como string

        seqnum = 1
        pld = payload.encode()
        while True:
            data = pld[:bufferSize-1] # pega bufferSize-1 bytes do payload
            pld = pld[bufferSize-1:] # remove os bufferSize-1 primeiros bytes de payload
            seqnum = (seqnum + 1) % 2
            if not data:
                break

            # molda o pacote no formato (numero de sequência, payload)
            datapacket = seqnum.to_bytes(1,'big') + data

            while True:

                self.UDPSocketS.sendto(datapacket, addr)
                #print(f"Pacote de dados com num. de seq. {seqnum} enviado pelo servidor")

                try:
                    ack, server = self.UDPSocketS.recvfrom(4)
                    if ack == b'ACK'+seqnum.to_bytes(1,'big'):
                        #print(f"ACK{seqnum} recebido corretamente pelo servidor.")
                        break
                    else:
                        #print(f"ACK{seqnum} duplicado recebido pelo servidor, reenviando pacote...")
                        continue
                except socket.timeout:
                    #print("Timeout, reenviando pacote...")
                    continue

    def receive(self): 
        #recebe os dados de qualquer emissor e retorna a dupla (dados, end. do emissor)

        receiver = b''
        seqnum = 0
        while True:
            while True:
                try:
                    datapacket, addr = self.UDPSocketR.recvfrom(bufferSize)
                    #print("Pacote recebido do cliente")
                    break
                except socket.timeout: # receptor rdt nao tem timeout
                    continue

            packetseqnum, data = datapacket[0], datapacket[1:] # divide o pacote (seq,payload) em seus dois componentes

            if(packetseqnum == seqnum):
                self.UDPSocketR.sendto(b'ACK'+seqnum.to_bytes(1,'big'), addr)
                #print(f"ACK{seqnum} enviado pelo servidor")
                seqnum = (seqnum + 1) % 2
            else: 
                self.UDPSocketR.sendto(b'ACK'+((seqnum+1)%2).to_bytes(1,'big'), addr)
                #print(f"ACK{(seqnum+1)%2} enviado pelo servidor")
                continue

            if not data:
                break
            receiver = receiver + data
            if len(data) < bufferSize-1:
                break
        return (receiver.decode(), addr)

    def close(self):
        # Fecha o socket do servidor
        self.UDPSocketS.close()
        self.UDPSocketR.close()

class Client:
    def __init__(self):
        self.host = '127.0.0.1'  # Endereço IP do servidor
        self.port = 8080      # Porta do servidor

        self.UDPSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.UDPSocket.settimeout(timeout)

        #print(f"Cliente inicializado")

    def send(self, payload: str):
        # envia os dados em pacotes para o servidor, payload tratada como string

        seqnum = 1
        pld = payload.encode()

        while True:
            data = pld[:bufferSize-1] # pega bufferSize-1 bytes do payload
            pld = pld[bufferSize-1:] # remove os bufferSize-1 primeiros bytes de payload
            seqnum = (seqnum + 1) % 2

            if not data:
                break

            # molda o pacote no formato (numero de sequência, payload)
            datapacket = seqnum.to_bytes(1,'big') + data

            while True:

                self.UDPSocket.sendto(datapacket, (self.host, self.port))
                #print(f"Pacote de dados com num. de seq. {seqnum} enviado pelo cliente")

                try:
                    ack, server = self.UDPSocket.recvfrom(4)
                    if ack == b'ACK'+seqnum.to_bytes(1,'big'):
                        #print(f"ACK{seqnum} recebido corretamente pelo cliente.")
                        break
                    else:
                        #print(f"ACK{seqnum} duplicado recebido pelo cliente, reenviando pacote...")
                        continue
                except socket.timeout:
                    #print("Timeout, reenviando pacote...")
                    continue

    def receive(self): 
        #recebe os dados do servidor e os retorna

        receiver = b''
        seqnum = 0
        while True:
            while True:
                try:
                    datapacket, addr = self.UDPSocket.recvfrom(bufferSize)
                    print("Pacote recebido do servidor")
                    break
                except socket.timeout: # receptor rdt nao tem timeout
                    continue

            packetseqnum, data = datapacket[0], datapacket[1:] # divide o pacote (seq,payload) em seus dois componentes

            if(packetseqnum == seqnum):
                self.UDPSocket.sendto(b'ACK'+seqnum.to_bytes(1,'big'), addr)
                print(f"ACK{seqnum} enviado pelo cliente")
                seqnum = (seqnum + 1) % 2
            else: 
                self.UDPSocket.sendto(b'ACK'+((seqnum+1)%2).to_bytes(1,'big'), addr)
                print(f"ACK{(seqnum+1)%2} enviado pelo cliente")
                continue

            if not data:
                break
            receiver = receiver + data
            if len(data) < bufferSize-1:
                break
        return receiver.decode()

    def close(self):
        # Fecha o socket do cliente
        self.UDPSocket.close()