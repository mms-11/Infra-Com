from RDTUtils import *
import threading
import queue

#queue é thread-safe por default
#estamos usando 2 portas diferentes para o servidor, logo não é necessário mutex

server = Server()
user_queue = queue.Queue(maxsize=100)
running = True

def listening():
    while True:
        
        input, addr = server.receive()

        print(input)
        user_queue.put((input, addr))

def main():
    
    listening_thread = threading.Thread(target=listening, daemon=True)
    listening_thread.start()

    clientes = [] # cliente é registrado no formato(input, (ip, porta))
    acomodacoes = [] # acomodação é registrada no formato (nome, lugar, (reserva))

    while running:
        

        command, addr = user_queue.get()

        command.split()

        if command[0] == "login":
            #login
            #usuário é command[1]
            pass

        elif command[0] == "logout":
            pass

        elif command[0] == "create":
            pass

        elif command[0] == "book":
            pass

        elif command[0] == "cancel":
            pass

        elif command[0] == "list:myacmd":
            pass
        
        elif command[0] == "list:acmd":
            pass

        elif command[0] == "list:myrsv":
            pass
        else:
            server.send("INVALID COMMAND", addr)

        user_queue.task_done()

    listening_thread.join()
    server.close()

if __name__ == "__main__":
    main()