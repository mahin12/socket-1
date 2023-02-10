from tqdm import tqdm
import os
import socket
import sys
import time
import datetime

# #lets add a password

# password = input("Enter the password to start transferring: ")
# if password == "secret":
#     # code to transfer the file
#     print("File transfer successful")
# else:
#     print("Incorrect password. File transfer failed.")

IP = "127.0.0.1"
PORT = 4456
SIZE = 1024
FORMAT = "utf"
CLIENT_FOLDER = "client_folder"


def main():
    #Starting a tcp socket
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((IP, PORT))

    # Prompt the user to enter the username and password
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    # Send the username and password to the server
    client.send(username.encode(FORMAT))
    client.send(password.encode(FORMAT))

    # Receive the authentication result
    msg = client.recv(SIZE).decode(FORMAT)
    print(f"[SERVER] {msg}")
    while True:
        msg = client.recv(SIZE).decode(FORMAT)
        if not msg:
            print("[ERROR] Connection with the client closed.")
            break
        cmd, data = msg.split(":")

    if msg == "Authentication successful.":
        """ The rest of the file transfer code """
    else:
        print("[ERROR] Authentication failed. Exiting...")
        client.close()
        sys.exit(0)

    # This part adds the progress bar to my program

    total = 100
    with tqdm(total=total) as pbar:
        for i in range(total):
            time.sleep(0.1)
            pbar.update(1)

    #Folder path
    path = os.path.join(CLIENT_FOLDER, "files")
    folder_name = path.split("/")[-1]

    #Sending the folder name
    msg = f"{folder_name}"
    print(f"[CLIENT] Sending folder name: {folder_name}")
    client.send(msg.encode(FORMAT))

    #Receiving the reply from the server
    msg = client.recv(SIZE).decode(FORMAT)
    print(f"[SERVER] {msg}\n")

    #Sending files
    files = sorted(os.listdir(path))

    for file_name in files:
        #Send the file name
        msg = f"FILENAME:{file_name}"
        print(f"[CLIENT] Sending file name: {file_name}")
        client.send(msg.encode(FORMAT))

        #Recieve the reply from the server
        msg = client.recv(SIZE).decode(FORMAT)
        print(f"[SERVER] {msg}")
        

        #Send the data
        file = open(os.path.join(path, file_name), "r")
        file_data = file.read()

        msg = f"DATA:{file_data}"
        client.send(msg.encode(FORMAT))
        msg = client.recv(SIZE).decode(FORMAT)
        print(f"[SERVER] {msg}")
        
        #Sending the close command
        msg = f"FINISH:Complete data send"
        client.send(msg.encode(FORMAT))
        msg = client.recv(SIZE).decode(FORMAT)
        print(f"[SERVER] {msg}")


        

        # Adding transfer history
        with open("transfer_history_log.txt", "a") as f:
            current_time = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

    #Closing the connection from the server
    msg = f"CLOSE:File transfer is completed"
    client.send(msg.encode(FORMAT))
    client.close()


if __name__ == "__main__":
    main()



