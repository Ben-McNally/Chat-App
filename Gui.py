import tkinter as tk
import getpass, sys, threading, socket
username = getpass.getuser()

HEADER = 64
HOST = "192.168.1.45"
PORT = 5050
DISCONNECT_MSG = "!DISCONNECT"
FORMAT = 'utf-8'

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

disconnected = False

def send_msg(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)

def send():
    msg = chat_box.get()
    chat_box.delete(0, tk.END)
    send_msg(msg)

def accept_msg():
    if disconnected:
        return
    while True:
        msg = client.recv(2048).decode(FORMAT)
        chat.insert(tk.INSERT, f"{msg}\n")

thread = threading.Thread(target = accept_msg)
thread.start()

def disconnect():
    send_msg(DISCONNECT_MSG)
    disconnected = True
    exit()
    sys.exit()


win = tk.Tk()
win.maxsize(300, int(300 * 1.641))

title_bar = tk.Frame(win)
settings = tk.Button(title_bar, text="⚙️", relief=tk.FLAT)
settings.pack(side=tk.LEFT)
conversation = tk.Label(title_bar, text="Current Chat", anchor=tk.W)
conversation.pack(side=tk.RIGHT)
title_bar.pack(fill=tk.X)

chat = tk.Text(win, font=("Arial", 10))
chat.pack(side=tk.TOP)
chat.insert(tk.INSERT, "")
entry = tk.Frame(win, relief=tk.FLAT).pack(side=tk.BOTTOM)

chat_box = tk.Entry(entry, width=45)
send_button = tk.Button(entry, text="►", relief=tk.FLAT, command=send, font=("Arial", 10))

chat_box.pack(side=tk.LEFT, padx=(5, 0))
send_button.pack(side=tk.RIGHT)

win.protocol("WM_DELETE_WINDOW", disconnect)
win.mainloop()