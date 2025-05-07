from flask import Flask, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)

@app.route('/api/track/<qr_id>', methods=['GET'])
def track_scan(qr_id):
    try:
        conn = sqlite3.connect('qr_codes.db')
        c = conn.cursor()
        c.execute('INSERT INTO scans (qr_id, timestamp, ip, user_agent) VALUES (?, ?, ?, ?)',
                  (qr_id, datetime.utcnow(), 'tracked', 'tracked'))
        conn.commit()
        conn.close()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) 