from flask import Flask, redirect, request, render_template, jsonify, url_for
from datetime import datetime, timedelta
import os
import pandas as pd
import plotly.express as px
import plotly.utils
import json
import sqlite3
from telegram_bot import TelegramAnalytics
from flask_talisman import Talisman

app = Flask(__name__)
# Enable HTTPS
Talisman(app, content_security_policy=None)

TELEGRAM_LINK = "https://t.me/test_anoosh"
TELEGRAM_ANALYTICS = TelegramAnalytics()

# Database setup
def init_db():
    conn = sqlite3.connect('qr_codes.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS qr_codes
                 (id TEXT PRIMARY KEY, name TEXT, created_at TIMESTAMP)''')
    c.execute('''CREATE TABLE IF NOT EXISTS scans
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  qr_id TEXT,
                  timestamp TIMESTAMP,
                  ip TEXT,
                  user_agent TEXT,
                  FOREIGN KEY (qr_id) REFERENCES qr_codes (id))''')
    conn.commit()
    conn.close()

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/qr/<qr_id>")
def track_and_redirect(qr_id):
    # Log scan
    ip = request.remote_addr
    timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    user_agent = request.headers.get('User-Agent', 'Unknown')
    
    conn = sqlite3.connect('qr_codes.db')
    c = conn.cursor()
    c.execute('INSERT INTO scans (qr_id, timestamp, ip, user_agent) VALUES (?, ?, ?, ?)',
              (qr_id, timestamp, ip, user_agent))
    conn.commit()
    conn.close()

    # Redirect to Telegram
    return redirect(TELEGRAM_LINK, code=302)

@app.route("/dashboard")
def dashboard():
    return render_template('dashboard.html')

@app.route("/api/scan-stats")
def scan_stats():
    conn = sqlite3.connect('qr_codes.db')
    
    # Get all QR codes with their scan counts
    qr_stats = pd.read_sql_query('''
        SELECT q.id, q.name, COUNT(s.id) as scan_count
        FROM qr_codes q
        LEFT JOIN scans s ON q.id = s.qr_id
        GROUP BY q.id, q.name
    ''', conn)
    
    # Get daily scans for each QR code
    daily_scans = pd.read_sql_query('''
        SELECT qr_id, date(timestamp) as date, COUNT(*) as count
        FROM scans
        GROUP BY qr_id, date(timestamp)
        ORDER BY date
    ''', conn)
    
    # Get device distribution
    device_stats = pd.read_sql_query('''
        SELECT 
            CASE 
                WHEN user_agent LIKE '%Mobile%' THEN 'Mobile'
                ELSE 'Desktop'
            END as device,
            COUNT(*) as count
        FROM scans
        GROUP BY device
    ''', conn)
    
    conn.close()
    
    return jsonify({
        'qr_stats': qr_stats.to_dict('records'),
        'daily_scans': daily_scans.to_dict('records'),
        'device_stats': device_stats.to_dict('records'),
        'total_scans': int(qr_stats['scan_count'].sum())
    })

@app.route("/api/telegram-stats")
def telegram_stats():
    stats = TELEGRAM_ANALYTICS.get_stats()
    if stats:
        return jsonify(stats)
    return jsonify({'error': 'Could not fetch Telegram stats'}), 500

@app.route("/api/qr-codes", methods=['GET', 'POST'])
def manage_qr_codes():
    if request.method == 'POST':
        data = request.json
        qr_id = data.get('id')
        name = data.get('name')
        
        conn = sqlite3.connect('qr_codes.db')
        c = conn.cursor()
        c.execute('INSERT INTO qr_codes (id, name, created_at) VALUES (?, ?, ?)',
                  (qr_id, name, datetime.utcnow()))
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'qr_url': url_for('track_and_redirect', qr_id=qr_id, _external=True)})
    
    conn = sqlite3.connect('qr_codes.db')
    qr_codes = pd.read_sql_query('SELECT * FROM qr_codes', conn)
    conn.close()
    
    return jsonify(qr_codes.to_dict('records'))

if __name__ == "__main__":
    init_db()
    # For local development
    app.run(host="0.0.0.0", port=5000) 