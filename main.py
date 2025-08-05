from services.cost_usage import fetch_cost_by_service
from services.alerts import check_threshold
from utils.formatter import print_cost_report
from dotenv import load_dotenv
import os

def main():
    load_dotenv()
    print("🚀 AWS Free Tier Usage Monitor\n")

    region = os.getenv("AWS_REGION", "us-east-1")
    threshold = float(os.getenv("ALERT_THRESHOLD", "0.01"))

    cost_data, total = fetch_cost_by_service(region)
    print_cost_report(cost_data, total)

    # 🛎️ Alert check
    print("\n🛎️ Alert Status:")
    print(check_threshold(total, threshold))

if __name__ == "__main__":
    main()
