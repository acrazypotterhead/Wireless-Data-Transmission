import socket
import time
import threading
import logging
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

# Configure logging
logging.basicConfig(filename='client.log', level=logging.DEBUG, format='%(asctime)s %(message)s')

class Client(App):
    counter = 0

    def build(self):
        # Specific to iOS
        #Bridge = autoclass('bridge')
        #self.br = Bridge.alloc().init()
        #self.br.startGyroscope()

        # ip found using socket.gethostbyname(socket.gethostname()) on the server (your computer)
        g = GridLayout(cols=1)
        b = Button(on_release=self.go)
        self.l = Label()
        self.host = TextInput(text='192.168.56.1')
        g.add_widget(b)
        g.add_widget(self.host)
        g.add_widget(self.l)
        return g

    def go(self, *args):
        try:
            HOST = self.host.text
            PORT = 65436  # The port used by the server
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            logging.debug(f"Tentative de connexion à {HOST}:{PORT}")
            self.s.connect((HOST, PORT))
            logging.debug("Connexion réussie")

            # Exécuter la boucle dans un thread séparé
            threading.Thread(target=self.run_loop).start()
        except Exception as e:
            logging.error(f"Erreur lors de la connexion : {e}")

    def run_loop(self):
        try:
            while True:
                time.sleep(.25)
                self.send_msg()
        except Exception as e:
            logging.error(f"Erreur dans run_loop : {e}")

    def send_msg(self, *args):
        try:
            gyro_data = "hello world"
            self.s.sendall(str(gyro_data).encode('utf-8'))
            logging.debug("Message envoyé")
        except Exception as e:
            logging.error(f"Erreur lors de l'envoi du message : {e}")

    def on_stop(self):
        if self.s:
            self.s.close()
            logging.debug("Connexion fermée")

Client().run()