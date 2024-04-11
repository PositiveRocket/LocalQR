# LocalQR

LocalQR is a simple Python application that allows you to select a file from your local system and generate a QR code that links to that file. The file is served over HTTP on your local network, so you can access it from any device that can scan the QR code. I made this program with the main use of CIA files for installation on 3DS. 

## Features

- File selection dialog for choosing the file to share
- QR code generation for the selected file
- Local HTTP server for serving the selected file

## Usage

1. Run the script: `python main.py`
2. Click the "Browse" button to select a file to share.
3. Click the "Generate QR Code" button to generate a QR code for the selected file.
4. Scan the QR code with a device to download the file.

## Requirements

- Python 3
- tkinter
- qrcode
- http.server
- socketserver
- socket

## Note

This application is intended for use in a local network environment. The HTTP server it starts is not secure or scalable enough for use in a production environment.