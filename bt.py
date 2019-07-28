from bluepy.btle import DefaultDelegate, Scanner, Peripheral, ADDR_TYPE_RANDOM


class BluetoothManager:

    def __init__(self, mac=None):
        if mac is None:
            mac = '00:00:00:00:00'  # ~ Asumiendo la MAC del ESP32
        self.uuid = mac
        self.Open()

    def __async(self):
        while True:
            if self.per.waitForNotifications(1.0):
                # ~ Deberia ir al delegate
                continue
            print("Esperando...")

    def Open(self):
        self.per = Peripheral(self.uuid, ADDR_TYPE_RANDOM)
        # ~ Servicio definido en el ESP32
        self.srvc = self.per.getServiceByUUID('')
        # ~ Caracteristica definida
        self.esp_char = self.srvc.getCharacteristics('')[0]
        self.per.setDelegate(DelegateNotification(self.esp_char.getHandle()))

    def Send(self, trama):
        self.esp_char.write(trama)
        self.__async()

    def Close(self):
        self.per.disconnect()


class DelegateNotification(DefaultDelegate):
    def __init__(self, hndl):
        DefaultDelegate.__init__(self)
        print("handleNotification init")
        self.hndl = hndl

    def handleNotification(self, cHandle, data):
        if (cHandle == self.hndl):
            print("handle %s, data %s" % (cHandle, data))
        else:
            print("handle %s, checking %s" % (cHandle, data))
