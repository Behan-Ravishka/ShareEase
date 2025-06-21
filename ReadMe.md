# ShareEase 📁

**Effortless file sharing across your local network**

ShareEase is a lightweight, web-based file sharing application that allows you to easily share files between devices on the same local network. No internet connection required, no data usage, just simple file sharing with a beautiful, modern interface, now with a companion browser extension for one-click access.

![ShareEase Interface](https://img.shields.io/badge/Interface-Modern%20Web%20UI-blue)
![Python](https://img.shields.io/badge/Python-3.7%2B-green)
![Flask](https://img.shields.io/badge/Framework-Flask-red)
![License](https://img.shields.io/badge/License-MIT-yellow)

## ✨ Features

- 🌐 **Local Network Sharing** - Share files without internet connection
- 📱 **QR Code Access** - Scan QR code to instantly connect from mobile devices
- 📤 **Easy Upload** - Drag and drop or click to upload files (up to 16GB)
- 📥 **Simple Download** - One-click download for all shared files
- 🗑️ **File Management** - Delete files directly from the web interface
- 📊 **Upload Progress** - Real-time progress tracking for file uploads
- 🎨 **Modern UI** - Beautiful, responsive design that works on all devices
- 🧩 **Browser Extension Companion** - Instantly access your server, view the QR code, and open the share page directly from your browser's toolbar
- 🔒 **Secure** - Files stay on your local network, never uploaded to the internet

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- All devices must be connected to the same Wi-Fi network

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/ShareEase.git
   cd ShareEase
   ```

2. **Install required dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Access the application**
   - The server will start. Keep this terminal window open.
   - On your computer, open a browser and go to the address shown in the terminal (e.g., http://192.168.1.5:5000 or http://localhost:5000).
   - From other devices, scan the QR code displayed on the page or use the browser extension.

## 📦 Dependencies

```
Flask==2.3.3
qrcode==7.4.2
Pillow==10.0.1
```

## 🖥️ Usage

### Starting the Server

```bash
python app.py
```
## 🧩 ShareEase Companion Extension

For even faster access, ShareEase comes with a companion browser extension.

![image](https://github.com/user-attachments/assets/ec09c32a-aa19-4eed-ac96-d2766a5bd4df)
![Screenshot_20-6-2025_3647_192 168 79 211](https://github.com/user-attachments/assets/52c599be-01d1-49ae-bc33-5cc99ed20d71)

### Extension Features:
-   **Server Status Check**: Instantly see if your ShareEase server is online or offline.
-   **One-Click Access**: Opens your ShareEase page in a new tab.
-   **Quick QR Code**: Displays the QR code in the popup, so you don't have to open the main page to connect a new device.

### How to Install the Extension:

1.  Open your browser (Google Chrome, Microsoft Edge, etc.).
2.  Navigate to the extensions management page:
    -   **Chrome**: `chrome://extensions`
    -   **Edge**: `edge://extensions`
3.  Enable **"Developer mode"**. This toggle is usually in the top-right corner.
4.  Click the **"Load unpacked"** button.
5.  A file dialog will open. Navigate to and select the `ShareEase` folder inside the project directory.
6.  The ShareEase Companion icon will appear in your browser's toolbar. Click it to use it!

**Note:** The main `app.py` server must be running for the extension to work.

# 🖥️ Web Interface Usage

### Connecting Devices

1.  **Same Network**: Ensure all devices are on the same Wi-Fi network.
2.  **Web Browser**: Open a web browser on any device.
3.  **Access Methods**:
    -   **Extension (Recommended)**: Click the ShareEase Companion icon in your browser.
    -   **QR Code**: Scan the QR code displayed on the main page or in the extension.
    -   **Manual**: Type the IP address shown in the terminal (e.g., `http://192.168.x.x:5000`).

### Sharing Files

1.  **Upload**: Click "Choose File to Share" or drag and drop a file onto the page.
2.  **Progress**: Watch the real-time upload progress bar.
3.  **Access**: The file will immediately appear in the "Available Files" list for all connected devices.
4.  **Manage**: Download or delete files as needed.

## 📱 Device Support

ShareEase works on any device with a web browser:

- 💻 **Desktop**: Windows, macOS, Linux
- 📱 **Mobile**: iOS Safari, Android Chrome
- 📟 **Tablets**: iPad, Android tablets
- 🖥️ **Smart TVs**: Any TV with a web browser

## 🛠️ Configuration

### Port Configuration
By default, ShareEase runs on port 5000. To change the port:

```python
app.run(host='0.0.0.0', port=8080, debug=False)  # Change 8080 to your preferred port
```

### Upload Size Limit
The default maximum upload size is 16GB. To modify:

```python
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024 * 1024  # 1GB limit
```

### Upload Directory
Files are stored in the `shareease_uploads` folder by default. To change:

```python
UPLOAD_FOLDER = 'my_custom_folder'
```

## 🔧 Advanced Features

### Network Discovery
The application automatically detects your local IP address and generates a QR code for easy access.

### File Management
- **Automatic Sorting**: Files are sorted by upload time (newest first)
- **Safe Deletion**: Confirmation dialog prevents accidental deletion
- **Error Handling**: Graceful handling of network and file system errors

### Security Considerations
- Files are only accessible on your local network
- No external internet connection required
- Files are stored locally on the host machine
- Consider firewall settings if having connection issues

## 🐛 Troubleshooting

### Common Issues

-   **Can't connect from other devices?**
    -   Ensure all devices are on the **same Wi-Fi network**. This is the most common issue.
    -   Check if a firewall is blocking the connection to the port (e.g., 5000).
    -   Verify the IP address is correct.

-   **Upload fails?**
    -   Check if you have enough disk space on the server machine.
    -   Verify the file size is under the configured limit (16GB default).

-   **Browser Extension shows 'Server Offline'?**
    -   Make sure you have started the Python server by running `python app.py` in your terminal. The extension can only connect to a running server.

**QR code not working?**
- Make sure your camera app or QR scanner is working
- Try typing the URL manually instead

### Firewall Configuration

If you're having connection issues, you may need to allow Python through your firewall:

**Windows:**
- Go to Windows Defender Firewall
- Allow Python through the firewall

**macOS:**
- Go to System Preferences > Security & Privacy > Firewall
- Add Python to allowed applications

**Linux:**
- Use `ufw` or `iptables` to allow port 5000

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### Development Setup

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [Flask](https://flask.palletsprojects.com/) - The web framework
- [QRCode](https://pypi.org/project/qrcode/) - For QR code generation
- [Pillow](https://pillow.readthedocs.io/) - For image processing
- Icons from [Lucide](https://lucide.dev/) - Beautiful icon set

## 📞 Support

If you encounter any issues or have questions, please:

1. Check the [Troubleshooting](#-troubleshooting) section
2. Search existing [Issues](https://github.com/yourusername/shareease/issues)
3. Create a new issue if your problem isn't covered

*ShareEase - Because sharing files shouldn't be complicated!*
