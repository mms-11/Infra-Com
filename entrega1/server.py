from UDPComm import *

def main():
    UDPClient = UDPComm('server')

    file = UDPClient.receiveFileName()

    UDPClient.receiveFile(file)
    
    UDPClient.sendFileName(file)
    UDPClient.sendFile(file)

    UDPClient.close()

if __name__ == "__main__":
    main()



