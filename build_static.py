import os
import shutil
from flask import Flask, render_template
from app import app

def build_static():
    # Create static directory if it doesn't exist
    if os.path.exists('static'):
        shutil.rmtree('static')
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
    
    # Create static assets directory
    os.makedirs('static/assets', exist_ok=True)
    
    # Copy any existing static files
    if os.path.exists('static_files'):
        for item in os.listdir('static_files'):
            s = os.path.join('static_files', item)
            d = os.path.join('static', item)
            if os.path.isdir(s):
                shutil.copytree(s, d, dirs_exist_ok=True)
            else:
                shutil.copy2(s, d)
    
    # Create a simple API endpoint for QR code tracking
    with open('static/assets/qr.js', 'w') as f:
        f.write('''
        async function trackAndRedirect(qrId) {
            try {
                // Store the scan in localStorage
                const scans = JSON.parse(localStorage.getItem('qr_scans') || '[]');
                scans.push({
                    qrId: qrId,
                    timestamp: new Date().toISOString(),
                    userAgent: navigator.userAgent
                });
                localStorage.setItem('qr_scans', JSON.stringify(scans));
                
                // Redirect to Telegram
                window.location.href = 'https://t.me/test_anoosh';
            } catch (error) {
                console.error('Error:', error);
                window.location.href = 'https://t.me/test_anoosh';
            }
        }
        ''')
    
    # Create a simple analytics page
    with open('static/analytics.html', 'w') as f:
        f.write('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>QR Code Analytics</title>
            <script src="https://cdn.tailwindcss.com"></script>
            <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
        </head>
        <body class="bg-gray-100">
            <div class="container mx-auto px-4 py-8">
                <h1 class="text-3xl font-bold mb-8">QR Code Analytics</h1>
                <div id="analytics" class="bg-white p-6 rounded-lg shadow-lg">
                    Loading analytics...
                </div>
            </div>
            <script>
                function loadAnalytics() {
                    const scans = JSON.parse(localStorage.getItem('qr_scans') || '[]');
                    const analytics = document.getElementById('analytics');
                    
                    if (scans.length === 0) {
                        analytics.innerHTML = '<p class="text-gray-500">No scans recorded yet.</p>';
                        return;
                    }
                    
                    // Group scans by date
                    const dailyScans = {};
                    scans.forEach(scan => {
                        const date = new Date(scan.timestamp).toLocaleDateString();
                        dailyScans[date] = (dailyScans[date] || 0) + 1;
                    });
                    
                    // Create chart
                    const dates = Object.keys(dailyScans);
                    const counts = dates.map(date => dailyScans[date]);
                    
                    const trace = {
                        x: dates,
                        y: counts,
                        type: 'scatter',
                        mode: 'lines+markers',
                        name: 'Daily Scans'
                    };
                    
                    const layout = {
                        title: 'Daily QR Code Scans',
                        xaxis: { title: 'Date' },
                        yaxis: { title: 'Number of Scans' }
                    };
                    
                    Plotly.newPlot('analytics', [trace], layout);
                    
                    // Show total scans
                    analytics.innerHTML += `
                        <div class="mt-4">
                            <p class="text-lg">Total Scans: <span class="font-bold">${scans.length}</span></p>
                        </div>
                    `;
                }
                
                loadAnalytics();
            </script>
        </body>
        </html>
        ''')
    
    # Create a simple index page if it doesn't exist
    if not os.path.exists('static/index.html'):
        with open('static/index.html', 'w') as f:
            f.write('''
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>QR Code Generator</title>
                <script src="https://cdn.tailwindcss.com"></script>
            </head>
            <body class="bg-gray-100">
                <div class="container mx-auto px-4 py-8">
                    <h1 class="text-3xl font-bold mb-8">QR Code Generator</h1>
                    <div class="bg-white p-6 rounded-lg shadow-lg">
                        <p class="text-gray-600">Welcome to the QR Code Generator!</p>
                    </div>
                </div>
            </body>
            </html>
            ''')
    
    print("Static files built successfully!")
    print("Contents of static directory:")
    for root, dirs, files in os.walk('static'):
        for file in files:
            print(os.path.join(root, file))

if __name__ == '__main__':
    build_static() 