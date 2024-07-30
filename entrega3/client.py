from RDTUtils import *

def main():
    running = True
    print("Inicializando cliente...")
    client = Client()
    while running:
        command = input()
        client.send(command)
        output = client.receive()
        if(output == "INVALID COMMAND"):
            print("Comando invalido!")
        elif(output != "COMMAND DONE"): # indicador de sucesso para comandos sem output
            print(output)
    client.close()

if __name__ == "__main__":
    main()