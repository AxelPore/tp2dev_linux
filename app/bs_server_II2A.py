import socket
import sys
import argparse
import re
from psutil import net_if_addrs
import logging

logger = logging.getLogger("logs")
logger.setLevel(10)
fmt = "%(levelname)8s"
fmt2 = "%(asctime)s %(levelname)8s %(message)s"
class CustomFormatter(logging.Formatter):

    grey = '\x1b[38;21m'
    blue = '\x1b[38;5;39m'
    yellow = '\x1b[38;5;226m'
    red = '\x1b[38;5;196m'
    bold_red = '\x1b[31;1m'
    reset = '\x1b[0m'
    white = '\x1b[38;5;255m'


    def __init__(self, fmt):
        super().__init__()
        self.fmt = fmt
        self.FORMATS = {
            logging.DEBUG: "%(asctime)s" + self.grey + self.fmt + self.reset + " %(message)s",
            logging.INFO: "%(asctime)s" + self.white + self.fmt + self.reset + " %(message)s",
            logging.WARNING: "%(asctime)s" + self.yellow + self.fmt + self.reset + " %(message)s",
            logging.ERROR: "%(asctime)s" + self.red + self.fmt + self.reset + " %(message)s",
            logging.CRITICAL: "%(asctime)s" + self.bold_red + self.fmt + self.reset + " %(message)s",
            
        }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, datefmt="%Y-%m-%d %H:%M:%S")
        return formatter.format(record)
    
console_handler = logging.StreamHandler()
console_handler.setLevel(10)
console_handler.setFormatter(CustomFormatter(fmt))

file_handler = logging.FileHandler("/var/log/bs_server/bs_server.log", mode="a", encoding="utf-8")
file_handler.setLevel(10)
file_handler.setFormatter(logging.Formatter(fmt2))

logger.addHandler(console_handler)
logger.addHandler(file_handler)

parser = argparse.ArgumentParser()
parser = argparse.ArgumentParser(add_help=False)


parser.add_argument("-p", "--port", action="store")
parser.add_argument("-h", "--help", action="store_true")
parser.add_argument("-l", "--listen", action="store")
args = parser.parse_args()


def port_receive(port):
    
    
    if type(port) != int :
        print("Need a valid port")
    elif 0 > port or 65535 < port :
        print(f'ERROR -p argument invalide. Le port spécifié {port} est un port privilégié. Spécifiez un port au dessus de 1024.')
        sys.exit(1)
    elif 0 < port and 1024 > port :
        print(f'ERROR -p argument invalide. Le port spécifié {port} est un port privilégié. Spécifiez un port au dessus de 1024.')
        sys.exit(2)
    else :
        return port 

def host_recieve(host):

    
    if not re.search(r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$', host) :
        print(f"ERROR -l argument invalide. L'adresse {host} n'est pas une adresse IP valide.")
        sys.exit(3)
    else :
        dic = net_if_addrs()
        addr = None       
        for key, value in dic.items():
            
            for i in range(len(value)):
                if value[i].family == socket.AddressFamily.AF_INET:
                    addr = value[i].address                
                if addr == host :
                    return host            
        print(f"ERROR -l argument invalide. L'adresse {host} n'est pas l'une des adresses IP de cette machine.")
        sys.exit(4)     
                    
def Shelp(help):
    
    if help:
        print("Usage: python server.py [options]")
        print("Options:")
        print("-p, --port <port> : Port sur lequel écouter. Par défaut, 13337.")
        print("-l, --listen <adresse> : Adresse IP sur laquelle écouter. Par défaut, toutes les adresses IP disponibles.")
        print("-h, --help : Afficher cette aide.")
        sys.exit(0)
                     

def server(host, port):

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.bind((host, port))
    
    s.listen(1)
    logger.info(f"Le serveur tourne sur {host}:{port}")
    compteur = 0
    while True :
        if compteur == 10 :
            logger.warning(f"Aucun client depuis plus de 10 minute. Mise en veille du serveur")
            sys.exit()
        s.settimeout(6)                
        try :
            
            conn, addr = s.accept()
            compteur = 0
            data = conn.recv(1024)
            if not data : 
                sys.exit()
            logger.info(f"Un client ({addr[0]}) s'est connecté.")
            
            
            data = conn.recv(1024)
            
            if not data : continue
            message = data.decode()
            logger.info(f"Le client {addr[0]} a envoyé \"{message}\".")
            response = ""
            
            if "meo" in message :
                response = "Meo à toi confrère."
                conn.sendall(response.encode('utf-8'))
                logger.info(f"Réponse envoyée au client {addr[0]} : \"{response}\".")
                
                
            elif "waf" in message :
                response = "ptdr t ki"
                conn.sendall(response.encode('utf-8'))
                logger.info(f"Réponse envoyée au client {addr[0]} : \"{response}\".")
                
            else :
                response = "Mes respects humble humain."
                conn.sendall(response.encode('utf-8'))
                logger.info(f"Réponse envoyée au client {addr[0]} : \"{response}\".")
            conn.close()
            
            
            
        
        except socket.error:
            
            logger.warning(f"Aucun client depuis plus de une minute.")
            compteur += 1
            continue
        conn.close()
        
        

def main() :
    port = 13337
    host = "10.1.2.17"
    Shelp(args.help)
    if args.port != None :
        port = port_receive(int(args.port))
    if args.listen != None :
        host = host_recieve(args.listen)
    server(host, port)

main()