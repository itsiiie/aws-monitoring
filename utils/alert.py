import yaml

def load_thresholds():
    with open("config.yaml", "r") as f:
        config = yaml.safe_load(f)
    return config["thresholds"]

def check_thresholds(usage_data, total_cost, thresholds):
    alerts = []

    if usage_data["EC2"].split()[0] != "N/A":
        ec2 = float(usage_data["EC2"].split()[0])
        if ec2 > thresholds["ec2_hours"]:
            alerts.append("⚠️ EC2 usage exceeded threshold!")

    if usage_data["S3"].split()[0] != "N/A":
        s3 = float(usage_data["S3"].split()[0])
        if s3 > thresholds["s3_gb"]:
            alerts.append("⚠️ S3 usage exceeded threshold!")

    if usage_data["Lambda"].split()[0] != "N/A":
        lambda_use = float(usage_data["Lambda"].split()[0])
        if lambda_use > thresholds["lambda_gb_sec"]:
            alerts.append("⚠️ Lambda usage exceeded threshold!")

    if usage_data["RDS"].split()[0] != "N/A":
        rds = float(usage_data["RDS"].split()[0])
        if rds > thresholds["rds_hours"]:
            alerts.append("⚠️ RDS usage exceeded threshold!")

    if total_cost > thresholds["cost"]:
        alerts.append("⚠️ AWS billing exceeded threshold!")

    return alerts
