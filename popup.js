document.addEventListener('DOMContentLoaded', () => {
    // Get references to all the HTML elements we need to manipulate
    const statusIndicator = document.getElementById('status-indicator');
    const qrContainer = document.getElementById('qr-container');
    const qrImage = document.getElementById('qr-image');
    const errorMessage = document.getElementById('error-message');
    const openBtn = document.getElementById('open-shareease-btn');

    // Function to update the UI when the server is found
    function setOnlineStatus(data) {
        statusIndicator.textContent = 'Server Online';
        statusIndicator.classList.remove('offline');
        statusIndicator.classList.add('online');

        errorMessage.style.display = 'none';
        
        qrImage.src = `data:image/png;base64,${data.qr_code_base64}`;
        qrContainer.style.display = 'inline-block';

        openBtn.href = data.access_url;
        openBtn.disabled = false;
        openBtn.textContent = `Open at ${data.ip_address}`;
    }

    // Function to update the UI when the server is NOT found
    function setOfflineStatus() {
        statusIndicator.textContent = 'Server Offline';
        statusIndicator.classList.remove('online');
        statusIndicator.classList.add('offline');
        
        qrContainer.style.display = 'none';

        errorMessage.style.display = 'block';
        errorMessage.innerHTML = "Could not connect. <br>Please run the Python script.";

        openBtn.disabled = true;
        openBtn.textContent = 'Open ShareEase';
    }

    // Try to fetch the status from the server. 
    // We check localhost first as it's the most common address.
    fetch('http://localhost:5000/api/status')
        .then(response => {
            if (!response.ok) {
                // If response is not 200 OK, throw an error to be caught below
                throw new Error('Server responded but with an error.');
            }
            return response.json();
        })
        .then(data => {
            // If we successfully get JSON data, the server is online
            if (data.server_online) {
                setOnlineStatus(data);
            } else {
                setOfflineStatus();
            }
        })
        .catch(error => {
            // If the fetch fails completely (e.g., network error), the server is offline
            console.error('Error connecting to ShareEase server:', error);
            setOfflineStatus();
        });

    // Add a click listener to the button to close the popup after clicking
    openBtn.addEventListener('click', () => {
        if (!openBtn.disabled) {
            window.close(); // Closes the popup window
        }
    });
});