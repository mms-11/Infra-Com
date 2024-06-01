import socket

class udpServidor():
    def __init__(self,sktFam,sktType,sktBinding, maxBuff):
        self.socket = socket.socket(sktFam,sktType)
        self.socket.bind(sktBinding)
        self.socket.settimeout(0.1)

        if self.socket is None:
            raise "SOCKET NÃO DISPONÍVEL"
        self.maxBuff = maxBuff
        self.init_trans = 0
        self.stop = 0

        def listen(self):
            while True:
                try:
                    data, fonte = self.socket.recvfrom(self, maxBuff)
                    if data:
                     filename = data.decode()
                     self.receive_file(filename, fonte)
                     modified_filename = 'modified_' + filename
                     self.send_file(modified_filename, fonte)
                except socket.timeout:
                 continue
        def receive_file(nome,fonte):
            with open('received_' + filename, 'wb') as f:
             while True:
                try:
                    data, _ = self.socket.recvfrom(self.maxBuff)
                    if data == b'EOF':
                        break
                    f.write(data)
                except socket.timeout:
                    continue
                 
        def send(self, end_servidor: (str,str), msg: str):
                self.socket.sendto(msg,end_servidor,porta_servidor)
                time.sleep(0.001)