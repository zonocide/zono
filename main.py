from flask import Flask, request
import datetime
import requests
import os

app = Flask(__name__)

# Get webhook URL from environment variable (much safer than hardcoding)
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")

@app.route('/')
def log_ip():
    ip = request.remote_addr
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    data = {
        "content": f"**IP Logged**\n**Time:** {now}\n**IP:** `{ip}`"
    }
    
    if WEBHOOK_URL:
        try:
            requests.post(WEBHOOK_URL, json=data, timeout=5)
        except:
            pass  # Silently fail if webhook is down or invalid
    else:
        print("Warning: WEBHOOK_URL environment variable not set")
    
    return "test"  # You can change this to a better message if needed

# Only run with Flask's dev server locally
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"Starting Flask app on port {port}")
    app.run(host="0.0.0.0", port=port)
