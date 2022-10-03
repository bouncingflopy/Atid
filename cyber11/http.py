import socket
import os

ROOT = "C://Networks//webroot//"

def modify_file(file):
    if file == "" and os.path.isfile(ROOT + "index.html"):
        file = "index.html"

    if file == "oldindex.html":
        header = "HTTP/1.1 302 Moved Temporarily\r\n"
        response = header.encode()
        cs.send(response)
        file = "index.html"

    return file

def function_request(file):
    file = file.split('?')
    if file[0] == "calculate-next":
        header = "HTTP/1.1 200 OK\r\n"
        data = str(int(file[1].split("=")[1]) + 1)
        header += f'Content-Length: {str(len(data))}\r\n'
        header += "Content-Type: text/plain\r\n"
        header += "\r\n"
        response = header.encode() + data.encode()
    elif file[0] == "calculate-area":
        header = "HTTP/1.1 200 OK\r\n"
        data = file[1].split("&")
        data = str(int(data[0].split("=")[1]) * int(data[1].split("=")[1]) / 2)
        header += f'Content-Length: {str(len(data))}\r\n'
        header += "Content-Type: text/plain\r\n"
        header += "\r\n"
        response = header.encode() + data.encode()

    return response

def file_request(file):
    if os.path.isfile(ROOT + file):
        if file == "admin.txt":
            header = "HTTP/1.1 403 Forbidden\r\n"
            response = header.encode()
        else:
            with open(ROOT + file, 'rb') as f:
                lines = f.read()
                header = "HTTP/1.1 200 OK\r\n"
                header += 'Content-Length: ' + str(len(lines)) + '\r\n'

                filetype = file.split(".")[1]
                if filetype == "html" or filetype == "txt":
                    header += "Content-Type: text/html; charset=utf-8\r\n"
                elif filetype == "jpg":
                    header += "Content-Type: image/jpeg\r\n"
                elif filetype == "js":
                    header += "Content-Type: text/javascript; charset=UTF-8\r\n"
                elif filetype == "css":
                    header += "Content-Type: text/css\r\n"

                header += "\r\n"
                response = header.encode() + lines
    else:
        header = "HTTP/1.1 404 Not Found\r\n"
        response = header.encode()

    return response

s = socket.socket()
s.bind(('0.0.0.0', 80))

while True:
    s.listen()
    cs, ca = s.accept()
    data = cs.recv(1024).decode()
    data = [i.split(" ") for i in data.split("\r\n")]

    if data[0][0] == "GET":
        try:
            file = data[0][1][1:]
            file = file.replace("/", "//")

            if '?' in file:
                response = function_request(file)
            else:
                file = modify_file(file)
                response = file_request(file)
        except:
            header = "HTTP/1.1 505 Internal Server Error\r\n"
            response = header.encode()
    else:
        response = "Not in HTTP format".encode()

    cs.send(response)
    cs.close()
