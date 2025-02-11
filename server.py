import socket

def listen_forever():
    HOST = "0.0.0.0"  # Écoute sur toutes les interfaces réseau
    PORT = 65436      # Port d'écoute
    print(f"🔵 Serveur en attente de connexion sur {HOST}:{PORT}")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()

        while True:
            conn, addr = s.accept()  # Accepte une connexion
            print(f"🟢 Client connecté : {addr}")

            with conn:
                while True:
                    try:
                        data = conn.recv(1024)
                        if not data:
                            print("🔴 Client déconnecté")
                            break  # Sort de la boucle et attend un nouveau client
                        
                        data_decoded = data.decode().strip()
                        print(f"📨 Reçu : {data_decoded}")

                    except Exception as e:
                        print(f"⚠️ Erreur de réception : {e}")
                        break  # En cas d'erreur, on sort de la boucle

if __name__ == "__main__":
    listen_forever()
