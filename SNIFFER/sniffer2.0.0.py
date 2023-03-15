import tkinter as tk
from tkinter import ttk
from scapy.all import *

class PacketSniffer:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Packet Sniffer")
        self.root.geometry("600x400")
        self.create_widgets()

    def create_widgets(self):
        self.tree = ttk.Treeview(self.root, columns=("src", "dst", "proto", "len"))
        self.tree.heading("#0", text="No.")
        self.tree.heading("src", text="Source IP")
        self.tree.heading("dst", text="Destination IP")
        self.tree.heading("proto", text="Protocol")
        self.tree.heading("len", text="Length")
        self.tree.pack(expand=True, fill=tk.BOTH)

        self.start_btn = tk.Button(self.root, text="Start", command=self.start_sniffing)
        self.start_btn.pack(side=tk.LEFT, padx=10, pady=10)

        self.stop_btn = tk.Button(self.root, text="Stop", command=self.stop_sniffing)
        self.stop_btn.pack(side=tk.LEFT, padx=10, pady=10)
        self.stop_btn.config(state=tk.DISABLED)

    def start_sniffing(self):
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.sniff_thread = threading.Thread(target=self.sniff_packets)
        self.sniff_thread.start()

    def stop_sniffing(self):
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.sniff_thread.join()

    def sniff_packets(self):
        self.tree.delete(*self.tree.get_children())
        sniff(prn=self.process_packet, filter="tcp or udp", store=False)

    def process_packet(self, packet):
        src = packet[IP].src
        dst = packet[IP].dst
        proto = packet[IP].proto
        length = len(packet)
        self.tree.insert("", tk.END, text="", values=(src, dst, proto, length))

if __name__ == "__main__":
    app = PacketSniffer()
    app.root.mainloop()