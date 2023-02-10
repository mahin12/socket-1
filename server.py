import os
import socket
import sys
import csv
import socket
import time

IP = "127.0.0.1"
PORT = 4456
SIZE = 1024
FORMAT = "utf"
SERVER_FOLDER = "server_folder"

# # Create a dictionary to store usernames and passwords
user_data = {"user1": "pass1", "user2": "pass2", "pass": "pass", "try": "try"}


def main():
    print("[STARTING] Server is starting.\n")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((IP, PORT))
    server.listen()
    print("[LISTENING] Server is waiting for clients.")

    while True:
        conn, addr = server.accept()
        print(f"[NEW CONNECTION] {addr} connected.\n")

        # Authenticate the user
        authenticated = False
        while not authenticated:
            # Receive the username and password
            username = conn.recv(SIZE).decode(FORMAT)
            password = conn.recv(SIZE).decode(FORMAT)

            # Check if the username and password match
            if username in user_data and user_data[username] == password:
                authenticated = True
                conn.send("Authentication successful.".encode(FORMAT))
                print(
                    f"[AUTHENTICATION] {username} successfully authenticated.")
            else:
                conn.send("Authentication failed.".encode(FORMAT))
                print(f"[AUTHENTICATION] {username} authentication failed.")

            # set a timeout of 5 seconds for the receive operation
            conn.settimeout(5)
            try:
                username = conn.recv(SIZE).decode(FORMAT)
                password = conn.recv(SIZE).decode(FORMAT)
            except socket.timeout:
                # if the receive operation takes too long, close the connection
                print("[ERROR] Connection timed out.")
                conn.close()
                break

        """ Receiving the folder_name """
        folder_name = conn.recv(SIZE).decode(FORMAT)

        """ Creating the folder """
        folder_path = os.path.join(SERVER_FOLDER, folder_name)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            conn.send(f"Folder ({folder_name}) created.".encode(FORMAT))
        else:
            conn.send(f"Folder ({folder_name}) already exists.".encode(FORMAT))

        """ Receiving files """
        while True:
            msg = conn.recv(SIZE).decode(FORMAT)
            cmd, data = msg.split(":")

            if cmd == "FILENAME":
                """ Recv the file name """
                print(f"[CLIENT] Received the filename: {data}.")

                file_path = os.path.join(folder_path, data)
                file = open(file_path, "w")
                conn.send("Filename received.".encode(FORMAT))

            elif cmd == "DATA":
                """ Recv data from client """
                print(f"[CLIENT] Receiving the file data.")
                file.write(data)
                conn.send("File data received".encode(FORMAT))

            elif cmd == "FINISH":
                file.close()
                print(f"[CLIENT] {data}.\n")
                conn.send("The data is saved.".encode(FORMAT))

            elif cmd == "CLOSE":
                conn.close()
                print(f"[CLIENT] {data}")
                break

            # set a timeout of 5 seconds for the receive operation
            conn.settimeout(5)
            try:
                msg = conn.recv(SIZE).decode(FORMAT)
            except socket.timeout:
                # if the receive operation takes too long, close the connection
                print("[ERROR] Connection timed out.")
                conn.close()
                break


if __name__ == "__main__":
    main()
