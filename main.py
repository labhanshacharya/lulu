import base64,json
from os import path,system as sys
from hashlib import sha256
import socket as soc ,threading as t
from playsound import playsound as play
user_name = ''
def authentication():
        global user_name
        tries = 0
        while True:
            try:
                if tries == 0:
                    print('''
    __          _   _  __          _   _ 
    \\ \\  ^ ^   | | | | \\ \\  0 0   | | | |
     \\ \\  -    |^| |^|  \\ \\  -    |0| |0|
      \\ \\      | |_| |   \\ \\      | |_| |
       \\_____  |  O  |    \\_____  |  O  |\n\n''')
                    print("Login with to default credential given below if you are first logging in.\nuser_name = admin\nuser_pass = admin_pass\n")
                user_name = input("ENTER THE APPLICATION USER NAME : ")
                user_pass = input("ENTER THE APPLICATION PASSWORD : ")
                hash_in = sha256((user_name+user_pass).encode('utf-8')).hexdigest()
                with open("hash.txt","r") as f:
                    correct_hash = f.readline()
                if hash_in == correct_hash:
                    sys("cls")
                    return 1
                else:
                    if tries == 2:
                        sys("cls")
                        print("\n(^_^) SORRY TRY AGAIN LATER")
                        return 0
                    else:
                        sys("cls")
                        print("\nWRONG PASSWORD OR USER NAME")
                        tries += 1
            except:
                print("Sorry Some Technical Issue Occurred")
                exit(1)
def prompt():
    try:
        while True:
            command = input(f"lulu(^_^) [{user_name}@{str(soc.gethostbyname(soc.gethostname()))}]$ ")
            commands = ["help","change crd","send m","send f","receive f","manage d","clear","bye"]
            if command in commands:
                if command == "help":
                    print("\n ^  ^\n  ︸")
                    print('''The lulu is a simple terminal based message application which work on peer-to-peer concept.\nThe main purpose of this is to communicate any one in the lan privately\nThis are the all command and usage:\n(*) help : to print help page\n(*) send m : send message\n(*) clear : clear the screen\n(*) send f: send any file\n(*) manage d : manage contact\n(*) receive f: receive any file\n(*) bye : exit''')
                elif command == "clear":
                    sys("cls")
                elif command == "manage d":
                    manage_d()
                elif command == "change crd":
                    print(change_pass().decode())
                elif command == "receive f":
                    receive_file()
                elif command == "send f":
                    ip = input("[+] ENTER THE RECIPIENT NAME : ")
                    file_path = input("(input file path with double backslash)\nENTER THE FULL PATH OF FILE : ")
                    print(send(ip,file_path,typo="f",port=6666).decode())
                elif command == "send m":
                    contact_n = input("[+] ENTER THE RECIPIENT NAME : ")
                    with open("directory.txt", "r") as f:
                        match = json.loads(f.read())
                        if contact_n in match['Name']:
                            index_m = match['Name'].index(contact_n)
                            ip = match['IP'][index_m]
                        else:
                            print(f"{contact_n} is not in your contact list")
                            ip = input("ENTER THE RECIPIENT IP ADDRESS : ")
                    message = input("lulu(^_^) message plz : ")
                    print(send(ip,message,typo="m",port=5557).decode())
                elif command == "bye":
                    print("(^_^) GOOD BYE, SEE YOU LATER")
                    break
            elif command == "":
                continue
            else:
                print(f"(^_^) THE COMMAND \"{command}\" NOT FOUND ")
    except:
        print("Sorry Some Technical Issue Occurred")
        exit(1)
    exit(0)
def manage_d():
    try:
        with open("directory.txt", "r+") as f:
            directory_list = json.loads(f.read())
            print("(^_^) List of contacts")
            for i in range(0, len(directory_list['Name'])):
                print(f"{directory_list['Name'][i]} : {directory_list['IP'][i]}")
            choice = int(input("[1] Add contact\n[2] Remove contact\n[3] Modify contact\n(^_^) Enter your choice : "))
            if choice in range(1,4):
                f.seek(0)
                f.truncate()
                if choice == 1:
                    contact_name = input("(^_^) Name plz : ")
                    contact_ip = input("(^_^) Corresponding Ip : ")
                    directory_list['Name'].append(contact_name)
                    directory_list['IP'].append(contact_ip)
                    f.write(json.dumps(directory_list))
                    print("(^_^) Added successfully")
                elif choice == 2:
                    f.seek(0)
                    f.truncate()
                    contact_name = input("(^_^) Name plz : ")
                    if contact_name in directory_list['Name']:
                        directory_list['IP'].pop(directory_list['Name'].index(contact_name))
                        directory_list['Name'].remove(contact_name)
                        f.write(json.dumps(directory_list))
                        print("(^_^) Contact removed successfully")
                    else:
                        print("(^_^) The name is not in contacts list")
                elif choice == 3:
                    contact_name = input("(^_^) Name plz : ")
                    index_no = directory_list['Name'].index(contact_name)
                    print(f"\n{directory_list['Name'][index_no]} : {directory_list['IP'][index_no]}")
                    contact_name = input("(^_^) Name plz : ")
                    contact_ip = input("(^_^) Corresponding Ip : ")
                    directory_list['Name'].insert(index_no, contact_name)
                    directory_list['IP'].insert(index_no, contact_ip)
                    f.write(json.dumps(directory_list))
                    print("(^_^) Contact modify successfully")
            else:
                print("(^_^) plz enter correct option next time")
    except:
        print("Sorry Some Technical Issue Occurred")
def change_pass():
    try:
        username = input("ENTER THE APPLICATION USER NAME : ")
        userpass = input("ENTER THE APPLICATION PASSWORD : ")
        hash_in = sha256((username + userpass).encode('utf-8')).hexdigest()
        with open("hash.txt", "w") as f:
            f.write(hash_in)
        return b"(^_^) THE PASSWORD HAS BEEN CHANGED!"
    except:
        return b"(^_^) THEIR IS AN UNEXPECTED ERROR"
def receive_file():
    try:
        print("(^_^) LISTENING FOR FILE .....")
        listening_socket = soc.socket(soc.AF_INET, soc.SOCK_STREAM)
        listening_socket.setsockopt(soc.SOL_SOCKET, soc.SO_REUSEADDR, 1)
        listening_socket.bind(('0.0.0.0', 6665))
        listening_socket.listen(0)
        connection, address = listening_socket.accept()
        file_name = connection.recv(1024).decode()
        file_size = int(connection.recv(1024).decode())
        with open(file_name, "wb") as f:
            bytes_received = 0
            while bytes_received < file_size:
                data = connection.recv(1024)
                if not data:
                    break
                f.write(data)
                bytes_received += len(data)
        listening_socket.close()
        play("audio.mp3")
        with open("directory.txt","r") as f:
            match = json.loads(f.read())
            if address[0] in match['IP']:
                index_m = match['IP'].index(address[0])
                print(f"Received File From {match['Name'][index_m]} : {file_name}")
            else:
                print(f"Received File From Unknown :{address[0]}")
    except:
        print("THEIR IS AN UNEXPECTED ERROR")
def send(ip, data,typo, port):
    try:
        sending_socket = soc.socket(soc.AF_INET,soc.SOCK_STREAM)
        sending_socket.setsockopt(soc.SOL_SOCKET, soc.SO_REUSEADDR, 1)
        sending_socket.settimeout(10)
        sending_socket.connect((ip,port))
        if typo == "f":
            file_name = str(data.split("\\")[-1])
            sending_socket.send(file_name.encode())
            file_size = path.getsize(data)
            sending_socket.send(str(file_size).encode())
            with open(file_name, "rb") as f:
                while chunk := f.read(1024):
                    sending_socket.send(chunk)
            sending_socket.close()
            return b"(^_^) File SENT SUCCESSFULLY."
        else:
            send_data = base64.b64encode(data.encode())
            json_data = json.dumps(send_data.decode())
            sending_socket.sendall(json_data.encode())
            sending_socket.close()
            return b"SEND SUCCESSFULLY!"
    except:
        return b"THEIR IS AN UNEXPECTED ERROR"
def listener():
    try:
        while True:
                listening_socket = soc.socket(soc.AF_INET, soc.SOCK_STREAM)
                listening_socket.setsockopt(soc.SOL_SOCKET, soc.SO_REUSEADDR, 1)
                listening_socket.bind(('0.0.0.0' , 5555))
                listening_socket.listen(5)
                connection, address = listening_socket.accept()
                json_result = ''
                while True:
                    try:
                        json_result += connection.recv(1024).decode()
                        result = base64.b64decode(json.loads(json_result).encode()).decode()
                        connection.close()
                        play("audio.mp3")
                        with open("directory.txt", "r") as f:
                            match = json.loads(f.read())
                            if address[0] in match['IP']:
                                index_m = match['IP'].index(address[0])
                                print(f"\n(^_^) MESSAGE!\n{match['Name'][index_m]} :\t{result}")
                            else:
                                print(f"{address[0]} : {result}")
                        print("*** PRESS ENTER TO CONTINUE ***")
                        break
                    except:
                        print("Sorry Some Technical Issue Occurred")
                        break
    except:
        print("Sorry Some Technical Issue Occurred")
        exit(1)
auth = authentication()
if auth == 1:
    prompt_thread = t.Thread(target=prompt)
    listener_thread = t.Thread(target=listener, daemon=True,name='lulu_message_listener')
    listener_thread.start()
    prompt_thread.start()
else:
    exit(1)
