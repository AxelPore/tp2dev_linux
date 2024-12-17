import socket
import sys 
import re
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
            logging.ERROR: self.red + "%(asctime)s" + self.fmt  + " %(message)s"+ self.reset,
            logging.CRITICAL: "%(asctime)s" + self.bold_red + self.fmt + self.reset + " %(message)s",
            
        }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, datefmt="%Y-%m-%d %H:%M:%S")
        return formatter.format(record)

file_handler = logging.FileHandler("/var/log/bs_clientlog/bs_server.log", mode="a", encoding="utf-8")
file_handler.setLevel(10)
file_handler.setFormatter(logging.Formatter(fmt2))

console_handler = logging.StreamHandler()
console_handler.setLevel(40)
console_handler.setFormatter(CustomFormatter(fmt))

logger.addHandler(console_handler)
logger.addHandler(file_handler)

host = "10.1.2.17"
port = 13337

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)



try :
    s.connect((host, port))
    s.sendall(b"Hello there")
    print(f"Connecté avec succès au serveur {host} sur le port {port}")
    logger.info(f"Connexion réussie à {host}:{port}.")
except :
    logger.error(f"Impossible de se connecter au serveur {host} sur le port {port}.")
    sys.exit()

message = input('Que veux-tu envoyer au serveur : ')
if type(message) != str :
    raise TypeError
elif not re.search(r'[a-z,A-Z,0-9,\s]*(meo)[a-z,A-Z,0-9,\s]*|[a-z,A-Z,0-9,\s]*(waf)[a-z,A-Z,0-9,\s]*', message):
    raise ValueError("Data not sent, can only send 'meo' or 'waf'. Piece of shit of human !")
s.sendall(message.encode('utf-8'))
logger.info(f"Message envoyé au serveur {host} : {message}.")
data = s.recv(1024)

response = data.decode()
logger.info(f"Réponse reçue du serveur {host} : {response}.")
print(f"Le serveur a répondu {repr(response)}")

s.close()

sys.exit()