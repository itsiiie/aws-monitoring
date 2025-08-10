import boto3
from datetime import datetime, timezone, timedelta

def get_ec2_running_hours(region):
    ec2 = boto3.client('ec2', region_name=region)
    now = datetime.now(timezone.utc)

    response = ec2.describe_instances()
    total_hours = 0

    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            if instance['State']['Name'] == 'running':
                launch_time = instance['LaunchTime']
                run_time = now - launch_time
                hours = run_time.total_seconds() / 3600
                total_hours += hours

    return round(total_hours, 2)

def get_s3_storage_usage():
    s3 = boto3.client('s3')
    buckets = s3.list_buckets()['Buckets']
    total_size_bytes = 0

    for bucket in buckets:
        bucket_name = bucket['Name']
        try:
            # Get total size of all objects in the bucket
            paginator = s3.get_paginator('list_objects_v2')
            pages = paginator.paginate(Bucket=bucket_name)

            for page in pages:
                if 'Contents' in page:
                    for obj in page['Contents']:
                        total_size_bytes += obj['Size']
        except Exception as e:
            print(f"⚠️ Could not access bucket {bucket_name}: {e}")

    total_gb = round(total_size_bytes / (1024 ** 3), 2)
    return total_gb

def get_rds_running_hours(region):
    client = boto3.client('rds', region_name=region)
    total_hours = 0
    now = datetime.now(timezone.utc)

    response = client.describe_db_instances()
    for db in response['DBInstances']:
        if db['DBInstanceStatus'] == 'available':
            launch_time = db['InstanceCreateTime']
            hours = (now - launch_time).total_seconds() / 3600
            total_hours += hours

    return round(total_hours, 2)

def get_lambda_usage(region):
    client = boto3.client('cloudwatch', region_name=region)
    now = datetime.now(timezone.utc)
    start_time = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    end_time = now

    response = client.get_metric_statistics(
        Namespace='AWS/Lambda',
        MetricName='Duration',
        Dimensions=[
            {
                'Name': 'FunctionName',
                'Value': 'ALL'
            },
        ],
        StartTime=start_time,
        EndTime=end_time,
        Period=3600,
        Statistics=['Sum'],
        Unit='Milliseconds'
    )

    total_duration_ms = 0
    if 'Datapoints' in response:
        for datapoint in response['Datapoints']:
            total_duration_ms += datapoint['Sum']
    
    total_duration_sec = total_duration_ms / 1000
    compute_gb_seconds = total_duration_sec * 0.125
    
    return round(compute_gb_seconds, 2)
