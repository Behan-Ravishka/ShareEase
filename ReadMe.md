# ShareEase 📁

**Effortless file sharing across your local network**

ShareEase is a lightweight, web-based file sharing application that allows you to easily share files between devices on the same local network. No internet connection required, no data usage, just simple drag-and-drop file sharing with a beautiful, modern interface.

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
- 🔒 **Secure** - Files stay on your local network, never uploaded to the internet

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- All devices must be connected to the same Wi-Fi network

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/shareease.git
   cd shareease
   ```

2. **Install required dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python shareease.py
   ```

4. **Access the application**
   - Open your browser and go to the address shown in the terminal
   - Or scan the QR code displayed on the main page from other devices

## 📦 Dependencies

Create a `requirements.txt` file with the following dependencies:

```
Flask==2.3.3
qrcode==7.4.2
Pillow==10.0.1
```

## 🖥️ Usage

### Starting the Server

```bash
python shareease.py
```

The application will start and display:
- Local IP address and port (usually `http://192.168.x.x:5000`)
- Instructions for connecting other devices
- QR code for easy mobile access

### Connecting Devices

1. **Same Network**: Ensure all devices are connected to the same Wi-Fi network
2. **Web Browser**: Open a web browser on any device
3. **Access Methods**:
   - **QR Code**: Scan the QR code displayed on the main page
   - **Manual**: Type the IP address shown in the terminal (e.g., `http://192.168.1.100:5000`)

### Sharing Files

1. **Upload**: Click "Choose File to Share" or drag and drop files
2. **Progress**: Watch real-time upload progress
3. **Access**: Files appear in the "Available Files" section
4. **Download**: Other devices can download files with one click
5. **Manage**: Delete files when no longer needed

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

**Can't connect from other devices?**
- Ensure all devices are on the same Wi-Fi network
- Check if firewall is blocking the connection
- Verify the IP address is correct

**Upload fails?**
- Check available disk space
- Verify file size is under the limit (16GB default)
- Ensure the upload folder has write permissions

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

---

**Made with ❤️ for easy file sharing**

*ShareEase - Because sharing files shouldn't be complicated!*