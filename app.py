import os
import socket
import io
import base64
from flask import Flask, request, send_from_directory, redirect, url_for, render_template_string, jsonify

#Import libraries for QR Code generation 
import qrcode
from PIL import Image

# --- Basic Flask App Setup ---
app = Flask(__name__)
UPLOAD_FOLDER = 'shareease_uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 * 1024  # 16 GB max upload size

# Create the upload folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# --- Helper Functions ---
def get_ip_address():
    """A helper function to get the local IP address of the machine."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

# Helper function to generate QR code 
def generate_qr_code(data):
    """Generates a QR code and returns it as a base64 encoded string."""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Save QR code to a bytes buffer
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    byte_im = buf.getvalue()
    
    # Encode to base64
    return base64.b64encode(byte_im).decode('utf-8')

# --- HTML Template ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ShareEase - Local File Sharing</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --primary-color: #4A90E2;
            --secondary-color: #50E3C2;
            --danger-color: #e74c3c;
            --background-color: #1a1a2e;
            --card-background: rgba(255, 255, 255, 0.05);
            --text-color: #e0e0e0;
            --text-muted-color: #a0a0c0;
            --border-color: rgba(255, 255, 255, 0.1);
        }
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Poppins', sans-serif;
            background-color: var(--background-color);
            color: var(--text-color);
            background-image: linear-gradient(135deg, #162238 0%, #1a1a2e 80%);
            display: flex;
            justify-content: center;
            align-items: flex-start;
            min-height: 100vh;
            padding: 2rem 1rem;
        }
        .container {
            width: 100%;
            max-width: 800px;
            background: var(--card-background);
            border: 1px solid var(--border-color);
            border-radius: 20px;
            padding: 2rem 2.5rem;
            backdrop-filter: blur(10px);
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        }
        @media (max-width: 768px) { .container { padding: 1.5rem; } body { padding: 1rem 0.5rem; } }
        .header { text-align: center; margin-bottom: 2rem; }
        .logo { font-size: 3rem; font-weight: 700; background: linear-gradient(45deg, var(--primary-color), var(--secondary-color)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 0.5rem; }
        .tagline { font-size: 1rem; color: var(--text-muted-color); }
        .section { margin-bottom: 2.5rem; }
        .section-title { font-size: 1.5rem; font-weight: 600; margin-bottom: 1rem; padding-bottom: 0.5rem; border-bottom: 2px solid var(--primary-color); display: inline-block; }
        .instructions-grid { display: grid; grid-template-columns: 1fr; gap: 2rem; }
        @media (min-width: 768px) { .instructions-grid { grid-template-columns: 1fr auto; align-items: center; } }
        .instructions ol { list-style-position: inside; padding-left: 0; color: var(--text-muted-color); }
        .instructions li { margin-bottom: 0.75rem; line-height: 1.6; }
        .instructions code { background-color: rgba(0, 0, 0, 0.3); color: var(--secondary-color); padding: 0.2rem 0.5rem; border-radius: 5px; font-weight: 600; font-size: 1.1rem; }
        /* --- NEW: QR Code Styles --- */
        .qr-code-container { text-align: center; }
        .qr-code-box { background: white; padding: 15px; border-radius: 10px; display: inline-block; line-height: 0; }
        .qr-code-box img { width: 150px; height: 150px; }
        .qr-code-container p { color: var(--text-muted-color); margin-top: 1rem; }
        .upload-form { text-align: center; }
        .file-input-wrapper { position: relative; display: inline-block; width: 100%; max-width: 400px; margin-bottom: 1rem; }
        .file-input { position: absolute; left: 0; top: 0; opacity: 0; width: 100%; height: 100%; cursor: pointer; }
        .file-input-label { display: flex; align-items: center; justify-content: center; width: 100%; padding: 1rem; background: linear-gradient(45deg, var(--primary-color), #3a7bbd); color: white; border-radius: 10px; font-weight: 600; cursor: pointer; transition: all 0.3s ease; }
        .file-input-label:hover { transform: translateY(-2px); box-shadow: 0 4px 15px rgba(74, 144, 226, 0.4); }
        .file-name { margin-top: -0.5rem; margin-bottom: 1rem; color: var(--text-muted-color); height: 1.2em; font-style: italic; }
        .submit-btn { padding: 0.8rem 2.5rem; background: var(--secondary-color); color: var(--background-color); border: none; border-radius: 10px; font-weight: 700; font-size: 1rem; cursor: pointer; transition: all 0.3s ease; }
        .submit-btn:disabled { background: #888; cursor: not-allowed; }
        .submit-btn:hover:not(:disabled) { background: #45d1b4; transform: scale(1.05); }
        /* --- NEW: Progress Bar Styles --- */
        .progress-container { width: 100%; max-width: 400px; margin: 0 auto; background-color: var(--border-color); border-radius: 5px; height: 10px; margin-bottom: 1rem; overflow: hidden; display: none; }
        .progress-bar { width: 0%; height: 100%; background: linear-gradient(90deg, var(--primary-color), var(--secondary-color)); transition: width 0.2s ease-out; }
        
        .file-list-container { list-style: none; }
        .file-item { display: flex; justify-content: space-between; align-items: center; background: var(--card-background); padding: 1rem 1.5rem; border-radius: 10px; margin-bottom: 1rem; border: 1px solid var(--border-color); transition: all 0.2s ease; flex-wrap: wrap; }
        .file-item:hover { border-color: var(--primary-color); transform: translateX(5px); }
        .file-details { display: flex; align-items: center; flex-grow: 1; word-break: break-all; margin-right: 1rem; }
        .file-actions { display: flex; align-items: center; }
        .download-btn, .delete-btn { display: flex; align-items: center; padding: 0.5rem 1rem; color: white; text-decoration: none; border-radius: 8px; font-weight: 600; white-space: nowrap; transition: background-color 0.2s ease; border: none; font-family: 'Poppins', sans-serif; font-size: 0.9rem; cursor: pointer; }
        .download-btn { background-color: var(--primary-color); margin-right: 0.5rem; }
        .download-btn:hover { background-color: #3a7bbd; }
        /* --- NEW: Delete Button Styles --- */
        .delete-btn { background-color: var(--danger-color); }
        .delete-btn:hover { background-color: #c0392b; }
        .btn-icon { width: 1.2em; height: 1.2em; margin-right: 0.5rem; }
        .no-files { text-align: center; color: var(--text-muted-color); padding: 2rem; border: 2px dashed var(--border-color); border-radius: 10px; }
    </style>
</head>
<body>
    <div class="container">
        <header class="header">
            <h1 class="logo">ShareEase</h1>
            <p class="tagline">Effortless file sharing across your local network.</p>
        </header>

        <section class="section">
            <h2 class="section-title">How to Connect</h2>
            <div class="instructions-grid">
                <div class="instructions">
                    <ol>
                        <li>Ensure all devices are on the <strong>same Wi-Fi network</strong>.</li>
                        <li>On your other device, scan the QR code to the right.</li>
                        <li>Alternatively, type this address in the browser: <br><code>http://{{ ip }}:5000</code></li>
                        <li>Start sharing! No internet data is used.</li>
                    </ol>
                </div>
                <!-- --- NEW: QR Code Display --- -->
                <div class="qr-code-container">
                    <div class="qr-code-box">
                        <img src="data:image/png;base64,{{ qr_code_data }}" alt="QR Code">
                    </div>
                    <p>Scan Me!</p>
                </div>
            </div>
        </section>

        <section class="section">
            <h2 class="section-title">Upload a File</h2>
            <!-- --- MODIFIED: Form now uses JS for submission --- -->
            <form class="upload-form" id="upload-form" enctype="multipart/form-data">
                <div class="file-input-wrapper">
                    <label for="file" class="file-input-label">
                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="btn-icon"><path d="M18 10h-1.26A8 8 0 1 0 9 20h9a5 5 0 0 0 0-10z"></path><polyline points="16 16 12 12 8 16"></polyline><line x1="12" y1="12" x2="12" y2="21"></line></svg>
                        Choose File to Share
                    </label>
                    <input type="file" name="file" id="file" class="file-input" onchange="updateFileName(this)">
                </div>
                <div class="file-name" id="file-name-display">No file selected</div>
                <!-- --- NEW: Progress Bar --- -->
                <div class="progress-container" id="progress-container">
                    <div class="progress-bar" id="progress-bar"></div>
                </div>
                <button type="submit" class="submit-btn" id="submit-btn" disabled>Upload</button>
            </form>
        </section>

        <section class="section">
            <h2 class="section-title">Available Files</h2>
            <ul class="file-list-container">
                {% if files %}
                    {% for file in files %}
                    <li class="file-item">
                        <div class="file-details">
                            <span class="file-name-text">{{ file }}</span>
                        </div>
                        <div class="file-actions">
                            <a href="/download/{{ file }}" class="download-btn">
                                <svg class="btn-icon" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="7 10 12 15 17 10"></polyline><line x1="12" y1="15" x2="12" y2="3"></line></svg>
                                Download
                            </a>
                            <!-- --- NEW: Delete Button and Form --- -->
                            <form action="/delete/{{ file }}" method="post" onsubmit="return confirm('Are you sure you want to delete this file?');">
                                <button type="submit" class="delete-btn">
                                    <svg class="btn-icon" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path><line x1="10" y1="11" x2="10" y2="17"></line><line x1="14" y1="11" x2="14" y2="17"></line></svg>
                                    Delete
                                </button>
                            </form>
                        </div>
                    </li>
                    {% endfor %}
                {% else %}
                    <li class="no-files">No files have been shared yet.</li>
                {% endif %}
            </ul>
        </section>
    </div>
    <script>
        const uploadForm = document.getElementById('upload-form');
        const fileInput = document.getElementById('file');
        const submitBtn = document.getElementById('submit-btn');
        const fileNameDisplay = document.getElementById('file-name-display');
        const progressContainer = document.getElementById('progress-container');
        const progressBar = document.getElementById('progress-bar');

        function updateFileName(input) {
            if (input.files && input.files.length > 0) {
                fileNameDisplay.textContent = input.files[0].name;
                submitBtn.disabled = false;
            } else {
                fileNameDisplay.textContent = 'No file selected';
                submitBtn.disabled = true;
            }
        }

        uploadForm.addEventListener('submit', function(e) {
            e.preventDefault();
            if (fileInput.files.length === 0) {
                alert('Please select a file to upload.');
                return;
            }

            const formData = new FormData();
            formData.append('file', fileInput.files[0]);

            const xhr = new XMLHttpRequest();

            xhr.upload.addEventListener('progress', function(e) {
                if (e.lengthComputable) {
                    const percentComplete = (e.loaded / e.total) * 100;
                    progressContainer.style.display = 'block';
                    progressBar.style.width = percentComplete.toFixed(2) + '%';
                }
            });

            xhr.addEventListener('load', function() {
                if (xhr.status === 200) {
                    // Success, reload the page to see the new file
                    location.reload();
                } else {
                    // Error
                    alert('Upload failed. Status: ' + xhr.status);
                    resetUploadUI();
                }
            });

            xhr.addEventListener('error', function() {
                alert('An error occurred during the upload.');
                resetUploadUI();
            });
            
            xhr.addEventListener('abort', function() {
                alert('Upload aborted.');
                resetUploadUI();
            });

            submitBtn.disabled = true;
            submitBtn.textContent = 'Uploading...';

            xhr.open('POST', '/upload', true);
            xhr.send(formData);
        });
        
        function resetUploadUI() {
            progressContainer.style.display = 'none';
            progressBar.style.width = '0%';
            submitBtn.disabled = false;
            submitBtn.textContent = 'Upload';
            fileInput.value = ''; // Reset file input
            updateFileName(fileInput);
        }

    </script>
</body>
</html>
"""

# --- Flask Routes ---

@app.route('/')
def index():
    """Displays the main page with file list and QR code."""
    try:
        files = sorted(os.listdir(UPLOAD_FOLDER), key=lambda f: os.path.getmtime(os.path.join(UPLOAD_FOLDER, f)), reverse=True)
    except OSError:
        files = []
        
    local_ip = get_ip_address()
    access_url = f"http://{local_ip}:5000"
    qr_code_data = generate_qr_code(access_url)
    
    return render_template_string(HTML_TEMPLATE, files=files, ip=local_ip, qr_code_data=qr_code_data)

@app.route('/api/status')
def api_status():
    """Provides status information for the browser extension."""
    local_ip = get_ip_address()
    access_url = f"http://{local_ip}:5000"
    qr_code_data = generate_qr_code(access_url)
    
    return jsonify({
        'server_online': True,
        'ip_address': local_ip,
        'access_url': access_url,
        'qr_code_base64': qr_code_data
    })

# Dedicated route for asynchronous uploads
@app.route('/upload', methods=['POST'])
def upload_file_async():
    """Handles the asynchronous file upload."""
    if 'file' not in request.files:
        return jsonify(success=False, error="No file part"), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify(success=False, error="No selected file"), 400
    if file:
        filename = file.filename # In a real app, you'd secure this filename.
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return jsonify(success=True, filename=filename)
    return jsonify(success=False, error="File upload failed"), 500

@app.route('/download/<path:filename>')
def download_file(filename):
    """Serves files for download."""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

# Route for deleting files
@app.route('/delete/<path:filename>', methods=['POST'])
def delete_file(filename):
    """Handles file deletion."""
    try:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if os.path.exists(file_path):
            os.remove(file_path)
        else:
            print(f"File {filename} does not exist.")
            pass
    except Exception as e:
        # Log the error, maybe show an error page
        print(f"Error deleting file {filename}: {e}")
    return redirect(url_for('index'))


if __name__ == '__main__':
    print("--- ShareEase is starting ---")
    print("1. Make sure your devices are on the SAME Wi-Fi network.")
    local_ip = get_ip_address()
    print(f"2. On this computer, open a browser to http://{local_ip}:5000")
    print("3. On your other devices, SCAN the QR code shown on the page.")
    print("4. Press CTRL+C here to stop the server.")
    print("-----------------------------")
    app.run(host='0.0.0.0', port=5000, debug=False)