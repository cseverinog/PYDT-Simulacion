import json
import socket
import threading

HOST = "127.0.0.1"
PORT = 5000
DEFAULT_USERNAME = "cliente1"
DEFAULT_PASSWORD = "1234"
DESTINATION = "cliente2"


def send_json(conn, data):
    conn.sendall((json.dumps(data) + "\n").encode("utf-8"))


def recv_json(file_obj):
    line = file_obj.readline()
    if not line:
        return None
    try:
        return json.loads(line.strip())
    except Exception:
        return None


def login(conn, file_obj, username, password):
    send_json(conn, {"type": "login", "user": username, "pass": password})
    response = recv_json(file_obj)
    return response and response.get("ok")


def show(packet):
    if packet.get("type") == "confirmed":
        print("[CONFIRMED] Mensaje entregado" if packet.get("ok") else "[CONFIRMED-ERROR] No entregado")
    elif packet.get("type") == "msg":
        print(f"\n[RECIBIDO] {packet.get('from')}: {packet.get('text')}")


def receive_loop(file_obj):
    while True:
        packet = recv_json(file_obj)
        if not packet:
            print("\n[INFO] Conexion cerrada por servidor")
            return
        show(packet)


def ask_credentials():
    user = input(f"Usuario [{DEFAULT_USERNAME}]: ").strip() or DEFAULT_USERNAME
    password = input(f"Clave [{DEFAULT_PASSWORD}]: ").strip() or DEFAULT_PASSWORD
    return user, password


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as conn:
        conn.connect((HOST, PORT))
        file_obj = conn.makefile("r", encoding="utf-8")

        username, password = ask_credentials()
        if not login(conn, file_obj, username, password):
            print("Login fallido")
            return

        threading.Thread(target=receive_loop, args=(file_obj,), daemon=True).start()
        print(f"Conectado como {username}. Envia a {DESTINATION}. Escribe 'salir'.")
        while True:
            text = input("> ").strip()
            if text.lower() == "salir":
                break
            if not text:
                continue
            send_json(conn, {"type": "msg", "to": DESTINATION, "text": text})


if __name__ == "__main__":
    main()
