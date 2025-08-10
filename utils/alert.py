import yaml

def load_thresholds():
    """
    Loads usage and cost thresholds from the config.yaml file.
    """
    try:
        with open("config.yaml", "r") as f:
            config = yaml.safe_load(f)
        return config.get("thresholds", {})
    except FileNotFoundError:
        print("❌ Error: config.yaml not found. Please ensure it exists.")
        return {}
    except yaml.YAMLError as e:
        print(f"❌ Error parsing config.yaml: {e}")
        return {}

def check_thresholds(usage_data, total_cost, thresholds):
    """
    Checks current AWS usage and total cost against predefined thresholds.

    Args:
        usage_data (dict): A dictionary containing current usage for various services
                           (e.g., EC2, S3, Lambda, RDS).
        total_cost (float): The current total estimated AWS cost.
        thresholds (dict): A dictionary containing the threshold values for each service
                           and the overall cost.

    Returns:
        list: A list of strings, where each string is an alert message for a breached threshold.
              Returns an empty list if no thresholds are breached.
    """
    alerts = []

    # Check EC2 usage
    ec2_usage_str = usage_data.get("EC2", "N/A").split()[0]
    if ec2_usage_str != "N/A" and "ec2_hours" in thresholds:
        try:
            ec2 = float(ec2_usage_str)
            if ec2 > thresholds["ec2_hours"]:
                alerts.append("⚠️ EC2 usage exceeded threshold!")
        except ValueError:
            print(f"⚠️ Could not parse EC2 usage: {ec2_usage_str}")

    # Check S3 usage
    s3_usage_str = usage_data.get("S3", "N/A").split()[0]
    if s3_usage_str != "N/A" and "s3_gb" in thresholds:
        try:
            s3 = float(s3_usage_str)
            if s3 > thresholds["s3_gb"]:
                alerts.append("⚠️ S3 usage exceeded threshold!")
        except ValueError:
            print(f"⚠️ Could not parse S3 usage: {s3_usage_str}")

    # Check Lambda usage
    lambda_usage_str = usage_data.get("Lambda", "N/A").split()[0]
    if lambda_usage_str != "N/A" and "lambda_gb_sec" in thresholds:
        try:
            lambda_use = float(lambda_usage_str)
            if lambda_use > thresholds["lambda_gb_sec"]:
                alerts.append("⚠️ Lambda usage exceeded threshold!")
        except ValueError:
            print(f"⚠️ Could not parse Lambda usage: {lambda_usage_str}")

    # Check RDS usage
    rds_usage_str = usage_data.get("RDS", "N/A").split()[0]
    if rds_usage_str != "N/A" and "rds_hours" in thresholds:
        try:
            rds = float(rds_usage_str)
            if rds > thresholds["rds_hours"]:
                alerts.append("⚠️ RDS usage exceeded threshold!")
        except ValueError:
            print(f"⚠️ Could not parse RDS usage: {rds_usage_str}")

    # Check total cost
    if "cost" in thresholds and total_cost > thresholds["cost"]:
        alerts.append(f"⚠️ AWS billing exceeded threshold! Current: ${total_cost:.2f}, Threshold: ${thresholds['cost']:.2f}")

    return alerts
