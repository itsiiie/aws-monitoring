import os
import json
import csv
from datetime import datetime

def save_reports(cost_data, total_cost, usage_data, alerts=None, report_dir="reports"):
    os.makedirs(report_dir, exist_ok=True)
    date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Save CSV report
    csv_path = os.path.join(report_dir, f"usage_report_{date_str[:10]}.csv")
    with open(csv_path, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Service", "Cost ($)"])
        for item in cost_data:
            writer.writerow([item[0], item[1]])
        writer.writerow(["TOTAL", total_cost])

    # Save dated JSON report
    json_path = os.path.join(report_dir, f"usage_report_{date_str[:10]}.json")
    with open(json_path, "w") as jsonfile:
        json.dump({
            "date": date_str,
            "cost_data": cost_data,
            "total_cost": total_cost,
            "usage": usage_data,
            "alerts": alerts or []
        }, jsonfile, indent=2)

    # Append to logs
    log_path = os.path.join(report_dir, "logs.txt")
    with open(log_path, "a") as logfile:
        logfile.write(f"[{date_str}] Total: ${total_cost:.2f} | Usage: {usage_data} | Alerts: {alerts or 'None'}\n")

    # Save latest usage-only report
    latest_usage_path = os.path.join(report_dir, "latest_usage_report.json")
    with open(latest_usage_path, "w") as f:
        json.dump(usage_data, f, indent=2)

    # Save latest cost-only report
    latest_cost_path = os.path.join(report_dir, "latest_cost_report.json")
    with open(latest_cost_path, "w") as f:
        json.dump({
            "cost_data": cost_data,
            "total": total_cost
        }, f, indent=2)

    # Save a full combined latest report (for dashboard)
    latest_combined_path = os.path.join(report_dir, "latest_report.json")
    with open(latest_combined_path, "w") as f:
        json.dump({
            "timestamp": date_str,
            "total_cost": total_cost,
            "cost_by_service": cost_data,
            "usage_data": usage_data,
            "alerts": alerts or []
        }, f, indent=2)
