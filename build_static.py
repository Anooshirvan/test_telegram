import os
import shutil
from flask import Flask, render_template
from app import app

def build_static():
    # Create static directory if it doesn't exist
    if not os.path.exists('static'):
        os.makedirs('static')
    
    # Create a test client
    client = app.test_client()
    
    # Get the home page
    response = client.get('/')
    with open('static/index.html', 'wb') as f:
        f.write(response.data)
    
    # Get the dashboard page
    response = client.get('/dashboard')
    with open('static/dashboard.html', 'wb') as f:
        f.write(response.data)
    
    # Copy static assets
    if os.path.exists('static'):
        shutil.rmtree('static')
    shutil.copytree('templates', 'static/templates')
    
    # Create a simple API endpoint for QR code tracking
    with open('static/qr.js', 'w') as f:
        f.write('''
        async function trackAndRedirect(qrId) {
            try {
                await fetch(`/api/track/${qrId}`);
                window.location.href = 'https://t.me/test_anoosh';
            } catch (error) {
                console.error('Error:', error);
                window.location.href = 'https://t.me/test_anoosh';
            }
        }
        ''')
    
    print("Static files built successfully!")

if __name__ == '__main__':
    build_static() 