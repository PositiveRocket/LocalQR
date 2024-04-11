import os
import threading
import tkinter as tk
from tkinter import filedialog
import http.server
import socketserver
import socket
import qrcode
from urllib.parse import quote

def importFile(entry, button):
    global httpd
    global full_file_path  # Add this line
    file_path = filedialog.askopenfilename()
    if file_path:  # A file was selected
        full_file_path = file_path  # Save the full file path
        entry.configure(state='normal')  # Enable editing
        entry.delete(0, tk.END)  # Clear the entry field
        entry.insert(0, os.path.basename(file_path))  # Insert the file name into the entry field
        entry.configure(state='readonly')  # Disable editing
        if httpd:
            httpd.shutdown()  # Stop the existing server
        httpd = start_server(os.path.dirname(file_path))  # Start a new server
        button.configure(state='normal')  # Enable the button

def quit_app():
    # Check if the server is running
    if httpd:
        print("Shutting down server")
        httpd.shutdown()  # Stop the server
    root.destroy()  # Destroy the Tkinter window

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP


def start_server(directory):
    global encoded_file_path
    global httpd
    handler = http.server.SimpleHTTPRequestHandler
    os.chdir(directory)
    httpd = socketserver.TCPServer(("", 8000), handler)
    server_thread = threading.Thread(target=httpd.serve_forever)
    server_thread.start()

    encoded_file_path = quote(os.path.basename(file_path_entry.get()))  # Percent-encode the file path

    local_ip = get_local_ip()
    print(f"Serving at port 8000\nURL http://{local_ip}:8000/{encoded_file_path}")


    return httpd

def generateQR(file_path):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    local_ip = get_local_ip()
    qr.add_data(f"http://{local_ip}:8000/{encoded_file_path}")
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    script_dir = os.path.dirname(__file__)
    qr_path = os.path.join(script_dir, "qr.png")
    img.save(qr_path)
    renderQR(qr_path)

def renderQR(fileName):
    img = tk.PhotoImage(file=fileName)
    image_label.configure(image=img)
    image_label.image = img
    new_width = (root.winfo_width() + img.width()) 
    new_height = (root.winfo_height() + img.height() - 400)
    root.geometry(f"{new_width}x{new_height}")  # Resize the window to fit the QR code

root = tk.Tk()
root.title("Local QR Code Generator")
root.geometry("300x400")  # Width x Height
root.resizable(False, False)  # Disable resizing

root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)

file_path_entry = tk.Entry(root, width=50)
file_path_entry.configure(state='readonly')  # Set initial state to read-only
file_path_entry.grid(row=0, column=0, sticky='nsew')  # Place the entry in the grid

browse_button = tk.Button(root, text="Browse", command=lambda: importFile(file_path_entry, generateQR_button))
browse_button.grid(row=1, column=0 , sticky='nesw')  # Place the button in the grid

generateQR_button = tk.Button(root, text="Generate QR Code", state='disabled', command=lambda: generateQR(file_path_entry.get()))
generateQR_button.grid(row=2, column=0, sticky='nsew')  # Place the button in the grid


root.protocol("WM_DELETE_WINDOW", quit_app)

image_label = tk.Label(root)
image_label.grid(row=0, column=1, rowspan=3)  # Place the label in the grid

httpd = None  # Start the server in the current directory

root.mainloop()