from flask import Flask, request
import datetime
import requests
import os

app = Flask(__name__)

# Trust the proxy (Railway uses 1 proxy layer)
from werkzeug.middleware.proxy_fix import ProxyFix
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

WEBHOOK_URL = os.environ.get("WEBHOOK_URL")

def get_client_ip():
    """Get real client IP even behind Railway's proxy"""
    # Try X-Forwarded-For first (most reliable on Railway)
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        # Take the first IP in the list (leftmost = real client)
        return forwarded.split(",")[0].strip()
    
    # Fallbacks
    return request.remote_addr or request.headers.get("X-Real-IP") or "Unknown"

@app.route('/')
def log_ip():
    ip = get_client_ip()
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    data = {
        "content": f"**IP Logged**\n**Time:** {now}\n**IP:** `{ip}`"
    }
    
    if WEBHOOK_URL:
        try:
            requests.post(WEBHOOK_URL, json=data, timeout=10)
            print(f"✅ Webhook sent for IP: {ip}")   # This appears in Deploy Logs
        except Exception as e:
            print(f"❌ Webhook failed: {e}")
    else:
        print("⚠️  WEBHOOK_URL environment variable is not set!")
    
    # Better response so you know it worked
    return f"""
    <h2>IP Logger</h2>
    <p>Your IP has been logged.</p>
    <p><strong>Logged IP:</strong> {ip}</p>
    <p>Time: {now}</p>
    """

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"🚀 Starting app on port {port}")
    app.run(host="0.0.0.0", port=port)
