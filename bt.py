import bluetooth as BT
import threading


class BluetoothManager:

    def Open(self):
        print("Pase por aqui")
        self.nearby_devices = BT.discover_devices(lookup_names=True)
        self.s = BT.BluetoothSocket(BT.RFCOMM)
        print(self.nearby_devices)
        print(self.nearby_devices)
        for addr, name in self.nearby_devices:
            if name == "ESP32test":
                service = BT.find_service(address=addr)
                first_match = service[0]
                port = first_match["port"]
                name = first_match["name"]
                host = first_match["host"]
                self.s.connect((host, 1))
                self.s.send("CONECTADO")
                print("CONECTADO")

        while True:
            server_sock = BT.BluetoothSocket(BT.RFCOMM)
            server_sock.bind(("", BT.PORT_ANY))
            server_sock.listen(1)

            port = server_sock.getsockname()[1]

            ## uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

            #~ advertise_service( server_sock, "SampleServer",service_id = uuid,service_classes = [ uuid, SERIAL_PORT_CLASS ], profiles = [ SERIAL_PORT_PROFILE ],)
            # protocols = [ OBEX_UUID ]

            print("Waiting for connection on RFCOMM channel %d" % port)

            client_sock, client_info = server_sock.accept()
            print("Accepted connection from ", client_info)

            try:
                while True:
                    data = client_sock.recv(1024)
                    if len(data) == 0:
                        break
                    print("received [%s]" % data)
            except IOError:
                pass

            print("disconnected")

            client_sock.close()
            server_sock.close()
            print("all done")

    def EnviarInformacion(self, trama):
        self.nearby_devices = BT.discover_devices(lookup_names=True)
        self.s = BT.BluetoothSocket(BT.RFCOMM)
        #~ print(self.nearby_devices)
        for addr, name in self.nearby_devices:
            if name == "ESP32test":
                service = BT.find_service(address=addr)
                first_match = service[0]
                ## port = first_match["port"]
                name = first_match["name"]
                host = first_match["host"]
                self.s.connect((host, 1))
                self.s.send(trama)
        self.s.close()

    def EscucharBT(self):
        print('Hello')
        # self.AbrirConexionBT()
        # ~ while True:
        # ~ server_sock=BluetoothSocket( RFCOMM )
        #~ print("DEspues del RFCOMM")

        # ~ port = 2
        #~ server_sock.bind(("",port))
        #~ print("Despues del bind")
        #~ server_sock.listen(2)
        #~ print("despues del listen")

        # ~ client_sock,address = server_sock.accept()
        #~ print("Accepted connection from " + str(address))

        # ~ data = client_sock.recv(1024)
        #~ print("received [%s]" % data)
        #~ print("Aqui en el while")
        #~ sleep(0.1)
        # ~ server_sock=BluetoothSocket( L2CAP )
        #~ print("AQui despues de server sock")

        # ~ port = 0x1001

        #~ server_sock.bind(("",port))
        #~ print("AQui despues de .bind")
        #~ server_sock.listen(1)
        #~ print("Aqui despues de listen 1")

        # ~ #uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ef"
        # ~ #bluetooth.advertise_service( server_sock, "SampleServerL2CAP",
        # ~ #                   service_id = uuid,
        # ~ #                   service_classes = [ uuid ]
        # ~ #                    )

        # ~ client_sock,address = server_sock.accept()
        #~ print("Accepted connection from ",address)

        # ~ data = client_sock.recv(1024)
        #~ print("Data received: ", str(data))

        # ~ while data:
        #~ print("Aqui en while data")
        #~ client_sock.send('Echo => ' + str(data))
        # ~ data = client_sock.recv(1024)
        #~ print("Data received:", str(data))
