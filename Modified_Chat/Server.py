import socket
import threading
import pickle
userpass = {} 
clientuser = {}
clientAvatar = {}
HeaderSize = 10
recvsize = 20
clients = []
onlineusers = []
clientmessage = []
clientmessagename = []
userimage = []
userimagename = []
clientMessageMapper = []
clientMessageMapperIndex = []
namefontdict = {}
# Font, fontsize, background-color, font-color, border-color 
defaultFont = ["FZHTJW", 9, "#12b7f5", "white", "#12b7f5"]


def getlentext(c):
    usname = ""
    unba = bytearray()
    b = c.recv(HeaderSize)
    namelen = int(b)
    while True:
        b = c.recv(1)
        unba.extend(b)
        try:
            usname = unba.decode("utf-8")
        except:
            continue
        if len(usname) == namelen:
            break
    return usname


def getclientmessage(c, usnamefromclient):
    global recvsize
    full_msg = ""
    usname =  clientuser[c]
    if usnamefromclient != usname:
        print("Client name does not match with server data")
        return
    fullmsginbyte = bytearray()
    try:
        b = c.recv(HeaderSize)
        msglen = int(b)
    except:
        c.close()
        print("client close in Connection")
    while True:
        try:
            msg = c.recv(recvsize)
        except:
            print("Error occurred on server side when getting message")
            c.close()
            return
        fullmsginbyte.extend(msg)
        try:
            full_msg = fullmsginbyte.decode("utf-8")
        except:
            continue
        if len(full_msg) == msglen:
            clientmessagename.append(usname)
            clientmessage.append(full_msg)
            clientMessageMapper.append(full_msg)
            clientMessageMapperIndex.append('T' + usname)
            print("Received full msg as " + full_msg)
            full_msg =  'T' + f'{len(usname):<{HeaderSize}}'+ usname  + f'{len(full_msg):< {HeaderSize}}' + full_msg
            sendtootherclients(c, full_msg)
            print("Sent message back to other clients")
            break

def sendtootherclients(c, msg):
    for client in clients:
        if client is not c:
            try:
                client.send(bytes(msg, 'utf-8'))
            except:
                client.close()
                print("close in send to other clients")

def sendtoself(c, msg):
    try:
        c.send(bytes(msg,'utf-8'))
    except:
        c.close()
        print("close in send to self with msg: " + msg)

def updateonlineclients(broadcastsig, c):
    lenname = 'U' + f'{len(onlineusers):<{HeaderSize}}'
    for username in onlineusers:
        lenname += f'{len(username):<{HeaderSize}}' + username
    if broadcastsig == 0:
        sendtootherclients(c, lenname)
    elif broadcastsig == 1:
        sendtoself(c, lenname)

    nameavatar = bytes('V' + f'{len(clientAvatar):<{HeaderSize}}', "utf-8")
    for client in clientAvatar.keys():
        imgdata = clientAvatar[client]
        nameavatar += bytes(f'{len(client):<{HeaderSize}}' + client + f'{len(imgdata):<{HeaderSize}}',"utf-8") +  imgdata
    try:
        c.send(nameavatar)
    except:
        c.close()
        print("client close in Connection")

    namefont = bytes('B' + f'{len(namefontdict):<{HeaderSize}}' , "utf-8")
    for name in namefontdict.keys():
        fontdata = namefontdict[name]
        fontdatatosend = pickle.dumps(fontdata)
        namefont += bytes(f'{len(name):<{HeaderSize}}' + name + f'{len(fontdatatosend):<{HeaderSize}}', "utf-8") + fontdatatosend
    try:
        c.send(namefont)
    except:
        c.close()
        print("client close in Connection")
    


def broadcast(broadcastsig, client):
    if broadcastsig == 0:
        if clientuser[client] is None:
            return
        else:
            usname = clientuser[client]
            del clientuser[client]
            onlineusers.remove(usname)
            signalbyte = 'L'
            msg = signalbyte + f'{len(usname):<{HeaderSize}}' + usname
            sendtootherclients(client, msg)
            updateonlineclients(0,client)

    if broadcastsig == 1:
        usname = getlentext(client)
        print("broadcasting name = " + usname)
        if usname not in userpass.keys():
            print("usname not in dict")
            prompt = usname + "不存在"
            failtologinmsg = 'F' + f'{len(usname):<{HeaderSize}}' + usname +  f'{len(prompt):<{HeaderSize}}' + prompt
            client.send(bytes(failtologinmsg, 'utf-8'))
            return
        else:
            uspass = userpass[usname]
            print("uspass = " + uspass)
            inputpass = getlentext(client)
            print("inputpass = " + inputpass)
            if uspass != inputpass:
                prompt = "密码错误"
                failtologinmsg = 'F' + f'{len(usname):<{HeaderSize}}' + usname +  f'{len(prompt):<{HeaderSize}}' + prompt
                client.send(bytes(failtologinmsg, 'utf-8'))
                return
            else:
                onlineusers.append(usname)
                clientuser.update({client:usname})
                namefontdict[usname] = defaultFont
                signalbyte = 'J'
                msg = signalbyte + f'{len(usname):<{HeaderSize}}' + usname
                sendtoself(client, msg)
                sendtootherclients(client, msg)
                updateonlineclients(1,client)
                updateonlineclients(0,client)
                

def getAvatar(c ,username):
    global recvsize
    global clientAvatar
    full_msg = b''
    usname =  clientuser[c]
    if username != usname:
        print("Client name does not match with server data")
        return
    try:
        b = c.recv(HeaderSize)
        msglen = int(b)
        print("Received msg length of " + f'{msglen}')
    except:
        c.close()
        print("client close in Connection")
    while True:
        try:
            msg = c.recv(recvsize)
        except:
            print("Error occurred on server side when getting message")
            c.close()
            print("client close in Connection")
            return
        full_msg += msg
        
        if len(full_msg)-3 == msglen:
            #print(full_msg)
            clientAvatar[username] = full_msg
            avatartosend = bytes('A' + f'{len(username):<{HeaderSize}}' + username + f'{msglen:<{HeaderSize}}', "utf-8") + full_msg
            for client in clients:
                if client is not c:
                    try:
                        client.send(avatartosend)
                    except:
                        client.close()

            print("Sent message back to other clients")
            break
def getImageData(c, username):
    global userimage
    global userimagename
    global clientMessageMapperIndex
    full_img_data = b''
    try:
        imgsize = int(c.recv(HeaderSize))
        print("image size is "+ f'{imgsize}')
    except:
        c.close()
        print("client close in Connection")
        return
    while True:
        try:
            data = c.recv(recvsize)
        except:
            c.close()
            print("client close in Connection")
            return
        full_img_data += data
        if len(full_img_data) -3 == imgsize:
            print("Retrieve all img data")
            userimage.append(full_img_data)
            userimagename.append(username)
            clientMessageMapper.append(full_img_data)
            clientMessageMapperIndex.append('I' + username)
            imgdatatosend = bytes('I' + f'{len(username):<{HeaderSize}}' + username + f'{imgsize:<{HeaderSize}}', "utf-8") + full_img_data
            for client in clients:
                if client is not c:
                    try:
                        client.send(imgdatatosend)
                        #print("sent to client " + client)
                    except:
                        client.close()
                        #print("closed during sending imgfile")
            print("ImgFile sent back")
            break

def run(c, a):
    global namefontdict
    global defaultFont
    while True:
        try:
            sig = c.recv(1)
            print(sig)
        except:
            broadcast(0, c)
            print("Failed to receive 1 byte")
            break
        signal = sig.decode("utf-8")
        print("successful got 1 byte, as " + signal)
        if signal == 'L':
            print("got message to login")
            broadcast(1, c)
        elif signal == 'T':
            usname = getlentext(c)
            if usname == "":
                continue
            print("Receive T and username is: " + usname)
            getclientmessage(c, usname)
        elif signal == 'R':
            username = getlentext(c)
            if username == "":
                continue
            password = getlentext(c)
            if password == "":
                continue
            if username in userpass.keys():
                prompt = username + "已经注册过"
                failtologinmsg = 'W' + f'{len(username):<{HeaderSize}}' + username +  f'{len(prompt):<{HeaderSize}}' + prompt
                c.send(bytes(failtologinmsg, 'utf-8'))
                continue
            userpass.update({username:password})
            prompt = username + "注册成功"
            failtologinmsg = 'S' + f'{len(username):<{HeaderSize}}' + username +  f'{len(prompt):<{HeaderSize}}' + prompt
            #namefontdict[username] = defaultFont
            c.send(bytes(failtologinmsg, 'utf-8'))

        elif signal == 'A':
            username = getlentext(c)
            if username == "":
                continue
            getAvatar(c, username)
        elif signal == 'M':
            if len(clientMessageMapperIndex) == 0:
                try:
                    c.send('M' + f'{0:<{HeaderSize}}', "utf-8")
                except:
                    continue
            signalbyte = 'M'
            fullmsg = bytes(signalbyte + f'{len(clientMessageMapperIndex):<{HeaderSize}}',"utf-8")
            for i in range(0,len(clientMessageMapperIndex)):
                datatype = clientMessageMapperIndex[i][0]
                username = clientMessageMapperIndex[i][1:]
                data = clientMessageMapper[i]
                if datatype == 'T':
                    fullmsg += bytes(f'{len(username):<{HeaderSize}}' + username + datatype + f'{len(data):<{HeaderSize}}' + data, "utf-8")
                elif datatype == 'I':
                    fullmsg += bytes(f'{len(username):<{HeaderSize}}' + username + datatype + f'{len(data):<{HeaderSize}}', "utf-8") + data
            head = 0
            tail = 0
            while True:
                try:
                    tail += recvsize
                    if len(fullmsg) <= tail:
                        tail = len(fullmsg)
                    c.send(fullmsg[head:tail])
                except:
                    c.close()
                    print("client close in Connection")
                head = tail
                if tail == len(fullmsg):
                    break

            
        elif signal == 'Q':
            try:
                username = getlentext(c)
                sizeofbytes = int(c.recv(HeaderSize))
                fontlistbyte = c.recv(sizeofbytes)
                fontlist = pickle.loads(fontlistbyte)
                namefontdict[username] = fontlist
            except:
                c.close()
                print("client close in Connection")
            
            signalbyte = 'Q'
            fullmsg = bytes(signalbyte + f'{len(username):<{HeaderSize}}' + username + f'{sizeofbytes:<{HeaderSize}}', "utf-8") + fontlistbyte
            for client in clients:
                if clients != c:
                    try:
                        client.send(fullmsg)
                    except:
                        client.close()
                        print("client close in Connection")
                


        elif signal == 'I':
            print("Start getting image file")
            username = getlentext(c)
            print("Username is " + username)
            if username == "":
                continue
            getImageData(c, username)



    

if __name__ == "__main__":
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            print("Successfully set up socket")
        except:
            print("An error has occured when setting up socket")
            continue
        try:
            #s.bind((socket.gethostname(), 1234))
            s.bind(('', 1234))
            print("Successfully bind to socket")
            break
        except:
            print("An error has occured when binding to port 1234")
            continue

    s.listen(5)
    userpass.update({"admin":"password"})
    userpass.update({"root":"password"})
    #userpass.update({"丢那黄":"diunahuang"})
    #userpass.update({"丢那池":"diunachi"})
    while True:
        c, a = s.accept()
        clients.append(c)
        print(f"Connection from {a} has been established!")
        newThread = threading.Thread(target=run, args=[c, a])
        newThread.daemon = True
        newThread.start()
       
