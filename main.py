from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
from plyer import accelerometer  # Utilisation du capteur pour Android
import socket
import time
import threading

class Client(App):
    def build(self):
        # Activation de l'accéléromètre (qui inclut le gyroscope)
        try:
            accelerometer.enable()
        except NotImplementedError:
            print("Accéléromètre non disponible sur cet appareil.")

        # Interface graphique
        layout = GridLayout(cols=1)
        self.btn_connect = Button(text="Connecter", on_release=self.start_client)
        self.lbl_status = Label(text="Statut : Déconnecté")
        self.host_input = TextInput(text='192.168.0.6', multiline=False)

        layout.add_widget(self.host_input)
        layout.add_widget(self.btn_connect)
        layout.add_widget(self.lbl_status)

        return layout

    def start_client(self, *args):
        """Démarre la connexion réseau dans un thread séparé."""
        self.HOST = self.host_input.text  # Récupère l'IP entrée
        self.PORT = 65436  # Port du serveur
        self.counter = 0

        # Lancement d'un thread pour éviter de bloquer l'UI
        self.client_thread = threading.Thread(target=self.connect_to_server)
        self.client_thread.daemon = True
        self.client_thread.start()

    def connect_to_server(self):
        """Connexion au serveur et envoi des données du gyroscope."""
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self.s.connect((self.HOST, self.PORT))
            self.update_status("Connecté")
            
            while True:
                time.sleep(0.25)
                self.send_msg()
        
        except Exception as e:
            print(f"Erreur de connexion : {e}")
            self.update_status("Connexion échouée")

    def send_msg(self):
        """Envoie les données du gyroscope au serveur."""
        self.counter += 1
        try:
            gyro_data = accelerometer.acceleration or (0, 0, 0)  # Gyroscope via accelerometer (fallback)
            msg = f"Gyro: {gyro_data[0]:.2f}, {gyro_data[1]:.2f}, {gyro_data[2]:.2f}"
            self.s.sendall(msg.encode())
            print(f"Envoyé : {msg}")
        
        except Exception as e:
            print(f"Erreur d'envoi : {e}")
            self.update_status("Erreur d'envoi")

    def update_status(self, status):
        """Met à jour le label de statut sur l'UI principale."""
        Clock.schedule_once(lambda dt: setattr(self.lbl_status, 'text', f"Statut : {status}"), 0)

    def on_stop(self):
        """Ferme la connexion proprement quand l'application se ferme."""
        try:
            self.s.close()
        except AttributeError:
            pass

if __name__ == "__main__":
    Client().run()
