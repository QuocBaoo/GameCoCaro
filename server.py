import socket
import threading
import json
from const import *

clients = [] 
rooms = {}       
client_names = {} 

def handle_client(conn, addr):
    print(f"[KET NOI MOI] {addr}")
    try:
        # Nhan ten nguoi choi
        data = conn.recv(BUFF_SIZE).decode(FORMAT)
        first_msg = json.loads(data)
        name = first_msg.get('name', 'VoDanh')
        client_names[conn] = name
        print(f"[DANG NHAP] {name} tu {addr}")

        # Ghep cap
        if len(clients) % 2 != 0:
            send_json(conn, {"type": MSG_WAIT})
        else:
            if len(clients) > 0:
                opponent = clients[-1] 
                rooms[conn] = opponent
                rooms[opponent] = conn
                
                # Gui thong bao BAT DAU
                send_json(conn, {"type": MSG_START, "symbol": "O", "turn": False, "opponent_name": client_names[opponent]})
                send_json(opponent, {"type": MSG_START, "symbol": "X", "turn": True, "opponent_name": client_names[conn]})
                print(f"[GHEP CAP] {client_names[conn]} vs {client_names[opponent]}")

        clients.append(conn)

        # Nhan tin nhan trong tran
        while True:
            data = conn.recv(BUFF_SIZE).decode(FORMAT)
            if not data: break
            msg = json.loads(data)
            
            opponent = rooms.get(conn)
            if not opponent: continue

            if msg['type'] == MSG_MOVE:
                send_json(opponent, msg)
            elif msg['type'] == MSG_WIN:
                send_json(opponent, {"type": MSG_LOSE})

    except: pass
    finally:
        print(f"[THOAT] {addr}")
        opponent = rooms.get(conn)
        if opponent:
            try:
                send_json(opponent, {"type": MSG_DISCONNECT})
                opponent.close()
            except: pass
        if conn in clients: clients.remove(conn)
        if conn in client_names: del client_names[conn]
        if conn in rooms: del rooms[conn]
        conn.close()

def send_json(conn, data):
    try: conn.send(json.dumps(data).encode(FORMAT))
    except: pass

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"[SERVER DANG CHAY] {HOST}:{PORT}")
    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_client, args=(conn, addr)).start()

if __name__ == "__main__":
    start_server()