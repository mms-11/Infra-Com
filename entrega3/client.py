from RDTUtils import *

def main():
    server = Server(8081)
    server.send("ahr", ("127.0.0.1",8080))

if __name__ == "__main__":
    main()