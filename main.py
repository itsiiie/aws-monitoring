from services.cost_usage import fetch_cost_by_service
from services.alerts import check_threshold
from utils.formatter import print_cost_report
from services.usage_tracker import get_s3_storage_usage
from services.usage_tracker import get_ec2_running_hours, get_rds_running_hours
from utils.report_generator import save_reports
from services.usage_tracker import get_lambda_usage
from utils.alert import load_thresholds, check_thresholds


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

    ec2_hours = get_ec2_running_hours(region)
    print(f"\n🖥️  EC2 Running Hours: {ec2_hours} / 750 hours (Free Tier)")

    s3_gb = get_s3_storage_usage()
    print(f"📦  S3 Storage Used: {s3_gb} GB / 5 GB (Free Tier)")

    lambda_usage = get_lambda_usage(region)
    print(f"\n🧠 Lambda Compute Time: {lambda_usage} GB-seconds / 400,000 GB-sec (Free Tier)")

    
    rds_hours = get_rds_running_hours(region)
    print(f"🗃️  RDS usage: {rds_hours} hours")
    if rds_hours > 750:
        print("⚠️  Warning: RDS usage exceeds Free Tier limit (750 hours)")


        # Prepare usage data for report
    usage_data = {
        "EC2": f"{ec2_hours} / 750 hrs",
        "S3": f"{s3_gb:.2f} / 5 GB",
        "Lambda": f"{lambda_usage} / 400,000 GB-sec",
        "RDS": f"{rds_hours} / 750 hrs"
    }

    # Save reports
    save_reports(cost_data, total, usage_data)

    
# Load thresholds from config
    thresholds = load_thresholds()

# Run alert checks
    alerts = check_thresholds(usage_data, total, thresholds)

    print("\n🚨 Alert Summary:")
    if alerts:
        for a in alerts:
            print(a)
    else:
        print("✅ All usage within safe limits.")

    

        
        


    



if __name__ == "__main__":
    main()
