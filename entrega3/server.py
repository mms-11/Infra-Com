from RDTUtils import *

def main():
    server = Server()
    valor, end = server.receive()
    print(f"Recebido {valor} de {end}")

if __name__ == "__main__":
    main()