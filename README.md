# Telegram Channel QR Code Tracker

This Flask application tracks QR code scans for your Telegram channel and redirects users to your channel.

## Setup

1. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the application:
   ```
   python app.py
   ```

The application will run on `http://localhost:5000`

## Usage

1. Generate a QR code for your application URL (e.g., `http://your-domain.com` or `http://localhost:5000` if testing locally)
2. When someone scans the QR code, it will:
   - Log the scan with timestamp, IP address, and user agent
   - Automatically redirect to your Telegram channel

## Logs

Scans are logged in `scan_log.txt` with the following format:
```
Timestamp - IP - User Agent
```

## Customization

To change the Telegram channel link, modify the `TELEGRAM_LINK` variable in `app.py`. 

TELEGRAM_BOT_TOKEN=7756366586:AAESp8XYT_M8Yx8lDrtjOgffHky9A6L3SqU
TELEGRAM_CHANNEL_USERNAME=test_anoosh 