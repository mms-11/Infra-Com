import socket
import time

class udpCliente():
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
                except: 
                    continue
            def send(self, end_servidor: tuple[str ,str ], msg: str):
                self.socket.sendto(msg,end_servidor,porta_servidor)
                time.sleep(0.001)