# import claraVR
# import pythomation
import time
import socket
class CRole:
    def Header(self):
        # description
        self.description.title = 'Role'

    def displayhex(self, bytes):
        ls = []
        for x in bytes:
            ls.append(hex(x))
        return ls

    def trigger(self, chanel, state):
        s = socket.socket()         # Create a socket object
        host = '192.168.1.253' # Get local machine name
        port = 1030                # Reserve a port for your service.
        data = bytes.fromhex('483A0157'+ chanel + state + '00004544')
        s.connect((host, port))
        print('Send:' + str(self.displayhex(data)))
        s.send(data)
        data2 = s.recv(1024)
        print('Receive:' + str(self.displayhex(data2)))
        s.close()
    
    def test_write(self, data_send):
        s = socket.socket()         # Create a socket object
        host = '192.168.1.253' # Get local machine name
        port = 1030                # Reserve a port for your service.

        # Convert the hexadecimal string to bytes
        byte_array = bytes.fromhex(data_send)

        # Convert the bytes object to a list of integers
        byte_list = list(byte_array)
        print(byte_list)
        # data = bytes.fromhex('483A01575555555555555555824544')
        # data = bytes.fromhex('483A01570000000000000000da4544')
        checksum = hex(0x48+0x3A+0x01+0x57)
        for i in range(8):
            checksum = hex(0x48+0x3A+0x01+0x57 + int(hex(byte_list[i]),16))
            print(checksum)
        data_str = '483A0157' + data_send + checksum[2:] + '4544'
        data = bytes.fromhex(data_str)
        s.connect((host, port))
        print('Send:' + str(self.displayhex(data)))
        s.send(data)
        data2 = s.recv(1024)
        print('Receive:' + str(self.displayhex(data2)))
        checksum = 0
        s.close()

    def test_ascii(self):
        s = socket.socket()         # Create a socket object
        host = '192.168.1.253' # Get local machine name
        port = 1030                # Reserve a port for your service.
        command = 'zq 1 set y02 2 qz'
        s.connect((host, port))
        print('Send:' + command)
        s.send(command.encode(encoding="ascii"))
        ret = s.recv(1024)
        print('Receive:' + ret.decode(encoding="ascii"))
        s.close()

    def OpenState(self):
        self.trigger('01', '00')

    def GNDState(self):
        self.trigger('01', '01')
        self.trigger('02', '00')

    def VCCState(self):
        self.trigger('01', '01')
        self.trigger('02', '01')
                
    def BusoffEN(self, chanel):
        if chanel == '01':
            self.trigger('05', '01')
        if chanel == '02':
            self.trigger('06', '01')
        self.result.passed('BusOff trigger channel {0}'.format(chanel))

    def BusoffDIS(self, chanel):
        if chanel == '01':
            self.trigger('05', '00')
        if chanel == '02':
            self.trigger('06', '00')
        self.result.passed('BusOff release channel {0}'.format(chanel))

    def ResetPort(self):
        for i in range(1, 8, 1):
            channel = "0{0}".format(i)
            self.trigger(channel, '00')
            time.sleep(0.5)

Role = CRole()

if __name__ == "__main__":
    Role.test_write('0000000000000000')
    # time.sleep(3)
    # Role.BusoffDIS('01')

