from RDTUtils import *
import threading
import queue
import datetime
import Acomodacao

#queue é thread-safe por default
#estamos usando 2 portas diferentes para o servidor, logo não é necessário mutex

#thread auxiliar recebe comandos dos clientes
#enquanto a main é responsavel pela lógica

server = Server()
user_queue = queue.Queue(maxsize=100)
running = True

def listening():
    while True:
        input, addr = server.receive()
        user_queue.put((input, addr))

def main():
    
    listening_thread = threading.Thread(target=listening, daemon=True)
    listening_thread.start()

    clientes = [] # cliente é registrado no formato (nome,(ip, porta))
    acomodacoes = [] # acomodação é registrada no formato (nome, lugar, disponibiliade)

    while running:
        
        nome = ""
        not_logged = True

        command, addr = user_queue.get()

        for client in clientes:
            if addr == client[1]:
                nome = client[0]
                not_logged = False
                break

        command = command.split()

        if(not_logged and (command[0] != "login")):
            server.send("NOT LOGGED", addr)
            continue

        if command[0] == "login":
            if(len(command) < 2):
                server.send("Argumentos insuficientes", addr)
                continue
            username = command[1]
            port = addr[1]
            flag_username = any(t[0] == username for t in clientes)
            flag_port = any(t[1][1] == port for t in clientes)

            if flag_username or flag_port:
                server.send("Nao foi possivel realizar o login", addr)

            else:
                tupla = (username, addr)
                clientes.append(tupla)
                server.send("Você está online!", addr) 

        elif command[0] == "logout":
            tupla = (nome, addr)
            clientes.remove(tupla)
            server.send("Desconectado", addr) 

        elif command[0] == "create":
            if(len(command) < 4):
                server.send("Argumentos insuficientes", addr)
                continue

            nomeacom = command[1]
            lugaracom = command[2]
            idacom = command[3]

            for acom in acomodacoes:
                if(acom.id == idacom):
                    server.send("Já existe acomodação com mesmo ID", addr)
                    continue
                if((acom.nome == nomeacom) and (acom.lugar == lugaracom)):
                    server.send("Já existe acomodação com mesmo nome e localização", addr)
                    continue

            acomodacoes.append(Acomodacao.Acomodacao(nomeacom, lugaracom, idacom, (nome, addr)))
            server.send(f"Acomodacao {nomeacom} criada em {lugaracom}", addr)

        elif command[0] == "book":
            if(len(command) < 4):
                server.send("Argumentos insuficientes", addr)
                continue
            nomeOfertante = command[1]
            id_acomodacao = command[2]
            data = command[3]

            d0 = datetime.date(2024, 7, 17)
            d = datetime.datetime.strptime(data, '%d/%m/%Y').date()
            diff = (d - d0).days

            for cliente in clientes:
                if cliente[0] == nomeOfertante:  # achado o cliente
                    # agendar na acomodação certa
                    for acom in acomodacoes:
                        if id_acomodacao == acom.id:
                            actual = (nome, addr)
                            if(acom.dono == actual):
                                server.send("Essa acomodação é sua", addr)
                                continue
                            diff, reserved = acom.agenda_status(data)
                            if reserved == False:
                                acom.agenda[diff] = True
                                acom.clientes[diff] = actual
                                server.send(f"[{actual[0]}/{actual[1][0]}:{actual[1][1]}] Reserva realizada na acomodação de local {acom.lugar}, ID {acom.id} e ofertante {acom.dono[0]} no dia {17+diff}/07/2024", addr)
                            else:
                                server.send("Data já reservada nessa acomodação", addr)
                            break

        elif command[0] == "cancel":
            if(len(command) < 4):
                server.send("Argumentos insuficientes", addr)
                continue

            actual = (nome, addr)

            nomeOfertante = command[1]
            id_acomodacao = command[2]
            data = command[3]

            d0 = datetime.date(2024, 7, 17)
            d = datetime.datetime.strptime(data, '%d/%m/%Y').date()
            diff = (d - d0).days

            cliente_encontrado = False

            for cliente in clientes:
                if cliente[0] == nomeOfertante:  # achado o cliente
                    # agendar na acomodação certa
                    for acom in acomodacoes:
                        if id_acomodacao == acom.id:
                            diff, reserved = acom.agenda_status(data)
                            if(actual != acom.clientes[diff]):
                                server.send("Você não é o dono da reserva")
                            if reserved == True:
                                acom.agenda[diff] = False
                                acom.clientes[diff] = ("",("",0))
                                server.send(f"[{actual[0]}/{actual[1][0]}:{actual[1][1]}] Reserva cancelada na acomodação de local {acom.lugar}, ID {acom.id} e ofertante {acom.dono[0]} no dia {17+diff}/07/2024", addr)
                            else:
                                server.send("Acomodação não está reservada", addr)

        elif command[0] == "list:myacmd": # lista todas as acomodações que pertecem ao usuario
            actual = (nome, addr)
            string = ""
            if len(acomodacoes) == 0: string = "Não existem acomodações"
            else:
                for acom in acomodacoes: # para cada acom, verifica se a acomodacao esta disponivel no dia 17+cont
                    if(acom.dono == actual):
                        cont = 0
                        disponibility = []
                        not_disponibility = []
                        disponibility_str = ""
                        not_disponibility_str = ""
                        while cont < 6:
                            reserved = acom.agenda[cont]
                            if reserved == False: #significa que está disponivel
                                disponibility.append(f"{17+cont}/07/2024")
                            else:
                                not_disponibility.append(f"{17+cont}/07/2024 (ocupada por {acom.clientes[cont]})")
                            cont = cont + 1
                        for i in range(len(disponibility)):
                            disponibility_str += disponibility[i]
                            if i < len(disponibility)-1: disponibility_str += ", "
                        for i in range(len(not_disponibility)):
                            not_disponibility_str += not_disponibility[i]
                            if i < len(not_disponibility)-1: not_disponibility_str += ", "

                        string += f"A sua acomodação {acom.nome} de ID {acom.id}, localização {acom.lugar} está:\n" 
                        if disponibility_str != "": 
                            string += f"Disponível nos dias: " + disponibility_str + '\n'
                        if not_disponibility_str != "":
                            string += f"Indisponível nos dias: " + not_disponibility_str + '\n'
            if string == "":
                server.send("Você não tem acomodações em seu nome", addr)
            server.send(string, addr)
        
        elif command[0] == "list:acmd": # lista todas as acomodações com disponibilidade
            string = ""
            if len(acomodacoes) == 0: string = "Não existem acomodações"
            else:
                for acom in acomodacoes: # para cada acom, verifica se a acomodacao esta disponivel no dia 17+cont
                    cont = 0
                    disponibility = ""
                    while cont < 6:
                        reserved = acom.agenda[cont]
                        if reserved == False: #significa que está disponivel
                            disponibility = disponibility + f"{17+cont}/07/2024"
                            if cont != 5: disponibility += ", " #adiciona virgula exceto antes da primeira data
                        cont = cont + 1
                    if disponibility != "": #se esta completamente indisponivel, nao printa
                        string += f"A acomodação {acom.nome} de ID {acom.id}, localização {acom.lugar} e ofertante {acom.dono[0]} está disponível no dias:\n" + disponibility + '\n'
                    else: string = "Não há acomodações disponíveis"
            server.send(string, addr)

        elif command[0] == "list:myrsv": #lista todas as suas reservas
            actual = (nome, addr)
            message = ""
            for acom in acomodacoes:
                cont = 0
                while cont < 6:
                    if actual == acom.clientes[cont]:
                        message += f"[{acom.dono[0]}/{acom.dono[1][0]}:{acom.dono[1][1]}]  Reserva no nome de {actual[0]} na localização {acom.lugar} no dia {cont + 17}/07/2024" + '\n'
                    cont = cont + 1
            if message == "":
                server.send("Você não tem acomodações reservadas", addr)
                continue
            server.send(message, addr)

        else:
            server.send("INVALID COMMAND", addr)

        user_queue.task_done()

    listening_thread.join()
    server.close()

if __name__ == "__main__":
    main()