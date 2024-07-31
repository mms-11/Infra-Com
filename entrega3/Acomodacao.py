import datetime

class Acomodacao:
    #pela documentacao, admitimos que toda acomodacao tem dos dias 17 a 22 livres inicialmente
    def __init__(self, nome, lugar, id, dono):
        self.agenda = [False, False, False, False, False, False] #seg,ter,....sex,sab, 17/07~22/07
        #cliente dono da reserva alinhado ao dia de agenda
        self.clientes = [('',('',0)),('',('',0)),('',('',0)),('',('',0)),('',('',0)),('',('',0))] 
        self.dono = dono #dono da acomodacao
        self.nome = nome #nome do dono
        self.lugar = lugar
        self.id = id

    def agenda_status(self, data): #converte o dia no formato DIA/MES/ANO no indice de agenda/clientes
        d0 = datetime.date(2024, 7, 17)
        d = datetime.datetime.strptime(data, '%d/%m/%Y').date()
        diff = (d - d0).days
        return (diff, self.agenda[diff])
    
        