import socket

bufferSize = 1024
timeout = 0.1 # em segundos

#baseado em RDTComm, modificada para o uso na entrega3
#ao invés de utilizar arquivos, apenas obtem variaveis

class Server:
    def __init__(self, port = 8080):
        #Inicialização do servidor
        self.host = '127.0.0.1'  # Endereço IP do servidor
        self.port = port       # Porta do servidor

        self.UDPSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.UDPSocket.settimeout(timeout)

        self.UDPSocket.bind((self.host, self.port))
        print(f"Servidor inicializado na porta {port}.")
        
        #Variáveis lógicas

        clientList = [] # triplas (nome do cliente, ip, porta)


    def send(self, payload, addr):
        # envia os dados em pacotes, payload tratada como string

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

                self.UDPSocket.sendto(datapacket, addr)
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

    def receive(self): 
        #recebe os dados de qualquer emissor e retorna a dupla (dados, end. do emissor)

        receiver = b''
        seqnum = 0
        while True:
            while True:
                try:
                    datapacket, addr = self.UDPSocket.recvfrom(bufferSize)
                    break
                except socket.timeout: # receptor rdt nao tem timeout
                    continue

            packetseqnum, data = datapacket[0], datapacket[1:] # divide o pacote (seq,payload) em seus dois componentes

            if(packetseqnum == seqnum):
                self.UDPSocket.sendto(b'ACK'+seqnum.to_bytes(1,'big'), addr)
                print(f"ACK{seqnum} enviado pelo servidor")
                seqnum = (seqnum + 1) % 2
            else: 
                self.UDPSocket.sendto(b'ACK'+((seqnum+1)%2).to_bytes(1,'big'), addr)
                print(f"ACK{(seqnum+1)%2} enviado pelo servidor")
                continue

            if not data:
                break
            receiver = receiver + data
            if len(data) < bufferSize-1:
                break
        return (receiver.decode(), addr)

    def close(self):
        # Fecha o socket do servidor
        self.UDPSocket.close()