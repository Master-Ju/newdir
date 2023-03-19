from PyQt5.QtWidgets import QApplication, QMainWindow, QTableView, QTextEdit


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 创建Packet List栏
        self.packet_list = QTableView(self)
        self.packet_list.setGeometry(10, 10, 300, 200)

        # 创建Packet Details栏
        self.packet_details = QTextEdit(self)
        self.packet_details.setGeometry(320, 10, 300, 200)

        # 创建Packet in Binary栏
        self.packet_binary = QTextEdit(self)
        self.packet_binary.setGeometry(10, 220, 610, 200)

        self.show()
