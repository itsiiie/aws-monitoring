import requests
import os

def send_discord_alert(message: str):
    webhook_url = os.getenv("DISCORD_WEBHOOK_URL")  # Best practice: use env var
    if not webhook_url:
        print("❌ Discord webhook URL not set.")
        return

    data = {
        "content": message
    }

    try:
        response = requests.post(webhook_url, json=data)
        if response.status_code == 204:
            print("✅ Discord alert sent successfully.")
        else:
            print(f"❌ Failed to send Discord alert. Status: {response.status_code}")
    except Exception as e:
        print(f"❌ Discord webhook error: {e}")
