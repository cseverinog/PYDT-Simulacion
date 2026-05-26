import json
import socket
import threading

HOST = "127.0.0.1"
PORT = 5000
USERS = {"cliente1": "1234", "cliente2": "1234"}
clients = {}
lock = threading.Lock()


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


def handle_client(conn):
    username = None
    file_obj = conn.makefile("r", encoding="utf-8")

    login = recv_json(file_obj)
    if not login or login.get("type") != "login":
        send_json(conn, {"type": "login_result", "ok": False, "reason": "Login invalido"})
        conn.close()
        return

    user = login.get("user")
    password = login.get("pass")
    if USERS.get(user) != password:
        send_json(conn, {"type": "login_result", "ok": False, "reason": "Credenciales invalidas"})
        conn.close()
        return

    username = user
    with lock:
        clients[username] = conn
    send_json(conn, {"type": "login_result", "ok": True})

    while True:
        msg = recv_json(file_obj)
        if not msg:
            break
        if msg.get("type") != "msg":
            continue

        to_user = msg.get("to")
        text = msg.get("text", "")

        with lock:
            to_conn = clients.get(to_user)

        if not to_conn:
            send_json(conn, {"type": "confirmed", "ok": False, "reason": "Destino no conectado"})
            continue

        send_json(to_conn, {"type": "msg", "from": username, "text": text})
        send_json(conn, {"type": "confirmed", "ok": True})

    if username:
        with lock:
            clients.pop(username, None)
    conn.close()


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, PORT))
        server.listen()
        print(f"Servidor en {HOST}:{PORT}")

        while True:
            conn, _ = server.accept()
            threading.Thread(target=handle_client, args=(conn,), daemon=True).start()


if __name__ == "__main__":
    main()
