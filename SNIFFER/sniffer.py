import dpkt
import sys
from winpcapy import WinPcapUtils
from winpcapy import WinPcapDevices
from winpcapy import WinPcap
from PyQt5.QtWidgets import (QApplication, QWidget, QMainWindow,
	QComboBox, QPushButton, QHeaderView, QLabel, QTextEdit, QLineEdit,
	QTableWidget, QTableWidgetItem,
	QGridLayout)
from PyQt5.QtCore import QObject, QThread, pyqtSignal
from parse import parsePkt


class Worker(QObject):
	finished = pyqtSignal()
	received = pyqtSignal(bytes)
	def __init__(self, deviceName, pcapFile=None, filterStr=None):
		super().__init__()
		self.deviceName = deviceName
		self.pcapFile = pcapFile
		if filterStr:
			self.filterStr = bytes(filterStr, 'ascii')
		else:
			self.filterStr = None
		self.win_pcap = None
	def run(self):
		if self.pcapFile:
			try:
				pcap = dpkt.pcap.Reader(open(self.pcapFile, 'rb'))
				for t, buf in pcap:
					self.received.emit(buf)
			except Exception:
				pass
			self.finished.emit()
		else:
			with WinPcap(self.deviceName) as capture:
				if self.filterStr:
					if not capture.compile(self.filterStr):
						self.finished.emit()
					capture.setfilter()
				self.win_pcap = capture
				capture.run(callback=self.packet_callback)
	def packet_callback(self, win_pcap, param, header, pkt_data):
		self.received.emit(pkt_data)
	def stop(self):
		if self.win_pcap:
			self.win_pcap.stop()

class dctQTableWidgetItem(QTableWidgetItem):
	def __init__(self, dct, *args, **kargvs):
		super().__init__(*args, **kargvs)
		self.dct = dct

class SnifferUI(QWidget):
	def __init__(self, deviceList = []):
		super().__init__()
		self.deviceList = list(deviceList.items())
		self.on = False
		self.pktCnt = 0
		self.initUI()
	def initDeviceSelector(self):
		deviceSelector = QComboBox()
		for name, desciption in self.deviceList:
			deviceSelector.addItem(desciption)
		self.deviceSelector = deviceSelector
	def initStartButton(self):
		startButton = QPushButton('Start')
		startButton.clicked.connect(self.buttonClicked)
		self.startButton = startButton
	def initDetailedInfo(self):
		detailedInfo = QTextEdit('')
		self.detailedInfo = detailedInfo
	def initPackageTable(self):
		packageTable = QTableWidget()
		packageTable.setRowCount(0)
		packageTable.setColumnCount(5)
		packageTable.setHorizontalHeaderLabels(['id', 'srcAddr', 'dstAddr', 'type', 'info'])
		packageTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
		packageTable.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
		packageTable.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
		packageTable.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
		packageTable.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
		packageTable.verticalHeader().setHidden(True)
		packageTable.setGeometry(0, 150, 1000, 400)
		packageTable.itemClicked.connect(self.printDetailedInfo)
		self.packageTable = packageTable
	'''def initFileInput(self):
		fileInput = QLineEdit('')
		#fileInput.resize(fileInput.sizeHint())
		self.fileInput = fileInput
	'''
	def initFilterInput(self):
		filterInput = QLineEdit('')
		self.filterInput = filterInput
	def initLayout(self):
		layout = QGridLayout()
		layout.addWidget(self.startButton, 0, 0, 1, 1)
		layout.addWidget(self.deviceSelector, 0, 1, 1, 3)
		layout.addWidget(self.filterInput, 0, 4, 1, 2)
		layout.addWidget(self.packageTable, 1, 0, 5, 3)
		layout.addWidget(self.detailedInfo, 1, 3, 5, 3)
		self.layout = layout
		self.setLayout(self.layout)
	
	def initUI(self):
		self.initDeviceSelector()
		self.initStartButton()
		self.initDetailedInfo()
		self.initFilterInput()
		self.initPackageTable()
		self.initLayout()
		self.setGeometry(150, 150, 1000, 500)
		self.setWindowTitle('Sniffer')
		self.show()
		
	def printDetailedInfo(self, tableItem):
		oneLine = 50
		if isinstance(tableItem, dctQTableWidgetItem):
			dct = tableItem.dct
			info = ''
			for k, v in dct.items():
				if not isinstance(k, str):
					k = str(k)
				if not isinstance(v, str):
					v = str(v)
				info += k + ':\n'
				while len(v) >= oneLine:
					info += '\t' + v[:oneLine] + '\n'
					v = v[oneLine:]
				info += '\t' + v + '\n'
			self.detailedInfo.setText(info)
		
	def addPacket(self, layers):
		self.pktCnt += 1
		curRow = self.packageTable.rowCount()
		nLayer = 0
		for pkt in layers:
			if pkt:
				src, dst, type, info, dct = pkt[0], pkt[1], pkt[2], pkt[3], pkt[4]
				rowCnt = self.packageTable.rowCount()
				self.packageTable.insertRow(rowCnt)
				self.packageTable.setItem(rowCnt, 1, dctQTableWidgetItem(dct, src))
				self.packageTable.setItem(rowCnt, 2, dctQTableWidgetItem(dct, dst))
				self.packageTable.setItem(rowCnt, 3, dctQTableWidgetItem(dct, type))
				self.packageTable.setItem(rowCnt, 4, dctQTableWidgetItem(dct, info))
				nLayer += 1
		self.packageTable.setSpan(curRow, 0, nLayer, 1);
		self.packageTable.setItem(curRow, 0, QTableWidgetItem(str(self.pktCnt)))
	
	def receivePacket(self, pkt_data):
		layers = parsePkt(pkt_data)
		self.addPacket(layers)

	def buttonClicked(self):
		if self.on:
			self.on = False
			self.startButton.setText('Start')
			self.deviceSelector.setEnabled(True)
			self.filterInput.setReadOnly(False)
			self.worker.stop()
			self.thread.quit()
			self.thread.wait()
			self.worker.deleteLater()
			self.thread.deleteLater()
		else:
			self.on = True
			self.pktCnt = 0
			self.startButton.setText('Stop')
			self.packageTable.setRowCount(0)
			self.deviceSelector.setEnabled(False)
			self.filterInput.setReadOnly(False)
			self.startSniff()
	
	def startSniff(self):
		print('Start Sniff')
		idx = self.deviceSelector.currentIndex()
		currentDevice = self.deviceList[idx][0]
		print(currentDevice)
		self.thread = QThread()
		self.filterStr = self.filterInput.text()
		if len(self.filterStr) == 0:
			self.filterStr = None
		self.worker = Worker(currentDevice, pcapFile=None, filterStr=self.filterStr)
		self.worker.moveToThread(self.thread)
		self.thread.started.connect(self.worker.run)
		self.worker.received.connect(self.receivePacket)
		self.worker.finished.connect(self.buttonClicked)
		self.thread.start()
		
if __name__ == '__main__':
	app = QApplication([])
	deviceList = WinPcapDevices.list_devices()
	mainWD = SnifferUI(deviceList)
	sys.exit(app.exec_())