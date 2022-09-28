import socket
import os

ROOT = "D://Users//flopybouncer//Downloads//webroot//"

s = socket.socket()
s.bind(('0.0.0.0', 80))

while True:
    s.listen()
    cs, ca = s.accept()
    data = cs.recv(1024).decode()
    data = [i.split(" ") for i in data.split("\r\n")]

    if data[0][0] == "GET":
        file = data[0][1][1:]
        file = file.replace("/", "//")

        if file == "" and os.path.isfile(ROOT + "index.html"):
            file = "index.html"

        if file == "oldindex.html":
            header = "HTTP/1.1 302 Moved Temporarily\r\n"
            response = header.encode()
            cs.send(response)
            file = "index.html"
        elif os.path.isfile(ROOT + file):
            if file == "admin.txt":
                header = "HTTP/1.1 403 Forbidden\r\n"
                response = header.encode()
            else:
                with open(ROOT + file, 'rb') as f:
                    lines = f.read()
                    header = "HTTP/1.1 200 OK\r\n"
                    header += f'Content-Length: {len(lines)}\r\n'

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

    else:
        header = "HTTP/1.1 505 Internal Server Error\r\n"
        response = header.encode()

    cs.send(response)
    cs.close()
    
