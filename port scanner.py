# Port-scanning-
import socket
import ipaddress
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox

# Dictionary mapping ports to common services
port_services = {
    20: "FTP Data Transfer",
    21: "FTP Control",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    443: "HTTPS",
    110: "POP3",
    143: "IMAP",
    3306: "MySQL",
    5432: "PostgreSQL",
    6379: "Redis",
    # Add more as needed
}

# Function to scan a single port
def scan_port(ip, port, output_widget):
    sock = socket.socket(socket.AF_INET6 if ':' in ip else socket.AF_INET, socket.SOCK_STREAM)
    socket.setdefaulttimeout(1)  # Set timeout for connection attempts
    result = sock.connect_ex((ip, port))
    if result == 0:
        service = port_services.get(port, "Unknown Service")
        output_widget.insert(tk.END, f"Port {port} is open on {ip} ({service})\n")
    sock.close()

# Function to scan a range of ports
def scan_ports(ip, start_port, end_port, output_widget):
    for port in range(start_port, end_port + 1):
        thread = threading.Thread(target=scan_port, args=(ip, port, output_widget))
        thread.start()

# Function to handle the scan button click
def start_scan():
    ip_input = ip_entry.get()
    try:
        start_port = int(start_port_entry.get())
        end_port = int(end_port_entry.get())
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid port numbers.")
        return

    # Validate the IP address
    try:
        ipaddress.ip_address(ip_input)
    except ValueError:
        messagebox.showerror("Input Error", "Invalid IP address.")
        return

    output_widget.delete(1.0, tk.END)  # Clear previous results
    output_widget.insert(tk.END, f"Scanning {ip_input} from port {start_port} to {end_port}...\n")
    scan_ports(ip_input, start_port, end_port, output_widget)

# GUI setup
app = tk.Tk()
app.title("Port Scanner")

# IP Address input
tk.Label(app, text="IP Address (IPv4 or IPv6):").grid(row=0, column=0, padx=10, pady=10)
ip_entry = tk.Entry(app)
ip_entry.grid(row=0, column=1, padx=10, pady=10)

# Start and end port input
tk.Label(app, text="Start Port:").grid(row=1, column=0, padx=10, pady=10)
start_port_entry = tk.Entry(app)
start_port_entry.grid(row=1, column=1, padx=10, pady=10)

tk.Label(app, text="End Port:").grid(row=2, column=0, padx=10, pady=10)
end_port_entry = tk.Entry(app)
end_port_entry.grid(row=2, column=1, padx=10, pady=10)

# Scan button
scan_button = tk.Button(app, text="Scan", command=start_scan)
scan_button.grid(row=3, columnspan=2, pady=10)

# Output area
output_widget = scrolledtext.ScrolledText(app, width=60, height=20)
output_widget.grid(row=4, columnspan=2, padx=10, pady=10)

# Start the GUI event loop
app.mainloop()
