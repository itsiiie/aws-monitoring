import os
import json
import csv
from datetime import datetime

def save_reports(cost_data, total_cost, usage_data, report_dir="reports"):
    os.makedirs(report_dir, exist_ok=True)
    date_str = datetime.now().strftime("%Y-%m-%d")
    
    # CSV report
    csv_path = os.path.join(report_dir, f"usage_report_{date_str}.csv")
    with open(csv_path, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Service", "Cost ($)"])
        for item in cost_data:
            writer.writerow([item["Service"], item["Cost"]])
        writer.writerow(["TOTAL", total_cost])
    
    # JSON report
    json_path = os.path.join(report_dir, f"usage_report_{date_str}.json")
    with open(json_path, "w") as jsonfile:
        json.dump({
            "date": date_str,
            "cost_data": cost_data,
            "total_cost": total_cost,
            "usage": usage_data
        }, jsonfile, indent=2)
    
    # Log file
    log_path = os.path.join(report_dir, "logs.txt")
    with open(log_path, "a") as logfile:
        logfile.write(f"[{date_str}] Total: ${total_cost} | Usage: {usage_data}\n")
