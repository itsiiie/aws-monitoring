from services.cost_usage import fetch_cost_by_service
from services.usage_tracker import (
    get_s3_storage_usage,
    get_ec2_running_hours,
    get_rds_running_hours,
    get_lambda_usage
)
from utils.formatter import print_cost_report
from utils.report_generator import save_reports
from utils.alert import load_thresholds, check_thresholds # Updated import
from utils.discord_notify import send_discord_alert
from dotenv import load_dotenv
import os

def main():
    load_dotenv()
    print("🚀 AWS Free Tier Usage Monitor\n")

    region = os.getenv("AWS_REGION", "us-east-1")
    # The ALERT_THRESHOLD environment variable is now less critical as detailed thresholds are in config.yaml
    # We keep it for backward compatibility or if a user prefers a single global cost threshold
    global_cost_threshold_env = float(os.getenv("ALERT_THRESHOLD", "0.01"))

    cost_data, total_cost = fetch_cost_by_service(region)
    print_cost_report(cost_data, total_cost)

    ec2_hours = get_ec2_running_hours(region)
    print(f"\n🖥️  EC2 Running Hours: {ec2_hours} / 750 hours (Free Tier)")

    s3_gb = get_s3_storage_usage()
    print(f"📦  S3 Storage Used: {s3_gb} GB / 5 GB (Free Tier)")

    lambda_usage = get_lambda_usage(region)
    # Note: The get_lambda_usage function currently returns 0.0 as a placeholder.
    # For actual monitoring, this function needs to be fully implemented to query CloudWatch metrics.
    print(f"\n🧠 Lambda Compute Time: {lambda_usage} GB-seconds / 400,000 GB-sec (Free Tier)")

    rds_hours = get_rds_running_hours(region)
    print(f"🗃️  RDS usage: {rds_hours} hours")
    if rds_hours > 750:
        print("⚠️  Warning: RDS usage exceeds Free Tier limit (750 hours)")

    # Prepare usage data for report and alert checks
    usage_data = {
        "EC2": f"{ec2_hours} / 750 hrs",
        "S3": f"{s3_gb:.2f} / 5 GB",
        "Lambda": f"{lambda_usage} / 400,000 GB-sec",
        "RDS": f"{rds_hours} / 750 hrs"
    }

    # Load thresholds from config.yaml
    thresholds = load_thresholds()

    # Add the global cost threshold from environment variable to the thresholds if it's not already in config.yaml
    if "cost" not in thresholds:
        thresholds["cost"] = global_cost_threshold_env

    # Run alert checks using the consolidated function
    alerts = check_thresholds(usage_data, total_cost, thresholds)

    print("\n🚨 Alert Summary:")
    if alerts:
        for a in alerts:
            print(a)
        alert_message = "\n".join(alerts)
        send_discord_alert(
            f"⚠️ AWS Free Tier Alert(s) Triggered:\n\n{alert_message}\n\nCurrent Cost: ${total_cost:.2f}"
        )
    else:
        print("✅ All usage within safe limits.")
        send_discord_alert(f"✅ AWS Free Tier usage is within safe limits. Current Cost: ${total_cost:.2f}")


    # Save reports after alerts are generated
    save_reports(cost_data, total_cost, usage_data, alerts)

if __name__ == "__main__":
    main()
