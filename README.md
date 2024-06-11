# Infra-Com

Respositorio do projeto da cadeira de Infraestrutura de Comunicação

## Equipe

- Elisson Rodrigo da Silva Araújo (ersa)
- Manoel Lira de Carvalho (mlc6)
- Mariana Melo dos Santos (mms11)
- Victor Mendonça Aguiar (vma3)
- Vítor Manoel de Melo Silva (vmms)

# Instruções

### Rodar o servidor
1. Na pasta raiz do projeto execute: ```python3 src/server.py```
2. Após execução o servidor será encerrado, caso queira enviar outro arquivo execute o passo 1 novamente.

### Rodar o client:
1. Na pasta raiz do projeto execute: ```python3 src/client.py```
2. Digite o nome do arquivo que deseja enviar
    - Os arquivos disponiveis para o envio então na pasta ```file/send```
    - Disponiblizamos tres arquivos (test.png, test.txt e test.pdf)
3. Após execução o client será encerrado, caso queira enviar outro arquivo execute os passo 1 e 2 novamente.

### Verificar reenvio:
1. Os arquivos recebidos pelo server estarão na pasta ```file/received/server```
2. Os arquivos reenviados do server para o client estarão na pasta ```file/received/client```