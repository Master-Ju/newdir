import socket
from PyQt5.QtWidgets import QMainWindow, QTableView, QTextEdit
from PyQt5.QtCore import QAbstractTableModel, Qt
import binascii

class PacketTableModel(QAbstractTableModel):
    def __init__(self, data=None):
        super().__init__()
        self._data = data or []

    def rowCount(self, parent=None):
        return len(self._data)

    def columnCount(self, parent=None):
        return len(Packet.fields)

    def headerData(self, section, orientation, role):
        if role != Qt.DisplayRole:
            return None
        if orientation == Qt.Horizontal:
            return Packet.fields[section].name
        else:
            return str(section + 1)

    def data(self, index, role):
        if role == Qt.DisplayRole:
            packet = self._data[index.row()]
            field = Packet.fields[index.column()]
            value = getattr(packet, field.value_name)
            if field.name == 'Source' or field.name == 'Destination':
                return ':'.join(f'{c:02x}' for c in value)
            else:
                return str(value)
        else:
            return None

class Packet:
    fields = []

    def __init__(self, raw_data):
        self.raw_data = raw_data
        for field in self.fields:
            setattr(self, field.value_name, field.parse(raw_data))

    def __len__(self):
        return len(self.raw_data)

class EthernetField:
    def __init__(self, name, offset, length):
        self.name = name
        self.offset = offset
        self.length = length
        self.value_name = name.lower()

    def parse(self, raw_data):
        value = raw_data[self.offset:self.offset + self.length]
        if self.name == 'Source' or self.name == 'Destination':
            return bytes(value)
        else:
            return int.from_bytes(value, byteorder='big')

class Ethernet(Packet):
    fields = [
        EthernetField('Destination', 0, 6),
        EthernetField('Source', 6, 6),
        EthernetField('Type', 12, 2)
    ]

class IPv4Field:
    def __init__(self, name, offset, length):
        self.name = name
        self.offset = offset
        self.length = length
        self.value_name = name.lower()

    def parse(self, raw_data):
        value = raw_data[self.offset:self.offset + self.length]
        if self.name == 'Source' or self.name == 'Destination':
            return socket.inet_ntoa(value)
        else:
            return int.from_bytes(value, byteorder='big')

class IPv4(Packet):
    fields = [
        IPv4Field('Version', 0, 1),
        IPv4Field('IHL', 0, 1),
        IPv4Field('DSCP', 1, 1),
        IPv4Field('ECN', 1, 1),
        IPv4Field('Total Length', 2, 2),
        IPv4Field('Identification', 4, 2),
        IPv4Field('Flags', 6, 2),
        IPv4Field('Fragment Offset', 6, 2),
        IPv4Field('Time to Live', 8, 1),
        IPv4Field('Protocol',    9, 1),
        IPv4Field('Header Checksum', 10, 2),
        IPv4Field('Source', 12, 4),
        IPv4Field('Destination', 16, 4)
    ]

class TCPField:
    def init(self, name, offset, length):
        self.name = name
        self.offset = offset
        self.length = length
        self.value_name = name.lower()

    def parse(self, raw_data):
        value = raw_data[self.offset:self.offset + self.length]
        return int.from_bytes(value, byteorder='big')

class TCP(Packet):
    fields = [
        TCPField('Source Port', 0, 2),
        TCPField('Destination Port', 2, 2),
        TCPField('Sequence Number', 4, 4),
        TCPField('Acknowledgment Number', 8, 4),
        TCPField('Data Offset', 12, 1),
        TCPField('Reserved', 12, 1),
        TCPField('Flags', 13, 1),
        TCPField('Window Size', 14, 2),
        TCPField('Checksum', 16, 2),
        TCPField('Urgent Pointer', 18, 2)
    ]

class UDPPacket(Packet):
    def init(self, raw_data):
        self.raw_data = raw_data
        self.source_port = int.from_bytes(raw_data[0:2], byteorder='big')
        self.destination_port = int.from_bytes(raw_data[2:4], byteorder='big')
        self.length = int.from_bytes(raw_data[4:6], byteorder='big')
        self.checksum = int.from_bytes(raw_data[6:8], byteorder='big')

class MainWindow(QMainWindow):
    def init(self):
        super().init()
        self.setWindowTitle('Packet Sniffer')
        self.setGeometry(100, 100, 800, 600)
        self.packet_table = QTableView(self)
        self.packet_table.setGeometry(0, 0, 600, 600)
        self.packet_table.setEditTriggers(QTableView.NoEditTriggers)
        self.packet_details = QTextEdit(self)
        self.packet_details.setGeometry(600, 0, 200, 300)
        self.packet_details.setReadOnly(True)
        self.packet_binary = QTextEdit(self)
        self.packet_binary.setGeometry(600, 300, 200, 300)
        self.packet_binary.setReadOnly(True)
        self.show()
        self.packet_list = []
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)
        self.socket.bind(('127.0.0.1', 0))
        self.socket.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
        self.socket.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)
        self.timer = QTimer(self)
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.read_packets)
        self.timer.start()

    def read_packets(self):
        try:
            raw_data, _ = self.socket.recvfrom(65535)
            ethernet = Ethernet(raw_data)
            if ethernet.type == 0x0800:
                ip = IPv4(ethernet.raw_data[14:])
                if ip.protocol == 6:  # TCP
                    tcp = TCP(ip.raw_data[20:])
                    self.packet_list.append(tcp)
                elif ip.protocol == 17:  # UDP
                    udp = UDPPacket(ip.raw_data[20:])
                    self.packet_list.append(udp)

            self.packet_table.setModel(PacketTableModel(self.packet_list))
        except:
            pass

        selected = self
        index = self.packet_table.currentIndex().row()
        if index >= 0:
            packet = self.packet_list[index]
            self.packet_details.setText(str(packet))
            self.packet_binary.setText(packet.raw_data.hex())

class PacketTableModel(QAbstractTableModel):
    def init(self, packets):
        super().init()
        self.packets = packets

    def rowCount(self, parent):
        return len(self.packets)

    def columnCount(self, parent):
        return len(Packet.fields) + 1

    def headerData(self, section, orientation, role):
        if role != Qt.DisplayRole:
            return
        if orientation == Qt.Horizontal:
            if section == 0:
                return 'Protocol'
            else:
                return Packet.fields[section - 1].name
        else:
            return str(section)

    def data(self, index, role):
        if role != Qt.DisplayRole:
            return
        row = index.row()
        column = index.column()
        packet = self.packets[row]
        if column == 0:
            return packet.__class__.__name__
        else:
            field = Packet.fields[column - 1]
            value = getattr(packet, field.value_name)
            if field.name == 'Flags':
                value = format(value, '02x')
            elif field.name in ('Source', 'Destination'):
                value = socket.inet_ntoa(value.to_bytes(4, byteorder='big'))
            return str(value)
        app = QApplication(sys.argv)
        window = MainWindow()
        sys.exit(app.exec_())


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
