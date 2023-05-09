import socket
import threading
import tkinter as tk
from tkinter import simpledialog

'''
#using tkinter for GUI
import tkinter
import tkinter.scrolledtext
from tkinter import simpledialog

HOST = '127.0.0.1'
PORT = 8000

class Client:
    def __init__(self,host,port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))

        msg = tkinter.Tk()
        msg.withdraw()

        self.nickname = simpledialog.askstring("Nickname","Please choose a nickname", parent=msg)
        self.gui_done = False
        #set to false when we stop everything
        self.running = True
        gui_thread = threading.Thread(target=self.gui_loop)
        receive_thread = threading.Thread(target=self.receive)

        gui_thread.start()
        receive_thread.start()

#can change the formatting specifications
    def gui_loop(self):
        self.win = tkinter.Tk()
        self.win.configure(bg="lightblue")
        self.chat_lab = tkinter.Label(self.win, text="Chat:", bg="lightblue")
        self.chat_lab.config(font=("Arial",12))
        self.chat_lab.pack(padx=20,pady=5)
        self.text_area = tkinter.scrolledtext.ScrolledText(self.win)
        self.text_area.pack(padx=20,pady=5)
        #dont want user to change chat history
        self.text_area.config(state='disabled')

        self.msg_lab = tkinter.Label(self.win, text="Message:", bg="lightblue")
        self.msg_lab.config(font=("Arial", 12))
        self.msg_lab.pack(padx=20, pady=5)

        self.input_area = tkinter.Text(self.win, height=3)
        self.input_area.pack(padx=20,pady=5)

        self.send_button = tkinter.Button(self.win, text="Send", command=self.write)
        #self.send_button(font=("Arial", 12))
        self.send_button.config(font=("Arial", 12), padx=20,pady=5)
        #self.send_button(padx=20, pady=5)

        self.gui_done = True
        self.win.protocol("WM_DEL_WINDOW", self.stop)

    def write(self):
        message = f"{self.nickname}: {self.input_area.get('1.0','end')}"
        self.sock.send(message.encode('utf-8'))
        self.input_area.delete('1.0','end')

    def stop(self):
        self.running = False
        self.win.destroy()
        self.sock.close()
        exit(0)

    def receive(self):
        while self.running:
            try:
                message = self.sock.recv(1024)
                if message == 'NICK':
                    self.sock.send(self.nickname_encode('utf-8'))
                else:
                    if self.gui_done:
                        self.text_area.config(state='normal')
                        self.text_area.insert('end',message)
                        self.text_area.yview('end')
                        self.text_area.config(state='disabled')

            except ConnectionAbortedError:
                break
            except:
                print("Error!")
                self.sock.close()
                break
client = Client(HOST, PORT)



'''


nickname = input("Choose nickname")
client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(('127.0.0.1', 8000))

def receive():
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send(nickname.encode('ascii'))
                pass
            else:
                print(message)
        except:
            print("Error occured")
            client.close()
            break

def write():
    while True:
        message = f'{nickname}: {input("")}'
        client.send(message.encode('ascii'))

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()

class ChatClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port

        self.root = tk.Tk()
        self.root.title("Chat Client")

        self.message_frame = tk.Frame(self.root)
        self.message_frame.pack()

        self.scrollbar = tk.Scrollbar(self.message_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.message_list = tk.Listbox(self.message_frame, height=20, width=80, yscrollcommand=self.scrollbar.set)
        self.message_list.pack(side=tk.LEFT, fill=tk.BOTH)
        self.scrollbar.config(command=self.message_list.yview)

        self.entry_field = tk.Entry(self.root)
        self.entry_field.pack()
        self.entry_field.bind("<Return>", self.send_message)

        self.send_button = tk.Button(self.root, text="Send", command=self.send_message)
        self.send_button.pack()

        self.nickname = tk.simpledialog.askstring("Nickname", "Choose a nickname:", parent=self.root)
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.host, self.port))
        self.client_socket.send(self.nickname.encode('ascii'))

        receive_thread = threading.Thread(target=self.receive)
        receive_thread.start()

        self.root.mainloop()

    def receive(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode('ascii')
                self.message_list.insert(tk.END, message)
            except:
                print("An error occurred!")
                self.client_socket.close()
                break

    def send_message(self, event=None):
        message = self.entry_field.get()
        self.entry_field.delete(0, tk.END)
        self.client_socket.send(f"{self.nickname}: {message}".encode('ascii'))
