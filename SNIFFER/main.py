import tkinter as tk
import tkinter.scrolledtext as scrolledtext
from tkinter import ttk
import threading
import time
import struct
import socket
import textwrap

# 创建嗅探器窗口
root = tk.Tk()
root.title("嗅探器")
root.geometry("800x600")

# 创建包列表
packet_list = ttk.Treeview(height=20, columns=("ID", "源IP", "目的IP", "协议", "长度", "时间"))
packet_list.pack(pady=20)

# 添加列表头
packet_list.heading("#0", text="包编号", anchor=tk.CENTER)
packet_list.column("#0", width=50, anchor=tk.CENTER)
packet_list.heading("ID", text="ID", anchor=tk.CENTER)
packet_list.column("ID", width=50, anchor=tk.CENTER)
packet_list.heading("源IP", text="源IP", anchor=tk.CENTER)
packet_list.column("源IP", width=100, anchor=tk.CENTER)
packet_list.heading("目的IP", text="目的IP", anchor=tk.CENTER)
packet_list.column("目的IP", width=100, anchor=tk.CENTER)
packet_list.heading("协议", text="协议", anchor=tk.CENTER)
packet_list.column("协议", width=80, anchor=tk.CENTER)
packet_list.heading("长度", text="长度", anchor=tk.CENTER)
packet_list.column("长度", width=80, anchor=tk.CENTER)
packet_list.heading("时间", text="时间", anchor=tk.CENTER)
packet_list.column("时间", width=120, anchor=tk.CENTER)

# 创建包细节文本框
packet_detail = scrolledtext.ScrolledText(root, width=100, height=10)
packet_detail.pack(pady=20)

# 创建二进制数据文本框
packet_binary = scrolledtext.ScrolledText(root, width=100, height=10)
packet_binary.pack(pady=20)

# 创建过滤器标签和输入框
filter_label = tk.Label(root, text="过滤器:", font=("Arial", 12))
filter_label.pack(pady=10)
filter_entry = tk.Entry(root, width=50, font=("Arial", 12))
filter_entry.pack(pady=10)

# 创建开始按钮
def start_sniffing():
    # 该函数用于开始嗅探器

    def sniffing():
        # 该函数用于嗅探网络流量

        # 创建套接字并绑定到本地主机的所有网络接口和指定端口
        conn = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(3))

        # 循环嗅探网络流量
        while True:
            try:
                # 接收数据包并解析出协议、源IP地址、目的IP地址和数据
                raw_data, addr = conn.recvfrom(65535)
                dest_mac, src_mac, eth_proto, data = ethernet_frame(raw_data)
                proto, src_addr, dest_addr, data = parse_ip_packet(data)

                # 将解析出的数据添加到包列表中
                packet_list.insert("", tk.END, text=str(len(packet_list.get_children()) + 1),
                                   values=(len(packet_list.get_children()) + 1, src_addr, dest_addr, proto, len(raw_data), time.strftime('%Y-%m-%d %H:%M:%S',
