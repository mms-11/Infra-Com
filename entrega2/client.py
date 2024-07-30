from RDTComm import *

def main():
    UDPClient = RDTComm()
    
    # Nome do arquivo a ser enviado
    fileName = input("Digite o nome do arquivo a ser enviado: [test.txt, test.png ou test.pdf]: ")

    UDPClient.sendFileName(fileName)
    UDPClient.sendFile(fileName)

    file = UDPClient.receiveFileName()
    UDPClient.receiveFile(file)

    UDPClient.close()

if __name__ == "__main__":
    main()
