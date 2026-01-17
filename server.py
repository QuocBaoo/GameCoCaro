# server.py
import socket, threading, json
from const import *

clients = [] 
rooms = {}       
client_names = {} 
scores = {} # {conn: score}

def send_json(conn, data):
    try: conn.send((json.dumps(data) + "\n").encode(FORMAT))
    except: pass

def handle_client(conn, addr):
    try:
        data = conn.recv(BUFF_SIZE).decode(FORMAT)
        name = json.loads(data).get('name', 'User')
        client_names[conn] = name
        scores[conn] = 0
        clients.append(conn)

        if len(clients) % 2 == 0:
            opp = clients[-2]
            rooms[conn] = opp; rooms[opp] = conn
            # Gửi tên đối thủ và điểm số ban đầu
            send_json(opp, {"type": MSG_START, "symbol": "X", "turn": True, "opp_name": name, "s1": 0, "s2": 0})
            send_json(conn, {"type": MSG_START, "symbol": "O", "turn": False, "opp_name": client_names[opp], "s1": 0, "s2": 0})
        else:
            send_json(conn, {"type": MSG_WAIT})

        while True:
            raw = conn.recv(BUFF_SIZE).decode(FORMAT)
            if not raw: break
            for line in raw.strip().split("\n"):
                msg = json.loads(line)
                opp = rooms.get(conn)
                if not opp: continue

                if msg['type'] == MSG_WIN:
                    scores[conn] += 1
                    # Reset ván mới ngay lập tức
                    send_json(conn, {"type": MSG_START, "symbol": "X", "turn": True, "opp_name": client_names[opp], "s1": scores[conn], "s2": scores[opp]})
                    send_json(opp, {"type": MSG_START, "symbol": "O", "turn": False, "opp_name": client_names[conn], "s1": scores[opp], "s2": scores[conn]})
                else:
                    send_json(opp, msg)
    except: pass
    finally:
        if conn in clients: clients.remove(conn)
        conn.close()

if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT)); s.listen()
    print(f"Server Pro đang chạy...")
    while True:
        c, a = s.accept()
        threading.Thread(target=handle_client, args=(c, a), daemon=True).start()